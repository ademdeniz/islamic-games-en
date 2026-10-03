# Tajna mektebska šifra -> Secret Maktab Code (solo: every right answer reveals a letter of a hidden message;
# guess the whole message for a bonus). Shared Ilmihal question bank (_ilmihal_bank.translate); UI strings and the
# 58 hidden messages (English sayings in place of the Bosnian ones – children type them in) below.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>Tajna mektebska šifra</title>', '<title>Secret Maktab Code</title>'),
    ('<h1>🔐 Tajna mektebska šifra</h1><p class="sub">Odgovori tačno i otključaj skrivenu poruku!</p>',
     '<h1>🔐 Secret Maktab Code</h1><p class="sub">Answer correctly and unlock the hidden message!</p>'),
    ('aria-label="Odabir nivoa"><option value="ALL">Svih 6 nivoa</option>', 'aria-label="Choose a level"><option value="ALL">All 6 levels</option>'),
    ('🔄 Nova igra', '🔄 New game'), ('aria-label="Zvuk"', 'aria-label="Sound"'),
    ('<div class="mission" id="mission">Pronađi tajnu šifru!</div>', '<div class="mission" id="mission">Find the secret code!</div>'),
    ('aria-label="Upiši tajnu šifru" placeholder="✍️ Upiši cijelu šifru"', 'aria-label="Type the secret code" placeholder="✍️ Type the whole code"'),
    ('🔓 Pogodi</button>', '🔓 Guess</button>'),
    ('<p class="foot">Pripremio Abdo ef. Rekić · Radi bez interneta</p>', '<p class="foot">Works without the internet</p>'),
    ('["ZNANJE JE BLAGO", "MEKTEB JE RADOST", "UČENJE JE USPJEH", "DOBROTA JE SNAGA", "ČUVAJ SVOJ NAMAZ", "ILMIHAL JE ZNANJE", "LIJEPA RIJEČ JE SADAKA", "BUDI DOBAR DRUG", "ALLAH JE JEDAN", "ALLAH SVE VIDI", "ALLAH SVE ZNA", "ALLAH NAS VOLI", "ISLAM JE NAŠA VJERA", "KUR\'AN JE ALLAHOVA KNJIGA", "KUR\'AN JE UPUTA", "NAMAZ JE IBADET", "NAMAZ JE NAŠA OBAVEZA", "ČUVAJ SVOJ NAMAZ", "ABDEST JE ČISTOĆA", "ČISTOĆA JE DIO IMANA", "POST JE IBADET", "RAMAZAN JE MUBAREK", "BAJRAM JE RADOST", "DŽAMIJA JE MJESTO IBADETA", "MEKTEB JE ŠKOLA ZNANJA", "UČI SVOJU VJERU", "VOLI SVOJ MEKTEB", "ZNANJE JE SVJETLO", "BUDI VRIJEDAN UČENIK", "UČI SVAKOGA DANA", "POŠTUJ SVOGA MUALLIMA", "SLUŠAJ SVOJE RODITELJE", "POŠTUJ STARIJE", "VOLI MLAĐE", "POMOZI PRIJATELJU", "BUDI DOBAR DRUG", "GOVORI ISTINU", "NE GOVORI LAŽI", "ČUVAJ TUĐE STVARI", "ISPUNI OBEĆANJE", "BUDI POŠTEN", "BUDI STRPLJIV", "BUDI ZAHVALAN", "ČINI DOBRA DJELA", "DOBRO SE DOBRIM VRAĆA", "OSMIJEH JE SADAKA", "NAZOVI SELAM", "ODGOVORI NA SELAM", "BISMILLA PRIJE JELA", "ZAHVALI ALLAHU", "UČI DOVE", "VOLI SVOJE RODITELJE", "ČUVAJ SVOJU PORODICU", "POMAŽI KOMŠIJAMA", "ČUVAJ PRIRODU", "NE RASIPAJ VODU", "ČUVAJ SVOJ JEZIK", "BUDI PRIMJER DOBROTE"]',
     '["KNOWLEDGE IS A TREASURE", "THE MAKTAB IS A JOY", "LEARNING IS SUCCESS", "KINDNESS IS STRENGTH", "GUARD YOUR SALAH", "THE ILMIHAL IS KNOWLEDGE", "A KIND WORD IS SADAQAH", "BE A GOOD FRIEND", "ALLAH IS ONE", "ALLAH SEES EVERYTHING", "ALLAH KNOWS EVERYTHING", "ALLAH LOVES US", "ISLAM IS OUR RELIGION", "THE QUR\'AN IS ALLAH\'S BOOK", "THE QUR\'AN IS GUIDANCE", "SALAH IS WORSHIP", "SALAH IS OUR DUTY", "GUARD YOUR SALAH", "WUDU IS CLEANLINESS", "CLEANLINESS IS PART OF IMAN", "FASTING IS WORSHIP", "RAMADAN IS BLESSED", "EID IS A JOY", "THE MOSQUE IS A PLACE OF WORSHIP", "THE MAKTAB IS A SCHOOL OF KNOWLEDGE", "LEARN YOUR RELIGION", "LOVE YOUR MAKTAB", "KNOWLEDGE IS LIGHT", "BE A HARDWORKING STUDENT", "LEARN EVERY DAY", "RESPECT YOUR TEACHER", "LISTEN TO YOUR PARENTS", "RESPECT YOUR ELDERS", "BE KIND TO THE YOUNGER ONES", "HELP A FRIEND", "BE A GOOD FRIEND", "TELL THE TRUTH", "DO NOT TELL LIES", "LOOK AFTER OTHER PEOPLE\'S THINGS", "KEEP YOUR PROMISE", "BE HONEST", "BE PATIENT", "BE THANKFUL", "DO GOOD DEEDS", "GOOD IS REPAID WITH GOOD", "A SMILE IS SADAQAH", "SAY SALAM", "ANSWER THE SALAM", "BISMILLAH BEFORE EATING", "THANK ALLAH", "LEARN DUAS", "LOVE YOUR PARENTS", "LOOK AFTER YOUR FAMILY", "HELP YOUR NEIGHBOURS", "LOOK AFTER NATURE", "DO NOT WASTE WATER", "GUARD YOUR TONGUE", "BE AN EXAMPLE OF KINDNESS"]'),
    ("'Šifra '+round+' / '+SECRETS.length+' · Tačan odgovor otkriva slovo'", "'Code '+round+' / '+SECRETS.length+' · A right answer reveals a letter'"),
    ("'🎉 Otključana šifra: '+secret", "'🎉 Code unlocked: '+secret"),
    ("'Šifra '+round+' riješena!'", "'Code '+round+' solved!'"),
    ("'Čestitamo! Otključao/la si tajnu mektebsku šifru.'", "'Congratulations! You unlocked the secret maktab code.'"),
    ("'🔐 Sljedeća tajna šifra'", "'🔐 Next secret code'"),
    ("'Bravo! Nastavi otkrivati nove šifre.'", "'Well done! Keep unlocking new codes.'"),
    ("' · Pitanje '+pos+' / '+deck.length", "' · Question '+pos+' / '+deck.length"),
    ("'Odgovori na pitanje ili pogodi cijelu šifru!'", "'Answer the question or guess the whole code!'"),
    ("toLocaleUpperCase('bs')", "toLocaleUpperCase('en')"),
    ("'✍️ Prvo upiši cijelu šifru.'", "'✍️ Type the whole code first.'"),
    ("'🎉 Bravo! Pogodio/la si: '+secret", "'🎉 Well done! You guessed it: '+secret"),
    ("'🌟 Bonus +20! Sljedeća šifra stiže automatski.'", "'🌟 Bonus +20! The next code is on its way.'"),
    ("'❌ Šifra nije tačna. Pokušaj ponovo ili odgovaraj na pitanja.'", "'❌ That’s not the code. Try again or answer more questions.'"),
    ("'✅ Tačno! Otkriveno je novo slovo.'", "'✅ Correct! A new letter is revealed.'"),
    ("'❌ Netačno. Tačan odgovor je označen zeleno.'", "'❌ Wrong. The right answer is shown in green.'"),
    ("a.download='index.html'", "a.download='secret-maktab-code.html'"),
]


def transform(src):
    return _ilmihal_bank.translate(src)
