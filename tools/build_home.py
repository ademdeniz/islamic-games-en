"""Build the home page: tools/templates/home.html -> index.html, with the mosque's name, logo and address
from site.json. Edit the list of games (SECTIONS) in the template, then run:

  python3 tools/build_home.py
"""
import html
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import site_settings  # noqa: E402


def build():
    page = open(os.path.join(ROOT, 'tools', 'templates', 'home.html'), encoding='utf-8').read()
    page = (page.replace('__SITE_NAME__', html.escape(site_settings.NAME))
                .replace('__LOGO__', site_settings.LOGO).replace('__SITE_URL__', site_settings.URL))
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(page)
    print('built index.html')


if __name__ == '__main__':
    build()
