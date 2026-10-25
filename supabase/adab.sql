-- Adab (behaviour) rubric – database setup for the same Supabase project.
-- Run once in Supabase: Dashboard → SQL Editor → New query → paste this whole file → Run.
-- Needs schema.sql, tracking.sql and parents.sql first. Safe to re-run.
--
-- After class the teacher scores each child 1–3 on five points (teacher/ → Adab):
--   listen   – listening: eyes on the teacher, follows instructions
--   turn     – speaking in turn: raises a hand, no side talk
--   part     – taking part: answers, reads, tries
--   respect  – respect to the teacher, friends and the masjid
--   phone    – no phone during class
-- 3 = 🌟 all class · 2 = 🙂 after a reminder · 1 = 😠 did not, even after many reminders. Empty = not scored.
-- Only the teacher (admin and activity_viewers) can see or change the scores. A parent sees their own children's scores on
-- parents/ (my_children_adab) – never the teacher's notes, never other children.

create table if not exists public.adab (
  kid_id     uuid not null references public.kids(id) on delete cascade,
  day        date not null,                                            -- the class Sunday
  listen     smallint check (listen between 1 and 3),
  turn       smallint check (turn between 1 and 3),
  part       smallint check (part between 1 and 3),
  respect    smallint check (respect between 1 and 3),
  phone      smallint check (phone between 1 and 3),
  absent     boolean not null default false,
  note       text check (length(note) <= 300),
  updated_at timestamptz not null default now(),
  primary key (kid_id, day)
);
create index if not exists adab_day on public.adab (day);

alter table public.adab enable row level security;
drop policy if exists "teacher manages adab" on public.adab;
create policy "teacher manages adab" on public.adab for all to authenticated
  using (public.can_see_activity()) with check (public.can_see_activity());
revoke all on public.adab from anon, authenticated;
grant select, insert, update, delete on public.adab to authenticated;

-- A parent's own children's scores (logged in with a code from their inbox, like my_children in parents.sql). No notes.
create or replace function public.my_children_adab(p_from date, p_to date) returns jsonb
language plpgsql stable security definer set search_path = public as $$
declare e text := public.parent_email();
begin
  if e is null then return null; end if;
  if p_from is null or p_to is null or p_to < p_from or p_to - p_from > 400 then raise exception 'Bad date range.'; end if;
  return coalesce((
    select jsonb_agg(jsonb_build_object('kid_id', a.kid_id, 'day', a.day, 'listen', a.listen, 'turn', a.turn, 'part', a.part,
             'respect', a.respect, 'phone', a.phone, 'absent', a.absent) order by a.day)
      from public.adab a
     where a.kid_id in (select kid_id from public.kid_parents where email = e)
       and a.day between p_from and p_to
       and (a.absent or coalesce(a.listen, a.turn, a.part, a.respect, a.phone) is not null)), '[]'::jsonb);
end $$;
revoke execute on function public.my_children_adab(date, date) from public, anon;
grant execute on function public.my_children_adab(date, date) to authenticated;
