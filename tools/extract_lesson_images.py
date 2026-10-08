"""Take illustrations out of the Ilmihal PDFs for the lesson pages -> lessons/<book>/img/<name>.webp

Needs the PDFs (default folder ~/Downloads, or ILMIHAL_PDFS=/path) and poppler's `pdfimages`.
Illustrations with a soft mask (a grayscale image right after the colour one) keep their transparent edges;
tiled pictures are stitched back together.

  .venv/bin/python tools/extract_lesson_images.py
"""
import os
import subprocess
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDFS = os.environ.get('ILMIHAL_PDFS', os.path.expanduser('~/Downloads'))
MAX_SIDE = 900

# Image numbers are as listed by `pdfimages -f <first> -l <last> -list` for each book's page range below.
RANGES = {1: (8, 9), 2: (9, 9), 3: (9, 9)}
# name: (book number, pdf page, [image numbers], layout[, (first, last)][, sign])
#   sign = {'box': (x0, y0, x1, y1), 'lines': [...]}: Bosnian words painted on a sign are erased and English drawn in
#   the optional range overrides RANGES for that picture (numbers are then counted from its first page)
#   layout 'mask'  = colour image + soft mask;  'photo' = plain image;  '2x2' = four tiles
IMAGES = {
    'ilmihal-1': {
        'reading': (1, 8, [25, 26], 'mask'),
        'waking-up': (1, 9, [29, 30], 'mask'),
        'bike': (1, 9, [31, 32], 'mask'),
        'studying': (1, 9, [33, 34], 'mask'),
        'playing': (1, 9, [35, 36], 'mask'),
        'car': (1, 9, [37, 38], 'mask'),
        'sleeping': (1, 9, [39, 40], 'mask'),
        'muallim': (1, 9, [43, 44], 'mask'),
        'thinking': (1, 10, [0, 1], 'mask', (10, 10)),
        'baby': (1, 10, [2, 3], 'mask', (10, 10)),
        'to-maktab': (1, 11, [1, 2], 'mask', (11, 11)),
        'classroom': (1, 11, [3, 4], 'mask', (11, 11)),
        'muallim-boy': (1, 11, [7, 8], 'mask', (11, 11)),
        'dua-girl': (1, 12, [0, 1], 'mask', (12, 12)),
        'children-dua': (1, 13, [1, 2], 'mask', (13, 13)),
        'i-am-muslim': (1, 14, [0, 1], 'mask', (14, 14), {'box': (60, 252, 414, 486), 'lines': ['I AM', 'A', 'MUSLIM']}),
        'islam-my-religion': (1, 14, [2, 3], 'mask', (14, 14), {'box': (48, 254, 315, 475), 'lines': ['ISLAM', 'IS MY', 'RELIGION']}),
        'reading-together': (1, 15, [0, 1], 'mask', (15, 15)),
        'mirza-and-father': (1, 16, [0, 1], 'mask', (16, 16)),
        'salam': (1, 18, [0, 1], 'mask', (18, 18)),
        'madinah-mosque': (1, 26, [0, 1], 'mask', (26, 26)),
    },
    'ilmihal-2': {
        'arafat': (2, 9, [0], 'photo'),
        'sajdah': (2, 11, [0, 1], 'mask', (11, 11)),
        'mushaf': (2, 16, [0], 'photo', (16, 16)),
        'scales': (2, 19, [0, 1], 'mask', (19, 19)),
    },
    'ilmihal-3': {
        'straight-path': (3, 9, [0, 1, 2, 3], '2x2'),
        'two-faces': (3, 18, [0, 1], 'side', (18, 18)),
    },
}


def book_images(book, tmp, rng=None):
    pdf = os.path.join(PDFS, f'Ilmihal {book}, 2020.pdf')
    first, last = map(str, rng or RANGES[book])
    prefix = os.path.join(tmp, f'b{book}-{first}-{last}')
    subprocess.run(['pdfimages', '-f', first, '-l', last, '-png', pdf, prefix], check=True)
    listing = subprocess.run(['pdfimages', '-f', first, '-l', last, '-list', pdf],
                             capture_output=True, text=True, check=True).stdout.splitlines()[2:]
    nums = [int(line.split()[1]) for line in listing]   # image numbers, in the same order as the files
    files = sorted(f for f in os.listdir(tmp) if f.startswith(f'b{book}-{first}-{last}-'))
    return {n: os.path.join(tmp, f) for n, f in zip(nums, files)}


