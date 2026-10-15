# Mektebski Čovječe, ne ljuti se! -> Maktab Board Game – Don’t Get Angry! (2–4 players, one phone: roll the die, answer, move).
# Shared Ilmihal question bank (_ilmihal_bank.translate); UI strings below.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

DELETE = ['<div class="footer">Pripremio Abdo ef. Rekić · Džemat Turija–Vrsta · Medžlis IZ Bihać</div>']

# '.' ends two different sentences ("It is X’s turn." needs the ’s before it).
ALLOW_INCONSISTENT = ['.']

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>Mektebski Čovječe, ne ljuti se!</title>', '<title>Maktab Board Game – Don’t Get Angry!</title>'),
    ('<h1>🎲 Mektebski Čovječe, ne ljuti se!</h1><small>Znanje • Igra • Druženje · A1–B3</small>',
     '<h1>🎲 Maktab Board Game – Don’t Get Angry!</h1><small>Knowledge • Play • Friendship · A1–B3</small>'),
    ('⚙️ Postavke igre', '⚙️ Game settings'),
    ('<label>Broj igrača</label>', '<label>Number of players</label>'),
    ('>2 igrača<', '>2 players<'), ('>3 igrača<', '>3 players<'), ('>4 igrača<', '>4 players<'),
    ('<label>Broj polja do cilja</label>', '<label>Squares to the finish</label>'),
    ('>20 (brza igra)<', '>20 (quick game)<'), ('>40 (klasična)<', '>40 (classic)<'),
    ('<label>Odaberi nivoe pitanja</label>', '<label>Choose the question levels</label>'),
    ('▶️ POKRENI IGRU', '▶️ START THE GAME'),
    ('⬇️ DOWNLOADS', '⬇️ DOWNLOAD'),
    ('Pravilo: baci kockicu i odgovori na pitanje. Tačno = pomjeri figuru za broj na kockici. Netačno = ostaješ na mjestu. Ako staneš na protivnika, vraćaš ga na početak. Za pobjedu treba tačno stići do cilja.',
     'Rules: roll the die and answer the question. Right = move your piece by the number on the die. Wrong = you stay where you are. If you land on another player, they go back to the start. To win, you must land exactly on the finish.'),
    ('🏅 MEKTEBSKA STAZA', '🏅 MAKTAB TRACK'),
    ('🎲 BACI KOCKICU', '🎲 ROLL THE DIE'),
    ('<strong id="qLevel">Pitanje</strong>', '<strong id="qLevel">Question</strong>'),
    ('Baci kockicu da dobiješ pitanje.', 'Roll the die to get a question.'),
    ('Čeka se bacanje kockice.', 'Waiting for the die to be rolled.'),
    ('Nastavi ▶', 'Continue ▶'),
    ('↩️ NOVA IGRA', '↩️ NEW GAME'), ('🔄 IGRAJ PONOVO', '🔄 PLAY AGAIN'),
    ("+' Igrač '+(i+1)", "+' Player '+(i+1)"),
    ("'Ukupno '+Object.values(BANK)", "'In total '+Object.values(BANK)"),
    ("+' pitanja iz priloženih baza.'", "+' questions from the Ilmihal question banks.'"),
    ("a.download='mektebski_covjece_ne_ljuti_se.html'", "a.download='maktab-board-game.html'"),
    ("<br><span class=\"score\">Polje '+p.pos+'/'+target+' · Tačno '+p.right+' · Netačno '+p.wrong+'</span>'",
     "<br><span class=\"score\">Square '+p.pos+'/'+target+' · Right '+p.right+' · Wrong '+p.wrong+'</span>'"),
    ("+' Na redu: '+players[turn].name", "+' Your turn: '+players[turn].name"),
    ("'Do cilja: '+(target-players[turn].pos)+' polja'", "'To the finish: '+(target-players[turn].pos)+' squares'"),
    ("alert('Odaberi najmanje jedan nivo!')", "alert('Choose at least one level!')"),
    ("||'Igrač '+(i+1)", "||'Player '+(i+1)"),
    ("'Tačan odgovor pomjera tvoju figuru.'", "'A right answer moves your piece.'"),
    ("$('qLevel').textContent='Spremni!'", "$('qLevel').textContent='Ready!'"),
    ("+' · Kockica: '+rolled", "+' · Die: '+rolled"),
    ("'Pitanje '+asked", "'Question '+asked"),
    ("'Odaberi jedan od četiri odgovora.'", "'Choose one of the four answers.'"),
    ("'✅ Tačno! Za cilj treba tačan broj. Ostaješ na polju '+p.pos+'.'", "'✅ Correct! You need the exact number to finish. You stay on square '+p.pos+'.'"),
    ("'✅ Tačno! Napredovao/la si '+rolled+' polja.'", "'✅ Correct! You move '+rolled+' squares.'"),
    ("+' vraća se na START!'", "+' goes back to START!'"),
    ("'❌ Netačno. Ostaješ na polju '+p.pos+'. Tačan odgovor je označen zeleno.'", "'❌ Wrong. You stay on square '+p.pos+'. The right answer is shown in green.'"),
    ("'🏆 PRIKAŽI POBJEDNIKA'", "'🏆 SHOW THE WINNER'"),
    ("'Na redu je '+players[turn].name+'.'", "'It is '+players[turn].name+'’s turn.'"),
    ("$('qLevel').textContent='Sljedeći igrač'", "$('qLevel').textContent='Next player'"),
    ("'Pobjednik: '+p.name+'!'", "'Winner: '+p.name+'!'"),
    ("'Čestitamo! Osvojeno '+target+' polja · '+p.right+' tačnih odgovora · '+p.wrong+' netačnih odgovora.'",
     "'Congratulations! '+target+' squares · '+p.right+' right answers · '+p.wrong+' wrong answers.'"),
]


def transform(src):
    return _ilmihal_bank.translate(src)
