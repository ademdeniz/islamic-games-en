"""Shared helpers for pages built from tools/templates/lesson.html (Sufara, Ilmihal lessons)."""
import base64
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import skel  # noqa: E402

import site_settings  # noqa: E402


def brand(page):
    """Add the community logo header (same as every game)."""
    page = page.replace('</head>', skel.BRAND_CSS + '</head>', 1)
    page = page.replace('__SITE_URL__', site_settings.URL)
    return re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + site_settings.brand_html(), page, count=1)
