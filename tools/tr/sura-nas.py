# sura-nas: Abdo ef. Rekić's recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('Sura En-Nas', 'Surah An-Nas'),
    ('Sura_En_Nas_Abdo_ef_Rekic.html', 'Surah_An_Nas.html'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('sura-nas', EXTRA)
