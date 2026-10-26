# dova-poslije-ezana: Abdo ef. Rekić's "Salah Academy" lesson on the dua after the Adhan (learn, match, order, missing part,
# meaning, final test). Dua lines and buttons from _rekic_dua.py; the quiz questions are built from a few patterns.
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_dua import TABLE  # noqa: E402
from _rekic_ui import page  # noqa: E402

DELETE, ALLOW_ARABIC, _base, BRAND_FIT = page('dova-poslije-ezana', TABLE)
ALLOW_ARABIC = []   # the transliteration only, no Arabic script
EN = dict(TABLE)
PATTERNS = [
    (r'Šta znači „(.+?)”\?', 'What does “{}” mean?'),
    (r'Koji dio dove znači: „(.+?)”\?', 'Which part of the dua means: “{}”?'),
    (r'Koji dio dove dolazi odmah poslije „(.+?)”\?', 'Which part of the dua comes right after “{}”?'),
    (r'Koji dio dove dolazi neposredno prije „(.+?)”\?', 'Which part of the dua comes right before “{}”?'),
]


def transform(src):
    for pat, en in PATTERNS:   # whole JS strings only
        src = re.sub(r'(?<=")' + pat + r'(?=")', lambda m: en.format(EN[m.group(1)]), src)
    return _base(src)
