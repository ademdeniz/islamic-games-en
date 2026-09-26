-- Islamic Millionaire (online) – database setup for your own Supabase project.
-- Run once in Supabase: Dashboard → SQL Editor → New query → paste this whole file → Run.
-- Safe to re-run: it creates things only if they don't exist yet and replaces the functions.
--
-- Roles:  ucenik = student (everyone starts here) · mualim = teacher (approved by an admin) · admin
-- Flow:   student asks to become a teacher → admin approves → teacher gets a code →
--         students send a request with that code → teacher accepts → the student's quiz results reach the teacher.

create extension if not exists pgcrypto;

-- ------------------------------------------------------------------ tables
create table if not exists public.profiles (
  id             uuid primary key references auth.users(id) on delete cascade,
  full_name      text not null default '',
  role           text not null default 'ucenik' check (role in ('ucenik', 'mualim', 'admin')),
  teacher_status text check (teacher_status in ('pending', 'approved', 'rejected')),
  teacher_code   text unique,
  created_at     timestamptz not null default now()
);

create table if not exists public.teacher_students (           -- one teacher per student
  student_id uuid primary key references public.profiles(id) on delete cascade,
  teacher_id uuid not null references public.profiles(id) on delete cascade,
  created_at timestamptz not null default now()
);

create table if not exists public.student_requests (
  id         uuid primary key default gen_random_uuid(),
  student_id uuid not null references public.profiles(id) on delete cascade,  -- FK name: student_requests_student_id_fkey
  teacher_id uuid not null references public.profiles(id) on delete cascade,
  status     text not null default 'pending' check (status in ('pending', 'accepted', 'rejected')),
  created_at timestamptz not null default now()
);
create unique index if not exists student_requests_one_pending
  on public.student_requests (student_id, teacher_id) where status = 'pending';

create table if not exists public.quiz_attempts (
  id             uuid primary key default gen_random_uuid(),
  student_id     uuid not null references public.profiles(id) on delete cascade,  -- FK name: quiz_attempts_student_id_fkey
  teacher_id     uuid not null references public.profiles(id) on delete cascade,
  question_count int  not null check (question_count between 1 and 100),
  correct_count  int  not null check (correct_count >= 0),
  wrong_count    int  not null check (wrong_count >= 0),
  score          int  not null check (score >= 0),
  percentage     numeric(5, 2) not null check (percentage between 0 and 100),
  started_at     timestamptz,
  finished_at    timestamptz not null default now()
);
create index if not exists quiz_attempts_teacher on public.quiz_attempts (teacher_id, finished_at desc);

create table if not exists public.quiz_answers (
  id              bigint generated always as identity primary key,
  attempt_id      uuid not null references public.quiz_attempts(id) on delete cascade,
  question_key    text,
  level           text,
  selected_answer text,
  correct_answer  text,
  is_correct      boolean not null
);

-- ------------------------------------------------------------------ new account → profile
create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, full_name)
  values (new.id, left(coalesce(new.raw_user_meta_data ->> 'full_name', ''), 80))
  on conflict (id) do nothing;
  return new;
end $$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();

-- ------------------------------------------------------------------ helpers (bypass RLS safely, no recursion)
create or replace function public.my_role() returns text
language sql stable security definer set search_path = public as $$
  select role from public.profiles where id = auth.uid()
$$;

create or replace function public.my_teacher() returns uuid
language sql stable security definer set search_path = public as $$
  select teacher_id from public.teacher_students where student_id = auth.uid()
$$;

-- ------------------------------------------------------------------ actions (the only way to change roles/links)
create or replace function public.request_teacher() returns void
language plpgsql security definer set search_path = public as $$
begin
  update public.profiles set teacher_status = 'pending'
   where id = auth.uid() and role = 'ucenik' and teacher_status is distinct from 'pending';
  if not found then raise exception 'You can’t send this request right now.'; end if;
end $$;

create or replace function public.approve_teacher(p_user uuid) returns void
language plpgsql security definer set search_path = public as $$
declare code text;
begin
  if public.my_role() is distinct from 'admin' then raise exception 'Only an administrator can do this.'; end if;
  loop  -- 6-character code without look-alike letters (0/O, 1/I)
    code := (select string_agg(substr('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', 1 + floor(random() * 32)::int, 1), '')
               from generate_series(1, 6));
    exit when not exists (select 1 from public.profiles where teacher_code = code);
  end loop;
  update public.profiles
     set role = 'mualim', teacher_status = 'approved', teacher_code = coalesce(teacher_code, code)
   where id = p_user and role = 'ucenik';
  delete from public.teacher_students where student_id = p_user;
  update public.student_requests set status = 'rejected' where student_id = p_user and status = 'pending';
end $$;

create or replace function public.reject_teacher(p_user uuid) returns void
language plpgsql security definer set search_path = public as $$
begin
  if public.my_role() is distinct from 'admin' then raise exception 'Only an administrator can do this.'; end if;
  update public.profiles set teacher_status = 'rejected' where id = p_user and teacher_status = 'pending';
