# pomozimo-maci-abdest: table mode.
T = [
    ('<title>Pomozimo maci da uzme abdest</title>', '<title>Let’s Help the Kitty Make Wudu</title>'),
    ('aria-label="Zvuk"', 'aria-label="Sound"'),
    ('<span class="collectedLabel">SAKUPLJENO:</span></div><div id="hud">BODOVI',
     '<span class="collectedLabel">COLLECTED:</span></div><div id="hud">POINTS'),
    ('<div class="progress" id="progress">Korak 0 / 13</div>', '<div class="progress" id="progress">Step 0 / 13</div>'),
    ('▶ ZAPOČNI IGRU', '▶ START GAME'),
    ("{text:'Euza, bismilla i nijet'", "{text:'A’udhu, Bismillah and niyyah'"),
    ("{text:'Šake 3x'", "{text:'Hands 3x'"),
    ("{text:'Usta 3x'", "{text:'Mouth 3x'"),
    ("{text:'Nos 3x'", "{text:'Nose 3x'"),
    ("{text:'Lice 3x'", "{text:'Face 3x'"),
    ("{text:'Desnu ruku do iza laktova 3x'", "{text:'Right arm past the elbow 3x'"),
    ("{text:'Lijevu ruku do iza laktova 3x'", "{text:'Left arm past the elbow 3x'"),
    ("{text:'Mesh'", "{text:'Masah (wipe the head)'"),
    ("{text:'Uši'", "{text:'Ears'"),
    ("{text:'Vrat'", "{text:'Neck'"),
    ("{text:'Desnu nogu do članaka'", "{text:'Right foot up to the ankle'"),
    ("{text:'Lijevu nogu do članaka'", "{text:'Left foot up to the ankle'"),
    ("{text:'Kelimei-šehadet'", "{text:'Shahadah'"),
    ("prog.textContent='Korak '+next+' / 13'", "prog.textContent='Step '+next+' / 13'"),
    ("msg.innerHTML='🎉 Bravo! Maca je pravilno uzela abdest!<br>Osvojeno: '+score+' bodova 🐾'",
     "msg.innerHTML='🎉 Well done! The kitty made Wudu the right way!<br>You earned: '+score+' points 🐾'"),
    ("start.textContent='↻ IGRAJ PONOVO'", "start.textContent='↻ PLAY AGAIN'"),
    ("collected.innerHTML='<span class=\"collectedLabel\">SAKUPLJENO:</span>'",
     "collected.innerHTML='<span class=\"collectedLabel\">COLLECTED:</span>'"),
    ("prog.textContent='Korak 0 / 13'", "prog.textContent='Step 0 / 13'"),
]

# ---- Make the 13 painted drops tappable (the original only had small falling drops, hidden behind the top bar) ----
STRUCTURAL = ('the 13 Wudu drops in the picture are tappable in order (hint after 2 wrong taps); the whole picture is '
              'always visible and the game fits under the logo header (tests/test_kitty.py)')
# Drop outlines in picture pixels (1536×1404), by step: 0 A’udhu … 12 Shahadah (same order as `steps`)
SPOTS = [(510, 1070, 700, 1320), (722, 500, 905, 735), (790, 770, 980, 1010), (535, 270, 695, 500), (470, 570, 650, 810),
         (1015, 620, 1210, 860), (900, 290, 1090, 540), (1275, 430, 1460, 670), (250, 215, 430, 435), (1245, 795, 1430, 1035),
         (740, 1085, 935, 1325), (1190, 1085, 1375, 1325), (968, 1065, 1160, 1320)]

