/* Maktab tracker – who opened this page and for how many active minutes (see tools/tracking.py, supabase/tracking.sql).
   A child signs in once per device: class code → tap your name → (Group with PIN) 3 pictures. Time counts only while the
   page is on screen and was touched in the last minute, or audio is playing. After a minute without a touch a small
   "Still reading?" card appears; tapping it (or the page) counts the quiet reading time, up to 4 minutes. The name chip
   shows a daily-goal ring and opens "I'm done for today", "Switch" and "Sign out". After 30 active minutes in a row a
   break reminder appears. Nothing is sent before a child signs in. */
(function () {
  var URL = '__URL__', KEY = '__KEY__';
  if (!URL || navigator.webdriver) return;
  var PICS = ['🍎', '🐪', '🌙', '⭐', '🌴', '📖', '🕌', '🐝', '🌸'];
  var ID_KEY = 'maktab.kid', SKIP_KEY = 'maktab.just-looking', SESSION_KEY = 'maktab.session', GOAL_KEY = 'maktab.goal-done';
  var IDLE = 60000, READ_CREDIT = 240, AWAY = 600, BREAK_AFTER = 1800, NEW_SESSION = 600000;
  // Shown on the "I'm done for today" card, one per day. DRAFT – waiting for the mu'allim's approval.
  var REMINDERS = [
    { en: 'The most beloved deeds to Allah are those done regularly, even if they are small.',
      bs: 'Allahu su najdraža djela ona koja se čine redovno, makar bila i mala.', src: 'Bukhari & Muslim' },
    { en: 'Whoever takes a path to seek knowledge, Allah makes easy for him a path to Paradise.',
      bs: 'Ko krene putem tražeći znanje, Allah će mu olakšati put do Dženneta.', src: 'Muslim' },
    { en: 'The best of you are those who learn the Qur’an and teach it.',
      bs: 'Najbolji među vama je onaj koji nauči Kur’an i podučava mu druge.', src: 'Bukhari' },
    { en: 'The one who recites the Qur’an well is with the noble, righteous angels; and the one who recites it with difficulty, struggling, gets a double reward.',
      bs: 'Ko lijepo uči Kur’an bit će sa časnim i dobrim melekima, a ko ga uči s mukom i teškoćom, ima dvostruku nagradu.', src: 'Bukhari & Muslim' },
    { en: '“My Lord, increase me in knowledge.”', bs: '„Gospodaru moj, povećaj mi znanje!“', src: 'Qur’an 20:114' },
    { en: '“Indeed, with hardship [will be] ease.”', bs: '„Zaista, s mukom je i last.“', src: 'Qur’an 94:6' },
    { en: 'Allah does not look at your appearance or your wealth, but He looks at your hearts and your deeds.',
      bs: 'Allah ne gleda u vaš izgled i imetak, nego gleda u vaša srca i djela.', src: 'Muslim' },
    { en: 'Say “Alhamdulillah” for what you learned today.', bs: 'Reci „Elhamdulillah“ za ono što si danas naučio/la.', src: '' }
  ];
  var BREAK = { en: 'Great work! Time for a short break – stretch, drink some water, help at home. “My Lord, have mercy upon them as they brought me up [when I was] small.”',
                bs: 'Svaka čast! Vrijeme je za kratku pauzu – protegni se, popij vode, pomozi kod kuće. „Gospodaru moj, smiluj im se kao što su oni mene odgajali kad sam bio malen.“',
                src: 'Qur’an 17:24' };
  var KIND = { lesson: ['📚', 'lessons'], sufara: ['✍️', 'Sufara'], quran: ['📖', 'Qur’an'], surah: ['🌙', 'surahs'], game: ['🎮', 'games'] };

  // ------------------------------------------------------------ which page is this
  var parts = location.pathname.split('/').filter(function (p) { return p && p !== 'index.html'; });
  var at = -1;
  for (var i = parts.length - 1; i >= 0; i--) if (['lessons', 'sufara', 'games'].indexOf(parts[i]) >= 0) { at = i; break; }
  if (at < 0) return;
  var rest = parts.slice(at), type = null;
  if (rest[0] === 'lessons' && rest.length >= 3) type = 'lesson';
  else if (rest[0] === 'sufara' && rest.length >= 2) type = 'sufara';
  else if (rest[0] === 'games' && rest.length >= 2)
    type = rest[1] === 'citaj-kuran' ? 'quran' : (rest[1] === 'learn-surahs-by-heart' || rest[1] === 'memori-sure') ? 'surah' : 'game';
  if (!type) return;
  var baseKey = rest.join('/');
  function pageKey() { return type === 'surah' && location.hash ? baseKey + location.hash : baseKey; }

  // ------------------------------------------------------------ small helpers
  function get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } }
  function put(k, v) { try { v === null ? localStorage.removeItem(k) : localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function uuid() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = Math.random() * 16 | 0; return (c === 'x' ? r : (r & 3 | 8)).toString(16);
    });
  }
  function rpc(fn, body, keep) {
    return fetch(URL + '/rest/v1/rpc/' + fn, {
      method: 'POST', keepalive: !!keep, body: JSON.stringify(body),
      headers: { 'Content-Type': 'application/json', apikey: KEY }
    }).then(function (r) {
      return r.json().catch(function () { return null; }).then(function (j) {
        if (!r.ok) throw new Error((j && j.message) || 'No connection. Try again.');
        return j;
      });
    }, function () { throw new Error('No internet connection. Try again.'); });
  }
  function startOfDay() { var d = new Date(); d.setHours(0, 0, 0, 0); return d; }
  function dayStamp() { return startOfDay().toDateString(); }
  function first(name) { return String(name).split(' ')[0]; }
  function mins(s) { return s >= 60 ? Math.round(s / 60) : s > 0 ? '<1' : 0; }
  var kid = get(ID_KEY);

  // ------------------------------------------------------------ active time
  var lastAct = Date.now(), pending = 0, visit = uuid(), key = pageKey(), media = [];
  var idleSecs = 0, stillShown = false, paused = false, pausedAt = 0;
  var today = { seconds: 0, goal: 0, loaded: false }, sinceLoad = 0;
  function touched() {
    if (paused && Date.now() - pausedAt > 1500) paused = false;
    if (stillShown) {   // they came back: the quiet minutes were reading, unless they were away for long
      if (idleSecs <= AWAY) count(Math.min(idleSecs, READ_CREDIT));
      hideStill();
    }
    idleSecs = 0;
    lastAct = Date.now();
  }
  ['pointerdown', 'keydown', 'touchstart', 'scroll', 'wheel', 'input'].forEach(function (e) {
    addEventListener(e, function (ev) { if (ev.target !== host) touched(); }, { passive: true, capture: true });   // taps on our own cards don't count
  });
  var play = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function () { if (media.indexOf(this) < 0) media.push(this); return play.apply(this, arguments); };
  function count(s) {
    if (!s || paused) return;
    pending += s; sinceLoad += s;
    var now = Date.now(), ses = get(SESSION_KEY) || {};
    if (!ses.last || now - ses.last > NEW_SESSION) ses = { active: 0, reminded: false };
    ses.active += s; ses.last = now;
    if (kid && ses.active >= BREAK_AFTER && !ses.reminded) { ses.reminded = true; setTimeout(breakCard, 0); }
    put(SESSION_KEY, ses);
    ring();
  }
  setInterval(function () {
    if (document.visibilityState !== 'visible' || paused) return;
    var playing = media.some(function (m) { return !m.paused && !m.ended; });
    if (playing) { lastAct = Date.now(); if (stillShown) hideStill(); idleSecs = 0; return count(5); }
    if (Date.now() - lastAct < IDLE) return count(5);
    idleSecs += 5;
    if (kid && !stillShown && $('veil').hidden) showStill();
  }, 5000);
  function flush(keep) {
    if (!kid || pending < 5) return;
    var s = Math.min(pending, 120), v = visit, k = key;
    pending -= s;
    rpc('track_visit', { p_token: kid.token, p_visit: v, p_type: type, p_key: k, p_title: document.title, p_seconds: s }, keep)
      .then(function (ok) { if (ok === false) forget(); })
      .catch(function () { if (v === visit) pending += s; });
  }
  setInterval(flush, 30000);
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') flush(true); });
  addEventListener('pagehide', function () { flush(true); });
  addEventListener('hashchange', function () {
    if (pageKey() === key) return;
    flush(true); visit = uuid(); key = pageKey(); pending = 0;
  });
  function forget() { kid = null; put(ID_KEY, null); hideStill(); chip(); }
  function loadToday() {
    if (!kid) return;
    rpc('kid_today', { p_token: kid.token, p_from: startOfDay().toISOString() }).then(function (t) {
      if (t === null) return forget();
      today = { seconds: t.seconds, goal: t.goal_minutes, loaded: true };   // what the server has …
      sinceLoad = pending;                                                 // … plus what is not sent yet
      ring();
    }, function () {});
  }

  // ------------------------------------------------------------ cards, the name chip, the "still reading?" note
  var host = document.createElement('div'), root = host.attachShadow ? host.attachShadow({ mode: 'open' }) : host;
  host.style.cssText = 'position:fixed;inset:auto;z-index:2147483647';
  root.innerHTML = '<style>' +
    '*{box-sizing:border-box;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}' +
    '[hidden]{display:none!important}' +
    '.chip{position:fixed;left:10px;bottom:10px;display:flex;align-items:center;gap:7px;background:rgba(7,89,67,.92);color:#fff;' +
      'border:2px solid #c99b3b;border-radius:999px;padding:4px 12px 4px 5px;font-size:13px;font-weight:700;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.2)}' +
    '.ring{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;font-size:12px;flex:none}' +
    '.ring i{width:16px;height:16px;border-radius:50%;background:#075943;display:grid;place-items:center;font-style:normal}' +
    '.still{position:fixed;left:50%;bottom:58px;transform:translateX(-50%);background:#fffdf7;color:#17372d;border:2px solid #c99b3b;' +
      'border-radius:999px;padding:8px 16px;font-size:15px;font-weight:700;box-shadow:0 4px 14px rgba(0,0,0,.25);cursor:pointer;white-space:nowrap}' +
    '.veil{position:fixed;inset:0;background:rgba(10,30,24,.6);display:flex;align-items:center;justify-content:center;padding:16px}' +
    '.card{background:#fffdf7;color:#17372d;border:3px solid #c99b3b;border-radius:20px;padding:20px;width:100%;max-width:440px;' +
      'max-height:calc(100vh - 32px);overflow:auto;text-align:center}' +
    'h2{margin:0 0 6px;font-size:22px}p{margin:6px 0 12px;color:#5d6b64}' +
    'input{font-size:24px;letter-spacing:.15em;text-transform:uppercase;text-align:center;width:100%;padding:10px;border:2px solid #e6d8b3;border-radius:12px}' +
    'input:focus{outline:none;border-color:#0b6b50}' +
    'button{font:inherit;cursor:pointer;border-radius:12px}' +
    '.go{background:#075943;color:#fff;border:2px solid #075943;font-weight:700;font-size:17px;padding:10px 22px;margin-top:12px}' +
    '.go.ghost{background:#fff;color:#075943}' +
    '.go:disabled{opacity:.6}' +
    '.names{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;margin:10px 0}' +
    '.names button{background:#fff;border:2px solid #e6d8b3;padding:12px 6px;font-size:16px;font-weight:700;color:#17372d}' +
    '.names button:hover{border-color:#c99b3b;background:#f3e6c4}' +
    '.slots{display:flex;gap:8px;justify-content:center;margin:8px 0}' +
    '.slots span{width:54px;height:54px;border:2px dashed #c99b3b;border-radius:12px;font-size:32px;display:grid;place-items:center;background:#fff}' +
    '.pics{display:grid;grid-template-columns:repeat(3,64px);gap:8px;justify-content:center}' +
    '.pics button{font-size:34px;height:64px;background:#fff;border:2px solid #e6d8b3}' +
    '.link{background:none;border:0;color:#0b6b50;text-decoration:underline;font-size:14px;margin-top:12px;padding:4px}' +
    '.link.small{font-size:12px;color:#5d6b64}' +
    '.err{color:#a3271d;font-weight:700;min-height:1.2em;margin:8px 0 0}' +
    '.big{font-size:44px;margin:4px 0}' +
    '.today{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:6px 0}' +
    '.today span{background:#eef3ef;border-radius:999px;padding:4px 10px;font-size:14px;font-weight:700;color:#075943}' +
    '.quote{background:#f3e6c4;border-radius:14px;padding:12px;margin:12px 0 4px;font-size:15px;color:#17372d}' +
    '.quote small{display:block;color:#5d6b64;margin-top:6px}' +
    '.bar{height:12px;border-radius:6px;background:#eef3ef;overflow:hidden;margin:8px 0 2px}.bar i{display:block;height:100%;background:#c99b3b}' +
    '</style><div id="chip" class="chip" hidden></div><div id="still" class="still" hidden>📖 Still reading? Tap to keep going</div>' +
    '<div id="veil" class="veil" hidden><div class="card" id="card"></div></div>';
  (document.body || document.documentElement).appendChild(host);
  var $ = function (id) { return root.getElementById ? root.getElementById(id) : root.querySelector('#' + id); };
  var card = $('card');
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function open(htmlStr) { hideStill(); card.innerHTML = htmlStr; $('veil').hidden = false; }
  function close() { $('veil').hidden = true; card.innerHTML = ''; }
  function showStill() { stillShown = true; $('still').hidden = false; }
  function hideStill() { stillShown = false; $('still').hidden = true; }
  $('still').onclick = touched;
  function quote(q) { return '<div class="quote">' + esc(q.en) + '<small>' + esc(q.bs) + (q.src ? ' — ' + esc(q.src) : '') + '</small></div>'; }

  function todaySeconds() { return Math.max(0, today.seconds + sinceLoad); }
  function ring() {
    if (!kid) return;
    var r = $('chip').querySelector('.ring');
    if (!r) return;
    var goal = today.goal * 60, done = goal ? Math.min(1, todaySeconds() / goal) : 0;
    r.hidden = !today.loaded || !goal;
    r.style.background = 'conic-gradient(#f3c969 ' + Math.round(done * 360) + 'deg, rgba(255,255,255,.28) 0)';
    r.querySelector('i').textContent = done >= 1 ? '★' : '';
    r.title = mins(todaySeconds()) + ' of ' + today.goal + ' minutes today';
    if (goal && done >= 1 && get(GOAL_KEY) !== dayStamp() + kid.token && $('veil').hidden) {
      put(GOAL_KEY, dayStamp() + kid.token);
      open('<div class="big">🌟</div><h2>Today’s goal reached!</h2><p>MashaAllah, ' + esc(first(kid.name)) + ' – you practised ' + today.goal +
        ' minutes today. Keep going or take a rest.<br>Današnji cilj je ispunjen – mašaAllah!</p><button class="go" id="ok">Alhamdulillah</button>');
      $('ok').onclick = close;
    }
  }

  function chip() {
    var c = $('chip');
    c.hidden = false;
    c.innerHTML = kid ? '<span class="ring" hidden><i></i></span><span>👤 ' + esc(kid.name) + '</span>' : '<span>👤 Sign in</span>';
    c.style.paddingLeft = kid ? '5px' : '12px';
    ring();
    c.onclick = function () { if (!kid) askCode(); else menu(); };
  }

  function menu() {
    var goal = today.goal * 60, done = goal ? Math.min(1, todaySeconds() / goal) : 0;
    open('<div class="big">👤</div><h2>' + esc(kid.name) + '</h2>' +
      (today.loaded ? '<p>Today: <b>' + mins(todaySeconds()) + ' minutes</b>' + (goal ? ' of your ' + today.goal + '-minute goal' : '') + '</p>' +
        (goal ? '<div class="bar"><i style="width:' + Math.round(done * 100) + '%"></i></div>' : '') : '<p>This device counts your learning time for ' + esc(kid.name) + '.</p>') +
      '<button class="go" id="done">✋ I’m done for today</button><br>' +
      '<button class="go ghost" id="stay">Keep learning</button><br>' +
      '<button class="link" id="switch">Not ' + esc(first(kid.name)) + '? Switch</button><br>' +
      '<button class="link small" id="out">Sign out on this device</button>');
    $('stay').onclick = close;
    $('done').onclick = doneForToday;
    $('switch').onclick = function () { flush(true); kid = null; put(ID_KEY, null); chip(); askCode(); };
    $('out').onclick = function () {
      open('<h2>Sign out on this device?</h2><p>Next time ' + esc(first(kid.name)) + ' types the class code and taps the name again' +
        '. Use this on a phone that is not yours.</p><button class="go" id="yes">Sign out</button><br><button class="link" id="no">Cancel</button>');
      $('no').onclick = menu;
      $('yes').onclick = function () {
        flush(true);
        var tok = kid.token;
        rpc('sign_out_device', { p_token: tok }).catch(function () {});
        forget(); put(SESSION_KEY, null); close();
      };
    };
  }

  function doneForToday() {
    flush(true);
    paused = true; pausedAt = Date.now(); hideStill();
    var name = first(kid.name);
    open('<div class="big">🌙</div><h2>MashaAllah, ' + esc(name) + '!</h2><p>Saving…</p>');
    setTimeout(function () {   // give the last report a moment to arrive
      rpc('kid_today', { p_token: kid.token, p_from: startOfDay().toISOString() }).then(function (t) {
        if (t === null) return forget();
        var kinds = Object.keys(t.by_type || {}).filter(function (k) { return t.by_type[k] >= 30 && KIND[k]; });
        var q = REMINDERS[Math.floor(startOfDay() / 864e5) % REMINDERS.length];
        today = { seconds: t.seconds, goal: t.goal_minutes, loaded: true }; sinceLoad = 0; ring();
        open('<div class="big">🌙</div><h2>MashaAllah, ' + esc(name) + '!</h2>' +
          '<p>Today you practised <b>' + mins(t.seconds) + ' minutes</b>.<br>Danas si vježbao/la ' + mins(t.seconds) + ' minuta.</p>' +
          (kinds.length ? '<div class="today">' + kinds.map(function (k) { return '<span>' + KIND[k][0] + ' ' + mins(t.by_type[k]) + ' min ' + KIND[k][1] + '</span>'; }).join('') + '</div>' : '') +
          (t.pages && t.pages.length ? '<p style="font-size:14px">' + t.pages.map(esc).join(' · ') + '</p>' : '') +
          quote(q) + '<button class="go" id="bye">See you next time · Vidimo se!</button>');
        $('bye').onclick = function () { pausedAt = Date.now(); close(); };
      }, function () {
        open('<div class="big">🌙</div><h2>MashaAllah, ' + esc(name) + '!</h2><p>See you next time.</p>' +
          quote(REMINDERS[0]) + '<button class="go" id="bye">Close</button>');
        $('bye').onclick = function () { pausedAt = Date.now(); close(); };
      });
    }, 800);
  }

  function breakCard() {
    if (!$('veil').hidden) return;
    open('<div class="big">🧃</div><h2>30 minutes – great work!</h2>' + quote(BREAK) + '<button class="go" id="ok">OK</button>');
    $('ok').onclick = close;
  }

  // ------------------------------------------------------------ signing in
  function askCode(err) {
    open('<div class="big">👋</div><h2>Assalamu alaikum!</h2><p>Who is learning? Type your <b>class code</b> (your teacher gave it).</p>' +
      '<form id="f"><input id="code" autocomplete="off" autocapitalize="characters" spellcheck="false" maxlength="12" placeholder="CODE">' +
      '<div class="err" id="err">' + esc(err || '') + '</div><button class="go" id="next">Next</button></form>' +
      '<button class="link" id="look">I’m a parent / just looking</button>');
    $('code').focus();
    $('look').onclick = function () { put(SKIP_KEY, Date.now()); close(); chip(); };
    $('f').onsubmit = function (e) {
      e.preventDefault();
      var code = $('code').value.trim();
      if (!code) return;
      $('next').disabled = true;
      rpc('join_class', { p_code: code }).then(function (g) { askName(code, g); }, function (x) { askCode(x.message); });
    };
  }

  function askName(code, g) {
    open('<h2>Tap your name</h2><p>' + esc(g.group_name) + '</p><div class="names" id="names"></div>' +
      '<button class="link" id="back">← Different class code</button>');
    $('names').innerHTML = g.kids.map(function (k, n) { return '<button data-n="' + n + '">' + esc(k.name) + '</button>'; }).join('') ||
      '<p>No names yet – ask your teacher.</p>';
    $('back').onclick = function () { askCode(); };
    Array.prototype.forEach.call($('names').querySelectorAll('button'), function (b) {
      b.onclick = function () {
        var k = g.kids[+b.dataset.n];
        if (g.pin_required) askPin(code, g, k); else signIn(code, k, null);
      };
    });
  }

  function askPin(code, g, k, err) {
    var pin = '';
    open('<h2>' + esc(k.name) + '</h2><p>' + (k.has_pin ? 'Tap your <b>3 pictures</b>.' : 'Choose <b>3 pictures</b> and remember them! You will need them on a new phone or tablet.') + '</p>' +
      '<div class="slots"><span></span><span></span><span></span></div><div class="pics" id="pics">' +
      PICS.map(function (p, n) { return '<button data-n="' + n + '">' + p + '</button>'; }).join('') + '</div>' +
      '<div class="err">' + esc(err || '') + '</div><button class="link" id="undo">⌫ Undo</button> <button class="link" id="back">← Not me</button>');
    var slots = card.querySelectorAll('.slots span');
    function show() { Array.prototype.forEach.call(slots, function (s, n) { s.textContent = pin[n] ? PICS[+pin[n]] : ''; }); }
    Array.prototype.forEach.call($('pics').querySelectorAll('button'), function (b) {
      b.onclick = function () {
        if (pin.length >= 3) return;
        pin += b.dataset.n; show();
        if (pin.length === 3) signIn(code, k, pin, function (msg) { askPin(code, g, k, msg); });
      };
    });
    $('undo').onclick = function () { pin = pin.slice(0, -1); show(); };
    $('back').onclick = function () { askName(code, g); };
  }

  function signIn(code, k, pin, onErr) {
    rpc('sign_in_kid', { p_code: code, p_kid: k.id, p_pin: pin }).then(function (r) {
      kid = { token: r.token, name: r.name, group: r.group };
      put(ID_KEY, kid); put(SKIP_KEY, null); chip(); loadToday();
      open('<div class="big">🌟</div><h2>Welcome, ' + esc(first(r.name)) + '!</h2>' +
        (r.new_pin ? '<p>Your pictures are</p><div class="slots">' + pin.split('').map(function (n) { return '<span>' + PICS[+n] + '</span>'; }).join('') +
          '</div><p>Remember them!</p>' : '<p>Have fun learning. Your teacher can see what you practised.</p>') +
        '<button class="go" id="ok">Start</button>');
      $('ok').onclick = close;
      if (!r.new_pin) setTimeout(function () { if ($('ok')) close(); }, 2500);
    }, function (x) { if (onErr) onErr(x.message); else askCode(x.message); });
  }

  chip();
  loadToday();
  var skipped = get(SKIP_KEY);
  if (!kid && !(skipped && Date.now() - skipped < 7 * 24 * 3600 * 1000)) askCode();
})();
