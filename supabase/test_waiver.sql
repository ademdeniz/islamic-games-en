-- Local test of waiver.sql on plain Postgres (run after test_schema.sql has set up the stand-ins, in the same database).
-- Run:  tests/run_supabase_test.sh
\set ON_ERROR_STOP on
\set QUIET on

\ir waiver.sql
\ir waiver.sql
-- re-running the main schema must not break the waiver
\ir schema.sql

\o /dev/null
select set_config('my.ok', $j${
  "event": "youth-gathering-2026",
  "parent_first": "Amra", "parent_last": "Hodzic", "parent_email": " Amra@Example.com ",
  "parent_phone": "(814) 555-0101", "relationship": "Mother", "is_adult_guardian": true,
  "children": [{"first": "Emir", "last": "Hodzic", "birth_date": "2012-04-02", "gender": "Boy", "medical": "Peanut allergy"}],
  "emergency_name": "Senad Hodzic", "emergency_phone": "814-555-0102",
  "photo_consent": false, "acknowledgements": ["I have read the event details."],
  "signature_name": "Amra Hodzic", "signature_image": "data:image/png;base64,iVBORw0KGgo="
}$j$, false);
\o

-- ---------------------------------------------------------- a parent (not logged in) signs
begin; set local role anon;
select t.check(public.submit_waiver(current_setting('my.ok')::jsonb) is not null, 'parent signs without an account');
select t.expect_error($$select count(*) from public.trip_waivers$$, 'anonymous visitor reads waivers');
select t.expect_error($$insert into public.trip_waivers (event) values ('x')$$, 'anonymous visitor inserts directly');
select t.expect_error($$delete from public.trip_waivers$$, 'anonymous visitor deletes waivers');
select t.expect_error($$select public.submit_waiver(current_setting('my.ok')::jsonb || '{"is_adult_guardian": false}')$$, 'sign without confirming 18+ parent/guardian');
select t.expect_error($$select public.submit_waiver(current_setting('my.ok')::jsonb || '{"relationship": "Brother"}')$$, 'relationship other than parent/guardian');
select t.expect_error($$select public.submit_waiver(current_setting('my.ok')::jsonb || '{"parent_email": "nope"}')$$, 'bad e-mail');
select t.expect_error($$select public.submit_waiver(current_setting('my.ok')::jsonb || '{"parent_phone": "12"}')$$, 'short phone number');
select t.expect_error($$select public.submit_waiver(current_setting('my.ok')::jsonb || '{"children": []}')$$, 'no children');
select t.expect_error($$select public.submit_waiver(current_setting('my.ok')::jsonb || '{"children": [{"first": "A", "last": "B", "birth_date": "2012-01-01"}]}')$$, 'child without boy/girl');
select t.expect_error($$select public.submit_waiver(current_setting('my.ok')::jsonb || '{"signature_image": ""}')$$, 'no drawn signature');
select t.expect_error($$select public.submit_waiver(current_setting('my.ok')::jsonb - 'photo_consent')$$, 'photo question unanswered');
select t.expect_error($$select public.submit_waiver(current_setting('my.ok')::jsonb || '{"acknowledgements": []}')$$, 'no statements ticked');
commit;

-- ---------------------------------------------------------- only the admin sees and deletes
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000000b', true);
select t.check((select count(*) from public.trip_waivers) = 0, 'a teacher cannot see waivers');
delete from public.trip_waivers;
commit;
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000000a', true);
select t.check((select count(*) from public.trip_waivers) = 1, 'admin sees the signed waiver (teacher delete did nothing)');
select t.check((select parent_email from public.trip_waivers) = 'amra@example.com', 'e-mail saved trimmed and lower-case');
select t.check((select children -> 0 ->> 'medical' from public.trip_waivers) = 'Peanut allergy', 'child details saved');
select t.expect_error($$update public.trip_waivers set parent_last = 'X'$$, 'admin edits a signed waiver');
delete from public.trip_waivers;
select t.check((select count(*) from public.trip_waivers) = 0, 'admin deletes a waiver');
commit;

\echo ALL WAIVER TESTS PASSED