def make(layout, paths):
    if layout == 'mask':
        img = Image.open(paths[0]).convert('RGB')
        img.putalpha(Image.open(paths[1]).convert('L').resize(img.size))
        return img
    if layout == 'photo':
        return Image.open(paths[0]).convert('RGB')
    if layout == 'side':   # one picture stored as two halves, left and right
        a, b = (Image.open(p).convert('RGB') for p in paths)
        img = Image.new('RGB', (a.width + b.width, max(a.height, b.height)))
        img.paste(a, (0, 0))
        img.paste(b, (a.width, 0))
        return img
    tiles = [Image.open(p).convert('RGB') for p in paths]   # 2x2: top-left, top-right, bottom-left, bottom-right
    w, h = tiles[0].width + tiles[1].width, tiles[0].height + tiles[2].height
    img = Image.new('RGB', (w, h))
    img.paste(tiles[0], (0, 0))
    img.paste(tiles[1], (tiles[0].width, 0))
    img.paste(tiles[2], (0, tiles[0].height))
    img.paste(tiles[3], (tiles[2].width, tiles[1].height))
    return img


def resign(img, sign):
    """Erase the coloured letters inside sign['box'] (inpainting from the pale sign around them) and write the English."""
    import cv2
    import numpy as np
    from PIL import ImageDraw, ImageFont
    x0, y0, x1, y1 = sign['box']
    rgb = np.array(img.convert('RGB'))
    region = rgb[y0:y1, x0:x1].astype(int)
    ink = (region.sum(2) < 560) | (np.abs(region[:, :, 0] - region[:, :, 1]) > 60)   # darker or strongly coloured = letters
    colour = tuple(int(c) for c in np.median(region[ink], axis=0)) if ink.any() else (40, 60, 160)
    mask = np.zeros(rgb.shape[:2], np.uint8)
    mask[y0:y1, x0:x1] = cv2.dilate(ink.astype(np.uint8) * 255, np.ones((5, 5), np.uint8))
    clean = cv2.inpaint(rgb, mask, 7, cv2.INPAINT_TELEA)
    out = Image.fromarray(clean)
    if img.mode == 'RGBA':
        out.putalpha(img.getchannel('A'))
    d = ImageDraw.Draw(out)
    font_path = '/System/Library/Fonts/Supplemental/Comic Sans MS Bold.ttf'
    size = 120
    while size > 10:
        f = ImageFont.truetype(font_path, size)
        boxes = [d.textbbox((0, 0), t, font=f) for t in sign['lines']]
        h = sum(b[3] - b[1] for b in boxes) + (len(boxes) - 1) * size * 0.15
        if max(b[2] - b[0] for b in boxes) <= (x1 - x0) * 0.9 and h <= (y1 - y0) * 0.85:
            break
        size -= 2
    y = y0 + ((y1 - y0) - h) / 2
    for t, b in zip(sign['lines'], boxes):
        d.text((x0 + ((x1 - x0) - (b[2] - b[0])) / 2 - b[0], y - b[1]), t, font=f, fill=colour)
        y += (b[3] - b[1]) + size * 0.15
    return out


def main():
    with tempfile.TemporaryDirectory() as tmp:
        cache = {}
        for book_id, items in IMAGES.items():
            out_dir = os.path.join(ROOT, 'lessons', book_id, 'img')
            os.makedirs(out_dir, exist_ok=True)
            for name, (book, page, nums, layout, *more) in items.items():
                rng = [m for m in more if isinstance(m, tuple)]
                sign = next((m for m in more if isinstance(m, dict)), None)
                key = (book, *(rng[0] if rng else RANGES[book]))
                if key not in cache:
                    cache[key] = book_images(book, tmp, rng[0] if rng else None)
                img = make(layout, [cache[key][n] for n in nums])
                if sign:
                    img = resign(img, sign)
                img.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
                path = os.path.join(out_dir, name + '.webp')
                img.save(path, 'WEBP', quality=80, method=6)
                print(f'{book_id}/img/{name}.webp  {img.size[0]}x{img.size[1]}  {os.path.getsize(path) // 1024} KB')


if __name__ == '__main__':
    main()
