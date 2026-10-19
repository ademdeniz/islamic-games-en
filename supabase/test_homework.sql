-- Local test of homework.sql (run after test_schema.sql, test_tracking.sql and test_parents.sql, in the same database).
-- Run:  tests/run_supabase_test.sh
\set ON_ERROR_STOP on
\set QUIET on

\ir homework.sql
\ir homework.sql
-- re-running the other files must not break the homework check
\ir tracking.sql
\ir parents.sql

-- ---------------------------------------------------------- which visits count for which task page
select t.check(public.homework_match('lessons/ilmihal-2/17-messengers', 'lessons/ilmihal-2/17-messengers'), 'same page counts');
select t.check(public.homework_match('games/learn-surahs-by-heart#fil', 'games/learn-surahs-by-heart'), 'any surah counts for the whole game');
select t.check(not public.homework_match('games/citaj-kuran#page-4', 'games/citaj-kuran#page-5'), 'Read Along page 4 is not page 5');
select t.check(public.homework_match('games/citaj-kuran', 'games/citaj-kuran#page-5'), 'an old Read Along visit (no page recorded) counts');
select t.check(not public.homework_match('lessons/ilmihal-2/17', 'lessons/ilmihal-2/19'), 'another lesson does not count');

delete from public.activity;
insert into public.activity (id, kid_id, page_type, page_key, title, active_seconds) values
  (gen_random_uuid(), '10000000-0000-0000-0000-000000000001', 'lesson', 'lessons/x', 'Lesson X', 400),
  (gen_random_uuid(), '10000000-0000-0000-0000-000000000001', 'quran', 'games/citaj-kuran#page-5', 'Read Along', 600),
  (gen_random_uuid(), '10000000-0000-0000-0000-000000000001', 'surah', 'games/learn-surahs-by-heart#fil', 'Surahs', 700),
  (gen_random_uuid(), '10000000-0000-0000-0000-000000000002', 'quran', 'games/citaj-kuran', 'Read Along', 1000),
  (gen_random_uuid(), '10000000-0000-0000-0000-000000000002', 'lesson', 'lessons/x', 'Lesson X', 100);
insert into public.activity (id, kid_id, page_type, page_key, title, active_seconds, started_at) values
  (gen_random_uuid(), '10000000-0000-0000-0000-000000000002', 'game', 'games/kviz', 'Old week', 5000, now() - interval '20 days');
select set_config('my.tasks', $j${"g1": [
  {"id": "lesson-x", "keys": ["lessons/x"], "min": 5},
  {"id": "q-5", "keys": ["games/citaj-kuran#page-5"], "min": 15},
  {"id": "games", "keys": ["games/kviz", "games/learn-surahs-by-heart"], "min": 10}],
 "g2": [{"id": "lesson-y", "keys": ["lessons/y"], "min": 5}], "nope": [{"id": "z", "keys": ["z"], "min": 1}]}$j$, false) is not null;
select set_config('my.week', current_date::text, false) is not null;

-- ---------------------------------------------------------- the teacher ticks and adds a written task
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000000b', true);
insert into public.homework_marks (kid_id, week, task_id) values ('10000000-0000-0000-0000-000000000002', current_date, 'lesson-x');
insert into public.homework_extra (week, group_id, label) values (current_date, 'g1', 'Notebook: book p. 8');
insert into public.homework_marks (kid_id, week, task_id)
  select '10000000-0000-0000-0000-000000000001', current_date, id::text from public.homework_extra where label = 'Notebook: book p. 8';
select t.check((select count(*) from public.homework_marks) = 2, 'listed teacher ticks tasks');
commit;
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-000000000001', true);
select t.expect_error($$insert into public.homework_marks (kid_id, week, task_id) values ('10000000-0000-0000-0000-000000000001', current_date, 'q-5')$$, 'a student ticks their own homework');
select t.check((select count(*) from public.homework_marks) = 0, 'a student cannot see the ticks');
commit;

