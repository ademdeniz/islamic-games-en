"""Build work/otkljucaj-vrata-dzamije.en.html from work/otkljucaj-vrata-dzamije.bs.html.
Run from project root:  python3 tools/tr/otkljucaj-vrata-dzamije_build.py && python3 tools/skel.py build otkljucaj-vrata-dzamije"""
import glob, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'otkljucaj-vrata-dzamije'
src = open(os.path.join(ROOT, 'work', G + '.bs.html'), encoding='utf-8').read()

tr = {}
for f in sorted(glob.glob(os.path.join(ROOT, 'tools', 'tr', G + '_en*.txt'))):
    for line in open(f, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line:
            continue
        k, en = line.split('\t', 1)
        assert int(k) not in tr, ('duplicate key', k)
        tr[int(k)] = en

i = src.index('const BANK=') + len('const BANK=')
j = src.index(';\nlet game', i)
bank = json.loads(src[i:j])
seen = []
for lvl in ('A1', 'A2'):
    for x in bank[lvl]:
        for t in [x['q']] + x['options']:
            if t not in seen:
                seen.append(t)
missing = [k for k in range(len(seen)) if k not in tr]
extra = [k for k in tr if k >= len(seen)]
assert not missing and not extra, (missing[:20], extra)
m = {bs: tr[k] for k, bs in enumerate(seen)}
for en in m.values():
    assert "'" not in en and '"' not in en and en.strip() == en and en, repr(en)
out = {}
for lvl in ('A1', 'A2'):
    out[lvl] = []
    for x in bank[lvl]:
        y = dict(x)
        y['q'] = m[x['q']]
        y['options'] = [m[o] for o in x['options']]
        assert len(set(y['options'])) == len(y['options']), ('duplicate options', x['q'], y['options'])
        out[lvl].append(y)
new = json.dumps(out, ensure_ascii=False)
assert json.dumps(bank, ensure_ascii=False) == src[i:j], 'bank formatting differs from json.dumps'
src = src[:i] + new + src[j:]

T = [
    ('<title>Otključaj vrata džamije – A1 + A2</title>', '<title>Unlock the Mosque Doors – A1 + A2</title>'),
    ('<div class="brand">🕌 Otključaj vrata džamije</div>', '<div class="brand">🕌 Unlock the Mosque Doors</div>'),
    ('<div class="by">15 pitanja • A1 + A2 • pripremio Abdo ef. Rekić</div>', '<div class="by">15 questions • A1 + A2</div>'),
    ('<div id="msg" class="msg">Tačan odgovor otključava jedan katanac.</div>', '<div id="msg" class="msg">Each correct answer unlocks one padlock.</div>'),
    ("$('msg').textContent='Tačan odgovor otključava jedan katanac.';", "$('msg').textContent='Each correct answer unlocks one padlock.';"),
    ('↻ Nova igra', '↻ New game'),
    ('<h2 id="finishTitle">Vrata su otključana!</h2>', '<h2 id="finishTitle">The doors are unlocked!</h2>'),
    ('>Igraj ponovo<', '>Play again<'),
    ('`Pitanje ${idx+1}/15 • Nivo ${x.level}`', '`Question ${idx+1}/15 • Level ${x.level}`'),
    ("'✓ Tačno! Jedna brava je otključana.'", "'✓ Correct! One lock is open.'"),
    ("'✗ Netačno. Tačan odgovor je označen zeleno.'", "'✗ Wrong. The correct answer is marked in green.'"),
    ("'✨ Sve brave su otključane — vrata se otvaraju!'", "'✨ All the locks are open — the doors are opening!'"),
    ("'Mašallah! Otključao si sva vrata!'", "'MashaAllah! You unlocked all the doors!'"),
    ('`15/15 tačnih odgovora • ${score} bodova. Pogledaj prelijepu prirodu i cvijeće iza otvorenih vrata.`',
     '`15/15 correct answers • ${score} points. Look at the beautiful nature and flowers behind the open doors.`'),
    ("'Još malo do otvorenih vrata!'", "'Almost there – the doors are nearly open!'"),
    ('`Tačnih odgovora: ${keys}/15 • Bodovi: ${score}. Vrata se potpuno otvaraju kada otključaš svih 15 katanaca.`',
     '`Correct answers: ${keys}/15 • Points: ${score}. The doors open fully when you unlock all 15 padlocks.`'),
]
for bs, en in T:
    assert src.count(bs) == 1, bs
    src = src.replace(bs, en)
open(os.path.join(ROOT, 'work', G + '.en.html'), 'w', encoding='utf-8').write(src)
print('ok', {k: len(v) for k, v in out.items()}, 'questions,', len(seen), 'strings')
