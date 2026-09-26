"""Build work/potraga-za-blagom-b1.en.html from work/potraga-za-blagom-b1.bs.html.
Run from project root:  python3 tools/tr/potraga-za-blagom-b1_build.py && python3 tools/skel.py build potraga-za-blagom-b1"""
import glob, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'potraga-za-blagom-b1'
src = open(os.path.join(ROOT, 'work', G + '.bs.html'), encoding='utf-8').read()

rows = {}
for f in sorted(glob.glob(os.path.join(ROOT, 'tools', 'tr', G + '_en*.txt'))):
    for line in open(f, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(' | ')]
        assert len(parts) == 6, line
        n = int(parts[0])
        assert n not in rows, n
        rows[n] = parts[1:]

i = src.index('const BANK=') + len('const BANK=')
j = src.index('];', i) + 1
assert json.dumps(json.loads(src[i:j]), ensure_ascii=False, separators=(',', ':')) == src[i:j]
bank = json.loads(src[i:j])
assert sorted(rows) == [x['n'] for x in bank], 'question numbers mismatch'
m, errors = {}, []
out = []
for x in bank:
    en = rows[x['n']]
    for bs, e in zip([x['q']] + x['a'], en):
        assert e, (x['n'], bs)
        assert "'" not in e and '"' not in e and '\\' not in e, (x['n'], e)
        if m.setdefault(bs, e) != e:
            errors.append(f'{x["n"]}: {bs!r} -> {m[bs]!r} vs {e!r}')
    assert len(set(en[1:])) == 4, ('duplicate options', x['n'], en)
    out.append({'n': x['n'], 'q': en[0], 'a': en[1:], 'correct': x['correct']})
assert not errors, '\n'.join(errors)
src = src[:i] + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + src[j:]

T = [
    ('<title>Potraga za blagom – B1</title>', '<title>Treasure Hunt – B1</title>'),
    ('<h1>🗺️ POTRAGA ZA BLAGOM – B1</h1>', '<h1>🗺️ TREASURE HUNT – B1</h1>'),
    ('<div class="sub">Baza B1: 451 pitanje • svaki put nova pitanja i izmiješani odgovori • Pripremio Abdo ef. Rekić</div>',
     '<div class="sub">Level B1: 451 questions • new questions and shuffled answers every time</div>'),
    ('⭐ Bodovi: <b', '⭐ Points: <b'),
    ('📍 Lokacija: <b', '📍 Location: <b'),
    ('alt="Ilustracija potrage za blagom"', 'alt="Treasure hunt illustration"'),
    ('>Riješi pitanja da nastaviš put.<', '>Answer the questions to continue your journey.<'),
    ('>Pritisni „Započni potragu“.<', '>Press “Start the hunt”.<'),
    ('>🔑 ZAPOČNI POTRAGU<', '>🔑 START THE HUNT<'),
    ('<h2>🏆 PRONAŠAO/LA SI BLAGO!</h2>', '<h2>🏆 YOU FOUND THE TREASURE!</h2>'),
    ('>🔄 Nova potraga<', '>🔄 New hunt<'),
    ('["🕌", "Džamija"], ["🪨", "Kameni prolaz"], ["🌴", "Palmina oaza"], ["🕳️", "Pećina"], ["⛰️", "Planina"], ["🏞️", "Rijeka"], ["🏛️", "Drevni grad"], ["🌊", "Izvor"], ["🏰", "Tvrđava"], ["💎", "Pećina blaga"]',
     '["🕌", "Mosque"], ["🪨", "Stone Pass"], ["🌴", "Palm Oasis"], ["🕳️", "Cave"], ["⛰️", "Mountain"], ["🏞️", "River"], ["🏛️", "Ancient City"], ["🌊", "Spring"], ["🏰", "Fortress"], ["💎", "Treasure Cave"]'),
    ('} • pitanje ${', '} • question ${'),
    ("'✅ Tačno! +10'", "'✅ Correct! +10'"),
    ("'❌ Netačno! −3'", "'❌ Wrong! −3'"),
    ("'Završio/la si svih 10 lokacija sa '+score+' bodova.'", "'You completed all 10 locations with '+score+' points.'"),
]
for bs, en in T:
    assert src.count(bs) == 1, bs
    src = src.replace(bs, en)
open(os.path.join(ROOT, 'work', G + '.en.html'), 'w', encoding='utf-8').write(src)
print('ok', len(out), 'questions')
