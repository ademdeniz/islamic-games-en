# Mektebski turnir -> Maktab Tournament (4 students: semi-finals, final, trophy – one phone).
# Shared Ilmihal question bank (_ilmihal_bank.translate, which also drops the "✅" that gave answers away
# in some of this game's options); UI strings below.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>🏅 Mektebski turnir</title>', '<title>🏅 Maktab Tournament</title>'),
    ('<h1>🏅 MEKTEBSKI TURNIR</h1><small>Polufinale → Finale → Pobjednički pehar</small>',
     '<h1>🏅 MAKTAB TOURNAMENT</h1><small>Semi-finals → Final → Winner’s trophy</small>'),
    ('⬇️ DOWNLOADS – PREUZMI IGRU (HTML)', '⬇️ DOWNLOAD THE GAME'),
    ('👥 Prijava četiri učenika', '👥 Sign up four students'),
    ('<label>Broj pitanja po igraču u jednom meču</label>', '<label>Questions per player in each match</label>'),
    ('>5 pitanja<', '>5 questions<'), ('>10 pitanja<', '>10 questions<'), ('>15 pitanja<', '>15 questions<'), ('>20 pitanja<', '>20 questions<'),
    ('<label>Odaberi nivoe pitanja</label>', '<label>Choose the question levels</label>'),
    ('Svaki igrač odgovara na jednak broj pitanja. Tačno +10, netačno −3. Kod izjednačenja igra se dodatno pitanje dok se ne dobije pobjednik. Pitanja i odgovori se miješaju.',
     'Each player answers the same number of questions. Correct +10, wrong −3. If it’s a tie, extra questions are played until there is a winner. Questions and answers are shuffled.'),
    ('🏁 Započni turnir', '🏁 Start the tournament'),
    ('🏆 Turnirska tabela', '🏆 Tournament bracket'),
    ('Nastavi ➜', 'Continue ➜'),
    ('<h2>POBJEDNIK TURNIRA</h2>', '<h2>TOURNAMENT WINNER</h2>'),
    ('🔄 Novi turnir', '🔄 New tournament'), ('⬇️ Preuzmi rezultate', '⬇️ Download the results'),
    ('Pripremio Abdo ef. Rekić · Džemat Turija–Vrsta · Radi i bez interneta', 'Works without the internet'),
    ('`<label>Učenik ${i+1}</label><input maxlength="40" id="n${i}" placeholder="Ime učenika ${i+1}" value="">`',
     '`<label>Student ${i+1}</label><input maxlength="40" id="n${i}" placeholder="Student ${i+1}’s name" value="">`'),
    ("'Baza: '+Object.entries(BANK)", "'Question bank: '+Object.entries(BANK)"),
    (".join(' · ')+' pitanja'", ".join(' · ')+' questions'"),
    ("||'Učenik '+(i+1)", "||'Student '+(i+1)"),
    ("alert('Odaberi barem jedan nivo.')", "alert('Choose at least one level.')"),
    ("[['POLUFINALE 1',[0,1]],['POLUFINALE 2',[2,3]],['FINALE',", "[['SEMI-FINAL 1',[0,1]],['SEMI-FINAL 2',[2,3]],['FINAL',"),
    ("'Čeka se...'", "'Waiting…'"),
    ("match.scores[j]+' b.':results[i]?results[i].scores[j]+' b.'", "match.scores[j]+' pts':results[i]?results[i].scores[j]+' pts'"),
    ("'🥇 FINALE':'⚔️ POLUFINALE '", "'🥇 FINAL':'⚔️ SEMI-FINAL '"),
    ("'Dodatno pitanje':`Pitanje ${done+1}/${count}`", "'Extra question':`Question ${done+1}/${count}`"),
    ("+match.scores[p]+' bodova'", "+match.scores[p]+' points'"),
    ("'✅ Tačno! +10 bodova':'❌ Netačno! −3 boda'", "'✅ Correct! +10 points':'❌ Wrong! −3 points'"),
    ("' · Sljedeće pitanje automatski za 1,2 s'", "' · Next question in 1.2 s'"),
    ("+' prolazi dalje!</h2><p>Rezultat: '", "+' goes through!</h2><p>Result: '"),
    ("'🏆 Pokreni finale':'▶️ Sljedeće polufinale'", "'🏆 Start the final':'▶️ Next semi-final'"),
    ("a.download='mektebski_turnir_A1_B3.html'", "a.download='maktab-tournament.html'"),
    ("'MEKTEBSKI TURNIR\\nPripremio Abdo ef. Rekić\\n\\n'", "'MAKTAB TOURNAMENT\\nBosnian Islamic Community of Erie\\n\\n'"),
    ("(i<2?'Polufinale '+(i+1):'Finale')", "(i<2?'Semi-final '+(i+1):'Final')"),
    ("'\\nPobjednik: '+names[results[2].winner]", "'\\nWinner: '+names[results[2].winner]"),
    ("a.download='mektebski-turnir-rezultati.txt'", "a.download='maktab-tournament-results.txt'"),
]


def transform(src):
    return _ilmihal_bank.translate(src)
