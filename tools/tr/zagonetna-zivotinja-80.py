# zagonetna-zivotinja-80: table mode for the page text + transform() for the data line
# (const A = animals, Q = 321 questions). The question bank is translated per question from
# tools/tr/zagonetna-zivotinja-80_en{1,2,3}.txt ("N. question | opt | opt | opt | opt", same option order
# as the original, so the correct-answer index is untouched). Identical Bosnian strings must get identical
# English (checked here). zagonetna-zivotinja-a3 has the identical bank and reuses this file.
import json
import os

T = [
    ('<title>Zagonetna životinja – A3</title>', '<title>Mystery Animal – A3</title>'),
    ('content="Zagonetna životinja"', 'content="Mystery Animal"'),
    ('<h1>🐾 ZAGONETNA ŽIVOTINJA</h1>', '<h1>🐾 MYSTERY ANIMAL</h1>'),
    ('<div class="author">Pripremio Abdo ef. Rekić • Nivo A3</div>', '<div class="author">Level A3</div>'),
    ('📚 321 pitanja', '📚 321 questions'),
    ('>🔎 POGODI ŽIVOTINJU<', '>🔎 GUESS THE ANIMAL<'),
    ('Tačan odgovor +10 i otkriva karticu • netačan −3 • tačan pogodak životinje +50 • pitanja i odgovori se miješaju',
     'Correct answer +10 and opens a tile • wrong −3 • guessing the animal right +50 • questions and answers are shuffled'),
    ('<h2>Koja je životinja?</h2>', '<h2>Which animal is it?</h2>'),
    ('>Nastavi otkrivati<', '>Keep uncovering<'),
    ('"🏆 Bravo! Otkrio/la si sve životinje!"', '"🏆 Well done! You found all the animals!"'),
    ('`Sve ${animals.length} završene`', '`All ${animals.length} done`'),
    ('`Životinja ${ai+1}/${animals.length}`', '`Animal ${ai+1}/${animals.length}`'),
    ('"✓ Tačno! Otkriven je dio slike."', '"✓ Correct! A piece of the picture is uncovered."'),
    ('"✗ Netačno. Kartica ostaje."', '"✗ Wrong. The tile stays."'),
    ('🎉 Tačno! To je ${n}!', '🎉 Correct! The animal is: ${n}!'),
    ('>SLJEDEĆA ŽIVOTINJA ➜<', '>NEXT ANIMAL ➜<'),
    ('"Nije ta životinja. Nastavi otkrivati!"', '"That’s not the animal. Keep uncovering!"'),
]
T80 = [
    ('content:"🌿  KVIZ ZNANJA  🌿"', 'content:"🌿  KNOWLEDGE QUIZ  🌿"'),
]

# Surnames/first names of Bosnian poets (answer options to “Who wrote the mawlid poem …?”).
ALLOW = ['Bašagić', 'Ćazim', 'Ćatić', 'Rešad', 'Kadić', 'Handžić']

# “Na putovanje” is “Of a journey” in Q78 (what Salah reminds us of) but “On a journey” in Q162 (where we go).
# Options are only compared with the correct answer of the same question (same array), so this is safe.
ALLOW_INCONSISTENT = ['Na putovanje']

ANIMALS = {
    'Jelen': 'Deer', 'Golub': 'Dove', 'Zebra': 'Zebra', 'Paun': 'Peacock', 'Pčela': 'Bee', 'Ćurka': 'Turkey',
    'Krava': 'Cow', 'Roda': 'Stork', 'Mačka': 'Cat', 'Koza': 'Goat', 'Janje': 'Lamb', 'Tigar': 'Tiger',
    'Panter': 'Panther', 'Labud': 'Swan', 'Noj': 'Ostrich', 'Jež': 'Hedgehog', 'Deva': 'Camel',
    'Žirafa': 'Giraffe', 'Guska': 'Goose', 'Kengur': 'Kangaroo', 'Lama': 'Llama', 'Žaba': 'Frog',
    'Fazan': 'Pheasant', 'Riba': 'Fish', 'Orao': 'Eagle', 'Kornjača': 'Turtle', 'Vjeverica': 'Squirrel',
    'Lav': 'Lion', 'Patka': 'Duck', 'Pijetao': 'Rooster', 'Panda': 'Panda', 'Pingvin': 'Penguin',
    'Čimpanza': 'Chimpanzee', 'Djetlić': 'Woodpecker',
}

PREFIX = 'const A='
HERE = os.path.dirname(os.path.abspath(__file__))


def load_english():
    en = {}
    for k in (1, 2, 3):
        for line in open(os.path.join(HERE, f'zagonetna-zivotinja-80_en{k}.txt'), encoding='utf-8').read().splitlines():
            if not line.strip():
                continue
            num, rest = line.split('. ', 1)
            parts = [p.strip() for p in rest.split(' | ')]
            en[int(num)] = parts
    return en


def transform(src):
    lines = src.split('\n')
    k = next(n for n, l in enumerate(lines) if l.startswith(PREFIX))
    line = lines[k]
    a_txt, q_txt = line[len(PREFIX):].split(', Q=', 1)
    assert q_txt.endswith(';')
    q_txt = q_txt[:-1]
    A, Q = json.loads(a_txt), json.loads(q_txt)
    assert json.dumps(A, ensure_ascii=False) == a_txt and json.dumps(Q, ensure_ascii=False) == q_txt, 'no round-trip'
    en = load_english()
    assert sorted(en) == [q[0] for q in Q], 'question numbers do not match'
    table, clash = {}, []
    for q in Q:
        e = en[q[0]]
        assert len(e) == 1 + len(q[2]), f'Q{q[0]}: expected {1 + len(q[2])} parts, got {len(e)}'
        assert len(set(e[1:])) == len(e) - 1, f'Q{q[0]}: two English options are identical'
        for bs, tx in zip([q[1]] + q[2], e):
            if table.setdefault(bs, tx) != tx and bs not in ALLOW_INCONSISTENT:
                clash.append((q[0], bs, table[bs], tx))
    assert not clash, 'inconsistent translations:\n' + '\n'.join(map(str, clash))
    for a in A:
        a['name'] = ANIMALS[a['name']]
    for q in Q:
        e = en[q[0]]
        q[1], q[2] = e[0], e[1:]
    lines[k] = PREFIX + json.dumps(A, ensure_ascii=False) + ', Q=' + json.dumps(Q, ensure_ascii=False) + ';'
    return '\n'.join(lines)


T = T + T80
