"""Tests for "Learn the Surahs by Heart" (games/learn-surahs-by-heart)."""
import json
import os
import re

import pytest

import gamecheck as gc

DATA = json.load(open(os.path.join(gc.ROOT, 'data', 'hifz.json'), encoding='utf-8'))
PAGE = 'file://' + os.path.join(gc.ROOT, 'games', 'learn-surahs-by-heart', 'index.html')
ARABIC = re.compile(r'[؀-ۿ]')
BY_ID = {s['id']: s for s in DATA['surahs']}


# ---------------------------------------------------------------- content
def test_has_every_surah_from_the_memory_game_plus_ayat_al_kursi():
    keys = {l['key'] for s in DATA['surahs'] for l in s['lines']}
    for surah, count in [(1, 7), (101, 11), (102, 8), (103, 3), (104, 9), (105, 5), (106, 4), (107, 7), (108, 3),
                         (109, 6), (110, 3), (111, 5), (112, 4), (113, 5), (114, 6)]:
        assert {f'{surah}:{n}' for n in range(1, count + 1)} <= keys, f'surah {surah} incomplete'
    assert {f'2:{n}' for n in range(1, 6)} <= keys, 'Alif-Lam-Mim (Al-Baqarah 1–5)'
    assert '2:255' in keys, 'Ayat al-Kursi'
    assert len(DATA['surahs']) == 17


def test_bismillah_before_each_surah_except_fatiha_and_ayat_al_kursi():
    for s in DATA['surahs']:
        first = s['lines'][0]
        expect = s['id'] not in ('fatiha', 'kursi')
        assert (first['n'] == 0) == expect, s['id']


@pytest.mark.parametrize('surah', DATA['surahs'], ids=lambda s: s['id'])
def test_every_ayah_is_complete_and_timed(surah):
    for l in surah['lines']:
        assert all(ARABIC.search(w) for w in l['words']), l['key']
        assert len(l['wtr']) == len(l['words']) and all(l['wtr']), f'{l["key"]}: transliteration for every word'
        assert l['en'], l['key']
        # parts cover every word exactly once, in order
        flat = [k for a, b in l['parts'] for k in range(a, b)]
        assert flat == list(range(len(l['words']))), f'{l["key"]}: parts {l["parts"]}'
        assert all(b - a >= 2 or len(l['words']) == 1 or len(l['parts']) == 1 for a, b in l['parts']), l['parts']
        for rid in DATA['reciters']:
            segs = l['audio'][rid]['segments']
            assert l['audio'][rid]['url'].startswith('https://')
            assert segs and all(0 <= k < len(l['words']) and 0 <= t0 < t1 for k, t0, t1 in segs), (l['key'], rid)
            for a, b in l['parts']:   # every part can be played on its own
                assert any(a <= k < b for k, _, _ in segs), f'{l["key"]} {rid}: part {a}-{b} has no timing'


def test_transliteration_is_kid_friendly_and_recited_style():
    alltr = ' '.join(w for s in DATA['surahs'] for l in s['lines'] for w in l['wtr'])
    assert not re.search('[ḥṣḍṭẓāīūʿ]', alltr), 'no scholarly letters'
    ikhlas = BY_ID['ikhlas']['lines']
    assert ikhlas[2]['wtr'] == ['Allahu', 's-samad'], 'sun letter + stop at the end of the ayah'
    assert BY_ID['fatiha']['lines'][0]['wtr'][-2:] == ['r-rahmaani', 'r-raheem']
    assert BY_ID['fatiha']['lines'][2]['wtr'][0] == 'ar-rahmaani', 'word-initial al- before a sun letter'
    assert not re.search(r'(?<![\w-])al-(th|dh|sh|t|d|r|z|s|n)', alltr, re.I), 'al- before a sun letter must assimilate'


# ---------------------------------------------------------------- browser
@pytest.fixture
def page(browser):
    p = browser.new_page()
    p.errors = []
    p.on('pageerror', lambda e: p.errors.append(str(e)))
    p.route(re.compile(r'^https://'), lambda route: route.abort())
    p.goto(PAGE)
    yield p
    assert not p.errors, p.errors
    p.close()


def choose(page, sid):
    page.select_option('#surah', str([s['id'] for s in DATA['surahs']].index(sid)))


def test_picker_lists_all_surahs_in_learning_order(page):
    titles = page.eval_on_selector_all('#surah option', 'os => os.map(o => o.textContent)')
    assert titles[0] == 'Al-Fatiha' and titles[1] == 'An-Nas' and titles[-1].startswith('Ayat al-Kursi')
    assert len(titles) == 17


