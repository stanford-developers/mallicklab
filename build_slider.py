#!/usr/bin/env python3
"""Rebuild the home page slider from the SLIDES list below.

The slider is DJ MediaTools markup left behind by the Joomla -> static
migration. Rather than hand-editing seven nested blocks, this regenerates the
slides and the tab strip from data, and injects CSS that repositions the
navigation controls (the mirror lost the runtime positioning that the
`navi_margin` option used to apply, leaving prev/next stacked on top of the
tab strip and play/pause floating in the middle of the image).

Run from the repo root:  python3 build_slider.py
Idempotent.
"""
import os, re, html, sys

REPO = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(REPO, 'index.html')
CACHE = 'media/djmediatools/cache'

# Slideshow timing. `delay` is the dwell on each slide, `duration` the length
# of the cross-fade. The mirrored defaults were 9000/3000, which meant twelve
# seconds a slide.
DELAY_MS    = 5000
DURATION_MS = 900

# Order follows the research page, with meaningful AI pulled to the front.
# `link` targets research.html anchors; -simple opens the plain-language
# summary for that area. See build_research.py for the anchor ids.
SLIDES = [
    dict(title='meaningful AI',
         desc='building AI for biomedicine that embeds biological knowledge, learns from '
              'realistic amounts of data, and explains itself',
         img=f'{CACHE}/5-front/700x350-crop-90-meaningful_ai.png',
         thumb=f'{CACHE}/5-front/70x40-crop-80-meaningful_ai.png',
         link='research.html#meaningful-ai-simple'),
    dict(title='tumor ecology &amp; spatial biology',
         desc='how cells, their neighbors, and their local environments interact to drive '
              'disease progression and drug resistance',
         img=f'{CACHE}/images/figs/banners/700x350-crop-90-flippedandstuff_compressed.jpg',
         thumb=f'{CACHE}/images/figs/banners/70x40-crop-80-flippedandstuff_compressed.jpg',
         link='research.html#ecology-simple'),
    dict(title='biomarker discovery',
         desc='connecting what happens inside a diseased tissue to what we can actually '
              'measure in a blood draw',
         img=f'{CACHE}/images/figs/banners/700x350-crop-90-bloodsamples_compressed.jpg',
         thumb=f'{CACHE}/images/figs/banners/70x40-crop-80-bloodsamples_compressed.jpg',
         link='research.html#biomarkers-simple'),
    dict(title='systems &amp; network biology',
         desc='how sets of molecules work together across regulatory scales to control '
              'cell behavior',
         img=f'{CACHE}/images/figs/banners/700x350-crop-90-networkyness_compressed.jpg',
         thumb=f'{CACHE}/images/figs/banners/70x40-crop-80-networkyness_compressed.jpg',
         link='research.html#networks-simple'),
    dict(title='methods &amp; technology',
         desc='instruments, laboratory methods, and open-source software built for the '
              'whole field to use',
         img=f'{CACHE}/images/figs/700x350-crop-90-psuedo2d_gel.jpg',
         thumb=f'{CACHE}/images/figs/70x40-crop-80-psuedo2d_gel.jpg',
         link='research.html#methods-simple'),
    dict(title='proteoWizard',
         desc='open-source software that accelerates the development of proteomics '
              'analysis tools',
         img=f'{CACHE}/images/figs/banners/700x350-crop-90-proteowizard_psdeps_onpurple_compressed.jpg',
         thumb=f'{CACHE}/images/figs/banners/70x40-crop-80-proteowizard_psdeps_onpurple_compressed.jpg',
         # TODO: point at proteowizard.html once that page exists
         link='research.html#methods-simple'),
]

def alt(s):
    return html.unescape(s).replace('"', '')

