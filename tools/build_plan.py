"""Build the yearly Sunday class plan.

  python3 tools/build_plan.py                      # plan/index.html – read-only copy for parents (public site)
  python3 tools/build_plan.py --private out.html   # + the teacher's tracker (ticks, notes, "No class" switches;
                                                   #   published as a private claude.ai page with the db capability)
  --no-class 2027-01-03,...   extra Sundays without class (the parents' copy has no switches, so bake them in here)
"""
import datetime as dt
import glob
import json
import os
import re
import sys


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from plan_curriculum import FALLBACK, GAMES, ILMIHAL, SITE  # noqa: E402
idx = open(os.path.join(ROOT, 'sufara', 'index.html'), encoding='utf-8').read()
SUF = json.loads(re.search(r'const D=(\{.*?\});\n', idx, re.S).group(1))['pages']

START, END = dt.date(2026, 9, 27), dt.date(2027, 6, 6)
SUNDAYS = [START + dt.timedelta(weeks=k) for k in range((END - START).days // 7 + 1)]
NO_CLASS = json.load(open(os.path.join(ROOT, 'data', 'plan', 'no_class.json'), encoding='utf-8'))   # Sundays without class
EVENTS = {   # approximate Islamic dates 1448 AH, shown on the Sunday of that week
    '2026-12-06': 'Laylat al-Raghaib ~Thu Dec 10',
    '2027-01-03': 'Isra & Mi‘raj ~Tue Jan 5',
    '2027-01-24': 'Laylat al-Bara’ah ~Sun Jan 24',
    '2027-02-07': 'Ramadan starts ~Mon Feb 8',
    '2027-02-14': 'Ramadan', '2027-02-21': 'Ramadan', '2027-02-28': 'Ramadan',
    '2027-03-07': 'Laylat al-Qadr ~Fri Mar 5 · Eid al-Fitr ~Wed Mar 10',
    '2027-05-16': 'Eid al-Adha ~Sun May 16',
    '2027-06-06': 'Islamic New Year 1449 ~Sat Jun 5',
}
EVENT_GAMES = {'Ramadan': ['ramazanski-put'], 'Laylat': ['oslobodi-papagaja'], 'Isra': ['oslobodi-papagaja'], 'Eid': ['oslobodi-papagaja', 'ramazanski-put']}

TAJWID = [   # (rule, what the lesson covers)
    ('Tajwid intro – why we recite beautifully', 'what tajwid is, makharij (where letters come from)'),
    ('Heavy and light letters (tafkhim & tarqiq)', 'خ ص ض غ ط ق ظ are always heavy'),
    ('Ghunnah – nun and mim with shaddah', 'نّ مّ held 2 counts through the nose'),
    ('Nun sakinah & tanwin: Izhar', 'clear before ء ه ع ح غ خ'),
    ('Nun sakinah & tanwin: Idgham with ghunnah', 'merge into ي ن م و (يَنمُو)'),
    ('Nun sakinah & tanwin: Idgham without ghunnah', 'merge into ل ر'),
    ('Nun sakinah & tanwin: Iqlab', 'turns into mim before ب'),
    ('Nun sakinah & tanwin: Ikhfa', 'hidden before the other 15 letters'),
    ('Review: the four rules of nun sakinah & tanwin', 'sort Qur’an examples into Izhar, Idgham, Iqlab, Ikhfa'),
    ('Mim sakinah: Ikhfa shafawi, Idgham shafawi, Izhar shafawi', 'مْ before ب, before م, and before the rest'),
    ('Qalqalah', 'bouncing ق ط ب ج د (قُطْبُ جَدٍّ)'),
    ('Lam in “Allah” – heavy or light', 'heavy after fatha/damma, light after kasra'),
    ('Ra – heavy or light', 'when ر is heavy and when light'),
    ('Al- : sun and moon letters', 'lam shamsiyyah and lam qamariyyah'),
    ('Madd tabi‘i – natural lengthening', 'ا و ي lengthened 2 counts'),
    ('Madd muttasil & munfasil', 'madd followed by hamza – same word or next word'),
    ('Madd lazim and madd ‘arid', 'long madd (6 counts) and madd when stopping'),
    ('Stopping signs (waqf)', 'مـ لا ج صلى قلى and how to stop on a word'),
    ('Review: Tajwid in Al-Baqarah', 'find the rules on the mushaf pages we read'),
]


def built_lessons():
    """(book, book page) -> lesson url, for every page a built lesson covers (data/lessons/ilmihal-N/*.json)."""
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'data', 'lessons', 'ilmihal-*', '*.json'))):
        book, lid = int(f.split(os.sep)[-2].split('-')[1]), os.path.basename(f)[:-5]
        first, _, last = json.load(open(f, encoding='utf-8'))['pages'].partition('–')
        for pg in range(int(first), int(last or first) + 1):
            out.setdefault((book, pg), f'{SITE}lessons/ilmihal-{book}/{lid}/')
    return out


