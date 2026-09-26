"""Download data for "Learn the Surahs by Heart" (games/learn-surahs-by-heart) into data/hifz.json.

Per ayah: Arabic words (Uthmani) with per-word transliteration, English meaning (Sahih International),
and per-ayah audio with per-word timings for two reciters. Sources: Quran.com API v4, AlQuran.cloud.
Longer ayahs are split into memorisation "parts" at pause marks (see split_parts).

  python3 tools/fetch_hifz.py
"""
import json
import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QC = 'https://api.quran.com/api/v4'
RECITERS = {'alafasy': {'id': 7, 'name': 'Mishary Alafasy', 'base': 'https://verses.quran.com/'},
            'husary': {'id': 12, 'name': 'Husary – teaching (slow)', 'base': ''}}
# (id, title, surah, first ayah, last ayah, bismillah line before it) – in learning order, shortest first
SURAHS = [
    ('fatiha', 'Al-Fatiha', 1, 1, 7, False),
    ('nas', 'An-Nas', 114, 1, 6, True),
    ('falaq', 'Al-Falaq', 113, 1, 5, True),
    ('ikhlas', 'Al-Ikhlas', 112, 1, 4, True),
    ('masad', 'Al-Masad (Al-Lahab)', 111, 1, 5, True),
    ('nasr', 'An-Nasr', 110, 1, 3, True),
    ('kafirun', 'Al-Kafirun', 109, 1, 6, True),
    ('kawthar', 'Al-Kawthar', 108, 1, 3, True),
    ('maun', "Al-Ma'un", 107, 1, 7, True),
    ('quraysh', 'Quraysh', 106, 1, 4, True),
    ('fil', 'Al-Fil', 105, 1, 5, True),
    ('humazah', 'Al-Humazah', 104, 1, 9, True),
    ('asr', "Al-'Asr", 103, 1, 3, True),
    ('takathur', 'At-Takathur', 102, 1, 8, True),
    ('qariah', "Al-Qari'ah", 101, 1, 11, True),
    ('alif-lam-mim', 'Alif-Lam-Mim (Al-Baqarah 1–5)', 2, 1, 5, True),
    ('kursi', 'Ayat al-Kursi (Al-Baqarah 255)', 2, 255, 255, False),
]
PAUSE = re.compile('[ۖ-ۜ]')  # Qur'anic pause marks (waqf signs) – natural places to split an ayah


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'islamic-games-en/1.0'})
    return json.load(urllib.request.urlopen(req, timeout=60))


def audio_url(rec, url):
    return 'https:' + url if url.startswith('//') else url if url.startswith('http') else rec['base'] + url


def split_parts(words, target=4):
    """Split an ayah's words into parts of ~target words, preferring to break right after a pause mark."""
    if len(words) <= target + 2:
        return [[0, len(words)]]
    parts, start = [], 0
    while start < len(words):
        if len(words) - start <= target + 2:
            parts.append([start, len(words)])
            break
        best = None
        for end in range(start + 3, min(start + target + 5, len(words)) + 1):   # parts of 3..target+4 words
            if PAUSE.search(words[end - 1]):
                best = end if best is None or abs(end - start - target) < abs(best - start - target) else best
        end = best or start + target
        if len(words) - end < 2:            # don't leave a 1-word tail
            end = len(words)
        parts.append([start, end])
        start = end
    return parts


KID_FRIENDLY = str.maketrans({'ā': 'aa', 'ī': 'ee', 'ū': 'oo', 'Ā': 'Aa', 'Ī': 'Ee', 'Ū': 'Oo', 'ḥ': 'h', 'Ḥ': 'H',
                              'ṣ': 's', 'Ṣ': 'S', 'ḍ': 'd', 'Ḍ': 'D', 'ṭ': 't', 'Ṭ': 'T', 'ẓ': 'z', 'Ẓ': 'Z', 'ʿ': '‘'})
