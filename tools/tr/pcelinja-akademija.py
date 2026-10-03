# Pčelinja akademija -> Bee Academy (solo, Levels A1–A2: every right answer brings a jar of honey to the hive).
# Shared Ilmihal question bank (_ilmihal_bank.translate); UI strings below.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

DELETE = ['<div class="foot">Pripremio Abdo ef. Rekić · Mektebska akademija</div>']

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>Pčelinja akademija</title>', '<title>Bee Academy</title>'),
    ('<h1>🐝 Pčelinja akademija</h1>', '<h1>🐝 Bee Academy</h1>'),
    ('<span class="honey" id="honey">0 tegli</span>', '<span class="honey" id="honey">0 jars</span>'),
    ('<h2>🌻 Od cvijeta do cvijeta!</h2>', '<h2>🌻 From flower to flower!</h2>'),
    ('Svaki cvijet krije pitanje iz Ilmihala. Za tačan odgovor pčelica donosi <b>jednu teglu meda</b> u košnicu. Pitanja i odgovori se miješaju pri svakoj igri.',
     'Every flower hides a question from the Ilmihal. For each right answer the bee brings <b>one jar of honey</b> to the hive. The questions and answers are shuffled every game.'),
    ('aria-label="Nivo"><option value="mix">A1 + A2 zajedno</option><option value="A1">Samo A1</option><option value="A2">Samo A2</option>',
     'aria-label="Level"><option value="mix">A1 + A2 together</option><option value="A1">Only A1</option><option value="A2">Only A2</option>'),
    ('aria-label="Broj cvjetova"', 'aria-label="Number of flowers"'),
    ('>10 cvjetova<', '>10 flowers<'), ('>20 cvjetova<', '>20 flowers<'), ('>30 cvjetova<', '>30 flowers<'), ('>50 cvjetova<', '>50 flowers<'),
    ('<option value="all">Sva pitanja</option>', '<option value="all">All questions</option>'),
    ('▶️ Započni let', '▶️ Start flying'),
    ('📥 DOWNLOADS – Preuzmi igru za offline igranje', '📥 DOWNLOAD the game to play offline'),
    ('<span class="pill" id="step">Cvijet 1 / 20</span>', '<span class="pill" id="step">Flower 1 / 20</span>'),
    ('<div class="muted" id="tag">Nivo A1</div>', '<div class="muted" id="tag">Level A1</div>'),
    ('<h2>Bravo, vrijedna pčelice!</h2>', '<h2>Well done, busy little bee!</h2>'),
    ('🔄 Igraj ponovo', '🔄 Play again'),
    ("'Cvijet '+(index+1)+' / '+deck.length", "'Flower '+(index+1)+' / '+deck.length"),
    ("'Pitanje iz nivoa '+q.level", "'Question from level '+q.level"),
    ("'Odaberi tačan odgovor!'", "'Choose the right answer!'"),
    ("score+' tegli'", "score+' jars'"),
    ("correct?'✅ Tačno! Pčelica je sakupila med!':'❌ Netačno. Tačan odgovor je označen zeleno.'", "correct?'✅ Correct! The bee collected some honey!':'❌ Wrong. The right answer is shown in green.'"),
    ("'Sakupila si '+score+' od '+deck.length+' tegli meda! Tačnih odgovora: '+score+', netačnih: '+(deck.length-score)+'. Uspješnost: '+Math.round(score/deck.length*100)+'%.'",
     "'You collected '+score+' of '+deck.length+' jars of honey! Right answers: '+score+', wrong: '+(deck.length-score)+'. Score: '+Math.round(score/deck.length*100)+'%.'"),
    ("a.download='Pcelinja_akademija_A1_A2.html'", "a.download='bee-academy-A1-A2.html'"),
    ("$('honey').textContent='0 tegli'", "$('honey').textContent='0 jars'"),
    ("'Uključeno '+BANK.length+' pitanja iz priloženih baza A1 i A2. Igra radi i bez interneta.'", "'Includes '+BANK.length+' questions from Levels A1 and A2. Works without the internet.'"),
]


def transform(src):
    return _ilmihal_bank.translate(src)
