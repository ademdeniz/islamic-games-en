# mektebski-ribolov: Abdo ef. Rekić's "Maktab Fishing" – answer fast to catch a golden, big or small fish (1 or 2 players).
# The 1,568 questions are the shared Ilmihal bank (_ilmihal_bank.py); 37 copies have a section heading glued to their last
# answer ("… DINSKI ŠARTI") – they are matched by question and answer start, and the English drops the stray heading.
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank as IB  # noqa: E402
from _rekic_ui import page  # noqa: E402

GAME = 'mektebski-ribolov'
EXTRA = [
    ('Mektebski ribolov', 'Maktab Fishing'), ('🎣 MEKTEBSKI RIBOLOV', '🎣 MAKTAB FISHING'), ('Pitanje 1/20', 'Question 1/20'), ('🎣 Igrač 1', '🎣 Player 1'),
    ('Spremni za ribolov?', 'Ready to go fishing?'), ('🌟 Do 5 s: +20', '🌟 Up to 5 s: +20'), ('🐟 Do 10 s: +10', '🐟 Up to 10 s: +10'),
    ('🐠 Poslije 10 s: +5', '🐠 After 10 s: +5'),
    ('Tačno odgovori i ulovi ribicu! Što brže odgovoriš, više bodova osvajaš.', 'Answer right and catch a fish! The faster you answer, the more points you win.'),
    ('🌟 Zlatna do 5 s = 20 bodova · 🐟 Velika do 10 s = 10 · 🐠 Mala nakon 10 s = 5', '🌟 Golden within 5 s = 20 points · 🐟 Big within 10 s = 10 · 🐠 Small after 10 s = 5'),
    ('Izaberi pitanja:', 'Choose the questions:'), ('SVA PITANJA', 'ALL QUESTIONS'), ('Broj igrača:', 'Players:'), ('1 igrač', '1 player'),
    ('2 igrača — naizmjenično', '2 players — taking turns'), ('Broj pitanja po igraču:', 'Questions per player:'), ('🎣 ZAPOČNI RIBOLOV', '🎣 START FISHING'),
    ('⛶ PUNI EKRAN', '⛶ FULL SCREEN'),
    ('Ugrađeno je 1568 pitanja iz šest priloženih baza A1–B3. Pitanja se nasumično biraju.', 'There are 1,568 questions from the six levels A1–B3. The questions are picked at random.'),
    ('🏆 KRAJ RIBOLOVA', '🏆 FISHING IS OVER'), ('🔁 Igraj ponovo', '🔁 Play again'), ('Okreni telefon vodoravno za ribolov!', 'Turn the phone sideways to go fishing!'),
    ('Odaberi najmanje jedan nivo!', 'Choose at least one level!'), ('Pitanje ', 'Question '), ('🎣 Igrač ', '🎣 Player '), ('🌟 Zlatna ribica', '🌟 Golden fish'),
    ('🐟 Velika riba', '🐟 Big fish'), ('🐠 Mala ribica', '🐠 Small fish'), ('🌟 Zlatna ribica!', '🌟 Golden fish!'), ('🐟 Velika riba!', '🐟 Big fish!'),
    ('🐠 Mala ribica!', '🐠 Small fish!'), (' bodova', ' points'), ('❌ Nema ulova — pokušaj ponovo!', '❌ No catch — try again!'),
    ('<h2>🎣 Osvojeno ', '<h2>🎣 You won '), (' bodova!</h2>', ' points!</h2>'), ('<h2>🎣 Igrač 1: ', '<h2>🎣 Player 1: '),
    (' bodova</h2><h2>🎣 Igrač 2: ', ' points</h2><h2>🎣 Player 2: '), (' bodova</h2><h3>', ' points</h3><h3>'), ('🤝 Neriješeno!', '🤝 A draw!'),
    ('🏆 Pobijedio je igrač ', '🏆 The winner is player '),
]
DELETE, ALLOW_ARABIC, _base, BRAND_FIT = page(GAME, EXTRA)
ALLOW_ARABIC = []


def english(q, opts):
    try:
        return IB.english(q, opts)
    except AssertionError:   # a section heading glued to an answer in this copy
        cands = [e for e in IB.BY_Q.get(q, []) if len(e['bs']['a']) == len(opts)
                 and all(o == a or o.startswith(a + ' ') for o, a in zip(opts, e['bs']['a']))]
        assert len(cands) == 1, (q, opts)
        return cands[0]['en']['q'], list(cands[0]['en']['a'])


def transform(src):
    key = 'const BANKS='
    i = src.index(key) + len(key)
    j = i + len(src[i:]) - len(src[i:].lstrip())
    banks, n = json.JSONDecoder().raw_decode(src[j:])
    for items in banks.values():
        for x in items:
            x[0], x[1] = english(x[0], x[1])
    return _base(src[:j] + json.dumps(banks, ensure_ascii=False, separators=(',', ':')) + src[j + n:])
