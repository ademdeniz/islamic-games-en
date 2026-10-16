-- Who opened what, and for how long – database setup for the same Supabase project.
-- Run once in Supabase: Dashboard → SQL Editor → New query → paste this whole file → Run.
-- Needs schema.sql first (public.my_role()). Safe to re-run, and it keeps working if schema.sql is re-run later.
--
-- Children have no accounts. On a new device a child types the class code of their group, taps their name and,
-- if the group uses one, their 3-picture PIN (chosen the first time). The device then keeps a secret token, and the
-- pages send "this child spent N active seconds on this page" with it. The children, codes and activity can only be
-- read by the admin and the accounts listed in activity_viewers (the teacher dashboard at teacher/).
--
-- Let a teacher see the dashboard (with their e-mail):
--   insert into public.activity_viewers (user_id) select id from auth.users where email = 'you@example.com' on conflict do nothing;

create extension if not exists pgcrypto;

-- ------------------------------------------------------------------ tables
create table if not exists public.class_groups (
  id           text primary key check (id ~ '^[a-z0-9]{1,10}$'),     -- g1, g2 (the ids in data/plan/plan.json)
  name         text not null check (length(name) between 1 and 40),
  code         text not null unique check (code ~ '^[A-Z0-9]{4,12}$'),
  pin_required boolean not null default false,
  updated_at   timestamptz not null default now()
);

create table if not exists public.kids (
  id         uuid primary key default gen_random_uuid(),
  group_id   text not null references public.class_groups(id) on update cascade,
  first_name text not null check (length(trim(first_name)) between 1 and 40),
  last_name  text not null default '' check (length(last_name) <= 40),
  pin        text check (pin ~ '^[0-8]{3}$'),                         -- 3 pictures, chosen by the child the first time
  active     boolean not null default true,                           -- false = left the maktab (kept for the history)
  created_at timestamptz not null default now()
);

create table if not exists public.kid_devices (                       -- a device a child signed in on
  token_hash text primary key,                                        -- sha256 of the secret kept in that browser
  kid_id     uuid not null references public.kids(id) on delete cascade,
  created_at timestamptz not null default now(),
  last_seen  timestamptz not null default now()
);
create index if not exists kid_devices_kid on public.kid_devices (kid_id);

create table if not exists public.activity (                          -- one row per visit of one page
  id             uuid primary key,                                    -- made by the page
  kid_id         uuid not null references public.kids(id) on delete cascade,
  page_type      text not null check (page_type in ('lesson', 'sufara', 'quran', 'surah', 'game')),
  page_key       text not null check (length(page_key) between 1 and 160),
  title          text not null default '' check (length(title) <= 160),
  started_at     timestamptz not null default now(),
  last_seen      timestamptz not null default now(),
  active_seconds int  not null default 0 check (active_seconds between 0 and 86400)
);
create index if not exists activity_kid_time on public.activity (kid_id, started_at desc);
create index if not exists activity_time on public.activity (started_at desc);

create table if not exists public.activity_viewers (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  created_at timestamptz not null default now()
);

-- ------------------------------------------------------------------ who may see it
create or replace function public.can_see_activity() returns boolean
language sql stable security definer set search_path = public as $$
  select auth.uid() is not null and (public.my_role() = 'admin'
         or exists (select 1 from public.activity_viewers where user_id = auth.uid()))
$$;

alter table public.class_groups     enable row level security;
alter table public.kids             enable row level security;
alter table public.kid_devices      enable row level security;
alter table public.activity         enable row level security;
alter table public.activity_viewers enable row level security;

drop policy if exists "teacher manages groups" on public.class_groups;
create policy "teacher manages groups" on public.class_groups for all to authenticated
  using (public.can_see_activity()) with check (public.can_see_activity());
drop policy if exists "teacher manages kids" on public.kids;
create policy "teacher manages kids" on public.kids for all to authenticated
  using (public.can_see_activity()) with check (public.can_see_activity());
drop policy if exists "teacher sees devices" on public.kid_devices;
create policy "teacher sees devices" on public.kid_devices for select to authenticated using (public.can_see_activity());
drop policy if exists "teacher signs out devices" on public.kid_devices;
create policy "teacher signs out devices" on public.kid_devices for delete to authenticated using (public.can_see_activity());
drop policy if exists "teacher sees activity" on public.activity;
create policy "teacher sees activity" on public.activity for select to authenticated using (public.can_see_activity());
drop policy if exists "teacher deletes activity" on public.activity;
create policy "teacher deletes activity" on public.activity for delete to authenticated using (public.can_see_activity());

