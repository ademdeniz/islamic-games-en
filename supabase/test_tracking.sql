-- Local test of tracking.sql on plain Postgres (run after test_schema.sql has set up the stand-ins, in the same database).
-- Run:  tests/run_supabase_test.sh
\set ON_ERROR_STOP on
\set QUIET on

\ir tracking.sql
\ir tracking.sql
-- re-running the main schema must not break tracking
\ir schema.sql

insert into public.class_groups (id, name, code, pin_required) values ('g1', 'Group 1', 'SABR27', true), ('g2', 'Group 2', 'NUR48', false);
insert into public.kids (id, group_id, first_name, last_name) values
  ('10000000-0000-0000-0000-000000000001', 'g1', 'Emir', 'Hodzic'),
  ('10000000-0000-0000-0000-000000000002', 'g1', 'Sara', 'Begic'),
  ('10000000-0000-0000-0000-000000000003', 'g2', 'Mina', 'Zukic');
insert into public.kids (group_id, first_name, last_name, active) values ('g2', 'Gone', 'Away', false);

-- ---------------------------------------------------------- a child joins (no login)
begin; set local role anon;
select t.expect_error($$select public.join_class('WRONG1')$$, 'wrong class code');
select t.check(jsonb_array_length(public.join_class(' sabr27 ') -> 'kids') = 2, 'class code (any case, spaces) lists the group''s names');
select t.check((public.join_class('SABR27') -> 'kids' -> 0 ->> 'name') = 'Emir H.', 'names are first name + last initial');
select t.check(public.join_class('SABR27')::text !~ 'Hodzic', 'full last name is never sent');
select t.check(jsonb_array_length(public.join_class('NUR48') -> 'kids') = 1, 'children who left are not listed');
select t.expect_error($$select count(*) from public.kids$$, 'anonymous visitor reads the children list');
select t.expect_error($$select count(*) from public.class_groups$$, 'anonymous visitor reads the class codes');
select t.expect_error($$select public.sign_in_kid('NUR48', '10000000-0000-0000-0000-000000000001', null)$$, 'sign in with another group''s code');
select t.expect_error($$select public.sign_in_kid('SABR27', '10000000-0000-0000-0000-000000000001', null)$$, 'PIN group without a PIN');
select t.check((public.sign_in_kid('SABR27', '10000000-0000-0000-0000-000000000001', '307') ->> 'new_pin')::boolean, 'first sign-in sets the PIN');
select t.expect_error($$select public.sign_in_kid('SABR27', '10000000-0000-0000-0000-000000000001', '111')$$, 'wrong PIN');
\o /dev/null
select set_config('my.tok', public.sign_in_kid('SABR27', '10000000-0000-0000-0000-000000000001', '307') ->> 'token', true);
\o
select t.check(public.track_visit(current_setting('my.tok'), '20000000-0000-0000-0000-000000000001', 'lesson', 'lessons/ilmihal-2/01-amantu', 'Amantu billahi', 30), 'page reports 30 seconds');
select t.check(public.track_visit(current_setting('my.tok'), '20000000-0000-0000-0000-000000000001', 'lesson', 'lessons/ilmihal-2/01-amantu', 'Amantu billahi', 5000), 'a too-big report is cut to 120');
select t.check(not public.track_visit('not-a-token', '20000000-0000-0000-0000-000000000002', 'game', 'games/x', 'X', 30), 'unknown token is refused');
select t.expect_error($$select public.track_visit(current_setting('my.tok'), '20000000-0000-0000-0000-000000000003', 'hacking', 'x', 'x', 30)$$, 'unknown page type');
select t.expect_error($$select count(*) from public.activity$$, 'anonymous visitor reads activity');
select t.expect_error($$insert into public.activity (id, kid_id, page_type, page_key) values (gen_random_uuid(), '10000000-0000-0000-0000-000000000002', 'game', 'x')$$, 'anonymous visitor writes activity directly');
select t.check((public.sign_in_kid('NUR48', '10000000-0000-0000-0000-000000000003', null) ->> 'name') = 'Mina Z.', 'group without PIN: tap the name only');
commit;

