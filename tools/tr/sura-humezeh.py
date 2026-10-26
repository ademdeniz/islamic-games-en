# sura-humezeh: Abdo ef. Rekić's recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('Sura El-Humeze – Završna verzija', 'Surah Al-Humazah'),
    ('سُورَةُ الْهُمَزَةِ · Sura El-Humeze', 'سُورَةُ الْهُمَزَةِ · Surah Al-Humazah'),
    ('sura_el_humeze_offline.html', 'surah_al_humazah.html'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('sura-humezeh', EXTRA)
