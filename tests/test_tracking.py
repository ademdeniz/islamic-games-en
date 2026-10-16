"""The activity tracker (tools/tracking.js) is on every children's page – lessons, Sufara, every game (Read Along, surahs) –
once, and nowhere else; with no Supabase project (the clean starter) pages get none; and it never gets in the way."""
import glob
import json
import os
import sys

import pytest

from conftest import ROOT

sys.path.insert(0, os.path.join(ROOT, 'tools'))
import tracking  # noqa: E402

MARK = 'Maktab tracker'
TRACKED = (glob.glob(os.path.join(ROOT, 'lessons', '*', '*', 'index.html')) +
           glob.glob(os.path.join(ROOT, 'sufara', '*', 'index.html')) +
           glob.glob(os.path.join(ROOT, 'games', '*', 'index.html')))
UNTRACKED = [os.path.join(ROOT, p) for p in ('index.html', 'lessons/index.html', 'sufara/index.html', 'plan/index.html',
                                             'duty/index.html', 'waiver/index.html')]


def test_tracker_on_every_childrens_page_once():
    assert len(TRACKED) > 130
    cfg = json.load(open(os.path.join(ROOT, 'supabase', 'config.json')))
    for p in TRACKED:
        page = open(p, encoding='utf-8').read()
        assert page.count(MARK) == 1, p
        assert cfg['url'] in page and cfg['publishable_key'] in page, p
        assert '__URL__' not in page and '__KEY__' not in page, p
        assert page.index(MARK) > page.rfind('</main>'), 'tracker must come after the page itself: ' + p


def test_tracker_not_on_other_pages():
    for p in UNTRACKED:
        if os.path.exists(p):
            assert MARK not in open(p, encoding='utf-8').read(), p


def test_no_supabase_project_means_no_tracker(tmp_path, monkeypatch):
    (tmp_path / 'supabase').mkdir()
    (tmp_path / 'tools').mkdir()
    (tmp_path / 'tools' / 'tracking.js').write_text(open(os.path.join(ROOT, 'tools', 'tracking.js')).read())
    (tmp_path / 'supabase' / 'config.json').write_text('{"url": "", "publishable_key": ""}')
    monkeypatch.setattr(tracking, 'ROOT', str(tmp_path))
    assert tracking.add('<body>x</body>') == '<body>x</body>'


@pytest.mark.parametrize('page', ['lessons/ilmihal-1/01-audhu-bismillah', 'sufara/01-alif', 'games/citaj-kuran'])
def test_sign_in_card_shows_and_steps_aside(page, browser):
    """A child's first visit shows the class-code card; “just looking” closes it for good; no errors; nothing sent."""
    ctx = browser.new_context()
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")
    p = ctx.new_page()
    sent, errors = [], []
    p.on('request', lambda r: sent.append(r.url) if 'supabase.co' in r.url else None)
    p.on('pageerror', lambda e: errors.append(str(e)))
    p.goto('file://' + os.path.join(ROOT, page, 'index.html'))
    assert p.locator('#veil').is_visible() and p.locator('#code').is_visible()
    p.locator('#look').click()
    assert not p.locator('#veil').is_visible()
    assert p.locator('#chip').text_content() == '👤 Sign in'
    p.reload()
    assert not p.locator('#veil').is_visible()
    assert not errors and not sent
    ctx.close()


def test_automated_browsers_see_no_card(browser):
    """The page tests (and other robots) click through pages; the card must not cover them."""
    p = browser.new_page()
    p.goto('file://' + TRACKED[0])
    assert p.locator('#veil').count() == 0
    p.close()


def test_games_compare_without_the_tracker():
    """The translation checks read games without the tracker, so its English/Bosnian texts are not counted as game text."""
    import gamecheck as gc
    for game in ('kviz-namaz', 'memori-sure', 'mektebski-fudbal'):
        page = open(os.path.join(ROOT, 'games', game, 'index.html'), encoding='utf-8').read()
        assert MARK in page and MARK not in gc.translated_html(game)
        assert tracking.strip(page) == gc.translated_html(game)
