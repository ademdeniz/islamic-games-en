"""Build the Sufara (Arabic letters) section: sufara/<NN-letter>/ for each letter, sufara/review-<n>/ after every
7 letters, and sufara/index.html. Uses the lesson page design (tools/templates/lesson.html).

  python3 tools/fetch_sufara_words.py   # only when the letter list changes
  python3 tools/build_sufara.py
"""
import html
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from build_lessons_core import brand  # noqa: E402

DATA = json.load(open(os.path.join(ROOT, 'data', 'sufara', 'letters.json'), encoding='utf-8'))
LETTERS = DATA['letters']
WORDS = json.load(open(os.path.join(ROOT, 'data', 'sufara', 'words.json'), encoding='utf-8'))
HEAVY = set('خصضغطقظ')   # the "full mouth" (isti‘la) letters
FOOTER = ('Letter names and sounds explained for English-speaking children. Qur’an words, their recitation and '
          'meanings: Quran.com. Videos: the “Sufara” playlist by Amsal Memic, with hfz. Nermin Spahić (YouTube).')
HAS_LESSONS = os.path.isdir(os.path.join(ROOT, 'data', 'lessons'))   # the Lessons section exists on this branch
SITE = {'root': '../../', 'section': 'sufara', 'lessons_link': HAS_LESSONS}
TEMPLATE = open(os.path.join(ROOT, 'tools', 'templates', 'lesson.html'), encoding='utf-8').read()


def forms(L):
    c = L['ch']
    if L['joins']:
        return [['Alone', c], ['Start', c + 'ـ'], ['Middle', 'ـ' + c + 'ـ'], ['End', 'ـ' + c]]
    return [['Alone', c], ['Start', c], ['Middle', 'ـ' + c], ['End', 'ـ' + c]]


def bare(w):
    import re
    return re.sub('[ً-ٰٟۖ-ۭـ]', '', w).translate(str.maketrans('أإآٱ', 'اااا'))


def page_id(n, L):
    return f'{n:02d}-{L["slug"]}'


def letter_lesson(n, L):
    rnd = random.Random(n)   # same "random" layout every build
    words = WORDS[L['slug']]
    others = [w for s, ws in WORDS.items() if s != L['slug'] for w in ws if bare(L['ch']) not in bare(w['ar'])]
    cells = [L['ch']] * 5 + [rnd.choice(L['similar']) for _ in range(11)]
    rnd.shuffle(cells)
    questions = [{'q': f'Which one is the letter {L["name"]}?', 'options': [L['ch']] + L['similar'][:3], 'answer': 0}]
    for w in words:
        verb = 'starts with' if w['how'] == 'starts' else 'has'
        opts = [w['ar']] + [o['ar'] for o in rnd.sample(others, 3)]
        questions.append({'q': f'Which word {verb} {L["name"]} ({L["ch"]})?', 'options': opts, 'answer': 0})
    harakat_q = rnd.randrange(3)
    ar, tr = L['harakat'][harakat_q]
    questions.append({'q': f'How do we read {ar}?', 'options': [h[1] for h in L['harakat']], 'answer': harakat_q})
    return {
        'book': 'sufara', 'id': page_id(n, L), 'number': n, 'title': f'{L["name"]}  {L["ch"]}',
        'tag': f'Sufara • Letter {n} of {len(LETTERS)}', 'intro': L['tip'],
        'crumbs': [['🏠 Home', '../../'], ['🔤 Sufara', '../'], [L['name'], None]], 'footer': FOOTER, **SITE,
        'learn': [
            {'type': 'letter', 'ch': L['ch'], 'name': L['name'], 'bs': L['bs'], 'forms': forms(L), 'joins': L['joins']},
            {'type': 'tip', 'html': html.escape(L['tip'])},
            {'type': 'heading', 'text': 'Read it with the short vowels'},
            {'type': 'harakat', 'items': L['harakat']},
            {'type': 'heading', 'text': f'Qur’an words with {L["name"]} – tap to listen'},
            {'type': 'words', 'items': words},
            {'type': 'video', 'id': L['video'], 'title': f'Watch the video: {L["bs"]}',
             'note': ' – from the Sufara playlist by Amsal Memic, with hfz. Nermin Spahić (opens YouTube)'},
        ],
        'practice': [
            {'type': 'find', 'title': f'Find {L["name"]}', 'prompt': f'Tap every {L["name"]} ({L["ch"]}).', 'target': L['ch'], 'cells': cells},
            {'type': 'quiz', 'title': 'Quick quiz', 'questions': questions},
        ],
    }


