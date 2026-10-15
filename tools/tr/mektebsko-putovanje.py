# Mektebsko putovanje – 100 stanica -> Maktab Journey (solo: 100 stops in 10 worlds of the Ilmihal, a medal per
# world, progress saved on the device). Shared Ilmihal question bank (_ilmihal_bank.translate – it also repairs the
# 6 questions that had another question's options in this copy); UI strings and world names below.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

DELETE = ['Pripremio Abdo ef. Rekić · Džemat Turija–Vrsta<br>']

STRUCTURAL = ('6 questions in this copy of the bank had another question’s answer options; they get their own options '
              'and right answer from the shared bank (_ilmihal_bank.repair), so a few numbers change')

WORLDS = [('Čistoća', 'Cleanliness'), ('Abdest', 'Wudu'), ('Namaz', 'Salah'), ('Sure', 'Surahs'), ('Dove', 'Duas'),
          ('Ahlak', 'Manners'), ('Poslanici', 'Messengers'), ('Kur’an', 'Qur’an')]

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>Mektebsko putovanje – 100 stanica</title>', '<title>Maktab Journey – 100 Stops</title>'),
    ('<h1>🧭 Mektebsko putovanje</h1><div class="sub">100 stanica · 10 svjetova Ilmihala · 10 medalja</div>',
     '<h1>🧭 Maktab Journey</h1><div class="sub">100 stops · 10 worlds of the Ilmihal · 10 medals</div>'),
    ('<label for="per">Pitanja po stanici: <select', '<label for="per">Questions per stop: <select'),
    ('⬇ Preuzmi igru</a>', '⬇ Download the game</a>'),   # (the download="…" file name is markup – kept)
    ('<span id="counter">Stanica 1 / 100</span><span class="badge" id="score">⭐ 0 bodova</span>', '<span id="counter">Stop 1 / 100</span><span class="badge" id="score">⭐ 0 points</span>'),
    ('Nastavi putovanje ➜', 'Continue the journey ➜'),
    ('<b>🏅 Osvojene medalje</b>', '<b>🏅 Medals won</b>'),
    ('↻ Započni novo putovanje', '↻ Start a new journey'),
    ('Radi i bez interneta nakon preuzimanja HTML datoteke.', 'Works without the internet once you download the game.'),
    ("const worlds=['Iman','Islam','Čistoća','Abdest','Namaz','Sure','Dove','Ahlak','Poslanici','Kur’an']",
     "const worlds=['Iman','Islam','Cleanliness','Wudu','Salah','Surahs','Duas','Manners','Messengers','Qur’an']"),
] + [(f'"{bs}":[', f'"{en}":[') for bs, en in WORLDS] + [
    ("'Baza: '+BANK.length+' različitih pitanja iz A1, A2, A3, B1, B2 i B3 · Stanica '+(step+1)+': '+(state.sub+1)+'/'+state.per+' pitanja'",
     "'Question bank: '+BANK.length+' different questions from A1, A2, A3, B1, B2 and B3 · Stop '+(step+1)+': '+(state.sub+1)+'/'+state.per+' questions'"),
    ("'Stanica '+Math.min(100,n+1)+' / 100'", "'Stop '+Math.min(100,n+1)+' / 100'"),
    ("'⭐ '+state.points+' bodova'", "'⭐ '+state.points+' points'"),
    ("'🏆<br><b>Čestitamo!</b><br>Završeno svih 100 stanica i osvojeno 10 medalja!<br><small>Ukupno bodova: '",
     "'🏆<br><b>Congratulations!</b><br>You finished all 100 stops and won all 10 medals!<br><small>Total points: '"),
    ("'Svijet '+(w+1)+'/10 · Stanica '+(step+1)+'/10 · Pitanje '+(state.sub+1)+'/'+state.per+' · Izvor: '+item.level",
     "'World '+(w+1)+'/10 · Stop '+(step+1)+'/10 · Question '+(state.sub+1)+'/'+state.per+' · Level: '+item.level"),
    ("'❌ Pokušaj ponovo!'", "'❌ Try again!'"),
    ("'🏅 Osvojena medalja: '+worlds[Math.floor((state.n-1)/10)]+'!':finished?'✅ Stanica završena!':'✅ Tačno! Nastavi pitanja na ovoj stanici.'",
     "'🏅 Medal won: '+worlds[Math.floor((state.n-1)/10)]+'!':finished?'✅ Stop completed!':'✅ Correct! Carry on with the questions at this stop.'"),
    ("state.n===100?'🏆 Pogledaj rezultat':won?'🧭 U sljedeći svijet ➜':finished?'Sljedeća stanica ➜':'Sljedeće pitanje ➜'",
     "state.n===100?'🏆 See your result':won?'🧭 On to the next world ➜':finished?'Next stop ➜':'Next question ➜'"),
    ("confirm('Promjena broja pitanja započinje novo putovanje. Nastaviti?')", "confirm('Changing the number of questions starts a new journey. Carry on?')"),
    ("confirm('Želiš li obrisati napredak i krenuti od prve stanice?')", "confirm('Clear your progress and start again from the first stop?')"),
    ('// Self-contained download button, including full embedded question bank.', '// Self-contained download button, including full embedded question bank.'),
]


def transform(src):
    return _ilmihal_bank.translate(src)
