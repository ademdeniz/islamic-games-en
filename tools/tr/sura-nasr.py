# sura-nasr: Abdo ef. Rekić's recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('Sura En-Nasr', 'Surah An-Nasr'),
    ('Sura_En_Nasr.html', 'Surah_An_Nasr.html'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('sura-nasr', EXTRA)
