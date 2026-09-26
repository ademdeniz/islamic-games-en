"""Apply per-game translation tables: work/<game>.bs.html -> work/<game>.en.html -> games/<game>/index.html.

  python3 tools/translate.py <game> [<game> ...]

Each table is a list of (bosnian, english) exact-string replacements in tools/tr/<game>.py (variable T),
plus an optional transform(src) function for structural edits.
Every Bosnian string must occur in the source, so typos fail loudly instead of silently skipping.
"""
import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import skel  # noqa: E402

ROOT = skel.ROOT

for game in sys.argv[1:]:
    skel.extract(game)  # first: some tables read work/<game>.bs.html while loading
    frozen = os.path.join(ROOT, 'tools', 'tr', game + '.en.html')
    if os.path.exists(frozen):  # finished English skeleton kept in the repo (games that were edited by hand)
        import shutil
        shutil.copy(frozen, os.path.join(ROOT, 'work', game + '.en.html'))
        skel.build(game)
        continue
    spec0 = importlib.util.spec_from_file_location(game + '_cfg', os.path.join(ROOT, 'tools', 'tr', game + '.py'))
    cfg = importlib.util.module_from_spec(spec0)
    spec0.loader.exec_module(cfg)
    if hasattr(cfg, 'BUILD'):
        print(f'{game}: built by {cfg.BUILD}, not a translation table – run that instead')
        continue
    spec = importlib.util.spec_from_file_location(game, os.path.join(ROOT, 'tools', 'tr', game + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    src = open(os.path.join(ROOT, 'work', game + '.bs.html'), encoding='utf-8').read()
    for bs, en in getattr(mod, 'T', []) + [(d, '') for d in getattr(mod, 'DELETE', [])]:
        assert bs in src, f'{game}: not found: {bs[:80]!r}'
        src = src.replace(bs, en)
    if hasattr(mod, 'transform'):  # for structural changes a plain replacement table can't express
        src = mod.transform(src)
    open(os.path.join(ROOT, 'work', game + '.en.html'), 'w', encoding='utf-8').write(src)
    skel.build(game)
