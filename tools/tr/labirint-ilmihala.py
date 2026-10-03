# Labirint Ilmihala -> Ilmihal Maze (solo: every new step through the maze is a question).
# Shared Ilmihal question bank (_ilmihal_bank.translate); UI strings below.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

DELETE = ['Pripremio Abdo ef. Rekić • Džemat Turija–Vrsta • Medžlis IZ Bihać<br>']

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>Labirint Ilmihala</title>', '<title>Ilmihal Maze</title>'),
    ('<h1>🗝️ LABIRINT ILMIHALA 🕌</h1><p class="sub">Pronađi izlaz • Odgovori tačno • Osvoji medalju</p>',
     '<h1>🗝️ ILMIHAL MAZE 🕌</h1><p class="sub">Find the way out • Answer correctly • Win a medal</p>'),
    ('Odaberi nivo</h2>', 'Choose a level</h2>'),
    ('Koristi strelice ili dodirni susjedno prohodno polje. Za svaki novi korak dobijaš pitanje iz izabranog nivoa. Tačan odgovor otvara prolaz; netačan te zadržava na mjestu.',
     'Use the arrows or tap an open square next to you. Every new step gives you a question from the level you chose. A right answer opens the way; a wrong one keeps you where you are.'),
    ('<label>Veličina lavirinta <select', '<label>Maze size <select'),
    ('Kratki – 7 × 7', 'Small – 7 × 7'), ('Srednji – 9 × 9', 'Medium – 9 × 9'), ('Veliki – 11 × 11', 'Large – 11 × 11'),
    ('▶️ ZAPOČNI IGRU', '▶️ START THE GAME'),
    ('<span id="levelText">Nivo A1</span><span id="score">⭐ 0 bodova</span><span id="steps">👣 0 koraka</span>',
     '<span id="levelText">Level A1</span><span id="score">⭐ 0 points</span><span id="steps">👣 0 steps</span>'),
    ('aria-label="Labirint s prohodnim poljima"', 'aria-label="Maze with open squares"'),
    ('Odaberi susjedno polje!', 'Choose a square next to you!'),
    ('aria-label="Gore"', 'aria-label="Up"'), ('aria-label="Lijevo"', 'aria-label="Left"'), ('aria-label="Dolje"', 'aria-label="Down"'), ('aria-label="Desno"', 'aria-label="Right"'),
    ('<button class="secondary" id="sound">🔊 Zvuk uključen</button>', '<button class="secondary" id="sound">🔊 Sound on</button>'),
    ('🔁 Novi labirint', '🔁 New maze'), ('<button class="secondary" id="back">⚙️ Nivoi</button>', '<button class="secondary" id="back">⚙️ Levels</button>'),
    ('🏆 BRAVO, PRONAŠAO/LA SI IZLAZ!', '🏆 WELL DONE, YOU FOUND THE WAY OUT!'),
    ('🗝️ IGRAJ PONOVO', '🗝️ PLAY AGAIN'), ('⚙️ Promijeni nivo', '⚙️ Change level'),
    ('⬇️ PREUZMI HTML IGRU', '⬇️ DOWNLOAD THE GAME'),
    ('Android i iPhone • Igra radi bez interneta', 'Android and iPhone • Works without the internet'),
    ("'SVI NIV0I'", "'ALL LEVELS'"),
    ("(chosen==='SVI'?'Svi nivoi':chosen)", "(chosen==='SVI'?'All levels':chosen)"),
    ("'🧭 Pronađi put do izlaza 🏁'", "'🧭 Find the way to the exit 🏁'"),
    ("i===position?'Igrač':i===exit?'Izlaz':v?'Prohodno polje':'Zid'", "i===position?'You':i===exit?'Exit':v?'Open square':'Wall'"),
    ("'⭐ '+points+' bodova'", "'⭐ '+points+' points'"),
    ("'👣 '+steps+' koraka'", "'👣 '+steps+' steps'"),
    ("'👣 Vraćaš se poznatim putem.'", "'👣 You go back along a path you know.'"),
    ("'Pitanje '+(qi+1)+' • Nivo '+q.l", "'Question '+(qi+1)+' • Level '+q.l"),
    ("'🔐 Odgovori da otključaš prolaz!'", "'🔐 Answer to unlock the way!'"),
    ("ok?'✅ Tačno! Prolaz je otvoren!':'❌ Netačno! Tačan odgovor: '+q.a[q.c]", "ok?'✅ Correct! The way is open!':'❌ Wrong! The right answer: '+q.a[q.c]"),
    ("ok?'🔓 Odlično! Odaberi sljedeći prolaz.':'🧩 Pokušaj drugi put – ostaješ na mjestu.'", "ok?'🔓 Great! Choose your next step.':'🧩 Try another way – you stay where you are.'"),
    ("'🏆 Uspješno si izašao/la iz labirinta!'", "'🏆 You made it out of the maze!'"),
    ("'Osvojeno '+points+' bodova • '+steps+' koraka • '+qi+' pitanja'", "'You scored '+points+' points • '+steps+' steps • '+qi+' questions'"),
    ("muted?'🔇 Zvuk isključen':'🔊 Zvuk uključen'", "muted?'🔇 Sound off':'🔊 Sound on'"),
    ("a.download='labirint-ilmihala.html'", "a.download='ilmihal-maze.html'"),
]


def transform(src):
    return _ilmihal_bank.translate(src)
