"""Tests for the Ilmihal lesson pages (data/lessons -> lessons/)."""
import glob
import json
import os
import re
import sys
import urllib.request

import pytest

import gamecheck as gc

sys.path.insert(0, os.path.join(gc.ROOT, 'tools'))
import build_lessons  # noqa: E402

BOOKS = build_lessons.load_all()
LESSONS = [l for b in BOOKS.values() for l in b['lessons']]
IDS = [f"{l['book']}/{l['id']}" for l in LESSONS]
LEARN_TYPES = {'phrase', 'text', 'heading', 'quran', 'list', 'cards', 'point'}


def page_path(l):
    return os.path.join(gc.ROOT, 'lessons', l['book'], l['id'], 'index.html')


def strings(obj):
    if isinstance(obj, str):
        yield re.sub(r'<[^>]+>', '', obj)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k not in ('ar', 'audio', 'type', 'icon', 'source'):   # source = the book credit with authors' names
                yield from strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings(v)


# ---------------------------------------------------------------- data
@pytest.mark.parametrize('lesson', LESSONS, ids=IDS)
def test_lesson_data_is_valid(lesson):
    for k in ('number', 'title', 'pages', 'intro', 'learn', 'practice'):
        assert lesson.get(k), k
    assert all(b['type'] in LEARN_TYPES for b in lesson['learn'])
    kinds = [a['type'] for a in lesson['practice']]
    assert sum(k != 'reflect' for k in kinds) >= 2, 'at least two activities that earn stars'
    for a in lesson['practice']:
        if a['type'] == 'quiz':
            for q in a['questions']:
                assert 0 <= q['answer'] < len(q['options']) and len(set(q['options'])) == len(q['options']), q['q']
        elif a['type'] == 'order':
            assert len(a['items']) >= 3 and len(set(a['items'])) == len(a['items'])
        elif a['type'] == 'memory':
            assert len(a['pairs']) >= 3 and len({x for p in a['pairs'] for x in p}) == 2 * len(a['pairs'])
        elif a['type'] == 'sort':
            assert all(0 <= i['bin'] < len(a['bins']) for i in a['items'])
            assert {i['bin'] for i in a['items']} == set(range(len(a['bins']))), 'every bin is used'
        elif a['type'] == 'choose_all':
            assert any(o['correct'] for o in a['options']) and all(o.get('why') for o in a['options'] if not o['correct'])


@pytest.mark.parametrize('lesson', LESSONS, ids=IDS)
def test_lesson_is_english(lesson):
    import skel
    hits = {m.group(0) for s in strings(lesson) for m in skel.BS_WORDS.finditer(s)}
    assert not hits - {'Rekić'}, f'Bosnian words: {hits}'


