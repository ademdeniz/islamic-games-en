"""Replace Bosnian text painted into game background pictures with English.

For each text box: find the text pixels (by brightness), erase them by inpainting from the surrounding picture,
then draw the English text centred in the same place.

  .venv/bin/python tools/fix_images.py <game>    -> assets/fixed/<game>-bg-<n>.jpg  (+ a before/after preview)
"""
import base64
import io
import json
import os
import re
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = '/System/Library/Fonts/Supplemental/'
NARROW, ROUNDED, SERIF = FONTS + 'Arial Narrow Bold.ttf', FONTS + 'Arial Rounded Bold.ttf', FONTS + 'Georgia Bold.ttf'
SANS, GEORGIA = FONTS + 'Trebuchet MS.ttf', FONTS + 'Georgia.ttf'
ARIALB = FONTS + 'Arial Bold.ttf'
MACA_INK, MACA_WHITE = (58, 30, 12), (255, 248, 235)
GOLD, CREAM, WHITE, INK = (240, 196, 104), (236, 226, 206), (250, 250, 250), (42, 26, 10)

# box = (x0, y0, x1, y1) in image pixels; dark=True -> text is darker than its background (else lighter)
# threshold = brightness that separates text from background; lines = English text; font; colour; max size
JOBS = {
    'pomozimo-maci-abdest': {'blob': 0, 'boxes': [
        dict(box=(405, 25, 920, 152), dark=True, threshold=110, lines=['Let’s Help the Kitty', 'Make Wudu'],
             font=ROUNDED, color=(62, 34, 18), size=54),
        dict(box=(455, 150, 860, 195), dark=True, threshold=120, lines=[], font=ROUNDED, color=(62, 34, 18), size=30),
        dict(box=(1335, 32, 1475, 62), dark=True, threshold=120, lines=['POINTS:'], font=ROUNDED, color=(62, 34, 18), size=24),
        dict(box=(1335, 125, 1475, 158), dark=True, threshold=120, lines=['TIME:'], font=ROUNDED, color=(62, 34, 18), size=24),
        dict(box=(1345, 220, 1470, 252), dark=True, threshold=120, lines=['LIVES:'], font=ROUNDED, color=(62, 34, 18), size=24),
        dict(box=(1180, 345, 1305, 378), dark=True, threshold=120, lines=['MOSQUE'], font=ROUNDED, color=(70, 60, 55), size=20),
        dict(box=(305, 285, 395, 322), dark=True, threshold=120, lines=['Ears'], font=NARROW, color=(14, 30, 82), size=30),
        dict(box=(585, 335, 660, 402), dark=True, threshold=120, lines=['Nose', '3x'], font=NARROW, color=(14, 30, 82), size=28),
        dict(box=(925, 368, 1075, 452), dark=True, threshold=120, lines=['Left arm', 'past elbow', '3x'], font=NARROW, color=(14, 30, 82), size=26),
        dict(box=(1325, 490, 1410, 528), dark=True, threshold=120, lines=['Masah'], font=NARROW, color=(14, 30, 82), size=28),
        dict(box=(775, 570, 860, 638), dark=True, threshold=120, lines=['Hands', '3x'], font=NARROW, color=(14, 30, 82), size=28),
        dict(box=(530, 640, 605, 702), dark=True, threshold=120, lines=['Face', '3x'], font=NARROW, color=(14, 30, 82), size=28),
        dict(box=(1050, 695, 1195, 782), dark=True, threshold=120, lines=['Right arm', 'past elbow', '3x'], font=NARROW, color=(14, 30, 82), size=26),
        dict(box=(845, 845, 925, 912), dark=True, threshold=120, lines=['Mouth', '3x'], font=NARROW, color=(14, 30, 82), size=28),
        dict(box=(1310, 865, 1385, 903), dark=True, threshold=120, lines=['Neck'], font=NARROW, color=(14, 30, 82), size=28),
        dict(box=(535, 1135, 668, 1232), dark=True, threshold=120, lines=['A’udhu,', 'Bismillah,', 'niyyah'], font=NARROW, color=(14, 30, 82), size=25),
        dict(box=(775, 1160, 910, 1222), dark=True, threshold=120, lines=['Right foot', 'to ankle'], font=NARROW, color=(14, 30, 82), size=25),
        dict(box=(1005, 1135, 1115, 1196), dark=True, threshold=120, lines=['Shahadah'], font=NARROW, color=(14, 30, 82), size=26),
        dict(box=(1215, 1160, 1345, 1225), dark=True, threshold=120, lines=['Left foot', 'to ankle'], font=NARROW, color=(14, 30, 82), size=25),
    ]},
    'kviz-nivo-a1': {'blob': 0, 'boxes': [
        dict(box=(490, 50, 1050, 128), dark=False, threshold=90, lines=['QUIZ LEVEL A1'], font=SERIF, color=GOLD, size=66),
        dict(box=(548, 132, 990, 180), dark=False, threshold=110, lines=[], font=GEORGIA, color=CREAM, size=36),
        dict(box=(668, 205, 868, 240), dark=False, threshold=110, lines=['“Knowledge is light.”'], font=SANS, color=CREAM, size=22),
        dict(box=(103, 72, 200, 98), dark=False, threshold=110, lines=['Islam'], font=SANS, color=CREAM, size=22),
        dict(box=(103, 106, 210, 132), dark=False, threshold=110, lines=['Knowledge'], font=SANS, color=CREAM, size=22),
        dict(box=(103, 140, 215, 166), dark=False, threshold=110, lines=['Character'], font=SANS, color=CREAM, size=22),
        dict(box=(103, 174, 205, 200), dark=False, threshold=110, lines=['Better future'], font=SANS, color=CREAM, size=22),
        dict(box=(1350, 70, 1450, 98), dark=False, threshold=110, lines=['Learn'], font=SANS, color=CREAM, size=22),
        dict(box=(1350, 104, 1455, 132), dark=False, threshold=110, lines=['Reflect'], font=SANS, color=CREAM, size=22),
        dict(box=(1350, 138, 1455, 166), dark=False, threshold=110, lines=['Apply'], font=SANS, color=CREAM, size=22),
        dict(box=(1350, 172, 1450, 200), dark=False, threshold=110, lines=['Be better'], font=SANS, color=CREAM, size=22),
        dict(box=(572, 425, 963, 452), dark=False, threshold=110, lines=['Questions are picked at random from 163'], font=SANS, color=CREAM, size=21),
        dict(box=(48, 460, 132, 490), dark=False, threshold=100, lines=['Question'], font=SERIF, color=GOLD, size=24),
        dict(box=(48, 618, 212, 650), dark=False, threshold=100, lines=['Correct answers'], font=SERIF, color=GOLD, size=24),
        dict(box=(48, 733, 133, 762), dark=False, threshold=100, lines=['Points'], font=SERIF, color=GOLD, size=24),
        dict(box=(42, 932, 220, 996), dark=False, threshold=110, lines=['Little by little', 'to great knowledge!'], font=SANS, color=CREAM, size=19),
        dict(box=(485, 535, 1060, 640), dark=False, threshold=110, lines=['What was the name of the father', 'of Muhammad (SAW)?'], font=SERIF, color=WHITE, size=36),
        dict(box=(885, 715, 1005, 752), dark=False, threshold=110, lines=['Abu Talib'], font=SERIF, color=WHITE, size=30),
        dict(box=(885, 818, 1070, 856), dark=False, threshold=110, lines=['Abdul-Muttalib'], font=SERIF, color=WHITE, size=30),
        dict(box=(610, 925, 720, 968), dark=False, threshold=200, lines=['Correct!'], font=SERIF, color=WHITE, size=32),
        dict(box=(810, 925, 968, 965), dark=False, threshold=200, lines=['+10 points'], font=SERIF, color=WHITE, size=28),
        dict(box=(1325, 572, 1480, 625), dark=False, threshold=110, lines=['Removes two', 'wrong answers'], font=SANS, color=CREAM, size=18),
        dict(box=(1398, 693, 1492, 730), dark=False, threshold=110, lines=['Audience'], font=SERIF, color=WHITE, size=26),
        dict(box=(1335, 762, 1475, 812), dark=False, threshold=110, lines=['See what the', 'audience says'], font=SANS, color=CREAM, size=18),
        dict(box=(1398, 870, 1495, 945), dark=False, threshold=110, lines=['Ask the', 'teacher'], font=SERIF, color=WHITE, size=26),
        dict(box=(1322, 958, 1485, 988), dark=False, threshold=110, lines=['Advice from the teacher'], font=SANS, color=CREAM, size=18),
        dict(box=(630, 1040, 878, 1088), dark=True, threshold=100, lines=['Next question'], font=SERIF, color=INK, size=32),
        dict(box=(588, 1125, 938, 1155), dark=False, threshold=110, lines=['Question 2/30 loads automatically…'], font=SANS, color=CREAM, size=20),
        dict(box=(555, 1245, 982, 1308), dark=False, threshold=110, lines=['“The best among you are those who learn', 'the Qur’an and teach it.”'], font=SANS, color=CREAM, size=22),
        dict(box=(730, 1312, 805, 1335), dark=False, threshold=110, lines=['(Bukhari)'], font=SANS, color=CREAM, size=15),
        dict(box=(92, 1316, 198, 1342), dark=False, threshold=110, lines=['Sound on'], font=SANS, color=CREAM, size=17),
        dict(box=(312, 1316, 450, 1342), dark=False, threshold=110, lines=['Background music'], font=SANS, color=CREAM, size=16),
        dict(box=(1155, 1313, 1380, 1342), dark=False, threshold=110, lines=['Let knowledge be your path.'], font=SANS, color=CREAM, size=18),
    ]},
    'kviz-maca-namaz': {'blob': 0, 'flatten': (20, 53, 28), 'boxes': [
        dict(box=(100, 30, 345, 108), dark=True, threshold=120, lines=['Let’s help the kitty', 'get back home!'], font=ROUNDED, color=MACA_INK, size=30),
        dict(box=(45, 110, 322, 200), dark=True, threshold=120, lines=['Match the pairs on each obstacle.', 'When all the pairs are gone,', 'the kitty can move on!'], font=ARIALB, color=MACA_INK, size=19),
        dict(box=(845, 24, 995, 58), dark=False, threshold=170, lines=['Points:'], font=ROUNDED, color=MACA_WHITE, size=24, draw=(850, 24, 928, 58), align='left'),
        dict(box=(845, 82, 1000, 116), dark=False, threshold=170, lines=['Obstacle:'], font=ROUNDED, color=MACA_WHITE, size=22, draw=(850, 82, 935, 116), align='left'),
        dict(box=(845, 139, 1000, 173), dark=False, threshold=170, lines=['Time: --:--'], font=ROUNDED, color=MACA_WHITE, size=22),
        dict(box=(478, 188, 578, 246), dark=True, threshold=120, lines=['HOME IS', 'WAITING!'], font=ROUNDED, color=MACA_INK, size=22),
        dict(box=(416, 293, 510, 337), dark=True, threshold=120, lines=['The Creator'], font=ARIALB, color=MACA_INK, size=17),
        dict(box=(618, 283, 710, 320), dark=True, threshold=120, lines=['Qur’an'], font=ARIALB, color=MACA_INK, size=18),
        dict(box=(713, 325, 807, 374), dark=True, threshold=120, lines=['Allah’s', 'book'], font=ARIALB, color=MACA_INK, size=16),
        dict(box=(212, 365, 322, 412), dark=True, threshold=120, lines=['Muhammad', '(SAW)'], font=ARIALB, color=MACA_INK, size=16),
        dict(box=(355, 373, 462, 414), dark=True, threshold=120, lines=['Angels'], font=ARIALB, color=MACA_INK, size=18),
        dict(box=(543, 343, 628, 397), dark=True, threshold=120, lines=['Created', 'from light'], font=ARIALB, color=MACA_INK, size=15),
        dict(box=(670, 388, 768, 434), dark=True, threshold=120, lines=['Allah’s', 'Messenger'], font=ARIALB, color=MACA_INK, size=15),
        dict(box=(248, 523, 357, 562), dark=True, threshold=120, lines=['Wudu'], font=ARIALB, color=MACA_INK, size=19),
        dict(box=(383, 530, 497, 572), dark=True, threshold=120, lines=['Tayammum'], font=ARIALB, color=MACA_INK, size=18),
        dict(box=(523, 513, 632, 567), dark=True, threshold=120, lines=['Washing', 'with water'], font=ARIALB, color=MACA_INK, size=16),
        dict(box=(668, 521, 782, 572), dark=True, threshold=120, lines=['Symbolic', 'cleansing'], font=ARIALB, color=MACA_INK, size=16),
        dict(box=(238, 608, 347, 650), dark=True, threshold=120, lines=['Adhan'], font=ARIALB, color=MACA_INK, size=19),
        dict(box=(388, 613, 492, 657), dark=True, threshold=120, lines=['Qiblah'], font=ARIALB, color=MACA_INK, size=19),
        dict(box=(533, 603, 642, 657), dark=True, threshold=120, lines=['Call to', 'Salah'], font=ARIALB, color=MACA_INK, size=16),
        dict(box=(678, 603, 792, 657), dark=True, threshold=120, lines=['Direction of', 'the Ka’bah'], font=ARIALB, color=MACA_INK, size=15),
        dict(box=(222, 746, 323, 784), dark=True, threshold=100, lines=['Al-Fatiha'], font=ARIALB, color=MACA_INK, size=17),
        dict(box=(383, 763, 482, 802), dark=True, threshold=100, lines=['Ruku‘'], font=ARIALB, color=MACA_INK, size=18),
        dict(box=(543, 743, 652, 797), dark=True, threshold=100, lines=['Surah in', 'Salah'], font=ARIALB, color=MACA_INK, size=16),
        dict(box=(718, 760, 822, 799), dark=True, threshold=100, lines=['Salam'], font=ARIALB, color=MACA_INK, size=18),
        dict(box=(208, 843, 312, 882), dark=True, threshold=100, lines=['Sajdah'], font=ARIALB, color=MACA_INK, size=18),
        dict(box=(368, 848, 492, 887), dark=True, threshold=100, lines=['Bowing'], font=ARIALB, color=MACA_INK, size=18),
        dict(box=(538, 838, 662, 894), dark=True, threshold=100, lines=['Forehead to', 'the ground'], font=ARIALB, color=MACA_INK, size=15),
        dict(box=(713, 838, 842, 894), dark=True, threshold=100, lines=['End of', 'Salah'], font=ARIALB, color=MACA_INK, size=16),
        dict(box=(213, 998, 307, 1037), dark=True, threshold=120, lines=['Fajr'], font=ARIALB, color=MACA_INK, size=18),
        dict(box=(358, 978, 472, 1032), dark=True, threshold=120, lines=['2 sunnah', '+ 2 fard'], font=ARIALB, color=MACA_INK, size=15),
        dict(box=(558, 1001, 662, 1040), dark=True, threshold=120, lines=['Dhuhr'], font=ARIALB, color=MACA_INK, size=18),
        dict(box=(698, 983, 842, 1032), dark=True, threshold=120, lines=['4 sunnah + 4 fard', '+ 2 sunnah'], font=ARIALB, color=MACA_INK, size=14),
        dict(box=(230, 1073, 332, 1112), dark=True, threshold=120, lines=['Maghrib'], font=ARIALB, color=MACA_INK, size=18),
        dict(box=(378, 1056, 492, 1112), dark=True, threshold=120, lines=['3 fard', '+ 2 sunnah'], font=ARIALB, color=MACA_INK, size=15),
        dict(box=(548, 1076, 652, 1114), dark=True, threshold=120, lines=['Isha'], font=ARIALB, color=MACA_INK, size=18),
        dict(box=(703, 1066, 842, 1117), dark=True, threshold=120, lines=['4 fard + 2 sunnah', '+ witr'], font=ARIALB, color=MACA_INK, size=14),
        dict(box=(18, 548, 140, 610), dark=True, threshold=110, lines=['You can', 'do it!'], font=ROUNDED, color=MACA_INK, size=21, angle=12),
        dict(box=(890, 335, 1000, 398), dark=True, threshold=110, lines=['Almost', 'there!'], font=ROUNDED, color=MACA_INK, size=21, angle=-15),
        dict(box=(40, 1062, 185, 1150), dark=True, threshold=110, lines=['Be brave,', 'keep going!'], font=ROUNDED, color=MACA_INK, size=21, angle=14),
        dict(box=(862, 1118, 995, 1200), dark=True, threshold=110, lines=['Together to', 'the finish!'], font=ROUNDED, color=MACA_INK, size=19, angle=-16),
        dict(box=(50, 1372, 215, 1400), dark=True, threshold=120, lines=['Every correct pair'], font=ARIALB, color=MACA_INK, size=19),
        dict(box=(50, 1401, 215, 1428), dark=True, threshold=120, lines=['brings us closer'], font=ARIALB, color=MACA_INK, size=19),
        dict(box=(50, 1430, 118, 1458), dark=True, threshold=120, lines=['home!'], font=ARIALB, color=MACA_INK, size=19),
        dict(box=(722, 1402, 995, 1478), dark=True, threshold=120, lines=['Tap two cards that belong together.', 'Those two stones, blocks or logs', 'will disappear!'], font=ARIALB, color=MACA_INK, size=16),
    ]},
}
JOBS['maca-pripreme-za-namaz'] = JOBS['kviz-maca-namaz']   # same picture


