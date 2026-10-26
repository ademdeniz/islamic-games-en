"""Shared helpers for Abdo ef. Rekić's recitation pages (surahs, Al-Baqarah, duas): one English table for the buttons
and messages they all share, and the author credit / analytics tag to remove.

A page's table does:   from _rekic_ui import page;  DELETE, ALLOW_ARABIC, transform, BRAND_FIT = page(GAME, EXTRA)
transform() replaces whole strings only – a Bosnian string is changed where it is a complete HTML text node,
attribute value or JS string (or the text part of a template literal), never inside code or a longer string.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# The page keeps the Qur’an / dua in Arabic script on purpose (like our Read Along): it is a recitation page.
ARABIC_REASON = ['recitation page – the Arabic text is what the child reads along with the reciter']

UI = [
    # buttons
    ('▶ Uči ajet', '▶ Recite ayah'), ('▶ Uči redom', '▶ Recite all in order'), ('▶ Uči sve redom', '▶ Recite all in order'),
    ('▶ Uči sve ajete redom', '▶ Recite all ayahs in order'), ('▶ Uči Bismillu', '▶ Recite the Bismillah'),
    ('▶ Uči bismilla', '▶ Recite the Bismillah'),
    ('▶ Uči', '▶ Recite'),
    ('◀ Prethodni', '◀ Previous'), ('Sljedeći ▶', 'Next ▶'), ('■ Zaustavi redom', '■ Stop'), ('■ Zaustavi', '■ Stop'),
    ('■ Zaustavi učenje', '■ Stop reciting'), ('⏸ Pauza', '⏸ Pause'), ('Ⅱ Pauza', 'Ⅱ Pause'), ('▶ Nastavi', '▶ Continue'),
    ('↻ Ponovi ajet', '↻ Repeat ayah'), ('▶ Ponovi', '▶ Repeat'), ('↺ Ponovi', '↺ Repeat'), ('🔁 Ponavljaj', '🔁 Repeat'),
    ('Ponavljanje', 'Repeat'), ('Stalno', 'Non-stop'),
    ('⛶ Cijeli ekran', '⛶ Full screen'), ('⛶ Izađi iz cijelog ekrana', '⛶ Exit full screen'), ('⛶ Obični prikaz', '⛶ Normal view'),
    ('⛶ Veliki prikaz (preglednik ograničava)', '⛶ Big view (the browser limits it)'),
    ('⬇ Preuzmi HTML', '⬇ Download page'), ('⬇ Preuzmi', '⬇ Download'), ('⬇ DOWNLOADS', '⬇ DOWNLOAD'),
    *[(f'▶ Uči {n}. ajet', f'▶ Recite ayah {n}') for n in range(1, 13)],
    *[(f'{n}. ajet', f'Ayah {n}') for n in range(1, 13)],
    ('Ajet ', 'Ayah '), ('Ajet 1 / 6', 'Ayah 1 / 6'),
    ('↶ 3 sekunde', '↶ 3 seconds'), ('▶ Pusti / pauziraj', '▶ Play / pause'), ('▶ Uči redom: DA', '▶ Recite in order: ON'),
    ('▶ Uči redom: ', '▶ Recite in order: '), ('DA', 'ON'), ('NE', 'OFF'), ('UKLJ.', 'ON'), ('ISKLJ.', 'OFF'),
    ('🔁 Ponavljanje: ', '🔁 Repeat: '), ('🔁 Ponavljanje: NE', '🔁 Repeat: OFF'), ('🔁 Ponavljanje: ISKLJ.', '🔁 Repeat: OFF'),
    ('🔁 Ponavljanje ajeta: ', '🔁 Repeat ayah: '), ('🔁 Ponavljanje ajeta: NE', '🔁 Repeat ayah: OFF'),
    ('⬇ Downloads MP3', '⬇ Download MP3'), ('⬇ Downloads HTML', '⬇ Download page'), ('⬇ Preuzmi MP3 ajeta', '⬇ Download the ayah’s MP3'),
    ('⬇ Downloads – preuzmi cijelu lekciju', '⬇ Download the whole lesson'), ('↺ Od početka', '↺ From the start'),
    ('Uči se ajet ', 'Reciting ayah '), ('Riječ ', 'Word '), (' s • riječ ', ' s • word '), (' ajeta.', ' ayahs.'),
    ('Pokrenite zvuk ponovnim dodirom.', 'Tap again to start the sound.'),
    ('Za cijeli ekran otvorite lekciju u pregledniku.', 'For full screen, open the lesson in the browser.'),
    ('Preglednik ne dopušta skrivanje sistemskih traka.', 'The browser does not let the page hide the system bars.'),
    ('Snimak se ne može pokrenuti: ', 'The recording cannot start: '),
    ('Interaktivno učenje Kur’ana • označavanje riječi', 'Learning the Qur’an • each word lights up'),
    ('Učenje prema podešenim vremenima riječi · Snimak obuhvata sva tri ajeta.', 'The words light up with the recitation · The recording has all three ayahs.'),
    # the author's timing tool on the Al-Baqarah pages
    ('⚙ Podešavanje žutog praćenja', '⚙ Set up the yellow word tracking'), ('Vrati posljednju oznaku', 'Undo the last mark'),
    ('Označeni JSON kopirajte ručno.', 'Copy the marked JSON by hand.'), ('Vrijeme (s):', 'Time (s):'), ('Primijeni', 'Apply'),
    ('Učitaj JSON', 'Load JSON'), ('Prikaži JSON', 'Show JSON'), ('Kopiraj JSON', 'Copy JSON'), ('⬇ Sačuvaj JSON', '⬇ Save JSON'),
    ('Vrijeme (s): ', 'Time (s): '), ('Prvo dodirnite riječ.', 'First tap a word.'), ('Dodirnite riječ.', 'Tap a word.'), ('JSON kopiran.', 'JSON copied.'),
    ('JSON pripremljen za preuzimanje. Ako preuzimanje ne radi, koristite Kopiraj JSON.', 'The JSON is ready to download. If the download does not work, use Copy JSON.'),
    ('Podešavanje sačuvano.', 'Timings saved.'), ('Učitano podešavanje za ', 'Timings loaded for '), ('Postavi trenutno vrijeme', 'Use the current time'),
    ('Posljednja oznaka vraćena.', 'Last mark undone.'), ('Neispravna JSON datoteka.', 'Invalid JSON file.'),
    ('Početna vremena su okvirna. Podesite ih prema audiozapisu.', 'The first timings are rough. Set them to match the recording.'),
    ('Pustite učenje i dodirnite arapsku riječ tačno kada je učač izgovara. Vrijeme se odmah pamti. Možete odabrati riječ i ručno promijeniti sekundu.',
     'Play the recitation and tap each Arabic word exactly when the reciter says it. The time is saved at once. You can also choose a word and change the second by hand.'),
    # messages
    ('Uči se Bismilla', 'Reciting the Bismillah'), ('Učenje završeno', 'Finished'), ('Učenje završeno.', 'Finished.'),
    ('Učenje ajeta ', 'Reciting ayah '), ('Zaustavljeno', 'Stopped'), ('Spremno za učenje.', 'Ready to recite.'),
    ('Zvuk nije pokrenut. Dodirnite Uči ajet.', 'The sound did not start. Tap Recite ayah.'),
    ('Zvuk nije pokrenut: ', 'The sound did not start: '),
    ('Dodirnite dugme za pokretanje zvuka', 'Tap the button to start the sound'),
    ('Dodirnite dugme još jednom za pokretanje zvuka.', 'Tap the button once more to start the sound.'),
    ('Dodirnite Uči ajet za pokretanje zvuka.', 'Tap Recite ayah to start the sound.'),
    ('Za pokretanje zvuka dodirnite Uči ajet.', 'To start the sound, tap Recite ayah.'),
    ('Dodirnite Uči ajet da omogućite zvuk: ', 'Tap Recite ayah to turn on the sound: '),
    ('Nije moguće pokrenuti Bismillu', 'Could not start the Bismillah'),
    ('Preglednik ne dopušta cijeli ekran. Otvorite u Chromeu ili Safari.', 'This browser does not allow full screen. Open the page in Chrome or Safari.'),
    ('Preglednik ne dopušta puni ekran; otvorite HTML u Chromeu ili Safariju.', 'This browser does not allow full screen. Open the page in Chrome or Safari.'),
    ('Cijeli ekran nije dozvoljen u ovom pregledniku.', 'Full screen is not allowed in this browser.'),
    ('Preglednik ograničava skrivanje sistemskih traka.', 'The browser does not let the page hide the system bars.'),
    (' • Okrenite telefon vodoravno za veći prikaz', ' • Turn the phone sideways for a bigger view'),
    ('Dodirnite broj ajeta za odabir. Zvuk je ugrađen i radi bez interneta.', 'Tap an ayah number to choose it. The sound is built in and works without internet.'),
    ('Svaki ajet posebno · označavanje riječi', 'One ayah at a time · each word lights up'),
    ('Bismilla · početak sure', 'Bismillah · the start of the surah'), ('Bismilla · prije prvog ajeta', 'Bismillah · before the first ayah'),
    ('Bismilla', 'Bismillah'), ('Greška: ', 'Error: '),
    *[(f'Bismilla + {n} ajeta • riječ po riječ', f'Bismillah + {n} ayahs • word by word') for n in range(2, 9)],
    ('Bismilla + 6 ajeta • svaka riječ u svom polju • riječ po riječ', 'Bismillah + 6 ayahs • each word in its own box • word by word'),
    # the author's tool for setting the word timings (hidden for children, translated anyway)
    ('👆 Uključi podešavanje dodirom', '👆 Set the word timings by tapping'), ('✓ Isključi podešavanje', '✓ Turn timing setup off'),
    ('Podešavanje isključeno', 'Timing setup off'), ('Podešavanje učitano', 'Timings loaded'),
    ('Podešavanje uključeno – pokrenite ajet i dodirujte riječi', 'Timing setup on – start the ayah and tap the words'),
    ('Pokrenite zvuk i dodirnite svaku riječ kada počne.', 'Start the sound and tap each word as it begins.'),
    ('JSON učitan', 'JSON loaded'), ('Neodgovarajući JSON', 'This JSON does not fit'), ('Pogrešan JSON', 'Wrong JSON'),
    ('Zabilježeno: ', 'Recorded: '), (' na ', ' of '),
    ('Sve riječi označene. Pritisni 💾 SAČUVAJ.', 'All words marked. Press 💾 SAVE.'),
    ('Prvo pokreni START i označi riječi.', 'First press START and mark the words.'),
    ('Označeno ', 'Marked '), (' riječi. Označi sve.', ' words. Mark them all.'),
    ('Slušaj i dodiruj riječi redom…', 'Listen and tap the words in order…'),
    ('✅ Vremena ovog ajeta su sačuvana na ovom telefonu.', '✅ This ayah’s timings are saved on this phone.'),
]

_CREDIT = re.compile(r'<(footer|div|p|span|header|small)\b[^>]*>\s*Pripremio:?\s*Abdo ef\. Rekić[^<]*</\1>\s*')
_CREDIT_B = re.compile(r'<(header|div|footer|p)\b[^>]*>\s*<(b|strong)>\s*Pripremio:?\s*Abdo ef\. Rekić[^<]*</\2>\s*</\1>\s*')
_PORTAL = re.compile(r'<a href="https://rekicabdo-bihac\.github\.io/mektebski-portal/">[^<]*</a>')   # link to his Bosnian portal
_GA = re.compile(r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=[^"]+"></script>\s*'
                 r'<script>window\.dataLayer=window\.dataLayer\|\|\[\];function gtag\(\)\{dataLayer\.push\(arguments\)\}'
                 r'gtag\("js",new Date\(\)\);gtag\("config","[^"]+"\);</script>')


def original(game):
    d = os.path.join(ROOT, 'original', game)
    return open(os.path.join(d, 'index.html'), encoding='utf-8').read()


def deletions(game):
    """The author credit element and his Google Analytics tag (our pages must not report children's visits to it)."""
    src = original(game)
    return [m.group(0) for r in (_CREDIT, _CREDIT_B, _PORTAL, _GA) for m in r.finditer(src)]


def make_transform(pairs):
    pairs = sorted(dict(pairs).items(), key=lambda p: -len(p[0]))   # longest first

    def transform(src):
        for bs, en in pairs:
            pat = re.compile(r'([>\'"`}][ \t]*)' + re.escape(bs) + r'(?=[ \t]*[<\'"`$])')
            src = pat.sub(lambda m: m.group(1) + en, src)
        return src
    return transform


def fits_screen(game):
    """A one-screen app (no scrolling): skel.build then fits it under the logo header (BRAND_FIT)."""
    return bool(re.search(r'html,\s*body\s*\{[^}]*overflow:hidden', original(game)))


def page(game, extra=()):
    """DELETE, ALLOW_ARABIC, transform and BRAND_FIT for one page: the shared UI table plus the page's own strings."""
    return deletions(game), ARABIC_REASON, make_transform(list(UI) + list(extra)), fits_screen(game)


def _span_end(src, i):
    """Index just past the </span> that closes the <span ...> whose content starts at i (nested spans counted)."""
    depth = 1
    for m in re.compile(r'<span\b[^>]*>|</span>').finditer(src, i):
        depth += 1 if m.group(0) != '</span>' else -1
        if depth == 0:
            return m.start(), m.end()
    raise ValueError('unclosed span')


def word_pairs(game, words):
    """T pairs for transliteration pages: {"v0w1": "English inner HTML", ...} → (original word box, English word box).
    Only the text changes; the coloured letter spans inside must stay the same (tests/test_games.py checks it)."""
    src = original(game)
    out = []
    for wid, en in words.items():
        m = re.search(r'<span class="word[^"]*"[^>]*\bid="%s">' % wid, src)
        assert m, f'{game}: no word box {wid}'
        end, close = _span_end(src, m.end())
        out.append((src[m.start():close], m.group(0) + en + '</span>'))
    return out
