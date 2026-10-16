-- Local test of parents.sql on plain Postgres (run after test_schema.sql and test_tracking.sql, in the same database).
-- Run:  tests/run_supabase_test.sh
\set ON_ERROR_STOP on
\set QUIET on

-- Supabase stand-in: the claims of the logged-in user (amr = how they logged in)
create or replace function auth.jwt() returns jsonb language sql stable as
  $$ select coalesce(nullif(current_setting('request.jwt.claims', true), ''), '{}')::jsonb $$;
grant execute on function auth.jwt() to anon, authenticated;

\ir parents.sql
\ir parents.sql
-- re-running the other files must not break the parents' view
\ir schema.sql
\ir tracking.sql

insert into auth.users (id, email) values
  ('30000000-0000-0000-0000-000000000001', 'Mom@X.com'),
  ('30000000-0000-0000-0000-000000000002', 'dad@x.com'),
  ('30000000-0000-0000-0000-000000000003', 'stranger@x.com');
insert into public.kid_parents (kid_id, email) values
  ('10000000-0000-0000-0000-000000000001', 'mom@x.com'),
  ('10000000-0000-0000-0000-000000000002', 'mom@x.com'),
  ('10000000-0000-0000-0000-000000000001', 'dad@x.com');
insert into public.activity (id, kid_id, page_type, page_key, title, active_seconds) values
  (gen_random_uuid(), '10000000-0000-0000-0000-000000000001', 'lesson', 'lessons/a', 'Lesson A', 300),
  (gen_random_uuid(), '10000000-0000-0000-0000-000000000002', 'quran', 'games/citaj-kuran', 'Read Along', 600),
  (gen_random_uuid(), '10000000-0000-0000-0000-000000000003', 'game', 'games/x', 'Somebody else', 900);
select t.expect_error($$insert into public.kid_parents (kid_id, email) values ('10000000-0000-0000-0000-000000000001', 'Not An Email')$$, 'e-mail must be lower case and valid');

-- ---------------------------------------------------------- a parent who logged in with a code
begin; set local role authenticated;
select set_config('request.jwt.claim.sub', '30000000-0000-0000-0000-000000000001', true);
select set_config('request.jwt.claims', '{"amr": [{"method": "otp", "timestamp": 1}]}', true);
select t.check(jsonb_array_length(public.my_children()) = 2, 'mother sees her two children (e-mail matched without case)');
select t.check(public.my_children() -> 0 ->> 'class_code' is not null, 'parent sees the class code of the child''s group');
select t.check(jsonb_array_length(public.my_children_activity(now() - interval '1 day', now() + interval '1 day')) = 2, 'mother sees only her children''s visits');
select t.check(public.my_children_activity(now() - interval '1 day', now() + interval '1 day')::text !~ 'Somebody else', 'another family''s visits are not there');
select t.expect_error($$select public.my_children_activity(now(), now() - interval '1 day')$$, 'backwards date range');
select t.check((select count(*) from public.kid_parents) = 0, 'parent cannot read the e-mail list');
select t.check((select count(*) from public.activity) = 0, 'parent cannot read the activity table directly');
select t.check((select count(*) from public.kids) = 0, 'parent cannot read the children table directly');
select t.expect_error($$insert into public.kid_parents (kid_id, email) values ('10000000-0000-0000-0000-000000000003', 'mom@x.com')$$, 'parent links another child to herself');
commit;

-- ---------------------------------------------------------- same e-mail, but logged in with a password
begin; set local role authenticated;
select set_config('request.jwt.claim.sub', '30000000-0000-0000-0000-000000000001', true);
select set_config('request.jwt.claims', '{"amr": [{"method": "password", "timestamp": 1}]}', true);
select t.check(public.my_children() is null, 'a password login (e.g. a game account with her e-mail) sees nothing');
select t.check(public.my_children_activity(now() - interval '1 day', now() + interval '1 day') is null, '… and no activity');
commit;

-- ---------------------------------------------------------- other parents
begin; set local role authenticated;
select set_config('request.jwt.claim.sub', '30000000-0000-0000-0000-000000000002', true);
select set_config('request.jwt.claims', '{"amr": [{"method": "magiclink", "timestamp": 1}]}', true);
select t.check(jsonb_array_length(public.my_children()) = 1, 'father (e-mail link) sees the one child linked to his e-mail');
commit;
begin; set local role authenticated;
select set_config('request.jwt.claim.sub', '30000000-0000-0000-0000-000000000003', true);
select set_config('request.jwt.claims', '{"amr": [{"method": "otp", "timestamp": 1}]}', true);
select t.check(jsonb_array_length(public.my_children()) = 0, 'an unknown e-mail sees no children');
commit;
begin; set local role anon;
select t.expect_error($$select public.my_children()$$, 'anonymous visitor asks for children');
commit;

-- ---------------------------------------------------------- the teacher links e-mails
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000000b', true);
insert into public.kid_parents (kid_id, email) values ('10000000-0000-0000-0000-000000000003', 'stranger@x.com');
select t.check((select count(*) from public.kid_parents) = 4, 'listed teacher sees and adds parent e-mails');
delete from public.kid_parents where email = 'stranger@x.com';
commit;
select t.check((select count(*) from public.kid_parents) = 3, 'listed teacher removes a parent e-mail');

\echo ALL PARENTS TESTS PASSED