def load_blob(game, n):
    blob = json.load(open(os.path.join(ROOT, 'work', game + '.blobs.json')))[n]
    m = re.match(r'data:(image/[a-z]+);base64,(.*)', blob, re.S)
    return m.group(1), Image.open(io.BytesIO(base64.b64decode(re.sub(r'\s', '', m.group(2)))))


def text_mask(img, spec):
    x0, y0, x1, y1 = spec['box']
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    mask = np.zeros(gray.shape, np.uint8)
    region = gray[y0:y1, x0:x1]
    hit = region < spec['threshold'] if spec['dark'] else region > spec['threshold']
    mask[y0:y1, x0:x1] = hit.astype(np.uint8) * 255
    return cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=1)  # include anti-aliased edges


def fit_font(path, lines, width, height, size):
    while size > 10:
        f = ImageFont.truetype(path, size)
        w = max(f.getbbox(line)[2] - f.getbbox(line)[0] for line in lines)
        h = len(lines) * size * 1.08
        if w <= width and h <= height * 1.05:
            return f
        size -= 1
    return ImageFont.truetype(path, size)


def draw_lines(draw, spec, img=None):
    if not spec['lines']:
        return
    if spec.get('angle') and img is not None:
        return draw_rotated(img, spec)
    x0, y0, x1, y1 = spec.get('draw', spec['box'])   # 'draw': where to write, if not the whole erased box
    f = fit_font(spec['font'], spec['lines'], x1 - x0, y1 - y0, spec['size'])
    lh = f.size * 1.08
    top = (y0 + y1) / 2 - lh * len(spec['lines']) / 2
    left = spec.get('align') == 'left'
    for i, line in enumerate(spec['lines']):
        draw.text((x0 if left else (x0 + x1) / 2, top + lh * (i + 0.5)), line, font=f, fill=spec['color'],
                  anchor='lm' if left else 'mm')


