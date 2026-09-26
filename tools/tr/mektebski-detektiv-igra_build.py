"""Build work/mektebski-detektiv-igra.en.html from work/mektebski-detektiv-igra.bs.html.
Run from project root:
  python3 tools/skel.py extract mektebski-detektiv-igra
  python3 tools/tr/mektebski-detektiv-igra_build.py && python3 tools/skel.py build mektebski-detektiv-igra"""
import glob, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'mektebski-detektiv-igra'
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

i = src.index('const DATA=') + len('const DATA=')
data, n = json.JSONDecoder().raw_decode(src[i:])
j = i + n
seen = []
for x in data:
    for t in [x['name']] + x['clues']:
        if t not in seen:
            seen.append(t)
missing = [k for k in range(len(seen)) if k not in tr]
extra = [k for k in tr if k >= len(seen)]
assert not missing and not extra, (missing[:20], extra)
m = {bs: tr[k] for k, bs in enumerate(seen)}
for en in m.values():
    assert "'" not in en and '"' not in en and '`' not in en and '<' not in en, en
# Shared Bosnian clues whose English pronoun must differ for a person answer
# (Bosnian 'Povezan je' works for both; English needs He vs It). Listed in ALLOW_INCONSISTENT.
OVERRIDE = {
    (145, 'Povezan je s ezanom.'): 'He is connected with the Adhan.',
    (164, "Povezan je s Kur'anom."): 'He is connected with the Qur’an.',
}
out = []
for x in data:
    y = dict(x)
    y['name'] = m[x['name']]
    y['clues'] = [OVERRIDE.get((x['n'], c), m[c]) for c in x['clues']]
    out.append(y)
used = {(x['n'], c) for x in data for c in x['clues']}
assert set(OVERRIDE) <= used, set(OVERRIDE) - used
names = [y['name'] for y in out]
assert len(set(names)) == len(names), 'duplicate answer names'
src = src[:i] + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + src[j:]

T = [
    ('<title>Mektebski detektiv</title>', '<title>Maktab Detective</title>'),
    ('🕵️ MEKTEBSKI DETEKTIV', '🕵️ MAKTAB DETECTIVE'),
    ('id="round">Slučaj 1/20<', 'id="round">Case 1/20<'),
    ('id="score">0 bodova<', 'id="score">0 points<'),
    ('id="sound">🔊 Zvuk<', 'id="sound">🔊 Sound<'),
    ('TRAG 1 • vrijedi 100 bodova', 'CLUE 1 • worth 100 points'),
    ('Pronađi tačno rješenje koristeći što manje tragova.', 'Find the right answer using as few clues as you can.'),
    ('🔎 Novi trag', '🔎 New clue'),
    ('🎯 Pogodi', '🎯 Guess'),
    ('id="continue">Sljedeći slučaj →<', 'id="continue">Next case →<'),
    ('<div class="footer">Pripremio Abdo ef. Rekić • Android & iPhone</div>', ''),
    ('`Slučaj ${idx+1}/20`', '`Case ${idx+1}/20`'),
    ('`TRAGOVI 1–${ci+1} • odgovor vrijedi ${pts[ci]} bodova`', '`CLUES 1–${ci+1} • answer is worth ${pts[ci]} points`'),
    ('`✅ Tačno! +${pts[ci]} bodova — ${current.name}`', '`✅ Correct! +${pts[ci]} points — ${current.name}`'),
    ('`❌ Nije tačno. Rješenje je: ${current.name}`', '`❌ Not correct. The answer is: ${current.name}`'),
    ("'Igraj ponovo ↻':'Sljedeći slučaj →'", "'Play again ↻':'Next case →'"),
    ("soundOn?'🔊 Zvuk':'🔇 Zvuk'", "soundOn?'🔊 Sound':'🔇 Sound'"),
]
for bs, en in T:
    assert src.count(bs) == 1, bs
    src = src.replace(bs, en)
c = '`${total} bodova`'
assert src.count(c) == 2
src = src.replace(c, '`${total} points`')
open(os.path.join(ROOT, 'work', G + '.en.html'), 'w', encoding='utf-8').write(src)
print('ok', len(out), 'cases')
