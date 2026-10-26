# penali2: Abdo ef. Rekić's "BiH – Penalties & album" – shared table and question banks in _penali.py.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _penali import PLAYERS, setup  # noqa: E402

DELETE, BRAND_FIT, transform = setup('penali2')
ALLOW = PLAYERS
