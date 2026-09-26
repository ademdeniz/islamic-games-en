# tajna-zivotinja (Secret Animal): direct mode. Built by tools/tr/tajna-zivotinja_build.py
# (question bank = the A3 bank of ilmihal-2-nivo-b1; English lines in tools/tr/tajna-zivotinja_bank.txt).
# The author credit is removed from the header line ("Nivo A3 • 321 pitanja • Pripremio ...") and the footer.
DELETE = ['<footer>Pripremio Abdo ef. Rekić</footer>']
ALLOW = []
# Short answer options whose English depends on the question (Bosnian case endings). Answers are checked by index
# (q.a), never by comparing text, so different English per question is safe.
ALLOW_INCONSISTENT = ['Ljudima', 'Melekima', 'Poslanicima', 'Oprati noge', 'Oprati ruke', 'Na putovanje']
