"""Tests for translated games.  Run:  .venv/bin/pytest tests            (all built games)
                                     .venv/bin/pytest tests --game kviz-namaz
"""
import base64
import hashlib
import os
import re
import subprocess
import tempfile

import pytest

import gamecheck as gc
from conftest import all_games, built_games

CREDIT = re.compile(r'Rekić|Pripremio|Pripremila|Prepared by', re.I)


def test_every_game_is_translated(request):
    if request.config.getoption('game'):
        pytest.skip('checking selected games only')
    missing = [g for g in all_games() if g not in built_games()]
    assert not missing, f'{len(missing)} games not translated yet: {missing}'


def test_is_english_and_branded(game):
    html = gc.translated_html(game)
    assert re.search(r'<html[^>]*lang="en"', html, re.I), 'missing <html lang="en">'
    assert html.count('bz-brand') >= 1 or 'class="brand"' in html, 'community logo header missing'


def test_no_author_credit(game):
    text = gc.BLOB.sub('', gc.translated_html(game))
    m = CREDIT.search(text)
    assert not m, f'author credit still present: …{text[max(0, m.start() - 60):m.end() + 30]}…'


def test_no_bosnian_left(game):
    _, strings = gc.skeleton(gc.translated_html(game))
    hits = gc.visible_bosnian(strings, gc.allow(game, 'ALLOW'))
    assert not hits, 'untranslated Bosnian in visible text (add deliberate terms to ALLOW):\n' + \
        '\n'.join(f'  {w!r}: …{ctx}…' for w, ctx in hits.items())


def test_no_arabic_script(game):
    if gc.allow(game, 'ALLOW_ARABIC'):
        pytest.skip('game deliberately keeps Arabic script: ' + ', '.join(gc.allow(game, 'ALLOW_ARABIC')))
    _, strings = gc.skeleton(gc.translated_html(game))
    bad = [s[:80] for s in strings if gc.ARABIC.search(gc.BLOB.sub('', s))]
    assert not bad, f'Arabic script left (use transliteration + italic English): {bad[:5]}'


def test_media_preserved(game):
    def blobs(h):
        return {hashlib.md5(b.encode()).hexdigest() for b in gc.BLOB.findall(h)}
    orig = gc.BLOB.findall(gc.original_html(game))
    replaced = {i for i in range(len(orig)) if gc.skel.fixed_image(game, i)}
    expected = {hashlib.md5(b.encode()).hexdigest() for i, b in enumerate(orig) if i not in replaced}
    missing = expected - blobs(gc.translated_html(game))
    assert not missing, f'{len(missing)} embedded images/sounds from the original are missing or altered'
    html = gc.translated_html(game)
    for i in replaced:  # pictures we deliberately replaced with an English version must really be in the game
        fixed = base64.b64encode(open(gc.skel.fixed_image(game, i), 'rb').read()).decode()
        assert fixed in html, f'English version of picture {i} is not in the game'


def test_code_unchanged(game):
    """Only text may change: the masked skeletons of original and translation must be identical."""
    reason = gc.structural_reason(game)
    if reason:
        pytest.skip('deliberate structural change: ' + reason)
    a, _ = gc.skeleton(gc.original_minus_deletions(game))
    b, _ = gc.skeleton(gc.strip_brand(gc.translated_html(game)))
    a = re.sub(r'lang=T', '', a)
    b = re.sub(r'lang=T', '', b)
    if a != b:
        i = next(k for k in range(min(len(a), len(b))) if a[k] != b[k]) if a[:min(len(a), len(b))] != b[:min(len(a), len(b))] else min(len(a), len(b))
        pytest.fail('code/structure changed, not just text. First difference:\n'
                    f'  original:    …{a[max(0, i - 120):i + 120]}…\n'
                    f'  translation: …{b[max(0, i - 120):i + 120]}…')


