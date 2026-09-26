"""Build work/escape-room-b1-sifra.en.html from work/escape-room-b1-sifra.bs.html.
Run from project root:  python3 tools/tr/escape-room-b1-sifra_build.py && python3 tools/skel.py build escape-room-b1-sifra"""
import glob, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'escape-room-b1-sifra'
src = open(os.path.join(ROOT, 'work', G + '.bs.html'), encoding='utf-8').read()

tr = {}
for f in sorted(glob.glob(os.path.join(ROOT, 'tools', 'tr', G + '_en*.txt'))):
    for line in open(f, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line:
            continue
        k, en = line.split('\t', 1)
        assert int(k) not in tr, k
        tr[int(k)] = en

i = src.index('const ALLQ=') + len('const ALLQ=')
j = src.index(';\nconst OBJECTS', i)
bank = json.loads(src[i:j])
assert json.dumps(bank, ensure_ascii=False) == src[i:j]
seen = []
for x in bank:
    for t in [x['q']] + x['opts'] + [x['correct']]:
        if t not in seen:
            seen.append(t)
missing = [k for k in range(len(seen)) if k not in tr]
extra = [k for k in tr if k >= len(seen)]
assert not missing and not extra, (missing[:20], extra)
m = {bs: tr[k] for k, bs in enumerate(seen)}
for bs, en in m.items():
    assert "'" not in en and '"' not in en and '\\' not in en, en
    assert en.strip() == en and en, (bs, en)
out = []
bad = []
for x in bank:
    y = {'q': m[x['q']], 'opts': [m[o] for o in x['opts']], 'correct': m[x['correct']]}
    assert y['opts'].index(y['correct']) == x['opts'].index(x['correct'])
    if len(set(y['opts'])) != len(y['opts']):
        bad.append((x, y['opts']))
    out.append(y)
assert not bad, '\n'.join(map(str, bad))
src = src[:i] + json.dumps(out, ensure_ascii=False) + src[j:]

# Hidden objects in the room picture ("Find: <name>")
OBJ = {
    'viseći fenjer kod lijevog prozora': 'the hanging lantern by the left window',
    'veliki saz na zidu lijevo od ormara': 'the big saz (lute) on the wall left of the cupboard',
    'veliki zidni sat desno gore': 'the big wall clock at the top right',
    'crveni fes lijevo': 'the red fez on the left',
    'mačku koja spava lijevo dole': 'the sleeping cat at the bottom left',
    'upaljenu svijeću na okruglom stolu': 'the lit candle on the round table',
    'šahovsku tablu desno': 'the chessboard on the right',
    'tesbih na okruglom stolu': 'the tasbih (prayer beads) on the round table',
    'crni kotlić iznad vatre u kaminu': 'the black pot over the fire in the fireplace',
    'zelenu bocu pored kamina': 'the green bottle next to the fireplace',
}
T = [('"name": "%s"' % k, '"name": "%s"' % v) for k, v in OBJ.items()] + [
    ('<title>Mektebski Escape Room – Nivo B1</title>', '<title>Maktab Escape Room – Level B1</title>'),
    ('<h1>🔐 Mektebski Escape Room – B1</h1>', '<h1>🔐 Maktab Escape Room – B1</h1>'),
    ('<div class="sig">Pripremio Abdo ef. Rekić</div>', ''),
    ('<span class="pill" id="found">Predmeti 0/10</span>', '<span class="pill" id="found">Items 0/10</span>'),
    ('<span class="pill" id="score">Bodovi 0</span>', '<span class="pill" id="score">Points 0</span>'),
    ('<div class="task" id="task">Pronađi: …</div>', '<div class="task" id="task">Find: …</div>'),
    ('alt="Bosanska soba puna skrivenih predmeta"', 'alt="A Bosnian room full of hidden objects"'),
    ('<div class="code">ŠIFRA: <span', '<div class="code">CODE: <span'),
    ('id="restart">Nova igra</button>', 'id="restart">New game</button>'),
    ("foundEl.textContent='Predmeti '+step", "foundEl.textContent='Items '+step"),
    ("scoreEl.textContent='Bodovi '+score;codeEl", "scoreEl.textContent='Points '+score;codeEl"),
    ("task.textContent='🔎 Pronađi: '+", "task.textContent='🔎 Find: '+"),
    ("'🎉 Svi predmeti pronađeni! Tvoja šifra je '", "'🎉 All items found! Your code is '"),
    ("'❌ To nije traženi predmet. Pronađi: '", "'❌ That is not the item you are looking for. Find: '"),
    ("qmeta.textContent='Predmet '+(step+1)+'/10 • pitanje '+(qi+1)+'/3'", "qmeta.textContent='Item '+(step+1)+'/10 • question '+(qi+1)+'/3'"),
    ("msg.textContent='✅ Tačno!'", "msg.textContent='✅ Correct!'"),
    ("msg.textContent='❌ Netačno. Pokušaj ponovo.'", "msg.textContent='❌ Wrong. Try again.'"),
    ("scoreEl.textContent='Bodovi '+score;\n}", "scoreEl.textContent='Points '+score;\n}"),
    ('Dio šifre je osvojen!', 'You won a part of the code!'),
    ("'Odlično! Riješena su sva 3 pitanja.'", "'Excellent! All 3 questions are solved.'"),
    ("qmeta.textContent='Predmet riješen'", "qmeta.textContent='Item solved'"),
    ("alert('Čestitamo! Konačna šifra: '", "alert('Congratulations! Final code: '"),
]
for bs, en in T:
    assert src.count(bs) == 1, bs
    src = src.replace(bs, en)
open(os.path.join(ROOT, 'work', G + '.en.html'), 'w', encoding='utf-8').write(src)
print('ok', len(out), 'questions')
