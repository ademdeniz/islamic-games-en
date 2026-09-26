# mektebski-detektiv-igra: direct mode. Built by tools/tr/mektebski-detektiv-igra_build.py
# (200 cases: names + 5 clues each, translated in tools/tr/mektebski-detektiv-igra_en[1-3].txt,
#  one line per unique Bosnian string, numbered in order of first appearance).
DELETE = ['<div class="footer">Pripremio Abdo ef. Rekić • Android & iPhone</div>']
ALLOW = []
# Clue text only (never compared): 'He' for Bilal (RA) / Hafiz, 'It' for Minaret / Mushaf / Qira'ah.
ALLOW_INCONSISTENT = ['Povezan je s ezanom.', "Povezan je s Kur'anom."]
