"""Build work/mektebski-detektiv.en.html from the .bs.html (direct mode).
Run: python3 tools/tr/mektebski-detektiv_build.py && python3 tools/skel.py build mektebski-detektiv
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib
EN = importlib.import_module('mektebski-detektiv_db').EN

GAME = 'mektebski-detektiv'
ALLOW_INC = set(importlib.import_module(GAME).ALLOW_INCONSISTENT)
src = open(os.path.join(ROOT, 'work', GAME + '.bs.html'), encoding='utf-8').read()

UI = [
    ('<title>Mektebski detektiv</title>', '<title>Maktab Detective</title>'),
    ('<div class="brand">🕵️ Mektebski detektiv</div><div class="sig">Pripremio Abdo ef. Rekić</div>',
     '<div class="brand">🕵️ Maktab Detective</div>'),
    ('<span class="pill">Slučaj <b id="round">', '<span class="pill">Case <b id="round">'),
    ('<span class="pill">Ukupno: <b id="total">', '<span class="pill">Total: <b id="total">'),
    ('🔎 OTKRIJ TAJNI POJAM', '🔎 UNCOVER THE SECRET WORD'),
    ('<span id="value">100</span> bod.</div>', '<span id="value">100</span> pts</div>'),
    ('🔍 Novi trag (−20)', '🔍 New clue (−20)'),
    ('🎯 Pogodi', '🎯 Guess'),
    ('<span>200 pojmova u bazi</span>', '<span>200 terms in the database</span>'),
    ('<span>5 tragova po pojmu</span>', '<span>5 clues per term</span>'),
    ('type="button">Nova igra</button>', 'type="button">New game</button>'),
    ('<h2 id="modalTitle">Slučaj riješen!</h2>', '<h2 id="modalTitle">Case solved!</h2>'),
    ('<button id="continue">Nastavi</button>', '<button id="continue">Continue</button>'),
    ('showModal("Detektivska misija završena!","Osvojio/la si "+total+" bodova u 20 slučajeva.","Igraj ponovo",start)',
     'showModal("Detective mission complete!","You scored "+total+" points in 20 cases.","Play again",start)'),
    ('"Prvi trag je otkriven. Možeš pogađati odmah ili tražiti novi trag."',
     '"The first clue is revealed. You can guess now or ask for a new clue."'),
    ('"Trag zaključan"', '"Clue locked"'),
    ('"✅ Slučaj riješen! +"+casePoints+" bodova."', '"✅ Case solved! +"+casePoints+" points."'),
    ('showModal("Slučaj riješen!","Tačan odgovor je: "+current.answer+". Osvojeno: "+casePoints+" bodova.","Sljedeći slučaj",nextCase)',
     'showModal("Case solved!","The correct answer is: "+current.answer+". You earned: "+casePoints+" points.","Next case",nextCase)'),
    ('"❌ Pogrešan trag! Ovaj slučaj je izgubljen."', '"❌ Wrong lead! This case is lost."'),
    ('showModal("Slučaj nije riješen","Tačan odgovor je: "+current.answer+". Za ovaj slučaj nema bodova.","Novi slučaj",nextCase)',
     'showModal("Case not solved","The correct answer is: "+current.answer+". No points for this case.","New case",nextCase)'),
    ('showModal("Nova igra?","Trenutni rezultat će biti obrisan.","Pokreni novu igru",start)',
     'showModal("New game?","Your current score will be erased.","Start a new game",start)'),
]

out = src
for bs, en in UI:
    assert out.count(bs) == 1, (out.count(bs), bs)
    out = out.replace(bs, en)

m = re.search(r'const DB=(\[.*?\]);\n', out)
db = json.loads(m.group(1))
assert json.dumps(db, ensure_ascii=False) == m.group(1)
assert len(db) == len(EN) == 200
seen = {}
new = []
for e in db:
    ans, clues = EN[e['id']]
    assert len(clues) == len(e['clues']) == 5, e['id']
    for b, t in zip([e['answer']] + e['clues'], [ans] + clues):
        assert "'" not in t and '"' not in t, t
        if b in seen and seen[b] != t and b not in ALLOW_INC:
            raise SystemExit(f'inconsistent: {b!r} -> {seen[b]!r} / {t!r}')
        seen[b] = t
    new.append({'id': e['id'], 'answer': ans, 'clues': clues})
answers = [x['answer'] for x in new]
assert len(set(answers)) == len(answers), 'duplicate answers'
out = out[:m.start(1)] + json.dumps(new, ensure_ascii=False) + out[m.end(1):]
open(os.path.join(ROOT, 'work', GAME + '.en.html'), 'w', encoding='utf-8').write(out)
print('ok')
