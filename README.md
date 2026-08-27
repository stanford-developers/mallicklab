# research_new.html — drop-in files

Copy the contents of this folder into the root of the `mallicklab` repo,
preserving the directory structure. Nothing here overwrites an existing file.

```
research_new.html                        the page
images/figs/section1-ecology.jpg         }
images/figs/section3-coordination.jpg    } section figures (interim; Michelle's
images/figs/section4-interpretability.jpg} diagrams will replace these)
images/figs/section5-infrastructure.jpg  }
research_content.md                      source text for the page
build_research.py                        regenerates the page from that text
```

Sections 2 and 3 also use `images/figs/BiomarkerModeling.png` and
`images/figs/IntegratedOmics.png`, which are already in the repo.

## What is live and what is not

`research.html` is untouched and still serves the site. `research_new.html` is
a draft, reachable only by direct URL — nothing in the site navigation links to
it. It carries `<meta name="robots" content="noindex,nofollow">` so that it does
not appear in search results while it is being reviewed.

## Editing the text

Edit `research_content.md`, then from the repo root:

```
python3 build_research.py
```

The script rewrites only the article body of `research_new.html` and injects its
stylesheet and tab script. Site header, navigation, pager and footer are left
alone. It is idempotent, so running it repeatedly is safe.

Editing the HTML directly also works, but the next build will overwrite it.
Prefer the markdown.

## Going live

1. In `build_research.py`, change `PAGE` from `research_new.html` to
   `research.html`.
2. Run the script. The `noindex` directive removes itself automatically when the
   target is `research.html`.
3. Delete `research_new.html`.

## Notes

- **No external fonts.** The page uses Lato, which the site already loads.
- **Anchors.** Each section has an id — `#ecology`, `#biomarkers`, `#networks`,
  `#meaningful-ai`, `#methods` — so individual areas can be linked directly.
- **JavaScript.** The Simple/Technical summary tabs need it. Without it, both
  summaries render stacked and labelled, so nothing is hidden from a reader or a
  crawler that never runs the script.
- **Citations.** 36 links into `pdfs/`, all verified to resolve against the
  current repo.
