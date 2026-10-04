"""site.json is the one place with the mosque's name, logo and address: change it, run tools/build_site.py, and
no page may still show the old mosque. Runs on a temporary copy of the website (takes a few minutes)."""
import json
import os
import re
import shutil
import subprocess
import sys

import pytest

import gamecheck as gc

OLD = json.load(open(os.path.join(gc.ROOT, 'site.json'), encoding='utf-8'))
NEW = {'name': 'Islamic Center of Testville', 'short_name': 'IC Testville', 'logo': 'assets/test-logo.png',
       'url': 'https://testville-maktab.github.io/maktab/', 'contact': ''}


@pytest.fixture(scope='module')
def rebuilt(tmp_path_factory):
    dst = tmp_path_factory.mktemp('site') / 'maktab'
    keep = ['original', 'games', 'lessons', 'sufara', 'plan', 'duty', 'credits', 'assets', 'data', 'tools', 'supabase', 'index.html', 'site.json']
    for k in keep:
        src = os.path.join(gc.ROOT, k)
        (shutil.copytree(src, dst / k, ignore=shutil.ignore_patterns('__pycache__')) if os.path.isdir(src) else shutil.copy(src, dst / k))
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (800, 200), (20, 80, 140))
    ImageDraw.Draw(img).text((40, 80), 'Islamic Center of Testville', fill='white')
    img.save(dst / NEW['logo'])
    (dst / 'site.json').write_text(json.dumps(NEW))
    r = subprocess.run([sys.executable, 'tools/build_site.py'], cwd=dst, capture_output=True, text=True, timeout=1500)
    assert r.returncode == 0, r.stdout[-800:] + r.stderr[-1500:]
    return dst


def pages(root):
    for d in ['games', 'lessons', 'sufara', 'plan', 'duty', 'credits']:
        for dirpath, _, files in os.walk(root / d):
            for f in files:
                if f.endswith('.html'):
                    yield os.path.join(dirpath, f)
    yield str(root / 'index.html')


def test_no_page_shows_the_old_mosque(rebuilt):
    old_logo = open(os.path.join(gc.ROOT, OLD['logo']), 'rb').read()
    import base64
    old_b64 = base64.b64encode(old_logo).decode()[:200]
    bad = []
    for p in pages(rebuilt):
        s = open(p, encoding='utf-8').read()
        if p.endswith(os.path.join('credits', 'index.html')):   # names Erie on purpose, as the website's original makers
            s = s.replace(OLD['name'] + ', Pennsylvania', '').replace('github.com/rekicabdo-bihac', '')
        for needle in (OLD['name'], OLD['url'], 'ademdeniz', old_b64, os.path.basename(OLD['logo'])):
            if needle in s:
                bad.append((os.path.relpath(p, rebuilt), needle[:40]))
    assert not bad, bad[:15]


def test_every_page_shows_the_new_mosque(rebuilt):
    missing = [os.path.relpath(p, rebuilt) for p in pages(rebuilt) if NEW['name'] not in open(p, encoding='utf-8').read()]
    assert not missing, missing[:15]


def test_share_links_use_the_new_address(rebuilt):
    for p in [rebuilt / 'index.html', rebuilt / 'lessons' / 'index.html', rebuilt / 'sufara' / '06-ba' / 'index.html']:
        s = open(p, encoding='utf-8').read()
        if 'PUBLIC' in s or 'games/${' in s:
            assert NEW['url'] in s, p
