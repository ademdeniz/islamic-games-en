# sura-kafirun: Abdo ef. Rekić's recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('Sura El-Kafirun', 'Surah Al-Kafirun'),
    ('سُورَةُ الْكَافِرُونَ · El-Kafirun', 'سُورَةُ الْكَافِرُونَ · Al-Kafirun'),
    ('sura_el_kafirun_sa_bismillom_offline.html', 'surah_al_kafirun.html'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('sura-kafirun', EXTRA)
