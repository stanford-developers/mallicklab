# Safari anchor-scroll fix — on top of commit 2c6877f

Two files: `research.html` and `build_research.py`.

## What your console output showed

```
hash: "#ecology-simple"   section_id: "ecology"   section_top: -134
scrollY: 720              scrollMarginTop: "18px"   bodyPad: "0px"
```

Working the numbers: `scrollY + section_top` gives the section's real position
in the document, 586. Landing correctly needs `scrollY = 586 - 18 = 568`. The
page was actually at 720 — **152px too far**, and 152px is close to how far
down the "Learn more" tab row sits inside that section (thumbnail + title +
question + blurb). That points at a specific, known Safari behaviour: Safari
can perform its **own** native scroll-to-fragment on whatever element has the
id in the URL, and it can do this *after* our corrective script has already
run, silently overriding it. Since the id in the URL is `#ecology-simple` —
the small "Simple summary" button, not the section — Safari's native jump
lands on the button. That's "the Learn More row."

This also explains why it couldn't be reproduced in Chromium: Chromium doesn't
have this deferred-native-scroll behaviour, so every test I ran locally showed
the fix already working.

## The fix

Strip the hash from the URL the instant our script runs, so Safari has
nothing left to act on natively. Do the scroll ourselves using the saved
value. Restore the hash afterward via `history.replaceState`, which does not
itself trigger a scroll — so the URL still looks like `research.html#ecology-simple`
and stays shareable/bookmarkable.

## Verified (Chromium only — see caveat below)

- All five anchor forms land at exactly 18px from top
- The URL hash is correctly restored after the fix runs
- The correct summary panel opens in each case
- In-page navigation between two hash targets, no reload, still works
- The home-page slider's click-through still opens the right section and panel
- Build is idempotent

## I cannot test this directly in Safari

I don't have access to a Safari environment, only headless Chromium. The fix
is built on a real, working theory backed by the arithmetic in your console
output, and a documented Safari behaviour (deferred native fragment scroll),
but I have not been able to confirm the fix itself in the one browser where
the bug occurs. Please retest on the live site once this is deployed, and if
it's still off, send the same console snippet again — the new `finalHash`
output will tell us whether the hash-strip is even taking effect on your end.

## Regenerating

```
python3 build_research.py
```
