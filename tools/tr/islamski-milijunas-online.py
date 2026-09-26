# Islamski milijunaš (online) -> Islamic Millionaire (online).
# Same question bank and game UI as islamski-milijunas: reuse that table + bank, then add the online/login strings.
# Role values ('ucenik', 'mualim', 'admin') and database/RPC names are code and stay unchanged.
import os
import runpy

_base = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'islamski-milijunas.py'))
transform = _base['transform']
DELETE = _base['DELETE']
ALLOW = _base['ALLOW']

_ONLINE_ONLY = {
    'Offline kviz • radi bez interneta',  # footer differs in the online version
    "fail('Vrijeme je isteklo!')",
}
T = [p for p in _base['T'] if p[0] not in _ONLINE_ONLY] + [
    ("fail('Vrijeme je isteklo!')", "fail('Time is up!')"),
    ('🌐 ONLINE / PRIJAVA', '🌐 ONLINE / LOG IN'),
    ('<div class="big" style="text-align:center">ONLINE PRIJAVA</div>',
     '<div class="big" style="text-align:center">ONLINE LOG IN</div>'),
    ('<h3>Prijava / registracija</h3>', '<h3>Log in / sign up</h3>'),
    ('placeholder="Ime i prezime"', 'placeholder="First and last name"'),
    ('placeholder="Lozinka (najmanje 6 znakova)"', 'placeholder="Password (at least 6 characters)"'),
    ('<button class="primary" id="loginBtn">Prijavi se</button>', '<button class="primary" id="loginBtn">Log in</button>'),
    ('<button id="signupBtn">Registruj se</button>', '<button id="signupBtn">Sign up</button>'),
    ('placeholder="Kod mualima"', 'placeholder="Mu’allim (teacher) code"'),
    ('<button id="joinBtn">Pošalji zahtjev mualimu</button>', '<button id="joinBtn">Send a request to the mu’allim</button>'),
    ('<div>Kod mualima: <b id="myCode"', '<div>Mu’allim code: <b id="myCode"'),
    ('<h3>Zahtjevi učenika</h3>', '<h3>Student requests</h3>'),
    ('<h3>Moji učenici i rezultati</h3>', '<h3>My students and results</h3>'),
    ('<h3>Zahtjevi za mualima</h3>', '<h3>Requests to become a mu’allim</h3>'),
    ('▶ IGRAJ KVIZ', '▶ PLAY THE QUIZ'),
    ('<button id="logoutBtn">Odjava</button>', '<button id="logoutBtn">Log out</button>'),
    ('Online praćenje učenika • kviz može raditi i bez prijave',
     'Online student tracking • the quiz also works without logging in'),
    ("'Unesite ime, e-mail i lozinku od najmanje 6 znakova.'",
     "'Enter your name, e-mail and a password of at least 6 characters.'"),
    ("'Registracija je poslana. Ako je potrebna potvrda e-maila, otvorite poruku koju ste dobili.'",
     "'Sign-up sent. If e-mail confirmation is needed, open the message you received.'"),
    ("'Prijavljeni ste.'", "'You are logged in.'"),
    ("'Zahtjev je poslan mualimu.'", "'Your request has been sent to the mu’allim.'"),
    ("'Uloga: '", "'Role: '"),
    ("?'Mualim':'Učenik')", "?'Mu’allim (teacher)':'Student')"),
    ('<button onclick="requestMualim()">Želim biti mualim</button>',
     '<button onclick="requestMualim()">I want to be a mu’allim</button>'),
    ("'Zahtjev za mualima je poslan administratoru.'", "'Your request to become a mu’allim has been sent to the administrator.'"),
    ('>Prihvati</button>', '>Accept</button>'),
    ('>Odbij</button>', '>Decline</button>'),
    ("'Nema novih zahtjeva.'", "'No new requests.'"),
    ("full_name||'Učenik')", "full_name||'Student')"),
    ('<br>Tačno: ${x.correct_count}', '<br>Correct: ${x.correct_count}'),
    ('% • Bodovi: ${x.score}', '% • Points: ${x.score}'),
    ("'Još nema rezultata.'", "'No results yet.'"),
]
