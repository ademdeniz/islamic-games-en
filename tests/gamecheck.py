"""Checks that an English game is a faithful, working translation of its Bosnian original.

The core idea: a translation may change *text* (HTML text, JS/CSS string contents, a few text attributes) but not
*code*. So we reduce both files to a "skeleton" where every piece of text is masked, and require the skeletons to be
identical. Because the skeletons match, the strings line up one-to-one, which lets us also check that repeated
strings (e.g. quiz answers compared with `===` against option text) were translated consistently.
"""
import html as htmllib
import importlib.util
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import skel  # noqa: E402

BLOB = re.compile(r'data:[a-z]+/[a-z0-9.+-]+;base64,[A-Za-z0-9+/=\s]+?(?=["\')])')
TEXT_ATTRS = {'title', 'alt', 'placeholder', 'aria-label', 'content', 'value', 'label', 'lang'}
ARABIC = re.compile(r'[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]')
REGEX_BEFORE = set('(,=:[!&|?{};+-*%<>~^')
REGEX_WORDS = {'return', 'typeof', 'case', 'do', 'else', 'in', 'of', 'new', 'delete', 'void', 'throw', 'yield', 'await'}

# Games built by a dedicated script instead of a translation table, with deliberate structural changes.
BUILT_SPECIALLY = {'memori-sure': 'adds translation, reader panel and recitation audio (tools/build_memori_sure.py)'}


# ---------------------------------------------------------------- JS lexer
def lex_js(src, strings):
    """Return JS with string/template text masked and comments removed; append string contents to `strings`."""
    out, i, n = [], 0, len(src)
    prev, word = '', ''
    while i < n:
        c = src[i]
        nx = src[i + 1] if i + 1 < n else ''
        if c in '"\'':
            j = i + 1
            while j < n and src[j] != c and src[j] != '\n':
                j += 2 if src[j] == '\\' else 1
            strings.append(src[i + 1:j])
            out.append(c + 'S' + c)
            i, prev, word = j + 1, 'S', ''
        elif c == '`':
            i = lex_template(src, i + 1, out, strings)
            prev, word = 'S', ''
        elif c == '/' and nx == '/':
            while i < n and src[i] != '\n':
                i += 1
        elif c == '/' and nx == '*':
            e = src.find('*/', i + 2)
            i = n if e < 0 else e + 2
        elif c == '/' and (prev == '' or prev in REGEX_BEFORE or word in REGEX_WORDS):
            j, in_class = i + 1, False
            while j < n and src[j] != '\n':
                if src[j] == '\\':
                    j += 2
                    continue
                if src[j] == '[':
                    in_class = True
                elif src[j] == ']':
                    in_class = False
                elif src[j] == '/' and not in_class:
                    break
                j += 1
            j += 1
            while j < n and src[j].isalpha():
                j += 1
            out.append(src[i:j])
            i, prev, word = j, 'R', ''
        else:
            out.append(c)
            if not c.isspace():
                if c.isalnum() or c in '_$':
                    last = src[i - 1] if i else ''
                    word = word + c if (last.isalnum() or last in '_$') else c
                else:
                    word = ''
                prev = c
            i += 1
    return re.sub(r'\s+', ' ', ''.join(out)).strip()


def lex_template(src, i, out, strings):
    """Lex a template literal starting after the opening backtick; returns index after the closing backtick."""
    n, buf = len(src), []
    out.append('`')
    while i < n:
        c = src[i]
        if c == '\\':
            buf.append(src[i:i + 2])
            i += 2
        elif c == '`':
            strings.append(''.join(buf))
            out.append('T`')
            return i + 1
        elif c == '$' and i + 1 < n and src[i + 1] == '{':
            strings.append(''.join(buf))
            buf = []
            depth, j = 1, i + 2
            while j < n and depth:
                if src[j] == '{':
                    depth += 1
                elif src[j] == '}':
                    depth -= 1
                elif src[j] in '"\'`':
                    q = src[j]
                    j += 1
                    while j < n and src[j] != q:
                        j += 2 if src[j] == '\\' else 1
                j += 1
            out.append('T${' + lex_js(src[i + 2:j - 1], strings) + '}')
            i = j
        else:
            buf.append(c)
            i += 1
    return n


