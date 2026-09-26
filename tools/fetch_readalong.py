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
# Pages of the standard 604-page Madani mushaf. The ayahs on each page come from Quran.com (verses/by_page), so they
# can't be mistyped; `surah` keeps only that surah's ayahs (page 440 also holds the last ayah of Fatir).
# A Bismillah line is added when the page starts a surah (except Al-Fatiha, where it is ayah 1).
PAGES = [
    {'id': 'baqarah-p2', 'title': 'Al-Baqarah – page 2', 'mushaf_page': 2, 'surah': 2},
    {'id': 'baqarah-p3', 'title': 'Al-Baqarah – page 3', 'mushaf_page': 3, 'surah': 2},
    {'id': 'baqarah-17-24', 'title': 'Al-Baqarah – page 4', 'mushaf_page': 4, 'surah': 2},
    {'id': 'baqarah-p5', 'title': 'Al-Baqarah – page 5', 'mushaf_page': 5, 'surah': 2},
    {'id': 'yasin-1-12', 'title': 'Ya-Sin – page 440', 'mushaf_page': 440, 'surah': 36},
]


def page_keys(p):
    vs = get(f'{QURAN_COM}/verses/by_page/{p["mushaf_page"]}?per_page=50')['verses']
    return [v['verse_key'] for v in vs if int(v['verse_key'].split(':')[0]) == p['surah']]


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
        keys = page_keys(p)
        first, last = keys[0].split(':')[1], keys[-1].split(':')[1]
        page = dict(p, ayahs=f'{first}–{last}' if first != last else first, lines=[])
        if keys[0].endswith(':1') and p['surah'] != 1:
            b = ayah('1:1')
            b.update(n=0, en='In the name of Allah, the Entirely Merciful, the Especially Merciful.', end='')
            page['lines'].append(b)
        for key in keys:
            page['lines'].append(ayah(key))
        print(f"{page['title']}: ayahs {page['ayahs']}, {len(page['lines'])} lines")
        data['pages'].append(page)
    path = os.path.join(ROOT, 'data', 'readalong.json')
    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', path)


if __name__ == '__main__':
    main()
