# Translating a game (Bosnian → English)

Audience: English-speaking Muslim children (maktab / weekend Islamic school, Bosniak community in Erie, PA).
Each game is a single self-contained HTML file in `original/<game>/`. The English version goes to `games/<game>/index.html`.

## Golden rule: change text, never code

Translate only what a child sees or hears: HTML text, JS/CSS string contents, and `title`/`alt`/`placeholder`/
`aria-label`/`value`/`content` attributes. Do **not** change code, markup, ids, class names, numbers, the number or
order of questions/answers/cards, or which answer is correct. `tests/test_games.py::test_code_unchanged` enforces this
by masking all text and requiring the rest of the file to be byte-identical (whitespace-insensitive).

- Keep string concatenation shape: `"Riječ ima "+n+" slova"` → `"The word has "+n+" letters"` (same pieces).
- Inside JS strings use the typographic apostrophe **’** (`Allah’s`, `Let’s`) so quotes never break the code.
- If the same Bosnian string appears in several places (e.g. a correct answer and the matching option), translate
  every copy identically — the game compares them with `===`.

## How to work

```
python3 tools/skel.py extract <game>     # work/<game>.bs.html = original with images/audio replaced by @@BLOB_n@@
```
Then either:
- **Table mode** (small games): write `tools/tr/<game>.py` with `T = [(bosnian, english), ...]` exact-string pairs,
  then `python3 tools/translate.py <game>`. Every Bosnian string must exist in the source or the script stops.
- **Direct mode** (big quiz files): `cp work/<game>.bs.html work/<game>.en.html`, translate that file in place (Edit tool
  or your own Python), then `python3 tools/skel.py build <game>`. Still create `tools/tr/<game>.py` for the settings below.

`build` restores the media, sets `lang="en"` and adds the community logo header. Never touch the `@@BLOB_n@@` tokens.
Then run the tests until they all pass:
```
.venv/bin/pytest tests --game <game> -q
```

### Per-game settings in `tools/tr/<game>.py` (all optional)
- `DELETE = ['<exact original snippet>']` — elements removed entirely (the author credit, see below). In table mode you
  can instead use a `T` entry whose English is `''`.
- `ALLOW = ['word']` — Bosnian/Arabic words kept **on purpose** (glossary terms like `abdest`, names). Keep it short and
  never use it to silence genuinely untranslated text.
- `ALLOW_INCONSISTENT = ['bosnian string']` — same Bosnian string deliberately translated differently in different
  places, only when that string is not used in any comparison.
- `STRUCTURAL = "reason"` — only if code truly must change (e.g. a word-search grid too small for the English word).
  Avoid it; it switches off the strongest test and forces a manual review.

## Content rules

1. **Remove the author credit** — any "Pripremio/Pripremila: Abdo ef. Rekić" line, button, or footer: delete the whole
   element (use `DELETE`), don't translate it. If the name is inside a longer JS string/text, just drop that part.
2. **No Arabic script.** Qur’an ayahs → English-style transliteration + English translation in *italics*
   (Sahih International). Get both from AlQuran.cloud, never from memory:
   `curl -s "https://api.alquran.cloud/v1/ayah/<surah>:<ayah>/editions/en.transliteration,en.sahih"`
   (or `/v1/surah/<n>/editions/...`). Duas/dhikr that are not Qur’an: standard English transliteration + short English meaning.
3. **Transliteration style:** Bosnian spellings → English conventions: dž→j, š→sh, č/ć→ch, j→y, v→w (in Arabic words),
   e→a where standard (`Kul huvallahu ehad` → `Qul huwallahu ahad`, `Elhamdulillah` → `Alhamdulillah`,
   `Subhanallah`, `Allahu ekber` → `Allahu akbar`, `Bismillah`, `Es-selamu alejkum` → `As-salamu alaykum`).
4. **Terminology** — keep the Arabic term, add English where a child may not know it (first mention is enough):

   | Bosnian | English |
   |---|---|
   | namaz | Salah (prayer) · sabah/podne/ikindija/akšam/jacija → Fajr/Dhuhr/Asr/Maghrib/Isha |
   | abdest / gusul / tejemum | Wudu (ablution) / Ghusl / Tayammum |
   | ezan / ikamet | Adhan / Iqamah |
   | džamija / mekteb / imam / hodža / efendija | mosque (masjid) / maktab / imam / teacher (hoca) / efendi |
   | Kur'an / sura / ajet / hadis / sunnet / farz / vadžib | Qur’an / surah / ayah / hadith / Sunnah / fard / wajib |
   | imanski šarti / islamski šarti | pillars of Iman (faith) / pillars of Islam |
   | melek, meleki | angel(s) (mala’ika) |
   | Džennet / Džehennem / kabur / Sudnji dan / Kijamet | Jannah / Jahannam / grave (qabr) / Day of Judgement / Qiyamah |
   | Allah dž.š. / Poslanik s.a.v.s. / a.s. / r.a. | Allah (SWT) / the Prophet (SAW) / (AS) / (RA) |
   | ramazan / bajram / post / zekat / hadž / kurban | Ramadan / Eid / fasting (sawm) / Zakah / Hajj / Qurbani |
   | sifati (Allahovi) / Esmaul-husna | Attributes of Allah (sifat) / Al-Asma’ al-Husna |
   | kitabi | books (kutub) · Tevrat/Zebur/Indžil → Tawrat/Zabur/Injil |
   | Mašallah / Inšallah / Bravo | MashaAllah / InshaAllah / Well done |
   | Prophet names | Ibrahim, Musa, Isa, Nuh, Adem→Adam, Jusuf→Yusuf, Jakub→Yaqub, Sulejman→Sulayman, Davud→Dawud |

5. **Kid-friendly English**, short sentences, same tone. Gendered forms like `Pronašao/la si` → `You found`.
6. **Word games must still work in English:** word-search words use only A–Z (no spaces/diacritics) and must fit the
   grid; if the grid's filler alphabet contains Bosnian letters (ČĆŽŠĐ), switch it to A–Z. Anagrams, ciphers, codes,
   letter counts, crossword answers, first-letter puzzles, "the word starts with…" hints: **re-derive them for the English
   words** so every puzzle is solvable. Escape-room / treasure-hunt codes must still be reachable from the English clues.
7. **Clues must not give the answer away** — e.g. don't add "(the Torah)" to a clue whose answer is TAWRAT.
8. **Images/audio:** never edit them. If the game has images that might contain words (title cards, signs, labels), look
   at a few (decode a blob from `work/<game>.blobs.json` to a file in your scratchpad and view it) and report any with
   Bosnian text. Audio is Qur’an recitation — keep it.
9. Don't edit shared files (`tools/skel.py`, `tools/translate.py`, `tests/`, `data/`, other games) and don't commit.
   Put any extra data you need in `tools/tr/<game>_*.{py,json,txt}`.