-- ---------------------------------------------------------- another child cannot add time to Emir's visit
begin; set local role anon;
\o /dev/null
select set_config('my.tok2', public.sign_in_kid('SABR27', '10000000-0000-0000-0000-000000000002', '555') ->> 'token', false);
select public.track_visit(current_setting('my.tok2'), '20000000-0000-0000-0000-000000000001', 'lesson', 'lessons/ilmihal-2/01-amantu', 'Amantu billahi', 100);
\o
commit;
select t.check((select active_seconds from public.activity where id = '20000000-0000-0000-0000-000000000001') = 150, 'visit has 30 + 120 seconds, nothing from another child');
-- ---------------------------------------------------------- today's summary, sign out
begin; set local role anon;
select t.check((public.kid_today(current_setting('my.tok2'), now() - interval '1 hour') ->> 'seconds')::int = 0, 'Sara has nothing today yet');
select t.check((public.kid_today(current_setting('my.tok2'), now() - interval '1 hour') ->> 'goal_minutes')::int = 10, 'default daily goal is 10 minutes');
select t.check(public.kid_today('not-a-token', now()) is null, 'unknown device gets no summary');
select t.expect_error($$select public.kid_today(current_setting('my.tok2'), now() - interval '30 days')$$, 'summary only for recent days');
commit;
begin; set local role anon;
\o /dev/null
select set_config('my.tok3', public.sign_in_kid('NUR48', '10000000-0000-0000-0000-000000000003', null) ->> 'token', false);
select public.track_visit(current_setting('my.tok3'), '20000000-0000-0000-0000-000000000005', 'quran', 'games/citaj-kuran', 'Read Along', 90);
select public.track_visit(current_setting('my.tok3'), '20000000-0000-0000-0000-000000000006', 'lesson', 'lessons/b', 'Lesson B', 40);
\o
select t.check((public.kid_today(current_setting('my.tok3'), now() - interval '1 hour') ->> 'seconds')::int = 130, 'Mina''s today total');
select t.check((public.kid_today(current_setting('my.tok3'), now() - interval '1 hour') -> 'by_type' ->> 'quran')::int = 90, 'today by kind');
select t.check(jsonb_array_length(public.kid_today(current_setting('my.tok3'), now() - interval '1 hour') -> 'pages') = 2, 'pages practised today');
select public.sign_out_device(current_setting('my.tok3'));
select t.check(public.kid_today(current_setting('my.tok3'), now()) is null, 'signed-out device gets nothing');
select t.check(not public.track_visit(current_setting('my.tok3'), '20000000-0000-0000-0000-000000000007', 'game', 'g', 'G', 10), 'signed-out device cannot report time');
commit;

-- ---------------------------------------------------------- who sees the dashboard
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000000b', true);
select t.check(not public.can_see_activity(), 'a teacher is not a viewer until listed');
select t.check((select count(*) from public.activity) = 0, 'unlisted teacher sees no activity');
select t.check((select count(*) from public.kids) = 0, 'unlisted teacher sees no children');
select t.expect_error($$insert into public.activity_viewers values (auth.uid())$$, 'teacher adds self as a viewer');
commit;
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-000000000001', true);
select t.check((select count(*) from public.kids) = 0, 'a student sees no children');
commit;
insert into public.activity_viewers (user_id) select id from auth.users where email = 'teacher@x';
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000000b', true);
select t.check(public.can_see_activity(), 'listed teacher is a viewer');
select t.check((select count(*) from public.activity a join public.kids k on k.id = a.kid_id where k.last_name = 'Hodzic') = 1, 'listed teacher sees activity with full names');
insert into public.kids (group_id, first_name, last_name) values ('g2', 'Novi', 'Ucenik');
update public.class_groups set code = 'SABR99' where id = 'g1';
update public.class_groups set daily_goal_minutes = 15 where id = 'g1';
select t.expect_error($$update public.class_groups set daily_goal_minutes = 500 where id = 'g1'$$, 'daily goal over 120 minutes');
update public.kids set pin = null where first_name = 'Emir';
select t.expect_error($$update public.activity set active_seconds = 99999$$, 'teacher edits activity');
delete from public.kid_devices where kid_id = '10000000-0000-0000-0000-000000000001';
commit;
begin; set local role anon;
select t.check(public.track_visit(current_setting('my.tok2'), '20000000-0000-0000-0000-000000000009', 'game', 'games/x', 'X', 10), 'Sara''s device still works after the code changed');
select t.check(jsonb_array_length(public.join_class('SABR99') -> 'kids') = 2, 'new class code works');
select t.expect_error($$select public.join_class('SABR27')$$, 'old class code stops working');
commit;
select t.check((select count(*) from public.kid_devices where kid_id = '10000000-0000-0000-0000-000000000001') = 0, 'teacher signed out Emir''s devices');
select t.check((select pin from public.kids where first_name = 'Emir') is null, 'teacher reset Emir''s PIN');
begin; set local role authenticated; select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000000a', true);
select t.check(public.can_see_activity(), 'the admin is always a viewer');
delete from public.activity;
commit;
select t.check((select count(*) from public.activity) = 0, 'end of year: viewer deletes the activity');

\echo ALL TRACKING TESTS PASSED
