"""Build the weekly update for parents: updates/<date>/index.html (+ updates/index.html).

What each group learned that Sunday, with links to the lessons and games, homework, how many children came,
and what is coming next. The lessons come from the class plan (tools/build_plan.py); the rest from
data/updates/<date>.json:

  {"kids": {"g1": 9, "g2": 7},                  # null = not shown
   "homework": {"g1": ["..."], "g2": ["..."]},  # plain text, one line per task
   "note": ""}                                  # optional message at the top

  python3 tools/build_update.py 2026-09-27      # one week
  python3 tools/build_update.py                 # every week that has a data file
"""
import datetime as dt
import glob
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_plan as bp  # noqa: E402
from build_lessons_core import brand  # noqa: E402

SITE = bp.SITE
GROUPS = {'g1': ('Group 1', 'Ilmihal 2 & 3, Qur’an, Sufara & Tajwid', bp.G1), 'g2': ('Group 2', 'Ilmihal 1 & Sufara', bp.G2)}
E = html.escape


def nice(d, year=True):
    return dt.date.fromisoformat(d).strftime('%A, %B %-d, %Y' if year else '%A, %B %-d')


def item(it, cont=False):
    title = f'<a href="{it["url"]}">{E(it["title"])}</a>' if it['url'] else E(it['title'])
    meta = [f'book p. {it["page"]}' if it['kind'].startswith('Ilmihal') else '',
            'pick this page in Read Along' if it['kind'] == 'Qur’an' and it['url'] else '',
            'continued from last week' if cont else '']
    meta = ' · '.join(m for m in meta if m)
    return f'<li>{title}{f"<span class=m>{meta}</span>" if meta else ""}</li>'


def group_html(g, entries, games, homework):
    name, sub, tracks = GROUPS[g]
    rows = ''.join(f'<h4>{E(n)}</h4><ul>{"".join(item(it, c) for it, c in entries[t])}</ul>' for t, n in tracks if entries[t])
    hw = ''.join(f'<li>{E(h)}</li>' for h in homework)
    gm = ''.join(f'<a class=game href="{SITE}games/{s}/">🎮 {E(bp.data["games"][s]["t"])}</a>' for s in games)
    return (f'<section class=grp><h3>{name} <small>{E(sub)}</small></h3><p class=lbl>📖 Today we learned</p>{rows}'
            + (f'<p class=lbl>📝 Homework</p><ul class=hw>{hw}</ul>' if hw else '')
            + f'<p class=lbl>🎮 Practise at home</p><div class=games>{gm}</div></section>')


def build(day):
    info = json.load(open(os.path.join(ROOT, 'data', 'updates', day + '.json'), encoding='utf-8'))
    plan, cls = bp.schedule(), bp.class_days()
    assert day in plan, f'{day} is not a class day'
    w = cls.index(day)
    groups = []
    for g, (_, _, tracks) in GROUPS.items():
        entries = {t: plan[day][t] for t, _ in tracks}
        games = bp.games_for([e for t, _ in tracks for e in entries[t]], day, w, bp.BOOKS[g])
        groups.append(group_html(g, entries, games, info.get('homework', {}).get(g, [])))
    kids = info.get('kids') or {}
    att = ' · '.join(f'{GROUPS[g][0]}: <b>{n}</b> {"child" if n == 1 else "children"}' for g, n in kids.items() if n is not None)
    notes = [info['note']] if info.get('note') else []
    notes += [s['text'] for s in bp.data['standing'] if day >= s['from']]
    if bp.data['events'].get(day):
        notes.append('🌙 ' + bp.data['events'][day])
    nxt = cls[w + 1] if w + 1 < len(cls) else None
    coming = ''
    if nxt:
        coming = ''.join(f'<p class=lbl>{GROUPS[g][0]}</p><ul>{"".join(item(it) for t, _ in GROUPS[g][2] for it, c in plan[nxt][t] if not c)}</ul>'
                         for g in GROUPS)
        coming = f'<section class=card><h2>Next class: {nice(nxt, False)}</h2>{coming}</section>'
    soon = [(d, why) for d, why in sorted(bp.NO_CLASS.items()) if day < d <= (dt.date.fromisoformat(day) + dt.timedelta(weeks=8)).isoformat()]
    soon += [(d, '🌙 ' + ev) for d, ev in sorted(bp.data['events'].items()) if day < d <= (dt.date.fromisoformat(day) + dt.timedelta(weeks=8)).isoformat()]
    dates = ''.join(f'<li><b>{nice(d, False)}</b> – {E(why)}</li>' for d, why in sorted(soon))
    body = f'''<main>
<h1>Maktab Weekly Update</h1>
<p class=date>{nice(day)} · Class {w + 1} of {len(cls)}</p>
<p>Assalamu alaikum, dear parents! Here is what our children learned in the maktab today, with links to the lessons and games so you can practise together at home.</p>
{f'<p class=att>👧👦 Today in class – {att}</p>' if att else ''}
{''.join(f'<p class=note>📌 {E(n)}</p>' for n in notes)}
<div class=groups>{''.join(groups)}</div>
{coming}
{f'<section class=card><h2>Dates to remember</h2><ul>{dates}</ul></section>' if dates else ''}
<p class=tools><button id=share>🔗 Share this update</button> <a href="../../plan/">📅 The whole year’s plan</a> <a href="../">📰 All updates</a></p>
<p class=foot>Bosnian Islamic Community of Erie · Islamic dates are approximate.</p>
</main>'''
    page = TEMPLATE.replace('__TITLE__', f'Maktab Update – {dt.date.fromisoformat(day).strftime("%b %-d, %Y")}').replace('__BODY__', body)
    out = os.path.join(ROOT, 'updates', day, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(brand(page))
    return out


def build_index():
    days = sorted((os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'data', 'updates', '*.json'))), reverse=True)
    li = ''.join(f'<li><a href="{d}/">{nice(d)}</a></li>' for d in days)
    body = (f'<main><h1>Maktab Weekly Updates</h1><p>What our children learned each Sunday, with links to the lessons and games.</p>'
            f'<section class=card><ul class=list>{li}</ul></section><p class=tools><a href="../plan/">📅 The whole year’s plan</a></p>'
            f'<p class=foot>Bosnian Islamic Community of Erie</p></main>')
    open(os.path.join(ROOT, 'updates', 'index.html'), 'w', encoding='utf-8').write(
        brand(TEMPLATE.replace('__TITLE__', 'Maktab Weekly Updates').replace('__BODY__', body)))


TEMPLATE = open(os.path.join(ROOT, 'tools', 'templates', 'update.html'), encoding='utf-8').read()

if __name__ == '__main__':
    days = sys.argv[1:] or sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'data', 'updates', '*.json')))
    for d in days:
        print('built', os.path.relpath(build(d), ROOT))
    build_index()
