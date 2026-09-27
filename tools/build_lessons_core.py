"""Shared helpers for pages built from tools/templates/lesson.html (Sufara, Ilmihal lessons)."""
import base64
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import skel  # noqa: E402

LOGO = base64.b64encode(open(os.path.join(ROOT, 'assets', 'logo-bz-erie-web.jpg'), 'rb').read()).decode()


def brand(page):
    """Add the community logo header (same as every game)."""
    page = page.replace('</head>', skel.BRAND_CSS + '</head>', 1)
    return re.sub(r'(<body[^>]*>)', r'\1<div class="bz-brand"><img alt="Bosnian Islamic Community of Erie" '
                  r'src="data:image/jpeg;base64,' + LOGO + '"></div>', page, count=1)
