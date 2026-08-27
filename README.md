# Remaining changes — on top of commit 0793b58

The dead-widget cleanup, `people.json`, the four section images and
`research_content.md` are already pushed. Nothing here repeats them.

## 1. Copy these four files to the repo root

```
research.html        the five-area page, now live (replaces the old 3-area page)
index.html           slider rebuilt; timing, tab strip and controls fixed
build_research.py    updated: targets research.html, adds deep-link anchors
build_slider.py      new: regenerates the slider from a SLIDES list
```

## 2. Delete 23 stale files

Nothing links to any of them. Verified with a reachability walk from
`index.html`, then a local-link check across all 496 references on the
remaining pages. The list is in `DELETE_THESE.txt`:

```
git rm $(cat DELETE_THESE.txt | tr '\n' ' ')
```

- **`*87e8.html`** (7) — HTTrack mirrors of `?tmpl=component&print=1`. Frozen at
  mirror time: `research87e8.html` still holds the old three-area text and
  `pubs87e8.html` renders zero publications against 125 live.
- **`component/mailto/`** (8) — forms POSTing to a Joomla endpoint that is gone.
- **`index-2.html`, `indexa699.html`** — homepage duplicates.
- **`index7b17.html`, `indexc0d0.html`** — RSS and Atom stubs with zero entries.
  `build_slider.py` strips the two `<link rel="alternate">` tags that pointed at
  them, so page and files go together.
- **`research_new.html`** — its content is now `research.html`.
- **`futzedpixels.png`** (both sizes) — artwork for the retired "integrated
  omics" slide.

Kept though unlinked: `peeps_template.html`, `pubs_template.html` (generator
inputs), `pubmed-import-tool.html`, and the 0-byte guards under `templates/`.

## Slider fixes in this round

- **Timing.** Was 9s dwell with a 3s cross-fade — about twelve seconds a slide.
  Now 5s and 900ms, set via `DELAY_MS` / `DURATION_MS` at the top of
  `build_slider.py`.
- **Missing separator.** The theme fixes tab height at 80px and zeroes the
  margin on `:nth-last-child(2)`, both tuned for the original seven slides. With
  six that overflowed the strip and dropped one separator. Tabs now divide the
  strip evenly whatever the count, with a separator between each and none
  trailing.
- **Black overview/news band.** A regression I introduced: `.dj-tab-indicator`
  lives *inside* `.dj-tabs-in`, and the `</div>` following it is what closes
  that container — so emitting my own closing tag left one extra `</div>`, which
  closed `#jm-allpage` early and dropped everything below the slider outside the
  white background. Fixed; div balance verified.

## Deep links

| Area | Section | Simple | Technical |
|---|---|---|---|
| Tumor Ecology | `#ecology` | `#ecology-simple` | `#ecology-technical` |
| Biomarker Discovery | `#biomarkers` | `#biomarkers-simple` | `#biomarkers-technical` |
| Systems Biology | `#networks` | `#networks-simple` | `#networks-technical` |
| Meaningful AI | `#meaningful-ai` | `#meaningful-ai-simple` | `#meaningful-ai-technical` |
| Methods & Technology | `#methods` | `#methods-simple` | `#methods-technical` |

## Regenerating

Both scripts sit at the repo root beside `generate_pubs.py`, resolve paths
relative to themselves, and are idempotent.

```
python3 build_research.py    # research.html from research_content.md
python3 build_slider.py      # the index.html slider from its SLIDES list
```

## Still open

- **proteoWizard slide** points at `research.html#methods-simple`. Change
  `SLIDES[5]['link']` to `proteowizard.html` once that page exists.
- **`proteowizard.html`** not built: outside the top nav, linked from the slider
  and the research page, pointing out to <http://www.proteowizard.org>.
- **Magic** not yet added as a top-level nav category.
- **Section figures** are interim; Michelle's diagrams can reuse the filenames.
- **`README.md` in the repo** still describes the draft workflow and is stale.
