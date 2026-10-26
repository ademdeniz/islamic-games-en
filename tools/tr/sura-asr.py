# sura-asr: Abdo ef. Rekić's recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('Sura El-Asr – Završna verzija', 'Surah Al-‘Asr'),
    ('Sura El-Asr', 'Surah Al-‘Asr'),
    ('سُورَةُ الْعَصْرِ · Sura El-Asr', 'سُورَةُ الْعَصْرِ · Surah Al-‘Asr'),
    ('sura_el_asr_offline.html', 'surah_al_asr.html'),
    ('sura_el_asr_podesavanje.json', 'surah_al_asr_timings.json'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('sura-asr', EXTRA)
