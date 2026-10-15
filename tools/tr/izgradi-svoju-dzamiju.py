# Izgradi svoju džamiju – A1 -> Build Your Mosque (solo, Level A1: every right answer builds part of the mosque).
# Shared Ilmihal question bank (_ilmihal_bank.translate); UI strings below.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

DELETE = ['Pripremio Abdo ef. Rekić · Džemat Turija–Vrsta<br>']

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>Izgradi svoju džamiju – A1</title>', '<title>Build Your Mosque – A1</title>'),
    ('<h1>🕌 Izgradi svoju džamiju</h1><div class="sub">MEKTEBSKA AKADEMIJA · ILMIHAL A1 · 163 pitanja</div>',
     '<h1>🕌 Build Your Mosque</h1><div class="sub">MAKTAB ACADEMY · ILMIHAL A1 · 163 questions</div>'),
    ('<label for="total">Broj pitanja:</label>', '<label for="total">Questions:</label>'),
    ('>10 pitanja<', '>10 questions<'), ('>16 pitanja<', '>16 questions<'), ('>20 pitanja<', '>20 questions<'),
    ('>30 pitanja<', '>30 questions<'), ('>50 pitanja<', '>50 questions<'), ('>Svih 163<', '>All 163<'),
    ('🔄 Nova gradnja', '🔄 Build again'), ('⬇️ DOWNLOADS', '⬇️ DOWNLOAD'),
    ('<span class="pill" id="counter">Pitanje 1/16</span><span class="pill" id="score">⭐ 0 bodova</span><span class="pill" id="parts">🧱 0/16 dijelova</span>',
     '<span class="pill" id="counter">Question 1/16</span><span class="pill" id="score">⭐ 0 points</span><span class="pill" id="parts">🧱 0/16 parts</span>'),
    ('<span class="badge" id="stage">Počinjemo gradnju!</span>', '<span class="badge" id="stage">Let’s start building!</span>'),
    ('aria-label="Džamija koja se gradi tačnim odgovorima"', 'aria-label="A mosque built with right answers"'),
    ('Odgovori tačno i izgradi novi dio džamije.', 'Answer correctly to build a new part of the mosque.'),
    ('<h2>🎉 Čestitamo, graditelju!</h2>', '<h2>🎉 Congratulations, builder!</h2>'),
    ('🕌 Izgradi novu džamiju', '🕌 Build a new mosque'),
    ('Radi i bez interneta nakon preuzimanja.', 'Works without the internet once downloaded.'),
    ("`Pitanje ${Math.min(index+1,deck.length)}/${deck.length}`", "`Question ${Math.min(index+1,deck.length)}/${deck.length}`"),
    ("`⭐ ${correct*10} bodova`", "`⭐ ${correct*10} points`"),
    ("`🧱 ${parts}/16 dijelova`", "`🧱 ${parts}/16 parts`"),
    ("parts===16?'🕌 Džamija je završena!':`Izgrađeno ${parts} od 16 dijelova`", "parts===16?'🕌 The mosque is finished!':`${parts} of 16 parts built`"),
    ("'Odaberi jedan od četiri odgovora'", "'Choose one of the four answers'"),
    ("ok?'✅ Tačno! Dodan je dio džamije.':'❌ Netačno. Pogledaj zeleni odgovor.'", "ok?'✅ Correct! A new part of the mosque is built.':'❌ Wrong. Look at the green answer.'"),
    ("'Gradnja završena'", "'Building finished'"),
    ("`Tačnih odgovora: ${correct} od ${deck.length}. Osvojeno ${correct*10} bodova. Izgrađeno ${Math.floor(correct/deck.length*16)} od 16 dijelova. ${correct===deck.length?'Izgradio/la si cijelu džamiju! 🕌':'Pokušaj ponovo da dovršiš cijelu džamiju!'}`",
     "`Right answers: ${correct} of ${deck.length}. You scored ${correct*10} points and built ${Math.floor(correct/deck.length*16)} of 16 parts. ${correct===deck.length?'You built the whole mosque! 🕌':'Try again to finish the whole mosque!'}`"),
    ("a.download='izgradi-svoju-dzamiju-A1.html'", "a.download='build-your-mosque-A1.html'"),
]


def transform(src):
    return _ilmihal_bank.translate(src)
