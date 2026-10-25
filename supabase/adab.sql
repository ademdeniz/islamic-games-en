-- Adab (behaviour) rubric – database setup for the same Supabase project.
-- Run once in Supabase: Dashboard → SQL Editor → New query → paste this whole file → Run.
-- Needs schema.sql and tracking.sql first. Safe to re-run.
--
-- After class the teacher scores each child 1–3 on five points (teacher/ → Adab):
--   listen   – listening: eyes on the teacher, follows instructions
--   turn     – speaking in turn: raises a hand, no side talk
--   part     – taking part: answers, reads, tries
--   respect  – respect to the teacher, friends and the masjid
--   phone    – no phone during class
-- 3 = 🌟 all class · 2 = 🙂 after a reminder · 1 = 🌱 many reminders. Empty = not scored.
-- Only the teacher (admin and activity_viewers) can see or change the scores – not the children, not the parents.

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
