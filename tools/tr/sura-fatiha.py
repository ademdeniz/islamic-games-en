# sura-fatiha: Abdo ef. Rekić's recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('Sura El-Fatiha', 'Surah Al-Fatiha'),
    ('Sura_El_Fatiha.html', 'Surah_Al_Fatiha.html'),
    ('Sura El-Fatiha • pomjeraj gore–dolje • kod svakog ajeta Uči i Ponavljaj • iPhone i Android', 'Surah Al-Fatiha • scroll up and down • Recite and Repeat at every ayah • iPhone and Android'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('sura-fatiha', EXTRA)
