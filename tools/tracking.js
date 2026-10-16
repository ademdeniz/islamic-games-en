/* Maktab tracker – who opened this page and for how many active minutes (see tools/tracking.py, supabase/tracking.sql).
   A child signs in once per device: class code → tap your name → (Group with PIN) 3 pictures. Time counts only while the
   page is on screen and was touched in the last minute, or audio is playing. Nothing is sent before a child signs in. */
(function () {
  var URL = '__URL__', KEY = '__KEY__';
  if (!URL || navigator.webdriver) return;
  var PICS = ['🍎', '🐪', '🌙', '⭐', '🌴', '📖', '🕌', '🐝', '🌸'];
  var ID_KEY = 'maktab.kid', SKIP_KEY = 'maktab.just-looking';

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
  var kid = get(ID_KEY);

  // ------------------------------------------------------------ active time
  var lastAct = Date.now(), pending = 0, visit = uuid(), key = pageKey(), media = [];
  ['pointerdown', 'keydown', 'touchstart', 'scroll', 'wheel', 'input'].forEach(function (e) {
    addEventListener(e, function () { lastAct = Date.now(); }, { passive: true, capture: true });
  });
  var play = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function () { if (media.indexOf(this) < 0) media.push(this); return play.apply(this, arguments); };
  setInterval(function () {
    if (document.visibilityState !== 'visible') return;
    var playing = media.some(function (m) { return !m.paused && !m.ended; });
    if (playing || Date.now() - lastAct < 60000) pending += 5;
  }, 5000);
  function flush(keep) {
    if (!kid || pending < 5) return;
    var s = Math.min(pending, 120), v = visit, k = key;
    pending -= s;
    rpc('track_visit', { p_token: kid.token, p_visit: v, p_type: type, p_key: k, p_title: document.title, p_seconds: s }, keep)
      .then(function (ok) { if (ok === false) { kid = null; put(ID_KEY, null); chip(); } })
      .catch(function () { if (v === visit) pending += s; });
  }
  setInterval(flush, 30000);
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') flush(true); });
  addEventListener('pagehide', function () { flush(true); });
  addEventListener('hashchange', function () {
    if (pageKey() === key) return;
    flush(true); visit = uuid(); key = pageKey(); pending = 0;
  });

  // ------------------------------------------------------------ the sign-in card and the name chip
  var host = document.createElement('div'), root = host.attachShadow ? host.attachShadow({ mode: 'open' }) : host;
  host.style.cssText = 'position:fixed;inset:auto;z-index:2147483647';
  root.innerHTML = '<style>' +
    '*{box-sizing:border-box;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}' +
    '[hidden]{display:none!important}' +
    '.chip{position:fixed;left:10px;bottom:10px;background:rgba(7,89,67,.92);color:#fff;border:2px solid #c99b3b;border-radius:999px;' +
      'padding:5px 12px;font-size:13px;font-weight:700;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.2)}' +
    '.veil{position:fixed;inset:0;background:rgba(10,30,24,.6);display:flex;align-items:center;justify-content:center;padding:16px}' +
    '.card{background:#fffdf7;color:#17372d;border:3px solid #c99b3b;border-radius:20px;padding:20px;width:100%;max-width:440px;' +
      'max-height:calc(100vh - 32px);overflow:auto;text-align:center}' +
    'h2{margin:0 0 6px;font-size:22px}p{margin:6px 0 12px;color:#5d6b64}' +
    'input{font-size:24px;letter-spacing:.15em;text-transform:uppercase;text-align:center;width:100%;padding:10px;border:2px solid #e6d8b3;border-radius:12px}' +
    'input:focus{outline:none;border-color:#0b6b50}' +
    'button{font:inherit;cursor:pointer;border-radius:12px}' +
    '.go{background:#075943;color:#fff;border:2px solid #075943;font-weight:700;font-size:17px;padding:10px 22px;margin-top:12px}' +
    '.go:disabled{opacity:.6}' +
    '.names{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;margin:10px 0}' +
    '.names button{background:#fff;border:2px solid #e6d8b3;padding:12px 6px;font-size:16px;font-weight:700;color:#17372d}' +
    '.names button:hover{border-color:#c99b3b;background:#f3e6c4}' +
    '.slots{display:flex;gap:8px;justify-content:center;margin:8px 0}' +
    '.slots span{width:54px;height:54px;border:2px dashed #c99b3b;border-radius:12px;font-size:32px;display:grid;place-items:center;background:#fff}' +
    '.pics{display:grid;grid-template-columns:repeat(3,64px);gap:8px;justify-content:center}' +
    '.pics button{font-size:34px;height:64px;background:#fff;border:2px solid #e6d8b3}' +
    '.link{background:none;border:0;color:#0b6b50;text-decoration:underline;font-size:14px;margin-top:12px;padding:4px}' +
    '.err{color:#a3271d;font-weight:700;min-height:1.2em;margin:8px 0 0}' +
    '.big{font-size:44px;margin:4px 0}' +
    '</style><div id="chip" class="chip" hidden></div><div id="veil" class="veil" hidden><div class="card" id="card"></div></div>';
  (document.body || document.documentElement).appendChild(host);
  var $ = function (id) { return root.getElementById ? root.getElementById(id) : root.querySelector('#' + id); };
  var card = $('card');
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function open(htmlStr) { card.innerHTML = htmlStr; $('veil').hidden = false; }
  function close() { $('veil').hidden = true; card.innerHTML = ''; }

  function chip() {
    var c = $('chip');
    c.hidden = false;
    c.textContent = kid ? '👤 ' + kid.name : '👤 Sign in';
    c.onclick = function () {
      if (!kid) return askCode();
      open('<div class="big">👤</div><h2>' + esc(kid.name) + '</h2><p>This device counts your learning time for ' + esc(kid.name) + '.</p>' +
        '<button class="go" id="stay">That’s me</button><br><button class="link" id="switch">Not ' + esc(kid.name.split(' ')[0]) + '? Switch</button>');
      $('stay').onclick = close;
      $('switch').onclick = function () { flush(true); kid = null; put(ID_KEY, null); chip(); askCode(); };
    };
  }

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
      put(ID_KEY, kid); put(SKIP_KEY, null); chip();
      open('<div class="big">🌟</div><h2>Welcome, ' + esc(r.name.split(' ')[0]) + '!</h2>' +
        (r.new_pin ? '<p>Your pictures are</p><div class="slots">' + pin.split('').map(function (n) { return '<span>' + PICS[+n] + '</span>'; }).join('') +
          '</div><p>Remember them!</p>' : '<p>Have fun learning. Your teacher can see what you practised.</p>') +
        '<button class="go" id="ok">Start</button>');
      $('ok').onclick = close;
      if (!r.new_pin) setTimeout(function () { if ($('ok')) close(); }, 2500);
    }, function (x) { if (onErr) onErr(x.message); else askCode(x.message); });
  }

  chip();
  var skipped = get(SKIP_KEY);
  if (!kid && !(skipped && Date.now() - skipped < 7 * 24 * 3600 * 1000)) askCode();
})();
