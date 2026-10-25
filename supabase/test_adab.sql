-- Local test of adab.sql (run after test_schema.sql and test_tracking.sql, in the same database).
-- Run:  tests/run_supabase_test.sh
\set ON_ERROR_STOP on
\set QUIET on

\ir adab.sql
\ir adab.sql
-- re-running the other files must not break the rubric
\ir tracking.sql

-- ---------------------------------------------------------- the teacher scores after class
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000000b', true);
insert into public.adab (kid_id, day, listen, phone) values ('10000000-0000-0000-0000-000000000001', '2026-10-25', 3, 1);
insert into public.adab (kid_id, day, turn) values ('10000000-0000-0000-0000-000000000001', '2026-10-25', 2)
  on conflict (kid_id, day) do update set turn = excluded.turn;
insert into public.adab (kid_id, day, absent) values ('10000000-0000-0000-0000-000000000002', '2026-10-25', true);
select t.check((select (listen, turn, phone) = (3::smallint, 2::smallint, 1::smallint) from public.adab where kid_id = '10000000-0000-0000-0000-000000000001'),
  'a second tap on another point keeps the first ones');
update public.adab set listen = null where kid_id = '10000000-0000-0000-0000-000000000001';
select t.check((select listen is null from public.adab where kid_id = '10000000-0000-0000-0000-000000000001'), 'teacher clears a score');
select t.expect_error($$insert into public.adab (kid_id, day, listen) values ('10000000-0000-0000-0000-000000000002', '2026-10-18', 4)$$, 'a score of 4');
select t.expect_error($$insert into public.adab (kid_id, day, respect) values ('10000000-0000-0000-0000-000000000002', '2026-10-18', 0)$$, 'a score of 0');
select t.expect_error($$insert into public.adab (kid_id, day, note) values ('10000000-0000-0000-0000-000000000002', '2026-10-18', repeat('x', 301))$$, 'a note longer than 300');
select t.check((select count(*) from public.adab) = 2, 'listed teacher sees the scores');
commit;

-- ---------------------------------------------------------- nobody else
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-000000000001', true);
select t.check((select count(*) from public.adab) = 0, 'a student cannot see the scores');
select t.expect_error($$insert into public.adab (kid_id, day, listen) values ('10000000-0000-0000-0000-000000000001', '2026-10-18', 3)$$, 'a student scores themselves');
update public.adab set listen = 3;
commit;
select t.check((select listen is null from public.adab where kid_id = '10000000-0000-0000-0000-000000000001'), 'a student''s update changes nothing');
begin; set local role authenticated;
select set_config('request.jwt.claim.sub', '30000000-0000-0000-0000-000000000001', true);
select set_config('request.jwt.claims', '{"amr": [{"method": "otp", "timestamp": 1}]}', true);
select t.check((select count(*) from public.adab) = 0, 'a parent cannot see the scores');
commit;
begin; set local role anon;
select t.expect_error($$select count(*) from public.adab$$, 'anonymous visitor reads the scores');
commit;

-- ---------------------------------------------------------- a child who is deleted takes their scores along
delete from public.kids where id = '10000000-0000-0000-0000-000000000002';
select t.check((select count(*) from public.adab) = 1, 'scores go with the child');

\echo ALL ADAB TESTS PASSED
