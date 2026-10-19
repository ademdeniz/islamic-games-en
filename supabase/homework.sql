-- Homework check – database setup for the same Supabase project.
-- Run once in Supabase: Dashboard → SQL Editor → New query → paste this whole file → Run.
-- Needs schema.sql, tracking.sql and parents.sql first. Safe to re-run.
--
-- The week's tasks come from updates/<Sunday>/homework.json (made by tools/build_update.py): lesson pages, the Read
-- Along page, surahs, Sufara and games, each with its minimum active minutes for the week (Sunday–Saturday).
-- A task is done when the child's active time on its pages reaches the minimum, or when the teacher ticks it.
-- Here: the teacher's ticks, written tasks the teacher adds (notebook work), and what the pages may ask.

create table if not exists public.homework_extra (                   -- written / notebook tasks the teacher adds
  id         uuid primary key default gen_random_uuid(),
  week       date not null,                                           -- the Sunday the homework was given
  group_id   text not null references public.class_groups(id) on update cascade,
  label      text not null check (length(trim(label)) between 1 and 160),
  created_at timestamptz not null default now()
);
create index if not exists homework_extra_week on public.homework_extra (week, group_id);

create table if not exists public.homework_marks (                   -- the teacher's tick: done, whatever the minutes say
  kid_id    uuid not null references public.kids(id) on delete cascade,
  week      date not null,
  task_id   text not null check (length(task_id) between 1 and 80), -- a task id from homework.json, or a homework_extra id
  marked_at timestamptz not null default now(),
  primary key (kid_id, week, task_id)
);

alter table public.homework_extra enable row level security;
alter table public.homework_marks enable row level security;
drop policy if exists "teacher manages written tasks" on public.homework_extra;
create policy "teacher manages written tasks" on public.homework_extra for all to authenticated
  using (public.can_see_activity()) with check (public.can_see_activity());
drop policy if exists "teacher manages ticks" on public.homework_marks;
create policy "teacher manages ticks" on public.homework_marks for all to authenticated
  using (public.can_see_activity()) with check (public.can_see_activity());
revoke all on public.homework_extra, public.homework_marks from anon, authenticated;
grant select, insert, delete on public.homework_extra, public.homework_marks to authenticated;

-- Does a visit's page (e.g. games/citaj-kuran#page-5) count for a task page? Exact, or the task names the whole game
-- (games/learn-surahs-by-heart counts every surah), or an old visit from before pages were recorded.
create or replace function public.homework_match(visit text, task text) returns boolean
language sql immutable as $$
  select visit = task
      or (strpos(task, '#') = 0 and split_part(visit, '#', 1) = task)
      or (strpos(visit, '#') = 0 and strpos(task, '#') > 0 and visit = split_part(task, '#', 1))
$$;

-- A child's own homework week: seconds per page, the teacher's ticks, written tasks for the group.
create or replace function public.kid_homework(p_token text, p_week date, p_from timestamptz, p_to timestamptz) returns jsonb
language plpgsql stable security definer set search_path = public, extensions as $$
declare k public.kids;
begin
  select kids.* into k from public.kid_devices d join public.kids on kids.id = d.kid_id
   where d.token_hash = encode(digest(coalesce(p_token, ''), 'sha256'), 'hex');
  if k.id is null then return null; end if;
  if p_from is null or p_to is null or p_to <= p_from or p_to - p_from > interval '8 days' then raise exception 'Bad week.'; end if;
  return jsonb_build_object(
    'seconds', coalesce((select jsonb_object_agg(page_key, s) from (select page_key, sum(active_seconds) s from public.activity
                          where kid_id = k.id and started_at >= p_from and started_at < p_to group by page_key) t), '{}'::jsonb),
    'marks', coalesce((select jsonb_agg(task_id) from public.homework_marks where kid_id = k.id and week = p_week), '[]'::jsonb),
    'extra', coalesce((select jsonb_agg(jsonb_build_object('id', id, 'label', label) order by created_at) from public.homework_extra
                        where week = p_week and group_id = k.group_id), '[]'::jsonb));
