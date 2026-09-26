"""Build work/kviz-nivo-a1.en.html from work/kviz-nivo-a1.bs.html.
Run from project root:  python3 tools/tr/kviz-nivo-a1_build.py && python3 tools/skel.py build kviz-nivo-a1"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'kviz-nivo-a1'
src = open(os.path.join(ROOT, 'work', G + '.bs.html'), encoding='utf-8').read()
m = json.load(open(os.path.join(ROOT, 'tools', 'tr', G + '_map.json'), encoding='utf-8'))

UI = [
    ('<title>Kviz nivo A1 – Abdo ef. Rekić</title>', '<title>Quiz Level A1</title>'),
    ('/* VEĆA POLJA ZA PITANJE I ODGOVORE */', '/* BIGGER QUESTION AND ANSWER BOXES */'),
    ('/* MAKSIMALNO VELIKA POLJA — PROŠIRENA PREMA DNU EKRANA */', '/* LARGEST BOXES — STRETCHED TOWARDS THE BOTTOM OF THE SCREEN */'),
    ('/* MOBITEL: KVIZ PREKO CIJELOG EKRANA */', '/* PHONE: FULL-SCREEN QUIZ */'),
    ('/* DOTJERANA MOBILNA VERZIJA */', '/* POLISHED MOBILE VERSION */'),
    ('/* statistika kao uredna gornja traka */', '/* stats as a neat top bar */'),
    ('/* FINALNA USPRAVNA MOBILNA VERZIJA — ANDROID + iPHONE */', '/* FINAL PORTRAIT MOBILE VERSION — ANDROID + iPHONE */'),
    ('/* statistika */', '/* stats */'),
    ('/* pitanje */', '/* question */'),
    ('/* odgovori jedan ispod drugog — maksimalna čitljivost */', '/* answers one below the other — best readability */'),
    ('/* pomoći na samom dnu */', '/* lifelines at the very bottom */'),
    ('/* Vodoravno i dalje radi, ali uspravni prikaz je glavni */', '/* Landscape still works, but portrait is the main layout */'),
    ('id="progress">Pitanje 1 od 30<', 'id="progress">Question 1 of 30<'),
    ('<div class="statlabel">Pitanje</div>', '<div class="statlabel">Question</div>'),
    ('<div class="statlabel">Tačni odgovori</div>', '<div class="statlabel">Correct answers</div>'),
    ('<div class="statlabel">Bodovi</div>', '<div class="statlabel">Points</div>'),
    ('<div class="tip">Malo po malo<br>do velikog znanja!</div>', '<div class="tip">Little by little<br>to great knowledge!</div>'),
    ('<small>Uklanja dva netačna odgovora</small>', '<small>Removes two wrong answers</small>'),
    ('👥 Publika<small>Pogledaj šta kaže publika</small>', '👥 Audience<small>See what the audience says</small>'),
    ('🎓 Muallim pomoć<small>Savjet od muallima</small>', '🎓 Ask the teacher<small>Advice from the teacher (muʿallim)</small>'),
    ("help('50:50 je uklonio dva netačna odgovora.')", "help('50:50 removed two wrong answers.')"),
    ("help('<b>Publika:</b> '", "help('<b>Audience:</b> '"),
    ('help(`Muallim kaže: Mislim da je odgovor <b>', 'help(`The teacher says: I think the answer is <b>'),
    ('`Pitanje ${i+1} od 30`', '`Question ${i+1} of 30`'),
    ("'✓ Tačno!   +10 bodova'", "'✓ Correct!   +10 points'"),
    ("'✗ Netačno'", "'✗ Wrong'"),
    ('<div>Završeno svih 30 pitanja</div><h2>Konačni rezultat</h2>', '<div>All 30 questions finished</div><h2>Final score</h2>'),
    ('<div>${score} bodova</div>', '<div>${score} points</div>'),
    ('>Nova igra</button>', '>New game</button>'),
]
out = src
for bs, en in UI:
    assert out.count(bs) == 1, (out.count(bs), bs)
    out = out.replace(bs, en)

i = out.index('const BANK=') + len('const BANK=')
bank, end = json.JSONDecoder().raw_decode(out[i:])
assert len(bank) == 163
num = re.compile(r'[\d ,]+')
def tr(t):
    if num.fullmatch(t):
        return t
    en = m[t]
    assert '"' not in en and "'" not in en and '\\' not in en, en
    return en
new = []
for x in bank:
    y = dict(x)
    y['q'] = tr(x['q'])
    y['answers'] = [tr(a) for a in x['answers']]
    y['correctText'] = tr(x['correctText'])
    assert list(y) == list(x)
    assert y['answers'].index(y['correctText']) == x['answers'].index(x['correctText'])
    assert len(set(y['answers'])) == 4, (x['n'], y['answers'])
    new.append(y)
out = out[:i] + json.dumps(new, ensure_ascii=False) + out[i + end:]
open(os.path.join(ROOT, 'work', G + '.en.html'), 'w', encoding='utf-8').write(out)
print('ok', len(new))
