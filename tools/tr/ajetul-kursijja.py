# ajetul-kursijja: Abdo ef. Rekić's recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('Učenje Ajetul-Kursije', 'Reciting Ayat al-Kursi'),
    ('Spremno za učenje Ajetul-Kursije.', 'Ready to recite Ayat al-Kursi.'),
    ('آيَةُ الْكُرْسِيِّ · Ajetul-Kursija (2:255)', 'آيَةُ الْكُرْسِيِّ · Ayat al-Kursi (2:255)'),
    ('Ajetul-Kursija – završna verzija dodirom', 'Ayat al-Kursi'),
    ('ajetul_kursija_zavrsna_offline.html', 'ayat_al_kursi.html'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('ajetul-kursijja', EXTRA)