_KITTY_CSS = (
    'body{display:flex!important;flex-direction:column;flex-wrap:nowrap!important;height:100vh;height:100dvh}.bz-brand{flex:none!important}'
    '.bz-brand img{max-height:13vh;width:auto!important;max-width:100%!important;height:auto}'
    '#hud .progress{white-space:nowrap;font-size:.75em}'
    '#game{flex:1;height:auto!important;min-height:0!important;background-size:contain;background-repeat:no-repeat;background-color:#2d5a2a}'
    '#collected{right:10px!important}'
    '#hud{min-width:0!important;padding:0!important;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:10px!important}'
    '#hud .score{font-size:1.7em;min-width:70%;margin:.2em 0}'
    '.spot{position:absolute;z-index:12;border:0;padding:0;background:transparent;border-radius:50%;cursor:pointer;pointer-events:none;'
    '-webkit-tap-highlight-color:transparent}#game.running .spot{pointer-events:auto}'
    '#game.running .spot:hover{box-shadow:0 0 0 4px #fff8}'
    '.spot.got{background:radial-gradient(circle,#ffffffb0 0 45%,#ffffff60 70%,transparent 72%);pointer-events:none!important}'
    '.spot.got::after{content:"✓";position:absolute;inset:0;display:flex;align-items:center;justify-content:center;'
    'font-size:min(9vh,9vw);font-weight:900;color:#1a8f3c;text-shadow:0 2px 4px #fff}'
    '.spot.hint{animation:glow 1s ease-in-out infinite}@keyframes glow{50%{box-shadow:0 0 0 6px #ffe066,0 0 28px 10px #ffd000}}'
    '.spot.wrong{animation:shake .25s 2}'
    '#help{position:absolute;left:50%;bottom:calc(5% + 80px);transform:translateX(-50%);z-index:40;background:#fffdebee;'
    'border:3px solid #7c451c;border-radius:14px;padding:8px 14px;font-weight:900;color:#52240c;text-align:center;max-width:90%}'
    '#game.running #help{display:none}'
)

_KITTY_JS = (
    "const SPOTS=" + repr(SPOTS).replace('(', '[').replace(')', ']') + ",IW=1536,IH=1404;let wrongs=0;"
    "const spots=SPOTS.map((r,id)=>{const b=document.createElement('button');b.className='spot';b.dataset.id=id;"
    "b.setAttribute('aria-label',steps[id].text);b.addEventListener('click',()=>tap(b,id));game.appendChild(b);return b});"
    "const HUD=[1292,18,1520,330];"
    "function rect(){const W=game.clientWidth,H=game.clientHeight,c=document.getElementById('collected'),top=c.offsetTop+c.offsetHeight+6,"
    "s=Math.min(W/IW,(H-top)/IH);return {s,ox:(W-IW*s)/2,oy:top+(H-top-IH*s)/2}}"
    "function place(){const {s,ox,oy}=rect();game.style.backgroundSize=(IW*s)+'px '+(IH*s)+'px';game.style.backgroundPosition=ox+'px '+oy+'px';"
    "const h=document.getElementById('hud');h.style.left=(ox+HUD[0]*s)+'px';h.style.top=(oy+HUD[1]*s)+'px';h.style.right='auto';"
    "h.style.width=((HUD[2]-HUD[0])*s)+'px';h.style.height=((HUD[3]-HUD[1])*s)+'px';h.style.fontSize=Math.max(9,30*s)+'px';"
    "spots.forEach((b,id)=>{const [x0,y0,x1,y1]=SPOTS[id];b.style.left=(ox+x0*s)+'px';b.style.top=(oy+y0*s)+'px';"
    "b.style.width=((x1-x0)*s)+'px';b.style.height=((y1-y0)*s)+'px'})}"
    "addEventListener('resize',place);place();"
    "function tap(b,id){if(!running)return;spots.forEach(s=>s.classList.remove('hint'));"
    "if(id===next){score+=10;addCollected(id);next++;good();floatText(b,'+10');b.classList.add('got');wrongs=0;"
    "prog.textContent='Step '+next+' / 13';scoreEl.textContent=score;if(next===steps.length){game.classList.remove('running');finish()}}"
    "else{score=Math.max(0,score-3);scoreEl.textContent=score;bad();floatText(b,'−3');b.classList.remove('wrong');void b.offsetWidth;"
    "b.classList.add('wrong');if(++wrongs>=2)spots[next].classList.add('hint')}}"
    "function armSpots(){spots.forEach(s=>s.classList.remove('got','hint','wrong'));wrongs=0;game.classList.add('running');place()}"
)

_KITTY = [
    ('</style>', _KITTY_CSS + '</style>'),
    ('<button id="start">▶ START GAME</button>',
     '<div id="help">Tap the water drops in the right order of Wudu 💧</div><button id="start">▶ START GAME</button>'),
    ("prog.textContent='Step 0 / 13';msg.style.display='none';start.style.display='none';running=true;clearTimeout(timer);spawn()}",
     "prog.textContent='Step 0 / 13';msg.style.display='none';start.style.display='none';running=true;clearTimeout(timer);armSpots()}"),
    ("start.addEventListener('click',begin);", _KITTY_JS + "start.addEventListener('click',begin);"),
]


def transform(src):
    for a, b in _KITTY:
        assert src.count(a) == 1, 'kitty patch target not found: ' + a[:70]
        src = src.replace(a, b)
    return src
