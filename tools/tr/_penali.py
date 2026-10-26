"""Shared table for Abdo ef. Rekić's "BiH – Penalties & album" games (penali A1–A3, penali2 B1–B3, penali-n Salah,
penali-t tajwid): the same game with a different QUESTION_BANKS. Answer right = goal; 5 goals win a card of a Bosnia
and Herzegovina national team player for the album. The questions come from our translated banks."""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank as IB  # noqa: E402
import _salah_bank as SB  # noqa: E402
import _tajwid_bank as TB  # noqa: E402
from _rekic_ui import page  # noqa: E402

UI = [
    ('BiH – Penali i album', 'BiH – Penalties & Album'), ('📱 Okreni telefon vodoravno za igru', '📱 Turn the phone sideways to play'),
    ('🇧🇦 PENALI BiH', '🇧🇦 PENALTIES BiH'), ('⚽ Pogodci 0/5 · 🧤 Promašaji 0/5 · 📒 Album 0', '⚽ Goals 0/5 · 🧤 Misses 0/5 · 📒 Album 0'),
    ('⚽ Pogodci 0 · 🧤 Promašaji 0 · 📒 Album 0', '⚽ Goals 0 · 🧤 Misses 0 · 📒 Album 0'),
    ('⚽ Pogodci 0/5 · 🧤 Promašaji 0/10 · 📒 Album 0', '⚽ Goals 0/5 · 🧤 Misses 0/10 · 📒 Album 0'),
    ('📒 Album', '📒 Album'), ('Izaberi stranu, odgovori na pitanje i šutiraj!', 'Choose a side, answer the question and shoot!'),
    ('⬅️ Lijevo', '⬅️ Left'), ('⬆️ Sredina', '⬆️ Middle'), ('Desno ➡️', 'Right ➡️'), ('Nastavi igru ⚽', 'Continue ⚽'), ('Nova serija', 'New round'),
    ('📚 Pitanje ', '📚 Question '), (' · Tačno = GOL, netačno = odbrana', ' · Right = GOAL, wrong = save'),
    ('⚽ Pogodci ', '⚽ Goals '), ('/5 · 🧤 Promašaji ', '/5 · 🧤 Misses '), (' · 🧤 Promašaji ', ' · 🧤 Misses '), ('/5 · 📒 Album ', '/5 · 📒 Album '),
    ('/10 · 📒 Album ', '/10 · 📒 Album '), ('⚽ GOOOL! ', '⚽ GOOOAL! '), ('🎉 Osvojena nova kartica!', '🎉 You won a new card!'),
    ('🏆 Album je popunjen!', '🏆 The album is full!'), ('🧤 Odbrana! Promašaji ', '🧤 Saved! Misses '),
    ('💔 10 promašaja! Izgubljena sličica: ', '💔 10 misses! Card lost: '), ('🧤 10 promašaja! Album je prazan.', '🧤 10 misses! The album is empty.'),
    ('📒 Album reprezentativaca BiH', '📒 Album of the Bosnia and Herzegovina team'),
    ('" alt="Fotografija igrača" style="width:100%;height:100%;object-fit:contain;border-radius:12px">',
     '" alt="Photo of the player" style="width:100%;height:100%;object-fit:contain;border-radius:12px">'),
    ('Još nema osvojenih kartica', 'No cards won yet'), ('Kolekcionarska sličica reprezentativca Bosne i Hercegovine.', 'A collector’s card of a Bosnia and Herzegovina national team player.'),
    ('Postigni 5 golova za novu sličicu. Nakon 10 promašaja gubiš jednu sličicu!', 'Score 5 goals for a new card. After 10 misses you lose one card!'),
    (' slika', ' cards'), ('0 slika', '0 cards'), ('Nova serija: postigni 5 golova!', 'New round: score 5 goals!'),
    # the Salah version (10 penalties a round)
    ('Rezultati deset penala', 'Results of the ten penalties'), ('📚 NAMAZ · Tačno = GOL, netačno = odbrana', '📚 SALAH · Right = GOAL, wrong = save'),
    ('Nova serija: 10 penala!', 'New round: 10 penalties!'), (' – Osvojena nova slika!', ' – You won a new card!'), (' – Album je popunjen!', ' – The album is full!'),
    ('Izgubljena slika: ', 'Card lost: '), ('Album je prazan.', 'The album is empty.'), ('🤝 5:5 – NERIJEŠENO! Album ostaje isti.', '🤝 5:5 – A DRAW! The album stays the same.'),
    (' pogodaka', ' goals'), ('🧤 Odbrana! ', '🧤 Saved! '), (' promašaja', ' misses'),
    ('Od 10 penala: 6+ pogodaka osvaja sliku, 6+ promašaja gubi sliku, 5:5 je neriješeno.', 'Out of 10 penalties: 6+ goals win a card, 6+ misses lose a card, 5:5 is a draw.'),
]
# the players on the cards keep their names
PLAYERS = ['Muharemović', 'Kolašinac', 'Memić', 'Alajbegović', 'Mahmić', 'Bajraktarević', 'Džeko', 'Demirović', 'Tabaković', 'Baždar',
           'Lukić', 'Hasić', 'Šunjić', 'Gigović', 'Bašić', 'Hamzić', 'Mujakić', 'Dedić']


def _english(bank_name, q, opts):
    if bank_name == 'NAMAZ':
        return SB.english(q), [SB.english(o) for o in opts]
    if bank_name == 'TEDZVID':
        return TB.english_q(q), [TB.english_opt(o) for o in opts]
    return IB.english(q, opts)   # Ilmihal levels A1–B3


def setup(game):
    DELETE, _a, base, BRAND_FIT = page(game, UI)

    def transform(src):
        key = 'const QUESTION_BANKS='
        i = src.index(key) + len(key)
        banks, n = json.JSONDecoder().raw_decode(src[i:])
        for name, items in banks.items():
            for x in items:
                x['q'], x['a'] = _english(name, x['q'], x['a'])
                assert len(set(x['a'])) == len(x['a']), ('two answers the same in English', x)
        return base(src[:i] + json.dumps(banks, ensure_ascii=False, separators=(',', ':')) + src[i + n:])
    return DELETE, BRAND_FIT, transform
