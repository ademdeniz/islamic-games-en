"""Translation helper: strip embedded media out of a game so only text/code remains, then put it back.

  python3 tools/skel.py extract <game>   -> work/<game>.bs.html  (Bosnian skeleton, media replaced by @@BLOB_n@@)
  python3 tools/skel.py build <game>     -> games/<game>/index.html from work/<game>.en.html
                                            (media restored, lang="en", community logo header added)
"""
import base64
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOB = re.compile(r'data:[a-z]+/[a-z0-9.+-]+;base64,[A-Za-z0-9+/=\s]+?(?=["\')])')

# Pages that only redirect or link to the real game: use the real game file instead.
MAIN_FILE = {
    'el-fatiha': 'index.html',
    'kviz-imanski-sarti': 'Imanski_sarti_iPhone_Android-3.html',
}

BRAND_CSS = (
    '<style>body{flex-wrap:wrap;align-content:flex-start}.bz-brand{flex:0 0 calc(100% - 20px);background:#fff;border:3px solid #c99b3b;border-radius:18px;padding:8px 12px;'
    'margin:10px auto;max-width:880px;width:calc(100% - 20px);box-sizing:border-box;text-align:center}'
    '.bz-brand img{display:block;width:100%;max-width:760px;height:auto;margin:auto}</style>'
)


def main_file(game):
    d = os.path.join(ROOT, 'original', game)
    if game in MAIN_FILE:
        return os.path.join(d, MAIN_FILE[game])
    return max(glob.glob(os.path.join(d, '*.html')), key=os.path.getsize)


def extract(game):
    src = open(main_file(game), encoding='utf-8').read()
    blobs = []

    def keep(m):
        blobs.append(m.group(0))
        return '@@BLOB_%d@@' % (len(blobs) - 1)

    skel = BLOB.sub(keep, src)
    os.makedirs(os.path.join(ROOT, 'work'), exist_ok=True)
    open(os.path.join(ROOT, 'work', game + '.bs.html'), 'w', encoding='utf-8').write(skel)
    json.dump(blobs, open(os.path.join(ROOT, 'work', game + '.blobs.json'), 'w'))
    print(f'{game}: {len(skel) // 1024}KB text, {len(blobs)} media blobs')


def fixed_image(game, n):
    path = os.path.join(ROOT, 'assets', 'fixed', f'{game}-bg-{n}.jpg')
    return path if os.path.exists(path) else None


def build(game):
    html = open(os.path.join(ROOT, 'work', game + '.en.html'), encoding='utf-8').read()
    blobs = json.load(open(os.path.join(ROOT, 'work', game + '.blobs.json')))
    for i, b in enumerate(blobs):
        fixed = fixed_image(game, i)
        if fixed:  # English version of a picture that had Bosnian text painted in (tools/fix_images.py)
            b = 'data:image/jpeg;base64,' + base64.b64encode(open(fixed, 'rb').read()).decode()
        tok = '@@BLOB_%d@@' % i
        assert html.count(tok) >= 1, f'missing {tok}'
        html = html.replace(tok, b)
    assert '@@BLOB_' not in html
    html = re.sub(r'<html([^>]*)lang="bs"', r'<html\1lang="en"', html, count=1)
    if '<div class="bz-brand">' not in html:  # the element itself, not just CSS that mentions it
        logo = base64.b64encode(open(os.path.join(ROOT, 'assets', 'logo-bz-erie-web.jpg'), 'rb').read()).decode()
        html = html.replace('</head>', BRAND_CSS + '</head>', 1)
        html = re.sub(r'(<body[^>]*>)', r'\1<div class="bz-brand"><img alt="Bosnian Islamic Community of Erie" '
                      r'src="data:image/jpeg;base64,' + logo + '"></div>', html, count=1)
    out = os.path.join(ROOT, 'games', game)
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
    print(f'built games/{game}/index.html ({len(html) // 1024}KB)')
    check(html)


BS_WORDS = re.compile(r"(?<![\w'’-])(" r'Rekić|Pripremio|Prepared by|\w*[čćžšđČĆŽŠĐ]\w*|je|su|se|na|za|od|da|sa|ili|ako|koji|koja|kako|nije|sve|svih|igra|igru|'
                      r'nova|pokusaj|pritisni|dodirni|pitanje|odgovor|bodovi|bodova|bod|zadatak|tacno|netacno|'
                      r'dalje|ponovo|pomoc|kraj|nivo|vrijeme|rezultat|meleki|kviz|znanja|pitanja|tacan|zivotinja|igrica)' r"(?![\w'’-])", re.I)


def check(html):
    """Report likely untranslated Bosnian words (ignores media, the author's name and Arabic transliteration fields)."""
    text = re.sub(r'data:[^"\')]+', '', html)
    hits = {}
    for m in BS_WORDS.finditer(text):
        ctx = text[max(0, m.start() - 30):m.end() + 30].replace('\n', ' ')
        hits.setdefault(m.group(0), ctx)
    for w, ctx in list(hits.items())[:25]:
        print(f'  ⚠ {w!r}: …{ctx}…')


if __name__ == '__main__':
    {'extract': extract, 'build': build}[sys.argv[1]](sys.argv[2])
