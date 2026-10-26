# bekare-22-24: Abdo ef. Rekić's Al-Baqarah recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('El-Bekare 22–24 – završna verzija', 'Al-Baqarah 22–24'),
    ('سورة البقرة · El-Bekare 22–24', 'سورة البقرة · Al-Baqarah 22–24'),
    ('bekare_22_23_24_zavrsna_offline.html', 'baqarah_22_24.html'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('bekare-22-24', EXTRA)
