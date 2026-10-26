# sura-kevser: Abdo ef. Rekić's recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('Sura El-Kevser', 'Surah Al-Kawthar'),
    ('Sura El-Kevser offline', 'Surah Al-Kawthar'),
    ('سُورَةُ الْكَوْثَرِ · El-Kevser', 'سُورَةُ الْكَوْثَرِ · Al-Kawthar'),
    ('sura_el_kevser_sa_ucenjem_bismille_offline.html', 'surah_al_kawthar.html'),
    ('sura_el_kevser_podesavanje.json', 'surah_al_kawthar_timings.json'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('sura-kevser', EXTRA)
