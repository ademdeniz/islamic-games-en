"""Direct-mode builder for tajna-zivotinja (Secret Animal, 321-question A3 bank).

  python3 tools/skel.py extract tajna-zivotinja
  python3 tools/tr/tajna-zivotinja_build.py      -> work/tajna-zivotinja.en.html
  python3 tools/skel.py build tajna-zivotinja

The question bank is identical to the A3 bank of ilmihal-2-nivo-b1 (same questions, options, order and answers,
verified string by string when this was set up). Its English lines are copied in
tools/tr/tajna-zivotinja_bank.txt (`A3<i> [question, opt0, opt1, opt2, opt3]`). The correct answer is chosen by
index (`q.a`), which is untouched.

Animal names: every name is translated, and every `override` is set to the English name. The game shows `override`
in a label strip over the bottom of the picture (the original author used it for two animals whose picture label was
wrong); the pictures all carry a printed Bosnian label there, so this covers them with the English name.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
GAME = 'tajna-zivotinja'

ANIMALS = {
    'Leptir': 'Butterfly', 'Koza': 'Goat', 'Mačka': 'Cat', 'Pijetao': 'Rooster', 'Bubamara': 'Ladybug',
    'Skakavac': 'Grasshopper', 'Sova': 'Owl', 'Zec': 'Rabbit', 'Pas': 'Dog', 'Krava': 'Cow',
    'Vilin konjic': 'Dragonfly', 'Pingvin': 'Penguin', 'Mrav': 'Ant', 'Hrčak': 'Hamster', 'Lisica': 'Fox',
    'Konj': 'Horse', 'Jelen': 'Deer', 'Medvjed': 'Bear', 'Krokodil': 'Crocodile', 'Lav': 'Lion',
    'Slon': 'Elephant', 'Zebra': 'Zebra', 'Pauk': 'Spider', 'Kornjača': 'Turtle', 'Žirafa': 'Giraffe',
    'Kokoš': 'Hen', 'Puž': 'Snail', 'Patka': 'Duck', 'Delfin': 'Dolphin', 'Ajkula': 'Shark', 'Kit': 'Whale',
    'Rak': 'Crab / Lobster', 'Riba': 'Fish', 'Hobotnica': 'Octopus', 'Gušter': 'Lizard', 'Žaba': 'Frog',
    'Šišmiš': 'Bat', 'Jastreb': 'Hawk', 'Orao': 'Eagle', 'Papagaj': 'Parrot', 'Kornjača (kopnena)': 'Tortoise',
    'Delfin (mornarski)': 'Dolphin (bottlenose)', 'Zvjezdica': 'Starfish', 'Morski konjic': 'Seahorse',
    'Škorpion': 'Scorpion', 'Pingvin (mali)': 'Penguin (little)', 'Deva': 'Camel', 'Slon (mali)': 'Elephant (little)',
    'Nosorog': 'Rhino', 'Vuk': 'Wolf', 'Jazavac': 'Badger', 'Rakun': 'Raccoon', 'Gorila': 'Gorilla',
}

UI = [
    ('<title>Tajna životinja – A3</title>', '<title>Secret Animal – A3</title>'),
    ('<h1>🐾 TAJNA ŽIVOTINJA 🐾</h1>', '<h1>🐾 SECRET ANIMAL 🐾</h1>'),
    ('<div class="sub">Odgovaraj na pitanja i otkrivaj sliku</div>',
     '<div class="sub">Answer the questions and uncover the picture</div>'),
    ('<div class="author">Nivo A3 • 321 pitanja • Pripremio Abdo ef. Rekić</div>',
     '<div class="author">Level A3 • 321 questions</div>'),
    ('⭐ Bodovi: <span', '⭐ Points: <span'),
    ('🧩 Otkriveno: <span', '🧩 Uncovered: <span'),
    ('alt="Tajna životinja"', 'alt="Secret animal"'),
    ('>🔍 Pogodi šta se krije<', '>🔍 Guess what’s hiding<'),
    ('Možeš pokušati u svakom trenutku. Što ranije pogodiš, veći je bonus.',
     'You can guess at any time. The sooner you guess, the bigger the bonus.'),
    ('<option value="">Izaberi životinju…</option>', '<option value="">Choose an animal…</option>'),
    ('id="guessBtn">Pogodi<', 'id="guessBtn">Guess<'),
    ('id="newBtn">Nova životinja<', 'id="newBtn">New animal<'),
    ('<div class="qtitle">PITANJE <span id="qnum">1</span> • TAČNO +10 • NETAČNO −3</div>',
     '<div class="qtitle">QUESTION <span id="qnum">1</span> • CORRECT +10 • WRONG −3</div>'),
    ('"✅ TAČNO! +10 bodova. Otkriveno je jedno polje."', '"✅ CORRECT! +10 points. One square is uncovered."'),
    ('"❌ NETAČNO! −3 boda. Polje ostaje zatvoreno."', '"❌ WRONG! −3 points. The square stays closed."'),
    ('"Izaberi životinju koju želiš pogoditi."', '"Choose the animal you want to guess."'),
    ('"🎉 TAČNO! Bonus +"+b+" bodova!"', '"🎉 CORRECT! Bonus +"+b+" points!"'),
    ('"❌ Nije ta životinja. −3 boda. Pokušaj ponovo kasnije."',
     '"❌ That’s not the animal. −3 points. Try again later."'),
    ('"🎉 Tajna životinja je otkrivena!"', '"🎉 The secret animal has been revealed!"'),
    ('"🏆 Bravo! Pogodio/la si: ":"Otkrivena životinja je: "', '"🏆 Well done! You guessed it: ":"The secret animal was: "'),
    ('" • Ukupno bodova: "', '" • Total points: "'),
]


def cut(src, start, end):
    i = src.index(start) + len(start)
    j = src.index(end, i)
    return i, j


def main():
    src = open(os.path.join(ROOT, 'work', GAME + '.bs.html'), encoding='utf-8').read()

    # --- question bank
    i, j = cut(src, 'const QUESTIONS=', ';\nconst ANIMALS')
    questions = json.loads(src[i:j])
    assert json.dumps(questions, ensure_ascii=False, separators=(',', ':')) == src[i:j], 'bank would not re-serialise'
    tr = []
    for ln in open(os.path.join(HERE, GAME + '_bank.txt'), encoding='utf-8'):
        if ln.strip():
            qid, rest = ln.rstrip('\n').split(' ', 1)
            tr.append((qid, json.loads(rest)))
    assert len(tr) == len(questions) == 321, (len(tr), len(questions))
    settings = {}
    exec(open(os.path.join(HERE, GAME + '.py'), encoding='utf-8').read(), settings)
    allowed = set(settings.get('ALLOW_INCONSISTENT', ()))
    mapping, errors = {}, []
    for k, (q, (qid, en)) in enumerate(zip(questions, tr)):
        assert qid == f'A3{k}' and len(en) == 5 and len(q['o']) == 4, (k, qid)
        for b, e in zip([q['q']] + q['o'], en):
            if not e.strip():
                errors.append(f'{qid}: empty translation for {b!r}')
            if b in mapping and mapping[b] != e and b not in allowed:
                errors.append(f'{qid}: {b!r} -> {e!r} but earlier -> {mapping[b]!r}')
            mapping.setdefault(b, e)
        if len(set(en[1:])) != 4:
            errors.append(f'{qid}: duplicate English options {en[1:]}')
        q['q'], q['o'] = en[0], en[1:]
    if errors:
        sys.exit('bank problems:\n' + '\n'.join(errors))
    src = src[:i] + json.dumps(questions, ensure_ascii=False, separators=(',', ':')) + src[j:]

    # --- animals
    i, j = cut(src, 'const ANIMALS=', ';\nconst GUESS_NAMES')
    animals = json.loads(src[i:j])
    assert json.dumps(animals, ensure_ascii=False, separators=(',', ':')) == src[i:j]
    for a in animals:
        assert a['override'] in ('', a['name']), a
        a['name'] = ANIMALS[a['name']]
        a['override'] = a['name']
    src = src[:i] + json.dumps(animals, ensure_ascii=False, separators=(',', ':')) + src[j:]
    i, j = cut(src, 'const GUESS_NAMES=', ';\n')
    names = json.loads(src[i:j])
    assert json.dumps(names, ensure_ascii=False, separators=(', ', ':')) == src[i:j]
    en_names = [ANIMALS[n] for n in names]
    assert len(set(en_names)) == len(en_names), 'duplicate English animal names'
    assert set(en_names) == {a['name'] for a in animals}, 'every animal must be guessable'
    src = src[:i] + json.dumps(en_names, ensure_ascii=False, separators=(', ', ':')) + src[j:]

    # --- UI
    for bs, en in UI:
        assert src.count(bs) >= 1, f'UI string not found: {bs!r}'
        src = src.replace(bs, en)
    src = src.replace('<footer>Pripremio Abdo ef. Rekić</footer>\n', '')
    open(os.path.join(ROOT, 'work', GAME + '.en.html'), 'w', encoding='utf-8').write(src)
    print(f'{len(questions)} questions, {len(mapping)} unique strings, {len(animals)} animals')


if __name__ == '__main__':
    main()
