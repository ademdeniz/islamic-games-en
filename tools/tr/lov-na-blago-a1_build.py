"""Build work/lov-na-blago-a1.en.html from work/lov-na-blago-a1.bs.html.
Run from project root:  python3 tools/tr/lov-na-blago-a1_build.py && python3 tools/skel.py build lov-na-blago-a1"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'tr'))
G = 'lov-na-blago-a1'
import importlib
bank_en = importlib.import_module('lov-na-blago-a1_bank').B
src = open(os.path.join(ROOT, 'work', G + '.bs.html'), encoding='utf-8').read()

UI = [
    ('<title>Lov na blago – Nivo A1</title>', '<title>Treasure Hunt – Level A1</title>'),
    ('<h1>LOV NA BLAGO</h1><b>NIVO A1</b>', '<h1>TREASURE HUNT</h1><b>LEVEL A1</b>'),
    ('<div class="by">Pripremio Abdo ef. Rekić</div>', ''),
    ('id="score">⭐ 0 bodova<', 'id="score">⭐ 0 points<'),
    ('id="right">✅ 0/20 tačnih<', 'id="right">✅ 0/20 correct<'),
    ('id="asked">❓ 0 pitanja<', 'id="asked">❓ 0 questions<'),
    ('aria-label="Ilustrovana mapa skrivenog blaga"', 'aria-label="Illustrated map of the hidden treasure"'),
    ('<h2>PRONAŠAO SI BLAGO!</h2>', '<h2>YOU FOUND THE TREASURE!</h2>'),
    ('🔄 Nova potraga', '🔄 New hunt'),
    ('`⭐ ${score} bodova`', '`⭐ ${score} points`'),
    ('`✅ ${correct}/20 tačnih`', '`✅ ${correct}/20 correct`'),
    ('`❓ ${asked} pitanja`', '`❓ ${asked} questions`'),
    ('`Potrebno još ${20-correct} tačnih odgovora`', '`Correct answers still needed: ${20-correct}`'),
    ('`✅ Tačno! +10 bodova. Otkriveno polje ${correct} od 20.`', '`✅ Correct! +10 points. Square ${correct} of 20 uncovered.`'),
    ('"❌ Netačno! −5 bodova. Dobijaš novo pitanje."', '"❌ Wrong! −5 points. Here is a new question."'),
    ('`Tačno si riješio <b>20 pitanja</b> nakon ukupno <b>${asked}</b> pitanja.<br>Konačni rezultat: <b>${score} bodova</b>.<br>Put je potpuno otkriven i sanduk s blagom je tvoj!`',
     '`You answered <b>20 questions</b> correctly out of <b>${asked}</b> questions in total.<br>Final score: <b>${score} points</b>.<br>The path is fully uncovered and the treasure chest is yours!`'),
]
out = src
for bs, en in UI:
    assert out.count(bs) == 1, (out.count(bs), bs)
    out = out.replace(bs, en)

i = out.index('const BANK=') + len('const BANK=')
bank, end = json.JSONDecoder().raw_decode(out[i:])
assert len(bank) == len(bank_en), (len(bank), len(bank_en))
seen = {}
new = []
for (q, opts, c), (qe, oe) in zip(bank, bank_en):
    assert len(opts) == len(oe) == 4
    for b, e in [(q, qe)] + list(zip(opts, oe)):
        assert '"' not in e and "'" not in e and '\\' not in e, e
        if b in seen:
            assert seen[b] == e, (b, seen[b], e)
        seen[b] = e
    new.append([qe, oe, c])
out = out[:i] + json.dumps(new, ensure_ascii=False) + out[i + end:]
open(os.path.join(ROOT, 'work', G + '.en.html'), 'w', encoding='utf-8').write(out)
print('ok', len(new))
