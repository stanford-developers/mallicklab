# Remaining changes — on top of commit 0793b58

The dead-widget cleanup, `people.json`, the four section images and
`research_content.md` are already pushed. Nothing here repeats them.

## 1. Copy these four files to the repo root

```
research.html        the five-area page, now live (replaces the old 3-area page)
index.html           slider rebuilt (6 slides, controls fixed); feed links removed
build_research.py    updated: targets research.html, adds deep-link anchors
build_slider.py      new: regenerates the slider from a SLIDES list
```

## 2. Delete 23 stale files

Nothing links to any of them. Verified with a reachability walk from
`index.html`, then a local-link check across all 496 references on the
remaining pages.

The full list is in `DELETE_THESE.txt`. As one command:

```
git rm $(cat DELETE_THESE.txt | tr '\n' ' ')
```

What they were:

- **`*87e8.html`** (7) — HTTrack mirrors of `?tmpl=component&print=1`, the print
  layouts. Frozen at mirror time: `research87e8.html` still holds the old
  three-area text, and `pubs87e8.html` renders zero publications against 125 in
  the live page. The gear menu that linked them is gone.
- **`component/mailto/`** (8) — email-a-friend forms POSTing to a Joomla
  endpoint that no longer exists.
- **`index-2.html`, `indexa699.html`** — homepage duplicates.
- **`index7b17.html`, `indexc0d0.html`** — Joomla RSS and Atom feeds, both with
  **zero entries**. They were reachable only through `<link rel="alternate">`
  autodiscovery; those two lines are already removed from the `index.html` in
  this folder, so the files and the page change go together.
- **`research_new.html`** — its content is now `research.html`.
- **`futzedpixels.png`** (both sizes) — artwork for the retired "integrated
  omics" slide.

Kept despite being unlinked: `peeps_template.html` and `pubs_template.html`
(generator inputs), `pubmed-import-tool.html` (the Publication Manager that
reads `publications.json`), and the 0-byte guards under `templates/`.

## Deep links

Tab controls carry linkable ids, so anything can open a specific summary:

| Area | Section | Simple | Technical |
|---|---|---|---|
| Tumor Ecology | `#ecology` | `#ecology-simple` | `#ecology-technical` |
| Biomarker Discovery | `#biomarkers` | `#biomarkers-simple` | `#biomarkers-technical` |
| Systems Biology | `#networks` | `#networks-simple` | `#networks-technical` |
| Meaningful AI | `#meaningful-ai` | `#meaningful-ai-simple` | `#meaningful-ai-technical` |
| Methods & Technology | `#methods` | `#methods-simple` | `#methods-technical` |

The page reads the hash on load and on change, opens the matching summary and
scrolls the section into view, re-running on `load` so images shifting the
layout can't leave the target off-screen.

## Regenerating

Both scripts sit at the repo root beside `generate_pubs.py`, resolve paths
relative to themselves, and are idempotent.

```
python3 build_research.py    # research.html from research_content.md
python3 build_slider.py      # the index.html slider from its SLIDES list
```

Edit `research_content.md` for wording, or `SLIDES` in `build_slider.py` for
slide order, captions and links. Editing the HTML directly works but the next
run overwrites it.

## Still open

- **proteoWizard slide** points at `research.html#methods-simple`. Change
  `SLIDES[5]['link']` to `proteowizard.html` once that page exists.
- **`proteowizard.html`** not built: outside the top nav, linked from the slider
  and the research page, pointing out to <http://www.proteowizard.org>.
- **Magic** not yet added as a top-level nav category.
- **Section figures** are interim; Michelle's diagrams can reuse the filenames.
- **`README.md` in the repo** still describes the draft workflow and is now
  stale — replace or remove it.
