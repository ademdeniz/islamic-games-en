# podmornica-znanja-namaz: Abdo ef. Rekić's "Submarine of Knowledge – Salah": 20 questions, every right answer brings a
# treasure into the album (up to 500). The 472 Salah questions come from our kviz-namaz translation (_salah_bank.py).
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _salah_bank as SB  # noqa: E402
from _rekic_ui import page  # noqa: E402

GAME = 'podmornica-znanja-namaz'
EXTRA = [
    ('Podmornica znanja – 31 dragocjenost', 'Submarine of Knowledge'), ('🌊 PODMORNICA ZNANJA – NAMAZ', '🌊 SUBMARINE OF KNOWLEDGE – SALAH'), ('↩ Meni', '↩ Menu'),
    ('Otkrij blago morskog dna!', 'Discover the treasure of the sea floor!'), ('Žuta podmornica s djecom', 'A yellow submarine with children'),
    ('Odgovori i kreni u potragu!', 'Answer and start the hunt!'), ('🌊 Podmornica znanja', '🌊 Submarine of Knowledge'),
    ('💎 Potraga za blagom – Namaz', '💎 Treasure hunt – Salah'),
    ('20 pitanja • 20 novih dragocjenosti • Svaki tačan odgovor donosi blago u tvoj album. Pogrešan odgovor? Podmornica nastavlja do sljedećeg blaga!',
     '20 questions • 20 new treasures • Every right answer puts a treasure in your album. A wrong answer? The submarine goes on to the next treasure!'),
    ('📒 Album čuva do', '📒 The album keeps up to'), ('500 osvojenih dragocjenosti', '500 treasures you have won'),
    ('i između igranja na istom uređaju.', 'between games on the same device.'), ('▶ POKRENI IGRU', '▶ START THE GAME'), ('⬇ PREUZMI IGRICU', '⬇ DOWNLOAD THE GAME'),
    ('📒 Pogledaj album', '📒 See the album'), ('Okreni telefon vodoravno. Za puni ekran dodirni ⛶.', 'Turn the phone sideways. For full screen, tap ⛶.'),
    ('📒 MOJ ALBUM BLAGA', '📒 MY TREASURE ALBUM'), ('✕ Zatvori', '✕ Close'), ('U album stane 500 dragocjenosti.', 'The album holds 500 treasures.'),
    ('⬇ Sačuvaj album (JSON)', '⬇ Save the album (JSON)'), ('🏆 Završeno putovanje!', '🏆 Journey complete!'),
    ('Osvojeno blago je spremljeno u tvoj album.', 'The treasure you won is saved in your album.'), ('▶ Nova plovidba', '▶ New voyage'), ('📒 Moj album', '📒 My album'),
    ('Okreni telefon vodoravno da vidiš cijelo morsko dno i četiri odgovora u jednom redu.', 'Turn the phone sideways to see the whole sea floor and all four answers in one row.'),
    ('biserna ogrlica', 'pearl necklace'), ('zlatni pehar', 'golden cup'), ('carska tijara', 'royal tiara'), ('zlatni ključ', 'golden key'), ('broš', 'brooch'),
    ('zlatna narukvica', 'golden bracelet'), ('dragocjena školjka', 'precious shell'), ('smaragdni privjesak', 'emerald pendant'), ('kraljevsko žezlo', 'royal sceptre'),
    ('zlatna naušnica', 'golden earring'), ('škrinjica blaga', 'treasure chest'), ('Osvojio/la si ', 'You won '), (' od 20 dragocjenosti!', ' of 20 treasures!'),
    ('Čestitamo na završenoj plovidbi!', 'Congratulations on finishing the voyage!'), ('Pronađi ', 'Find the '),
    ('✨ Tačno! Blago je u podmornici!', '✨ Correct! The treasure is in the submarine!'), ('🌊 Nastavi do sljedećeg blaga!', '🌊 On to the next treasure!'),
    ('Odaberi Pokreni ili Preuzmi igricu', 'Choose Start or Download the game'), ('Podmornica_znanja_31_dragocjenost.html', 'Submarine_of_Knowledge.html'),
    ('Album blaga – Podmornica znanja', 'Treasure album – Submarine of Knowledge'),
]
DELETE, ALLOW_ARABIC, _base, BRAND_FIT = page(GAME, EXTRA)
ALLOW_ARABIC = []


def transform(src):
    key = 'const BANK='
    i = src.index(key) + len(key)
    bank, n = json.JSONDecoder().raw_decode(src[i:])
    for x in bank:
        x['q'], x['a'], x['topic'] = SB.english(x['q']), [SB.english(o) for o in x['a']], SB.english(x['topic'])
        assert len(set(x['a'])) == len(x['a']), x
    return _base(src[:i] + json.dumps(bank, ensure_ascii=False) + src[i + n:])
