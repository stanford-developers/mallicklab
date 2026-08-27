# Slider timing + header alignment — on top of commit 1423deb

Two files: `index.html` and `build_slider.py`.

## 1. Dwell was still ~9s

I had been editing the wrong thing. `index.html` contains a hand-written
vanilla-JS slider at the end of `<body>`; the MooTools `new DJImageTabber(...)`
call near the top never initialises in the static mirror (no such object exists
on `window` at runtime), so that whole options block is dead code. The real
rotation is a plain `setInterval` with its own `var DELAY = 9000`.

Confirmed by setting `delay: 2000` in the MooTools config and measuring no
change at all — intervals stayed at exactly 9.0s.

Now `var DELAY = 5000` and `var DURATION = 900`, written by `build_slider.py`
from `DELAY_MS` / `DURATION_MS`. Measured: five consecutive intervals at 5.00s.
The dead MooTools options are kept in sync so nobody edits that number later
and concludes it does nothing.

Also fixed while in there: the inline script positioned the active-tab
indicator with a hard-coded `current * 80`, left from when tabs were 80px tall.
Since the tabs now divide the strip evenly it drifted a pixel per row. It
measures the tab instead — verified aligned on all six.

## 2. Nav wrapping below the logo on the home page

Not a regression: this predates all of my changes, back to the original HTTrack
import. And it isn't font size — nav metrics are identical on every page
(19px Lato 300, same padding, same 575px menu width).

`custom_css_*.css` pads `#jm-bar-in` 25px left and right on every page, and the
theme's more specific `#jm-bar.noheader #jm-bar-in` zeroes it again. Inner pages
carry `.noheader`; the home page cannot, because it has the `#jm-header` slider
region that tucks up into the bar. So the home page had 50px less usable width
and wrapped first.

Fixed with `#jm-bar:not(.noheader) #jm-bar-in { padding-left: 0; padding-right: 0 }`.
Deliberately without `!important`, so the 767px mobile rule (10px) still wins.

All pages now wrap at the same width (≤950px instead of ≤1000px for home).

## Note on the injected block

The generated stylesheet block is renamed from `slider-controls` to
`index-fixes`, since it now covers the header too. The strip pattern matches
both names, so regenerating won't leave a duplicate.

## Regenerating

```
python3 build_slider.py
```

Timing lives in `DELAY_MS` / `DURATION_MS` at the top.

## Still open

- **Pause/play timing.** `setInterval` keeps firing while paused and the handler
  just skips, so un-pausing lands mid-cycle and the next advance comes early.
  Fixing it properly means `clearInterval` on pause and `startTimer()` on play.
  Left alone as it's a behaviour change rather than a bug fix.
- proteoWizard page, Magic nav category, Michelle's diagrams, stale repo README.
