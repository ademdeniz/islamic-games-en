"""Build work/pcelica-skuplja-med.en.html from work/pcelica-skuplja-med.bs.html.
Run from project root:
  python3 tools/skel.py extract pcelica-skuplja-med && python3 tools/tr/pcelica-skuplja-med_build.py && python3 tools/skel.py build pcelica-skuplja-med
The question bank (const DB) is translated in tools/tr/pcelica-skuplja-med_en[1-3].txt:
one line per unique Bosnian string (question or option), '<index>\t<English>', in first-appearance order."""
import glob, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'pcelica-skuplja-med'
src = open(os.path.join(ROOT, 'work', G + '.bs.html'), encoding='utf-8').read()

tr = {}
for f in sorted(glob.glob(os.path.join(ROOT, 'tools', 'tr', G + '_en*.txt'))):
    for line in open(f, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line:
            continue
        k, en = line.split('\t', 1)
        assert int(k) not in tr, ('duplicate index', k)
        tr[int(k)] = en

i = src.index('const DB=') + len('const DB=')
j = src.index('];let game', i) + 1
db = json.loads(src[i:j])
assert json.dumps(db, ensure_ascii=False) == src[i:j]
seen = []
for x in db:
    for t in [x['q']] + x['opts']:
        if t not in seen:
            seen.append(t)
missing = [k for k in range(len(seen)) if k not in tr]
extra = [k for k in tr if k >= len(seen)]
assert not missing and not extra, (missing[:20], extra)
m = {bs: tr[k] for k, bs in enumerate(seen)}
for en in m.values():
    assert en.strip() == en and en, repr(en)
    assert "'" not in en and '"' not in en and '\\' not in en, en
out = []
for x in db:
    y = dict(x)
    y['q'] = m[x['q']]
    y['opts'] = [m[o] for o in x['opts']]
    assert len(set(y['opts'])) == len(y['opts']), ('duplicate options', x, y['opts'])
    out.append(y)
assert len(out) == 321
src = src[:i] + json.dumps(out, ensure_ascii=False) + src[j:]

T = [
    ('<title>Pčelica skuplja med – A3</title>', '<title>The Little Bee Collects Honey – A3</title>'),
    ('<h1>🐝 Pčelica skuplja med 🍯</h1>', '<h1>🐝 The Little Bee Collects Honey 🍯</h1>'),
    ('NIVO A3 • BAZA OD 321 PITANJA • 30 PITANJA PO IGRI', 'LEVEL A3 • BANK OF 321 QUESTIONS • 30 QUESTIONS PER GAME'),
    ('SAĆE — TAČAN ODGOVOR = JEDNO POLJE MEDA', 'HONEYCOMB — CORRECT ANSWER = ONE CELL OF HONEY'),
    ('<h2>Bravo!</h2>', '<h2>Well done!</h2>'),
    ('>Igraj ponovo<', '>Play again<'),
    ('`Pitanje ${idx+1}/30`', '`Question ${idx+1}/30`'),
    ('"Tačno! Pčelica nosi nektar prema kući! 🐝🍯"', '"Correct! The little bee is carrying nectar home! 🐝🍯"'),
    ('"Netačno — označen je tačan odgovor."', '"Wrong — the correct answer is highlighted."'),
    ('`Napunio/la si <b>${honey} od 30</b> polja saća.<br>Bodovi: <b>${score}</b><br>Baza A3: 321 pitanje.`',
     '`You filled <b>${honey} of 30</b> honeycomb cells.<br>Points: <b>${score}</b><br>Bank A3: 321 questions.`'),
]
for bs, en in T:
    assert src.count(bs) == 1, bs
    src = src.replace(bs, en)
assert src.count('`Bodovi: ${score}`') == 2
src = src.replace('`Bodovi: ${score}`', '`Points: ${score}`')
open(os.path.join(ROOT, 'work', G + '.en.html'), 'w', encoding='utf-8').write(src)
print('ok', len(out), 'questions')
