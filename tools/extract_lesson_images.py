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
# name: (book number, pdf page, [image numbers], layout)
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
    },
    'ilmihal-2': {
        'arafat': (2, 9, [0], 'photo'),
    },
    'ilmihal-3': {
        'straight-path': (3, 9, [0, 1, 2, 3], '2x2'),
    },
}


def book_images(book, tmp):
    pdf = os.path.join(PDFS, f'Ilmihal {book}, 2020.pdf')
    first, last = map(str, RANGES[book])
    prefix = os.path.join(tmp, f'b{book}')
    subprocess.run(['pdfimages', '-f', first, '-l', last, '-png', pdf, prefix], check=True)
    listing = subprocess.run(['pdfimages', '-f', first, '-l', last, '-list', pdf],
                             capture_output=True, text=True, check=True).stdout.splitlines()[2:]
    nums = [int(line.split()[1]) for line in listing]   # image numbers, in the same order as the files
    files = sorted(f for f in os.listdir(tmp) if f.startswith(f'b{book}-'))
    return {n: os.path.join(tmp, f) for n, f in zip(nums, files)}


def make(layout, paths):
    if layout == 'mask':
        img = Image.open(paths[0]).convert('RGB')
        img.putalpha(Image.open(paths[1]).convert('L').resize(img.size))
        return img
    if layout == 'photo':
        return Image.open(paths[0]).convert('RGB')
    tiles = [Image.open(p).convert('RGB') for p in paths]   # 2x2: top-left, top-right, bottom-left, bottom-right
    w, h = tiles[0].width + tiles[1].width, tiles[0].height + tiles[2].height
    img = Image.new('RGB', (w, h))
    img.paste(tiles[0], (0, 0))
    img.paste(tiles[1], (tiles[0].width, 0))
    img.paste(tiles[2], (0, tiles[0].height))
    img.paste(tiles[3], (tiles[2].width, tiles[1].height))
    return img


def main():
    with tempfile.TemporaryDirectory() as tmp:
        cache = {}
        for book_id, items in IMAGES.items():
            out_dir = os.path.join(ROOT, 'lessons', book_id, 'img')
            os.makedirs(out_dir, exist_ok=True)
            for name, (book, page, nums, layout) in items.items():
                if book not in cache:
                    cache[book] = book_images(book, tmp)
                img = make(layout, [cache[book][n] for n in nums])
                img.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
                path = os.path.join(out_dir, name + '.webp')
                img.save(path, 'WEBP', quality=80, method=6)
                print(f'{book_id}/img/{name}.webp  {img.size[0]}x{img.size[1]}  {os.path.getsize(path) // 1024} KB')


if __name__ == '__main__':
    main()
