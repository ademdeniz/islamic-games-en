# dove-namaska-dova: Abdo ef. Rekić's dua page – the dua lines and shared buttons are in _rekic_dua.py.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_dua import TABLE  # noqa: E402
from _rekic_ui import page  # noqa: E402

DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page('dove-namaska-dova', TABLE)
ALLOW = ['Amin']
ALLOW_INCONSISTENT = ['bs']   # a code name for the translation column (setMode('bs')), not text
