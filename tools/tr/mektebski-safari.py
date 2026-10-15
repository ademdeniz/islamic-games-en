# Mektebski safari -> Maktab Safari (solo: every right answer "photographs" an animal for your album).
# Shared Ilmihal question bank (_ilmihal_bank.translate); UI strings and animal names below.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

DELETE = ['<div class="credit">Pripremio Abdo ef. Rekić • Džemat Turija–Vrsta</div>']

# 'SVI' is both the internal code for “all levels” (kept) and a button label (translated).
ALLOW_INCONSISTENT = ['SVI']

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>🦁 Mektebski safari</title>', '<title>🦁 Maktab Safari</title>'),
    ('<h1>🦁 MEKTEBSKI SAFARI</h1><small>🚙 Istraži prirodu • odgovori • fotografiši životinje</small>',
     '<h1>🦁 MAKTAB SAFARI</h1><small>🚙 Explore nature • answer • photograph the animals</small>'),
    ('<button id="sound" type="button">🔊 Zvuk</button>', '<button id="sound" type="button">🔊 Sound</button>'),
    ('⬇️ Preuzmi HTML', '⬇️ Download the game'), ('↻ Nova igra', '↻ New game'),
    ('Odaberi nivo i dužinu putovanja. Svaki tačan odgovor donosi fotografiju životinje. Sva pitanja su iz tvojih baza Ilmihala.',
     'Choose a level and the length of the trip. Every right answer gives you a photo of an animal. All the questions come from the Ilmihal.'),
    ('<label for="length">Stanica:</label>', '<label for="length">Stops:</label>'),
    ('🚙 KRENI NA SAFARI', '🚙 GO ON SAFARI'),
    ('<span id="position">🧭 Stanica 1/20</span><span id="score">⭐ 0 bodova</span><span id="levelTag">SVI NIV0I</span>',
     '<span id="position">🧭 Stop 1/20</span><span id="score">⭐ 0 points</span><span id="levelTag">ALL LEVELS</span>'),
    ('aria-label="Animirani safari sa životinjama"', 'aria-label="An animated safari with animals"'),
    ('<div class="animal-label" id="animalName">Lav</div>', '<div class="animal-label" id="animalName">Lion</div>'),
    ('<span id="photoCount">📸 0 fotografija</span><span id="wrongCount">❌ 0 grešaka</span>', '<span id="photoCount">📸 0 photos</span><span id="wrongCount">❌ 0 mistakes</span>'),
    ('📷 Moj safari album', '📷 My safari album'),
    ('🚙 IGRAJ PONOVO', '🚙 PLAY AGAIN'),
    ("[['🦁','Lav'],['🦒','Žirafa'],['🐘','Slon'],['🦓','Zebra'],['🐒','Majmun'],['🦛','Nilski konj'],['🦏','Nosorog'],['🐆','Leopard'],['🐊','Krokodil'],['🦜','Papagaj'],['🦩','Flamingo'],['🐢','Kornjača'],['🦋','Leptir'],['🦌','Jelen'],['🦚','Paun'],['🐅','Tigar'],['🐪','Deva'],['🦉','Sova'],['🦔','Jež'],['🐿️','Vjeverica']]",
     "[['🦁','Lion'],['🦒','Giraffe'],['🐘','Elephant'],['🦓','Zebra'],['🐒','Monkey'],['🦛','Hippo'],['🦏','Rhino'],['🐆','Leopard'],['🐊','Crocodile'],['🦜','Parrot'],['🦩','Flamingo'],['🐢','Tortoise'],['🦋','Butterfly'],['🦌','Deer'],['🦚','Peacock'],['🐅','Tiger'],['🐪','Camel'],['🦉','Owl'],['🦔','Hedgehog'],['🐿️','Squirrel']]"),
    ("b.textContent=l==='SVI'?'SVI':l", "b.textContent=l==='SVI'?'ALL':l"),
    ("`Baza: ${BANK.length} pitanja • A1–B3 • bez ponavljanja tokom putovanja`", "`Question bank: ${BANK.length} questions • A1–B3 • no question twice in one trip`"),
    ("`🧭 Stanica ${idx+1}/${round.length}`", "`🧭 Stop ${idx+1}/${round.length}`"),
    ("`⭐ ${score} bodova`", "`⭐ ${score} points`"),
    ("`Nivo ${q.l} • ${animal[1]} čuva pitanje`", "`Level ${q.l} • ${animal[1]} guards this question`"),
    ("'Odaberi jedan odgovor'", "'Choose one answer'"),
    ("`📸 ${photos.length} fotografija`", "`📸 ${photos.length} photos`"),
    ("`❌ ${wrong} grešaka`", "`❌ ${wrong} mistakes`"),
    ("'📸 Tačno! Fotografisao/la si životinju! +10 ⭐'", "'📸 Correct! You took a photo of the animal! +10 ⭐'"),
    ("'❌ Netačno! Tačan odgovor je označen. −3 ⭐'", "'❌ Wrong! The right answer is marked. −3 ⭐'"),
    ("`🏆 <strong>SAFARI JE ZAVRŠEN!</strong><br>⭐ ${score} bodova<br>📸 ${photos.length} fotografija od ${round.length} stanica<br>❌ ${wrong} netačnih odgovora<br><small>Svaka nova igra donosi novi nasumični izbor pitanja.</small>`",
     "`🏆 <strong>THE SAFARI IS OVER!</strong><br>⭐ ${score} points<br>📸 ${photos.length} photos from ${round.length} stops<br>❌ ${wrong} wrong answers<br><small>Every new game picks new questions at random.</small>`"),
    ("soundOn?'🔊 Zvuk':'🔇 Bez zvuka'", "soundOn?'🔊 Sound':'🔇 No sound'"),
    ("a.download='mektebski-safari.html'", "a.download='maktab-safari.html'"),
]


def transform(src):
    return _ilmihal_bank.translate(src)
