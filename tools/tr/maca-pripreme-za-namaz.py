# maca-pripreme-za-namaz: table mode; same text as kviz-maca-namaz, so reuse its table.
import importlib.util as _u, os as _os
_spec = _u.spec_from_file_location('_kviz_maca', _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'kviz-maca-namaz.py'))
_m = _u.module_from_spec(_spec); _spec.loader.exec_module(_m)
T = list(_m.T)
