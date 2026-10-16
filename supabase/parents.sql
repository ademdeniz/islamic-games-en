-- Parents see their own children's activity – database setup for the same Supabase project.
-- Run once in Supabase: Dashboard → SQL Editor → New query → paste this whole file → Run.
-- Needs schema.sql and tracking.sql first. Safe to re-run.
--
-- A parent logs in on parents/ with their e-mail and a 6-digit code (or the button in the e-mail). kid_parents says which
-- e-mails belong to which child (from the registration form; the teacher can change it on teacher/). A parent only ever
-- sees the children linked to their e-mail, and only after logging in with a code or link from that inbox – never with a
-- password, so a game account made with someone else's e-mail address cannot see their children.

create table if not exists public.kid_parents (
  kid_id uuid not null references public.kids(id) on delete cascade,
  email  text not null check (email = lower(trim(email)) and email ~ '^[^@\s]+@[^@\s]+\.[^@\s]+$'),
  primary key (kid_id, email)
);
create index if not exists kid_parents_email on public.kid_parents (email);

alter table public.kid_parents enable row level security;
drop policy if exists "teacher manages parents" on public.kid_parents;
create policy "teacher manages parents" on public.kid_parents for all to authenticated
  using (public.can_see_activity()) with check (public.can_see_activity());
revoke all on public.kid_parents from anon, authenticated;
grant select, insert, delete on public.kid_parents to authenticated;

-- The logged-in parent's e-mail – only when this login came from their inbox (code or e-mail link), not a password.
create or replace function public.parent_email() returns text
language plpgsql stable security definer set search_path = public as $$
declare e text;
begin
  if auth.uid() is null then return null; end if;
  if not exists (select 1 from jsonb_array_elements(coalesce(auth.jwt() -> 'amr', '[]'::jsonb)) a
                  where a ->> 'method' in ('otp', 'magiclink', 'email/signup', 'recovery')) then
    return null;
  end if;
  select lower(u.email) into e from auth.users u where u.id = auth.uid();
  return e;
end $$;

create or replace function public.my_children() returns jsonb
language plpgsql stable security definer set search_path = public as $$
declare e text := public.parent_email();
begin
  if e is null then return null; end if;   -- not logged in with a code
  return coalesce((
    select jsonb_agg(jsonb_build_object('id', k.id, 'first_name', k.first_name, 'last_name', k.last_name,
             'group', g.name, 'class_code', g.code, 'pin_required', g.pin_required,
             'devices', (select count(*) from public.kid_devices d where d.kid_id = k.id))
           order by k.first_name)
      from public.kids k join public.class_groups g on g.id = k.group_id
     where k.id in (select kid_id from public.kid_parents where email = e)), '[]'::jsonb);
end $$;

create or replace function public.my_children_activity(p_from timestamptz, p_to timestamptz) returns jsonb
language plpgsql stable security definer set search_path = public as $$
declare e text := public.parent_email();
begin
  if e is null then return null; end if;
  if p_from is null or p_to is null or p_to <= p_from or p_to - p_from > interval '400 days' then
    raise exception 'Bad date range.';
  end if;
  return coalesce((
    select jsonb_agg(jsonb_build_object('kid_id', a.kid_id, 'page_type', a.page_type, 'title', a.title,
             'started_at', a.started_at, 'active_seconds', a.active_seconds) order by a.started_at)
      from public.activity a
     where a.kid_id in (select kid_id from public.kid_parents where email = e)
       and a.started_at >= p_from and a.started_at < p_to), '[]'::jsonb);
end $$;

revoke execute on function public.parent_email(), public.my_children(), public.my_children_activity(timestamptz, timestamptz)
  from public, anon;
grant execute on function public.parent_email(), public.my_children(), public.my_children_activity(timestamptz, timestamptz)
  to authenticated;