HIFZ_IDS = {s['id'] for s in json.load(open(os.path.join(ROOT, 'data', 'hifz.json'), encoding='utf-8'))['surahs']}
SURAH_WORDS = {'Fatiha': 'fatiha', 'An-Nasr': 'nasr', 'An-Nas': 'nas', 'Falaq': 'falaq', 'Ikhlas': 'ikhlas', 'Masad': 'masad',
               'Kafirun': 'kafirun', 'Kawthar': 'kawthar', 'Ma‘un': 'maun', 'Quraysh': 'quraysh', 'Al-Fil': 'fil',
               'Humazah': 'humazah', '‘Asr': 'asr', 'Takathur': 'takathur', 'Qari‘ah': 'qariah', 'Alif-Lam-Mim': 'alif-lam-mim',
               'Ayat al-Kursi': 'kursi'}


def surah_link(title):
    """Surah lessons are learned in “Learn the Surahs by Heart” – link straight to that surah."""
    for word, sid in SURAH_WORDS.items():
        if word in title and sid in HIFZ_IDS:
            return f'{SITE}games/learn-surahs-by-heart/#{sid}'


def lesson_items(book):
    built, out = built_lessons(), []
    for e in ILMIHAL[book]:
        page, title, topics = e[:3]
        url = built.get((book, page)) or surah_link(title)
        out.append({'k': f'i{book}-{page}', 'kind': f'Ilmihal {book}', 'title': title, 'page': page, 'topics': sorted(topics),
                    'url': url, **({'hint': 'practise it in Learn the Surahs by Heart'} if url and '#' in url else {})})
    return out


def sufara_items():
    return [{'k': 'sf-' + p['id'], 'kind': 'Sufara', 'title': (f"{p['name']} {p['ch']}" if p['kind'] == 'letter' else p['title']),
             'sub': p['kind'], 'url': SITE + 'sufara/' + p['id'] + '/', 'topics': []} for p in SUF]


def quran_items(n):
    built = {2, 3, 4, 5}
    return [{'k': f'q-{pg}', 'kind': 'Qur’an', 'title': f'Al-Baqarah – mushaf page {pg}', 'page': pg, 'topics': ['quran'],
             'url': SITE + 'games/citaj-kuran/' if pg in built else None,
             'hint': 'Read Along → pick this page' if pg in built else 'Read Along page to build'} for pg in range(2, 2 + n)]


def reading_items(n):
    out = [dict(it, k='g1' + it['k']) for it in sufara_items()]   # Group 1 also starts from Alif; own ticks
    return out


def tajwid_items():
    return [{'k': f'tj-{i}', 'kind': 'Tajwid', 'title': t, 'hint': h, 'url': None, 'topics': ['tajwid']} for i, (t, h) in enumerate(TAJWID)]


data = {
    'site': SITE, 'sundays': [d.isoformat() for d in SUNDAYS], 'noClass': NO_CLASS, 'starts': {'tj': '2026-11-01'}, 'standing': [{'from': '2026-11-01', 'text': 'Maktab competition preparation (schedule TBD)'}], 'events': EVENTS, 'eventGames': EVENT_GAMES,
    'games': {s: {'t': t, 'topics': sorted(tp)} for s, (t, tp) in GAMES.items()}, 'fallback': FALLBACK,
    'tracks': {
        'i1': lesson_items(1), 'sf': sufara_items(), 'i2': lesson_items(2), 'i3': lesson_items(3),
        'qr': quran_items(len(SUNDAYS)), 'rd': reading_items(0), 'tj': tajwid_items(),
    },
}
G1 = [('i2', 'Ilmihal 2'), ('i3', 'Ilmihal 3'), ('qr', 'Qur’an'), ('rd', 'Sufara'), ('tj', 'Tajwid')]
G2 = [('i1', 'Ilmihal 1'), ('sf', 'Sufara')]
BOOKS = {'g1': [2, 3], 'g2': [1]}


