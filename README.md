# Islamic Learning Games (English)

English versions of 42 maktab learning games (Qur’an, Salah, Iman, Ilmihal) for the Bosnian Islamic Community of Erie,
translated from the Bosnian originals at github.com/rekicabdo-bihac.

- `index.html` – home page listing the games (level filter, search, “Copy link” for homework)
- `games/<game>/index.html` – the English games (each is one self-contained file)
- `original/` – the Bosnian originals, unchanged
- `TRANSLATING.md` – translation rules and glossary · `tools/` – translation toolkit · `tests/` – checks every game

Run locally: `python3 -m http.server 8765` then open http://localhost:8765
Test: `.venv/bin/pytest tests`

`islamski-milijunas-online` uses our own Supabase project (`supabase/config.json`, publishable key only).
Database setup: run `supabase/schema.sql` in the Supabase SQL Editor; test it locally with `tests/run_supabase_test.sh`.
Youth Gathering 2026 parent waiver (separate from the games, not linked from the home page):
`waiver/index.html` – the form parents sign on their phone · `waiver/admin.html` – signed waivers, print, CSV (admin only).
Database setup: run `supabase/waiver.sql` in the SQL Editor after `schema.sql`; it is tested by the same script.
Not linked from the home page: `maca-pripreme-za-namaz` (near-duplicate of `kviz-maca-namaz`) and `el-fatiha`
(replaced by `learn-surahs-by-heart`, which includes Al-Fatiha).

New games (not translations): `games/learn-surahs-by-heart` (`tools/fetch_hifz.py` + `tools/build_hifz.py`) and the rebuilt
`games/citaj-kuran` Read Along (`tools/fetch_readalong.py` + `tools/build_citaj_kuran.py`).

Qur’an translation: Sahih International (via AlQuran.cloud) · Recitation: Mishary Rashid Alafasy