end $$;

create or replace function public.join_teacher(p_code text) returns void
language plpgsql security definer set search_path = public as $$
declare t uuid;
begin
  if public.my_role() is distinct from 'ucenik' then raise exception 'Only students can join a mu’allim.'; end if;
  if public.my_teacher() is not null then raise exception 'You already have a mu’allim.'; end if;
  select id into t from public.profiles
   where role = 'mualim' and teacher_code = upper(trim(coalesce(p_code, '')));
  if t is null then raise exception 'No mu’allim found with that code.'; end if;
  insert into public.student_requests (student_id, teacher_id) values (auth.uid(), t)
    on conflict do nothing;
end $$;

create or replace function public.decide_student_request(p_request uuid, p_accept boolean) returns void
language plpgsql security definer set search_path = public as $$
declare r public.student_requests;
begin
  select * into r from public.student_requests
   where id = p_request and teacher_id = auth.uid() and status = 'pending';
  if r.id is null then raise exception 'Request not found.'; end if;
  update public.student_requests set status = case when p_accept then 'accepted' else 'rejected' end
   where id = r.id;
  if p_accept then
    insert into public.teacher_students (student_id, teacher_id) values (r.student_id, r.teacher_id)
      on conflict (student_id) do update set teacher_id = excluded.teacher_id, created_at = now();
    update public.student_requests set status = 'rejected'
     where student_id = r.student_id and status = 'pending' and id <> r.id;
  end if;
end $$;

-- ------------------------------------------------------------------ row level security
alter table public.profiles         enable row level security;
alter table public.teacher_students enable row level security;
alter table public.student_requests enable row level security;
alter table public.quiz_attempts    enable row level security;
alter table public.quiz_answers     enable row level security;

drop policy if exists "read profiles" on public.profiles;
create policy "read profiles" on public.profiles for select to authenticated using (
  id = auth.uid()
  or public.my_role() = 'admin'
  or exists (select 1 from public.teacher_students ts where ts.teacher_id = auth.uid() and ts.student_id = profiles.id)
  or exists (select 1 from public.student_requests sr where sr.teacher_id = auth.uid() and sr.student_id = profiles.id)
);

drop policy if exists "read own links" on public.teacher_students;
create policy "read own links" on public.teacher_students for select to authenticated
  using (student_id = auth.uid() or teacher_id = auth.uid());

drop policy if exists "read own requests" on public.student_requests;
create policy "read own requests" on public.student_requests for select to authenticated
  using (student_id = auth.uid() or teacher_id = auth.uid());

drop policy if exists "read attempts" on public.quiz_attempts;
create policy "read attempts" on public.quiz_attempts for select to authenticated
  using (student_id = auth.uid() or teacher_id = auth.uid());

drop policy if exists "student saves own attempt" on public.quiz_attempts;
create policy "student saves own attempt" on public.quiz_attempts for insert to authenticated
  with check (student_id = auth.uid() and teacher_id = public.my_teacher() and public.my_role() = 'ucenik');

drop policy if exists "read answers" on public.quiz_answers;
create policy "read answers" on public.quiz_answers for select to authenticated using (
  exists (select 1 from public.quiz_attempts a where a.id = attempt_id
          and (a.student_id = auth.uid() or a.teacher_id = auth.uid())));

drop policy if exists "student saves own answers" on public.quiz_answers;
create policy "student saves own answers" on public.quiz_answers for insert to authenticated with check (
  exists (select 1 from public.quiz_attempts a where a.id = attempt_id and a.student_id = auth.uid()));

-- Nobody can update or delete rows directly; role and link changes only happen through the functions above.
revoke all on all tables in schema public from anon;
revoke insert, update, delete on public.profiles, public.teacher_students, public.student_requests from authenticated;
revoke update, delete, truncate on public.quiz_attempts, public.quiz_answers from authenticated;
grant select on public.profiles, public.teacher_students, public.student_requests to authenticated;
grant select, insert on public.quiz_attempts, public.quiz_answers to authenticated;

revoke execute on function public.request_teacher(), public.approve_teacher(uuid), public.reject_teacher(uuid),
  public.join_teacher(text), public.decide_student_request(uuid, boolean), public.my_role(), public.my_teacher(),
  public.handle_new_user() from public, anon;
grant execute on function public.request_teacher(), public.approve_teacher(uuid), public.reject_teacher(uuid),
  public.join_teacher(text), public.decide_student_request(uuid, boolean), public.my_role(), public.my_teacher()
  to authenticated;

-- ------------------------------------------------------------------ make yourself the admin
-- After you have signed up once in the game, run this (with your e-mail) in the SQL Editor:
--   update public.profiles set role = 'admin'
--    where id = (select id from auth.users where email = 'you@example.com');
