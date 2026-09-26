"""Build work/kviz-namaz.en.html from work/kviz-namaz.bs.html.
Run from project root:  python3 tools/tr/kviz-namaz_build.py && python3 tools/skel.py build kviz-namaz"""
import glob, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'kviz-namaz'
src = open(os.path.join(ROOT, 'work', G + '.bs.html'), encoding='utf-8').read()

tr = {}
for f in sorted(glob.glob(os.path.join(ROOT, 'tools', 'tr', G + '_en*.txt'))):
    for line in open(f, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line:
            continue
        k, en = line.split('\t', 1)
        tr[int(k)] = en.replace('\\n', '\n')

i = src.index('const BANK=') + len('const BANK=')
j = src.index('];\nconst TOTAL', i) + 1
bank = json.loads(src[i:j])
seen = []
for x in bank:
    for t in [x['q']] + x['options'] + [x['correctText']]:
        if t not in seen:
            seen.append(t)
missing = [k for k in range(len(seen)) if k not in tr]
extra = [k for k in tr if k >= len(seen)]
assert not missing and not extra, (missing[:20], extra)
m = {bs: tr[k] for k, bs in enumerate(seen)}
for bs, en in m.items():
    assert ('\n' in bs) == ('\n' in en), (bs, en)
    assert "'" not in en and '"' not in en, en
out = []
for x in bank:
    y = dict(x)
    y['q'] = m[x['q']]
    y['options'] = [m[o] for o in x['options']]
    y['correctText'] = m[x['correctText']]
    assert y['correctText'] in y['options']
    assert len(set(y['options'])) == len(y['options']), ('duplicate options', x['n'], y['options'])
    out.append(y)
src = src[:i] + json.dumps(out, ensure_ascii=False) + src[j:]

T = [
    ('<meta name="apple-mobile-web-app-title" content="Kviz Namaz">', '<meta name="apple-mobile-web-app-title" content="Salah Quiz">'),
    ('<title>Kviz Namaz</title>', '<title>Salah Quiz</title>'),
    ('<h1>ISLAMSKI KVIZ – NAMAZ</h1>', '<h1>ISLAMIC QUIZ – SALAH (PRAYER)</h1>'),
    ('<div class="sub">Pripremio: Abdo ef. Rekić</div>', ''),
    ('<p><b>30 pitanja</b> bira se iz baze od <b>472 pitanja</b>, iz svih lekcija. Za svako pitanje imaš <b>30 sekundi</b>. Tačni odgovori svaki put mijenjaju mjesto, a pitanja automatski prelaze dalje.</p>',
     '<p><b>30 questions</b> are picked from a bank of <b>472 questions</b>, from all the lessons. You have <b>30 seconds</b> for each question. The correct answers change place every time, and the quiz moves on to the next question automatically.</p>'),
    ('>POČNI KVIZ<', '>START QUIZ<'),
    ('Svako novo pokretanje bira novu kombinaciju pitanja.', 'Every new game picks a new mix of questions.'),
    ('<div class="stat">Pitanje<b', '<div class="stat">Question<b'),
    ('<div class="stat">Bodovi<b', '<div class="stat">Points<b'),
    ('<div class="stat">Vrijeme<b', '<div class="stat">Time<b'),
    ('<div>ZAVRŠEN KVIZ</div>', '<div>QUIZ FINISHED</div>'),
    ('>IGRAJ PONOVO<', '>PLAY AGAIN<'),
    ("let lesson='OSTALO';", "let lesson='OTHER';"),
    ("'Lekcija: '+item.lesson", "'Lesson: '+item.lesson"),
    ("'Tačan odgovor!'", "'Correct answer!'"),
    ("'Netačan odgovor.'", "'Wrong answer.'"),
    ("'Vrijeme je isteklo!'", "'Time is up!'"),
    ("'Uspjeh: '+", "'Score: '+"),
    ('// Najmanje jedno pitanje iz svake lekcije.', '// At least one question from every lesson.'),
    ('// Preostala mjesta popunjavaju se drugim, nasumičnim pitanjima iz različitih lekcija.', '// The remaining places are filled with other random questions from different lessons.'),
]
for bs, en in T:
    assert src.count(bs) == 1, bs
    src = src.replace(bs, en)
open(os.path.join(ROOT, 'work', G + '.en.html'), 'w', encoding='utf-8').write(src)
print('ok', len(out), 'questions')
