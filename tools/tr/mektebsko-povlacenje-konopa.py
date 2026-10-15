# Mektebsko povlačenje konopa -> Maktab Tug of War (two players, one phone). Shared Ilmihal question bank
# (_ilmihal_bank.translate); UI strings below.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

DELETE = ['<p>Pripremio Abdo ef. Rekić · Turija–Vrsta</p>']

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>Mektebsko povlačenje konopa</title>', '<title>Maktab Tug of War</title>'),
    ('<h1>🪢 Mektebsko povlačenje konopa</h1>', '<h1>🪢 Maktab Tug of War</h1>'),
    ('<input id="p1" value="Igrač 1" aria-label="Ime prvog igrača">', '<input id="p1" value="Player 1" aria-label="First player’s name">'),
    ('<input id="p2" value="Igrač 2" aria-label="Ime drugog igrača">', '<input id="p2" value="Player 2" aria-label="Second player’s name">'),
    ('<label>Nivo <select id="level"><option value="ALL">Svi nivoi A1–B3</option>', '<label>Level <select id="level"><option value="ALL">All levels A1–B3</option>'),
    ('<label>Rundi po igraču <select', '<label>Rounds per player <select'),
    ('▶ Započni igru', '▶ Start the game'),
    ('<span id="s1">🔵 Igrač 1: 0</span><span id="s2">🔴 Igrač 2: 0</span>', '<span id="s1">🔵 Player 1: 0</span><span id="s2">🔴 Player 2: 0</span>'),
    ('aria-label="Prikaz konopa"', 'aria-label="The rope"'),
    ('<span>🔵 Lijeva ekipa</span><span id="progress">Čeka početak</span><span>Desna ekipa 🔴</span>',
     '<span>🔵 Left team</span><span id="progress">Waiting to start</span><span>Right team 🔴</span>'),
    ('Odaberite nivo i pritisnite Započni', 'Choose a level and press Start'),
    ('Ko će pobijediti u povlačenju konopa?', 'Who will win the tug of war?'),
    ('<button class="minor" id="sound">🔊 Zvuk uključen</button>', '<button class="minor" id="sound">🔊 Sound on</button>'),
    ('⬇ Preuzmi HTML', '⬇ Download the game'), ('↻ Nova igra', '↻ New game'),
    ('Tačan odgovor: konop se pomjera na tvoju stranu. Netačan odgovor: konop ostaje na mjestu. Igrači se smjenjuju automatski. Pobjeđuje prvi koji povuče zastavicu do svoje strane ili onaj s više bodova nakon svih rundi.',
     'Right answer: the rope moves to your side. Wrong answer: the rope stays where it is. Players take turns automatically. The winner is the first to pull the flag to their side – or whoever has more points after all the rounds.'),
    ("names=['Igrač 1','Igrač 2']", "names=['Player 1','Player 2']"),
    ("+ 'Na potezu: '+names[turn]+' · nivo '+q.l", "+ 'Your turn: '+names[turn]+' · level '+q.l"),
    ("+' / '+limit+' rundi'", "+' / '+limit+' rounds'"),
    ("'✅ Tačno! Konop ide na tvoju stranu.'", "'✅ Correct! The rope moves to your side.'"),
    ("'❌ Netačno! Tačan odgovor je označen zeleno.'", "'❌ Wrong! The right answer is shown in green.'"),
    ("'🤝 Neriješeno!'", "'🤝 It’s a draw!'"),
    ("+'🏆 Pobijedio je '+names[winner]+'!'", "+'🏆 The winner is '+names[winner]+'!'"),
    ("'🏁 Igra završena'", "'🏁 Game over'"),
    ("'Rezultat: '+names[0]", "'Result: '+names[0]"),
    ("$('progress').textContent='Kraj'", "$('progress').textContent='The end'"),
    ("$('p1').value.trim()||'Igrač 1',$('p2').value.trim()||'Igrač 2'", "$('p1').value.trim()||'Player 1',$('p2').value.trim()||'Player 2'"),
    ("alert('Nema dovoljno pitanja za ovaj izbor.')", "alert('There are not enough questions for this choice.')"),
    ("'Odaberite opcije za novu igru'", "'Choose the options for a new game'"),
    ("'Spremni za novu igru'", "'Ready for a new game'"),
    ("audio?'🔊 Zvuk uključen':'🔇 Zvuk isključen'", "audio?'🔊 Sound on':'🔇 Sound off'"),
    ("a.download='mektebsko-povlacenje-konopa.html'", "a.download='maktab-tug-of-war.html'"),
    ("'Ugrađeno '+BANK.length+' pitanja iz originalnih baza. Radi i bez interneta.'", "'Built in: '+BANK.length+' Ilmihal questions. Works without the internet.'"),
]


def transform(src):
    return _ilmihal_bank.translate(src)
