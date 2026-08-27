# Header wrap fix + dead JavaScript removal — on top of commit 1423deb

## 1. Header wrap (the original problem)

Your console output settled it:

```
viewport: 1838   container: 962   logo: 380   menu: 583   slack: -0
barPad: "0px"    pad: "14px"      lato: true  wrapped: true
```

At 1838px it still wrapped, so this was never about window width.
`.container-fluid` is capped at 962px regardless, and with Lato the logo block
(380) plus the nav (583) comes to **963px** — one pixel over, so the nav dropped
below the logo at every size.

`barPad: 0px` confirms the earlier padding fix deployed and applied. It fixed a
real home-vs-inner-page inconsistency, but that one only bites below ~1010px,
so it was never your symptom.

Fix: nav item padding 14px -> 11px, taking the nav from 583 to 541 and turning
-1px of slack into **+41px**. Computed from your Lato measurement, not from my
sandbox, which cannot load Lato and was running ~12% narrow.

## 2. Dead JavaScript removed (`strip_dead_js.py`)

Nine of ten pages loaded scripts needing MooTools or jQuery without loading
either library, so every one threw on load. Removed: **33 script tags and 5
inline blocks across 10 files, ~13.8 KB.**

Console errors, before and after:

| page | before | after |
|---|---|---|
| index.html | 7 | 0 |
| research.html | 3 | 0 |
| bio.html | 1 | 0 |
| faq / funding / peeps / pubs / resources | 3 each | 0 |

Nothing user-facing was lost. The slider runs on the hand-written vanilla
script; the nav has no submenus on any page, so `djmenu.js` had nothing to do
even where it worked.

### The one behaviour change: bio.html mobile nav

`djselect.js` swapped the nav for a `<select>` under 800px, paired with the
inline rule `#dj-main90.allowHide { display:none }` and an inline MooTools call
that adds that class. That call threw everywhere except bio, which is why every
other page already fell back to a plain link list on mobile. Removing the script
and the class-adder together makes bio match: **all pages now show the link
list**. Verified 7 visible nav links at 480px on every page.

`bio.html` keeps jquery/mootools, since `templates/.../js/scripts.js` genuinely
uses jQuery for the back-to-top fade. Its other unused Joomla libraries
(caption, modal, bootstrap, styleswitcher) are left alone — removable later,
but not dead in the same sense.

### Analytics — worth knowing

The Google Analytics block on `bio.html` was removed. It could not work:

```js
_gaq.push(['_setAccount', '   (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r']);
```

Two GA snippets were merged at some point, overwriting the account id with
fragments of the other and leaving unescaped quotes, so the block was a syntax
error and never executed. It also targeted `ga.js` (Classic Analytics), which
Google shut down.

**bio.html was the only page with any analytics, so the site has none and has
not had any for some time.** If you want it, that is a fresh GA4 tag on every
page — a new task, not a restoration.

## Verified

- 0 console errors on all 8 content pages
- Nav works at 1280px and 480px on every page (7 links each)
- Slider: 6 slides, deep link to `research.html#meaningful-ai-simple` opens the
  right panel
- Research tabs still work
- All four generators re-run with no change, so nothing resurrects

## Regenerating

```
python3 strip_dead_js.py    # idempotent, safe to re-run
python3 build_slider.py
```
