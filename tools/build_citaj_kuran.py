"""Build games/citaj-kuran/index.html (Read Along with the Reciter) from tools/templates/citaj-kuran.html + data/readalong.json.

The Bosnian original only had Al-Baqarah 17–24 with Arabic typed in by hand; this version uses verified Arabic from
Quran.com, highlights each word while it is recited (word timings from Quran.com), has Normal/Slower/Slowest speed and a
slow teaching reciter, and more pages (add them in tools/fetch_readalong.py).

  python3 tools/fetch_readalong.py   # only when adding pages
  python3 tools/build_citaj_kuran.py
"""
import base64
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import skel  # noqa: E402



def build(game, data_file):
    """Template tools/templates/<game>.html + data/<data_file> (as __DATA__) + logo header -> games/<game>/index.html"""
    html = open(os.path.join(ROOT, 'tools', 'templates', game + '.html'), encoding='utf-8').read()
    data = json.load(open(os.path.join(ROOT, 'data', data_file), encoding='utf-8'))
    html = html.replace('__DATA__', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'), 1)
    logo = base64.b64encode(open(os.path.join(ROOT, 'assets', 'logo-bz-erie-web.jpg'), 'rb').read()).decode()
    html = html.replace('</head>', skel.BRAND_CSS + '</head>', 1)
    html = re.sub(r'(<body[^>]*>)', r'\1<div class="bz-brand"><img alt="Bosnian Islamic Community of Erie" '
                  r'src="data:image/jpeg;base64,' + logo + '"></div>', html, count=1)
    out = os.path.join(ROOT, 'games', game, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(html)
    print('built', out, len(html) // 1024, 'KB')
    return data


if __name__ == '__main__':
    build('citaj-kuran', 'readalong.json')
