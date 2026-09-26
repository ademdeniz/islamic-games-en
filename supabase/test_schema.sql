-- Local test of schema.sql on plain Postgres with a minimal stand-in for Supabase's auth schema and roles.
-- Run:  tests/run_supabase_test.sh   (starts a throwaway Postgres in Docker)
\set ON_ERROR_STOP on
\set QUIET on

-- ---------------------------------------------------------- Supabase stand-ins
do $$ begin create role anon nologin; exception when duplicate_object then null; end $$;
do $$ begin create role authenticated nologin; exception when duplicate_object then null; end $$;
create schema auth;
create table auth.users (id uuid primary key default gen_random_uuid(), email text, raw_user_meta_data jsonb);
create function auth.uid() returns uuid language sql stable as
  $$ select nullif(current_setting('request.jwt.claim.sub', true), '')::uuid $$;
grant usage on schema public, auth to anon, authenticated;
grant execute on function auth.uid() to anon, authenticated;
-- Supabase grants everything on new public tables to anon/authenticated by default; RLS + our revokes must hold anyway.
alter default privileges in schema public grant all on tables to anon, authenticated;

-- helpers for the test
create schema t;
grant usage on schema t to anon, authenticated;
create function t.expect_error(q text, why text) returns void language plpgsql as $$
begin
  begin execute q; exception when others then raise notice 'ok (blocked): %  [%]', why, sqlerrm; return; end;
  raise exception 'SECURITY HOLE – this should have failed: %', why;
end $$;
grant execute on function t.expect_error(text, text) to anon, authenticated;
create function t.check(ok boolean, what text) returns void language plpgsql as $$
begin if not ok then raise exception 'FAILED: %', what; end if; raise notice 'ok: %', what; end $$;
grant execute on function t.check(boolean, text) to anon, authenticated;

-- ---------------------------------------------------------- install twice (must be re-runnable)
\ir schema.sql
\ir schema.sql

-- ---------------------------------------------------------- users sign up
insert into auth.users (id, email, raw_user_meta_data) values
  ('00000000-0000-0000-0000-00000000000a', 'admin@x', '{"full_name":"Adem Admin"}'),
  ('00000000-0000-0000-0000-00000000000b', 'teacher@x', '{"full_name":"Teacher Tarik"}'),
  ('00000000-0000-0000-0000-000000000001', 's1@x', '{"full_name":"Student Sara"}'),
  ('00000000-0000-0000-0000-000000000002', 's2@x', '{"full_name":"Student Emir"}');
select t.check((select count(*) from public.profiles) = 4, 'signup creates a profile for every new account');
select t.check((select full_name from public.profiles where id = '00000000-0000-0000-0000-000000000001') = 'Student Sara', 'profile keeps the full name');
select t.check((select count(*) from public.profiles where role = 'ucenik') = 4, 'everyone starts as a student');
update public.profiles set role = 'admin' where id = (select id from auth.users where email = 'admin@x');

-- ---------------------------------------------------------- nobody can promote themselves
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-000000000001', true);
select t.expect_error($$update public.profiles set role = 'admin' where id = auth.uid()$$, 'student makes self admin');
select t.expect_error($$insert into public.teacher_students values (auth.uid(), '00000000-0000-0000-0000-00000000000b')$$, 'student links self to a teacher directly');
select t.expect_error($$select public.approve_teacher('00000000-0000-0000-0000-000000000001')$$, 'student approves self as teacher');
select t.check((select count(*) from public.profiles) = 1, 'student sees only their own profile');
commit;

-- ---------------------------------------------------------- teacher request → admin approves
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000000b', true);
select public.request_teacher();
commit;
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000000a', true);
select t.check((select count(*) from public.profiles where teacher_status = 'pending') = 1, 'admin sees the pending teacher request');
select public.approve_teacher('00000000-0000-0000-0000-00000000000b');
commit;
select t.check((select role = 'mualim' and teacher_code ~ '^[A-Z2-9]{6}$' from public.profiles where id = '00000000-0000-0000-0000-00000000000b'), 'approved teacher gets role mualim and a 6-character code');