-- ---------------------------------------------------------- the public weekly update: counts only
begin; set local role anon;
\o /dev/null
select set_config('my.sum', public.homework_summary(current_date, now() - interval '1 day', now() + interval '1 day', current_setting('my.tasks')::jsonb)::text, true);
\o
select t.check((current_setting('my.sum')::jsonb -> 'g1' ->> 'kids')::int = 2, 'Group 1 has 2 children in the list');
select t.check((current_setting('my.sum')::jsonb -> 'g1' -> 'tasks' ->> 'lesson-x')::int = 2, 'lesson: one by minutes (400s ≥ 5 min), one ticked by the teacher (100s)');
select t.check((current_setting('my.sum')::jsonb -> 'g1' -> 'tasks' ->> 'q-5')::int = 1, 'Read Along page 5: 600s is under 15 min; an old 1000s visit counts');
select t.check((current_setting('my.sum')::jsonb -> 'g1' -> 'tasks' ->> 'games')::int = 1, 'games: a surah in the surah game counts; last month does not');
select t.check((current_setting('my.sum')::jsonb -> 'g1' -> 'extra' -> 0 ->> 'done')::int = 1, 'written task: one ticked');
select t.check(current_setting('my.sum')::jsonb ? 'nope' = false, 'unknown group ignored');
select t.check(current_setting('my.sum') !~ 'Emir|Sara|Hodzic|Begic', 'no names in the summary');
select t.expect_error($$select public.homework_summary(current_date, now() - interval '30 days', now(), '{}')$$, 'summary only for one week');
select t.expect_error($$select count(*) from public.homework_marks$$, 'anonymous visitor reads the ticks');
select t.expect_error($$select public.my_children_homework(current_date)$$, 'anonymous visitor asks for a parent''s homework');
commit;

-- ---------------------------------------------------------- a child's own homework
update public.kids set pin = null where id = '10000000-0000-0000-0000-000000000001';
begin; set local role anon;
\o /dev/null
select set_config('my.tok9', public.sign_in_kid('SABR99', '10000000-0000-0000-0000-000000000001', '123') ->> 'token', false);
\o
select t.check((public.kid_homework(current_setting('my.tok9'), current_date, now() - interval '1 day', now() + interval '1 day') -> 'seconds' ->> 'lessons/x')::int = 400, 'child sees their own seconds per page');
select t.check(jsonb_array_length(public.kid_homework(current_setting('my.tok9'), current_date, now() - interval '1 day', now() + interval '1 day') -> 'marks') = 1, 'child sees the teacher''s tick');
select t.check((public.kid_homework(current_setting('my.tok9'), current_date, now() - interval '1 day', now() + interval '1 day') -> 'extra' -> 0 ->> 'label') = 'Notebook: book p. 8', 'child sees the written task');
select t.check(public.kid_homework('not-a-token', current_date, now(), now() + interval '1 day') is null, 'unknown device gets nothing');
commit;

-- ---------------------------------------------------------- a parent sees their children's ticks and written tasks
begin; set local role authenticated;
select set_config('request.jwt.claim.sub', '30000000-0000-0000-0000-000000000001', true);
select set_config('request.jwt.claims', '{"amr": [{"method": "otp", "timestamp": 1}]}', true);
select t.check(jsonb_array_length(public.my_children_homework(current_date)) = 2, 'mother gets both children');
select t.check(public.my_children_homework(current_date)::text ~ 'lesson-x' and public.my_children_homework(current_date)::text ~ 'Notebook', 'with ticks and the written task');
select t.check(public.my_children_activity(now() - interval '1 day', now() + interval '1 day') -> 0 ? 'page_key', 'visits carry the page');
commit;
begin; set local role authenticated;
select set_config('request.jwt.claim.sub', '30000000-0000-0000-0000-000000000001', true);
select set_config('request.jwt.claims', '{"amr": [{"method": "password", "timestamp": 1}]}', true);
select t.check(public.my_children_homework(current_date) is null, 'password login gets nothing');
commit;

\echo ALL HOMEWORK TESTS PASSED
