# Mektebska akademija -> Maktab Academy (solo: all six levels A1–B3 as missions of 10 questions, medals,
# a printable diploma; progress saved on the device). Shared Ilmihal question bank (_ilmihal_bank.translate –
# this game stores the right answer as its text, which is translated with the options); UI strings below.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import site_settings  # noqa: E402

DELETE = ['<footer class="footer">Pripremio Abdo ef. Rekić • Mektebska akademija</footer>']

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>Mektebska akademija</title>', '<title>Maktab Academy</title>'),
    ('<h1>🏫 Mektebska akademija</h1><p>Šest nivoa • sve lekcije i pitanja • diploma znanja</p>',
     '<h1>🏫 Maktab Academy</h1><p>Six levels • all the lessons and questions • a diploma of knowledge</p>'),
    ('<span class="pill" id="heroName">👧🧒 Učenik</span><span class="pill" id="heroPoints">⭐ 0 bodova</span><span class="pill" id="heroMedals">🏅 0 medalja</span>',
     '<span class="pill" id="heroName">👧🧒 Student</span><span class="pill" id="heroPoints">⭐ 0 points</span><span class="pill" id="heroMedals">🏅 0 medals</span>'),
    ('<h2>👤 Moj profil</h2>', '<h2>👤 My profile</h2>'),
    ('placeholder="Upiši ime učenika" aria-label="Ime učenika"', 'placeholder="Type the student’s name" aria-label="Student’s name"'),
    ('Napredak se čuva na ovom uređaju. Igra radi bez interneta.', 'Your progress is saved on this device. The game works without the internet.'),
    ('<h2>📚 Izaberi nivo</h2>', '<h2>📚 Choose a level</h2>'),
    ('Završi misije redom: A1, A2, A3, B1, B2 i B3. Svako pitanje dolazi na red.', 'Finish the missions in order: A1, A2, A3, B1, B2 and B3. Every question gets its turn.'),
    ('<h2 id="levelTitle">Misije</h2>', '<h2 id="levelTitle">Missions</h2>'),
    ('<h2>🏆 Moje nagrade</h2>', '<h2>🏆 My awards</h2>'),
    ('📜 Moja diploma', '📜 My diploma'), ('⬇️ Preuzmi akademiju', '⬇️ Download the academy'),
    ('id="soundBtn">🔊 Zvuk uključen</button>', 'id="soundBtn">🔊 Sound on</button>'),
    ('← Akademija', '← Academy'),
    ('<span class="note" id="hint">Odaberi jedan odgovor.</span>', '<span class="note" id="hint">Choose one answer.</span>'),
    ('onclick="nextQuestion()">Dalje →</button>', 'onclick="nextQuestion()">Next →</button>'),
    ('← Misije', '← Missions'), ('Ponovi misiju ↻', 'Play the mission again ↻'),
    ('<h1>DIPLOMA ZNANJA</h1><p>Mektebska akademija</p>', '<h1>DIPLOMA OF KNOWLEDGE</h1><p>Maktab Academy</p>'),
    ('<p style="font-weight:800">Pripremio Abdo ef. Rekić</p>', '<p style="font-weight:800">' + site_settings.NAME + '</p>'),
    ('🖨️ Štampaj diplomu', '🖨️ Print the diploma'), ('← Nazad', '← Back'),
    ("const NAMES=['Prvi koraci','Mali istraživač','Poznavalac namaza','Čuvar znanja','Majstor Ilmihala','Veliki poznavalac']",
     "const NAMES=['First steps','Little explorer','Salah expert','Keeper of knowledge','Ilmihal master','Great scholar']"),
    ("'👤 '+(state.name||'Učenik')", "'👤 '+(state.name||'Student')"),
    ("'⭐ '+totalPoints()+' bodova'", "'⭐ '+totalPoints()+' points'"),
    ("+' medalja'", "+' medals'"),
    ("'Završeno '+allDone()+' od '+LV.reduce((n,l)=>n+missionCount(l),0)+' misija'", "'Finished '+allDone()+' of '+LV.reduce((n,l)=>n+missionCount(l),0)+' missions'"),
    ("state.sound?'🔊 Zvuk uključen':'🔇 Zvuk isključen'", "state.sound?'🔊 Sound on':'🔇 Sound off'"),
    ("<b>Misija '+(k+1)+'</b><small>'+(d?'🏅 '+d.points+' bodova • završeno':un?Math.min(10,BANK[selected].length-k*10)+' pitanja • otključano':'Završi prethodnu misiju')+'</small></button>'",
     "<b>Mission '+(k+1)+'</b><small>'+(d?'🏅 '+d.points+' points • finished':un?Math.min(10,BANK[selected].length-k*10)+' questions • unlocked':'Finish the mission before')+'</small></button>'"),
    ("current.l+' • Misija '+(current.k+1)", "current.l+' • Mission '+(current.k+1)"),
    ("'Pitanje '+(idx+1)+'/'+items.length", "'Question '+(idx+1)+'/'+items.length"),
    ("'⭐ '+points+' bodova'", "'⭐ '+points+' points'"),
    ("'Greške: '+mistakes", "'Mistakes: '+mistakes"),
    ("'Odaberi jedan odgovor.'", "'Choose one answer.'"),
    ("ok?'✅ Tačno! Bravo! +10 bodova':'❌ Nije tačno. Tačan odgovor: '+q.a+' (−3 boda)'", "ok?'✅ Correct! Well done! +10 points':'❌ Not right. The right answer: '+q.a+' (−3 points)'"),
    ("idx===items.length-1?'Završi misiju 🏅':'Dalje →'", "idx===items.length-1?'Finish the mission 🏅':'Next →'"),
    ("'Završena misija '+(current.k+1)+'!'", "'Mission '+(current.k+1)+' finished!'"),
    ("'Osvojeno '+points+' bodova. '+(complete?'Čestitamo! Završio/la si nivo '+current.l+' i osvojio/la medalju!':'Otključana je sljedeća misija.')",
     "'You scored '+points+' points. '+(complete?'Congratulations! You finished level '+current.l+' and won a medal!':'The next mission is unlocked.')"),
    ("state.name||'Učenik';", "state.name||'Student';"),
    ("'Uspješno završeno '+allDone()+' od '+LV.reduce((n,l)=>n+missionCount(l),0)+' misija • '+totalPoints()+' bodova • '",
     "'Successfully finished '+allDone()+' of '+LV.reduce((n,l)=>n+missionCount(l),0)+' missions • '+totalPoints()+' points • '"),
    ("a.download='mektebska_akademija_A1_A2_A3_B1_B2_B3.html'", "a.download='maktab-academy.html'"),
]


def transform(src):
    return _ilmihal_bank.translate(src)