SUN = r'(th|dh|sh|t|d|r|z|s|l|n)'  # sun letters: the "l" of "al-" is not pronounced before them


def kid_tr(t):
    """Scholarly transliteration (ḥ, ā, ʿ) -> the simpler style kids know from the Fatiha game (h, aa, ‘)."""
    t = t.translate(KID_FRIENDLY)
    t = re.sub(r"(?<=[a-z])'(?=[a-z])", '', t)                  # Quran.com's syllable marks: bis'mi -> bismi
    t = re.sub(r'(^|-)l-(?=' + SUN + ')', lambda m: m.group(1) + '@', t)  # mark "l-" before a sun letter
    t = re.sub(r'@' + SUN, lambda m: m.group(1) + '-' + m.group(1), t)   # l-rahmaan -> r-rahmaan
    return t.replace('al-laahu', 'Allaahu').replace('al-lahu', 'Allahu')


def pausal(word):
    """How the last word of an ayah is recited when stopping: final short vowel / nunation dropped."""
    for full, stop in (('atan', 'ah'), ('atun', 'ah'), ('atin', 'ah'), ('ata', 'ah'), ('atu', 'ah'), ('ati', 'ah')):
        if word.endswith(full) and len(word) > len(full) + 1:
            return word[:-len(full)] + stop
    if word.endswith('an') and not word.endswith('aan'):
        return word[:-2] + 'aa'
    if word[-2:] in ('un', 'in') and word[-3:] not in ('oon', 'een'):
        return word[:-2]
    if word[-1:] in 'aiu' and word[-2:] not in ('aa', 'ee', 'oo') and len(word) > 2:
        return word[:-1]
    return word


def ayah(key):
    v = get(f'{QC}/verses/by_key/{key}?words=true&word_fields=text_uthmani')['verse']
    ws = [w for w in v['words'] if w['char_type_name'] == 'word']
    end = [w['text_uthmani'] for w in v['words'] if w['char_type_name'] == 'end']
    en = get(f'https://api.alquran.cloud/v1/ayah/{key}/en.sahih')['data']['text']
    words = [w['text_uthmani'] for w in ws]
    out = {'key': key, 'n': int(key.split(':')[1]), 'words': words,
           'wtr': [kid_tr((w.get('transliteration') or {}).get('text') or '') for w in ws],
           'end': end[0] if end else '', 'en': en, 'parts': split_parts(words), 'audio': {}}
    if out['wtr']:
        out['wtr'][-1] = pausal(out['wtr'][-1])
    for rid, rec in RECITERS.items():
        a = get(f'{QC}/recitations/{rec["id"]}/by_ayah/{key}?fields=segments')['audio_files'][0]
        segs = []
        for s in a.get('segments') or []:
            pos, t0, t1 = (s[1], s[2], s[3]) if len(s) == 4 else (s[0], s[1], s[2])
            assert 1 <= pos <= len(words), f'{key} {rid}: timing for word {pos} of {len(words)}'
            segs.append([pos - 1, t0, t1])
        assert segs, f'{key} {rid}: no word timings'
        out['audio'][rid] = {'url': audio_url(rec, a['url']), 'segments': segs}
    return out


def main():
    bismillah = ayah('1:1')
    bismillah.update(n=0, en='In the name of Allah, the Entirely Merciful, the Especially Merciful.', end='')
    data = {'reciters': {k: v['name'] for k, v in RECITERS.items()}, 'surahs': []}
    for sid, title, s, a0, a1, bism in SURAHS:
        lines = ([bismillah] if bism else []) + [ayah(f'{s}:{n}') for n in range(a0, a1 + 1)]
        data['surahs'].append({'id': sid, 'title': title, 'lines': lines})
        print(f'{title}: {len(lines)} lines, {sum(len(l["parts"]) for l in lines)} parts')
    path = os.path.join(ROOT, 'data', 'hifz.json')
    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('wrote', path, os.path.getsize(path) // 1024, 'KB')


if __name__ == '__main__':
    main()
