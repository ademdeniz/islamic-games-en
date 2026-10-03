"""The shared Ilmihal question bank (1,568 questions, levels A1–B3) used by Abdo ef. Rekić's newer games.

ilmihal-bank.json holds every question once: {"l": level, "c": correct index, "bs": {q, a}, "en": {q, a}}.
1,468 English versions come from games we had already translated (same question, same answers), the
other 100 (mostly level B3) were translated for this bank.

translate(src) finds the bank in a game (const BANK=[...] / const BANK={...} / <script id="question-bank">),
swaps every question and its options for English and puts it back in exactly the same JSON style.
Games store the options as "a" or "o" and the right answer as "c" or "a" – both are handled.
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

_START = re.compile(r'(?:const|let|var)\s+BANK\s*=\s*|<script id="question-bank" type="application/json">')


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


def _walk(x):
    if isinstance(x, list):
        return [_walk(i) for i in x]
    if isinstance(x, dict):
        if 'q' in x:
            key = 'o' if isinstance(x.get('o'), list) else 'a'
            x = dict(x)
            x['q'], x[key] = english(x['q'], x[key])
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
            if 'q' in x:
                n[0] += 1
            else:
                for v in x.values():
                    walk(v)
    walk(data)
    return n[0]
