# Weekly update for parents – prompt

Every Sunday after class, paste the prompt below into Claude Code, opened in `~/islamic-games-en`.
Change the date first. The kids count, homework and notes come from the teacher's tracker
(Maktab Year Plan, https://claude.ai/artifact/5E6BzFBCP4NA49mbT4P1KU): fill them in there first.

---

```
Make this week's maktab update for parents for Sunday <YYYY-MM-DD>.

1. Read my tracker (https://claude.ai/artifact/5E6BzFBCP4NA49mbT4P1KU) with ArtifactData:
   - weeks/<date>: kids_g1, kids_g2 (number of kids in each group), notes (homework and anything else for parents)
   - every weeks/* doc with noClass – Sundays I cancelled or re-opened
2. If the "No class" Sundays changed, update no_class in data/plan/plan.json (with a short reason parents can read)
   and rebuild the plan: python3 tools/build_plan.py --private <scratchpad>/plan.html
3. Write data/updates/<date>.json: kids {g1, g2}, homework {g1: [...], g2: [...]} and an optional note.
   Homework in plain English, one task per line, and say which book page. Leave out private notes.
4. python3 tools/build_update.py <date>, then run the tests (.venv/bin/python -m pytest tests/test_plan.py -q).
5. Show me the update. When I say yes: commit, push, and republish the tracker from the new plan.html.
6. Give me the link (https://ademdeniz.github.io/islamic-games-en/updates/<date>/), a short message
   I can paste into the parents' WhatsApp group, and send me updates/<date>/qr.png (the QR code picture).
```

---

## How it works

- **Lessons and games:** they come from the class plan (`tools/build_plan.py`), so the update always matches
  the plan. If a lesson moved, change the plan and the update follows.
- **Pages:** each update is `updates/<date>/index.html`. `updates/index.html` lists every update, and the
  parents' plan (`plan/`) links to that list.
- **Pages that aren't built:** a lesson without a page shows as plain text, not a link. Build the lesson
  (`data/lessons/...`, `tools/build_lessons.py`) before the update, and it becomes a link automatically.
- **Privacy:** never put children's names, photos or private notes in an update. It is a public page.
