"""Direct-mode builder for sta-radi-masa: work/sta-radi-masa.bs.html -> work/sta-radi-masa.en.html.

  python3 tools/tr/sta-radi-masa_build.py && python3 tools/skel.py build sta-radi-masa
"""
import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.Q


Q = {**load('sta-radi-masa_bank1'), **load('sta-radi-masa_bank2')}

ROUNDS = {
    'Maša hrani golubove': 'Masha is feeding pigeons',
    'Maša slika medu': 'Masha is painting the bear',
    'Maša je teniserka': 'Masha is a tennis player',
    'Maša i koza': 'Masha and the goat',
    'Maša i zeko': 'Masha and the bunny',
    'Maša je fotograf': 'Masha is a photographer',
    'Maša i pračovjek': 'Masha and the caveman',
    'Maša i panda slažu kocke': 'Masha and the panda stack blocks',
    'Maša je kuharica': 'Masha is a cook',
    'Maša bere maline': 'Masha is picking raspberries',
    'Maša pere ruke': 'Masha is washing her hands',
    'Maša čisti pod': 'Masha is cleaning the floor',
    'Maša pere zube': 'Masha is brushing her teeth',
    'Maša pere suđe': 'Masha is washing the dishes',
    'Maša usisava': 'Masha is vacuuming',
    'Maša uči sufaru': 'Masha is learning the Arabic alphabet (sufara)',
    'Maša zijeva': 'Masha is yawning',
    'Maša i maline': 'Masha and the raspberries',
    'Maša putuje svijetom': 'Masha is travelling the world',
    'Maša je gitaristica': 'Masha is a guitarist',
    'Maša je slikarica': 'Masha is a painter',
    'Maša vozi bicikl': 'Masha is riding a bike',
    'Maša i medo ispred kuće': 'Masha and the bear in front of the house',
    'Maša se igra s medom': 'Masha is playing with the bear',
    'Maša pije čaj s medom': 'Masha is drinking tea with the bear',
    'Maša i medo beru jagode': 'Masha and the bear are picking strawberries',
    'Maša i medo voze motor': 'Masha and the bear are riding a motorbike',
    'Maša kuha ručak': 'Masha is cooking lunch',
    'Maša plete': 'Masha is knitting',
    'Maša i medo pecaju': 'Masha and the bear are fishing',
    'Maša i medo beru bobice': 'Masha and the bear are picking berries',
    'Maša i medo odmaraju u prirodi': 'Masha and the bear are resting outdoors',
    'Maša se penje na palmu': 'Masha is climbing a palm tree',
    'Maša bere ribizle': 'Masha is picking currants',
    'Maša sjedi na lubenici': 'Masha is sitting on a watermelon',
    'Maša jede sladoled': 'Masha is eating ice cream',
    'Maša kliže na ledu': 'Masha is ice skating',
    'Maša se sanka': 'Masha is sledding',
    'Maša jede slatkiše': 'Masha is eating sweets',
    'Maša se igra s igračkom': 'Masha is playing with a toy',
    'Maša bere jabuke': 'Masha is picking apples',
    'Maša bere suncokret': 'Masha is picking a sunflower',
    'Maša je doktorica': 'Masha is a doctor',
    'Maša jede pizzu': 'Masha is eating pizza',
}

UI = [
    ('<title>Šta radi Maša?</title>', '<title>What Is Masha Doing?</title>'),
    ('/* Zadržava izgled ranije verzije; samo gornje informacije ostaju jasno vidljive. */',
     '/* Keeps the look of the earlier version; only the top info stays clearly visible. */'),
    ('<h1>🎀 ŠTA RADI MAŠA? 🎀</h1>', '<h1>🎀 WHAT IS MASHA DOING? 🎀</h1>'),
    ('<div class="sub">Kviz znanja • Pripremio Abdo ef. Rekić</div>', '<div class="sub">Knowledge quiz</div>'),
    ('⭐ Bodovi:', '⭐ Points:'), ('🧩 Otvoreno:', '🧩 Opened:'), ('🖼️ Slika:', '🖼️ Picture:'),
    ('📚 Baza: <b id="bankCount"></b> pitanja', '📚 Bank: <b id="bankCount"></b> questions'),
    ('onclick="testSound()">🔊 Zvuk</button>', 'onclick="testSound()">🔊 Sound</button>'),
    ('alt="Maša"', 'alt="Masha"'),
    ('🎯 POGODI ŠTA MAŠA RADI', '🎯 GUESS WHAT MASHA IS DOING'),
    ('➡️ NOVA SLIKA', '➡️ NEW PICTURE'),
    ('Za svaku sliku imaš samo jedan pokušaj pogađanja.', 'You get only one guess for each picture.'),
    ('<h2>🎯 Šta Maša radi?</h2>', '<h2>🎯 What is Masha doing?</h2>'),
    ('"✅ Tačno! Otvorena je jedna kartica."', '"✅ Correct! One tile has been opened."'),
    ('"❌ Netačno. Kartica se ne otvara."', '"❌ Wrong. No tile opens this time."'),
    ('"🎉 BRAVO! Tačan odgovor!<br><b>"', '"🎉 WELL DONE! Correct answer!<br><b>"'),
    ('"❌ Nije tačno.<br>Tačan odgovor je: <b>"', '"❌ Not correct.<br>The correct answer is: <b>"'),
    ('"🔊 Zvuk uključen"', '"🔊 Sound on"'),
]


def main():
    src = open(os.path.join(ROOT, 'work', 'sta-radi-masa.bs.html'), encoding='utf-8').read()
    m = re.search(r'const BANK=(\[.*?\]);\n', src)
    bank = json.loads(m.group(1))
    assert json.dumps(bank, ensure_ascii=False, separators=(',', ':')) == m.group(1)
    # every unique question is translated; exact repeats reuse the first translation
    first = {}
    for i, x in enumerate(bank):
        first.setdefault((x['q'], tuple(x['opts'])), i)
    tr = {}  # bosnian string -> english (must be consistent)
    conflicts = []
    out = []
    for i, x in enumerate(bank):
        j = first[(x['q'], tuple(x['opts']))]
        assert j in Q, f'question {i} (first seen {j}) not translated: {x["q"]}'
        q, opts = Q[j]
        assert len(opts) == len(x['opts']), f'question {j}: option count'
        for b, e in zip([x['q']] + x['opts'], [q] + opts):
            if tr.setdefault(b, e) != e:
                conflicts.append((b, tr[b], e))
        y = dict(x)
        y['q'] = q
        y['opts'] = list(opts)
        if 'src' in y:
            y['src'] = 'Quiz – 135 questions'
        out.append(y)
    extra = sorted(set(Q) - set(first.values()))
    assert not extra, f'translations for non-unique indices: {extra}'
    for c in conflicts:
        print('INCONSISTENT:', c)
    for i, (q, opts) in Q.items():
        for s in [q] + opts:
            assert '"' not in s and '\\' not in s, (i, s)
    html = src[:m.start(1)] + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + src[m.end(1):]
    for b, e in ROUNDS.items():
        k = html.count('"answer":"%s"' % b)
        assert k >= 1, b
        html = html.replace('"answer":"%s"' % b, '"answer":"%s"' % e)
    for b, e in UI:
        assert b in html, b
        html = html.replace(b, e)
    open(os.path.join(ROOT, 'work', 'sta-radi-masa.en.html'), 'w', encoding='utf-8').write(html)
    print('ok', len(out), 'questions,', len(conflicts), 'conflicts')


if __name__ == '__main__':
    main()