revoke all on public.class_groups, public.kids, public.kid_devices, public.activity, public.activity_viewers
  from anon, authenticated;
grant select, insert, update, delete on public.class_groups, public.kids to authenticated;
grant select, delete on public.kid_devices, public.activity to authenticated;

-- ------------------------------------------------------------------ what the pages may call (no login)
create or replace function public.kid_label(k public.kids) returns text
language sql immutable as $$
  select k.first_name || case when k.last_name <> '' then ' ' || upper(left(k.last_name, 1)) || '.' else '' end
$$;

-- Class code → the group's names (first name + last initial only).
create or replace function public.join_class(p_code text) returns jsonb
language plpgsql stable security definer set search_path = public as $$
declare g public.class_groups;
begin
  select * into g from public.class_groups where code = upper(regexp_replace(coalesce(p_code, ''), '\s', '', 'g'));
  if g.id is null then raise exception 'That class code is not right. Ask your teacher.'; end if;
  return jsonb_build_object('group', g.id, 'group_name', g.name, 'pin_required', g.pin_required,
    'kids', coalesce((select jsonb_agg(jsonb_build_object('id', k.id, 'name', public.kid_label(k), 'has_pin', k.pin is not null)
                                       order by k.first_name, k.last_name)
                        from public.kids k where k.group_id = g.id and k.active), '[]'::jsonb));
end $$;

-- Code + name (+ PIN) → a secret token for this device.
create or replace function public.sign_in_kid(p_code text, p_kid uuid, p_pin text) returns jsonb
language plpgsql security definer set search_path = public as $$
declare g public.class_groups; k public.kids; tok text; new_pin boolean := false;
begin
  select * into g from public.class_groups where code = upper(regexp_replace(coalesce(p_code, ''), '\s', '', 'g'));
  if g.id is null then raise exception 'That class code is not right. Ask your teacher.'; end if;
  select * into k from public.kids where id = p_kid and group_id = g.id and active;
  if k.id is null then raise exception 'That name is not in this class.'; end if;
  if g.pin_required then
    if coalesce(p_pin, '') !~ '^[0-8]{3}$' then raise exception 'Tap your 3 pictures.'; end if;
    if k.pin is null then
      update public.kids set pin = p_pin where id = k.id;
      new_pin := true;
    elsif k.pin <> p_pin then
      raise exception 'Those pictures are not right. Try again or ask your teacher.';
    end if;
  end if;
  tok := encode(gen_random_bytes(24), 'hex');
  insert into public.kid_devices (token_hash, kid_id) values (encode(digest(tok, 'sha256'), 'hex'), k.id);
  return jsonb_build_object('token', tok, 'name', public.kid_label(k), 'group', g.id, 'new_pin', new_pin);
end $$;

-- "This child spent p_seconds more on this page." Returns false if the device was signed out by the teacher.
create or replace function public.track_visit(p_token text, p_visit uuid, p_type text, p_key text, p_title text,
                                              p_seconds int) returns boolean
language plpgsql security definer set search_path = public as $$
declare kid uuid;
begin
  update public.kid_devices set last_seen = now()
   where token_hash = encode(digest(coalesce(p_token, ''), 'sha256'), 'hex')
   returning kid_id into kid;
  if kid is null then return false; end if;
  if p_visit is null or coalesce(p_type, '') not in ('lesson', 'sufara', 'quran', 'surah', 'game')
     or length(coalesce(p_key, '')) not between 1 and 160 then
    raise exception 'Bad visit.';
  end if;
  insert into public.activity as a (id, kid_id, page_type, page_key, title, active_seconds)
  values (p_visit, kid, p_type, p_key, left(coalesce(p_title, ''), 160), least(greatest(coalesce(p_seconds, 0), 0), 120))
  on conflict (id) do update
    set active_seconds = least(a.active_seconds + excluded.active_seconds, 86400), last_seen = now()
    where a.kid_id = excluded.kid_id;
  return true;
end $$;

revoke execute on function public.can_see_activity(), public.join_class(text), public.sign_in_kid(text, uuid, text),
  public.track_visit(text, uuid, text, text, text, int) from public;
grant execute on function public.can_see_activity() to authenticated;
grant execute on function public.join_class(text), public.sign_in_kid(text, uuid, text),
  public.track_visit(text, uuid, text, text, text, int) to anon, authenticated;
