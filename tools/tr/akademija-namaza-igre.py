# akademija-namaza-igre: table mode. Sequencing puzzle — put the steps of each Salah in order.
# JSON strings are matched with their quotes so short strings never hit longer ones.
# "group" keys that were Bosnian get exactly the same English as the matching "name" (compared with !==).
T = [
    ('content="Akademija namaza"', 'content="Salah Academy"'),
    ('<title>Akademija namaza – slagalice</title>', '<title>Salah Academy – Puzzles</title>'),
    ('<h1>🕌 Akademija namaza</h1><b>Složi pravilan redoslijed namaza</b>',
     '<h1>🕌 Salah Academy</h1><b>Put the steps of Salah (prayer) in the right order</b>'),
    ('>← Lekcije<', '>← Lessons<'),
    ('<footer>Pripremio Abdo ef. Rekić</footer>', ''),
    # lesson titles
    ('"Sabahski sunnet"', '"Fajr Sunnah"'),
    ('"Sabahski farz"', '"Fajr Fard"'),
    ('"Podnevski sunnet"', '"Dhuhr Sunnah"'),
    ('"Podnevski farz"', '"Dhuhr Fard"'),
    ('"Ikindijski i jacijski sunnet"', '"Asr and Isha Sunnah"'),
    ('"Akšamski farz"', '"Maghrib Fard"'),
    ('"Vitr-namaz"', '"Witr Salah"'),
    # steps (name / group)
    ('"Iftitahi tekbir"', '"Opening Takbir"'),
    ('"1. rekat – kijam"', '"Rak’ah 1 – Qiyam (standing)"'),
    ('"2. rekat – kijam"', '"Rak’ah 2 – Qiyam (standing)"'),
    ('"3. rekat – kijam"', '"Rak’ah 3 – Qiyam (standing)"'),
    ('"4. rekat – kijam"', '"Rak’ah 4 – Qiyam (standing)"'),
    ('"Ruku\'"', '"Ruku’ (bowing)"'),
    ('"Povratak sa ruku\'a"', '"Rising from Ruku’"'),
    ('"Dvije sedžde"', '"Two Sajdahs (prostrations)"'),
    ('"Prvo sjedenje"', '"First sitting"'),
    ('"Posljednje sjedenje"', '"Final sitting"'),
    ('"Selam desno i lijevo"', '"Salam to the right and left"'),
    ('"Tekbir za kunut"', '"Takbir for Qunut"'),
    ('"Kunut-dova"', '"Qunut dua"'),
    # recitations
    ('"Allahu ekber"', '"Allahu akbar"'),
    ('"Subhaneke • Euzu • Bismilla • Fatiha • sura"', '"Subhanaka • A’udhu billah • Bismillah • Al-Fatiha • surah"'),
    ('"Bismilla • Fatiha • sura"', '"Bismillah • Al-Fatiha • surah"'),
    ('"Bismilla • Fatiha"', '"Bismillah • Al-Fatiha"'),
    ('"Subhane rabbijel-azim"', '"Subhana Rabbiyal-Azim"'),
    ('"Semi\'allahu limen hamideh • Rabbena lekel-hamd"', '"Sami’Allahu liman hamidah • Rabbana lakal-hamd"'),
    ('"Dvije sedžde sa sjedenjem između"', '"Two prostrations with a short sitting in between"'),
    ('"Ettehijjatu • Salavati • dova"', '"At-Tahiyyat • Salawat • dua"'),
    ('"Ettehijjatu • Salavati"', '"At-Tahiyyat • Salawat"'),
    ('"Ettehijjatu"', '"At-Tahiyyat"'),
    ('"Es-selamu alejkum ve rahmetullah"', '"As-salamu alaykum wa rahmatullah"'),
    ('"Allahu ekber • podigni ruke pa ih sveži"', '"Allahu akbar • raise your hands, then fold them again"'),
    ('"Prouči kunut-dovu"', '"Recite the Qunut dua"'),
    # UI messages
    ('${l.steps.length} koraka', '${l.steps.length} steps'),
    ("'Počni sa <b>iftitahi tekbirom</b>. Jedna greška = ispočetka.'",
     "'Start with the <b>opening Takbir</b>. One mistake = start over.'"),
    ("'❌ Pogrešno — lekcija kreće ispočetka.'", "'❌ Wrong — the lesson starts over.'"),
    ("'🌟 Mašallah! Lekcija je završena tačno.'", "'🌟 MashaAllah! You finished the lesson correctly.'"),
]
ALLOW = []
