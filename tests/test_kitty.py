"""Tests for "Let’s Help the Kitty Make Wudu": the painted drops are tappable in Wudu order, on any screen size."""
import os
import re

import pytest

import gamecheck as gc

PAGE = 'file://' + os.path.join(gc.ROOT, 'games', 'pomozimo-maci-abdest', 'index.html')
ORDER = ['A’udhu, Bismillah and niyyah', 'Hands 3x', 'Mouth 3x', 'Nose 3x', 'Face 3x', 'Right arm past the elbow 3x',
         'Left arm past the elbow 3x', 'Masah (wipe the head)', 'Ears', 'Neck', 'Right foot up to the ankle',
         'Left foot up to the ankle', 'Shahadah']
SIZES = {'laptop': (1280, 800), 'tablet': (768, 1024), 'phone': (390, 844), 'phone-landscape': (844, 390)}


@pytest.fixture(params=list(SIZES), ids=list(SIZES))
def page(browser, request):
    w, h = SIZES[request.param]
    p = browser.new_page(viewport={'width': w, 'height': h})
    p.errors = []
    p.on('pageerror', lambda e: p.errors.append(str(e)))
    p.route(re.compile(r'^https?://'), lambda route: route.abort())
    p.goto(PAGE)
    yield p
    assert not p.errors, p.errors
    p.close()


def spot(page, name):
    return page.locator(f'.spot[aria-label="{name}"]')


def inside_viewport(page, locator):
    box = locator.bounding_box()
    vw, vh = page.viewport_size['width'], page.viewport_size['height']
    return box and box['x'] >= -1 and box['y'] >= -1 and box['x'] + box['width'] <= vw + 1 and box['y'] + box['height'] <= vh + 1


def test_start_button_and_all_13_drops_are_on_screen(page):
    assert inside_viewport(page, page.locator('#start')), 'START must be reachable without scrolling'
    assert page.locator('.spot').count() == 13
    for name in ORDER:
        assert inside_viewport(page, spot(page, name)), f'drop "{name}" is cut off'


def test_drops_are_not_tappable_before_start(page):
    spot(page, ORDER[0]).click(force=True)
    assert page.inner_text('#progress') == 'Step 0 / 13'


def test_collecting_all_drops_in_wudu_order_finishes_the_game(page):
    page.click('#start')
    for n, name in enumerate(ORDER, 1):
        spot(page, name).click()
        assert page.inner_text('#progress') == f'Step {n} / 13'
    assert page.locator('.miniDrop').count() == 13, 'every drop shows up in COLLECTED'
    assert 'Well done' in page.inner_text('#message')
    assert int(page.inner_text('#score')) == 130
    assert page.is_visible('#start') and 'PLAY AGAIN' in page.inner_text('#start')


def test_wrong_drop_costs_points_and_two_mistakes_show_a_hint(page):
    page.click('#start')
    spot(page, ORDER[0]).click()                 # +10
    spot(page, 'Neck').click()                   # wrong: −3
    assert page.inner_text('#progress') == 'Step 1 / 13' and page.inner_text('#score') == '7'
    assert 'hint' not in (spot(page, ORDER[1]).get_attribute('class') or '')
    spot(page, 'Ears').click()                   # second mistake -> the right drop glows
    assert 'hint' in spot(page, ORDER[1]).get_attribute('class')
    spot(page, ORDER[1]).click()
    assert page.inner_text('#progress') == 'Step 2 / 13'
    assert 'hint' not in spot(page, ORDER[1]).get_attribute('class')


def test_tap_areas_sit_on_the_painted_drops(page):
    """The centre of each tap area must map back into that drop's outline in the picture, whatever the screen size."""
    # where the picture is really drawn, read back from the page's own background settings
    res = page.evaluate("""() => {const G=document.getElementById('game'),g=G.getBoundingClientRect(),
        [bw]=G.style.backgroundSize.split(' ').map(parseFloat),[ox,oy]=G.style.backgroundPosition.split(' ').map(parseFloat),s=bw/1536;
        return [...document.querySelectorAll('.spot')].map(b=>{const r=b.getBoundingClientRect();
          return [(r.left-g.left+r.width/2-ox)/s,(r.top-g.top+r.height/2-oy)/s]})}""")
    spots = __import__('importlib').import_module('gamecheck').table('pomozimo-maci-abdest').SPOTS
    for (x, y), (x0, y0, x1, y1) in zip(res, spots):
        assert x0 < x < x1 and y0 < y < y1, (x, y, (x0, y0, x1, y1))


def test_play_again_resets_the_drops(page):
    page.click('#start')
    for name in ORDER:
        spot(page, name).click()
    page.click('#start')
    assert page.inner_text('#progress') == 'Step 0 / 13'
    assert page.locator('.spot.got').count() == 0


def test_score_box_covers_the_painted_one_and_collected_bar_does_not_cover_the_picture(page):
    r = page.evaluate("""() => {const G=document.getElementById('game'),g=G.getBoundingClientRect(),
        [bw]=G.style.backgroundSize.split(' ').map(parseFloat),[ox,oy]=G.style.backgroundPosition.split(' ').map(parseFloat),s=bw/1536,
        h=document.getElementById('hud').getBoundingClientRect(),c=document.getElementById('collected').getBoundingClientRect();
        return {hud:[(h.left-g.left-ox)/s,(h.top-g.top-oy)/s,(h.right-g.left-ox)/s,(h.bottom-g.top-oy)/s],collectedBottom:c.bottom-g.top,pictureTop:oy}}""")
    x0, y0, x1, y1 = r['hud']
    assert abs(x0 - 1292) < 12 and abs(y0 - 18) < 12 and abs(x1 - 1520) < 12 and abs(y1 - 330) < 12, r['hud']
    assert r['collectedBottom'] <= r['pictureTop'] + 1, r


def test_logo_header_is_shown(page):
    box = page.locator('.bz-brand img').bounding_box()
    assert box and box['height'] > 20 and box['y'] >= 0
    assert box['x'] >= 0 and box['x'] + box['width'] <= page.viewport_size['width'], 'logo must not be cut off'
