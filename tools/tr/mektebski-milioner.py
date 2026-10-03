# Mektebski milioner – izazov za dvoje -> Maktab Millionaire for Two (two players, one phone).
# Shared Ilmihal question bank (_ilmihal_bank.translate); UI strings below.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

DELETE = ['Pripremio Abdo ef. Rekić • Džemat Turija–Vrsta<br>']

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>Mektebski milioner – izazov za dvoje</title>', '<title>Maktab Millionaire for Two</title>'),
    ('🏆 MEKTEBSKI MILIONER', '🏆 MAKTAB MILLIONAIRE'),
    ('Izazov za dvoje • A1', 'A challenge for two • A1'),
    ('<strong id="name0">Igrač 1</strong>', '<strong id="name0">Player 1</strong>'),
    ('<strong id="name1">Igrač 2</strong>', '<strong id="name1">Player 2</strong>'),
    ('<span id="round0" class="small">0/10 odgovora</span>', '<span id="round0" class="small">0/10 answers</span>'),
    ('<span id="round1" class="small">0/10 odgovora</span>', '<span id="round1" class="small">0/10 answers</span>'),
    ('🎮 Pripremite se za igru!', '🎮 Get ready to play!'),
    ('<label>Ime prvog igrača<input id="input0" maxlength="22" value="Igrač 1">', '<label>First player’s name<input id="input0" maxlength="22" value="Player 1">'),
    ('<label>Ime drugog igrača<input id="input1" maxlength="22" value="Igrač 2">', '<label>Second player’s name<input id="input1" maxlength="22" value="Player 2">'),
    ('<label>Broj pitanja po igraču<select', '<label>Questions per player<select'),
    ('>10 pitanja<', '>10 questions<'), ('>15 pitanja<', '>15 questions<'), ('>20 pitanja<', '>20 questions<'), ('>30 pitanja<', '>30 questions<'),
    ('Uključi zvuk 🔊', 'Sound on 🔊'),
    ('Svaki igrač odgovara na isti broj pitanja. Nivoi se nasumično miješaju. Tačan odgovor: +100 zlatnika; netačan: −30 (najmanje 0). Pitanja se ne ponavljaju tokom partije.',
     'Both players answer the same number of questions. The levels are mixed at random. Right answer: +100 gold coins; wrong answer: −30 (never below 0). No question comes up twice in a game.'),
    ('▶ ZAPOČNI DVOBОJ', '▶ START THE DUEL'),
    ('<span id="turn" class="pill">Na potezu: Igrač 1</span>', '<span id="turn" class="pill">Your turn: Player 1</span>'),
    ('<span id="meta" class="small">Pitanje 1/20</span>', '<span id="meta" class="small">Question 1/20</span>'),
    ('🔄 Nova partija', '🔄 New game'), ('⬇ Preuzmi HTML', '⬇ Download the game'),
    ('<button class="btn secondary" id="mute">🔊 Zvuk</button>', '<button class="btn secondary" id="mute">🔊 Sound</button>'),
    ('↻ Početak', '↻ Start again'),
    ('Radi i bez interneta nakon preuzimanja', 'Works without the internet once downloaded'),
    ("names=['Igrač 1','Igrač 2']", "names=['Player 1','Player 2']"),
    ("+'/'+limit+' odgovora'", "+'/'+limit+' answers'"),
    ("$('input0').value.trim()||'Igrač 1',$('input1').value.trim()||'Igrač 2'", "$('input0').value.trim()||'Player 1',$('input1').value.trim()||'Player 2'"),
    ("muted?'🔇 Bez zvuka':'🔊 Zvuk'", "muted?'🔇 Sound off':'🔊 Sound'"),
    ("'🎤 Na potezu: '+names[player]", "'🎤 Your turn: '+names[player]"),
    ("'Pitanje '+(index+1)+'/'+(limit*2)+' · Nivo '+q.l", "'Question '+(index+1)+'/'+(limit*2)+' · Level '+q.l"),
    ("'Odaberi jedan od četiri odgovora'", "'Choose one of the four answers'"),
    ("ok?'✅ Tačno! +100 zlatnika':'❌ Netačno! −30 zlatnika. Tačan odgovor je označen zeleno.'",
     "ok?'✅ Correct! +100 gold coins':'❌ Wrong! −30 gold coins. The right answer is shown in green.'"),
    ("'🤝 NERIJEŠENO!':('🏆 POBJEDNIK: '", "'🤝 IT’S A DRAW!':('🏆 WINNER: '"),
    ("a.download='mektebski-milioner-za-dvoje.html'", "a.download='maktab-millionaire-for-two.html'"),
]


def transform(src):
    return _ilmihal_bank.translate(src)
