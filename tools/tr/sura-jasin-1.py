# sura-jasin-1: Abdo ef. Rekić's recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('سُورَةُ يسٓ · Ja-Sin – prvih 12 ajeta', 'سُورَةُ يسٓ · Ya-Sin – the first 12 ayahs'),
    ('Ja-Sin – prvih 12 ajeta, podešavanje', 'Ya-Sin – the first 12 ayahs'),
    ('ja_sin_12_ajeta_zavrsna_offline.html', 'ya_sin_12_ayahs.html'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('sura-jasin-1', EXTRA)
