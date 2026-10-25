-- Local test of adab.sql (run after test_schema.sql, test_tracking.sql and test_parents.sql, in the same database).
-- Run:  tests/run_supabase_test.sh
\set ON_ERROR_STOP on
\set QUIET on

\ir adab.sql
\ir adab.sql
-- re-running the other files must not break the rubric
\ir tracking.sql
\ir parents.sql

-- ---------------------------------------------------------- the teacher scores after class
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000000b', true);
insert into public.adab (kid_id, day, listen, phone) values ('10000000-0000-0000-0000-000000000001', '2026-10-25', 3, 1);
insert into public.adab (kid_id, day, turn) values ('10000000-0000-0000-0000-000000000001', '2026-10-25', 2)
  on conflict (kid_id, day) do update set turn = excluded.turn;
insert into public.adab (kid_id, day, absent, note) values ('10000000-0000-0000-0000-000000000002', '2026-10-25', true, 'quiet week at home');
insert into public.adab (kid_id, day, note) values ('10000000-0000-0000-0000-000000000002', '2026-10-18', 'only a note, no score');
select t.check((select (listen, turn, phone) = (3::smallint, 2::smallint, 1::smallint) from public.adab where kid_id = '10000000-0000-0000-0000-000000000001'),
  'a second tap on another point keeps the first ones');
update public.adab set listen = null where kid_id = '10000000-0000-0000-0000-000000000001';
select t.check((select listen is null from public.adab where kid_id = '10000000-0000-0000-0000-000000000001'), 'teacher clears a score');
select t.expect_error($$insert into public.adab (kid_id, day, listen) values ('10000000-0000-0000-0000-000000000002', '2026-10-18', 4)$$, 'a score of 4');
select t.expect_error($$insert into public.adab (kid_id, day, respect) values ('10000000-0000-0000-0000-000000000002', '2026-10-18', 0)$$, 'a score of 0');
select t.expect_error($$insert into public.adab (kid_id, day, note) values ('10000000-0000-0000-0000-000000000002', '2026-10-18', repeat('x', 301))$$, 'a note longer than 300');
select t.check((select count(*) from public.adab) = 3, 'listed teacher sees the scores');
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
select t.check((select count(*) from public.adab) = 0, 'a parent cannot read the table itself');
select t.check(jsonb_array_length(public.my_children_adab('2026-09-01', '2026-12-31')) = 2, 'mother sees her children''s scores');
select t.check(public.my_children_adab('2026-09-01', '2026-12-31')::text !~ 'note' and public.my_children_adab('2026-09-01', '2026-12-31')::text !~ 'quiet', 'but not the teacher''s notes');
select t.check(jsonb_array_length(public.my_children_adab('2026-10-26', '2026-12-31')) = 0, 'only the dates asked for');
select t.expect_error($$select public.my_children_adab('2026-12-31', '2026-09-01')$$, 'a backwards date range');
commit;
begin; set local role authenticated;
select set_config('request.jwt.claim.sub', '30000000-0000-0000-0000-000000000001', true);
select set_config('request.jwt.claims', '{"amr": [{"method": "password", "timestamp": 1}]}', true);
select t.check(public.my_children_adab('2026-09-01', '2026-12-31') is null, 'password login gets nothing');
commit;
begin; set local role authenticated;
select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-000000000001', true);
select set_config('request.jwt.claims', '{"amr": [{"method": "otp", "timestamp": 1}]}', true);
select t.check(coalesce(jsonb_array_length(public.my_children_adab('2026-09-01', '2026-12-31')), 0) = 0, 'someone with no linked child sees nothing');
commit;
begin; set local role anon;
select t.expect_error($$select count(*) from public.adab$$, 'anonymous visitor reads the scores');
select t.expect_error($$select public.my_children_adab('2026-09-01', '2026-12-31')$$, 'anonymous visitor asks for a parent''s scores');
commit;

-- ---------------------------------------------------------- a child who is deleted takes their scores along
delete from public.kids where id = '10000000-0000-0000-0000-000000000002';
select t.check((select count(*) from public.adab) = 1, 'scores go with the child');
select t.check(not exists (select 1 from public.adab where kid_id = '10000000-0000-0000-0000-000000000002'), 'none left for that child');

\echo ALL ADAB TESTS PASSED
