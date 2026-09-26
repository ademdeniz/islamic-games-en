# maca-pripreme-za-namaz: table mode; same text as kviz-maca-namaz, so reuse its table.
import importlib.util as _u, os as _os
_spec = _u.spec_from_file_location('_kviz_maca', _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'kviz-maca-namaz.py'))
_m = _u.module_from_spec(_spec); _spec.loader.exec_module(_m)
T = list(_m.T)


# ---- The live score and obstacle numbers sit right after the painted "Points:" / "Obstacle:" labels ----------------
STRUCTURAL = ('live score/obstacle numbers moved onto the painted score box (the picture was re-lettered in English '
              'without the static numbers, tools/fix_images.py)')
_HUD = [
    ('#sc{top:3%;width:20%}', '#sc{top:1.56%;right:2%;width:7.5%;height:2.2%}'),
    ('#lv{top:8%;width:20%}', '#lv{top:5.34%;right:0.8%;width:6.8%;height:2.2%}'),
    ('#sc,#lv{position:absolute;', '#g{container-type:size}#sc,#lv{display:flex;align-items:center;justify-content:flex-start;'
                                   'font-size:2.05cqh;white-space:nowrap;position:absolute;'),
]
_prev_transform = globals().get('transform')


def transform(src):
    if _prev_transform:
        src = _prev_transform(src)
    for a, b in _HUD:
        assert src.count(a) == 1, 'score position patch target not found: ' + a
        src = src.replace(a, b)
    return src