def class_days(no_class=None):
    off = NO_CLASS if no_class is None else no_class
    return [d for d in data['sundays'] if d not in off]


def schedule(no_class=None):
    """Which items each class covers: {date: {track: [(item, continued)]}} – the same as schedule() in the page."""
    cls, plan = class_days(no_class), {}
    for d in cls:
        plan[d] = {}
    for t, items in data['tracks'].items():
        n, st = len(items), data['starts'].get(t)
        days = [d for d in cls if not st or d >= st]
        for d in cls:
            plan[d][t] = []
        if t == 'qr':
            for w, d in enumerate(days):
                plan[d][t] = [(items[w], False)]
            continue
        m = len(days)
        if n >= m:
            for w, d in enumerate(days):
                plan[d][t] = [(it, False) for it in items[w * n // m:(w + 1) * n // m]]
        else:
            prev = -1
            for w, d in enumerate(days):
                i = w * n // m
                plan[d][t] = [(items[i], i == prev)]
                prev = i
    return plan


def games_for(entries, d, w, books):
    """Matching games for one group's class – the same as gamesFor() in the page."""
    topics = {p for it, _ in entries for p in it['topics']}
    score = {s: len(set(g['topics']) & topics) for s, g in data['games'].items() if set(g['topics']) & topics}
    ev = data['events'].get(d, '')
    for k, gs in data['eventGames'].items():
        if k in ev:
            for s in gs:
                score[s] = score.get(s, 0) + 5
    out = sorted(score, key=lambda s: (-score[s], s))[:4]
    if len(out) < 2:
        for b in books:
            f = data['fallback'][b]
            s = f[w % len(f)]
            if s not in out:
                out.append(s)
            if len(out) >= 3:
                break
    return out


TEXT = {
    False: {'__TITLE__': 'Maktab Year Plan', '__H1__': 'Maktab Year Plan 2026–27',
            '__SUB__': 'Bosnian Islamic Community of Erie · every Sunday from Sep 27 to early June. Tick lessons when you teach them. '
                       'Mark a Sunday “No class” and the plan moves everything forward.',
            '__FOOT__': 'Islamic dates are approximate (moon sighting). Qur’an: Read Along has Al-Baqarah pages 2–5; the pages marked '
                        '“to build” come next. Tajwid topics are placeholders until their lessons exist. Items marked “continued” carry on '
                        'from the week before.'},
    True: {'__TITLE__': 'Maktab Class Plan', '__H1__': 'Maktab Class Plan 2026–27',
           '__SUB__': 'Bosnian Islamic Community of Erie · what each group learns every Sunday, from Sep 27 to early June. '
                      'Tap a lesson or a game to practise together at home. 📰 <a href="../updates/">Weekly updates</a>',
           '__FOOT__': 'Group 1: Ilmihal 2 & 3, Qur’an (Al-Baqarah), Sufara and Tajwid. Group 2: Ilmihal 1 and Sufara. '
                       'Dates of Islamic holidays are approximate, and the plan may change during the year. '
                       'Items marked “continued” carry on from the week before.'},
}


def page(readonly):
    d = dict(data, readonly=readonly)
    out = open(os.path.join(ROOT, 'tools', 'templates', 'plan.html'), encoding='utf-8').read()
    for k, v in TEXT[readonly].items():
        out = out.replace(k, v)
    return out.replace('__DATA__', json.dumps(d, ensure_ascii=False).replace('</', '<\\/'))


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--private')
    ap.add_argument('--no-class', default='')
    args = ap.parse_args()
    for day in filter(None, args.no_class.split(',')):
        data['noClass'][day] = 'No class'
    from build_lessons_core import brand
    os.makedirs(os.path.join(ROOT, 'plan'), exist_ok=True)
    open(os.path.join(ROOT, 'plan', 'index.html'), 'w', encoding='utf-8').write(brand(page(True)))
    if args.private:
        open(args.private, 'w', encoding='utf-8').write(page(False))
    print({k: len(v) for k, v in data['tracks'].items()}, len(SUNDAYS), 'Sundays')
