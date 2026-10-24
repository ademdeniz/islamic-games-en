"""Tests for the Sunday pizza & parent duty page (tools/build_duty.py -> duty/index.html)."""
import os
import re
import sys

import pytest

import gamecheck as gc

sys.path.insert(0, os.path.join(gc.ROOT, 'tools'))
import build_duty  # noqa: E402
import build_plan  # noqa: E402
from build_lessons_core import brand  # noqa: E402,F401

PAGE = os.path.join(gc.ROOT, 'duty', 'index.html')


def test_turns_go_round_and_start_again_from_the_top():
    r, P = build_duty.rota(), build_duty.P
    assert [d for d, _, _ in r] == [d for d in build_plan.class_days() if d >= P['start']], 'every class Sunday of the year'
    for g, i in (('g1', 1), ('g2', 2)):
        done = {x[g] for x in P.get('done', []) if x.get(g)}
        names = [x[i] for x in r]
        first = [p for p in P[g] if p not in done]
        assert names[:len(first)] == first, 'first everyone who has not had a turn, in order'
        rest = names[len(first):]
        assert rest == (P[g] * len(r))[:len(rest)], 'then the whole list again from the top, round after round'
        assert build_duty.TBA not in names


def test_no_families_no_rota(monkeypatch):
    monkeypatch.setitem(build_duty.P, 'g1', [])
    monkeypatch.setitem(build_duty.P, 'g2', [])
    assert build_duty.rota() == []


def test_one_empty_group_waits_for_families(monkeypatch):
    monkeypatch.setitem(build_duty.P, 'g2', [])
    r = build_duty.rota()
    assert r and all(b == build_duty.TBA for _, _, b in r) and all(a != build_duty.TBA for _, a, _ in r)


def test_page_is_current_and_shares_nothing_private():
    html = open(PAGE, encoding='utf-8').read()
    build_duty.build()
    assert open(PAGE, encoding='utf-8').read() == html, 'run python3 tools/build_duty.py'
    text = re.sub(r'<[^>]+>|data:image[^"]+', ' ', html)
    assert 'Alketa' not in text, 'a student’s name, not a parent’s – that family is listed by family name'
    assert not re.search(r'\d{3}\D{0,3}\d{3}\D{0,3}\d{4}', text), 'no phone numbers'
    assert not re.search(r'[\w.]+@[\w.]+', text), 'no email addresses'
    assert all(re.fullmatch(r'\w+ (\w\.|family)', p) for g in ('g1', 'g2') for p in build_duty.P[g]), 'first name + initial only'
    assert '9:00 – 11:45 am' in html and '11:45 am – 12:15 pm' in html and 'from 12:15 pm' in html
    assert 'starts again from the top' in html and 'noindex' in html and 'The Imam will let you know if we need more or fewer' in html


def test_done_turns_are_shown_with_a_tick():
    html = open(PAGE, encoding='utf-8').read()
    done = build_duty.P.get('done', [])
    if not done:
        pytest.skip('no duty done yet')
    for x in done:
        assert f'<tr data-d="{x["date"]}" class=done>' in html and (x.get('g1') or x.get('g2')) in html