def slide_block(s, first):
    lazy = '' if first else ' loading="lazy"'
    # NB: .dj-image must stay a direct child of .dj-slide-in. Wrapping it in an
    # anchor breaks the module's sizing and drops the caption below the image.
    # Whole-slide clicking is handled by an overlay link in the caption block.
    return f'''\t\t\t\t<div class="dj-slide">
\t\t\t\t\t<div class="dj-slide-in">
\t\t\t\t\t\t<img{lazy} src="{s['img']}" alt="{alt(s['title'])}" class="dj-image" />
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t\t<div class="dj-slide-desc">
\t\t\t\t\t<!-- Slide description area: START -->
\t\t\t\t\t<div class="dj-slide-desc-in">
\t\t\t\t\t\t<div class="dj-slide-desc-bg"></div>
\t\t\t\t\t\t<div class="dj-slide-desc-text">
\t\t\t\t\t\t\t<a class="dj-slide-link" href="{s['link']}" target="_self">
\t\t\t\t\t\t\t\t<span class="dj-slide-title">{s['title']}</span>
\t\t\t\t\t\t\t\t<span class="dj-slide-description">{s['desc']}</span>
\t\t\t\t\t\t\t</a>
\t\t\t\t\t\t\t<div style="clear: both"></div>
\t\t\t\t\t\t</div>
\t\t\t\t\t</div>
\t\t\t\t\t<!-- Slide description area: END -->
\t\t\t\t</div>
'''

def tab_block(s, first):
    cls = 'dj-tab dj-tab-active' if first else 'dj-tab '
    return f'''\t\t\t\t<div class="{cls}">
\t\t\t\t\t<span class="dj-tab-in">
\t\t\t\t\t\t<span>
\t\t\t\t\t\t\t<img loading="lazy" src="{s['thumb']}" alt="{alt(s['title'])}" width="70" height="40" />
\t\t\t\t\t\t</span><span>
\t\t\t\t\t\t{s['title']}</span>
\t\t\t\t\t</span>
\t\t\t\t</div>
'''

STYLE = '''
  /* BEGIN slider-controls (generated by build_slider.py) */
  /* ---- slider controls -------------------------------------------------
     The static mirror lost the runtime positioning DJ MediaTools applied via
     its `navi_margin` option: prev/next ended up stacked on top of the tab
     strip and play/pause in the middle of the image. Position them here
     against the slide area instead. ------------------------------------- */
  #dj-tabber5m98 .dj-navigation {
    position: absolute !important;
    left: 0 !important; right: 258px !important; width: auto !important;
    top: 0 !important; bottom: 0 !important; margin: 0 !important;
    pointer-events: none;                 /* let clicks reach the slide link */
  }
  #dj-tabber5m98 .dj-navigation-in { position: static !important; margin: 0 !important; }
  #dj-tabber5m98 .dj-prev,
  #dj-tabber5m98 .dj-next {
    position: absolute !important; top: 50% !important; bottom: auto !important;
    transform: translateY(-50%); margin: 0 !important;
    cursor: pointer; pointer-events: auto; opacity: .7;
    transition: opacity .15s;
  }
  #dj-tabber5m98 .dj-prev { left: 14px !important; right: auto !important; }
  #dj-tabber5m98 .dj-next { right: 14px !important; left: auto !important; }
  #dj-tabber5m98 .dj-prev:hover,
  #dj-tabber5m98 .dj-next:hover { opacity: 1; }
  /* play/pause kept (the slider autoplays, so it needs to be stoppable) but
     moved to the top corner, clear of the description overlay */
  #dj-tabber5m98 .dj-play,
  #dj-tabber5m98 .dj-pause {
    position: absolute !important; top: 12px !important; right: 14px !important;
    left: auto !important; bottom: auto !important; margin: 0 !important;
    cursor: pointer; pointer-events: auto; opacity: .55; transition: opacity .15s;
  }
  #dj-tabber5m98 .dj-play:hover,
  #dj-tabber5m98 .dj-pause:hover { opacity: 1; }
  /* Tab strip. The theme sets a fixed 80px tab height and zeroes the margin on
     :nth-last-child(2) - both tuned for the original seven slides, which with
     six leaves the strip overflowing and one separator missing. Let the tabs
     divide the strip evenly instead, whatever the count. */
  #dj-tabber5m98 .dj-tabs-in {
    display: flex; flex-direction: column; height: 100%;
  }
  /* separator between tabs only: :last-of-type can't be used because the
     indicator div is the real last child of .dj-tabs-in */
  #dj-tabber5m98 .dj-tabs-in .dj-tab {
    flex: 1 1 0; height: auto !important; min-height: 0;
    margin-bottom: 0 !important;
  }
  #dj-tabber5m98 .dj-tabs-in .dj-tab + .dj-tab { margin-top: 2px !important; }
  #dj-tabber5m98 .dj-tabs-in .dj-tab .dj-tab-in {
    display: flex; align-items: center; height: 100%;
  }

  /* the whole caption is the click target for the slide */
  #dj-tabber5m98 .dj-slide-link { display: block; color: inherit; text-decoration: none; }
  #dj-tabber5m98 .dj-slide-link .dj-slide-title,
  #dj-tabber5m98 .dj-slide-link .dj-slide-description { display: block; }
  #dj-tabber5m98 .dj-slide-link:hover .dj-slide-title { text-decoration: underline; }
  @media (max-width: 767px) {
    #dj-tabber5m98 .dj-navigation { right: 0 !important; }
  }
  /* END slider-controls */
'''

