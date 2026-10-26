# Maktab Erie – English maktab website

The maktab (Islamic weekend school) website of the **Bosnian Islamic Community of Erie**: English learning games,
Ilmihal lessons, Sufara (the Arabic letters), the year plan, weekly updates for parents and the parent duty page.

**Live:** https://ademdeniz.github.io/islamic-games-en/ (the repository keeps its old name so links already sent to parents keep working)

| Page | Link | Built with |
|---|---|---|
| Games, recitation and tajwid pages (110) | [/](https://ademdeniz.github.io/islamic-games-en/) | `tools/templates/home.html` → `tools/build_home.py` |
| Ilmihal lessons (books 1–3) | [/lessons/](https://ademdeniz.github.io/islamic-games-en/lessons/) | `data/lessons/` → `tools/build_lessons.py` |
| Sufara | [/sufara/](https://ademdeniz.github.io/islamic-games-en/sufara/) | `data/sufara/` → `tools/build_sufara.py` |
| Year plan for parents | [/plan/](https://ademdeniz.github.io/islamic-games-en/plan/) | `data/plan/plan.json` → `tools/build_plan.py` |
| Weekly updates | [/updates/](https://ademdeniz.github.io/islamic-games-en/updates/) | `data/updates/<date>.json` → `tools/build_update.py` |
| QR code for the mosque wall (always opens the newest update) | [/qr/](https://ademdeniz.github.io/islamic-games-en/qr/) | `tools/build_update.py` |
| Pizza & parent duty | [/duty/](https://ademdeniz.github.io/islamic-games-en/duty/) | `data/duty/parents.json` → `tools/build_duty.py` |
| Credits | [/credits/](https://ademdeniz.github.io/islamic-games-en/credits/) | `tools/build_credits.py` |
| Teacher dashboard – who opened what, for how long, homework and adab (login) | [/teacher/](https://ademdeniz.github.io/islamic-games-en/teacher/) | hand-written · database `supabase/tracking.sql` |
| Parents – their own children's week and homework (e-mail code login) | [/parents/](https://ademdeniz.github.io/islamic-games-en/parents/) | hand-written · database `supabase/parents.sql` |
| Youth Gathering 2026 parent waiver (not linked; admin list at `waiver/admin.html`) | [/waiver/](https://ademdeniz.github.io/islamic-games-en/waiver/) | hand-written · database `supabase/waiver.sql` |

Classes are every Sunday. Group 1: Ilmihal 2 & 3, Qur’an (Al-Baqarah), Sufara, Tajwid from November.
Group 2: Ilmihal 1 and Sufara. New lessons are added through the year, one Sunday ahead.

## Credits and permission

- **Games:** English versions of the Bosnian maktab games by **Abdo ef. Rekić** ([github.com/rekicabdo-bihac](https://github.com/rekicabdo-bihac)), used with permission. The originals are kept unchanged in `original/`.
- **Ilmihal lessons:** adapted from the **El-Kalem** Ilmihal 1–3 books, used with permission.
- **Qur’an:** translation Sahih International (via AlQuran.cloud, checked word for word by the tests); recitation Mishary Rashid Alafasy.

## Every week

- **Before class:** build the lessons for the next Sunday (`data/lessons/ilmihal-N/<book page>-<name>.json`,
  pictures via `tools/extract_lesson_images.py`, then `python3 tools/build_lessons.py`).
- **After class:** the parents’ update – follow `docs/weekly-update-prompt.md`. Sent updates are frozen and never rebuilt.
  Each update has a “📱 QR code” button and `updates/<date>/qr.png` (for WhatsApp); `updates/latest/` always forwards to
  the newest one, so the printed sheet at `qr/` never needs reprinting. QR codes are made by `segno` (`.venv/bin/pip install segno`).
- **Publish:** run the tests, commit and push to `main`. GitHub Pages updates in 2–5 minutes (Cmd+Shift+R to see it).

## Settings – one place for the mosque's details

- `site.json` – name, short name, logo, website address, contact. Every builder reads it (`tools/site_settings.py`).
  After a change: `python3 tools/build_site.py` rebuilds every game, lesson, Sufara page, the plan, duty, credits and home page.
- `data/plan/plan.json` – the school year: dates, no-class days, groups and their tracks, notes.
  `python3 tools/build_plan.py` builds the parents’ copy; `--private <file>` builds the teacher’s tracker.

## Sharing with other mosques

`python3 tools/make_starter.py <empty folder>` makes the clean starter (no updates, parent names, Supabase project or
Erie logo), published as the template [ademdeniz/maktab-starter](https://github.com/ademdeniz/maktab-starter).
Teachers make their own copy from that template with the setup guide. **Nobody else pushes to this repository.**
The starter does not follow this repository on its own: re-run `make_starter.py` and push it to share new lessons.

## Games – how they are made

- `games/<game>/index.html` – one self-contained file per game, translated from `original/` with the toolkit in `tools/`
  (`tools/skel.py`, `tools/translate.py`, one table per game in `tools/tr/`). Rules and glossary: `TRANSLATING.md`.
- **Shared Ilmihal question bank** `tools/tr/ilmihal-bank.json` – Abdo ef. Rekić’s 1,568 questions (A1–B3) with their
  English, used through `tools/tr/_ilmihal_bank.py` by the 6 play-together games (Football, Tug of War, Millionaire for Two,
  Wheel of Fortune, Board Game – Don’t Get Angry!, Tournament) and the 12 play-alone games (Maktab Academy, Daily Challenge,
  Journey, Maze, Balloon, Safari, Garden, Aquarium, Secret Code, Hidden Picture, Build Your Mosque, Bee Academy).
- **New games** (not translations): `learn-surahs-by-heart` (`tools/fetch_hifz.py` + `tools/build_hifz.py`) and the
  Read Along `citaj-kuran` (`tools/fetch_readalong.py` + `tools/build_citaj_kuran.py`).
- **Recitation, tajwid pages and games** (50, from Abdo ef. Rekić's newer repositories): surahs ayah by ayah (`sura-*`, `ajetul-kursijja`), their
  tajwid-coloured transliterations (`sura-*-transkripcija`), Al-Baqarah 1–37 (`elif-lam-mim`, `bekare-*`) and duas & dhikr
  (`dove-*`, `dova-poslije-ezana`). They keep the Arabic on purpose and share their English in `tools/tr/_rekic_ui.py`
  (buttons and messages, author credit and his analytics tag removed) and `tools/tr/_rekic_dua.py` (each dua line's
  transliteration and meaning). Full-screen pages set `BRAND_FIT` so they fit under the logo (`skel.FIT_CSS`).
  Tajwid: `tedzvid` (= his `tedzvid-`), `kviz-tedzvid` (365 questions through `tools/tr/_tajwid_bank.py`, shared with the tajwid
  penalty game) and `tedzvid-arapski-brojevi`. A table can list attributes that hold text in `TEXT_ATTRS` (tedzvid: `data-lesson`).
  Games: the penalty games `penali` (A1–A3), `penali2` (B1–B3), `penali-n` (Salah), `penali-t` (tajwid) share `tools/tr/_penali.py`;
  `mektebski-ribolov` (Ilmihal bank) and `podmornica-znanja-namaz` (Salah bank, `tools/tr/_salah_bank.py` = kviz-namaz's translation).
  The tracker counts `sura-*`/`ajetul-kursijja` as surahs and `elif-lam-mim`/`bekare-*` as Qur’an.
  Local names that differ from his repositories: `sura-tekasur` = `sura-tekasur-`, `sura-nas` = `suretu-nnas`,
  `sura-fatiha` = `sura--fatiha-`, `sura-fatiha-transkripcija` = `sura-fatiha-transkripcija-`,
  `sura-nas-transkripcija` = `sura-nnas-transkripcija`, `elif-lam-mim` = `elif-lam-mim--`, `bekare-22-24` = `bekare22-23-24`.
- Not on the home page: `maca-pripreme-za-namaz` (near-duplicate of `kviz-maca-namaz`) and `el-fatiha`
  (replaced by `learn-surahs-by-heart`). Local name `moj-mektebski-vrt` = repo `moj-mektebski-vrt1`.
- `islamski-milijunas-online` uses our Supabase project (`supabase/config.json`, publishable key only).
  Database: run `supabase/schema.sql` in the Supabase SQL Editor; local test `tests/run_supabase_test.sh`.
- **Activity tracking** (`supabase/tracking.sql`, `tools/tracking.js` + `tools/tracking.py`): lessons, Sufara and every game
  (Read Along and the surah games included) carry a small tracker, added by their builders (`skel.build` for the
  translated games) – not on index pages, not in the starter. The game checks compare games without it. A child types the
  class code of their group once per device, taps their name and – where the group has it on – picks 3 pictures. Only active
  time counts (page on screen and touched in the last minute, or audio playing). Children, codes and activity are only visible
  in `teacher/` to the admin and accounts in `activity_viewers` (add one like `waiver_viewers` below). The children's names
  are entered in the dashboard or by a private SQL file – never in this public repository.
- **Parents** (`parents/`, `supabase/parents.sql`): a parent types their e-mail, gets a code (e-mail templates in
  `supabase/email-templates/`) and sees only the children linked to that e-mail in `kid_parents` (from the registration
  form; editable on `teacher/` → Children). Password logins never see children. The e-mails live only in Supabase.
- **Homework check** (`supabase/homework.sql`, `data/homework.json`): `tools/build_update.py` writes
  `updates/<Sunday>/homework.json` – each group's lesson pages, Read Along page, surahs, Sufara and games with the minimum
  active minutes for the week (Sunday–Saturday) from `data/homework.json`. A task is done when the child reaches the
  minimum, or when the teacher ticks it on `teacher/` → Homework (written tasks can be added there). Children see their
  list in the name chip, parents on `parents/`, and new weekly updates show “Last week’s homework” counts (no names).
  Read Along and Learn the Surahs put the page/surah in the address (`#page-5`, `#fil`) so time is counted per page.
  Time on Abdo ef. Rekić's matching recitation page counts too (`SURAH_PAGES`, `BAQARAH_PAGES` in `tools/build_update.py`).
- **Adab rubric** (`supabase/adab.sql`): after class the teacher scores each child on `teacher/` → Adab – listening, speaking
  in turn, taking part, respect and no phone – 🌟 3 all class · 🙂 2 after a reminder · 😠 1 did not, even after many reminders, with “absent” and a
  short note. The same tab shows each child’s year so far and whether the last 4 classes are better or need help. Only the
  admin and `activity_viewers` change them; a parent sees their own child's scores on `parents/` (not the notes).
  Run `supabase/adab.sql` after `parents.sql`.
- The parent waiver (`waiver/`) uses the same Supabase project: run `supabase/waiver.sql` after `schema.sql`.
  Only the admin and accounts in `waiver_viewers` can see signed waivers; `tests/run_supabase_test.sh` tests both files.
  To let an account see the waivers (it keeps its role in the games), run in the SQL Editor (with its e-mail):
  `insert into public.waiver_viewers (user_id) select id from auth.users where email = 'you@example.com' on conflict do nothing;`

## Run and test

```
python3 -m http.server 8765        # then open http://localhost:8765
.venv/bin/pytest tests              # every game, lesson, Sufara page, plan and update (~15 minutes)
python3 tools/rebuild_all.py        # rebuild all games and check they come out identical
```
Run `rebuild_all.py` in a fresh clone after bigger changes to prove nothing depends on files that exist only on one
computer (`work/` is only a scratch folder).
