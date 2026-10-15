"""The mosque's own details, in one place: site.json (name, short name, logo, website address, contact).

Every builder reads them from here, so another mosque changes site.json (and its logo file) and runs
  python3 tools/build_site.py
to put its own name, logo and address on every page.
"""
import base64
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_S = json.load(open(os.path.join(ROOT, 'site.json'), encoding='utf-8'))

NAME = _S['name']                     # "Bosnian Islamic Community of Erie"
SHORT = _S.get('short_name', NAME)
URL = _S['url'].rstrip('/') + '/'     # the public address; every "Copy link" uses it
LOGO = _S['logo']                     # path of the logo file, relative to the repository
CONTACT = _S.get('contact', '')


def logo_data_uri():
    path = os.path.join(ROOT, LOGO)
    mime = 'image/png' if path.lower().endswith('.png') else 'image/svg+xml' if path.lower().endswith('.svg') else 'image/jpeg'
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def brand_html():
    """The logo header shown at the top of every game and lesson."""
    return f'<div class="bz-brand"><img alt="{NAME}" src="{logo_data_uri()}"></div>'
