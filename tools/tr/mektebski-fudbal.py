# Mektebski fudbal -> Maktab Football (two players, one phone). The question bank is the shared
# Ilmihal bank, translated by _ilmihal_bank.translate(); UI strings below.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

DELETE = ['Pripremio Abdo ef. Rekić • Džemat Turija–Vrsta • Medžlis IZ Bihać<br>']

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>Mektebski fudbal</title>', '<title>Maktab Football</title>'),
    ('⚽ MEKTEBSKI FUDBAL 🏆', '⚽ MAKTAB FOOTBALL 🏆'),
    ('Znanje donosi golove • Dva igrača • Jedan telefon', 'Knowledge scores goals • Two players • One phone'),
    ('⚙️ Priprema utakmice', '⚙️ Match setup'),
    ('🔵 Igrač 1<input id="name1" maxlength="22" value="Igrač 1">', '🔵 Player 1<input id="name1" maxlength="22" value="Player 1">'),
    ('🔴 Igrač 2<input id="name2" maxlength="22" value="Igrač 2">', '🔴 Player 2<input id="name2" maxlength="22" value="Player 2">'),
    ('<b>Odaberi nivo pitanja</b>', '<b>Choose the question level</b>'),
    ('Penala po igraču<select', 'Penalties per player<select'),
    ('>5 penala<', '>5 penalties<'), ('>10 penala<', '>10 penalties<'), ('>15 penala<', '>15 penalties<'), ('>20 penala<', '>20 penalties<'),
    ('Zvuk<select', 'Sound<select'), ('Uključen 🔊', 'On 🔊'), ('Isključen 🔇', 'Off 🔇'),
    ('Svaki igrač naizmjenično odgovara. Tačan odgovor = gol; netačan = odbrana golmana. Pitanja se ne ponavljaju u utakmici.',
     'Players take turns to answer. Right answer = goal; wrong answer = the goalkeeper saves it. No question comes up twice in a match.'),
    ('⚽ ZAPOČNI UTAKMICU', '⚽ START THE MATCH'),
    ('<span id="p1">Igrač 1</span>', '<span id="p1">Player 1</span>'),
    ('<span id="p2">Igrač 2</span>', '<span id="p2">Player 2</span>'),
    ('🔁 NOVA UTAKMICA', '🔁 NEW MATCH'), ('⚙️ PROMIJENI POSTAVKE', '⚙️ CHANGE SETTINGS'),
    ('⬇️ PREUZMI HTML IGRU', '⬇️ DOWNLOAD THE GAME'),
    ('Radi na Androidu i iPhoneu • Igra radi i bez interneta', 'Works on Android and iPhone • Works without the internet'),
    ("'SVI NIV0I'", "'ALL LEVELS'"),
    ("names=['Igrač 1','Igrač 2']", "names=['Player 1','Player 2']"),
    ("$('name1').value.trim()||'Igrač 1',$('name2').value.trim()||'Igrač 2'", "$('name1').value.trim()||'Player 1',$('name2').value.trim()||'Player 2'"),
    ("alert('Nema dovoljno pitanja za izabranu utakmicu.')", "alert('There are not enough questions for this match.')"),
    ("+' izvodi penal '+n+' od '+rounds", "+' takes penalty '+n+' of '+rounds"),
    ("'Pitanje '+(step+1)+' / '+deck.length+' • Nivo '+deck[step].l", "'Question '+(step+1)+' / '+deck.length+' • Level '+deck[step].l"),
    ("names[p]+' – penal '+(i+1)", "names[p]+' – penalty '+(i+1)"),
    ("'⚽ GOOOL! Bravo, '+names[who]+'!'", "'⚽ GOOOAL! Well done, '+names[who]+'!'"),
    ("'⚽ GOOOL!'", "'⚽ GOOOAL!'"),
    ("'🧤 Golman brani! Tačan odgovor je: '+q.a[q.c]", "'🧤 The goalkeeper saves it! The right answer is: '+q.a[q.c]"),
    ("'🧤 ODBRANA!'", "'🧤 SAVED!'"),
    ("'🤝 NERIJEŠENO!':'🏆 POBJEDNIK: '", "'🤝 IT’S A DRAW!':'🏆 WINNER: '"),
    ("+rounds+' penala po igraču'", "+rounds+' penalties per player'"),
    ("'Utakmica je završena!'", "'The match is over!'"),
    ("'KRAJ UTAKMICE'", "'FULL TIME'"),
    ("a.download='mektebski-fudbal.html'", "a.download='maktab-football.html'"),
]


def transform(src):
    return _ilmihal_bank.translate(src)
