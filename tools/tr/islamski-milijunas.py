# Islamski milijunaš -> Islamic Millionaire.
# UI strings are in T; the 717-question bank (const BANK=[...]) is translated by transform() using
# islamski-milijunas_bank.json, a {bosnian: english} map of every unique question/option string.
# islamski-milijunas-online reuses both (same bank, same UI strings).
import json
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
BANK_MAP = json.load(open(os.path.join(_HERE, 'islamski-milijunas_bank.json'), encoding='utf-8'))

DELETE = ['<div class="sub">Pripremio: Abdo ef. Rekić</div>']

# Bosniak authors' names (answer options about who wrote the mawlid poem).
ALLOW = ['Bašagić', 'Ćazim', 'Ćatić', 'Rešad', 'Kadić', 'Handžić']

T = [
    ('<title>Islamski milijunaš</title>', '<title>Islamic Millionaire</title>'),
    ('<h1>ISLAMSKI MILIJUNAŠ</h1>', '<h1>ISLAMIC MILLIONAIRE</h1>'),
    ('<div class="big">KVIZ: 30 PITANJA</div>', '<div class="big">QUIZ: 30 QUESTIONS</div>'),
    ('<b>Baza: 717 pitanja</b>', '<b>Question bank: 717 questions</b>'),
    ('▶ POČNI IGRU', '▶ START GAME'),
    ('📚 BAZA PITANJA', '📚 QUESTION BANK'),
    ('<span class="pill">Pitanje <b id="num">', '<span class="pill">Question <b id="num">'),
    ('<span class="pill gold">Bodovi: <span id="score">', '<span class="pill gold">Points: <span id="score">'),
    ('👨‍🏫 Učitelj</button>', '👨‍🏫 Teacher</button>'),
    ('👥 Publika</button>', '👥 Audience</button>'),
    ('<button id="restart">Nova igra</button>', '<button id="restart">New game</button>'),
    ('<button id="sound">🔊 Zvuk</button>', '<button id="sound">🔊 Sound</button>'),
    ('<button id="dbGame">Baza</button>', '<button id="dbGame">Questions</button>'),
    ('<button data-filter="ALL">SVA</button>', '<button data-filter="ALL">ALL</button>'),
    ('← Nazad', '← Back'),
    ('placeholder="Pretraži bazu pitanja..."', 'placeholder="Search the question bank..."'),
    ('Offline kviz • radi bez interneta', 'Offline quiz • works without the internet'),
    ("'Nivo '+x.level", "'Level '+x.level"),
    ("toLocaleString('bs-BA')", "toLocaleString('en-US')"),
    ("fail('Vrijeme je isteklo!')", "fail('Time is up!')"),
    ("'Tačan odgovor!'", "'Correct answer!'"),
    ("fail('Netačan odgovor!')", "fail('Wrong answer!')"),
    ("'<br>Nova igra počinje od prvog pitanja.'", "'<br>A new game starts from the first question.'"),
    ("'🏆 ČESTITAMO!<br>Osvojili ste 1.000.000 bodova!'", "'🏆 CONGRATULATIONS!<br>You have won 1,000,000 points!'"),
    ("'Završili ste svih 30 pitanja.'", "'You have finished all 30 questions.'"),
    ("textContent='1.000.000'", "textContent='1,000,000'"),
    ("'Učitelj: '+c.textContent", "'Teacher: '+c.textContent"),
    ("'<div class=\"audience\">Publika: '", "'<div class=\"audience\">Audience: '"),
    ("'🔊 Zvuk':'🔇 Bez zvuka'", "'🔊 Sound':'🔇 Sound off'"),
    ("'Prikazano: '+arr.length+' pitanja'", "'Showing: '+arr.length+' questions'"),
    ('<div class="ok">Tačan odgovor: \'', '<div class="ok">Correct answer: \''),
]

_BANK = re.compile(r'(const BANK=)(\[.*?\])(;?\s*\n)')


def transform(src):
    m = _BANK.search(src)
    assert m, 'BANK not found'
    bank = json.loads(m.group(2))
    assert json.dumps(bank, ensure_ascii=False) == m.group(2), 'BANK is not in json.dumps format'
    missing = {t for x in bank for t in [x['q']] + x['opts'] if t not in BANK_MAP}
    assert not missing, f'untranslated bank strings: {sorted(missing)[:5]}'
    for x in bank:
        x['q'] = BANK_MAP[x['q']]
        x['opts'] = [BANK_MAP[o] for o in x['opts']]
    return src[:m.start(2)] + json.dumps(bank, ensure_ascii=False) + src[m.end(2):]
