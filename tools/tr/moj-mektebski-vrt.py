# Moj mektebski vrt -> My Maktab Garden (solo: every right answer plants a flower – 30 flowers fill the garden).
# Repo: moj-mektebski-vrt1. Shared Ilmihal question bank (_ilmihal_bank.translate); UI strings below.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>Moj mektebski vrt</title>', '<title>My Maktab Garden</title>'),
    ('<h1>🌻 Moj mektebski vrt 🌻</h1><p class="sub">Uči Ilmihal • Tačnim odgovorima zasadi cvijeće!</p>',
     '<h1>🌻 My Maktab Garden 🌻</h1><p class="sub">Learn the Ilmihal • Plant flowers with right answers!</p>'),
    ('<label>📚 Nivo: <select id="level"><option value="ALL">Svih 6 nivoa</option>', '<label>📚 Level: <select id="level"><option value="ALL">All 6 levels</option>'),
    ('🔄 Novi vrt', '🔄 New garden'),
    ('aria-label="Vrt sa 30 gredica"', 'aria-label="A garden with 30 flower beds"'),
    ('<div class="qmeta" id="qmeta">Pitanja iz Ilmihala</div>', '<div class="qmeta" id="qmeta">Questions from the Ilmihal</div>'),
    ('<div class="foot">Pripremio Abdo ef. Rekić · Android i iPhone · Radi bez interneta</div>', '<div class="foot">Android and iPhone · Works without the internet</div>'),
    ("'🏆 Vrt je procvjetao!'", "'🏆 Your garden is in full bloom!'"),
    ("'Čestitamo! Zasadio/la si svih 30 cvjetova. Pokreni novi vrt za novu igru.'", "'Congratulations! You planted all 30 flowers. Start a new garden to play again.'"),
    ("'🌼 Bravo, mali vrtlaru znanja!'", "'🌼 Well done, little gardener of knowledge!'"),
    ("' · Pitanje '+pos+' od '+deck.length", "' · Question '+pos+' of '+deck.length"),
    ("'Odaberi tačan odgovor i zasadi cvijet.'", "'Choose the right answer and plant a flower.'"),
    ("'✅ Tačno! Izrastao je novi cvijet! 🌷'", "'✅ Correct! A new flower has grown! 🌷'"),
    ("'❌ Netačno. Pokušaj s narednim pitanjem.'", "'❌ Wrong. Try the next question.'"),
    ("a.download='index.html'", "a.download='my-maktab-garden.html'"),
]


def transform(src):
    return _ilmihal_bank.translate(src)
