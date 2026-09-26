"""Browser tests for the online quiz's "Forgot password?" flow. Supabase is faked (page.route), so no real accounts
are touched; the Supabase JS library itself is loaded from its CDN, so these tests need internet access."""
import base64
import functools
import http.server
import json
import os
import re
import threading
import time

import pytest

import gamecheck as gc

GAME = 'islamski-milijunas-online'
SUPABASE = json.load(open(os.path.join(gc.ROOT, 'supabase', 'config.json')))['url']
USER = {'id': '11111111-1111-1111-1111-111111111111', 'aud': 'authenticated', 'role': 'authenticated',
        'email': 'kid@example.com', 'user_metadata': {'full_name': 'Test Kid'}, 'app_metadata': {},
        'created_at': '2026-01-01T00:00:00Z'}


def fake_jwt():
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip('=')
    return enc({'alg': 'HS256', 'typ': 'JWT'}) + '.' + enc(
        {'sub': USER['id'], 'exp': int(time.time()) + 3600, 'role': 'authenticated', 'email': USER['email']}) + '.sig'


@pytest.fixture(scope='module')
def server():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=gc.ROOT)
    handler.log_message = lambda *a: None
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield f'http://127.0.0.1:{httpd.server_address[1]}/games/{GAME}/'
    httpd.shutdown()


@pytest.fixture
def page(browser):
    p = browser.new_page()
    calls = []
    state = {'role': 'ucenik', 'teacher': None}

    def fake_supabase(route):
        req = route.request
        calls.append((req.method, req.url, req.post_data))
        path = req.url.split(SUPABASE, 1)[1]
        if path.startswith('/auth/v1/recover'):
            return route.fulfill(status=200, json={})
        if path.startswith('/auth/v1/user'):
            return route.fulfill(status=200, json=USER)
        if path.startswith('/rest/v1/profiles'):
            return route.fulfill(status=200, json={'id': USER['id'], 'full_name': 'Test Kid', 'role': state['role'],
                                                  'teacher_status': None, 'teacher_code': 'ABC123'})
        if path.startswith('/rest/v1/teacher_students'):
            return route.fulfill(status=200, json=[{'teacher_id': state['teacher']}] if state['teacher'] else [])
        if path.startswith('/rest/v1/'):
            return route.fulfill(status=200, json=[])
        return route.fulfill(status=200, json={})

    p.route(SUPABASE + '/**', fake_supabase)
    p.calls = calls
    p.state = state
    yield p
    p.close()


def load(page, url):
    try:
        page.goto(url, timeout=30000)
        page.wait_for_function('!!(window.supabase && window.supabase.createClient)', timeout=15000)
    except Exception as e:
        pytest.skip(f'Supabase library could not load from the CDN (offline?): {e}')


def open_login(page):
    page.click('#onlineBtn')
    page.wait_for_selector('#forgotBtn', state='visible')


def test_forgot_password_link_is_shown(page, server):
    load(page, server)
    open_login(page)
    assert page.inner_text('#forgotBtn') == 'Forgot password?'


def test_forgot_password_needs_an_email(page, server):
    load(page, server)
    open_login(page)
    page.click('#forgotBtn')
    assert 'Type your e-mail' in page.inner_text('#onlineMsg')
    assert not [c for c in page.calls if '/recover' in c[1]], 'no reset e-mail request without an address'


def test_forgot_password_sends_reset_email_back_to_this_game(page, server):
    load(page, server)
    open_login(page)
    page.fill('#email', 'kid@example.com')
    page.click('#forgotBtn')
    page.wait_for_function("document.getElementById('onlineMsg').textContent.includes('we sent it an e-mail')")
    recover = [c for c in page.calls if '/auth/v1/recover' in c[1]]
    assert len(recover) == 1
    method, url, body = recover[0]
    assert method == 'POST' and json.loads(body)['email'] == 'kid@example.com'
    assert 'redirect_to=' in url and GAME in url, 'the e-mail link must lead back to this game'


