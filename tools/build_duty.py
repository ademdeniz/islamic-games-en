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


TBA = 'To be announced'


def rota():
    """First round only: every parent once. When a group runs out first, its slots are “to be announced” –
    new families may join, and the next round is posted later."""
    done = {x[g] for x in P.get('done', []) for g in ('g1', 'g2') if x.get(g)}
    g1, g2 = [p for p in P['g1'] if p not in done], [p for p in P['g2'] if p not in done]   # already had their turn
    n = max(len(g1), len(g2))
    days = [d for d in bp.class_days() if d >= P['start']][:n]
    return [(d, g1[w] if w < len(g1) else TBA, g2[w] if w < len(g2) else TBA) for w, d in enumerate(days)]


def build():
    rows = ''.join(f'<tr data-d="{x["date"]}" class=done><td class=d>{dt.date.fromisoformat(x["date"]).strftime("%b %-d, %Y")} ✓</td>'
                   f'<td>{E(x.get("g1") or "—")}</td><td>{E(x.get("g2") or "—")}</td></tr>' for x in P.get('done', []))
    rows += ''.join(f'<tr data-d="{d}"><td class=d>{dt.date.fromisoformat(d).strftime("%b %-d, %Y")}</td>'
                   f'<td{" class=tba" if a == TBA else ""}>{E(a)}</td><td{" class=tba" if b == TBA else ""}>{E(b)}</td></tr>' for d, a, b in rota())
    last = rota()[-1][0]
    off = ''.join(f'<li><b>{dt.date.fromisoformat(d).strftime("%b %-d")}</b> – {E(why.removeprefix("No class – "))}</li>'
                  for d, why in sorted(bp.NO_CLASS.items()) if P['start'] <= d <= last)
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
<div class=card><b>📅 What comes next</b><p>This is the <b>first round</b> – every family once{" (✓ = already done – thank you!)" if P.get("done") else ""}. More families may still join, so the <b>next round will be posted after {dt.date.fromisoformat(last).strftime("%B %-d")}</b>, with everyone included.</p></div>
<p class=foot>Bosnian Islamic Community of Erie</p>
</main>'''
    page = open(os.path.join(ROOT, 'tools', 'templates', 'duty.html'), encoding='utf-8').read().replace('__BODY__', body)
    os.makedirs(os.path.join(ROOT, 'duty'), exist_ok=True)
    open(os.path.join(ROOT, 'duty', 'index.html'), 'w', encoding='utf-8').write(brand(page))


if __name__ == '__main__':
    build()
    print(len(rota()), 'Sundays')
