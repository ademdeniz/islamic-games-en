"""Tests for the Sufara (Arabic letters) section."""
import json
import os
import re

import pytest

import gamecheck as gc

DATA = json.load(open(os.path.join(gc.ROOT, 'data', 'sufara', 'letters.json'), encoding='utf-8'))
LETTERS = DATA['letters']
WORDS = json.load(open(os.path.join(gc.ROOT, 'data', 'sufara', 'words.json'), encoding='utf-8'))
RULES = json.load(open(os.path.join(gc.ROOT, 'data', 'sufara', 'rules.json'), encoding='utf-8'))['rules']
RULE_EX = json.load(open(os.path.join(gc.ROOT, 'data', 'sufara', 'rule_examples.json'), encoding='utf-8'))
PAGES = sorted(d for d in os.listdir(os.path.join(gc.ROOT, 'sufara')) if os.path.isdir(os.path.join(gc.ROOT, 'sufara', d)))
MARKS = re.compile('[ً-ٰٟۖ-ۭـ]')


def bare(w):
    return MARKS.sub('', w).translate(str.maketrans('أإآٱ', 'اااا'))


# ---------------------------------------------------------------- data
def test_all_28_letters_once():
    chars = [L['ch'] for L in LETTERS]
    assert len(chars) == 28 and len(set(chars)) == 28
    assert set(chars) == set('ابتثجحخدذرزسشصضطظعغفقكلمنهوي')


@pytest.mark.parametrize('L', LETTERS, ids=[L['slug'] for L in LETTERS])
def test_letter_data(L):
    assert re.fullmatch(r'[\w-]{11}', L['video']), 'YouTube video id'
    assert len(L['harakat']) == 3 and all(L['ch'] in bare(a) or L['ch'] == 'ا' for a, _ in L['harakat'])
    assert L['ch'] not in L['similar'] and len(L['similar']) >= 3
    assert L['tip'] and L['name'] and L['bs']
    words = WORDS[L['slug']]
    assert len(words) >= 2, 'at least two Qur’an example words'
    for w in words:
        assert bare(L['ch']) in bare(w['ar']), f"{w['ar']} does not contain {L['ch']}"
        assert w['audio'].startswith('https://audio.qurancdn.com/') and w['en'] and w['tr']
        assert re.fullmatch(r'\d+:\d+', w['key'])


def test_every_video_is_a_different_letter_video():
    assert len({L['video'] for L in LETTERS}) == 28


def test_pages_exist():
    assert PAGES == sorted([f'{n:02d}-{L["slug"]}' for n, L in enumerate(LETTERS, 1)] + [f'review-{k}' for k in range(1, 5)]
                           + [f'rule-{R["slug"]}' for R in RULES])
    idx = open(os.path.join(gc.ROOT, 'sufara', 'index.html'), encoding='utf-8').read()
    assert all(f'"{p}"' in idx for p in PAGES)


def test_pages_are_english_and_branded():
    import skel
    for p in PAGES:
        html = open(os.path.join(gc.ROOT, 'sufara', p, 'index.html'), encoding='utf-8').read()
        assert '<div class="bz-brand"><img' in html and 'lang="en"' in html
        data = json.loads(re.search(r'const L=(\{.*?\});\n', html, re.S).group(1))
        visible = json.dumps({k: v for k, v in data.items() if k not in ('footer',)}, ensure_ascii=False)
        visible = re.sub(r'"(bs|slug|id|audio|video|key|ch|target)": "[^"]*"', '', visible)
        hits = {m.group(0) for m in skel.BS_WORDS.finditer(re.sub(r'[؀-ۿ]+', ' ', visible))}
        readings = {t for L in LETTERS for _, t in L['harakat']}   # “da”, “na”… are how دَ, نَ are read
        allowed = {x.lower() for x in readings | {L['bs'] for L in LETTERS} | {w for R in RULES for w in R['bs'].split()} | {'Spahić', 'Memic'}}   # + Bosnian letter names, real names
        assert not {h for h in hits if h.lower() not in allowed}, f'{p}: {hits}'


# ---------------------------------------------------------------- browser
@pytest.fixture
def page(browser):
    p = browser.new_page(viewport={'width': 430, 'height': 900})
    p.errors = []
    p.on('pageerror', lambda e: p.errors.append(str(e)))
    p.route(re.compile(r'^https?://'), lambda route: route.abort())
    yield p
    assert not p.errors, p.errors
    p.close()


def play(page, i, a):
    box = page.locator(f'#act{i}')
    if a['type'] == 'find':
        for k, c in enumerate(a['cells']):
            if c == a['target']:
                box.locator(f'.cell[data-k="{k}"]').click()
    elif a['type'] == 'quiz':
        by_q = {q['q']: q['answer'] for q in a['questions']}
        for _ in a['questions']:
            qtext = box.locator('.qn').inner_text().split('. ', 1)[1]
            box.locator(f'.opt[data-k="{by_q[qtext]}"]').click()
            page.wait_for_timeout(950)
    elif a['type'] == 'memory':
        cards = page.evaluate(f"[...document.querySelectorAll('#act{i} .mc')].map(b=>+b.dataset.k)")
        for k in range(len(a['pairs'])):
            for j in [j for j, x in enumerate(cards) if x == k]:
                box.locator(f'.mc[data-j="{j}"]').click()
    elif a['type'] == 'sort':
        for _ in a['items']:
            cur = box.locator('.sortq').inner_text().strip()
            b = next(it['bin'] for it in a['items'] if it['text'] == cur)
            box.locator(f'[data-b="{b}"]').click()
            page.wait_for_timeout(850)


