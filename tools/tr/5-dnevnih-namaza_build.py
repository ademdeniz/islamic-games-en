"""Build work/5-dnevnih-namaza.en.html from work/5-dnevnih-namaza.bs.html.
Run from project root:  python3 tools/skel.py extract 5-dnevnih-namaza && python3 tools/tr/5-dnevnih-namaza_build.py && python3 tools/skel.py build 5-dnevnih-namaza
Question bank translated in tools/tr/5-dnevnih-namaza_en.txt (one line per unique Bosnian string, in order of first use)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = '5-dnevnih-namaza'
src = open(os.path.join(ROOT, 'work', G + '.bs.html'), encoding='utf-8').read()

tr = {}
for line in open(os.path.join(ROOT, 'tools', 'tr', G + '_en.txt'), encoding='utf-8'):
    line = line.rstrip('\n')
    if line:
        k, en = line.split('\t', 1)
        tr[int(k)] = en

i = src.index('const BANK=') + len('const BANK=')
j = src.index('; const P=', i)
bank = json.loads(src[i:j])
assert json.dumps(bank, ensure_ascii=False) == src[i:j]
seen = []
for x in bank:
    for t in [x['q']] + x['opts']:
        if t not in seen:
            seen.append(t)
assert sorted(tr) == list(range(len(seen))), (len(tr), len(seen))
m = {bs: tr[k] for k, bs in enumerate(seen)}
for en in m.values():
    assert "'" not in en and '"' not in en, en
out = []
for x in bank:
    y = {'q': m[x['q']], 'opts': [m[o] for o in x['opts']], 'ans': x['ans']}
    assert len(set(y['opts'])) == 4, ('duplicate options', y)
    out.append(y)
src = src[:i] + json.dumps(out, ensure_ascii=False) + src[j:]

T = [
    ('<title>5 DNEVNIH NAMAZA</title>', '<title>THE 5 DAILY PRAYERS</title>'),
    ('<h1>5 DNEVNIH NAMAZA</h1>', '<h1>THE 5 DAILY PRAYERS</h1>'),
    ('<div class="sub">Pripremio: Abdo ef. Rekić</div>', ''),
    ('<div class="hero">ISLAMSKI KVIZ</div>', '<div class="hero">ISLAMIC QUIZ</div>'),
    ('<p>Svaka igra sadrži <b>30 nasumičnih pitanja</b>.</p>', '<p>Every game has <b>30 random questions</b>.</p>'),
    ('<p>Baza pitanja: <b>168</b></p>', '<p>Question bank: <b>168</b></p>'),
    ('>▶ POČNI IGRU<', '>▶ START GAME<'),
    ('>📚 BAZA PITANJA<', '>📚 QUESTION BANK<'),
    ('<span class="pill">Pitanje <b id="num">', '<span class="pill">Question <b id="num">'),
    ('<span class="pill gold">Bodovi: <b', '<span class="pill gold">Points: <b'),
    ('>👨‍🏫 Učitelj<', '>👨‍🏫 Teacher<'),
    ('>👥 Publika<', '>👥 Audience<'),
    ('>Nova igra<', '>New game<'),
    ('>← Nazad<', '>← Back<'),
    ('placeholder="Pretraži bazu pitanja..."', 'placeholder="Search the question bank..."'),
    ('<div class="footer">Offline • Android i iPhone • 30 sekundi po pitanju</div>',
     '<div class="footer">Offline • Android and iPhone • 30 seconds per question</div>'),
    ("soundOn?'🔊 Zvuk':'🔇 Bez zvuka'", "soundOn?'🔊 Sound':'🔇 No sound'"),
    ("fail('Vrijeme je isteklo!')", "fail('Time is up!')"),
    ("'Tačan odgovor!'", "'Correct answer!'"),
    ("fail('Netačan odgovor!')", "fail('Wrong answer!')"),
    ("'<br>Nova igra počinje od prvog pitanja.'", "'<br>A new game starts from the first question.'"),
    ("'🏆 ČESTITAMO!<br>Osvojili ste 1.000.000 bodova!'", "'🏆 CONGRATULATIONS!<br>You won 1.000.000 points!'"),
    ("'Završili ste svih 30 pitanja.'", "'You finished all 30 questions.'"),
    ("'Učitelj: '", "'Teacher: '"),
    ("'Publika: '", "'Audience: '"),
    ("'Prikazano: '+a.length+' od '+BANK.length+' pitanja'", "'Showing: '+a.length+' of '+BANK.length+' questions'"),
    ('"ok">Tačan odgovor: ', '"ok">Correct answer: '),
]
for bs, en in T:
    assert src.count(bs) == 1, bs
    src = src.replace(bs, en)
# sound button label appears twice in the markup
assert src.count('>🔊 Zvuk<') == 2
src = src.replace('>🔊 Zvuk<', '>🔊 Sound<')
open(os.path.join(ROOT, 'work', G + '.en.html'), 'w', encoding='utf-8').write(src)
print('ok', len(out), 'questions')
