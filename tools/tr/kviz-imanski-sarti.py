# kviz-imanski-sarti: table mode for the page text + transform() for the question bank.
# The bank (const BANK=[...] JSON, 213 questions) is translated string-by-string from
# tools/tr/kviz-imanski-sarti_en.tsv (one line per unique Bosnian string: bosnian<TAB>english),
# so identical Bosnian strings always get identical English, and keys/answers/order stay untouched.
import json
import os
import re

T = [
    ('content="Imanski šarti"', 'content="Pillars of Iman"'),
    ('<title>Imanski šarti</title>', '<title>Pillars of Iman</title>'),
    ('<h1>IMANSKI ŠARTI</h1>', '<h1>PILLARS OF IMAN</h1>'),
    ('<h2>Kviz – 30 pitanja</h2>', '<h2>Quiz – 30 questions</h2>'),
    ('<p>Baza sadrži samo pitanja o imanskim šartima i Allahovim svojstvima: <b>213 pitanja</b>.</p>',
     '<p>The question bank covers the pillars of Iman (faith) and the attributes of Allah (sifat): <b>213 questions</b>.</p>'),
    ('<p>Vrijeme za svako pitanje: <b>30 sekundi</b>. Mjesto tačnog odgovora se nasumično mijenja.</p>',
     '<p>Time for each question: <b>30 seconds</b>. The position of the correct answer changes randomly.</p>'),
    ('<p class="small">iPhone: otvorite kviz u Safariju. Kada bude postavljen online, možete izabrati <b>Share → Add to Home Screen</b> za ikonu na početnom ekranu.</p>',
     '<p class="small">iPhone: open the quiz in Safari. Once it is online, you can choose <b>Share → Add to Home Screen</b> to get an icon on your home screen.</p>'),
    ('>POKRENI KVIZ<', '>START QUIZ<'),
    ('>BAZA PITANJA<', '>QUESTION BANK<'),
    ('>🔊 ZVUK: UKLJUČEN<', '>🔊 SOUND: ON<'),
    ("'🔊 ZVUK: UKLJUČEN':'🔇 ZVUK: ISKLJUČEN'", "'🔊 SOUND: ON':'🔇 SOUND: OFF'"),
    ('>NOVA IGRA<', '>NEW GAME<'),
    ('>POČETNI EKRAN<', '>HOME SCREEN<'),
    ('<h2>Baza pitanja (213)</h2>', '<h2>Question bank (213)</h2>'),
    ('placeholder="Pretraži pitanja..."', 'placeholder="Search questions..."'),
    ('>NAZAD<', '>BACK<'),
    ("'Kviz završen!'", "'Quiz finished!'"),
    ("'<h2>Rezultat: '", "'<h2>Result: '"),
    ("'Pitanje '", "'Question '"),
    ("'Bodovi: '", "'Points: '"),
    ("Tačan odgovor: <b>", "Correct answer: <b>"),
]
DELETE = ['<div class="sub">Pripremio: Abdo ef. Rekić</div>']

PREFIX = 'const BANK='


def transform(src):
    here = os.path.dirname(os.path.abspath(__file__))
    table = {}
    for line in open(os.path.join(here, 'kviz-imanski-sarti_en.tsv'), encoding='utf-8').read().splitlines():
        bs, en = line.split('\t')
        assert bs not in table, f'duplicate TSV key {bs!r}'
        table[bs] = en
    lines = src.split('\n')
    k = next(n for n, l in enumerate(lines) if l.startswith(PREFIX))
    body = lines[k][len(PREFIX):-1]
    bank = json.loads(body)
    assert json.dumps(bank, ensure_ascii=False) == body, 'bank JSON does not round-trip'
    missing = set()

    def tr(s):
        if s in table:
            return table[s]
        if not re.search(r'[A-Za-zČĆŽŠĐčćžšđ]', s):  # pure numbers stay as they are
            return s
        missing.add(s)
        return s
    for q in bank:
        q['cat'] = tr(q['cat'])
        q['q'] = tr(q['q'])
        q['opts'] = [tr(o) for o in q['opts']]
        assert len(set(q['opts'])) == len(q['opts']), f'options collapsed: {q["opts"]}'
    assert not missing, f'{len(missing)} untranslated bank strings, e.g. {sorted(missing)[:3]}'
    lines[k] = PREFIX + json.dumps(bank, ensure_ascii=False) + ';'
    return '\n'.join(lines)
