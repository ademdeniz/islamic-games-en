# Game tests

```
.venv/bin/pytest tests                      # everything
.venv/bin/pytest tests --game kviz-namaz    # one game (repeat --game for more)
```

`test_games.py` checks each translated game against its Bosnian original:

| Test | Catches |
|---|---|
| `test_code_unchanged` | anything other than text changed — code, markup, numbers, dropped/added quiz entries |
| `test_repeated_strings_translated_consistently` | an answer translated differently from its matching option (breaks `===` checks) |
| `test_javascript_syntax` | broken JS, e.g. an unescaped apostrophe in `'That's'` |
| `test_runs_without_new_errors` | JS errors when loading and clicking through the game in a real browser |
| `test_media_preserved` | embedded images/sounds lost or corrupted |
| `test_no_bosnian_left` | untranslated Bosnian in visible text |
| `test_no_arabic_script` | Arabic script left where transliteration + English should be |
| `test_no_author_credit` | "Pripremio / Prepared by" byline |
| `test_is_english_and_branded` | `lang="en"` and community logo header |

`test_selfcheck.py` breaks a good game on purpose in each of those ways and asserts the checks notice.

Per-game exceptions live in `tools/tr/<game>.py`: `ALLOW` (deliberate Bosnian terms), `ALLOW_INCONSISTENT`,
`ALLOW_ARABIC`, and `STRUCTURAL = "reason"` for games whose code had to change (these get a manual review).
