"""Add Arabic text + italic English translation (Sahih International) to the memori-sure game.

Reads data/surahs.json (fetched from api.alquran.cloud: quran-uthmani + en.sahih).
"""
import json
import re

data = json.load(open('data/surahs.json', encoding='utf-8'))
f = 'games/memori-sure/index.html'
src = open(f, encoding='utf-8').read()

m = re.search(r'const S=(\{.*?\});', src, re.S)
S = json.loads(m.group(1))
order = ['101', '102', '103', '104', '105', '106', '107', '108', '109', '110',
         '111', '112', '113', '114', '1', '2']
NS = {}
for (name, lines), num in zip(S.items(), order):
    ay = data[num]['ayahs']
    assert len(ay) == len(lines), name
    NS[name] = [{"t": t, "ar": a['ar'], "en": a['en']} for t, a in zip(lines, ay)]
src = src[:m.start()] + 'const S=' + json.dumps(NS, ensure_ascii=False) + ';' + src[m.end():]

CSS = (
    '.ar{font-family:"Amiri","Scheherazade New","Geeza Pro","Traditional Arabic","Noto Naskh Arabic",serif;'
    'direction:rtl;font-size:1.45em;line-height:1.9;font-weight:400;display:block}\n'
    '.tr{display:block;font-weight:700} .en{display:block;font-style:italic;font-weight:400;color:#4a5a52;margin-top:3px}\n'
    '.front .ar{font-size:1.25em;line-height:1.6} .front .tr{font-size:.8em;font-weight:600} .front{flex-direction:column;overflow:auto;justify-content:flex-start} '
    '.front>span:first-child{margin-top:auto} .front>span:last-child{margin-bottom:auto}\n'
    '.front.long .ar{font-size:.95em;line-height:1.45} .front.long .tr{font-size:.68em}\n'
    '#reader{display:none;background:#fff;border:3px solid #c99b3b;border-radius:17px;padding:14px;margin-top:12px} '
    '#reader h2{text-align:center;margin-top:0}\n'
    '.row{padding:10px 4px;border-bottom:1px solid #eadfc4;text-align:center} .row:last-child{border:0} '
    '.num{display:inline-block;min-width:26px;padding:1px 6px;margin-bottom:3px;border-radius:20px;background:#075943;'
    'color:#fff;font-size:12px;font-weight:800}\n'
    '.credit{text-align:center;font-size:12px;color:#6b7a72;margin:14px 0}'
)
JS = (
    "function ayahHTML(a){return '<span class=\"ar\" lang=\"ar\">'+a.ar+'</span><span class=\"tr\">'+a.t+'</span>"
    "<span class=\"en\">'+a.en+'</span>'}\n"
    "function showRead(){reader.style.display='block';document.getElementById('readerTitle').textContent='📖 '+sel.value;"
    "document.getElementById('readerBody').innerHTML=current.map((a,i)=>'<div class=\"row\"><span class=\"num\">'+(i+1)"
    "+'</span>'+ayahHTML(a)+'</div>').join('');reader.scrollIntoView()}"
)

R = [
    ('border-radius:10px;font-weight:750;font-size:15px}',
     'border-radius:10px;font-weight:750;font-size:15px;color:#17372d}\n' + CSS),
    ('min-height:105px;perspective:800px;padding:0} .inner{height:100%;min-height:105px;',
     'min-height:125px;perspective:800px;padding:0} .inner{height:100%;min-height:125px;'),
    ('.inner,.card{min-height:94px}', '.inner,.card{min-height:115px}'),
    ('<button id="showOrder" class="act">📖 Put the surah in order</button>',
     '<button id="showOrder" class="act">🧩 Put the surah in order</button>'
     '<button id="showRead" class="act">📖 Read with translation</button>'),
    ('<button id="again" class="act">🔀 Try the order again</button></section>',
     '<button id="again" class="act">🔀 Try the order again</button></section>\n'
     '<section id="reader"><h2 id="readerTitle"></h2><div id="readerBody"></div></section>\n'
     '<p class="credit">Arabic text: Tanzil.net (Uthmani) · English translation: Sahih International</p>'),
    ("current.forEach((t,i)=>{cards.push({id:i,t});cards.push({id:i,t})})",
     "current.forEach((a,i)=>{cards.push({id:i,a});cards.push({id:i,a})})"),
    ("<div class=\"face front\">'+x.t+'</div>",
     "<div class=\"face front'+(x.a.ar.length>70?' long':'')+'\"><span class=\"ar\" lang=\"ar\">'+x.a.ar+'</span><span class=\"tr\">'+x.a.t+'</span></div>"),
    ("sh(current.map((t,i)=>({t,i}))).forEach(x=>{let b=document.createElement('button');b.className='ayah';b.textContent=x.t;",
     "sh(current.map((a,i)=>({a,i}))).forEach(x=>{let b=document.createElement('button');b.className='ayah';b.innerHTML=ayahHTML(x.a);"),
    ("level2.style.display='none';grid.innerHTML='';",
     "level2.style.display='none';reader.style.display='none';grid.innerHTML='';"),
    ("document.getElementById('again').addEventListener('click',startOrder);",
     "document.getElementById('again').addEventListener('click',startOrder);"
     "document.getElementById('showRead').addEventListener('click',showRead);"),
    ("let next=0;", "let next=0;\n" + JS),
    ("const sel=document.getElementById('surah'),",
     "const reader=document.getElementById('reader'),sel=document.getElementById('surah'),"),
]
for a, b in R:
    assert src.count(a) == 1, a[:70]
    src = src.replace(a, b)
open(f, 'w', encoding='utf-8').write(src)
print('ok')