def test_reset_link_shows_new_password_box_and_saves_it(page, server):
    token = fake_jwt()
    load(page, server + f'#access_token={token}&refresh_token=r1&expires_in=3600&expires_at={int(time.time()) + 3600}'
                        '&token_type=bearer&type=recovery')
    page.wait_for_selector('#authRecover', state='visible', timeout=10000)
    assert page.is_hidden('#authLoggedOut') and page.is_hidden('#authLoggedIn')

    page.fill('#newPassword', '123')
    page.click('#savePwBtn')
    assert 'at least 6 characters' in page.inner_text('#onlineMsg')
    assert not [c for c in page.calls if c[0] == 'PUT'], 'short password must not be sent'

    page.fill('#newPassword', 'NewSecret123')
    page.click('#savePwBtn')
    page.wait_for_function("document.getElementById('onlineMsg').textContent.includes('new password is saved')")
    put = [c for c in page.calls if c[0] == 'PUT' and '/auth/v1/user' in c[1]]
    assert put and json.loads(put[-1][2])['password'] == 'NewSecret123'
    page.wait_for_selector('#authLoggedIn', state='visible')
    assert page.is_hidden('#authRecover')
    assert page.inner_text('#who') == 'Test Kid'


# ---------------------------------------------------------------- login required to play
def logged_in(page, server):
    """Start the page with a saved Supabase session, as if the child had logged in earlier."""
    ref = SUPABASE.split('//')[1].split('.')[0]
    session = {'access_token': fake_jwt(), 'refresh_token': 'r1', 'token_type': 'bearer', 'expires_in': 3600,
               'expires_at': int(time.time()) + 3600, 'user': USER}
    page.add_init_script(f"localStorage.setItem('sb-{ref}-auth-token', {json.dumps(json.dumps(session))})")
    load(page, server)
    page.wait_for_function("document.getElementById('whoBar').textContent.includes('Test Kid')", timeout=10000)


def screen(page):
    return page.evaluate("document.querySelector('.screen.active').id")


def test_start_is_blocked_when_not_logged_in(page, server):
    load(page, server)
    page.click('#startBtn')
    assert screen(page) == 'online'
    assert 'Please log in' in page.inner_text('#onlineMsg')
    assert 'Log in to play' in page.inner_text('#whoBar')


def test_start_is_blocked_for_student_without_a_class(page, server):
    logged_in(page, server)
    assert 'join your mu’allim’s class' in page.inner_text('#whoBar')
    page.click('#startBtn')
    page.wait_for_function("document.querySelector('.screen.active').id === 'online'")
    assert 'send a request' in page.inner_text('#onlineMsg')


def test_student_in_a_class_can_play(page, server):
    page.state['teacher'] = '22222222-2222-2222-2222-222222222222'
    logged_in(page, server)
    assert 'your results go to your mu’allim' in page.inner_text('#whoBar')
    page.click('#startBtn')
    page.wait_for_function("document.querySelector('.screen.active').id === 'game'")


def test_student_accepted_after_page_load_can_play_without_reloading(page, server):
    logged_in(page, server)                      # not in a class when the page loaded …
    page.state['teacher'] = '22222222-2222-2222-2222-222222222222'   # … then the mu'allim accepts
    page.click('#startBtn')
    page.wait_for_function("document.querySelector('.screen.active').id === 'game'")


def test_teacher_can_try_the_quiz(page, server):
    page.state['role'] = 'mualim'
    logged_in(page, server)
    assert 'results are not saved for teachers' in page.inner_text('#whoBar')
    page.click('#startBtn')
    page.wait_for_function("document.querySelector('.screen.active').id === 'game'")


def test_offline_shows_a_clear_message_instead_of_failing_silently(browser, server):
    page = browser.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.route(re.compile(r'^https://'), lambda route: route.abort())   # no internet: Supabase library can't load
    page.goto(server)
    page.click('#startBtn')
    page.wait_for_function("document.querySelector('.screen.active').id === 'online'")
    assert 'Check your internet connection' in page.inner_text('#onlineMsg')
    assert not [e for e in errors if 'before initialization' in e], errors
    page.close()
