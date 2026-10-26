# kviz-tedzvid: Abdo ef. Rekić's tajwid "Millionaire" quiz (365 questions). The question bank is translated through
# _tajwid_bank.py (templates + answers); the lesson names are the filter keys, so the menu and the bank change together.
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _tajwid_bank as TB  # noqa: E402
from _rekic_ui import page  # noqa: E402

GAME = 'kviz-tedzvid'
EXTRA = [
    ('Tedžvid Milijunaš', 'Tajwid Millionaire'), ('Tedžvidska pravila – Milijunaš', 'Tajwid Rules – Millionaire'), ('🏆 TEDŽVIDSKA PRAVILA', '🏆 TAJWID RULES'),
    ('Milijunaš', 'Millionaire'), ('Odaberi oblast', 'Choose a topic'), ('Sve oblasti – 365 pitanja', 'All topics – 365 questions'),
    *TB.LESSONS.items(),
    ('15 nasumičnih pitanja • pitanja se svaki put miješaju • tačan odgovor mijenja mjesto A–D', '15 random questions • shuffled every time • the right answer moves between A–D'),
    ('📱 Prilagođeno za Android i iPhone', '📱 Made for Android and iPhone'), ('▶ Pokreni igru', '▶ Start the game'), ('Bodovi: 0', 'Points: 0'),
    ('👥 Publika', '👥 Audience'), ('🔄 Zamijeni', '🔄 Swap'), ('Tedžvidska pravila • Pripremio Abdo ef. Rekić', 'Tajwid rules'),
    ('bs-BA', 'en-US'), ('Pitanje ', 'Question '), ('Bodovi: ', 'Points: '), ('✓ Tačno! +10 bodova', '✓ Correct! +10 points'),
    ('✗ Netačno. +0 bodova', '✗ Not quite. +0 points'), ('<h2>🏆 Kviz završen!</h2><p>Tačnih odgovora: <b>', '<h2>🏆 Quiz finished!</h2><p>Right answers: <b>'),
    ('</b></p><p>Ukupno bodova: <b>', '</b></p><p>Points in total: <b>'),
    ('</b></p><button class="btn" onclick="back()">Nova igra</button>', '</b></p><button class="btn" onclick="back()">New game</button>'),
    ('Tedzvidska_pravila_Milijunas_Abdo_ef_Rekic.html', 'Tajwid_Rules_Millionaire.html'), ('Publika: ', 'Audience: '),
]
DELETE, _ARABIC, _base, BRAND_FIT = page(GAME, EXTRA)
ALLOW_ARABIC = ['tajwid questions – the Arabic letters and Qur’an examples are what is being asked']
ALLOW = ['Sve']   # value of the "all topics" choice, compared in the code (v==="Sve"); the child sees "All topics"


def transform(src):
    i = src.index('const BANK=') + len('const BANK=')
    j = i + len(src[i:]) - len(src[i:].lstrip())
    bank, n = json.JSONDecoder().raw_decode(src[j:])
    for b in bank:
        b['lesson'] = TB.LESSONS[b['lesson']]
        b['q'] = TB.english_q(b['q'])
        b['opts'] = [TB.english_opt(o) for o in b['opts']]
        b['correct'] = TB.english_opt(b['correct'])
        assert b['correct'] in b['opts']
    return _base(src[:j] + json.dumps(bank, ensure_ascii=False) + src[j + n:])