@pytest.mark.parametrize('p', PAGES)
def test_every_page_can_be_completed(page, p):
    page.goto('file://' + os.path.join(gc.ROOT, 'sufara', p, 'index.html'))
    L = page.evaluate('LESSON.L')
    for i, a in enumerate(L['practice']):
        play(page, i, a)
        page.wait_for_function(f"document.getElementById('act{i}').classList.contains('done')", timeout=5000)
    assert 'Lesson complete' in page.inner_text('#stars')


def test_letter_page_shows_forms_words_and_video(page):
    page.goto('file://' + os.path.join(gc.ROOT, 'sufara', '06-ba', 'index.html'))
    assert page.inner_text('.letter .big') == 'ب'
    assert page.eval_on_selector_all('.forms .f', 'e => e.map(x => x.textContent)') == ['ب', 'بـ', 'ـبـ', 'ـب']
    assert page.locator('.word').count() == len(WORDS['ba'])
    href = page.get_attribute('a.video', 'href')
    assert href == 'https://www.youtube.com/watch?v=JgSH2C3BUL4'


def test_non_joining_letter_says_so(page):
    page.goto('file://' + os.path.join(gc.ROOT, 'sufara', '02-dal', 'index.html'))
    assert 'never joins' in page.inner_text('.letter')


def test_wrong_letter_in_find_game_is_not_counted(page):
    page.goto('file://' + os.path.join(gc.ROOT, 'sufara', '06-ba', 'index.html'))
    L = page.evaluate('LESSON.L')
    a = L['practice'][0]
    k = next(k for k, c in enumerate(a['cells']) if c != a['target'])
    page.locator(f'#act0 .cell[data-k="{k}"]').click()
    assert 'different letter' in page.inner_text('#act0 .fb')
    assert 'done' not in page.get_attribute('#act0', 'class')


def test_sufara_index_links_every_page_in_order(page):
    page.goto('file://' + os.path.join(gc.ROOT, 'sufara', 'index.html'))
    hrefs = page.eval_on_selector_all('#grid a', 'as => as.map(a => a.getAttribute("href"))')
    assert len(hrefs) == 28 + 4 + len(RULES) and hrefs[0] == '01-alif/' and hrefs[-1] == 'review-4/'
    for R in RULES:   # every rule comes right after its letter (or after the rules placed there before it)
        slug = next(f'{n:02d}-{L["slug"]}/' for n, L in enumerate(LETTERS, 1) if L['slug'] == R['after'])
        between = hrefs[hrefs.index(slug) + 1:hrefs.index(f'rule-{R["slug"]}/')]
        assert all(h.startswith('rule-') for h in between), (R['slug'], between)


def test_word_recitation_plays(browser):
    p = browser.new_page()
    p.goto('file://' + os.path.join(gc.ROOT, 'sufara', '06-ba', 'index.html'))
    p.click('.word >> nth=0')
    try:
        p.wait_for_function('document.querySelector(".word.playing") && window.audio === undefined', timeout=2000)
    except Exception:
        pass
    ok = p.evaluate("new Promise(r=>{const a=new Audio(document.querySelector('.word').dataset.audio);a.oncanplay=()=>r(true);a.onerror=()=>r(false);setTimeout(()=>r(null),15000)})")
    p.close()
    if ok is None:
        pytest.skip('audio could not be checked here (offline?)')
    assert ok, 'Quran.com word audio must load'


@pytest.mark.parametrize('R', RULES, ids=[R['slug'] for R in RULES])
def test_rule_data(R):
    assert R['after'] in {L['slug'] for L in LETTERS}
    assert re.fullmatch(r'[\w-]{11}', R['video']) and R['explain'] and R['quiz']
    ex = RULE_EX[R['slug']]
    assert len(ex) == len(R['examples']) >= 2
    for e, spec in zip(ex, R['examples']):
        assert len(e['ar'].split()) == len(spec['words'])
        if len(spec['words']) > 1:
            assert e['audio'].startswith('https://verses.quran.com/') and 0 <= e['clip'][0] < e['clip'][1], e
        else:
            assert e['audio'].startswith('https://audio.qurancdn.com/') and 'clip' not in e
    for q in R['quiz']:
        assert 0 <= q['answer'] < len(q['options'])


