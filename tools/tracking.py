"""Add the maktab tracker (tools/tracking.js) to a children's page: lessons, Sufara, Read Along, Learn the Surahs.

The tracker uses our Supabase project from supabase/config.json. With no project there (the clean starter), pages get
no tracker at all. Database: supabase/tracking.sql · dashboard: teacher/.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def script():
    try:
        cfg = json.load(open(os.path.join(ROOT, 'supabase', 'config.json'), encoding='utf-8'))
    except (OSError, ValueError):
        return ''
    if not cfg.get('url') or not cfg.get('publishable_key'):
        return ''
    js = open(os.path.join(ROOT, 'tools', 'tracking.js'), encoding='utf-8').read()
    js = js.replace('__URL__', cfg['url']).replace('__KEY__', cfg['publishable_key'])
    return '<script>\n' + js + '</script>'


def add(page):
    """Put the tracker just before </body> (after the page's own scripts)."""
    tag = script()
    if not tag:
        return page
    i = page.rfind('</body>')
    return page[:i] + tag + page[i:] if i >= 0 else page + tag
