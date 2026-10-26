# bekare-30-37: Abdo ef. Rekić's Al-Baqarah recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('bekare_30_37_index.html', 'baqarah_30_37.html'),
    ('El-Bekare • ajeti 30–37 • žuto praćenje riječi', 'Al-Baqarah • ayahs 30–37 • words light up in yellow'),
    ('El-Bekare 30–37 – završna', 'Al-Baqarah 30–37'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('bekare-30-37', EXTRA)