# ---------------------------------------------------------------- HTML skeleton
PARTS = re.compile(r'(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<!--.*?-->|<[^>]+>)', re.S | re.I)
ATTR = re.compile(r'(\s[\w:.-]+)(\s*=\s*)("[^"]*"|\'[^\']*\'|[^\s>]+)')


def mask_tag(tag, strings):
    def attr(m):
        name, eq, val = m.group(1), m.group(2), m.group(3)
        key = name.strip().lower()
        raw = val[1:-1] if val[:1] in '"\'' else val
        if key in TEXT_ATTRS:
            strings.append(htmllib.unescape(raw))
            return name + '=T'
        if key.startswith('on'):
            return name + '={' + lex_js(htmllib.unescape(raw), strings) + '}'
        return name + '=' + raw
    return re.sub(r'\s+', ' ', ATTR.sub(attr, tag))


def skeleton(html):
    """Return (skeleton, strings) for a whole HTML document."""
    html = BLOB.sub('BLOB', html)
    strings, out = [], []
    for part in PARTS.split(html):
        if not part:
            continue
        low = part[:8].lower()
        if low.startswith('<script'):
            head_end = part.index('>') + 1
            head, body = part[:head_end], part[head_end:-len('</script>')]
            if re.search(r'type\s*=\s*["\']?(application/(ld\+)?json|text/template)', head, re.I):
                strings.append(body)
                out.append(mask_tag(head, strings) + 'JSON</script>')
            else:
                out.append(mask_tag(head, strings) + lex_js(body, strings) + '</script>')
        elif low.startswith('<style'):
            body = re.sub(r'/\*.*?\*/', '', part, flags=re.S)

            def css_str(m):
                strings.append(m.group(0)[1:-1])
                return '"S"'
            out.append(re.sub(r'\s+', ' ', re.sub(r'"[^"\n]*"|\'[^\'\n]*\'', css_str, body)))
        elif low.startswith('<!--'):
            continue
        elif part.startswith('<'):
            out.append(mask_tag(part, strings))
        elif part.strip():
            strings.append(htmllib.unescape(part.strip()))
            out.append('T')
    return ''.join(out), strings


# ---------------------------------------------------------------- per-game data
def table(game):
    path = os.path.join(ROOT, 'tools', 'tr', game + '.py')
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location('tr_' + game.replace('-', '_'), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def original_html(game):
    return open(skel.main_file(game), encoding='utf-8').read()


def translated_html(game):
    return open(os.path.join(ROOT, 'games', game, 'index.html'), encoding='utf-8').read()


def strip_brand(html):
    html = html.replace(skel.BRAND_CSS, '')
    return re.sub(r'<div class="bz-brand"><img [^>]*></div>', '', html, count=1)


def original_minus_deletions(game):
    """Original HTML with the table's deletions applied (entries translated to '' such as the author credit)."""
    src = original_html(game)
    mod = table(game)
    for bs, en in (getattr(mod, 'T', []) if mod else []):
        if en == '':
            src = src.replace(bs, '')
    return src


def structural_reason(game):
    if game in BUILT_SPECIALLY:
        return BUILT_SPECIALLY[game]
    mod = table(game)
    return getattr(mod, 'STRUCTURAL', None) if mod else None


def allow(game, name):
    mod = table(game)
    return set(getattr(mod, name, ()) if mod else ())


def visible_bosnian(strings, allowed):
    """Bosnian-looking words found in user-visible text (not code identifiers)."""
    hits = {}
    for s in strings:
        s = BLOB.sub('', s)
        for m in skel.BS_WORDS.finditer(s):
            w = m.group(0)
            if w in allowed or w.lower() in allowed:
                continue
            hits.setdefault(w, s[max(0, m.start() - 40):m.end() + 40])
    return hits
