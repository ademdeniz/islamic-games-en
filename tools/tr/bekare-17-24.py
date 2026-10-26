# bekare-17-24: Abdo ef. Rekić's Al-Baqarah recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('El-Bekare · ajet ', 'Al-Baqarah · ayah '),
    ('سُورَةُ الْبَقَرَةِ · El-Bekare 17–24', 'سُورَةُ الْبَقَرَةِ · Al-Baqarah 17–24'),
    ('bekare_17_24_zavrsna_offline.html', 'baqarah_17_24.html'),
    ('El-Bekare 17–24 – Završna verzija', 'Al-Baqarah 17–24'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('bekare-17-24', EXTRA)
