# sura-tekasur: Abdo ef. Rekić's recitation page – shared button/message table in _rekic_ui.py, the page's own titles here.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

EXTRA = [
    ('Sura Et-Tekasur – Završna verzija', 'Surah At-Takathur'),
    ('سُورَةُ التَّكَاثُرِ · Sura Et-Tekasur', 'سُورَةُ التَّكَاثُرِ · Surah At-Takathur'),
    ('sura_et_tekasur_offline.html', 'surah_at_takathur.html'),
]
DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('sura-tekasur', EXTRA)
