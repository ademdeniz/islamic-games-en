"""Make the clean starter copy that other mosques start from (the GitHub template ademdeniz/maktab-starter).

  python3 tools/make_starter.py <empty folder>

Copies everything in git, then removes what belongs to Erie only – weekly updates, parent duty names, the Supabase
project, the private tracker link, Erie's notes and logo – puts in a neutral name and a "your logo here" picture,
and rebuilds every page. Run the tests in the new folder before pushing it.
"""
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = {'name': 'Your Mosque Name', 'short_name': 'Your Mosque', 'logo': 'assets/logo.png',
        'url': 'https://ademdeniz.github.io/maktab-starter/', 'contact': ''}

README = """# Maktab website – starter

English learning games, Ilmihal lessons, Sufara (the Arabic letters), a year plan and weekly parent updates for a
maktab (Islamic weekend school) – ready to become **your mosque's** website.

**Start here:** follow the *Maktab Website – Setup Guide for Teachers* (you received it with the link to this page).
In short: click **Use this template** → create your own repository called `maktab` → turn on GitHub Pages →
open your copy in Claude Code and paste the setup prompt from the guide. No programming needed.

> Work only in **your own copy**. Never change or push to this starter or to the Erie website.

- Games: English versions of the Bosnian maktab games by Abdo ef. Rekić (used with permission).
- Ilmihal lessons: from the El-Kalem Ilmihal 1–3 books (used with permission). New lessons are added over the year.
- Qur'an: Sahih International; recitation Mishary Rashid Alafasy. See `credits/`.

For Claude Code: read `CLAUDE.md` first.
"""

CLAUDE_MD = """# CLAUDE.md – maktab website

A maktab teacher's own copy of the Maktab website (made from the starter of the Bosnian Islamic Community of Erie).
The teacher is usually not technical: one question at a time, plain words, show previews, never ask them to edit files.

## Rules
- Only ever commit and push to the teacher's OWN repository. Check `git remote -v` before every push; never push to,
  open a pull request on or change anything under `ademdeniz` (the Erie website and this starter).
- Never ask for or accept passwords, the Supabase secret key (`sb_secret_…`), a database password, a Gmail app password
  or card numbers. Only the Supabase Project URL and publishable key (`sb_publishable_…`) go into `supabase/config.json`.
- Children's privacy: no children's names, photos or contact details on any page; parents first name + last initial;
  weekly updates only say how many children came.
- Keep the credits (Abdo ef. Rekić – games; El-Kalem – Ilmihal books; Sahih International; Alafasy) – `credits/`.
- Qur'an quotes are Sahih International word for word (the tests check); never change religious content without asking.
- Run the tests (`.venv/bin/pytest tests`) before every publish; never publish with a failing test.

## How the site is built
- `site.json` – the mosque's name, short name, logo, website address, contact. After changing it (and the logo file):
  `python3 tools/build_site.py` rebuilds every page.
- `data/plan/plan.json` – the school year: start/end (the weekday of `start` is the class day), no-class days, groups and
  what each learns (tracks: ilmihal book 1–3, quran, sufara, tajwid), notes. Then `python3 tools/build_plan.py`.
- Lessons: `data/lessons/ilmihal-N/<book page>-<name>.json` → `python3 tools/build_lessons.py` (see README of the
  Erie site for the lesson format; book PDFs are needed to build new lessons and pictures).
- Weekly parent update: `data/updates/<date>.json` → `python3 tools/build_update.py <date>`. Sent updates are not rebuilt.
  Each update gets a QR code (button + `qr.png`); `updates/latest/` forwards to the newest one and `qr/` is the
  printable sheet whose QR code opens it (needs `segno` in the .venv).
- Parent duty page: `data/duty/parents.json` → `python3 tools/build_duty.py`.
- Publishing = commit + push to `main`; GitHub Pages updates in 2–5 minutes (Ctrl/Cmd+Shift+R to see it).
"""


