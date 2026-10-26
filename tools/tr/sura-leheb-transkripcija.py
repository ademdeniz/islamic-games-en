# sura-leheb-transkripcija: Abdo ef. Rekić's transliteration page. The Bosnian-style transliteration becomes English style (š→sh, dž→j,
# j→y, v→w, e→a, k→q for ق, h→kh for خ, z→dh for ذ, s→th for ث, g→gh for غ); the tajwid colour spans stay as they are.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page, word_pairs  # noqa: E402

GAME = 'sura-leheb-transkripcija'
EXTRA = [
    ('SURA EL-MESED', 'SURAH AL-MASAD (AL-LAHAB)'),
    ('Sura El-Mesed', 'Surah Al-Masad (Al-Lahab)'),
    ('Crno: obično h i dugo ', 'Black: normal h and long '),
    ('Zeleno: meko z i meko s', 'Green: soft dh and soft th'),
    ('Crveno: oštro h, ʿajn i tvrdo t, d, k, z, s', 'Red: sharp h, ʿayn and heavy t, d, q, z, s'),
    ('ḣ = hrapavo h (tačka iznad)', 'kh = rough h'),
]
T = [
]
WORDS = {
    'v0w0': 'Tabbat',
    'v0w1': 'yad<span class="long-mark">a<span class="red-macron">¯</span></span>',
    'v0w2': 'ab<span class="long-mark">i<span class="red-macron">¯</span></span>',
    'v0w3': 'lahabi-w',
    'v0w4': 'wa tabb',
    'v1w1': 'aghn<span class="long-mark">a<span class="red-macron">¯</span></span>',
    'v1w4': 'wa m<span class="long-mark">a<span class="red-macron">¯</span></span>',
    'v1w5': 'kasab',
    'v2w0': 'Saya<span class="hard-letter">s</span>l<span class="long-mark">a<span class="red-macron">¯</span></span>',
    'v2w1': 'n<span class="long-mark">a<span class="red-macron">¯</span></span>ran',
    'v2w2': '<span class="soft-letter">dh</span><span class="long-mark">a<span class="red-macron">¯</span></span>ta',
    'v2w3': 'lahab',
    'v3w0': 'Wamra’atuhū',
    'v3w1': '<span class="hard-letter">h</span>amm<span class="long-mark">a<span class="red-macron">¯</span></span>latal',
    'v4w1': 'j<span class="long-mark">i<span class="red-macron">¯</span></span>dih<span class="long-mark">a<span class="red-macron">¯</span></span>',
    'v4w4': 'masad',
}
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page(GAME, EXTRA)
ALLOW_ARABIC = ['only the ornate ayah-number brackets ﴿ ﴾ – the ayahs themselves are transliterated']
ALLOW = ['na', 'sa']   # pieces of transliterated words (naʿbudu, an-nasa), split by the tajwid colour spans
T = word_pairs(GAME, WORDS) + T