def test_repeated_strings_translated_consistently(game):
    """If the same Bosnian string appears several times (e.g. an answer and the matching option), every copy must
    get the same English text, otherwise equality checks in the game logic break."""
    if gc.structural_reason(game):
        pytest.skip('structural change: strings do not line up')
    _, a = gc.skeleton(gc.original_minus_deletions(game))
    _, b = gc.skeleton(gc.strip_brand(gc.translated_html(game)))
    if len(a) != len(b):
        pytest.skip('string count differs (reported by test_code_unchanged)')
    seen, bad = {}, {}
    ok = gc.allow(game, 'ALLOW_INCONSISTENT')
    for x, y in zip(a, b):
        if x.strip() and x not in ok:
            seen.setdefault(x, set()).add(y)
    for x, ys in seen.items():
        if len(ys) > 1:
            bad[x] = ys
    assert not bad, 'same Bosnian string translated differently (list in ALLOW_INCONSISTENT if intended):\n' + \
        '\n'.join(f'  {x[:60]!r} -> {sorted(ys)}' for x, ys in list(bad.items())[:10])


def test_javascript_syntax(game):
    html = gc.translated_html(game)
    for k, m in enumerate(re.finditer(r'<script\b([^>]*)>(.*?)</script>', html, re.S | re.I)):
        attrs, body = m.group(1), m.group(2)
        if 'src=' in attrs or re.search(r'json|template', attrs, re.I) or not body.strip():
            continue
        ext = '.mjs' if 'module' in attrs else '.js'
        with tempfile.NamedTemporaryFile('w', suffix=ext, delete=False, encoding='utf-8') as f:
            f.write(body)
        r = subprocess.run(['node', '--check', f.name], capture_output=True, text=True)
        os.unlink(f.name)
        assert r.returncode == 0, f'script #{k} has a syntax error:\n{r.stderr[-1500:]}'


def _run_in_browser(browser, path):
    """Load a page, click through visible buttons, return the set of JS errors."""
    errors = []
    page = browser.new_page()
    page.on('pageerror', lambda e: errors.append(str(e).split('\n')[0]))
    page.on('dialog', lambda d: d.dismiss())
    page.route(re.compile(r'^https?://'), lambda route: route.abort())  # offline: no audio/fonts needed
    try:
        page.goto('file://' + path, timeout=20000)
        page.wait_for_timeout(500)
        for _ in range(12):
            try:  # the game may replace its buttons while we look at them; just look again
                buttons = [b for b in page.query_selector_all('button, [onclick]') if b.is_visible() and b.is_enabled()]
            except Exception:
                page.wait_for_timeout(250)
                continue
            if not buttons:
                break
            try:
                buttons[_ % len(buttons)].click(timeout=2000, no_wait_after=True)
            except Exception:
                pass
            page.wait_for_timeout(250)
    except Exception as e:  # a hang (e.g. word longer than the grid) shows up here as a timeout
        errors.append(f'page did not load/respond: {str(e).splitlines()[0]}')
    finally:
        page.close()
    return {re.sub(r'\d+', 'N', e) for e in errors}


def test_runs_without_new_errors(game, browser):
    """Load the game and click around; it must not raise JS errors that the original doesn't also raise."""
    new = _run_in_browser(browser, os.path.join(gc.ROOT, 'games', game, 'index.html'))
    if new:
        old = _run_in_browser(browser, gc.skel.main_file(game))
        new -= old
    assert not new, f'JavaScript errors in the translated game: {sorted(new)}'


def test_online_quiz_uses_our_own_database(game):
    if game != 'islamski-milijunas-online':
        pytest.skip('only the online quiz talks to a database')
    import json
    cfg = json.load(open(os.path.join(gc.ROOT, 'supabase', 'config.json')))
    html = gc.translated_html(game)
    assert 'jaxcricubwcvqudhknjj' not in html and 'sb_publishable_2gMnx' not in html, "original author's database still referenced"
    assert f"SUPABASE_URL='{cfg['url']}'" in html and f"SUPABASE_KEY='{cfg['publishable_key']}'" in html
    assert 'sb_secret_' not in html, 'a SECRET key must never be in a web page'