def main():
    page = open(PAGE, encoding='utf-8', errors='surrogateescape').read()

    # Each region is replaced wholesale, including its own closing tag, and
    # re-emitted with canonical whitespace. Preserving the original seam meant
    # inheriting leftover Joomla filler, which made repeat runs drift.

    # --- slides ---------------------------------------------------------
    m = re.search(r'<div class="dj-slides">.*?</div>\s*(?=<div class="dj-navigation">)',
                  page, re.S)
    if not m:
        sys.exit('could not locate the dj-slides block')
    slides = ''.join(slide_block(s, i == 0) for i, s in enumerate(SLIDES))
    page = (page[:m.start()]
            + '<div class="dj-slides">\n' + slides.rstrip('\n') + '\n\t\t</div>\n\t\t'
            + page[m.end():])

    # --- tab strip ------------------------------------------------------
    m = re.search(r'<div class="dj-tabs-in">.*?</div>\s*(?=<div class="dj-tab-indicator)',
                  page, re.S)
    if not m:
        sys.exit('could not locate the dj-tabs-in block')
    tabs = ''.join(tab_block(s, i == 0) for i, s in enumerate(SLIDES))
    # NB: .dj-tab-indicator lives inside .dj-tabs-in, and the </div> that
    # follows the indicator is what closes .dj-tabs-in. So no closing tag is
    # emitted here - adding one closes #jm-allpage early and the page loses
    # its white background below the slider.
    page = (page[:m.start()]
            + '<div class="dj-tabs-in">\n' + tabs.rstrip('\n') + '\n\t\t\t'
            + page[m.end():])

    # --- dead feed autodiscovery ---------------------------------------
    # index7b17.html / indexc0d0.html are Joomla RSS + Atom stubs with zero
    # entries, and are being deleted. Drop the <link rel="alternate"> pair so
    # nothing advertises them.
    page = re.sub(r'\n\t<link href="index(?:7b17|c0d0)\.html\?format=feed[^>]*/>', '', page)

    # --- slideshow timing ----------------------------------------------
    page, n = re.subn(r'(duration:\s*)\d+', r'\g<1>' + str(DURATION_MS), page)
    page, n2 = re.subn(r'(delay:\s*)\d+', r'\g<1>' + str(DELAY_MS), page)
    if not (n and n2):
        sys.exit('could not find the DJImageTabber timing options')

    # --- control CSS (idempotent) --------------------------------------
    page = re.sub(r'\n  /\* BEGIN slider-controls.*?/\* END slider-controls \*/\n',
                  '', page, flags=re.S)
    # Append at the very end of the last inline stylesheet. Anchoring to a
    # comment inside the sheet is unsafe: the obvious markers here sit inside
    # `@media (max-width: 480px)`, which would scope these rules to phones.
    m = re.search(r'\n</style>\s*</head>', page)
    if not m:
        sys.exit('could not find the stylesheet insertion point')
    page = page[:m.start()] + '\n' + STYLE.rstrip('\n') + page[m.start():]

    open(PAGE, 'w', encoding='utf-8', errors='surrogateescape').write(page)
    print(f'rebuilt slider: {len(SLIDES)} slides, {len(SLIDES)} tabs')
    for s in SLIDES:
        print(f"  {html.unescape(s['title']):32} -> {s['link']}")

if __name__ == '__main__':
    main()
