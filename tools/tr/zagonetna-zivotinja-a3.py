# zagonetna-zivotinja-a3: same page text and the identical 321-question bank as zagonetna-zivotinja-80
# (only the tile grid differs: 30 tiles instead of 80, and no jungle CSS banner), so it reuses that table.
import importlib.util
import os

_spec = importlib.util.spec_from_file_location(
    'zz80', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zagonetna-zivotinja-80.py'))
_zz80 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_zz80)

T = [t for t in _zz80.T if t not in _zz80.T80]
ALLOW = _zz80.ALLOW
ALLOW_INCONSISTENT = _zz80.ALLOW_INCONSISTENT
transform = _zz80.transform
