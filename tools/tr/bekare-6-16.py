# bekare-6-16: Abdo ef. Rekić's Al-Baqarah recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('El-Bekare 6–16', 'Al-Baqarah 6–16'),
    ('Ajet 6', 'Ayah 6'),
    ('bekare_6_16_podesavanje.json', 'baqarah_6_16_timings.json'),
    ('El-Bekare • ajeti 6–16 • interaktivno učenje', 'Al-Baqarah • ayahs 6–16 • learn along'),
    ('bekare_6_16_index.html', 'baqarah_6_16.html'),
    ('El-Bekare 6–16 – Downloads i učenje redom', 'Al-Baqarah 6–16'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('bekare-6-16', EXTRA)
