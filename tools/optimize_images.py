"""Make heavy games lighter for phones: re-save big JPEG pictures at a sensible size.

Pictures are resized so the longest side is at most MAX_SIDE and saved as progressive JPEG (quality QUALITY).
A smaller version is kept only if it saves at least 25%; it goes to assets/optimized/<game>/<n>.jpg and
tools/skel.py uses it instead of the original when building the game.

  .venv/bin/python tools/optimize_images.py <game> [<game> ...]
"""
import base64
import io
import json
import os
import re
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import skel  # noqa: E402

MAX_SIDE, QUALITY, MIN_SAVING = 1024, 78, 0.25


def optimize(game):
    skel.extract(game)
    blobs = json.load(open(os.path.join(ROOT, 'work', game + '.blobs.json')))
    out_dir = os.path.join(ROOT, 'assets', 'optimized', game)
    before = after = kept = 0
    for n, b in enumerate(blobs):
        m = re.match(r'data:image/[a-z]+;base64,(.*)', b, re.S)
        if not m or skel.fixed_image(game, n, optimized=False):   # hand-fixed pictures are handled elsewhere
            continue
        raw = base64.b64decode(re.sub(r'\s', '', m.group(1)))
        try:
            im = Image.open(io.BytesIO(raw))
            if im.format != 'JPEG':                                # PNGs may use transparency – leave them
                continue
            im = im.convert('RGB')
        except OSError:                                            # damaged in the original (browsers cope) – leave it
            print(f'  {game}: picture {n} is damaged in the original, kept as is')
            continue
        if max(im.size) > MAX_SIDE:
            im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, 'JPEG', quality=QUALITY, optimize=True, progressive=True)
        before += len(raw)
        if len(buf.getvalue()) <= len(raw) * (1 - MIN_SAVING):
            os.makedirs(out_dir, exist_ok=True)
            open(os.path.join(out_dir, f'{n}.jpg'), 'wb').write(buf.getvalue())
            after += len(buf.getvalue())
            kept += 1
        else:
            after += len(raw)
    print(f'{game}: {kept} pictures made smaller, {before // 1024} KB -> {after // 1024} KB')


if __name__ == '__main__':
    for g in sys.argv[1:]:
        optimize(g)