def test_start_over_clears_stars_on_this_device(page):
    page.on('dialog', lambda d: d.accept())
    page.goto('file://' + os.path.join(gc.ROOT, 'sufara', 'index.html'))
    page.evaluate("localStorage.setItem('lesson-sufara-06-ba', JSON.stringify({0: 1, 1: 1}))")
    page.reload()
    assert page.locator('a.t.done').count() == 1
    page.click('#reset')
    page.wait_for_load_state()
    assert page.locator('a.t.done').count() == 0
    assert page.evaluate("Object.keys(localStorage).filter(k => k.startsWith('lesson-sufara-')).length") == 0


def test_two_word_example_plays_only_those_words(browser):
    """Joining words: the clip starts at the first word and stops after the second (real recitation)."""
    p = browser.new_page()
    p.goto('file://' + os.path.join(gc.ROOT, 'sufara', 'rule-joining-words', 'index.html'))
    clip = RULE_EX['joining-words'][0]['clip']
    p.click('.word >> nth=0')
    try:
        p.wait_for_function('audio && audio.currentTime > 0.3', timeout=15000)
    except Exception:
        p.close()
        pytest.skip('audio could not be played here (offline?)')
    started = p.evaluate('audio.currentTime')
    p.wait_for_timeout((clip[1] - clip[0]) + 1500)
    state = p.evaluate('[audio.paused, audio.currentTime]')
    p.close()
    assert started >= clip[0] / 1000 - 0.1
    assert state[0] and state[1] <= clip[1] / 1000 + 0.35, f'should stop at {clip[1]} ms, is at {state}'


def test_play_again_restarts_a_finished_activity_and_keeps_the_stars(page):
    page.goto('file://' + os.path.join(gc.ROOT, 'sufara', '06-ba', 'index.html'))
    L = page.evaluate('LESSON.L')
    a = L['practice'][0]                                    # the "find the letter" game
    assert page.is_hidden('#act0 .again'), 'no Play again before the activity is done'
    play(page, 0, a)
    page.wait_for_function("document.getElementById('act0').classList.contains('done')")
    assert page.locator('#act0 .cell.ok').count() == a['cells'].count(a['target'])
    page.click('#act0 .again')
    assert page.locator('#act0 .cell.ok').count() == 0, 'the game starts fresh'
    assert 'done' in page.get_attribute('#act0', 'class') and '⭐' in page.inner_text('#stars'), 'stars are kept'
    play(page, 0, a)                                        # and it can be played to the end again
    assert page.locator('#act0 .cell.ok').count() == a['cells'].count(a['target'])
    page.reload()
    assert page.is_visible('#act0 .again'), 'Play again is offered for activities finished earlier'


def _ink(png):
    import io
    from PIL import Image
    im = Image.open(io.BytesIO(png)).convert('L')
    w, h = im.size
    px = im.load()
    bg = px[1, 1]
    pts = [(x, y) for y in range(h) for x in range(w) if abs(px[x, y] - bg) > 90]
    if not pts:
        return None, w, h
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys)), w, h


@pytest.mark.parametrize('p', ['', '21-jim/', '15-mim/', '27-ayn/', '01-alif/', 'rule-tanwin/', 'rule-long-u/'])
def test_arabic_letters_are_centred_in_their_boxes(page, p):
    """Every big letter, tile, letter form, vowel card and find-the-letter cell: the drawn shape is centred in its box
    and stays inside it (the font sits letters on a baseline, so tails like ج ع م used to spill out)."""
    page.goto('file://' + os.path.join(gc.ROOT, 'sufara', p, 'index.html'))
    page.evaluate('document.fonts.ready')
    page.wait_for_timeout(200)
    els = page.locator('.glyph')
    checked = 0
    for i in range(els.count()):
        e = els.nth(i)
        if not e.is_visible():
            continue
        e.scroll_into_view_if_needed()
        box = e.bounding_box()
        if e.evaluate("e => getComputedStyle(e).display === 'block' && !e.classList.contains('big') && getComputedStyle(e.parentElement).display !== 'grid'"):   # tiles, forms, vowel cards fill their card
            parent = e.evaluate("e => {const r = e.parentElement.getBoundingClientRect(), s = getComputedStyle(e.parentElement);"
                                "return r.width - parseFloat(s.paddingLeft) - parseFloat(s.paddingRight) - parseFloat(s.borderLeftWidth) - parseFloat(s.borderRightWidth)}")
            assert box['width'] >= parent - 2, f'{p}: glyph {i} does not fill its card ({box["width"]} < {parent})'
        ink, w, h = _ink(page.screenshot(clip={'x': box['x'] + 2, 'y': box['y'] + 2, 'width': box['width'] - 4, 'height': box['height'] - 4}))
        assert ink, f'{p}: glyph {i} is empty'
        dx, dy = (ink[0] + ink[2]) / 2 - w / 2, (ink[1] + ink[3]) / 2 - h / 2
        assert abs(dx) <= 4 and abs(dy) <= 4, f'{p}: glyph {i} {e.inner_text()!r} is off centre by ({dx}, {dy})'
        assert ink[0] > 0 and ink[1] > 0 and ink[2] < w - 1 and ink[3] < h - 1, f'{p}: glyph {i} {e.inner_text()!r} spills out of its box'
        checked += 1
    assert checked >= (1 if p.startswith('rule') else 6)
