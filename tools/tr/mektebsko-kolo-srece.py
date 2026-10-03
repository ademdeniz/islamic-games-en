# Mektebsko kolo sreće -> Maktab Wheel of Fortune (two players, one phone; the wheel picks the level).
# Shared Ilmihal question bank (_ilmihal_bank.translate); UI strings below. (Repo: mektebsko-kolo-srece.)
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>Mektebsko kolo sreće</title>', '<title>Maktab Wheel of Fortune</title>'),
    ('<h1>🎡 Mektebsko kolo sreće</h1>', '<h1>🎡 Maktab Wheel of Fortune</h1>'),
    ('— svih 1.568 pitanja', '— all 1,568 questions'),
    ('<input id="name0" value="Učesnik 1" aria-label="Ime prvog učesnika">', '<input id="name0" value="Player 1" aria-label="First player’s name">'),
    ('<input id="name1" value="Učesnik 2" aria-label="Ime drugog učesnika">', '<input id="name1" value="Player 2" aria-label="Second player’s name">'),
    ('<div class="small">bodova · <b id="plays0">0</b>/10 poteza</div>', '<div class="small">points · <b id="plays0">0</b>/10 turns</div>'),
    ('<div class="small">bodova · <b id="plays1">0</b>/10 poteza</div>', '<div class="small">points · <b id="plays1">0</b>/10 turns</div>'),
    ('🎡 ZAVRTI KOLO', '🎡 SPIN THE WHEEL'),
    ('<button class="secondary" id="reset">Nova igra</button>', '<button class="secondary" id="reset">New game</button>'),
    ('🎯 IGRA UČESNIK 1', '🎯 PLAYER 1’S TURN'),
    ('Pritisni „Zavrti kolo“. Kolo nasumično bira jedan od šest nivoa.', 'Press “Spin the wheel”. The wheel picks one of the six levels at random.'),
    ('10 poteza po igraču · Tačno +10 · Netačno −3 · Automatski prelazi na drugog učesnika.', '10 turns per player · Correct +10 · Wrong −3 · Then it is automatically the other player’s turn.'),
    ('Sljedeći učesnik →', 'Next player →'),
    ('Pripremio Abdo ef. Rekić · Džemat Turija–Vrsta · Radi i bez interneta', 'Works without the internet'),
    ("('Učesnik '+(turn+1))", "('Player '+(turn+1))"),
    ("'Kolo se okreće…'", "'The wheel is spinning…'"),
    ("'🎡 Koji nivo će se zaustaviti?'", "'🎡 Which level will it stop on?'"),
    ("who()+' vrti kolo…'", "who()+' spins the wheel…'"),
    ("who()+' · Nivo '+level+' · Pitanje '+shown", "who()+' · Level '+level+' · Question '+shown"),
    ("'Odaberi jedan odgovor.'", "'Choose one answer.'"),
    ("good?'✅ Tačno! +10 bodova.':'❌ Netačno! −3 boda. Tačno: '", "good?'✅ Correct! +10 points.':'❌ Wrong! −3 points. The answer is: '"),
    ("'Sljedeći igra: '", "'Next to play: '"),
    ("('Učesnik '+(2-turn))", "('Player '+(2-turn))"),
    ("el('name0').value.trim()||'Učesnik 1',b=el('name1').value.trim()||'Učesnik 2'", "el('name0').value.trim()||'Player 1',b=el('name1').value.trim()||'Player 2'"),
    ("'🤝 NERIJEŠENO!':('🏆 POBJEDNIK: '", "'🤝 IT’S A DRAW!':('🏆 WINNER: '"),
    ("'🏁 KRAJ IGRE — 10/10 POTEZA'", "'🏁 GAME OVER — 10/10 TURNS'"),
    ("+': '+scores[0]+' bodova  |  '+b+': '+scores[1]+' bodova. Za novu partiju pritisni „Nova igra“.'",
     "+': '+scores[0]+' points  |  '+b+': '+scores[1]+' points. Press “New game” to play again.'"),
    ("'Pritisni „Zavrti kolo“ za novo nasumično pitanje.'", "'Press “Spin the wheel” for a new random question.'"),
    ("'🎯 IGRA '+who().toUpperCase()", "'🎯 YOUR TURN: '+who().toUpperCase()"),
    ("'10 poteza po igraču · Tačno +10 · Netačno −3'", "'10 turns per player · Correct +10 · Wrong −3'"),
    ("confirm('Pokrenuti novu igru i obrisati bodove?')", "confirm('Start a new game and clear the points?')"),
    ("'Pritisni „Zavrti kolo“. Kolo nasumično bira nivo.'", "'Press “Spin the wheel”. The wheel picks a level at random.'"),
]


def transform(src):
    return _ilmihal_bank.translate(src)
