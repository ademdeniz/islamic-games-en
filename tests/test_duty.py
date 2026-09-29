"""Tests for the Sunday pizza & parent duty page (tools/build_duty.py -> duty/index.html)."""
import os
import re
import sys

import gamecheck as gc

sys.path.insert(0, os.path.join(gc.ROOT, 'tools'))
import build_duty  # noqa: E402
import build_plan  # noqa: E402
from build_lessons_core import brand  # noqa: E402,F401

PAGE = os.path.join(gc.ROOT, 'duty', 'index.html')


def test_first_round_only_every_parent_once():
    r, P = build_duty.rota(), build_duty.P
    assert [d for d, _, _ in r] == [d for d in build_plan.class_days() if d >= P['start']][:max(len(P['g1']), len(P['g2']))]
    for g, i in (('g1', 1), ('g2', 2)):
        names = [x[i] for x in r if x[i] != build_duty.TBA]
        assert names == P[g], 'each parent once, in order – no second round'
        assert all(x[i] == build_duty.TBA for x in r[len(P[g]):])


def test_page_is_current_and_shares_nothing_private():
    html = open(PAGE, encoding='utf-8').read()
    build_duty.build()
    assert open(PAGE, encoding='utf-8').read() == html, 'run python3 tools/build_duty.py'
    text = re.sub(r'<[^>]+>|data:image[^"]+', ' ', html)
    assert 'Alketa' not in text, 'a student’s name, not a parent’s – that family is listed by family name'
    assert not re.search(r'\d{3}\D{0,3}\d{3}\D{0,3}\d{4}', text), 'no phone numbers'
    assert not re.search(r'[\w.]+@[\w.]+', text), 'no email addresses'
    assert all(re.fullmatch(r'\w+ (\w\.|family)', p) for g in ('g1', 'g2') for p in build_duty.P[g]), 'first name + initial only'
    assert 'next round will be posted' in html and 'noindex' in html and 'The Imam will let you know if we need more or fewer' in html
