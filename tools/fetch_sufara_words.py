"""Pick Qur'an example words for every Sufara letter -> data/sufara/words.json

Words come from surahs kids know (Al-Fatiha, the short surahs, Al-Baqarah 1–5 and Ayat al-Kursi), with each word's
own recitation audio and English meaning from Quran.com (word-by-word). Words that START with the letter are
preferred; if a letter never starts a word there, words that begin with "al-" + the letter, then words that just
contain it, are used.

  python3 tools/fetch_sufara_words.py
"""
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_hifz import kid_tr  # noqa: E402  (same kid-friendly transliteration as Learn the Surahs by Heart)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = 'https://api.quran.com/api/v4'
SOURCES = [(1, None), (112, None), (113, None), (114, None), (111, None), (110, None), (109, None), (108, None),
           (107, None), (106, None), (105, None), (104, None), (103, None), (102, None), (101, None),
           (2, range(1, 6)), (2, [255]), (36, range(1, 13))]
PER_LETTER = 3
MARKS = re.compile('[ً-ٰٟۖ-ۭـ]')
ALIFS = str.maketrans({'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ٱ': 'ا'})


def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'islamic-games-en/1.0'}), timeout=30))


def bare(word):
    return MARKS.sub('', word).translate(ALIFS)


def words():
    for surah, ayahs in SOURCES:
        page = 1
        while True:
            d = get(f'{API}/verses/by_chapter/{surah}?words=true&word_fields=text_uthmani,audio_url&per_page=50&page={page}')
            for v in d['verses']:
                if ayahs is not None and v['verse_number'] not in ayahs:
                    continue
                for w in v['words']:
                    if w['char_type_name'] == 'word' and w.get('audio_url'):
                        yield {'ar': re.sub(r'\s*[\u06D6-\u06ED]+$', '', w['text_uthmani']).strip(), 'en': w['translation']['text'], 'tr': kid_tr(w['transliteration']['text'] or ''),
                               'key': v['verse_key'], 'pos': w['position'],
                               'audio': 'https://audio.qurancdn.com/' + w['audio_url']}
            if not d['pagination'].get('next_page'):
                break
            page += 1


def main():
    letters = json.load(open(os.path.join(ROOT, 'data', 'sufara', 'letters.json'), encoding='utf-8'))['letters']
    pool = list(words())
    out = {}
    for L in letters:
        ch = bare(L['ch'])
        seen, picked = set(), []
        for how, test in (('starts', lambda b: b.startswith(ch) and not b.startswith('ال')),
                          ('al', lambda b: b.startswith('ال' + ch)),
                          ('contains', lambda b: ch in b)):
            for w in pool:
                b = bare(w['ar'])
                if len(picked) < PER_LETTER and b not in seen and test(b):
                    seen.add(b)
                    picked.append(dict(w, how=how))
        out[L['slug']] = picked
        print(f"{L['name']:6} {L['ch']}: " + ' · '.join(f"{w['ar']} ({w['how']})" for w in picked))
    json.dump(out, open(os.path.join(ROOT, 'data', 'sufara', 'words.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
