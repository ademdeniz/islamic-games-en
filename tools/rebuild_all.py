"""Rebuild every game from what is in the repository, and report any game whose result differs from games/.

  python3 tools/rebuild_all.py            # rebuild all, compare, restore the committed files
  python3 tools/rebuild_all.py <game>...  # only these

Use it in a fresh clone to prove nothing depends on files that only exist on one computer (work/ is not in git).
"""
import hashlib
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
SPECIAL = {  # games that are built by their own script instead of a translation table
    'memori-sure': ['tools/build_memori_sure.py'],
    'citaj-kuran': ['tools/build_citaj_kuran.py'],
    'learn-surahs-by-heart': ['tools/build_hifz.py'],
}


def steps(game):
    if game in SPECIAL:
        return [[PY] + SPECIAL[game]]
    if os.path.exists(os.path.join(ROOT, 'tools', 'tr', game + '_build.py')):
        return [[PY, 'tools/skel.py', 'extract', game], [PY, f'tools/tr/{game}_build.py'], [PY, 'tools/skel.py', 'build', game]]
    if os.path.exists(os.path.join(ROOT, 'tools', 'tr', game + '.en.html')):   # frozen English skeleton
        return [[PY, 'tools/skel.py', 'extract', game], ['cp', f'tools/tr/{game}.en.html', f'work/{game}.en.html'],
                [PY, 'tools/skel.py', 'build', game]]
    return [[PY, 'tools/translate.py', game]]


def digest(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest() if os.path.exists(path) else None


def main(games):
    bad = []
    for game in games:
        out = os.path.join(ROOT, 'games', game, 'index.html')
        before = open(out, 'rb').read()
        err = None
        for cmd in steps(game):
            r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            if r.returncode:
                err = (' '.join(cmd) + ': ' + (r.stderr or r.stdout).strip().splitlines()[-1])[:300]
                break
        same = not err and open(out, 'rb').read() == before
        print(('OK      ' if same else 'DIFFERS ') + game + (f'  [{err}]' if err else ''))
        if not same:
            bad.append(game)
        open(out, 'wb').write(before)   # always restore the committed game
    print(f'\n{len(games) - len(bad)} of {len(games)} games rebuild identically from the repository.')
    if bad:
        print('Not reproducible:', ' '.join(bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:] or sorted(os.listdir(os.path.join(ROOT, 'games')))))
