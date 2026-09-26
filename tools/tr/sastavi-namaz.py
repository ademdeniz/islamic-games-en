# sastavi-namaz: table mode. The level data (const L) is rebuilt from STEPS/NAMES so every repeated
# step card gets the identical English text (the game compares cards with !==).
import json as _json
import os as _os

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

NAMES = {
    "Sabah – 2 rekata": "Fajr – 2 rak’ahs",
    "Podne – prvi sunnet (4 rekata)": "Dhuhr – first Sunnah (4 rak’ahs)",
    "Farz od 4 rekata": "Fard of 4 rak’ahs",
    "Akšam – farz (3 rekata)": "Maghrib – fard (3 rak’ahs)",
    "Ikindijski i jacijski sunnet (4 rekata)": "Asr and Isha Sunnah (4 rak’ahs)",
    "Vitr – 3 rekata": "Witr – 3 rak’ahs",
}
STEPS = {
    "Nijjet": "Niyyah (intention)",
    "Početni tekbir": "Opening takbir (Allahu akbar)",
    "1. rekat: Subhaneke → Euzu → Bismilla → Fatiha → sura": "1st rak’ah: Subhanaka → A’udhu → Bismillah → Al-Fatiha → surah",
    "Ruku → ispravljanje sa rukua → dvije sedžde": "Ruku (bowing) → standing up from ruku → two sajdahs (prostrations)",
    "2. rekat: Bismilla → Fatiha → sura": "2nd rak’ah: Bismillah → Al-Fatiha → surah",
    "Posljednje sjedenje: Ettehijjatu": "Last sitting: At-Tahiyyat",
    "Salavati": "Salawat (blessings on the Prophet)",
    "Dova": "Dua",
    "Selam na desnu stranu": "Salam to the right side",
    "Selam na lijevu stranu": "Salam to the left side",
    "Prvo sjedenje: Ettehijjatu": "First sitting: At-Tahiyyat",
    "3. rekat: Bismilla → Fatiha → sura": "3rd rak’ah: Bismillah → Al-Fatiha → surah",
    "4. rekat: Bismilla → Fatiha → sura": "4th rak’ah: Bismillah → Al-Fatiha → surah",
    "3. rekat: Bismilla → Fatiha": "3rd rak’ah: Bismillah → Al-Fatiha",
    "4. rekat: Bismilla → Fatiha": "4th rak’ah: Bismillah → Al-Fatiha",
    "Prvo sjedenje: Ettehijjatu → Salavati": "First sitting: At-Tahiyyat → Salawat",
    "3. rekat: Subhaneke → Euzu → Bismilla → Fatiha → sura": "3rd rak’ah: Subhanaka → A’udhu → Bismillah → Al-Fatiha → surah",
    "Tekbir": "Takbir (Allahu akbar)",
    "Kunut-dova": "Qunut dua",
}


def _levels():
    src = open(_os.path.join(_ROOT, 'work', 'sastavi-namaz.bs.html'), encoding='utf-8').read()
    i = src.index('const L=') + len('const L=')
    j = src.index(',$=x=>', i)
    bs = src[i:j]
    levels = _json.loads(bs)
    assert _json.dumps(levels, ensure_ascii=False) == bs
    en = [{"name": NAMES[l["name"]], "steps": [STEPS[s] for s in l["steps"]]} for l in levels]
    return bs, _json.dumps(en, ensure_ascii=False)


T = [
    ('content="Sastavi namaz"', 'content="Build the Salah"'),
    ('<title>Sastavi namaz</title>', '<title>Build the Salah</title>'),
    ('<h1>🕌 SASTAVI NAMAZ</h1>', '<h1>🕌 BUILD THE SALAH</h1>'),
    ('<div class="author">Pripremio Abdo ef. Rekić</div>', ''),
    ('📚 Baza zadataka i tačan redoslijed', '📚 Task list and correct order'),
    ('<div class="title">📚 Baza zadataka</div>', '<div class="title">📚 Task list</div>'),
    ('Ovdje možeš pregledati tačan redoslijed svih zadataka koji se koriste u igrici.',
     'Here you can see the correct order for every task used in the game.'),
    ('Zatvori bazu i vrati se na igru', 'Close the list and go back to the game'),
    ('⭐ Bodovi:', '⭐ Points:'),
    ('🏆 Nivo:', '🏆 Level:'),
    ('Svaka radnja je posebna kartica. Dodiruj kartice tačnim redoslijedom klanjanja.',
     'Each step of the Salah (prayer) is its own card. Tap the cards in the correct order of praying.'),
    ('↩ Vrati zadnju', '↩ Undo last'),
    ('✓ Provjeri', '✓ Check'),
    ('<h2>Bravo! Sastavio si namaze!</h2>', '<h2>Well done! You built all the prayers!</h2>'),
    ('Ukupno bodova:', 'Total points:'),
    ('Igraj ponovo', 'Play again'),
    ('"Složeno "+chosen.length+" od "+L[lv].steps.length+" radnji"',
     '"Placed "+chosen.length+" of "+L[lv].steps.length+" steps"'),
    ('Ovdje slaži redoslijed…', 'Build the order here…'),
    ('"Prvo složi sve radnje."', '"First place all the steps."'),
    ('"✅ Tačno! +10 bodova"', '"✅ Correct! +10 points"'),
    ('"❌ Provjeri karticu broj "+(wrong+1)+". Tu počinje greška. −3 boda"',
     '"❌ Check card number "+(wrong+1)+". The mistake starts there. −3 points"'),
]
T.insert(0, _levels())
