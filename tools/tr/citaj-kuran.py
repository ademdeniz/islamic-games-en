import os
import re

ARR = open(os.path.join(os.path.dirname(__file__), '_citaj_arr.txt'), encoding='utf-8').read()

T = [
    ('<title>Čitaj za učačem – El-Bekare 17–24</title>', '<title>Read Along with the Reciter – Al-Baqarah 17–24</title>'),
    ('<h1>📖 Čitaj za učačem</h1><div class="sub">El-Bekare • ajeti 17–24</div>',
     '<h1>📖 Read Along with the Reciter</h1><div class="sub">Al-Baqarah • ayahs 17–24</div>'),
    ('#arabic{direction:rtl;text-align:center;font-family:"Noto Naskh Arabic","Traditional Arabic",serif;font-size:clamp(38px,9vw,66px);line-height:1.9;min-height:230px;display:flex;align-items:center;justify-content:center}',
     '#arabic{text-align:center;min-height:230px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px}'
     '#arabic .tr{font-size:clamp(22px,5vw,32px);font-weight:800;line-height:1.5}'
     '#arabic .en{font-size:clamp(16px,3.6vw,20px);font-style:italic;color:#5a4d38;line-height:1.5}'
     '.credit{text-align:center;font-size:12px;color:#8a7c64;margin-top:8px}'),
    ('Pritisni „Učač čita“, zatim pročitaj isti dio.', 'Press “Reciter reads”, then read the same part yourself.'),
    ('🔊 UČAČ ČITA', '🔊 RECITER READS'), ('🔁 POSLUŠAJ PONOVO', '🔁 LISTEN AGAIN'), ('⏸ ZAUSTAVI', '⏸ STOP'),
    ('PROČITAO/LA SAM — SLJEDEĆI ➜', 'I READ IT — NEXT ➜'),
    ('Dijete prati tekst očima dok učač uči, zatim isti dio čita naglas.',
     'The child follows the text with their eyes while the reciter recites, then reads the same part out loud.</div>'
     '<div class="credit">Transliteration &amp; English translation (Sahih International) via AlQuran.cloud · Recitation: Mishary Rashid Alafasy'),
    ('document.getElementById("arabic").textContent=x[i][1];',
     'document.getElementById("arabic").innerHTML=\'<span class="tr">\'+x[i][1]+\'</span><span class="en">\'+x[i][2]+\'</span>\';'),
    ('"Ajet "+x[i][0]+" • "+(i+1)+" od "+x.length', '"Ayah "+x[i][0]+" • "+(i+1)+" of "+x.length'),
    ("'Pritisni „Učač čita“, prati tekst, pa ga pročitaj naglas.'", "'Press “Reciter reads”, follow the text, then read it out loud.'"),
    ('"👂 Slušaj i prati tekst očima…"', '"👂 Listen and follow the text with your eyes…"'),
    ('"🗣️ Sada ti pročitaj isti ajet naglas."', '"🗣️ Now you read the same ayah out loud."'),
    ('"Zvuk nije pokrenut. Provjeri internet vezu."', '"The audio did not start. Check your internet connection."'),
    ('"🌟 Bravo! Pročitao/la si ajete 17–24."', '"🌟 Well done! You read ayahs 17–24."'),
]


def transform(src):
    return re.sub(r'const x=\[.*?\]\];', lambda m: ARR, src, count=1, flags=re.S)
STRUCTURAL = "Arabic ayahs replaced by transliteration + translation (new data array and render code)"
