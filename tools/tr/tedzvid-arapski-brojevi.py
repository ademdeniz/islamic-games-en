# tedzvid-arapski-brojevi: Abdo ef. Rekić's "Learn the Arabic numbers 1–1000" (learn, table, quiz, match, memory, results).
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _rekic_ui import page  # noqa: E402

GAME = 'tedzvid-arapski-brojevi'
EXTRA = [
    ('Nauči arapske brojeve 1–1000', 'Learn the Arabic Numbers 1–1000'), ('Nauči arapske brojeve • ١–١٠٠٠', 'Learn the Arabic numbers • ١–١٠٠٠'),
    ('Uči redom', 'Learn in order'), ('Svi brojevi', 'All numbers'), ('Kviz', 'Quiz'), ('Spoji parove', 'Match pairs'), ('Memori', 'Memory'),
    ('Rezultati', 'Results'), ('Učenje brojeva', 'Learning the numbers'), ('Od', 'From'), ('Do', 'To'), ('Postavi raspon', 'Set the range'),
    ('Nasumičan broj', 'Random number'), ('🔊 Izgovori', '🔊 Say it'),
    ('Izgovor koristi glas uređaja ako je dostupan. Brojevi se prikazuju i bez interneta.', 'The number is spoken by your device’s voice, if it has one. The numbers show without internet too.'),
    ('Pregled brojeva 1–1000', 'All numbers 1–1000'), ('Pritisni broj da ga otvoriš u lekciji.', 'Tap a number to open it in the lesson.'),
    ('Prikaži', 'Show'), ('Svih 1000', 'All 1000'), ('Kviz: prepoznaj broj', 'Quiz: which number is it?'), ('Pitanja', 'Questions'),
    ('Pokreni kviz', 'Start the quiz'), ('Spoji arapski i naš broj', 'Match the Arabic number with ours'), ('Nova igra', 'New game'),
    ('Memori – pronađi par', 'Memory – find the pair'), ('Moji rezultati', 'My results'), ('Obriši rezultate', 'Delete my results'),
    ('Rezultati se čuvaju samo na ovom uređaju, u pregledniku.', 'Results are kept only on this device, in the browser.'),
    ('Preuzmi HTML za offline učenje', 'Download the page to learn offline'), ('Broj ', 'Number '), (' od ', ' from '), (' do ', ' to '),
    ('Izgovor nije podržan na ovom uređaju', 'This device cannot speak the number'), ('Kviz završen!', 'Quiz finished!'),
    ('Rezultat: ', 'Score: '), (' tačnih odgovora', ' right answers'), ('Koji je ovo broj?', 'Which number is this?'), ('Pitanje ', 'Question '),
    (' • Tačno ', ' • Right '), (' • Netačno ', ' • Wrong '), ('Tačno!', 'Correct!'), ('Tačan odgovor je ', 'The right answer is '),
    ('Odaberi najmanje dva broja', 'Choose at least two numbers'), ('Spojeno ', 'Matched '), (' • Greške ', ' • Mistakes '),
    ('Bravo! Svi parovi su spojeni!', 'Well done! All pairs are matched!'), ('Pronađeno ', 'Found '), (' • Pokušaji ', ' • Tries '),
    ('Bravo! Memori završen!', 'Well done! Memory finished!'), ('<p>Odigranih kvizova: <b>', '<p>Quizzes played: <b>'),
    ('</b></p><p>Tačnih odgovora u kvizovima: <b>', '</b></p><p>Right answers in quizzes: <b>'), ('</b></p><p>Uspješnost kviza: <b>', '</b></p><p>Quiz success: <b>'),
    ('%</b></p><p>Igara spajanja: <b>', '%</b></p><p>Matching games: <b>'), ('</b> • Ukupno grešaka: <b>', '</b> • Mistakes in total: <b>'),
    ('</b></p><p>Memori igara: <b>', '</b></p><p>Memory games: <b>'), ('</b> • Pokušaji: <b>', '</b> • Tries: <b>'),
    ('Obrisati sve rezultate na ovom uređaju?', 'Delete all results on this device?'),
]
DELETE, _ARABIC, transform, BRAND_FIT = page(GAME, EXTRA)
ALLOW_ARABIC = ['the Arabic (Eastern Arabic) numerals ١٢٣ are what the page teaches']