end $$;

-- The logged-in parent's children: ticks and written tasks for that week (the visits come from my_children_activity).
create or replace function public.my_children_homework(p_week date) returns jsonb
language plpgsql stable security definer set search_path = public as $$
declare e text := public.parent_email();
begin
  if e is null then return null; end if;
  return coalesce((
    select jsonb_agg(jsonb_build_object(
             'kid_id', k.id,
             'marks', coalesce((select jsonb_agg(task_id) from public.homework_marks m where m.kid_id = k.id and m.week = p_week), '[]'::jsonb),
             'extra', coalesce((select jsonb_agg(jsonb_build_object('id', x.id, 'label', x.label) order by x.created_at)
                                  from public.homework_extra x where x.week = p_week and x.group_id = k.group_id), '[]'::jsonb)))
      from public.kids k where k.id in (select kid_id from public.kid_parents where email = e)), '[]'::jsonb);
end $$;

-- For the public weekly update: per group, how many children did each task. Counts only – never names.
-- p_tasks = the "groups" object of homework.json: {"g1": [{"id", "keys": [...], "min": minutes}, ...], ...}
create or replace function public.homework_summary(p_week date, p_from timestamptz, p_to timestamptz, p_tasks jsonb) returns jsonb
language plpgsql stable security definer set search_path = public as $$
declare g text; task jsonb; out jsonb := '{}'::jsonb; tasks jsonb; extra jsonb; n int;
begin
  if p_from is null or p_to is null or p_to <= p_from or p_to - p_from > interval '8 days' then raise exception 'Bad week.'; end if;
  if jsonb_typeof(p_tasks) is distinct from 'object' or (select count(*) from jsonb_object_keys(p_tasks)) > 10 then raise exception 'Bad tasks.'; end if;
  for g in select jsonb_object_keys(p_tasks) loop
    if not exists (select 1 from public.class_groups where id = g) or jsonb_array_length(p_tasks -> g) > 40 then continue; end if;
    select count(*) into n from public.kids where group_id = g and active;
    tasks := '{}'::jsonb;
    for task in select * from jsonb_array_elements(p_tasks -> g) loop
      if jsonb_array_length(coalesce(task -> 'keys', '[]'::jsonb)) > 30 then continue; end if;
      tasks := tasks || jsonb_build_object(task ->> 'id', (
        select count(*) from public.kids k where k.group_id = g and k.active and (
          exists (select 1 from public.homework_marks m where m.kid_id = k.id and m.week = p_week and m.task_id = task ->> 'id')
          or coalesce((select sum(a.active_seconds) from public.activity a
                        where a.kid_id = k.id and a.started_at >= p_from and a.started_at < p_to
                          and exists (select 1 from jsonb_array_elements_text(task -> 'keys') t(key) where public.homework_match(a.page_key, t.key))), 0)
             >= coalesce((task ->> 'min')::int, 0) * 60)));
    end loop;
    select coalesce(jsonb_agg(jsonb_build_object('label', x.label, 'done',
             (select count(*) from public.homework_marks m join public.kids k on k.id = m.kid_id
               where m.week = p_week and m.task_id = x.id::text and k.group_id = g and k.active)) order by x.created_at), '[]'::jsonb)
      into extra from public.homework_extra x where x.week = p_week and x.group_id = g;
    out := out || jsonb_build_object(g, jsonb_build_object('kids', n, 'tasks', tasks, 'extra', extra));
  end loop;
  return out;
end $$;

revoke execute on function public.kid_homework(text, date, timestamptz, timestamptz), public.my_children_homework(date),
  public.homework_summary(date, timestamptz, timestamptz, jsonb) from public;
grant execute on function public.kid_homework(text, date, timestamptz, timestamptz), public.homework_summary(date, timestamptz, timestamptz, jsonb)
  to anon, authenticated;
grant execute on function public.my_children_homework(date) to authenticated;
