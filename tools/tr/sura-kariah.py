# sura-kariah: Abdo ef. Rekić's recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('Sura El-Karia – Završna verzija', 'Surah Al-Qari‘ah'),
    ('سُورَةُ الْقَارِعَةِ · Sura El-Karia', 'سُورَةُ الْقَارِعَةِ · Surah Al-Qari‘ah'),
    ('sura_el_karia_novi_snimci_zavrsna_offline.html', 'surah_al_qariah.html'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('sura-kariah', EXTRA)