-- ---------------------------------------------------------- student joins with the code (lower case, spaces)
select set_config('my.code', (select teacher_code from public.profiles where id = '00000000-0000-0000-0000-00000000000b'), false);
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-000000000001', true);
select t.expect_error($$select public.join_teacher('NOPE00')$$, 'join with a wrong code');
select public.join_teacher('  ' || lower(current_setting('my.code')) || ' ');
select public.join_teacher(current_setting('my.code'));  -- second click must not duplicate
select t.check((select count(*) from public.student_requests) = 1, 'one pending request, no duplicates');
select t.expect_error($$insert into public.quiz_attempts (student_id, teacher_id, question_count, correct_count, wrong_count, score, percentage)
  values (auth.uid(), '00000000-0000-0000-0000-00000000000b', 30, 5, 25, 1000, 16.67)$$, 'save a result before the teacher accepted');
commit;

-- ---------------------------------------------------------- teacher sees the request with the student's name, accepts
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000000b', true);
select t.check((select p.full_name from public.student_requests r join public.profiles p on p.id = r.student_id
                 where r.teacher_id = auth.uid() and r.status = 'pending') = 'Student Sara', 'teacher sees the requesting student''s name');
select public.decide_student_request((select id from public.student_requests limit 1), true);
commit;
select t.check((select teacher_id from public.teacher_students where student_id = '00000000-0000-0000-0000-000000000001') = '00000000-0000-0000-0000-00000000000b', 'student is now linked to the teacher');

-- ---------------------------------------------------------- student saves a quiz result (what saveAttempt() does)
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-000000000001', true);
-- two separate requests, like the game: insert the attempt (returning id), then its answers
with a as (insert into public.quiz_attempts (student_id, teacher_id, question_count, correct_count, wrong_count, score, percentage, started_at)
           values (auth.uid(), public.my_teacher(), 30, 12, 18, 4000, 40, now() - interval '5 min') returning id)
select set_config('my.attempt', id::text, true) from a;
insert into public.quiz_answers (attempt_id, question_key, level, selected_answer, correct_answer, is_correct)
values (current_setting('my.attempt')::uuid, 'q1', 'A1', 'Abdullah', 'Abdullah', true);
select t.check((select count(*) from public.quiz_attempts) = 1, 'student sees their own saved result');
select t.expect_error($$insert into public.quiz_attempts (student_id, teacher_id, question_count, correct_count, wrong_count, score, percentage)
  values ('00000000-0000-0000-0000-000000000002', public.my_teacher(), 30, 30, 0, 1000000, 100)$$, 'save a result in another student''s name');
select t.expect_error($$update public.quiz_attempts set score = 1000000$$, 'change a saved score');
commit;

-- ---------------------------------------------------------- teacher sees results + names; other student sees nothing
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000000b', true);
select t.check((select count(*) from public.quiz_attempts a join public.profiles p on p.id = a.student_id where a.teacher_id = auth.uid()) = 1, 'teacher sees the student''s result with name');
select t.check((select count(*) from public.quiz_answers) = 1, 'teacher sees the student''s answers');
commit;
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-000000000002', true);
select t.check((select count(*) from public.quiz_attempts) = 0, 'another student cannot see Sara''s results');
select t.check((select count(*) from public.profiles) = 1, 'another student sees only their own profile');
select t.expect_error($$select public.decide_student_request((select id from public.student_requests limit 1), true)$$, 'student decides a teacher''s request');
commit;

-- ---------------------------------------------------------- logged-out visitors get nothing
begin; set local role anon;
select t.expect_error($$select count(*) from public.profiles$$, 'anonymous visitor reads profiles');
select t.expect_error($$select count(*) from public.quiz_attempts$$, 'anonymous visitor reads results');
select t.expect_error($$select public.join_teacher('X')$$, 'anonymous visitor calls a function');
commit;

\echo ALL SUPABASE SCHEMA TESTS PASSED
