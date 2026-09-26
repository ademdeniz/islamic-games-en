# Islamic Learning Games (English)

English versions of 42 maktab learning games (Qur’an, Salah, Iman, Ilmihal) for the Bosniak Islamic Community of Erie,
translated from the Bosnian originals at github.com/rekicabdo-bihac.

- `index.html` – home page listing the games (level filter, search, “Copy link” for homework)
- `games/<game>/index.html` – the English games (each is one self-contained file)
- `original/` – the Bosnian originals, unchanged
- `TRANSLATING.md` – translation rules and glossary · `tools/` – translation toolkit · `tests/` – checks every game

Run locally: `python3 -m http.server 8765` then open http://localhost:8765
Test: `.venv/bin/pytest tests`

Not linked from the home page: `islamski-milijunas-online` (its login sends data to the original author’s database)
and `maca-pripreme-za-namaz` (near-duplicate of `kviz-maca-namaz`).

Qur’an translation: Sahih International (via AlQuran.cloud) · Recitation: Mishary Rashid Alafasy
