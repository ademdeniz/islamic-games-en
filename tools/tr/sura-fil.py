# sura-fil: Abdo ef. Rekić's recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('Sura El-Fil – Završna verzija', 'Surah Al-Fil'),
    ('Sura El-Fil', 'Surah Al-Fil'),
    ('سُورَةُ الْفِيلِ · Sura El-Fil', 'سُورَةُ الْفِيلِ · Surah Al-Fil'),
    ('sura_el_fil_offline.html', 'surah_al_fil.html'),
    ('sura_el_fil_podesavanje.json', 'surah_al_fil_timings.json'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('sura-fil', EXTRA)
