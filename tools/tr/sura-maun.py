# sura-maun: Abdo ef. Rekić's recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('Sura El-Maun – učenje', 'Surah Al-Ma’un'),
    ('سُورَةُ الْمَاعُونِ · El-Maun', 'سُورَةُ الْمَاعُونِ · Al-Ma’un'),
    ('sura_el_maun_offline.html', 'surah_al_maun.html'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('sura-maun', EXTRA)
