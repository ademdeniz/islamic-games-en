"""Build duty/index.html: which two parents bring pizza and stay the whole day each Sunday (one from each group).

  python3 tools/build_duty.py

Parents come from data/duty/parents.json and rotate in order, one per group per class Sunday (from "start").
Sundays without class (data/plan/no_class.json) are skipped.
"""
import datetime as dt
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_plan as bp  # noqa: E402
from build_lessons_core import brand  # noqa: E402

P = json.load(open(os.path.join(ROOT, 'data', 'duty', 'parents.json'), encoding='utf-8'))
E = html.escape


def rota():
    days = [d for d in bp.class_days() if d >= P['start']]
    return [(d, P['g1'][w % len(P['g1'])], P['g2'][w % len(P['g2'])]) for w, d in enumerate(days)]


def build():
    rows = ''.join(f'<tr data-d="{d}"><td class=d>{dt.date.fromisoformat(d).strftime("%b %-d, %Y")}</td>'
                   f'<td>{E(a)}</td><td>{E(b)}</td></tr>' for d, a, b in rota())
    off = ''.join(f'<li><b>{dt.date.fromisoformat(d).strftime("%b %-d")}</b> – {E(why.removeprefix("No class – "))}</li>'
                  for d, why in sorted(bp.NO_CLASS.items()) if d >= P['start'])
    each = P['pizzas']['each']
    body = f'''<main>
<h1>🍕 Sunday Pizza &amp; Parent Duty</h1>
<p class=sub>Bosnian Islamic Community of Erie · Maktab 2026–27</p>
<div class=card>
<p>Every Sunday <b>two parents</b> – one from Group 1 and one from Group 2 – <b>stay at the maktab for the whole day of classes</b>, for our children’s safety, and <b>bring pizza</b> for lunch.</p>
<ul>
<li>We need <b>{P['pizzas']['total']} pizzas</b> every Sunday: each parent brings <b>{each}</b> (half each).</li>
<li>📌 <b>The Imam will let you know if we need more or fewer.</b></li>
<li>Can’t make your Sunday? Swap with another parent and let the Imam know.</li>
</ul>
</div>
<p class=tools><button id=me>⬇️ Next Sunday</button></p>
<div class=wrap><table>
<thead><tr><th>Sunday</th><th>Group 1 parent<br><small>stays · brings {each} pizzas</small></th><th>Group 2 parent<br><small>stays · brings {each} pizzas</small></th></tr></thead>
<tbody>{rows}</tbody></table></div>
{f'<div class=card><b>No class (no duty):</b><ul>{off}</ul></div>' if off else ''}
<p class=foot>Bosnian Islamic Community of Erie. If a new family joins, they are added at the end of the list.</p>
</main>'''
    page = open(os.path.join(ROOT, 'tools', 'templates', 'duty.html'), encoding='utf-8').read().replace('__BODY__', body)
    os.makedirs(os.path.join(ROOT, 'duty'), exist_ok=True)
    open(os.path.join(ROOT, 'duty', 'index.html'), 'w', encoding='utf-8').write(brand(page))


if __name__ == '__main__':
    build()
    print(len(rota()), 'Sundays')