def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f'FAILED {" ".join(cmd)}:\n{(r.stderr or r.stdout)[-1500:]}')
    return r.stdout


def logo(path):
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new('RGB', (1200, 300), 'white')
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((8, 8, 1192, 292), 30, outline=(15, 90, 63), width=8)
    d.ellipse((60, 60, 240, 240), fill=(15, 90, 63))
    d.ellipse((100, 50, 260, 230), fill='white')
    try:
        f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 84)
        s = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 40)
    except OSError:
        f = s = ImageFont.load_default()
    d.text((300, 70), 'YOUR MOSQUE LOGO', font=f, fill=(15, 90, 63))
    d.text((304, 180), 'replace assets/logo.png with your own', font=s, fill=(120, 110, 90))
    img.save(path)


def main(dst):
    if os.path.exists(dst) and os.listdir(dst):
        sys.exit(f'{dst} is not empty')
    files = run(['git', 'ls-files'], ROOT).splitlines()
    for f in files:
        if f.startswith(('data/updates/', 'updates/', 'tools/__pycache__/')) or f in ('docs/weekly-update-prompt.md',):
            continue
        if f.startswith('assets/logo-bz-erie'):
            continue
        os.makedirs(os.path.join(dst, os.path.dirname(f)), exist_ok=True)
        shutil.copy2(os.path.join(ROOT, f), os.path.join(dst, f))

    logo(os.path.join(dst, 'assets', 'logo.png'))
    json.dump(SITE, open(os.path.join(dst, 'site.json'), 'w'), ensure_ascii=False, indent=2)
    plan = json.load(open(os.path.join(dst, 'data', 'plan', 'plan.json'), encoding='utf-8'))
    plan['notes'] = []
    plan['no_class'] = {d: why for d, why in plan['no_class'].items() if 'Eid' in why or 'Winter' in why}
    json.dump(plan, open(os.path.join(dst, 'data', 'plan', 'plan.json'), 'w'), ensure_ascii=False, indent=1)
    duty = json.load(open(os.path.join(dst, 'data', 'duty', 'parents.json'), encoding='utf-8'))
    duty.update(g1=[], g2=[], done=[], start=plan['start'])
    json.dump(duty, open(os.path.join(dst, 'data', 'duty', 'parents.json'), 'w'), ensure_ascii=False, indent=2)
    json.dump({'url': '', 'publishable_key': '', 'note': 'Fill in your own Supabase Project URL and publishable key '
               '(setup guide, Step 6). Never the secret key.'}, open(os.path.join(dst, 'supabase', 'config.json'), 'w'), indent=2)
    for t in os.listdir(os.path.join(dst, 'supabase', 'email-templates')):   # sign-up / reset e-mails: neutral name and logo
        p = os.path.join(dst, 'supabase', 'email-templates', t)
        txt = open(p, encoding='utf-8').read()
        for old in ('Bosnian Islamic Community of Erie', 'Bosnian Islamic Community Erie'):
            txt = txt.replace(old, SITE['name'])
        txt = txt.replace('https://ademdeniz.github.io/islamic-games-en/assets/logo-bz-erie-web.jpg', SITE['url'] + SITE['logo'])
        txt = txt.replace('https://ademdeniz.github.io/islamic-games-en/', SITE['url'])
        open(p, 'w', encoding='utf-8').write(txt)
    open(os.path.join(dst, 'README.md'), 'w').write(README)
    open(os.path.join(dst, 'CLAUDE.md'), 'w').write(CLAUDE_MD)

    py = os.path.join(ROOT, '.venv', 'bin', 'python')
    run([py if os.path.exists(py) else sys.executable, 'tools/build_site.py'], dst)
    os.makedirs(os.path.join(dst, 'updates'), exist_ok=True)
    os.makedirs(os.path.join(dst, 'data', 'updates'), exist_ok=True)
    run([py if os.path.exists(py) else sys.executable, 'tools/build_update.py'], dst)   # empty list of updates
    print('starter ready in', dst)


if __name__ == '__main__':
    main(sys.argv[1])
