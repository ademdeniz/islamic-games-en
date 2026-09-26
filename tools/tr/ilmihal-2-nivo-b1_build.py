"""Direct-mode builder for ilmihal-2-nivo-b1 (772-question quiz bank).

  python3 tools/skel.py extract ilmihal-2-nivo-b1
  python3 tools/tr/ilmihal-2-nivo-b1_build.py      -> work/ilmihal-2-nivo-b1.en.html
  python3 tools/skel.py build ilmihal-2-nivo-b1

The question bank (`const BANKS=...` on one line) is parsed as JSON; every question and option is replaced by the
matching line of ilmihal-2-nivo-b1_bank.txt (`<id> [question, A, B, C, D]`, same order as the original). Keys,
the correct-answer letters and the order of questions/options are untouched. Identical Bosnian strings must get
identical English (checked below). The UI strings are replaced from the UI table.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
GAME = 'ilmihal-2-nivo-b1'

UI = [
    ('<title>Kviz Ilmihal 2 – Nivo B1</title>', '<title>Ilmihal Quiz 2 – Level B1</title>'),
    ('<div class="title">KVIZ ILMIHAL 2</div>', '<div class="title">ILMIHAL QUIZ 2</div>'),
    ('<div class="sub">NIVO B1 • pripremio Abdo ef. Rekić</div>', '<div class="sub">LEVEL B1</div>'),
    ('<h2>30 pitanja</h2>', '<h2>30 questions</h2>'),
    ('<p>5 iz A3 • 25 iz B1</p>', '<p>5 from A3 • 25 from B1</p>'),
    ('<p>Tačno +10 bodova • netačno −3 boda</p>', '<p>Correct +10 points • wrong −3 points</p>'),
    ('>POČNI KVIZ<', '>START QUIZ<'),
    ('Bez vremenskog ograničenja • nema vraćanja na prethodno pitanje',
     'No time limit • no going back to the previous question'),
    ('>Publika<', '>Audience<'),
    ('>Muallim<', '>Teacher<'),
    ('<h1>KRAJ KVIZA</h1>', '<h1>END OF QUIZ</h1>'),
    ('>IGRAJ PONOVO<', '>PLAY AGAIN<'),
    ('`Pitanje ${i+1}/30`', '`Question ${i+1}/30`'),
    ('`Baza: ${q.level}`', '`Bank: ${q.level}`'),
    ('`Bodovi: ${score}`', '`Points: ${score}`'),
    ("'TAČNO! +10 bodova'", "'CORRECT! +10 points'"),
    ("'NETAČNO! −3 boda'", "'WRONG! −3 points'"),
    ("`Muallim smatra da je odgovor ${'ABCD'[ci]}.`", "`The teacher (mu’allim) thinks the answer is ${'ABCD'[ci]}.`"),
    ('`Osvojeno: ${score} bodova`', '`Your score: ${score} points`'),
    ('`Tačnih odgovora: ${correct} od 30 • Netačnih: ${30-correct}`',
     '`Correct answers: ${correct} of 30 • Wrong: ${30-correct}`'),
]


def main():
    src = open(os.path.join(ROOT, 'work', GAME + '.bs.html'), encoding='utf-8').read()
    lines = src.split('\n')
    k = next(n for n, l in enumerate(lines) if l.startswith('const BANKS='))
    body = lines[k][len('const BANKS='):]
    assert body.endswith(';')
    banks = json.loads(body[:-1])
    assert json.dumps(banks, ensure_ascii=False) + ';' == body, 'bank would not re-serialise identically'

    tr = []
    for ln in open(os.path.join(HERE, GAME + '_bank.txt'), encoding='utf-8'):
        if ln.strip():
            qid, rest = ln.rstrip('\n').split(' ', 1)
            tr.append((qid, json.loads(rest)))

    settings = {}
    exec(open(os.path.join(HERE, GAME + '.py'), encoding='utf-8').read(), settings)
    allowed = set(settings.get('ALLOW_INCONSISTENT', ()))
    mapping, errors, n = {}, [], 0
    for lvl in ['A3', 'B1']:
        for qi, q in enumerate(banks[lvl]):
            qid, en = tr[n]
            n += 1
            if qid != f'{lvl}{qi}' or len(en) != 5:
                sys.exit(f'bank line {n}: expected {lvl}{qi} with 5 strings, got {qid} ({len(en)})')
            bs = [q['q']] + [q['opts'][c] for c in 'ABCD']
            assert list(q['opts']) == list('ABCD')
            for b, e in zip(bs, en):
                if not e.strip():
                    errors.append(f'{qid}: empty translation for {b!r}')
                if b in mapping and mapping[b] != e and b not in allowed:
                    errors.append(f'{qid}: {b!r} -> {e!r} but earlier -> {mapping[b]!r}')
                mapping.setdefault(b, e)
            q['q'] = en[0]
            q['opts'] = {c: en[i + 1] for i, c in enumerate('ABCD')}
    assert n == len(tr), f'{len(tr) - n} extra lines in bank file'
    if errors:
        sys.exit('inconsistent translations:\n' + '\n'.join(errors))
    lines[k] = 'const BANKS=' + json.dumps(banks, ensure_ascii=False) + ';'
    out = '\n'.join(lines)
    for bs, en in UI:
        assert out.count(bs) >= 1, f'UI string not found: {bs!r}'
        out = out.replace(bs, en)
    open(os.path.join(ROOT, 'work', GAME + '.en.html'), 'w', encoding='utf-8').write(out)
    print(f'{n} questions, {len(mapping)} unique strings translated')


if __name__ == '__main__':
    main()
