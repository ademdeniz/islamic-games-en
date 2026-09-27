"""Tests for the yearly class plan (tools/build_plan.py -> plan/index.html, the read-only copy for parents)."""
import os
import re
import sys

import pytest

import gamecheck as gc

sys.path.insert(0, os.path.join(gc.ROOT, 'tools'))
import build_plan  # noqa: E402

D = build_plan.data
PARENTS = os.path.join(gc.ROOT, 'plan', 'index.html')


def local(url):
    assert url.startswith(D['site']), url
    return os.path.join(gc.ROOT, url[len(D['site']):].split('#')[0], 'index.html')


def test_every_link_points_to_a_real_page():
    urls = {it['url'] for items in D['tracks'].values() for it in items if it['url']}
    urls |= {D['site'] + 'games/' + s + '/' for s in D['games']}
    missing = [u for u in urls if not os.path.exists(local(u))]
    assert not missing, missing


def test_built_lessons_and_surahs_are_linked():
    items = {it['k']: it['url'] for items in D['tracks'].values() for it in items}
    assert items['i1-9'].endswith('lessons/ilmihal-1/01-audhu-bismillah/'), 'lesson 1 covers book pages 8–9'
    assert items['i2-10'].endswith('lessons/ilmihal-2/02-amantu-billahi/')
    assert items['i3-11'].endswith('games/learn-surahs-by-heart/#fil')
    assert items['i1-84'].endswith('#nasr') and items['i1-43'].endswith('#nas')
    assert items['i3-12'].endswith('lessons/ilmihal-3/02-amantu-billahi/')


def test_every_game_topic_is_used_and_fallbacks_exist():
    assert all(s in D['games'] for f in D['fallback'].values() for s in f)
    used = {t for items in D['tracks'].values() for it in items for t in it['topics']} | {'ramadan', 'blessed-nights', 'eid'}
    assert all(set(g['topics']) & used for g in D['games'].values()), 'a game no lesson can ever pick'


def test_parents_copy_is_up_to_date():
    from build_lessons_core import brand
    assert open(PARENTS, encoding='utf-8').read() == brand(build_plan.page(True)), 'run python3 tools/build_plan.py'


# ---------------------------------------------------------------- browser
@pytest.fixture
def page(browser):
    p = browser.new_page(viewport={'width': 390, 'height': 900})
    p.errors = []
    p.on('pageerror', lambda e: p.errors.append(str(e)))
    p.route(re.compile(r'^https?://'), lambda route: route.abort())
    yield p
    assert not p.errors, p.errors
    p.close()


def test_parents_copy_is_read_only_and_branded(page):
    page.goto('file://' + PARENTS)
    assert page.locator('.week').count() == len(D['sundays'])
    assert page.locator('input, textarea').count() == 0, 'no ticks, notes or switches for parents'
    assert page.locator('#status, #prog').count() == 0
    text = page.inner_text('body')
    assert 'to build' not in text and 'Tick lessons' not in text
    assert page.locator('div.bz-brand img').count() == 1
    hrefs = page.eval_on_selector_all('a', 'as => as.map(a => a.getAttribute("href"))')
    assert D['site'] not in hrefs and not any(h.startswith('../') for h in hrefs), 'no link to the whole site'
    assert page.evaluate('document.documentElement.scrollWidth') <= 390, 'no sideways scrolling on a phone'


def test_every_lesson_is_planned_once_and_in_order(page):
    page.goto('file://' + PARENTS)
    plan = page.evaluate('schedule()')
    for t, items in D['tracks'].items():
        seen = [x['it']['k'] for d in D['sundays'] if d in plan for x in plan[d].get(t, []) if not x.get('cont')]
        want = [it['k'] for it in items]
        if t == 'qr':
            want = want[:len(plan)]            # one mushaf page per class
        assert seen == want, t


def test_no_class_days_and_tajwid_start(page):
    page.goto('file://' + PARENTS)
    for d, why in D['noClass'].items():
        assert why in page.inner_text(f'#w-{d}') and page.locator(f'#w-{d} .grp').count() == 0
    plan = page.evaluate('schedule()')
    assert all(not plan[d]['tj'] for d in plan if d < D['starts']['tj'])
    assert plan[min(d for d in plan if d >= D['starts']['tj'])]['tj'][0]['it']['k'] == 'tj-0'
    assert page.locator('#w-2026-10-25 .pin').count() == 0 and 'competition' in page.inner_text('#w-2026-11-01 .pin')


def test_group_switch(page):
    page.goto('file://' + PARENTS)
    page.click('#grpSeg [data-g="g2"]')
    first = page.inner_text('#w-2026-09-27').lower()
    assert 'group 2' in first and 'group 1' not in first and 'alif' in first
