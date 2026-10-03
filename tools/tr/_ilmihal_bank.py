"""The shared Ilmihal question bank (1,568 questions, levels A1–B3) used by Abdo ef. Rekić's newer games.

ilmihal-bank.json holds every question once: {"l": level, "c": correct index, "bs": {q, a}, "en": {q, a}}.
1,468 English versions come from games we had already translated (same question, same answers), the
other 100 (mostly level B3) were translated for this bank. 89 more ("extra": "mektebski-akvarij") are an older set of
B1 questions that only the Aquarium game still has.

translate(src) finds the bank in a game (const BANK=[...] / const BANK={...} / <script id="question-bank">),
swaps every question and its options for English and puts it back in exactly the same JSON style.
Games store the question as "q" or "question", the options as "a", "o" or "options" and the right answer as
"c", "correct" or "a" – all are handled.
"""
import json
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
ENTRIES = json.load(open(os.path.join(_HERE, 'ilmihal-bank.json'), encoding='utf-8'))
BY_KEY = {(e['bs']['q'], tuple(e['bs']['a'])): e for e in ENTRIES}
BY_Q = {}
for _e in ENTRIES:
    BY_Q.setdefault(_e['bs']['q'], []).append(_e)

_START = re.compile(r'(?:const|let|var)\s+(?:BANK|DB)\s*=\s*|<script id="question-bank" type="application/json">')


def english(q, opts):
    """English (question, options) for a Bosnian question, options in the same order.
    A " ✅" left on the right option in some copies (it gives the answer away) is dropped."""
    opts = [re.sub(r'\s*✅\s*$', '', o) for o in opts]
    e = BY_KEY.get((q, tuple(opts)))
    if e is None:  # same question, options in another order
        e = next((x for x in BY_Q.get(q, []) if sorted(x['bs']['a']) == sorted(opts)), None)
    assert e is not None, f'question not in the bank: {q!r} {opts!r}'
    en = dict(zip(e['bs']['a'], e['en']['a']))
    return e['en']['q'], [en[o] for o in opts]


REPAIRED = []   # questions whose options belonged to another question in the original (see repair())


def _keys(x):
    qk = 'q' if 'q' in x else 'question'
    ok = 'options' if isinstance(x.get('options'), list) else 'o' if isinstance(x.get('o'), list) else 'a'
    return qk, ok


def repair(x, key, qk='q'):
    """A few copies of the bank have a question with another question's options (e.g. “Who is Allah’s last
    messenger?” offering “Allah’s Oneness / The number of prayers…”). Give it its own options and right answer."""
    cands = [e for e in BY_Q.get(x[qk], []) if len(e['bs']['a']) == len(x[key])]
    assert len(cands) == 1, f'question not in the bank: {x[qk]!r} {x[key]!r}'
    e = cands[0]
    right = 'c' if 'c' in x else 'correct' if 'correct' in x else 'a'
    REPAIRED.append(x[qk])
    return dict(x, **{key: list(e['bs']['a']), right: e['c']})


def _walk(x):
    if isinstance(x, list):
        return [_walk(i) for i in x]
    if isinstance(x, dict):
        if 'q' in x or 'question' in x:
            qk, key = _keys(x)
            opts = [re.sub(r'\s*✅\s*$', '', o) for o in x[key]]
            if (x[qk], tuple(opts)) not in BY_KEY and not any(sorted(e['bs']['a']) == sorted(opts) for e in BY_Q.get(x[qk], [])):
                x = repair(x, key, qk)
            x = dict(x)
            bs_opts = list(x[key])
            x[qk], x[key] = english(x[qk], x[key])
            for k in ('a', 'correct'):   # games that store the right answer as its text, not its number
                if k != key and isinstance(x.get(k), str):
                    x[k] = x[key][bs_opts.index(x[k])]
            return x
        return {k: _walk(v) for k, v in x.items()}
    return x


def _dumps(data, like):
    for kw in ({'separators': (',', ':')}, {}):
        if json.dumps(json.loads(like), ensure_ascii=False, **kw) == like:
            return json.dumps(data, ensure_ascii=False, **kw)
    raise AssertionError('bank is not in a JSON style we can reproduce')


def translate(src):
    m = _START.search(src)
    assert m, 'no question bank found'
    data, end = json.JSONDecoder().raw_decode(src, m.end())
    old = src[m.end():end]
    return src[:m.end()] + _dumps(_walk(data), old) + src[end:]


def count(src):
    m = _START.search(src)
    data, _ = json.JSONDecoder().raw_decode(src, m.end())
    n = [0]

    def walk(x):
        if isinstance(x, list):
            for i in x:
                walk(i)
        elif isinstance(x, dict):
            if 'q' in x or 'question' in x:
                n[0] += 1
            else:
                for v in x.values():
                    walk(v)
    walk(data)
    return n[0]
