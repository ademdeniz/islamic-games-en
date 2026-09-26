# kviz-ilmihal-1-a3: table mode for the page text + transform() for the question bank.
# The bank (const BANKS = {...} JSON, 717 questions) is translated string-by-string from
# tools/tr/kviz-ilmihal-1-a3_en.tsv (one line per unique Bosnian string: bosnian<TAB>english),
# so identical Bosnian strings always get identical English and keys/answers/order stay untouched.
import json
import os

T = [
    ('<title>Kviz Ilmihal 1 – Nivo A3</title>', '<title>Ilmihal Quiz 1 – Level A3</title>'),
    ('<div class="title">KVIZ ILMIHAL 1</div>', '<div class="title">ILMIHAL QUIZ 1</div>'),
    ('NIVO A3 • pripremio Abdo ef. Rekić', 'LEVEL A3 • Islamic basics (Ilmihal)'),
    ('<h2>30 pitanja</h2>', '<h2>30 questions</h2>'),
    ('<p>5 iz A1 • 10 iz A2 • 15 iz A3</p>', '<p>5 from A1 • 10 from A2 • 15 from A3</p>'),
    ('<p>Tačno +10 bodova • netačno −3 boda</p>', '<p>Correct +10 points • wrong −3 points</p>'),
    ('>POČNI KVIZ<', '>START QUIZ<'),
    ('Bez vremenskog ograničenja • nema vraćanja na prethodno pitanje',
     'No time limit • no going back to the previous question'),
    ('onclick="audience()">Publika<', 'onclick="audience()">Audience<'),
    ('onclick="teacher()">Muallim<', 'onclick="teacher()">Teacher<'),
    ('<h1>KRAJ KVIZA</h1>', '<h1>END OF QUIZ</h1>'),
    ('>IGRAJ PONOVO<', '>PLAY AGAIN<'),
    ('`Pitanje ${i+1}/30`', '`Question ${i+1}/30`'),
    ('`Baza ${q.level}`', '`Level ${q.level}`'),
    ('`Bodovi: ${score}`', '`Points: ${score}`'),
    ('"Tačan odgovor! +10 bodova"', '"Correct answer! +10 points"'),
    ('"Netačan odgovor! −3 boda"', '"Wrong answer! −3 points"'),
    ('`Muallim smatra da je odgovor ${label}.`', '`The teacher (mu’allim) thinks the answer is ${label}.`'),
    ('`Ukupno: ${score} bodova`', '`Total: ${score} points`'),
    ('`Tačnih odgovora: ${correct} • Netačnih odgovora: ${wrong} • Maksimalno: 300 bodova`',
     '`Correct answers: ${correct} • Wrong answers: ${wrong} • Maximum: 300 points`'),
]

# Proper names of Bosnian poets (answer options to “Who wrote the mawlid poem …?”) and the poem’s title.
ALLOW = ['Bašagić', 'Ćazim', 'Ćatić', 'Rešad', 'Kadić', 'Handžić']

PREFIX = 'const BANKS='


def transform(src):
    here = os.path.dirname(os.path.abspath(__file__))
    table = {}
    for line in open(os.path.join(here, 'kviz-ilmihal-1-a3_en.tsv'), encoding='utf-8').read().splitlines():
        bs, en = line.split('\t')
        table[bs] = en
    lines = src.split('\n')
    k = next(n for n, l in enumerate(lines) if l.startswith(PREFIX))
    body = lines[k][len(PREFIX):-1]
    banks = json.loads(body)
    assert json.dumps(banks, ensure_ascii=False) == body, 'bank JSON does not round-trip'
    missing = set()

    def tr(s):
        if s not in table:
            missing.add(s)
            return s
        return table[s]
    for level in banks.values():
        for q in level:
            q['q'] = tr(q['q'])
            q['opts'] = {key: tr(v) for key, v in q['opts'].items()}
    assert not missing, f'{len(missing)} untranslated bank strings, e.g. {sorted(missing)[:3]}'
    lines[k] = PREFIX + json.dumps(banks, ensure_ascii=False) + ';'
    return '\n'.join(lines)
