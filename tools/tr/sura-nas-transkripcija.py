# sura-nas-transkripcija: Abdo ef. Rekić's transliteration page. The Bosnian-style transliteration becomes English style (š→sh, dž→j,
# j→y, v→w, e→a, k→q for ق, h→kh for خ, z→dh for ذ, s→th for ث, g→gh for غ); the tajwid colour spans stay as they are.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page, word_pairs  # noqa: E402

GAME = 'sura-nas-transkripcija'
EXTRA = [
    ('Sura En-Nas – transkripcija', 'Surah An-Nas – transliteration'),
    ('6 ajeta • transkripcija s tedžvidskim bojama • riječ po riječ', '6 ayahs • transliteration with tajwid colours • word by word'),
    ('Crveno = tvrdi glasovi i oštro h • zeleno = meki s/z • plavo = vokal uz ajn • crna crta = dužina', 'Red = heavy sounds and sharp h • green = soft th/dh • blue = the vowel with ʿayn • black line = long vowel'),
]
T = [
]
WORDS = {
    'v0w0': 'Qul',
    'v0w1': 'a<span class="ayn">ʿ</span><span class="aynv">ū</span>dhu',
    'v1w0': 'Maliki',
    'v3w1': 'sharri',
    'v3w2': 'l-wasw<span class="madd">ā</span>si',
    'v3w3': 'l-<span class="hard">kh</span>ann<span class="madd">ā</span>s',
    'v4w0': 'Alla<span class="soft">dh</span><span class="madd">ī</span>',
    'v4w1': 'yuwaswisu',
    'v5w0': 'Mina',
    'v5w1': 'l-jinnati',
    'v5w2': 'wa-n-n<span class="madd">ā</span>s',
}
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page(GAME, EXTRA)
ALLOW_ARABIC = ['only the ornate ayah-number brackets ﴿ ﴾ – the ayahs themselves are transliterated']
ALLOW = ['na', 'sa']   # pieces of transliterated words (naʿbudu, an-nasa), split by the tajwid colour spans
T = word_pairs(GAME, WORDS) + T