def draw_rotated(img, spec):
    """Text on a tilted sign: draw it level on a transparent layer, rotate, and paste it centred on the box."""
    x0, y0, x1, y1 = spec['box']
    w, h = int((x1 - x0) * 0.92), int((y1 - y0) * 0.62)
    f = fit_font(spec['font'], spec['lines'], w, h, spec['size'])
    lh = f.size * 1.08
    layer = Image.new('RGBA', (w + 40, int(lh * len(spec['lines'])) + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i, line in enumerate(spec['lines']):
        d.text((layer.width / 2, 10 + lh * (i + 0.5)), line, font=f, fill=spec['color'] + (255,), anchor='mm')
    layer = layer.rotate(spec['angle'], resample=Image.BICUBIC, expand=True)
    img.paste(layer, (int((x0 + x1) / 2 - layer.width / 2), int((y0 + y1) / 2 - layer.height / 2)), layer)


def fix(game):
    job = JOBS[game]
    mime, img = load_blob(game, job['blob'])
    if img.mode in ('RGBA', 'LA', 'P'):   # slightly see-through picture: flatten it onto the game's background colour
        rgba = img.convert('RGBA')
        base = Image.new('RGBA', rgba.size, job.get('flatten', (255, 255, 255)) + (255,))
        img = Image.alpha_composite(base, rgba)
    img = img.convert('RGB')
    before = img.copy()
    mask = np.zeros((img.height, img.width), np.uint8)
    for spec in job['boxes']:
        mask |= text_mask(img, spec)
    clean = cv2.inpaint(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR), mask, 6, cv2.INPAINT_TELEA)
    out = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(out)
    for spec in job['boxes']:
        draw_lines(draw, spec, out)
    os.makedirs(os.path.join(ROOT, 'assets', 'fixed'), exist_ok=True)
    path = os.path.join(ROOT, 'assets', 'fixed', f'{game}-bg-{job["blob"]}.jpg')
    out.save(path, quality=86, optimize=True, progressive=True)
    preview = Image.new('RGB', (img.width * 2 + 20, img.height), 'white')
    preview.paste(before, (0, 0))
    preview.paste(out, (img.width + 20, 0))
    preview.save(os.path.join(ROOT, 'work', f'{game}-before-after.jpg'), quality=80)
    print('wrote', path, mime)


if __name__ == '__main__':
    fix(sys.argv[1])
