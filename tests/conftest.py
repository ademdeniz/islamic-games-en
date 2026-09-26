import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pytest_addoption(parser):
    parser.addoption('--game', action='append', default=[], help='only check these games (repeatable)')


def all_games():
    return sorted(d for d in os.listdir(os.path.join(ROOT, 'original')) if not d.startswith('.'))


def built_games():
    return [g for g in all_games() if os.path.exists(os.path.join(ROOT, 'games', g, 'index.html'))]


def pytest_generate_tests(metafunc):
    if 'game' in metafunc.fixturenames:
        chosen = metafunc.config.getoption('game') or built_games()
        metafunc.parametrize('game', chosen)


@pytest.fixture(scope='session')
def browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()
