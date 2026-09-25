"""Build games/memori-sure/index.html from the English pilot (commit f2614cc).

Adds: community logo header, italic English translation (Sahih International) under each
transliteration, and ayah-by-ayah recitation (Mishary Alafasy) with a Quran.com link.

Run from the project root:  python3 tools/build_memori_sure.py
"""
import base64
import json
import subprocess
import urllib.request

OUT = 'games/memori-sure/index.html'
src = subprocess.run(['git', 'show', 'f2614cc:' + OUT], capture_output=True, text=True, check=True).stdout
data = json.load(open('data/surahs.json', encoding='utf-8'))
logo = base64.b64encode(open('assets/logo-bz-erie-web.jpg', 'rb').read()).decode()

# Global ayah number of the first ayah of each surah (used by the audio CDN).
surahs = json.load(urllib.request.urlopen('https://api.alquran.cloud/v1/surah'))['data']
start, total = {}, 0
for s in surahs:
    start[s['number']] = total + 1
    total += s['numberOfAyahs']

# Game surah names (keys of S, in order) -> surah numbers.
NUMS = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 1, 2]
names = json.loads(src[src.index('const S=') + 8:src.index('};', src.index('const S=')) + 1]).keys()
EN, META = {}, {}
for name, n in zip(names, NUMS):
    EN[name] = [a['en'] for a in data[str(n)]['ayahs']]
    META[name] = {'g': start[n], 'q': '2/1-5' if n == 2 else str(n)}

CSS = """
.brand{background:#fff;border:3px solid #c99b3b;border-radius:18px;padding:10px 14px;margin-bottom:8px;text-align:center}
.brand img{display:block;width:100%;max-width:760px;height:auto;margin:auto}
.ayah{color:#17372d}
.tr{display:block;font-weight:700} .en{display:block;font-style:italic;font-weight:400;color:#4a5a52;margin-top:3px}
.listen{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:10px}
.listen .act{text-decoration:none} .link{background:#fff !important;color:#075943 !important;border:2px solid #075943 !important}
.reciter{font-size:13px;color:#4a5a52}
#reader{display:none;background:#fff;border:3px solid #c99b3b;border-radius:17px;padding:14px;margin-top:12px}
#reader h2{text-align:center;margin-top:0}
.row{padding:10px 8px;border-bottom:1px solid #eadfc4;text-align:center;border-radius:10px;cursor:pointer}
.row:last-child{border-bottom:0} .row.playing{background:#fff3cf;box-shadow:inset 0 0 0 2px #c99b3b}
.num{display:inline-block;min-width:26px;padding:1px 6px;margin-bottom:3px;border-radius:20px;background:#075943;color:#fff;font-size:12px;font-weight:800}
.credit{text-align:center;font-size:12px;color:#6b7a72;margin:14px 0}
"""

JS = """
const EN=%s,META=%s;
const reader=document.getElementById('reader'),playBtn=document.getElementById('play'),player=new Audio();
let playIdx=-1;
function ayahHTML(i){return '<span class="tr">'+current[i]+'</span><span class="en">'+EN[sel.value][i]+'</span>'}
function showRead(){reader.style.display='block';document.getElementById('readerTitle').textContent='📖 '+sel.value;
 document.getElementById('readerBody').innerHTML=current.map((t,i)=>'<div class="row" data-i="'+i+'"><span class="num">'+(i+1)+'</span>'+ayahHTML(i)+'</div>').join('');
 document.querySelectorAll('#readerBody .row').forEach(r=>r.addEventListener('click',()=>playFrom(+r.dataset.i)));mark()}
function mark(){document.querySelectorAll('#readerBody .row').forEach((r,k)=>r.classList.toggle('playing',k===playIdx));
 const r=document.querySelector('#readerBody .row.playing');if(r)r.scrollIntoView({block:'center',behavior:'smooth'})}
function stopAudio(){player.pause();playIdx=-1;playBtn.textContent='▶ Listen';mark()}
function playFrom(i){if(i>=current.length){stopAudio();return}playIdx=i;
 player.src='https://cdn.islamic.network/quran/audio/128/ar.alafasy/'+(META[sel.value].g+i)+'.mp3';
 player.play().catch(()=>{stopAudio();alert('Audio could not play. Check your internet connection.')});playBtn.textContent='⏹ Stop';mark()}
player.addEventListener('ended',()=>playFrom(playIdx+1));
playBtn.addEventListener('click',()=>{if(playIdx>=0){stopAudio();return}if(reader.style.display!=='block')showRead();playFrom(0)});
function setLink(){document.getElementById('qlink').href='https://quran.com/'+META[sel.value].q}
""" % (json.dumps(EN, ensure_ascii=False), json.dumps(META))

R = [
    ('</style>', CSS + '</style>'),
    ('<header>', '<div class="brand"><img alt="Islamic Community of Bosniaks – Erie" src="data:image/jpeg;base64,' + logo + '"></div>\n<header>'),
    ('<select id="surah"></select></div>',
     '<select id="surah"></select>'
     '<div class="listen"><button id="play" class="act">▶ Listen</button>'
     '<a id="qlink" class="act link" target="_blank" rel="noopener">Open on Quran.com ↗</a>'
     '<span class="reciter">Recitation: Mishary Rashid Alafasy</span></div></div>'),
    ('<button id="showOrder" class="act">📖 Put the surah in order</button>',
     '<button id="showOrder" class="act">🧩 Put the surah in order</button>'
     '<button id="showRead" class="act">📖 Read with translation</button>'),
    ('<button id="again" class="act">🔀 Try the order again</button></section>',
     '<button id="again" class="act">🔀 Try the order again</button></section>\n'
     '<section id="reader"><h2 id="readerTitle"></h2><div id="readerBody"></div></section>\n'
     '<p class="credit">English translation: Sahih International · Recitation: Mishary Rashid Alafasy</p>'),
    ("b.className='ayah';b.textContent=x.t;", "b.className='ayah';b.innerHTML=ayahHTML(x.i);"),
    ("level2.style.display='none';grid.innerHTML='';",
     "level2.style.display='none';reader.style.display='none';stopAudio();setLink();grid.innerHTML='';"),
    ("document.getElementById('again').addEventListener('click',startOrder);",
     "document.getElementById('again').addEventListener('click',startOrder);"
     "document.getElementById('showRead').addEventListener('click',()=>{showRead();reader.scrollIntoView()});"),
    ("let next=0;", "let next=0;" + JS),
]
for a, b in R:
    assert src.count(a) == 1, a[:70]
    src = src.replace(a, b)
open(OUT, 'w', encoding='utf-8').write(src)
print('built', OUT, len(src) // 1024, 'KB')
