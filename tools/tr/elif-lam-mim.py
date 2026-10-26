# elif-lam-mim: Abdo ef. Rekić's Al-Baqarah recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('El-Bekare – ajeti 1–5', 'Al-Baqarah – ayahs 1–5'),
    ('Bismilla i prvih 5 ajeta – automatsko praćenje riječi', 'Bismillah and the first 5 ayahs – the words light up with the recitation'),
    ('El_Bekare_ajeti_1-5_Abdo_ef_Rekic.html', 'Al_Baqarah_ayahs_1-5.html'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('elif-lam-mim', EXTRA)
