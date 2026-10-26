# sura-kurejs: Abdo ef. Rekić's recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('Sura Kurejš – Završna verzija', 'Surah Quraysh'),
    ('سُورَةُ قُرَيْشٍ · Sura Kurejš', 'سُورَةُ قُرَيْشٍ · Surah Quraysh'),
    ('sura_kurejs_offline.html', 'surah_quraysh.html'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('sura-kurejs', EXTRA)
