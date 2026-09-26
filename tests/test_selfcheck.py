"""Proves the checks in test_games.py catch real breakage: each test damages a known-good translation on purpose
and asserts the relevant check notices. If one of these fails, the game tests can't be trusted."""
import re
import subprocess
import tempfile

import gamecheck as gc
import skel
from test_games import browser  # noqa: F401  (shared Playwright fixture)

GAME = 'boziji-kitabi'  # small, known-good translation with quiz-style data


def good():
    return gc.strip_brand(gc.translated_html(GAME))


def skeleton_matches(html):
    a, _ = gc.skeleton(gc.original_minus_deletions(GAME))
    b, _ = gc.skeleton(html)
    return re.sub(r'lang=T', '', a) == re.sub(r'lang=T', '', b)


def test_known_good_translation_passes():
    assert skeleton_matches(good())


def test_detects_changed_code():
    assert not skeleton_matches(good().replace('N=10', 'N=12', 1))


def test_detects_dropped_quiz_entry():
    html = re.sub(r',\["ZABUR","[^"]*"\]', '', good(), count=1)
    assert html != good()
    assert not skeleton_matches(html)


def test_detects_changed_markup():
    assert not skeleton_matches(good().replace('<div class="q" id="q">', '<div class="q" id="question">', 1))


def test_detects_split_string():
    # "a"+x+"b" rewritten as one string (or vice versa) changes the code, even if the text looks right
    html = good().replace('"Total points: "', '"Total points: "+""', 1)
    assert not skeleton_matches(html)


def test_text_only_change_is_allowed():
    assert skeleton_matches(good().replace('Tap the first letter', 'Touch the first letter', 1))


def test_apostrophe_breaking_js_is_caught():
    html = good().replace('"✓ Correct! +10 points"', "'✓ That's correct! +10 points'", 1)
    body = max(re.findall(r'<script>(.*?)</script>', html, re.S), key=len)
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as f:
        f.write(body)
    assert subprocess.run(['node', '--check', f.name], capture_output=True).returncode != 0


def test_detects_leftover_bosnian():
    _, strings = gc.skeleton(good().replace('New game', 'Nova igra', 1))
    assert set(gc.visible_bosnian(strings, set())) >= {'Nova', 'igra'}


def test_ignores_bosnian_in_code_identifiers():
    _, strings = gc.skeleton('<script>var igra=1, bodovi=2; function nova(){}</script>')
    assert not gc.visible_bosnian(strings, set())


def test_transliteration_is_not_flagged():
    _, strings = gc.skeleton('<p>Thumma latus\'alunna yawma\'idhin \'anin-na\'im</p>')
    assert not gc.visible_bosnian(strings, set())


def test_detects_inconsistent_repeated_strings():
    orig = '<script>var o=["Tevrat","Zebur"],a="Tevrat";</script>'
    tr = '<script>var o=["Tawrat","Zabur"],a="Torah";</script>'
    _, a = gc.skeleton(orig)
    _, b = gc.skeleton(tr)
    pairs = {}
    for x, y in zip(a, b):
        pairs.setdefault(x, set()).add(y)
    assert pairs['Tevrat'] == {'Tawrat', 'Torah'}


def test_detects_arabic_script():
    _, strings = gc.skeleton('<p>قُلْ هُوَ ٱللَّهُ أَحَدٌ</p>')
    assert any(gc.ARABIC.search(s) for s in strings)


def test_media_placeholders_round_trip():
    html = '<img src="data:image/png;base64,QUJD"><p>Tekst</p>'
    blobs = []
    skel_html = skel.BLOB.sub(lambda m: blobs.append(m.group(0)) or '@@BLOB_0@@', html)
    assert skel_html == '<img src="@@BLOB_0@@"><p>Tekst</p>' and blobs == ['data:image/png;base64,QUJD']


def test_regex_literals_do_not_confuse_lexer():
    code, strings = gc.skeleton('<script>var r=/["\']/g, s="Zdravo";x=a/b/c;</script>')
    assert strings == ['Zdravo'] and 'x=a/b/c' in code


def test_browser_check_catches_runtime_error(browser, tmp_path):
    from test_games import _run_in_browser
    html = good().replace('e("r").onclick=start;', 'e("r").onclick=function(){missingFunction()};', 1)
    p = tmp_path / 'broken.html'
    p.write_text(html, encoding='utf-8')
    assert any('missingFunction' in e for e in _run_in_browser(browser, str(p)))
