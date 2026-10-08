# Maktab Erie – English maktab website

The maktab (Islamic weekend school) website of the **Bosnian Islamic Community of Erie**: English learning games,
Ilmihal lessons, Sufara (the Arabic letters), the year plan, weekly updates for parents and the parent duty page.

**Live:** https://ademdeniz.github.io/islamic-games-en/ (the repository keeps its old name so links already sent to parents keep working)

| Page | Link | Built with |
|---|---|---|
| Games (60) | [/](https://ademdeniz.github.io/islamic-games-en/) | `tools/templates/home.html` → `tools/build_home.py` |
| Ilmihal lessons (books 1–3) | [/lessons/](https://ademdeniz.github.io/islamic-games-en/lessons/) | `data/lessons/` → `tools/build_lessons.py` |
| Sufara | [/sufara/](https://ademdeniz.github.io/islamic-games-en/sufara/) | `data/sufara/` → `tools/build_sufara.py` |
| Year plan for parents | [/plan/](https://ademdeniz.github.io/islamic-games-en/plan/) | `data/plan/plan.json` → `tools/build_plan.py` |
| Weekly updates | [/updates/](https://ademdeniz.github.io/islamic-games-en/updates/) | `data/updates/<date>.json` → `tools/build_update.py` |
| QR code for the mosque wall (always opens the newest update) | [/qr/](https://ademdeniz.github.io/islamic-games-en/qr/) | `tools/build_update.py` |
| Pizza & parent duty | [/duty/](https://ademdeniz.github.io/islamic-games-en/duty/) | `data/duty/parents.json` → `tools/build_duty.py` |
| Credits | [/credits/](https://ademdeniz.github.io/islamic-games-en/credits/) | `tools/build_credits.py` |

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
- Not on the home page: `maca-pripreme-za-namaz` (near-duplicate of `kviz-maca-namaz`) and `el-fatiha`
  (replaced by `learn-surahs-by-heart`). Local name `moj-mektebski-vrt` = repo `moj-mektebski-vrt1`.
- `islamski-milijunas-online` uses our Supabase project (`supabase/config.json`, publishable key only).
  Database: run `supabase/schema.sql` in the Supabase SQL Editor; local test `tests/run_supabase_test.sh`.

## Run and test

```
python3 -m http.server 8765        # then open http://localhost:8765
.venv/bin/pytest tests              # every game, lesson, Sufara page, plan and update (~15 minutes)
python3 tools/rebuild_all.py        # rebuild all games and check they come out identical
```
Run `rebuild_all.py` in a fresh clone after bigger changes to prove nothing depends on files that exist only on one
computer (`work/` is only a scratch folder).
