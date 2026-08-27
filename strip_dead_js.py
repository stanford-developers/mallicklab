#!/usr/bin/env python3
"""Remove Joomla-era JavaScript that no longer functions.

Nine of the ten pages load scripts that require MooTools or jQuery without
loading either library, so every one of them throws on load. Only bio.html
still has the libraries.

Nothing user-facing depends on the removed code:

  * the slider runs on the hand-written vanilla script at the end of index.html
  * the nav has no submenus anywhere (`dj-submenu` count is zero), so djmenu.js
    has nothing to do even where it works
  * djselect.js swaps the nav for a <select> under 800px, paired with the inline
    rule `#dj-main90.allowHide { display:none }` and an inline MooTools call
    that adds that class. That call throws on every page except bio, which is
    why every page except bio already falls back to a plain link list on
    mobile. Removing the script and the class-adder together makes bio match.

bio.html keeps jquery/mootools: templates/.../js/scripts.js genuinely uses
jQuery for the back-to-top fade. Its unused Joomla libraries are left alone.

Run from the repo root:  python3 strip_dead_js.py
Idempotent.
"""
import os, re, sys

REPO = os.path.dirname(os.path.abspath(__file__))

DEAD_SRC = [
    'modules/mod_djmenu/assets/js/dropline-helper.js',
    'modules/mod_djmenu/assets/js/djselect.js',
    'modules/mod_djmenu/assets/js/djmenu.js',
    'components/com_djmediatools/assets/js/powertools-1.2.0.js',
    'components/com_djmediatools/layouts/slideshow/js/slideshow.js',
    'components/com_djmediatools/layouts/tabber/js/tabber.js',
]

# Inline blocks are removed only when they contain a MooTools domready call.
# That is Joomla/DJ generated code and is specific enough to be safe:
# `window.addEvent(` is not `window.addEventListener(`, which our own scripts
# use, so the research page's tab script and the slider script are untouched.
# Also removed: the Google Analytics block on bio.html. Two GA snippets were
# merged at some point, overwriting the account id with fragments of the other
# and leaving unescaped quotes, so the block is a syntax error and never runs.
# It also targets ga.js (Classic Analytics), which Google shut down. bio.html is
# the only page that had any analytics at all, so the site currently has none.
INLINE_MARKER = re.compile(r"window\.addEvent\('domready'|_gaq")

PAGES = [f for f in sorted(os.listdir(REPO)) if f.endswith('.html')]

def strip_src(html):
    n = 0
    for src in DEAD_SRC:
        pat = re.compile(r'[ \t]*<script[^>]*\bsrc="' + re.escape(src) + r'"[^>]*>\s*</script>\s*\n?', re.I)
        html, k = pat.subn('', html)
        n += k
    return html, n

def strip_inline(html):
    out, n, pos = [], 0, 0
    for m in re.finditer(r'[ \t]*<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>\s*\n?', html, re.S | re.I):
        if INLINE_MARKER.search(m.group(1)):
            out.append(html[pos:m.start()])
            pos = m.end()
            n += 1
    out.append(html[pos:])
    return ''.join(out), n

report = []
for f in PAGES:
    p = os.path.join(REPO, f)
    src = open(p, encoding='utf-8', errors='surrogateescape').read()
    out, n_src = strip_src(src)
    out, n_inline = strip_inline(out)
    if n_src or n_inline:
        open(p, 'w', encoding='utf-8', errors='surrogateescape').write(out)
        report.append((f, n_src, n_inline, len(src) - len(out)))

print(f"{'file':24}{'<script src>':>13}{'inline':>8}{'bytes':>10}")
print('-' * 55)
for f, a, b, d in report:
    print(f'{f:24}{a:>13}{b:>8}{d:>10,}')
print('-' * 55)
print(f'{len(report)} files, {sum(r[1] for r in report)} script tags, '
      f'{sum(r[2] for r in report)} inline blocks, {sum(r[3] for r in report):,} bytes')