def _quotes(obj):
    if isinstance(obj, dict):
        if obj.get('type') == 'quran' or ('ref' in obj and 'text' in obj):
            yield obj
        for v in obj.values():
            yield from _quotes(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _quotes(v)


def _norm(s):
    return re.sub(r'[^a-z]+', ' ', s.lower()).strip()


@pytest.mark.parametrize('lesson', LESSONS, ids=IDS)
def test_quran_quotes_are_exact_sahih_international(lesson):
    """Each quote (or each part of it around …) must appear word for word in Sahih International."""
    for q in _quotes(lesson):
        m = re.search(r'(\d+):(\d+)(?:–(\d+))?$', q['ref'])
        s, a0, a1 = int(m.group(1)), int(m.group(2)), int(m.group(3) or m.group(2))
        try:
            full = ' '.join(json.load(urllib.request.urlopen(
                f'https://api.alquran.cloud/v1/ayah/{s}:{a}/en.sahih', timeout=20))['data']['text'] for a in range(a0, a1 + 1))
        except Exception:
            pytest.skip('AlQuran.cloud not reachable')
        for part in q['text'].split('…'):
            if _norm(part):
                assert _norm(part) in _norm(full), f"{q['ref']}: “{part.strip()}” is not in Sahih International"


# ---------------------------------------------------------------- pages
def test_every_lesson_has_a_page_and_is_listed():
    idx = open(os.path.join(gc.ROOT, 'lessons', 'index.html'), encoding='utf-8').read()
    for l in LESSONS:
        assert os.path.exists(page_path(l)), l['id']
        assert f'"{l["id"]}"' in idx
    pages = glob.glob(os.path.join(gc.ROOT, 'lessons', '*', '*', 'index.html'))
    assert len(pages) == len(LESSONS), 'no leftover pages for deleted lessons'


@pytest.fixture
def page(browser):
    p = browser.new_page(viewport={'width': 430, 'height': 900})
    p.errors = []
    p.on('pageerror', lambda e: p.errors.append(str(e)))
    p.route(re.compile(r'^https?://'), lambda route: route.abort())
    yield p
    assert not p.errors, p.errors
    p.close()


def play(page, box, a):
    """Complete one activity the way a child would (knowing the answers)."""
    if a['type'] == 'order':
        for k in range(len(a['items'])):
            box.locator(f'.pool .chip[data-k="{k}"]').click()
    elif a['type'] == 'choose_all':
        for k, o in enumerate(a['options']):
            if o['correct']:
                box.locator(f'.opt[data-k="{k}"]').click()
        box.locator('button:has-text("Check")').click()
    elif a['type'] == 'quiz':
        by_q = {q['q']: q['answer'] for q in a['questions']}
        for _ in a['questions']:
            qtext = box.locator('.qn').inner_text().split('. ', 1)[1]
            box.locator(f'.opt[data-k="{by_q[qtext]}"]').click()
            page.wait_for_timeout(1000)
    elif a['type'] == 'memory':
        cards = page.evaluate(f"[...document.querySelectorAll('#{box.get_attribute('id')} .mc')].map(b=>+b.dataset.k)")
        for k in range(len(a['pairs'])):
            for j in [j for j, x in enumerate(cards) if x == k]:
                box.locator(f'.mc[data-j="{j}"]').click()
    elif a['type'] == 'sort':
        bins = {i['text']: i['bin'] for i in a['items']}
        for _ in a['items']:
            box.locator(f'[data-b="{bins[box.locator(".sortq").inner_text()]}"]').click()
            page.wait_for_timeout(900)


@pytest.mark.parametrize('lesson', LESSONS, ids=IDS)
def test_every_activity_can_be_completed_and_earns_stars(page, lesson):
    page.goto('file://' + page_path(lesson))
    assert page.inner_text('#title') == lesson['title']
    for i, a in enumerate(lesson['practice']):
        if a['type'] == 'reflect':
            continue
        box = page.locator(f'#act{i}')
        play(page, box, a)
        page.wait_for_function(f"document.getElementById('act{i}').classList.contains('done')", timeout=5000)
    assert 'Lesson complete' in page.inner_text('#stars')
    page.reload()
    assert 'Lesson complete' in page.inner_text('#stars'), 'stars are remembered'


def test_wrong_answers_do_not_earn_stars(page):
    lesson = next(l for l in LESSONS if any(a['type'] == 'choose_all' for a in l['practice']))
    page.goto('file://' + page_path(lesson))
    i, a = next((i, a) for i, a in enumerate(lesson['practice']) if a['type'] == 'choose_all')
    wrong = next(k for k, o in enumerate(a['options']) if not o['correct'])
    box = page.locator(f'#act{i}')
    box.locator(f'.opt[data-k="{wrong}"]').click()
    box.locator('button:has-text("Check")').click()
    assert 'done' not in box.get_attribute('class')
    assert a['options'][wrong]['why'] in box.inner_text()


def test_lessons_page_links_to_every_lesson(page):
    page.goto('file://' + os.path.join(gc.ROOT, 'lessons', 'index.html'))
    hrefs = page.eval_on_selector_all('a.lesson', 'as => as.map(a => a.getAttribute("href"))')
    assert hrefs == [f"{l['book']}/{l['id']}/" for l in LESSONS]
