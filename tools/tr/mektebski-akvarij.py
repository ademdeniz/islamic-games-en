# Mektebski akvarij -> Maktab Aquarium (solo: every right answer adds a fish or decoration; 30 questions).
# Shared Ilmihal question bank (_ilmihal_bank.translate) – this game still has an older set of 89 B1 questions,
# kept in the bank as "extra" entries. UI strings below.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

DELETE = ['<div class="footer">Pripremio Abdo ef. Rekić · Džemat Turija–Vrsta</div>']

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>Mektebski akvarij</title>', '<title>Maktab Aquarium</title>'),
    ('<h1>🐠 Mektebski akvarij</h1><button id="download">⬇️ Preuzmi HTML</button>', '<h1>🐠 Maktab Aquarium</h1><button id="download">⬇️ Download the game</button>'),
    ('Odgovaraj tačno i napuni svoj akvarij ribicama!', 'Answer correctly and fill your aquarium with fish!'),
    ('<b>Odaberi nivoe pitanja:</b>', '<b>Choose the question levels:</b>'),
    ('▶️ Započni igru (30 pitanja)', '▶️ Start the game (30 questions)'),
    ('<button id="sound">🔊 Zvuk uključen</button>', '<button id="sound">🔊 Sound on</button>'),
    ('Svaka igra nasumično bira 30 različitih pitanja iz odabranih originalnih baza. Tačan odgovor dodaje novu ribicu ili ukras. Tačno +10, netačno −3.',
     'Every game picks 30 different questions at random from the levels you chose. A right answer adds a new fish or decoration. Correct +10, wrong −3.'),
    ('<span id="position">Pitanje 0/30</span><span id="score">Bodovi: 0</span><span id="collected">Stanovnici: 0</span>',
     '<span id="position">Question 0/30</span><span id="score">Points: 0</span><span id="collected">Residents: 0</span>'),
    ('<h2>Akvarij je završen!</h2>', '<h2>Your aquarium is finished!</h2>'),
    ('🔄 Nova igra', '🔄 New game'), ('📸 Sačuvaj rezultat kao sliku', '📸 Save the result as a picture'),
    ('"Stanovnici: "+inhabitants.length', '"Residents: "+inhabitants.length'),
    ('"Pitanje "+Math.min(index+1,30)+"/30"', '"Question "+Math.min(index+1,30)+"/30"'),
    ('"Bodovi: "+score;$("fill")', '"Points: "+score;$("fill")'),
    ('"NIVO "+q.level', '"LEVEL "+q.level'),
    ('"Bravo! Nova ribica ili ukras u akvariju! 🐠"', '"Well done! A new fish or decoration for your aquarium! 🐠"'),
    ('"Tačan odgovor: "+q.options[q.correct]', '"The right answer: "+q.options[q.correct]'),
    ('alert("Odaberi najmanje jedan nivo.")', 'alert("Choose at least one level.")'),
    ('alert("Nema dovoljno pitanja.")', 'alert("There are not enough questions.")'),
    ('"Završeno: 30/30"', '"Finished: 30/30"'),
    ('"Tačno: "+correct+"/30 · Bodovi: "+score+" · Osvojeno ribica i ukrasa: "+inhabitants.length',
     '"Correct: "+correct+"/30 · Points: "+score+" · Fish and decorations won: "+inhabitants.length'),
    ('"mektebski-akvarij.html"', '"maktab-aquarium.html"'),
    ('"🐠 MEKTEBSKI AKVARIJ"', '"🐠 MAKTAB AQUARIUM"'),
    ('"Tačno: "+correct+"/30    Bodovi: "+score', '"Correct: "+correct+"/30    Points: "+score'),
    ('"Pripremio Abdo ef. Rekić"', '"Bosnian Islamic Community of Erie"'),
    ('"moj-mektebski-akvarij.png"', '"my-maktab-aquarium.png"'),
    ('$("position").textContent="Pitanje 0/30"', '$("position").textContent="Question 0/30"'),
    ('soundOn?"🔊 Zvuk uključen":"🔇 Zvuk isključen"', 'soundOn?"🔊 Sound on":"🔇 Sound off"'),
]


def transform(src):
    return _ilmihal_bank.translate(src)
