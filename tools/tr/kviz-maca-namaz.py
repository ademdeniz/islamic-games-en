# kviz-maca-namaz: table mode. maca-pripreme-za-namaz reuses this table (the two games share all text).
T = [
    ('<title>Pripreme za namaz – Pomozimo maci</title>', '<title>Preparing for Salah – Let’s Help the Kitty</title>'),
    ('<div id="autor">Pripremio Abdo ef. Rekić</div>', ''),
    ('<div id="msg">Pripreme za namaz – pronađi parove.</div>', '<div id="msg">Preparing for Salah (prayer) – find the pairs.</div>'),
    ("M.textContent=(L<2?'Pripreme za namaz':'Sastavni dijelovi namaza')+' – pronađi 4 para.'",
     "M.textContent=(L<2?'Preparing for Salah':'Parts of Salah')+' – find 4 pairs.'"),
    # level 1
    ("['Uvjeti za namaz',0],['6 uvjeta',0]", "['Conditions of Salah',0],['6 conditions',0]"),
    ("['Čistoća tijela, odijela i mjesta',1],['1. uvjet za namaz',1]", "['Clean body, clothes and place',1],['1st condition of Salah',1]"),
    ("['Propisno odijevanje',2],['3. uvjet za namaz',2]", "['Covering the body properly',2],['3rd condition of Salah',2]"),
    ("['Okrenuti se prema Kibli',3],['5. uvjet za namaz',3]", "['Facing the Qiblah',3],['5th condition of Salah',3]"),
    # level 2
    ("['Abdest',0],['Vjersko pranje',0]", "['Wudu',0],['Ablution (washing for prayer)',0]"),
    ("['Gusul',1],['Kupanje cijelog tijela',1]", "['Ghusl',1],['Washing the whole body',1]"),
    ("['Tejemum',2],['Simbolično čišćenje',2]", "['Tayammum',2],['Symbolic purification',2]"),
    ("['Kibla',3],['Pravac Kabe',3]", "['Qiblah',3],['Direction of the Ka’bah',3]"),
    # level 3
    ("['Nijet',0],['6. uvjet za namaz',0]", "['Niyyah (intention)',0],['6th condition of Salah',0]"),
    ("['Početni tekbir',1],['Allahu ekber',1]", "['Opening takbir',1],['Allahu akbar',1]"),
    ("['Kijam',2],['Stajanje u namazu',2]", "['Qiyam',2],['Standing in Salah',2]"),
    ("['Kiraet',3],['Učenje Kur’ana',3]", "['Qira’ah',3],['Reciting the Qur’an',3]"),
    # level 4
    ("['Ruku',0],['Pregibanje',0]", "['Ruku’',0],['Bowing',0]"),
    ("['Sedžda',1],['Spuštanje čela na tlo',1]", "['Sajdah (Sujud)',1],['Putting the forehead on the ground',1]"),
    ("['Ka’de-i ehire',2],['Posljednje sjedenje',2]", "['Qa’dah akhirah',2],['The final sitting',2]"),
    ("['Namaski ruknovi',3],['Sastavni dijelovi namaza',3]", "['Arkan of Salah',3],['Parts of Salah',3]"),
    # feedback
    ("'✓ Tačno! Još '+(4-F)+' para.'", "'✓ Correct! Pairs left: '+(4-F)+'.'"),
    ("'✗ Netačno. Pokušaj ponovo.'", "'✗ Not quite. Try again.'"),
    ("'🐾 Bravo! Maca se okreće...'", "'🐾 Well done! The kitty turns around...'"),
    ("'🐱 Mau! Mau!'", "'🐱 Meow! Meow!'"),
    ("'🏡 Mau! Mau! Maca je stigla kući! ⭐ '+S+' bodova'", "'🏡 Meow! Meow! The kitty made it home! ⭐ '+S+' points'"),
]
