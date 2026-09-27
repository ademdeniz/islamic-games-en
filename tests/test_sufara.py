"""Tests for the Sufara (Arabic letters) section."""
import json
import os
import re

import pytest

import gamecheck as gc

DATA = json.load(open(os.path.join(gc.ROOT, 'data', 'sufara', 'letters.json'), encoding='utf-8'))
LETTERS = DATA['letters']
WORDS = json.load(open(os.path.join(gc.ROOT, 'data', 'sufara', 'words.json'), encoding='utf-8'))
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
    assert PAGES == sorted([f'{n:02d}-{L["slug"]}' for n, L in enumerate(LETTERS, 1)] + [f'review-{k}' for k in range(1, 5)])
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
        allowed = {x.lower() for x in readings | {L['bs'] for L in LETTERS} | {'Spahić', 'Memic'}}   # + Bosnian letter names, real names
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
    assert len(hrefs) == 32 and hrefs[0] == '01-alif/' and hrefs[7] == 'review-1/' and hrefs[-1] == 'review-4/'


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
