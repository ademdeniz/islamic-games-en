# sura-ihlas-transkripcija: Abdo ef. Rekić's transliteration page. The Bosnian-style transliteration becomes English style (š→sh, dž→j,
# j→y, v→w, e→a, k→q for ق, h→kh for خ, z→dh for ذ, s→th for ث, g→gh for غ); the tajwid colour spans stay as they are.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page, word_pairs  # noqa: E402

GAME = 'sura-ihlas-transkripcija'
EXTRA = [
    ('Sura El-Ihlas', 'Surah Al-Ikhlas'),
    ('Bismilla + 4 ajeta • transkripcija riječ po riječ', 'Bismillah + 4 ayahs • transliteration word by word'),
]
T = [
]
WORDS = {
    'v0w0': '<span class="hard-letter">Q</span>ul',
    'v0w1': 'huwall<span class="madd-normal">a<span class="madd-line">¯</span></span>hu',
    'v0w3': 'a<span class="hard-letter">h</span>ad',
    'v1w1': '<span class="hard-letter">s</span>amad',
    'v2w0': 'lam',
    'v2w1': 'yalid',
    'v2w2': 'wa lam',
    'v2w3': 'y<span class="madd-normal">u<span class="madd-line">¯</span></span>lad',
    'v3w0': 'wa lam',
    'v3w1': 'yakul-lah<span class="madd-normal">u<span class="madd-line">¯</span></span>',
    'v3w3': 'kufuwan',
    'v3w4': 'a<span class="hard-letter">h</span>ad',
}
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page(GAME, EXTRA)
ALLOW_ARABIC = ['only the ornate ayah-number brackets ﴿ ﴾ – the ayahs themselves are transliterated']
ALLOW = ['na', 'sa']   # pieces of transliterated words (naʿbudu, an-nasa), split by the tajwid colour spans
T = word_pairs(GAME, WORDS) + T
