# bekare-25-29: Abdo ef. Rekić's Al-Baqarah recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('Ajet 25', 'Ayah 25'),
    ('El-Bekare 25–29 – interaktivno učenje', 'Al-Baqarah 25–29'),
    ('bekare_25_29_index.html', 'baqarah_25_29.html'),
    ('El-Bekare • ajeti 25–29', 'Al-Baqarah • ayahs 25–29'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('bekare-25-29', EXTRA)
