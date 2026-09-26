"""Download the data for the Read Along game (games/citaj-kuran) into data/readalong.json.

Arabic words (Uthmani), per-word audio timings for two reciters: Quran.com API v4.
English meaning (Sahih International) and transliteration: AlQuran.cloud.
Add a page by adding an entry to PAGES and re-running:  python3 tools/fetch_readalong.py
"""
import json
import os
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QURAN_COM = 'https://api.quran.com/api/v4'
RECITERS = {  # Quran.com recitation id -> how we show it
    'alafasy': {'id': 7, 'name': 'Mishary Alafasy', 'base': 'https://verses.quran.com/'},
    'husary': {'id': 12, 'name': 'Husary – teaching (slow)', 'base': ''},
}
PAGES = [
    {'id': 'baqarah-17-24', 'title': 'Al-Baqarah 17–24', 'mushaf_page': 4, 'surah': 2, 'ayahs': range(17, 25)},
    {'id': 'yasin-1-12', 'title': 'Ya-Sin 1–12', 'mushaf_page': 440, 'surah': 36, 'ayahs': range(1, 13), 'bismillah': True},
]


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'islamic-games-en/1.0'})
    return json.load(urllib.request.urlopen(req, timeout=30))


def audio_url(rec, url):
    if url.startswith('//'):
        return 'https:' + url
    return url if url.startswith('http') else rec['base'] + url


def ayah(key):
    v = get(f'{QURAN_COM}/verses/by_key/{key}?words=true&word_fields=text_uthmani')['verse']
    words = [w['text_uthmani'] for w in v['words'] if w['char_type_name'] == 'word']
    end = [w['text_uthmani'] for w in v['words'] if w['char_type_name'] == 'end']
    tr, en = [e['text'] for e in get(f'https://api.alquran.cloud/v1/ayah/{key}/editions/en.transliteration,en.sahih')['data']]
    out = {'key': key, 'n': int(key.split(':')[1]), 'words': words, 'end': end[0] if end else '', 'tr': tr, 'en': en, 'audio': {}}
    for rid, rec in RECITERS.items():
        a = get(f'{QURAN_COM}/recitations/{rec["id"]}/by_ayah/{key}?fields=segments')['audio_files'][0]
        segs = []
        for s in a.get('segments') or []:
            pos, start, stop = (s[1], s[2], s[3]) if len(s) == 4 else (s[0], s[1], s[2])
            assert 1 <= pos <= len(words), f'{key} {rid}: timing for word {pos} but only {len(words)} words'
            segs.append([pos - 1, start, stop])  # 0-based word index, ms from, ms to
        out['audio'][rid] = {'url': audio_url(rec, a['url']), 'segments': segs}
    return out


def main():
    data = {'reciters': {k: v['name'] for k, v in RECITERS.items()}, 'pages': []}
    for p in PAGES:
        page = {k: v for k, v in p.items() if k not in ('ayahs', 'bismillah')}
        page['lines'] = []
        if p.get('bismillah'):
            b = ayah('1:1')
            b.update(n=0, en='In the name of Allah, the Entirely Merciful, the Especially Merciful.', end='')
            page['lines'].append(b)
        for n in p['ayahs']:
            page['lines'].append(ayah(f"{p['surah']}:{n}"))
            print(page['title'], n, len(page['lines'][-1]['words']), 'words')
        data['pages'].append(page)
    path = os.path.join(ROOT, 'data', 'readalong.json')
    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', path)


if __name__ == '__main__':
    main()