def test_follow_shows_whole_surah_in_arabic_and_transliteration(page):
    choose(page, 'nas')
    s = BY_ID['nas']
    assert page.eval_on_selector_all('#text .ar .w', 'e => e.length') == sum(len(l['words']) for l in s['lines'])
    assert page.eval_on_selector_all('#text .tr .w', 'e => e.length') == sum(len(l['words']) for l in s['lines'])
    page.uncheck('#showTr')
    assert page.is_hidden('#text .tr')
    page.uncheck('#showAr')
    assert page.is_hidden('#text .ar')


def test_highlight_follows_recitation_and_moves_the_pointer(page):
    choose(page, 'ikhlas')
    line = BY_ID['ikhlas']['lines'][2]            # "Allahu s-samad"
    k, t0, t1 = line['audio']['alafasy']['segments'][1]
    assert page.evaluate(f'HZ.highlight(2, {(t0 + t1) / 2})') == k
    assert page.eval_on_selector_all('#text .w.on', 'e => e.map(x => x.textContent)') == [line['words'][k], line['wtr'][k]]
    assert page.evaluate('HZ.state().pIdx') == [i for i, p in enumerate(page.evaluate('HZ.parts()')) if p['li'] == 2][0]
    assert 'AYAH 2' in page.inner_text('#counter')


def test_part_playback_range_starts_and_stops_at_the_right_words(page):
    choose(page, 'kursi')
    parts = page.evaluate('HZ.parts()')
    segs = BY_ID['kursi']['lines'][0]['audio']['alafasy']['segments']
    r = page.evaluate('HZ.range(HZ.parts()[2])')
    a, b = parts[2]['a'], parts[2]['b']
    assert r['from'] == min(s[1] for s in segs if a <= s[0] < b)
    assert r['to'] == max(s[2] for s in segs if a <= s[0] < b)
    assert page.evaluate('HZ.range(HZ.parts()[0])')['from'] == 0, 'first part plays from the start of the ayah'
    assert page.evaluate(f'HZ.range(HZ.parts()[{len(parts) - 1}])')['to'] is None, 'last part plays to the end'


def test_build_the_ayah_adds_one_part_at_a_time(page):
    choose(page, 'kursi')
    page.click('#tBuild')
    parts = BY_ID['kursi']['lines'][0]['parts']
    assert page.eval_on_selector_all('#text .ar .w', 'e => e.length') == parts[0][1]
    page.click('#bAdd')
    assert page.eval_on_selector_all('#text .ar .w', 'e => e.length') == parts[1][1]
    assert 'Step 2 of 8' in page.inner_text('#panel')


def test_smart_review_hides_the_part_until_show_and_saves_progress(page):
    choose(page, 'kawthar')
    page.click('#tSmart')
    assert page.is_visible('#reveal')
    before = page.eval_on_selector_all('#text .ar .w', 'e => e.length')
    page.click('#reveal')
    assert page.eval_on_selector_all('#text .ar .w', 'e => e.length') > before
    for _ in range(12):
        page.click('button[data-rate="2"]')   # "I know it" every time
    assert 'Al-Kawthar ⭐' in page.inner_text('#surah'), 'progress shows in the surah picker'
    page.reload()
    choose(page, 'kawthar')
    assert max(page.evaluate('HZ.state().score')) >= 3, 'progress is remembered'


def test_speed_and_slow_reciter(page):
    page.click('#speed button:text("Slowest")')
    assert page.evaluate('[HZ.player.playbackRate, HZ.state().rate]') == [0.5, 0.5]
    page.select_option('#reciter', 'husary')
    page.click('#playPart')
    page.wait_for_function("HZ.player.src.includes('Husary_Muallim')")


def test_offline_shows_a_message(page):
    page.click('#playPart')
    page.wait_for_function("document.getElementById('pointer').textContent.includes('Check your internet')")


def test_real_recitation_highlights_words(browser):
    p = browser.new_page()
    p.goto(PAGE)
    p.select_option('#surah', '1')            # An-Nas
    p.click('#whole')
    try:
        p.wait_for_function('HZ.player.currentTime > 2.5', timeout=20000)
    except Exception:
        p.close()
        pytest.skip('audio could not be played here (offline or no audio support)')
    assert p.evaluate("document.querySelectorAll('#text .w.on').length") >= 1
    assert p.evaluate('HZ.state().playing')
    p.close()


def test_branded_english_page_without_credit_line():
    html = open(os.path.join(gc.ROOT, 'games', 'learn-surahs-by-heart', 'index.html'), encoding='utf-8').read()
    assert 'lang="en"' in html and 'bz-brand' in html and 'Rekić' not in html


def test_link_with_surah_id_opens_that_surah(browser):
    p = browser.new_page()
    p.goto('file://' + os.path.join(gc.ROOT, 'games', 'learn-surahs-by-heart', 'index.html') + '#fil')
    k = p.evaluate("DATA.surahs.findIndex(s => s.id === 'fil')")
    assert p.evaluate("sIdx") == k and p.input_value('#surah') == str(k)
    p.close()
