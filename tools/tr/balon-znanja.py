# Balon znanja -> Knowledge Balloon (solo: right answers lift the balloon). Shared Ilmihal question bank
# (_ilmihal_bank.translate); UI strings below.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

DELETE = ['<div class="footer">Pripremio Abdo ef. Rekić • Džemat Turija–Vrsta</div>']

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>Balon znanja – Mektebska akademija</title>', '<title>Knowledge Balloon</title>'),
    ('<h1>🎈 BALON ZNANJA</h1><div class="sub">Mektebska akademija • Putovanje kroz Ilmihal • A1–B3</div>',
     '<h1>🎈 KNOWLEDGE BALLOON</h1><div class="sub">Maktab Academy • A journey through the Ilmihal • A1–B3</div>'),
    ('☁️ Poleti prema vrhu!', '☁️ Fly to the top!'),
    ('Tačan odgovor podiže balon, netačan ga spušta. Sakupi što više bodova i osvoji zlatnu medalju!',
     'A right answer lifts the balloon, a wrong one brings it down. Collect as many points as you can and win the gold medal!'),
    ('<label for="level">Nivo pitanja</label>', '<label for="level">Question level</label>'),
    ('Svi nivoi A1–B3 (nasumično)', 'All levels A1–B3 (mixed)'),
    ('<label for="count">Dužina putovanja</label>', '<label for="count">Length of the journey</label>'),
    ('>10 pitanja<', '>10 questions<'), ('>20 pitanja<', '>20 questions<'), ('>30 pitanja<', '>30 questions<'), ('>50 pitanja<', '>50 questions<'),
    ('🚀 Započni let', '🚀 Take off'),
    ('<button id="sound">🔊 Zvuk: uključen</button>', '<button id="sound">🔊 Sound: on</button>'),
    ('aria-label="Balon koji se podiže prema vrhu"', 'aria-label="A balloon rising to the top"'),
    ('<span class="alt" id="height">Visina: 0 / 10</span>', '<span class="alt" id="height">Height: 0 / 10</span>'),
    ('<span id="progress">Pitanje 1/20</span>', '<span id="progress">Question 1/20</span>'),
    ('<span id="score">⭐ 0 bodova</span>', '<span id="score">⭐ 0 points</span>'),
    ('🔄 Nova igra', '🔄 New game'), ('<button id="back">⚙️ Postavke</button>', '<button id="back">⚙️ Settings</button>'),
    ('<h2>Putovanje je završeno!</h2>', '<h2>The journey is over!</h2>'),
    ('🔄 Igraj ponovo', '🔄 Play again'), ('⚙️ Izbor nivoa', '⚙️ Choose a level'),
    ('⬇️ Preuzmi HTML igru', '⬇️ Download the game'),
    ('Jedan HTML fajl • radi offline na Androidu i iPhoneu', 'One file • works offline on Android and iPhone'),
    ("'Visina: '+alt+' / 10'", "'Height: '+alt+' / 10'"),
    ("'⭐ '+score+' bodova'", "'⭐ '+score+' points'"),
    ("'Pitanje '+(pos+1)+'/'+pool.length", "'Question '+(pos+1)+'/'+pool.length"),
    ("'Nivo '+item.l", "'Level '+item.l"),
    ("'Odaberi tačan odgovor'", "'Choose the right answer'"),
    ("'✅ Tačno! Balon se podiže! +10 bodova'", "'✅ Correct! The balloon rises! +10 points'"),
    ("'❌ Netačno! Tačno: '+item.a[item.c]+' (−3 boda)'", "'❌ Wrong! The answer is: '+item.a[item.c]+' (−3 points)'"),
    ("'Tačnih odgovora: '+correct+' / '+pool.length+' • Osvojeno '+score+' bodova • Završna visina: '+alt+'/10'",
     "'Right answers: '+correct+' / '+pool.length+' • '+score+' points • Final height: '+alt+'/10'"),
    ("' • 🥇 Osvojena zlatna medalja!':' • Pokušaj ponovo i dođi do vrha!'", "' • 🥇 You won the gold medal!':' • Try again and reach the top!'"),
    ("muted?'🔇 Zvuk: isključen':'🔊 Zvuk: uključen'", "muted?'🔇 Sound: off':'🔊 Sound: on'"),
    ("a.download='balon-znanja.html'", "a.download='knowledge-balloon.html'"),
]


def transform(src):
    return _ilmihal_bank.translate(src)
