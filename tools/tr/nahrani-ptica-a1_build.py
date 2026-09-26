"""Build work/nahrani-ptica-a1.en.html from work/nahrani-ptica-a1.bs.html.
Run from project root:  python3 tools/tr/nahrani-ptica-a1_build.py && python3 tools/skel.py build nahrani-ptica-a1
The 163-question bank is the same as kviz-nivo-a1; translations are in tools/tr/nahrani-ptica-a1_map.json."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'nahrani-ptica-a1'
src = open(os.path.join(ROOT, 'work', G + '.bs.html'), encoding='utf-8').read()
m = json.load(open(os.path.join(ROOT, 'tools', 'tr', G + '_map.json'), encoding='utf-8'))

UI = [
    ('<title>Nahrani ptića – A1</title>', '<title>Feed the Baby Birds – A1</title>'),
    ('<h1>🐦 Nahrani ptića</h1>', '<h1>🐦 Feed the Baby Birds</h1>'),
    ('NIVO A1 • BAZA OD 163 PITANJA • 30 PITANJA PO IGRI', 'LEVEL A1 • 163 QUESTIONS IN TOTAL • 30 QUESTIONS PER GAME'),
    ('alt="Gnijezdo sa ptićima"', 'alt="Nest with baby birds"'),
    ('alt="Ptičica"', 'alt="Little bird"'),
    ('alt="Ptičica koja nosi hranu"', 'alt="Little bird carrying food"'),
    ('NAHRANI 30 PUTA PTIĆE — TAČAN ODGOVOR = HRANA U GNIJEZDO', 'FEED THE BABY BIRDS 30 TIMES — CORRECT ANSWER = FOOD IN THE NEST'),
    ('alt="Vesela ptičica"', 'alt="Happy little bird"'),
    ('<h2>Bravo!</h2>', '<h2>Well done!</h2>'),
    ('>Igraj ponovo</button>', '>Play again</button>'),
    ('`Nahranio/la si ptiće <b>${count} puta</b>.<br>Bodovi: <b>${score}</b><br>Baza A1: 163 pitanja.`',
     '`You fed the baby birds <b>${count} times</b>.<br>Points: <b>${score}</b><br>A1 question bank: 163 questions.`'),
    ('`Pitanje ${idx+1}/30`', '`Question ${idx+1}/30`'),
    ('`Bodovi: ${score}`', '`Points: ${score}`'),
    ('"Tačno! Ptičica nosi hranu ptićima! 🐦🌾"', '"Correct! The little bird takes food to the babies! 🐦🌾"'),
    ('"Netačno — označen je tačan odgovor."', '"Wrong — the correct answer is marked."'),
]
out = src
for bs, en in UI:
    n = out.count(bs)
    assert n >= 1, bs
    out = out.replace(bs, en)

i = out.index('const DB=') + len('const DB=')
db, end = json.JSONDecoder().raw_decode(out[i:])
assert len(db) == 163
num = re.compile(r'[\d ,]+')
def tr(t):
    if num.fullmatch(t):
        return t
    en = m[t]
    assert '"' not in en and '\\' not in en, en
    return en
new = []
for x in db:
    y = {'q': tr(x['q']), 'opts': [tr(o) for o in x['opts']], 'ans': x['ans']}
    assert list(y) == list(x) and len(set(y['opts'])) == 4
    new.append(y)
assert json.dumps(db, ensure_ascii=False) == out[i:i + end]
out = out[:i] + json.dumps(new, ensure_ascii=False) + out[i + end:]
open(os.path.join(ROOT, 'work', G + '.en.html'), 'w', encoding='utf-8').write(out)
print('ok', len(new))
