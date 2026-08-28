# Anchor fix, done properly — on top of commit 80943d8

Four files: `research.html`, `index.html`, `build_research.py`, `build_slider.py`.

## The actual fix, this time

Your suggestion was right, and it's a better fix than either of my previous
two attempts: **move the anchor, not the scroll logic.**

`#ecology-simple` and `#ecology-technical` used to be the *id of the visible
tab button*. That's the real root cause of everything in this thread: a
fragment pointing at a real, visible, interactive element is something a
browser can decide to scroll to on its own, at its own timing, and Safari's
timing put it after our correction ran — twice, in two different ways, which
is why the first two fixes (stripping the hash, then obfuscating it with a
`!` prefix) each patched one symptom and missed the next one.

This fix removes the conflict instead of racing it. Each section now has two
invisible, zero-height anchors as its very first content:

```html
<span class="rp-anchor" id="ecology-simple" data-panel="simple"></span>
<span class="rp-anchor" id="ecology-technical" data-panel="technical"></span>
```

`#ecology-simple` is now the anchor's id, not the button's. The button gets an
internal id (`ecology-tab-simple`) used only for `aria-controls` /
`aria-labelledby` wiring — never exposed as a link target. Wherever a browser
points a `#ecology-simple` link — natively, via our own script, whenever,
however many times — it lands in the same place, because that's the only
place the id exists. There is no wrong position left to land on, so there's
nothing to fight and no timing race to lose.

`display:none` was deliberately avoided for the anchor — a non-rendered
element has no box and can't be scrolled to at all by native fragment
navigation. `height:0; overflow:hidden; visibility:hidden` keeps it invisible
and inert while still occupying a real (zero-height) point in the layout.

## What's simpler now

- No more hash-stripping on load
- No more `#!` prefix, no more rewriting the address bar after scrolling
- `openFromHash` is about half the size of the last version
- The slider's links are back to the plain, ordinary form
  (`research.html#ecology-simple`) — no special-casing needed there either

The only piece carried over unchanged is `ensureScrollRoom`, which pads the
bottom of the page when a section near the very end doesn't have enough room
below it to reach the top of the viewport. That's a real, separate issue
(a short page can't be scrolled further than its own height) and has nothing
to do with the id-collision problem above.

## Verified (Chromium)

- `#ecology`, plus `#ecology-simple` / `#ecology-technical` and the same pairs
  for biomarkers, meaningful-ai, and methods, all land at exactly 18px
- Correct panel opens in every case
- Anchors measure 0px height; the section itself does not
- No-JS fallback still shows both summaries, stacked
- In-page hashchange navigation, both directions, no listener recursion
- Slider click-through, plain-form link, lands correctly end to end
- Both builds idempotent
- All tags balanced

## Still the same honest caveat

I don't have Safari to test against, only headless Chromium. What's different
this time is that the fix no longer depends on any Safari-specific timing
assumption at all — it works by making the "wrong" and "right" scroll
destinations the same physical point, which should hold regardless of when
any browser decides to act on the fragment. That's a stronger basis for
confidence than the previous two attempts, but it is still not the same as
having tested it in the browser where the bug lives.

## Regenerating

```
python3 build_research.py
python3 build_slider.py
```
