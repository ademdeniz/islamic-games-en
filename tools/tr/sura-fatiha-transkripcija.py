# sura-fatiha-transkripcija: Abdo ef. Rekić's transliteration page. The Bosnian-style transliteration becomes English style (š→sh, dž→j,
# j→y, v→w, e→a, k→q for ق, h→kh for خ, z→dh for ذ, s→th for ث, g→gh for غ); the tajwid colour spans stay as they are.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page, word_pairs  # noqa: E402

GAME = 'sura-fatiha-transkripcija'
EXTRA = [
    ('Sura El-Fatiha', 'Surah Al-Fatiha'),
    ('Sura El-Fatiha – transkripcija', 'Surah Al-Fatiha – transliteration'),
    ('Bismilla + 7 ajeta • prema učenju i tedžvidu', 'Bismillah + 7 ayahs • as recited, with tajwid'),
]
T = [
    ('<span class="hard">crveno</span> = oštro h i tvrda t/d/k/z/s • <span class="soft">zeleno</span> = meko s/z • <span class="ayn">ʿ</span><span class="aynv">a/i/u</span> = ajn + vokal • crna ravna crta = obična dužina • crvena valovita = posebna dužina', '<span class="hard">red</span> = sharp h and heavy t/d/q/z/s • <span class="soft">green</span> = soft th/dh • <span class="ayn">ʿ</span><span class="aynv">a/i/u</span> = ʿayn + vowel • straight black line = normal long vowel • red wavy line = extra-long vowel'),
]
WORDS = {
    'v1w0': "Al-<span class='hard'>h</span>amdu",
    'v1w3': "l-<span class='ayn'>ʿ</span><span class='aynv'>a</span><span class='madd'>a</span>lam<span class='madd'>i</span>n",
    'v2w0': "Ar-Ra<span class='hard'>h</span>m<span class='madd'>a</span>ni",
    'v3w1': 'yawmi',
    'v4w0': "Iyy<span class='madd'>a</span>ka",
    'v4w2': "wa iyy<span class='madd'>a</span>ka",
    'v4w3': "nasta<span class='ayn'>ʿ</span><span class='aynv'>i</span>n",
    'v5w0': 'Ihdina-s',
    'v5w2': 'mustaq<span class="madd">i</span>m',
    'v6w1': "la<span class='soft'>dh</span><span class='madd'>i</span>na",
    'v6w2': "an<span class='ayn'>ʿ</span><span class='aynv'>a</span>mta",
    'v6w3': "<span class='ayn'>ʿ</span><span class='aynv'>a</span>layhim",
    'v6w4': 'ghayril',
    'v6w5': "magh<span class='hard'>d</span><span class='madd'>u</span>bi",
    'v6w6': "<span class='ayn'>ʿ</span><span class='aynv'>a</span>layhim",
    'v6w7': "wa la<span class='hard'>d</span><span class='hard'>d</span><span class='maddx'>a</span>llin",
}
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page(GAME, EXTRA)
ALLOW_ARABIC = ['only the ornate ayah-number brackets ﴿ ﴾ – the ayahs themselves are transliterated']
ALLOW = ['na', 'sa']   # pieces of transliterated words (naʿbudu, an-nasa), split by the tajwid colour spans
T = word_pairs(GAME, WORDS) + T
