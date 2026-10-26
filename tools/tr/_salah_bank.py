"""The Salah (namaz) question bank, Bosnian → English, as translated for kviz-namaz (tools/tr/kviz-namaz_en*.txt, one
line per unique string of that game's bank, in order of first appearance). Abdo ef. Rekić reuses the same 472 questions
in newer games (the Salah penalty game, the submarine) – english(s) gives the English of one question or answer."""
import glob
import json
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))


def _load():
    d = os.path.join(_ROOT, 'original', 'kviz-namaz')
    main = [f for f in os.listdir(d) if f.endswith('.html')][0]
    src = open(os.path.join(d, main), encoding='utf-8').read()
    i = src.index('const BANK=') + len('const BANK=')
    bank, _ = json.JSONDecoder().raw_decode(src[i:])
    seen = []
    for x in bank:
        for t in [x['q']] + x['options'] + [x['correctText']]:
            if t not in seen:
                seen.append(t)
    tr = {}
    for f in sorted(glob.glob(os.path.join(_HERE, 'kviz-namaz_en*.txt'))):
        for line in open(f, encoding='utf-8'):
            line = line.rstrip('\n')
            if line:
                k, en = line.split('\t', 1)
                tr[int(k)] = en.replace('\\n', '\n')
    return {bs: tr[k] for k, bs in enumerate(seen)}


MAP = _load()
# questions the newer copies added (the submarine and the Salah penalty game), and the submarine's topic names
MAP.update({
    'Koji je prvi namaski šart?': 'What is the first condition of Salah?', 'Koji je drugi namaski šart?': 'What is the second condition of Salah?',
    'Koji je treći namaski šart?': 'What is the third condition of Salah?', 'Koji je četvrti namaski šart?': 'What is the fourth condition of Salah?',
    'Koji je peti namaski šart?': 'What is the fifth condition of Salah?', 'Koji je šesti namaski šart?': 'What is the sixth condition of Salah?',
    'Šta je gusul?': 'What is Ghusl?', 'Šta su namaski šarti?': 'What are the conditions of Salah?', 'Šta je ezan?': 'What is the Adhan?',
    'Kada učimo zikr poslije namaza?': 'When do we say the dhikr after Salah?', 'Kada klanjamo sabah-namaz?': 'When do we pray Fajr?',
    'Koji je po redu dnevni namaz podne-namaz?': 'Which of the daily prayers is Dhuhr – first, second…?',
    'Koji je po redu dnevni namaz ikindija-namaz?': 'Which of the daily prayers is Asr – first, second…?',
    'Koji je namaz večernji namaz?': 'Which prayer is the evening prayer?',
    'Šta je farz?': 'What is fard?', 'Koji je po redu dnevni namaz jacija-namaz?': 'Which of the daily prayers is Isha – first, second…?',
    'Šta se uči na prvom rekatu farza dnevnih namaza?': 'What do we recite in the first rak‘ah of the fard of the daily prayers?',
    'Kojih dana mjeseca ševvala se obilježava Ramazanski bajram?': 'On which days of the month of Shawwal is Eid al-Fitr?',
    'Namaz': 'Salah', 'ABDEST': 'WUDU', 'TEJEMUM': 'TAYAMMUM', 'MESH PO MESTVAMA I ZAVOJU': 'WIPING OVER SOCKS (KHUFFS) AND BANDAGES',
    'NAMASKI ŠARTI – UVJETI I PRIPREME ZA NAMAZ': 'CONDITIONS OF SALAH – GETTING READY TO PRAY', 'PROPISNO ODIJEVANJE ZA NAMAZ': 'DRESSING PROPERLY FOR SALAH',
    'NAMASKA VREMENA I DNEVNI NAMAZI': 'PRAYER TIMES AND THE DAILY PRAYERS', 'KIBLA I KABA': 'THE QIBLAH AND THE KA’BAH', 'EZAN I IKAMET': 'ADHAN AND IQAMAH',
    'NAMASKI RUKNOVI – SASTAVNI DIJELOVI NAMAZA': 'ARKAN – THE PARTS OF SALAH', 'ZIKR POSLIJE NAMAZA': 'DHIKR AFTER SALAH', 'SABAH-NAMAZ': 'FAJR',
    'PODNE-NAMAZ': 'DHUHR', 'IKINDIJA-NAMAZ': 'ASR', 'AKŠAM-NAMAZ': 'MAGHRIB', 'FARZ I SUNNET': 'FARD AND SUNNAH', 'JACIJA-NAMAZ I VITR-NAMAZ': 'ISHA AND WITR',
    'UČENJE I REDOSLIJED PO REKATIMA': 'WHAT WE RECITE IN EACH RAK‘AH', 'RAMAZANSKI I KURBAN-BAJRAM': 'EID AL-FITR AND EID AL-ADHA',
})


def english(s):
    s2 = re.sub(r'\s*✅\s*$', '', s)
    assert s2 in MAP, f'not in the Salah bank: {s!r}'
    return MAP[s2]