def review_lesson(k, group, first):
    rnd = random.Random(100 + k)
    qs = []
    for L in group:
        wrong = rnd.sample([x['ch'] for x in group if x is not L], 3)
        qs.append({'q': f'Which one is {L["name"]}?', 'options': [L['ch']] + wrong, 'answer': 0})
    last = first + len(group) - 1
    practice = [
        {'type': 'memory', 'title': 'Match the letter and its name', 'pairs': [[L['ch'], L['name']] for L in group]},
        {'type': 'quiz', 'title': 'Which letter is it?', 'questions': qs},
        {'type': 'sort', 'title': 'Does it join the next letter?', 'prompt': 'Some letters never join to the letter after them.',
         'bins': ['Joins', 'Never joins'], 'items': [{'text': L['ch'], 'bin': 0 if L['joins'] else 1} for L in group]},
    ]
    if {L['ch'] in HEAVY for L in group} == {True, False}:
        practice.append({'type': 'sort', 'title': 'Heavy or light?', 'prompt': 'Heavy letters are said with a full, deep mouth.',
                         'bins': ['Heavy', 'Light'], 'items': [{'text': L['ch'], 'bin': 0 if L['ch'] in HEAVY else 1} for L in group]})
    if len({L['joins'] for L in group}) == 1:   # the joins sort needs both kinds
        practice = [a for a in practice if a['title'] != 'Does it join the next letter?']
    return {
        'book': 'sufara', 'id': f'review-{k}', 'number': k, 'title': f'Review {k}: letters {first}–{last}',
        'tag': f'Sufara • Review {k}', 'intro': '  '.join(L['ch'] for L in group),
        'crumbs': [['🏠 Home', '../../'], ['🔤 Sufara', '../'], [f'Review {k}', None]], 'footer': FOOTER, **SITE,
        'learn': [{'type': 'text', 'html': 'Let’s practise the letters you have learned: ' +
                   ', '.join(f'<b>{L["name"]}</b> <span class="arq">{L["ch"]}</span>' for L in group) + '.'}],
        'practice': practice,
    }


def write(lesson, prev, nxt):
    lesson['prev'] = prev and {'id': prev['id'], 'title': prev['title']}
    lesson['next'] = nxt and {'id': nxt['id'], 'title': nxt['title']}
    page = (TEMPLATE.replace('__TITLE__', html.escape(f"{lesson['title'].strip()} – Sufara"))
            .replace('__DATA__', json.dumps(lesson, ensure_ascii=False).replace('</', '<\\/')))
    out = os.path.join(ROOT, 'sufara', lesson['id'], 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(brand(page))


def build():
    pages = []
    for n, L in enumerate(LETTERS, 1):
        pages.append(letter_lesson(n, L))
        if n % 7 == 0:
            pages.append(review_lesson(n // 7, LETTERS[n - 7:n], n - 6))
    for k, p in enumerate(pages):
        write(p, pages[k - 1] if k else None, pages[k + 1] if k + 1 < len(pages) else None)
    summary = [{'id': p['id'], 'kind': 'review' if p['id'].startswith('review') else 'letter', 'title': p['title'],
                'ch': LETTERS[p['number'] - 1]['ch'] if not p['id'].startswith('review') else '',
                'name': LETTERS[p['number'] - 1]['name'] if not p['id'].startswith('review') else p['title'],
                'activities': sum(a['type'] != 'reflect' for a in p['practice'])} for p in pages]
    index = open(os.path.join(ROOT, 'tools', 'templates', 'sufara-index.html'), encoding='utf-8').read()
    index = index.replace('__LESSONS__', '<a href="../lessons/">📚 Lessons</a>' if HAS_LESSONS else '')
    index = index.replace('__DATA__', json.dumps({'pages': summary, 'playlist': DATA['playlist']}, ensure_ascii=False))
    open(os.path.join(ROOT, 'sufara', 'index.html'), 'w', encoding='utf-8').write(brand(index))
    print(f'built {sum(s["kind"] == "letter" for s in summary)} letters, {sum(s["kind"] == "review" for s in summary)} reviews + sufara/index.html')


if __name__ == '__main__':
    build()
