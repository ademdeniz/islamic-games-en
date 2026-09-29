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


def test_every_class_sunday_has_one_parent_from_each_group():
    r = build_duty.rota()
    assert [d for d, _, _ in r] == [d for d in build_plan.class_days() if d >= build_duty.P['start']]
    assert all(a in build_duty.P['g1'] and b in build_duty.P['g2'] for _, a, b in r)
    for g, i in (('g1', 1), ('g2', 2)):    # everyone takes turns evenly
        counts = [sum(x[i] == p for x in r) for p in build_duty.P[g]]
        assert max(counts) - min(counts) <= 1, (g, counts)


def test_page_is_current_and_shares_nothing_private():
    html = open(PAGE, encoding='utf-8').read()
    build_duty.build()
    assert open(PAGE, encoding='utf-8').read() == html, 'run python3 tools/build_duty.py'
    text = re.sub(r'<[^>]+>|data:image[^"]+', ' ', html)
    assert 'Alketa' not in text and 'Xhekiqi' not in text, 'no parent name yet for that family'
    assert not re.search(r'\d{3}\D{0,3}\d{3}\D{0,3}\d{4}', text), 'no phone numbers'
    assert not re.search(r'[\w.]+@[\w.]+', text), 'no email addresses'
    assert all(re.fullmatch(r'\w+ \w\.', p) for g in ('g1', 'g2') for p in build_duty.P[g]), 'first name + initial only'
    assert 'noindex' in html and 'The Imam will let you know if we need more or fewer' in html
