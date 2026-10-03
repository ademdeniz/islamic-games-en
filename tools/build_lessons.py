"""Build the Ilmihal lesson pages: data/lessons/<book>/<NN-id>.json -> lessons/<book>/<NN-id>/index.html,
plus lessons/index.html (all books and their lessons).

  python3 tools/build_lessons.py

A lesson file has: number, title, pages, intro, learn[...] (phrase, text, heading, quran, list, cards, point) and
practice[...] (order, choose_all, quiz, memory, sort, reflect) – see tools/templates/lesson.html.
"""
import glob
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import skel  # noqa: E402

from build_lessons_core import brand  # noqa: E402  (same logo header as every page)


def load_all():
    books = json.load(open(os.path.join(ROOT, 'data', 'lessons', 'books.json'), encoding='utf-8'))
    for bid, book in books.items():
        book['lessons'] = []
        for f in sorted(glob.glob(os.path.join(ROOT, 'data', 'lessons', bid, '*.json'))):
            lesson = json.load(open(f, encoding='utf-8'))
            lesson.update(id=os.path.basename(f)[:-5], book=bid, book_title=book['title'], source=book['source'],
                          root='../../../', section='lessons', lessons_link=True)
            book['lessons'].append(lesson)
        for k, lesson in enumerate(book['lessons'], 1):   # lessons are numbered in book order: files are named by
            lesson['number'] = k                          # book page (14-…, 17-…), so a lesson added later slots in
    return books


def build():
    books = load_all()
    template = open(os.path.join(ROOT, 'tools', 'templates', 'lesson.html'), encoding='utf-8').read()
    count = 0
    for bid, book in books.items():
        ls = book['lessons']
        for k, lesson in enumerate(ls):
            lesson['prev'] = {'id': ls[k - 1]['id'], 'title': ls[k - 1]['title']} if k else None
            lesson['next'] = {'id': ls[k + 1]['id'], 'title': ls[k + 1]['title']} if k + 1 < len(ls) else None
            page = (template.replace('__TITLE__', html.escape(f"{lesson['title']} – {book['title']}"))
                    .replace('__BOOK__', html.escape(book['title']))
                    .replace('__DATA__', json.dumps(lesson, ensure_ascii=False).replace('</', '<\\/')))
            out = os.path.join(ROOT, 'lessons', bid, lesson['id'], 'index.html')
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, 'w', encoding='utf-8').write(brand(page))
            count += 1
    index = open(os.path.join(ROOT, 'tools', 'templates', 'lessons-index.html'), encoding='utf-8').read()
    summary = {bid: {k: b[k] for k in ('title', 'level', 'icon', 'source')} |
               {'lessons': [{'id': l['id'], 'number': l['number'], 'title': l['title'], 'intro': l['intro'],
                             'activities': sum(a['type'] != 'reflect' for a in l['practice'])} for l in b['lessons']]}
               for bid, b in books.items()}
    open(os.path.join(ROOT, 'lessons', 'index.html'), 'w', encoding='utf-8').write(
        brand(index.replace('__DATA__', json.dumps(summary, ensure_ascii=False).replace('</', '<\\/'))))
    print(f'built {count} lessons in {len(books)} books + lessons/index.html')


if __name__ == '__main__':
    build()
