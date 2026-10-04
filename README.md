# Islamic Learning Games (English)

English versions of 60 maktab learning games (Qur’an, Salah, Iman, Ilmihal) for the Bosnian Islamic Community of Erie,
translated from the Bosnian originals at github.com/rekicabdo-bihac.

- `index.html` – home page listing the games (level filter, search, “Copy link” for homework)
- `games/<game>/index.html` – the English games (each is one self-contained file)
- `lessons/` – Ilmihal lessons adapted from the El-Kalem Ilmihal books (permission requested): `data/lessons/`, `tools/build_lessons.py`, pictures via `tools/extract_lesson_images.py`
- `sufara/` – Arabic letters (28 letter pages + reviews): `data/sufara/`, `tools/fetch_sufara_words.py`, `tools/build_sufara.py`
- `original/` – the Bosnian originals, unchanged
- `TRANSLATING.md` – translation rules and glossary · `tools/` – translation toolkit · `tests/` – checks every game

Run locally: `python3 -m http.server 8765` then open http://localhost:8765
Test: `.venv/bin/pytest tests`

`islamski-milijunas-online` uses our own Supabase project (`supabase/config.json`, publishable key only).
Database setup: run `supabase/schema.sql` in the Supabase SQL Editor; test it locally with `tests/run_supabase_test.sh`.
Not linked from the home page: `maca-pripreme-za-namaz` (near-duplicate of `kviz-maca-namaz`) and `el-fatiha`
(replaced by `learn-surahs-by-heart`, which includes Al-Fatiha).

Shared Ilmihal question bank: `tools/tr/ilmihal-bank.json` – Abdo ef. Rekić’s 1,568 questions (A1–B3) with their English,
used by the newer games through `tools/tr/_ilmihal_bank.py`. The play-together games (Football, Tug of War, Millionaire for Two,
Wheel of Fortune, Board Game – Don’t Get Angry!, Tournament) and the twelve play-alone games (Maktab Academy, Daily Challenge,
Journey, Maze, Balloon, Safari, Garden, Aquarium, Secret Code, Hidden Picture, Build Your Mosque, Bee Academy) all use it;
`tests/test_bank_games.py` plays each one. (Local name `moj-mektebski-vrt` = repo `moj-mektebski-vrt1`.)
Also: `plan/` (year plan for parents, `tools/build_plan.py`), `updates/` (weekly updates, `tools/build_update.py`),
`duty/` (Sunday pizza & parent duty, `tools/build_duty.py`).

New games (not translations): `games/learn-surahs-by-heart` (`tools/fetch_hifz.py` + `tools/build_hifz.py`) and the rebuilt
`games/citaj-kuran` Read Along (`tools/fetch_readalong.py` + `tools/build_citaj_kuran.py`).

Qur’an translation: Sahih International (via AlQuran.cloud) · Recitation: Mishary Rashid Alafasy

## Settings – one place for the mosque's details

- `site.json` – name, short name, logo file, website address, contact. Every builder reads it (`tools/site_settings.py`).
  After a change: `python3 tools/build_site.py` rebuilds all games, lessons, Sufara, the plan, duty, credits and home page.
  `tests/test_site_settings.py` rebuilds a copy with another mosque's details and checks nothing of Erie is left.
- `data/plan/plan.json` – the school year: dates, no-class days, groups and their tracks (Ilmihal books, Qur'an, Sufara,
  Tajwid), notes. `python3 tools/build_plan.py` (parents' copy) and `--private <file>` (tracker).
- The home page is built from `tools/templates/home.html` (`python3 tools/build_home.py`) – edit the game list there.
- `python3 tools/make_starter.py <empty folder>` makes the clean starter for other mosques (template repository
  `ademdeniz/maktab-starter`): no updates, duty names, Supabase project or Erie logo.

## Rebuilding

Every game can be rebuilt from this repository alone (`work/` is only a scratch folder):
```
python3 tools/rebuild_all.py            # rebuild all games and check they come out identical
```
Run it in a fresh clone after bigger changes to prove nothing depends on files that exist only on one computer.
