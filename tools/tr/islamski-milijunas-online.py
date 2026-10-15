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

# Use our own Supabase project (supabase/config.json) instead of the original author's database.
import json as _json
_cfg = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'supabase', 'config.json')))
T += [
    ("SUPABASE_URL='https://jaxcricubwcvqudhknjj.supabase.co'", f"SUPABASE_URL='{_cfg['url']}'"),
    ("SUPABASE_KEY='sb_publishable_2gMnx-y-cNpBlCTW6V-pkg_SlYpda8R'", f"SUPABASE_KEY='{_cfg['publishable_key']}'"),
]

# ---- "Forgot password?" (added feature, not in the original) -------------------------------------------------
STRUCTURAL = ('adds a "Forgot password?" flow: reset e-mail via Supabase resetPasswordForEmail, and a '
              '"Choose a new password" box shown on the PASSWORD_RECOVERY event (tested in tests/test_online_auth.py)')

_FORGOT = [
    ('<button id="signupBtn">Sign up</button></div></div>',
     '<button id="signupBtn">Sign up</button></div>'
     '<button type="button" id="forgotBtn" class="linkBtn">Forgot password?</button></div>\n'
     '<div id="authRecover" class="onlineBox hide"><h3>Choose a new password</h3>'
     '<input id="newPassword" type="password" placeholder="New password (at least 6 characters)">'
     '<div class="menu"><button class="primary" id="savePwBtn">Save new password</button></div></div>'),
    ('.onlineBox{', '.linkBtn{background:none!important;border:0!important;box-shadow:none!important;color:#9cc3ff!important;'
                    'text-decoration:underline;padding:6px 0!important;margin-top:4px;cursor:pointer;font-size:14px}.onlineBox{'),
    ('function onlineMsg(x){', 'let recovering=false; function onlineMsg(x){'),
    ('me=user;$(\'authLoggedOut\')', 'me=user;if(recovering){$(\'authLoggedOut\').classList.add(\'hide\');$(\'authLoggedIn\').classList.add(\'hide\');return}$(\'authLoggedOut\')'),
    ('sb.auth.onAuthStateChange(()=>setTimeout(refreshOnline,0));',
     "$('forgotBtn').onclick=async()=>{let e=$('email').value.trim();"
     "if(!e)return onlineMsg('Type your e-mail above, then tap “Forgot password?” again.');"
     "let {error}=await sb.auth.resetPasswordForEmail(e,{redirectTo:location.origin+location.pathname});"
     "onlineMsg(error?error.message:'If there is an account for '+e+', we sent it an e-mail with a link to choose a new password.')};\n"
     "$('savePwBtn').onclick=async()=>{let p=$('newPassword').value;"
     "if(p.length<6)return onlineMsg('The new password needs at least 6 characters.');"
     "let {error}=await sb.auth.updateUser({password:p});if(error)return onlineMsg(error.message);"
     "recovering=false;$('authRecover').classList.add('hide');$('newPassword').value='';"
     "onlineMsg('Your new password is saved. You are logged in.');await refreshOnline()};\n"
     "sb.auth.onAuthStateChange(ev=>{if(ev==='PASSWORD_RECOVERY'){recovering=true;show('online');"
     "$('authLoggedOut').classList.add('hide');$('authLoggedIn').classList.add('hide');$('authRecover').classList.remove('hide');"
     "onlineMsg('Choose a new password for your account.')}});\n"
     "sb.auth.onAuthStateChange(()=>setTimeout(refreshOnline,0));"),
]

_base_transform = transform


def transform(src):
    src = _base_transform(src)
    for a, b in _FORGOT:
        assert src.count(a) == 1, 'forgot-password patch target not found: ' + a[:60]
        src = src.replace(a, b)
    return src

# ---- Login required to play (homework mode): students must be logged in and accepted into a mu'allim's class ------
STRUCTURAL += ('; requires login to play: students must be in a mu’allim’s class before START GAME works '
               '(tested in tests/test_online_auth.py)')

_LOGIN = [
    ('<div class="footer">Online student tracking • the quiz also works without logging in</div>',
     '<div class="footer">Log in and join your mu’allim’s class to play • your results are sent to your teacher</div>'),
    ('<button id="dbBtn">📚 QUESTION BANK</button></div>',
     '<button id="dbBtn">📚 QUESTION BANK</button></div><div id="whoBar" class="sub" style="margin-top:10px"></div>'),
    ('function startGame(){run=', 'async function startGame(){if(!(await canPlay()))return;run='),
    ("$('onlineBack').onclick=()=>show('start');", "$('onlineBack').onclick=()=>{show('start');showStatus()};"),
    ('sb.auth.onAuthStateChange(()=>setTimeout(refreshOnline,0));',
     "function blockPlay(t){show('online');onlineMsg(t);showStatus();return false}\n"
     "async function canPlay(){try{"
     "if(!me)return blockPlay('Please log in (or sign up) and join your mu’allim’s class to play – your results are sent to your teacher.');"
     "if(!myProfile)await refreshOnline();"
     "if(myProfile&&myProfile.role!=='ucenik')return true;"
     "if(!myTeacher){let {data:l}=await sb.from('teacher_students').select('teacher_id').eq('student_id',me.id).maybeSingle();myTeacher=l?.teacher_id||null}"
     "if(myTeacher)return true;"
     "return blockPlay('Type your mu’allim’s code below and send a request. You can play as soon as your mu’allim accepts it.')"
     "}catch(e){show('online');onlineMsg('Could not connect to the class server. Check your internet connection and try again.');return false}}\n"
     "function showStatus(){let w=$('whoBar');if(!w)return;try{"
     "w.textContent=!me||!myProfile?'🔒 Log in to play – tap 🌐 ONLINE / LOG IN':"
     "myProfile.role!=='ucenik'?'Logged in as '+myProfile.full_name+' (results are not saved for teachers)':"
     "myTeacher?'✅ Logged in as '+myProfile.full_name+' – your results go to your mu’allim':"
     "'Logged in as '+myProfile.full_name+' – join your mu’allim’s class to play'"
     "}catch(e){w.textContent='⚠️ Not connected – check your internet connection'}}\n"
     "sb.auth.onAuthStateChange(()=>setTimeout(async()=>{await refreshOnline();showStatus()},0));"),
]

_forgot_transform = transform


def transform(src):
    src = _forgot_transform(src)
    for a, b in _LOGIN:
        assert src.count(a) == 1, 'login-required patch target not found: ' + a[:60]
        src = src.replace(a, b)
    return src

# ---- Pin the Supabase library to the exact version the tests passed with (a floating "@2" could change under us) --
SUPABASE_JS = '2.117.2'
_login_transform = transform


def transform(src):
    src = _login_transform(src)
    a = '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>'
    assert src.count(a) == 1, 'supabase-js script tag not found'
    return src.replace(a, f'<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@{SUPABASE_JS}/dist/umd/supabase.min.js"></script>')
