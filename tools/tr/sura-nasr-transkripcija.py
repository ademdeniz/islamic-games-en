# sura-nasr-transkripcija: Abdo ef. Rekić's transliteration page. The Bosnian-style transliteration becomes English style (š→sh, dž→j,
# j→y, v→w, e→a, k→q for ق, h→kh for خ, z→dh for ذ, s→th for ث, g→gh for غ); the tajwid colour spans stay as they are.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page, word_pairs  # noqa: E402

GAME = 'sura-nasr-transkripcija'
EXTRA = [
    ('Sura En-Nasr', 'Surah An-Nasr'),
    ('Sura En-Nasr – transkripcija', 'Surah An-Nasr – transliteration'),
    ('Bismilla + 3 ajeta • prema učenju i tedžvidu', 'Bismillah + 3 ayahs • as recited, with tajwid'),
    ('Kratko objašnjenje oznaka:', 'What the marks mean:'),
    ('crveno', 'red'),
    (' = oštro h i tvrda slova', ' = sharp h and heavy letters'),
    ('zeleno', 'green'),
    (' = meko s/z', ' = soft th/dh'),
    (' = ajn + vokal', ' = ʿayn + vowel'),
    ('¯ crno = obična dužina', '¯ black = normal long vowel'),
    ('~ crveno = posebna dužina', '~ red = extra-long vowel'),
]
T = [
]
WORDS = {
    'v0w0': 'I<span class="soft">dh</span><span class="madd">a</span>',
    'v0w1': 'j<span class="madd">a</span>a',
    'v0w4': 'wal-fat<span class="hard">h</span>',
    'v1w0': 'wa ra’aytan-n<span class="madd">a</span>sa',
    'v1w2': 'yad<span class="roughh">kh</span>ul<span class="madd">u</span>na',
    'v1w6': 'afw<span class="madd">a</span>j<span class="madd">a</span>',
    'v2w0': 'fa sabbi<span class="hard">h</span>',
    'v2w2': 'rabbika',
    'v2w3': 'wastaghfirhu',
    'v2w4': 'innah<span class="madd">u</span>',
    'v2w5': 'k<span class="madd">a</span>na',
    'v2w6': 'taww<span class="madd">a</span>b<span class="madd">a</span>',
}
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page(GAME, EXTRA)
ALLOW_ARABIC = ['only the ornate ayah-number brackets ﴿ ﴾ – the ayahs themselves are transliterated']
ALLOW = ['na', 'sa']   # pieces of transliterated words (naʿbudu, an-nasa), split by the tajwid colour spans
T = word_pairs(GAME, WORDS) + T
ALLOW_INCONSISTENT = ['h']   # rough h (خ) is written kh, sharp h (ح) stays h – each a one-letter colour span
