"""Tests for the Read Along game (games/citaj-kuran): data integrity, word highlighting, speed, reciters, pages."""
import json
import os
import re

import pytest

import gamecheck as gc

DATA = json.load(open(os.path.join(gc.ROOT, 'data', 'readalong.json'), encoding='utf-8'))
PAGE = 'file://' + os.path.join(gc.ROOT, 'games', 'citaj-kuran', 'index.html')
ARABIC = re.compile(r'[؀-ۿ]')


# ---------------------------------------------------------------- data
def test_pages_are_the_requested_ayahs():
    keys = {p['id']: [l['key'] for l in p['lines']] for p in DATA['pages']}
    assert keys['baqarah-17-24'] == [f'2:{n}' for n in range(17, 25)]
    assert keys['yasin-1-12'] == ['1:1'] + [f'36:{n}' for n in range(1, 13)], 'Ya-Sin starts with the Bismillah'


@pytest.mark.parametrize('page', DATA['pages'], ids=lambda p: p['id'])
def test_every_line_has_arabic_words_meaning_and_timed_audio(page):
    for l in page['lines']:
        assert l['words'] and all(ARABIC.search(w) for w in l['words']), l['key']
        assert l['en'] and l['tr'], l['key']
        for rid in DATA['reciters']:
            a = l['audio'][rid]
            assert a['url'].startswith('https://') and a['url'].endswith('.mp3'), (l['key'], rid)
            segs = a['segments']
            assert segs, f'{l["key"]} {rid}: no word timings'
            for k, start, end in segs:
                assert 0 <= k < len(l['words']) and 0 <= start < end, (l['key'], rid, k, start, end)
            starts = [s[1] for s in segs]
            assert starts == sorted(starts), f'{l["key"]} {rid}: timings out of order'


# ---------------------------------------------------------------- browser
@pytest.fixture
def page(browser):
    p = browser.new_page()
    p.errors = []
    p.on('pageerror', lambda e: p.errors.append(str(e)))
    p.route(re.compile(r'^https://'), lambda route: route.abort())  # offline: fonts/audio not needed for these checks
    p.goto(PAGE)
    yield p
    assert not p.errors, p.errors
    p.close()


def words_on_screen(page):
    return page.eval_on_selector_all('#arabic .w', 'els => els.map(e => e.textContent)')


def test_shows_original_arabic_not_transliteration(page):
    first = DATA['pages'][0]['lines'][0]
    assert words_on_screen(page) == first['words']
    assert page.is_hidden('#trBox') and page.is_hidden('#enBox'), 'Arabic only by default'
    assert 'Ayah 17 • 1 of 8' in page.inner_text('#info')


def test_highlights_the_word_being_recited(page):
    line = DATA['pages'][0]['lines'][0]
    for k, start, end in line['audio']['alafasy']['segments']:
        mid = (start + end) / 2
        assert page.evaluate(f'RA.highlightAt({mid})') == k
        assert page.eval_on_selector_all('#arabic .w.on', 'els => els.map(e => +e.dataset.k)') == [k]
    assert page.evaluate('RA.highlightAt(999999)') == -1   # after the ayah: nothing highlighted …
    assert len(page.query_selector_all('#arabic .w.done')) == len(line['words'])   # … and all words marked as read


def test_speed_options_slow_the_recitation_and_are_remembered(page):
    for label, rate in [('Slower', 0.75), ('Slowest', 0.5), ('Normal', 1)]:
        page.click(f'#speed button:text("{label}")')
        assert page.evaluate('[RA.player.playbackRate, RA.player.defaultPlaybackRate, RA.state().rate]') == [rate] * 3
    page.click('#speed button:text("Slowest")')
    page.reload()
    assert page.evaluate('RA.state().rate') == 0.5
    assert page.get_attribute('#speed button:text("Slowest")', 'aria-pressed') == 'true'


def test_slow_teaching_reciter_uses_its_own_audio_and_timings(page):
    page.select_option('#reciter', 'husary')
    page.click('#play')
    page.wait_for_function("RA.player.src.includes('Husary_Muallim')")
    husary = DATA['pages'][0]['lines'][0]['audio']['husary']['segments']
    k, start, end = husary[-1]
    assert page.evaluate(f'RA.highlightAt({(start + end) / 2})') == k


def test_yasin_page_starts_with_bismillah(page):
    page.click('#pages .chip:text("Ya-Sin 1–12")')
    assert 'Bismillah • 1 of 13' in page.inner_text('#info')
    page.click('#next')
    assert 'Ayah 1 • 2 of 13' in page.inner_text('#info')
    assert words_on_screen(page) == DATA['pages'][1]['lines'][1]['words']


def test_previous_next_and_end_of_page(page):
    assert page.is_disabled('#prev')
    for _ in range(7):
        page.click('#next')
    assert 'Ayah 24 • 8 of 8' in page.inner_text('#info')
    page.click('#next')
    assert 'Well done' in page.inner_text('#status')
    page.click('#prev')
    assert 'Ayah 23' in page.inner_text('#info')


def test_meaning_and_transliteration_can_be_shown(page):
    page.check('#showEn')
    assert page.is_visible('#enBox') and 'Their example' in page.inner_text('#en')
    page.check('#showTr')
    assert page.is_visible('#trBox')


def test_offline_audio_shows_a_message(page):
    page.click('#play')
    page.wait_for_function("document.getElementById('status').textContent.includes('Check your internet')")


def test_real_recitation_moves_the_highlight(browser):
    """Plays the real audio (needs internet) and checks the highlight follows it."""
    p = browser.new_page()
    p.goto(PAGE)
    p.click('#play')
    try:
        p.wait_for_function('RA.player.currentTime > 2.5', timeout=20000)
    except Exception:
        p.close()
        pytest.skip('audio could not be played here (offline or no audio support)')
    word = p.evaluate("+document.querySelector('#arabic .w.on')?.dataset.k")
    assert word >= 1, 'after 2.5 s the reciter is past the first word'
    p.close()
