"""Build the credits page: credits/index.html – who made the games, lessons, Qur'an text and recitation.

  python3 tools/build_credits.py
"""
import html
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import site_settings  # noqa: E402
from build_lessons_core import brand  # noqa: E402

PAGE = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Credits</title>
<style>
:root{--bg:#fbf7ec;--card:#fff;--ink:#1d1a14;--muted:#6b604d;--line:#e7dcc2;--green:#0f5a3f}
@media (prefers-color-scheme:dark){:root{--bg:#15130f;--card:#1f1c17;--ink:#f1ebdf;--muted:#b3a78f;--line:#3a342a;--green:#6fcf9c}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Arial,sans-serif}
main{max-width:760px;margin:auto;padding:12px 16px 48px}h1{color:var(--green);margin:8px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:12px 16px;margin:12px 0}
h2{font-size:18px;color:var(--green);margin:0 0 4px}a{color:var(--green);font-weight:600}.muted{color:var(--muted);font-size:14px}
</style></head><body><main>
<h1>Credits</h1>
<p>This maktab website for __NAME__ is built on the work of others. May Allah reward them.</p>
<div class="card"><h2>The games – Abdo ef. Rekić</h2>
<p>The learning games are English versions of the Bosnian maktab games by <b>Abdo ef. Rekić</b> (Bihać), used with his kind permission.
His original games: <a href="https://github.com/rekicabdo-bihac">github.com/rekicabdo-bihac</a>.</p></div>
<div class="card"><h2>The Ilmihal lessons – El-Kalem</h2>
<p>The lessons follow the <b>Ilmihal 1–3</b> books for maktab (El-Kalem, Rijaset of the Islamic Community in Bosnia and Herzegovina,
Sarajevo, 2020), used with permission. Authors: Ibrahim Softić (Ilmihal 1); J. Salkica, R. Ibreljić, I. Jusufović, S. Hibović and
M. Bilčević (Ilmihal 2 and 3).</p></div>
<div class="card"><h2>The Qur’an</h2>
<p>English meanings: <b>Sahih International</b>, via <a href="https://alquran.cloud">AlQuran.cloud</a>. Recitation: <b>Mishary Rashid Alafasy</b>.
Arabic text, word-by-word audio and timings: <a href="https://quran.com">Quran.com</a>.</p></div>
<div class="card"><h2>Sufara</h2>
<p>Letter videos: the “Sufara” playlist by <b>Amsal Memic</b>, with hfz. <b>Nermin Spahić</b> (YouTube).</p></div>
<div class="card"><h2>The English website</h2>
<p>Translated and built for the maktab of the Bosnian Islamic Community of Erie, Pennsylvania, and shared with other Bosnian mosques.</p></div>
<p class="muted"><a href="../">← Back to the games</a></p>
</main></body></html>'''


def build():
    os.makedirs(os.path.join(ROOT, 'credits'), exist_ok=True)
    open(os.path.join(ROOT, 'credits', 'index.html'), 'w', encoding='utf-8').write(brand(PAGE.replace('__NAME__', html.escape(site_settings.NAME))))
    print('built credits/index.html')


if __name__ == '__main__':
    build()
