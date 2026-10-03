"""The shared Ilmihal question bank and the games for two or more players built on it.

Each game is played for real in a browser: start it, answer the question on screen correctly and check the score
goes up – so the English questions, their answers and the right-answer index still line up."""
import collections
import json
import os
import re
import sys

import pytest

import gamecheck as gc

sys.path.insert(0, os.path.join(gc.ROOT, 'tools'))
sys.path.insert(0, os.path.join(gc.ROOT, 'tools', 'tr'))
import _ilmihal_bank  # noqa: E402
import skel  # noqa: E402

BANK = _ilmihal_bank.ENTRIES
RIGHT = collections.defaultdict(set)   # English question -> its right answer(s)
for _e in BANK:
    RIGHT[_e['en']['q']].add(_e['en']['a'][_e['c']])


# ---------------------------------------------------------------- the bank
def test_bank_is_complete_and_english():
    assert len(BANK) == 1568
    assert collections.Counter(e['l'] for e in BANK) == {'A1': 163, 'A2': 233, 'A3': 321, 'B1': 451, 'B2': 308, 'B3': 92}
    for e in BANK:
        assert 0 <= e['c'] < 4 and len(e['en']['a']) == len(set(e['en']['a'])) == 4, e['en']
        text = ' '.join([e['en']['q']] + e['en']['a'])
        assert not re.search('[čćšžđČĆŠŽĐ]', text) and not skel.BS_WORDS.search(text), text
        assert '✅' not in text, 'no answer may give itself away'


def test_same_bosnian_text_has_one_english_text():
    seen = collections.defaultdict(set)
    for e in BANK:
        seen[e['bs']['q']].add(e['en']['q'])
        for b, en in zip(e['bs']['a'], e['en']['a']):
            seen[b].add(en)
    assert not {k: v for k, v in seen.items() if len(v) > 1}


# ---------------------------------------------------------------- the games, played
GAMES = {   # game: (start, question, answers, check after one right answer)
    'mektebski-fudbal': ('#start', '#question', '#answers button', ('#s1', '1')),
    'mektebsko-povlacenje-konopa': ('#begin', '#question', '#answers button', ('#s1', 'Player 1: 1')),
    'mektebski-milioner': ('#start', '#question', '#answers button', ('#score0', '100')),
    'mektebski-turnir': ('#start', '#question', '#answers button', ('#result', 'Correct')),
    'mektebsko-kolo-srece': ('#spin', '#question', '#answers button', ('#score0', '10')),
    'mektebski-covjece-ne-ljuti-se': ('#start', '#question', '#answers button', ('#notice', 'Correct')),
}


@pytest.fixture
def page(browser):
    p = browser.new_page(viewport={'width': 390, 'height': 900})
    p.errors = []
    p.on('pageerror', lambda e: p.errors.append(str(e)))
    p.route(re.compile(r'^https?://'), lambda route: route.abort())
    yield p
    assert not p.errors, p.errors
    p.close()


@pytest.mark.parametrize('name', GAMES)
def test_game_plays_in_english_and_counts_right_answers(page, name):
    game = name
    start, question, answers, (where, expect) = GAMES[game]
    page.goto('file://' + os.path.join(gc.ROOT, 'games', game, 'index.html'))
    page.click(start)
    if game == 'mektebski-covjece-ne-ljuti-se':
        page.click('#roll')
    page.wait_for_function(f"document.querySelectorAll('{answers}').length === 4", timeout=8000)
    q = page.inner_text(question).strip()
    assert q in RIGHT, f'question on screen is not an English bank question: {q!r}'
    texts = [re.sub(r'^[A-D]\) ', '', t.strip()) for t in page.eval_on_selector_all(answers, 'bs => bs.map(b => b.textContent)')]
    right = [i for i, t in enumerate(texts) if t in RIGHT[q]]
    assert len(right) == 1, (q, texts)
    page.locator(answers).nth(right[0]).click()
    page.wait_for_function(f"document.querySelector('{where}').textContent.includes({json.dumps(expect)})", timeout=4000)
    body = page.inner_text('body')
    assert not skel.BS_WORDS.search(body), skel.BS_WORDS.search(body).group(0)


def test_home_page_lists_every_game(page):
    page.goto('file://' + os.path.join(gc.ROOT, 'index.html'))
    hrefs = set(page.eval_on_selector_all('#list a', 'as => as.map(a => a.getAttribute("href"))'))
    built = {f'games/{g}/' for g in os.listdir(os.path.join(gc.ROOT, 'games'))
             if os.path.exists(os.path.join(gc.ROOT, 'games', g, 'index.html'))}
    missing = built - hrefs - {'games/maca-pripreme-za-namaz/', 'games/zagonetna-zivotinja-80/', 'games/el-fatiha/'}
    assert not missing, f'games not on the home page: {sorted(missing)}'
    assert {f'games/{g}/' for g in GAMES} <= hrefs
