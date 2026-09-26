"""Build work/islamski-escape-room-b1.en.html from work/islamski-escape-room-b1.bs.html.
Run from project root:
  python3 tools/tr/islamski-escape-room-b1_build.py && python3 tools/skel.py build islamski-escape-room-b1"""
import glob, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'islamski-escape-room-b1'
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

i = src.index('const QUESTIONS=') + len('const QUESTIONS=')
j = src.index('];\nlet score=', i) + 1
bank = json.loads(src[i:j])
assert json.dumps(bank, ensure_ascii=False, separators=(',', ':')) == src[i:j]
seen = []
for x in bank:
    for t in [x['q']] + x['options']:
        if t not in seen:
            seen.append(t)
missing = [k for k in range(len(seen)) if k not in tr]
extra = [k for k in tr if k >= len(seen)]
assert not missing and not extra, (missing[:20], extra)
m = {bs: tr[k] for k, bs in enumerate(seen)}
for bs, en in m.items():
    assert en.strip() == en and en, (bs, en)
    assert "'" not in en and '"' not in en and '\\' not in en, en
out = []
bad = []
for n, x in enumerate(bank):
    y = {'q': m[x['q']], 'options': [m[o] for o in x['options']], 'correct': x['correct']}
    if len(set(y['options'])) != len(y['options']):
        bad.append((n, x['options'], y['options']))
    out.append(y)
assert not bad, '\n'.join(map(str, bad))
src = src[:i] + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + src[j:]

T = [
    ('<title>Islamski Escape Room – Nivo B1</title>', '<title>Islamic Escape Room – Level B1</title>'),
    ('/* Interaktivne tačke koriste isključivo predmete koji već postoje na fotografiji. */',
     '/* The clickable spots use only objects that are already in the photo. */'),
    ('/* Predmeti na samoj fotografiji: viseći fenjer, zidni ćilim, bakreno posuđe na polici, čajnik na peći */',
     '/* Objects in the photo itself: hanging lantern, wall rug, copper pots on the shelf, teapot on the stove */'),
    ('/* Veća, ali i dalje kompaktna verzija: koristi skoro cijeli ekran */',
     '/* Bigger, but still compact version: uses almost the whole screen */'),
    ('/* Balans za jedan ekran: fotografija ostaje jasno vidljiva, pitanja dobijaju veci prostor. */',
     '/* One-screen balance: the photo stays clearly visible, the questions get more space. */'),
    ('/* Veća fotografija sobe uz zadržan kompaktan mobilni raspored. */',
     '/* Bigger room photo while keeping the compact mobile layout. */'),
    ('/* Prikazi CIJELU fotografiju, bez rezanja gornjeg fenjera. */',
     '/* Show the WHOLE photo, without cutting off the lantern at the top. */'),
    ('/* Zone su vezane za stvarne predmete na punoj fotografiji. */',
     '/* The zones are tied to the real objects in the full photo. */'),
    ('<h1>🔐 ISLAMSKI ESCAPE ROOM – NIVO B1</h1>', '<h1>🔐 ISLAMIC ESCAPE ROOM – LEVEL B1</h1>'),
    ('<small>Pripremio Abdo ef. Rekić • baza 451 pitanje</small>', '<small>Question bank: 451 questions</small>'),
    ('aria-label="Soba za escape room"', 'aria-label="Escape room"'),
    ('aria-label="Viseći fenjer"', 'aria-label="Hanging lantern"'),
    ('aria-label="Zidni ćilim"', 'aria-label="Wall rug"'),
    ('aria-label="Bakreno posuđe na polici"', 'aria-label="Copper pots on the shelf"'),
    ('aria-label="Čajnik na peći"', 'aria-label="Teapot on the stove"'),
    ('Pronađi predmet koji krije prvi trag. Dodirni predmete u sobi.',
     'Find the object that hides the first clue. Tap the objects in the room.'),
    ('<b>Pronašao/la si sve četiri cifre!</b>', '<b>You found all four digits!</b>'),
    ('<p>Unesi šifru redom kojim si ih otkrivao/la:</p>', '<p>Enter the code in the order you found them:</p>'),
    ('>OTKLJUČAJ<', '>UNLOCK<'),
    ('<h2>Vrata su otključana!</h2>', '<h2>The door is unlocked!</h2>'),
    ('<p>Čestitamo! Uspješno si završio/la Islamski escape room.</p>',
     '<p>Congratulations! You finished the Islamic Escape Room. MashaAllah!</p>'),
    ('⭐ Osvojeno bodova:', '⭐ Points earned:'),
    ('>IGRAJ PONOVO<', '>PLAY AGAIN<'),
    ("['viseći fenjer','zidni ćilim','bakreno posuđe na polici','čajnik na peći']",
     "['the hanging lantern','the wall rug','the copper pots on the shelf','the teapot on the stove']"),
    ('`🕵️ Trag ${stage+1}: dodirni <b>${names[order[stage]]}</b> na fotografiji i riješi 4 pitanja.`',
     '`🕵️ Clue ${stage+1}: tap <b>${names[order[stage]]}</b> in the photo and answer 4 questions.`'),
    ("'❌ Tu nema pravog traga. Pogledaj pažljivije sobu.'", "'❌ There is no clue here. Look at the room more carefully.'"),
    ("'✅ Pronašao/la si pravi predmet! Riješi 4 pitanja za trag.'", "'✅ You found the right object! Answer 4 questions to get the clue.'"),
    ('🔑 Cifra ${stage+1}:', '🔑 Digit ${stage+1}:'),
    ('`Pitanje ${solved+1}/4: ${base.q}`', '`Question ${solved+1}/4: ${base.q}`'),
    ("'✅ Tačno! +10'", "'✅ Correct! +10'"),
    ("'❌ Netačno! −3'", "'❌ Wrong! −3'"),
    ("'🔐 Sva četiri traga su pronađena. Složi cifre redom i otključaj vrata!'",
     "'🔐 All four clues have been found. Put the digits in order and unlock the door!'"),
    ("'❌ Pogrešna šifra. −3 boda. Pogledaj pronađene cifre.'", "'❌ Wrong code. −3 points. Look at the digits you found.'"),
]
for bs, en in T:
    assert src.count(bs) == 1, bs
    src = src.replace(bs, en)
open(os.path.join(ROOT, 'work', G + '.en.html'), 'w', encoding='utf-8').write(src)
print('ok', len(out), 'questions')
