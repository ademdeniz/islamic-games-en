"""Rebuild the whole website with the mosque's details from site.json (name, logo, address).

  python3 tools/build_site.py

Runs every builder: all games, the Ilmihal lessons, Sufara, the year plan, the duty page and the home page.
(Weekly updates already sent to parents are not rebuilt – see tools/build_update.py.)
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import rebuild_all  # noqa: E402

PY = sys.executable


def run(cmd):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f'FAILED: {" ".join(cmd)}\n{(r.stderr or r.stdout)[-1500:]}')


def main():
    games = sorted(g for g in os.listdir(os.path.join(ROOT, 'games')) if os.path.isdir(os.path.join(ROOT, 'games', g)))
    for k, game in enumerate(games, 1):
        for cmd in rebuild_all.steps(game):
            run(cmd)
        print(f'\rgames {k}/{len(games)}', end='', flush=True)
    print()
    for script in ['build_lessons.py', 'build_sufara.py', 'build_plan.py', 'build_duty.py', 'build_credits.py', 'build_home.py']:
        if os.path.exists(os.path.join(ROOT, 'tools', script)):
            run([PY, os.path.join('tools', script)])
            print('done', script)
    print('Website rebuilt for', __import__('site_settings').NAME)


if __name__ == '__main__':
    main()
