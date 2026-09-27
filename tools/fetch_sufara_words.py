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
    return MARKS.sub('', word).translate(ALIFS).strip()   # (a pause mark leaves a space behind)


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


def rule_examples():
    """Resolve the reading-rule examples (data/sufara/rules.json) to exact Qur'an text and audio. Two or more words are
    played as one clip from the ayah's recitation (Mishary Alafasy), so kids hear how the words join."""
    rules = json.load(open(os.path.join(ROOT, 'data', 'sufara', 'rules.json'), encoding='utf-8'))['rules']
    out = {}
    for r in rules:
        items = []
        for ex in r['examples']:
            v = get(f"{API}/verses/by_key/{ex['key']}?words=true&word_fields=text_uthmani,audio_url")['verse']
            ws = [w for w in v['words'] if w['char_type_name'] == 'word']
            want = [bare(x) for x in ex['words']]
            start = next(i for i in range(len(ws)) if [bare(w['text_uthmani']) for w in ws[i:i + len(want)]] == want)
            chosen = ws[start:start + len(want)]
            item = {'ar': ' '.join(re.sub(r'\s*[\u06D6-\u06ED]+$', '', w['text_uthmani']).strip() for w in chosen),
                    'tr': ex['read'], 'en': ' '.join(w['translation']['text'].strip() for w in chosen), 'key': ex['key']}
            if len(chosen) == 1:
                item['audio'] = 'https://audio.qurancdn.com/' + chosen[0]['audio_url']
            else:
                a = get(f"{API}/recitations/7/by_ayah/{ex['key']}?fields=segments")['audio_files'][0]
                segs = {s[1] if len(s) == 4 else s[0]: s[-2:] for s in a['segments']}
                first, last = chosen[0]['position'], chosen[-1]['position']
                item.update(audio='https://verses.quran.com/' + a['url'], clip=[segs[first][0], segs[last][1]])
            items.append(item)
        out[r['slug']] = items
        print(f"{r['name']:18}: " + ' · '.join(f"{i['ar']} ({i['tr']}){' [clip]' if 'clip' in i else ''}" for i in items))
    json.dump(out, open(os.path.join(ROOT, 'data', 'sufara', 'rule_examples.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


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
    rule_examples()
