"""Build games/learn-surahs-by-heart/index.html from tools/templates/learn-surahs-by-heart.html + data/hifz.json.

  python3 tools/fetch_hifz.py   # only when changing the surah list
  python3 tools/build_hifz.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_citaj_kuran import build  # noqa: E402

data = build('learn-surahs-by-heart', 'hifz.json')
print(len(data['surahs']), 'surahs,', sum(len(l['parts']) for s in data['surahs'] for l in s['lines']), 'parts')
