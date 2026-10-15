# Dnevni mektebski izazov -> Daily Maktab Challenge (10 new questions a day, streaks, progress saved on the device).
# Shared Ilmihal question bank (_ilmihal_bank.translate); UI strings below.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

DELETE = ['Pripremio Abdo ef. Rekić • Džemat Turija–Vrsta • Medžlis IZ Bihać<br>']

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>Dnevni mektebski izazov</title>', '<title>Daily Maktab Challenge</title>'),
    ('<h1>🌟 DNEVNI MEKTEBSKI IZAZOV</h1><div class="subtitle">Svaki dan 10 novih pitanja • A1',
     '<h1>🌟 DAILY MAKTAB CHALLENGE</h1><div class="subtitle">10 new questions every day • A1'),
    ('<button class="secondary" id="sound">🔊 Zvuk: uključen</button>', '<button class="secondary" id="sound">🔊 Sound: on</button>'),
    ('<small>🔥 Dana zaredom</small>', '<small>🔥 Days in a row</small>'),
    ('<small>⭐ Ukupno bodova</small>', '<small>⭐ Total points</small>'),
    ('<small>🏅 Završenih dana</small>', '<small>🏅 Days completed</small>'),
    ('Današnji izazov te čeka!', 'Today’s challenge is waiting for you!'),
    ('Deset nasumično izabranih pitanja iz tvojih mektebskih baza. Za svaki tačan odgovor dobijaš 10 bodova. Kada završiš svih deset pitanja, osvajaš dnevnu medalju.',
     'Ten questions picked at random from your maktab questions. Every right answer gives you 10 points. Finish all ten and you win today’s medal.'),
    ('Svaki datum ima svoj skup pitanja. Nedovršeni izazov možeš nastaviti kasnije na istom uređaju.',
     'Each day has its own set of questions. If you don’t finish, you can carry on later on the same device.'),
    ('▶️ ZAPOČNI DANAŠNJI IZAZOV', '▶️ START TODAY’S CHALLENGE'),
    ('<div class="winner" id="resultTitle">Bravo!</div>', '<div class="winner" id="resultTitle">Well done!</div>'),
    ('<span class="badge" id="medal">DNEVNA MEDALJA</span>', '<span class="badge" id="medal">TODAY’S MEDAL</span>'),
    ('Novi izazov bit će dostupan sljedećeg kalendarskog dana.', 'A new challenge will be ready tomorrow.'),
    ('🔁 Ponovi za vježbu', '🔁 Play again for practice'),
    ('🗓️ Tvojih posljednjih 7 dana', '🗓️ Your last 7 days'),
    ('🔥 Niz raste završavanjem izazova uzastopnih kalendarskih dana. Medalja za 7 dana zaredom: 🏆',
     '🔥 Your streak grows when you finish the challenge on days in a row. A medal for 7 days in a row: 🏆'),
    ('⬇️ PREUZMI HTML IGRU', '⬇️ DOWNLOAD THE GAME'),
    ('Android i iPhone • Radi bez interneta • Napredak se čuva na ovom uređaju', 'Android and iPhone • Works without the internet • Your progress is saved on this device'),
    ("toLocaleDateString('bs-BA',{day:'numeric',month:'long',year:'numeric'})", "toLocaleDateString('en-US',{day:'numeric',month:'long',year:'numeric'})"),
    ("toLocaleDateString('bs-BA',{day:'2-digit',month:'2-digit'})", "toLocaleDateString('en-US',{day:'2-digit',month:'2-digit'})"),
    ("'🏆 ČESTITAMO! OSVOJENA MEDALJA ZA 7 DANA!'", "'🏆 CONGRATULATIONS! YOU WON THE 7-DAY MEDAL!'"),
    ("'Pitanje '+(idx+1)+' od 10'+(practice?' • Vježba':'')", "'Question '+(idx+1)+' of 10'+(practice?' • Practice':'')"),
    ("'Nivo '+q.l", "'Level '+q.l"),
    ("correct?'✅ Tačno! +10 bodova':'❌ Tačan odgovor: '+q.a[q.c]", "correct?'✅ Correct! +10 points':'❌ The right answer: '+q.a[q.c]"),
    ("practice?'🎉 Vježba završena!':'🏅 Dnevni izazov završen!'", "practice?'🎉 Practice finished!':'🏅 Today’s challenge is done!'"),
    ("practice?'Sutra te čekaju nova pitanja.':'Osvojio/la si '+points+' od 100 bodova!'", "practice?'New questions are waiting for you tomorrow.':'You scored '+points+' out of 100 points!'"),
    ("streak()>=7?'🏆 MEDALJA ZA 7 DANA':'🏅 DNEVNA MEDALJA'", "streak()>=7?'🏆 7-DAY MEDAL':'🏅 TODAY’S MEDAL'"),
    ("muted?'🔇 Zvuk: isključen':'🔊 Zvuk: uključen'", "muted?'🔇 Sound: off':'🔊 Sound: on'"),
    ("a.download='dnevni-mektebski-izazov.html'", "a.download='daily-maktab-challenge.html'"),
    ("'▶️ NASTAVI DANAŠNJI IZAZOV'", "'▶️ CARRY ON WITH TODAY’S CHALLENGE'"),
    ("'Već si odgovorio/la na '+idx+' pitanja. Nastavi tamo gdje si stao/la.'", "'You have already answered '+idx+' questions. Carry on where you left off.'"),
]


def transform(src):
    return _ilmihal_bank.translate(src)
