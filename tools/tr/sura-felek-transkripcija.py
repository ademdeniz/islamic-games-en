# sura-felek-transkripcija: Abdo ef. Rekić's transliteration page. The Bosnian-style transliteration becomes English style (š→sh, dž→j,
# j→y, v→w, e→a, k→q for ق, h→kh for خ, z→dh for ذ, s→th for ث, g→gh for غ); the tajwid colour spans stay as they are.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page, word_pairs  # noqa: E402

GAME = 'sura-felek-transkripcija'
EXTRA = [
    ('Sura El-Felek', 'Surah Al-Falaq'),
    ('Sura El-Felek – transkripcija', 'Surah Al-Falaq – transliteration'),
    ('Bismilla + 5 ajeta • prema učenju i tedžvidu', 'Bismillah + 5 ayahs • as recited, with tajwid'),
    ('Kratko objašnjenje slova i oznaka:', 'What the letters and marks mean:'),
    ('crveno', 'red'),
    (' = oštro h i tvrda t/d/k/z/s', ' = sharp h and heavy t/d/q/z/s'),
    (' = hrapavo h', ' = rough h (kh)'),
    ('zeleno', 'green'),
    (' = meko s/z', ' = soft th/dh'),
    (' = ajn + vokal', ' = ʿayn + vowel'),
    ('¯ crno = obična dužina', '¯ black = normal long vowel'),
    ('~ crveno = neobična dužina', '~ red = extra-long vowel'),
    ('Kul', 'Qul'),
    ('euzu', 'a‘udhu'),
    ('l-felek', 'l-falaq'),
    ('šerri', 'sharri'),
    ('halek', 'khalaq'),
    ('ve min', 'wa min'),
    ('gasikin', 'ghasiqin'),
    ('iza', 'idha'),
    ('vekab', 'waqab'),
    ('n-neffasati', 'n-naffathati'),
    ('l-ukad', 'l-‘uqad'),
    ('hased', 'hasad'),
]
T = [
    ('<span class="roughh">h</span> = hrapavo h', '<span class="roughh">kh</span> = hrapavo h'),
]
WORDS = {
    'v0w0': '<span class="hard">Q</span>ul',
    'v0w1': 'a<span class="ayn">ʿ</span><span class="aynv">u</span><span class="madd">u</span><span class="soft">dh</span>u',
    'v0w3': 'l-fala<span class="hard">q</span>',
    'v1w3': '<span class="roughh">kh</span>ala<span class="hard">q</span>',
    'v2w2': 'gh<span class="madd">a</span>si<span class="hard">q</span>in',
    'v2w3': 'i<span class="soft">dh</span><span class="madd">a</span>',
    'v2w4': 'wa<span class="hard">q</span>ab',
    'v3w2': 'n-naff<span class="madd">a</span><span class="soft">th</span><span class="madd">a</span>ti',
    'v3w4': 'l-<span class="ayn">ʿ</span><span class="aynv">u</span><span class="hard">q</span>ad',
    'v4w3': 'i<span class="soft">dh</span><span class="madd">a</span>',
    'v4w4': '<span class="hard">h</span>asad',
}
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page(GAME, EXTRA)
ALLOW_ARABIC = ['only the ornate ayah-number brackets ﴿ ﴾ – the ayahs themselves are transliterated']
ALLOW = ['na', 'sa']   # pieces of transliterated words (naʿbudu, an-nasa), split by the tajwid colour spans
T = word_pairs(GAME, WORDS) + T
ALLOW_INCONSISTENT = ['h']   # rough h (خ) is written kh, sharp h (ح) stays h – each a one-letter colour span
