#!/usr/bin/env python3
"""Generate research.html from research_content.md, preserving the site chrome.

Reads the approved markdown so the page text cannot drift from the signed-off
content. Replaces only the articleBody region of the existing page and injects
a stylesheet into <head>; header, nav, pager and footer are untouched.
"""
import os, re, html, sys

# Paths resolve relative to this script, which lives at the repo root
# alongside generate_pubs.py and generate_peeps.py.
REPO = os.path.dirname(os.path.abspath(__file__))
MD   = os.path.join(REPO, 'research_content.md')
PAGE = os.path.join(REPO, 'research.html')
SEED = PAGE

# ---------------------------------------------------------------- parse md
md = open(MD, encoding='utf-8').read()

def inline(t):
    """Markdown inline -> HTML. Escapes first, so content can't inject markup."""
    t = html.escape(t, quote=False)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
               lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', t)
    t = t.replace('`', '')
    return t

def paras(block):
    out = []
    block = re.sub(r'(?m)^\s*-{3,}\s*$', '', block)   # drop markdown <hr> separators
    for p in re.split(r'\n\s*\n', block.strip()):
        p = ' '.join(l.strip() for l in p.strip().split('\n'))
        if p:
            out.append('<p>' + inline(p) + '</p>')
    return '\n\t\t\t\t'.join(out)

# overview = text between "## Overview" and the first "## 1."
ov = md[md.index('## Overview') + len('## Overview'): md.index('\n## 1.')]
overview_html = paras(ov)

SECTIONS = []
for n in range(1, 6):
    start = md.index(f'\n## {n}. ')
    nxt = md.find('\n## ', start + 5)
    block = md[start: nxt if nxt != -1 else len(md)]

    title = re.search(r'^## \d\.\s*(.+)$', block, re.M).group(1).strip()
    question = re.search(r'^\*(.+?)\*$', block, re.M).group(1).strip()
    blurb = re.search(r'^\*\*Blurb:\*\*\s*(.+)$', block, re.M).group(1).strip()

    lay = block[block.index('### Lay summary') + len('### Lay summary'):
                block.index('### Technical summary')]
    tech = block[block.index('### Technical summary') + len('### Technical summary'):
                 block.index('### Graphic suggestion')]

    SECTIONS.append(dict(n=n, title=title, question=question, blurb=blurb,
                         lay=paras(lay), tech=paras(tech)))

# ------------------------------------------------------- per-section assets
ASSETS = {
 1: dict(slug='ecology',    nav='Tumor Ecology',
         thumb='images/figs/section1-ecology.jpg',        band='images/figs/section1-ecology.jpg',
         talt='Aerial view of a river meander through mottled green and rust vegetation',
         balt='Aerial view of a river meander through mottled green and rust vegetation',
         tpos='55% 40%', bpos='55% 42%'),
 2: dict(slug='biomarkers', nav='Biomarkers',
         thumb='images/figs/BiomarkerModeling.png',       band='images/figs/BiomarkerModeling.png',
         talt='Diagram of protein transit from tumour cell through the interstitium into circulation',
         balt='Diagram of protein transit from tumour cell through the interstitium into circulation',
         tpos='50% 45%', bpos='50% 50%'),
 3: dict(slug='networks',   nav='Systems Biology',
         thumb='images/figs/section3-coordination.jpg',   band='images/figs/IntegratedOmics.png',
         talt="A conductor's hands above an open orchestral score, instrument staves labelled",
         balt='Genome, transcriptome, proteome, phosphoproteome and interactome shown as successive layers',
         tpos='62% 50%', bpos='50% 50%'),
 4: dict(slug='meaningful-ai', nav='Meaningful AI',
         thumb='images/figs/section4-interpretability.jpg', band='images/figs/section4-interpretability.jpg',
         talt='An antique telescope, compass and magnifier resting on a period map',
         balt='An antique telescope, compass and magnifier resting on a period map',
         tpos='50% 50%', bpos='50% 52%'),
 5: dict(slug='methods',    nav='Methods & Tools',
         thumb='images/figs/section5-infrastructure.jpg', band='images/figs/section5-infrastructure.jpg',
         talt='A worn wooden toolbox holding hand tools and rolled drawings',
         balt='A worn wooden toolbox holding hand tools and rolled drawings',
         tpos='50% 55%', bpos='50% 58%'),
}
# band images that are diagrams, not photographs: contain, don't crop
DIAGRAM_BANDS = {2, 3}

# ------------------------------------------------------------------- styles
STYLE = """
	<style type="text/css">
	/* ============================================================
	   Mallick Lab / research
	   Typography follows the site: Lato throughout, no imported face.
	   Each area keeps a fixed thumbnail, question and blurb; the two
	   readings open as tabs into a framed panel inside the text column,
	   so the left edge of the text never moves.
	   ============================================================ */
	#jm-maincontent .item-page{
		--ink:#2A2A2A; --ink-2:#4A4A4A; --ink-3:#7B7469;
		--rule:#E2DDD3; --wash:#FAF8F4;
		--blue:#00AEEF;      /* the site's own link colour, used for anything clickable */
		--ink-q:#6A6A6A;     /* guiding questions: neutral, so blue alone means "clickable" */
		--sans:'Lato',-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;
		color:var(--ink); font-family:var(--sans);
	}
	/* page title: inherit the site's own h2 treatment, don't restyle it */
	#jm-maincontent .item-page .page-header{border:0;margin:0 0 4px;padding:0}

	/* ---- overview ------------------------------------------------ */
	.rp-overview{margin:0 0 4px}
	.rp-overview p{
		font-family:var(--sans); font-size:1.0rem; line-height:1.68;
		color:var(--ink-2); margin:0 0 .95em;
	}
	.rp-overview p:first-child{font-size:1.09rem; line-height:1.62; color:var(--ink)}

	/* ---- area ----------------------------------------------------- */
	.rp-area{padding:0 0 34px; margin:26px 0 34px; border-bottom:1px solid var(--rule); scroll-margin-top:18px}
	.rp-area:last-of-type{border-bottom:0; margin-bottom:0}

	.rp-head{display:flex; gap:26px; align-items:flex-start}
	.rp-thumb{flex:0 0 200px; aspect-ratio:4/3; margin:4px 0 0; overflow:hidden; background:var(--wash)}
	.rp-thumb img{width:100%; height:100%; object-fit:cover; display:block}
	.rp-thumb.is-diagram{background:#fff; border:1px solid var(--rule); display:flex; align-items:center}
	.rp-thumb.is-diagram img{object-fit:contain; height:auto; padding:7px}
	/* the text column: its left edge is the page's vertical spine */
	.rp-col{flex:1; min-width:0}

	.rp-area h3{
		font-family:var(--sans); font-weight:700; font-size:1.34rem; line-height:1.25;
		color:var(--ink); margin:0 0 7px; letter-spacing:-.005em;
	}
	.rp-q{
		font-style:italic; font-size:1.0rem; line-height:1.5;
		color:var(--ink-q); margin:0 0 11px;
	}
	.rp-blurb{font-size:.985rem; line-height:1.66; color:var(--ink-2); margin:0}

	/* ---- tabs ------------------------------------------------------ */
	.rp-tabs{display:flex; align-items:baseline; flex-wrap:wrap; gap:18px; margin:14px 0 0}
	.rp-lead{font-size:.95rem; color:var(--ink-3); margin-right:-7px}
	/* These are controls, but the site's only clickable idiom is a blue link,
	   so they are styled as links: same colour, same size, underlined. The
	   template sets `button { background-color:#00aeef }` plus a brighter
	   :hover fill, so the fill is forced off in every state, not just at rest. */
	.rp-tab{
		appearance:none; -webkit-appearance:none; cursor:pointer; user-select:none;
		font-family:var(--sans); font-size:.95rem; font-weight:400; line-height:1.4;
		color:var(--blue); background:none !important; border:0; box-shadow:none;
		padding:0; margin:0; border-bottom:1px solid rgba(0,174,239,.45);
		transition:color .12s, border-color .12s;
	}
	.rp-tab:hover,.rp-tab:focus{background:none !important}
	.rp-tab:hover{border-bottom-color:var(--blue)}
	/* chevron points right when closed, turns down when the panel is open */
	.rp-tab::after{content:" ›"; margin-left:4px}
	.rp-tab[aria-selected="true"]{font-weight:700}
	.rp-tab[aria-selected="true"]::after{content:" ˅"; margin-left:4px}
	.rp-panelwrap{display:none}
	.rp-panelwrap.is-open{display:block; margin-top:11px}
	.rp-panel{
		border:1px solid var(--rule); background:var(--wash);
		border-radius:3px; padding:22px 26px;
	}
	.rp-panel[hidden]{display:none}
	.rp-panel p{font-size:.95rem; line-height:1.72; color:var(--ink-2); margin:0 0 1.05em}
	.rp-panel p:last-child{margin-bottom:0}
	.rp-panel a{color:var(--blue); text-decoration:none; border-bottom:1px solid rgba(0,174,239,.38)}
	.rp-panel a:hover,.rp-panel a:focus{border-bottom-color:var(--blue); background:rgba(0,174,239,.07)}
	.rp-panel.rp-lay p{font-size:1.0rem; line-height:1.74}

	@media (prefers-reduced-motion:no-preference){
		.rp-panelwrap.is-open .rp-panel{animation:rp-in .16s ease-out}
		@keyframes rp-in{from{opacity:0}to{opacity:1}}
	}

	/* no-JS: show both readings, labelled, rather than hiding them */
	.rp-area:not(.rp-ready) .rp-tabs{display:none}
	.rp-area:not(.rp-ready) .rp-panelwrap{display:block}
	.rp-area:not(.rp-ready) .rp-panelwrap{margin-top:14px}
	.rp-area:not(.rp-ready) .rp-panel[hidden]{display:block}

	:where(.rp-tab,.rp-panel a):focus-visible{outline:2px solid var(--blue); outline-offset:2px}

	/* ---- coda ------------------------------------------------------ */
	.rp-coda{
		margin:46px 0 6px; padding:26px 0 0; border-top:1px solid var(--rule);
		text-align:center;
	}
	.rp-coda blockquote{
		margin:0; padding:0; border:0; background:none;
		font-size:1.12rem; font-style:italic; line-height:1.55; color:var(--ink-2);
	}
	.rp-coda blockquote p{margin:0 0 9px; font-size:inherit; font-style:inherit; line-height:inherit}
	.rp-coda cite{
		display:block; font-style:normal; font-size:.72rem; font-weight:700;
		letter-spacing:.13em; text-transform:uppercase; color:var(--ink-3);
	}

	/* ---- responsive ------------------------------------------------ */
	@media (max-width:820px){
		.rp-head{gap:18px}
		.rp-thumb{flex-basis:150px}
		.rp-area h3{font-size:1.22rem}
		.rp-panel{padding:18px 20px}
	}
	@media (max-width:600px){
		.rp-head{display:block}
		.rp-thumb{width:100%; flex-basis:auto; aspect-ratio:5/2; margin:0 0 14px}
		.rp-tabs{gap:14px}
		.rp-tab{font-size:.92rem}
		.rp-lead{font-size:.92rem; flex:0 0 100%; margin:0 0 -6px}
		.rp-panel{padding:16px 15px}
		.rp-coda blockquote{font-size:1.02rem}
	}
	@media (prefers-reduced-motion:reduce){*{transition:none !important; animation:none !important}}
	@media print{
		.rp-tabs{display:none}
		.rp-panelwrap{display:block !important}
		.rp-panel{border:0; background:none; padding:0}
		.rp-panel[hidden]{display:block !important}
	}
	</style>
"""

SCRIPT = """
	<script type="text/javascript">
	/* Research area tabs. Progressive enhancement: without this script both
	   readings render stacked and labelled, so nothing is hidden from a
	   reader (or a crawler) that never runs it. */
	(function () {
		var areas = document.querySelectorAll('.rp-area');
		Array.prototype.forEach.call(areas, function (area) {
			var tabs   = area.querySelectorAll('.rp-tab');
			var wrap   = area.querySelector('.rp-panelwrap');
			if (!tabs.length || !wrap) { return; }
			var panels = {};
			Array.prototype.forEach.call(tabs, function (t) {
				panels[t.id] = document.getElementById(t.getAttribute('aria-controls'));
			});

			function show(tab) {
				var closing = tab && tab.getAttribute('aria-selected') === 'true';
				Array.prototype.forEach.call(tabs, function (t) {
					var on = !closing && t === tab;
					t.setAttribute('aria-selected', on ? 'true' : 'false');
					t.setAttribute('tabindex', on ? '0' : '-1');
					if (panels[t.id]) { panels[t.id].hidden = !on; }
				});
				wrap.classList.toggle('is-open', !closing);
				if (closing) { tabs[0].setAttribute('tabindex', '0'); }
			}

			Array.prototype.forEach.call(tabs, function (tab, i) {
				tab.setAttribute('tabindex', i === 0 ? '0' : '-1');
				if (panels[tab.id]) { panels[tab.id].hidden = true; }
				tab.addEventListener('click', function () { show(tab); });
				tab.addEventListener('keydown', function (e) {
					var k = e.key, n = null;
					if (k === 'ArrowRight' || k === 'ArrowDown') { n = tabs[(i + 1) % tabs.length]; }
					else if (k === 'ArrowLeft' || k === 'ArrowUp') { n = tabs[(i - 1 + tabs.length) % tabs.length]; }
					else if (k === 'Home') { n = tabs[0]; }
					else if (k === 'End') { n = tabs[tabs.length - 1]; }
					if (n) { e.preventDefault(); n.focus(); }
				});
			});
			wrap.classList.remove('is-open');
			area.classList.add('rp-ready');
			area._rpShow = show;
		});

		/* Deep links. #ecology jumps to the section; #ecology-simple and
		   #ecology-technical also open that summary. Both the initial load and
		   later hash changes are handled. */
		function openFromHash() {
			var id = (location.hash || '').replace(/^#/, '');
			if (!id) { return; }
			var tab = document.getElementById(id);
			if (!tab || !tab.classList.contains('rp-tab')) { return; }
			var area = tab.closest('.rp-area');
			if (!area || !area._rpShow) { return; }
			if (tab.getAttribute('aria-selected') !== 'true') { area._rpShow(tab); }
			area.scrollIntoView();
		}
		openFromHash();
		/* Re-run once images have loaded: they can shift the layout after the
		   first scroll, leaving the target section off-screen. */
		window.addEventListener('load', openFromHash);
		window.addEventListener('hashchange', openFromHash);
	})();
	</script>
"""

# -------------------------------------------------------------- build body
def esc(s):
    return html.escape(s, quote=True)

parts = ['\t\t\t\t\t\t\t\t<div itemprop="articleBody">',
         '\t<div class="rp-overview">',
         '\t\t' + overview_html.replace('\n\t\t\t\t', '\n\t\t'),
         '\t</div>',
         '']

for s in SECTIONS:
    a = ASSETS[s['n']]
    thumb_cls = ' is-diagram' if a['thumb'].endswith('.png') else ''
    thumb_pos = '' if thumb_cls else f' style="object-position:{a["tpos"]}"'
    sid = a['slug']
    parts += [
f'\t<section class="rp-area" id="{sid}">',
 '\t\t<div class="rp-head">',
f'\t\t\t<figure class="rp-thumb{thumb_cls}">',
f'\t\t\t\t<img src="{a["thumb"]}" alt="{esc(a["talt"])}" loading="lazy"{thumb_pos} />',
 '\t\t\t</figure>',
 '\t\t\t<div class="rp-col">',
f'\t\t\t\t<h3>{esc(s["title"])}</h3>',
f'\t\t\t\t<p class="rp-q">{inline(s["question"])}</p>',
f'\t\t\t\t<p class="rp-blurb">{inline(s["blurb"])}</p>',
f'\t\t\t\t<div class="rp-tabs" role="tablist" aria-label="Readings of {esc(s["title"])}">',
 '\t\t\t\t\t<span class="rp-lead" aria-hidden="true">Learn more:</span>',
f'\t\t\t\t\t<button type="button" class="rp-tab" role="tab" id="{sid}-simple"'
f' aria-controls="{sid}-p-simple" aria-selected="false">Simple summary</button>',
f'\t\t\t\t\t<button type="button" class="rp-tab" role="tab" id="{sid}-technical"'
f' aria-controls="{sid}-p-technical" aria-selected="false">Technical summary</button>',
 '\t\t\t\t</div>',
 '\t\t\t\t<div class="rp-panelwrap">',
f'\t\t\t\t\t<div class="rp-panel rp-lay" role="tabpanel" id="{sid}-p-simple" aria-labelledby="{sid}-simple">',
 '\t\t\t\t\t' + s['lay'],
 '\t\t\t\t\t</div>',
f'\t\t\t\t\t<div class="rp-panel rp-tech" role="tabpanel" id="{sid}-p-technical" aria-labelledby="{sid}-technical">',
 '\t\t\t\t\t' + s['tech'],
 '\t\t\t\t\t</div>',
 '\t\t\t\t</div>',
 '\t\t\t</div>',
 '\t\t</div>',
 '\t</section>', '']

# coda: the Pauling quote, kept off the top of the page and used to close it
parts += [
 '\t<div class="rp-coda">',
 '\t\t<blockquote>',
 '\t\t\t<p>&ldquo;Life is a relationship among molecules and not a property of any molecule.&rdquo;</p>',
 '\t\t\t<cite>Linus Pauling</cite>',
 '\t\t</blockquote>',
 '\t</div>', '']

parts.append('\t</div>')
body = '\n'.join(parts)

# ------------------------------------------------------------ splice page
page = open(PAGE if os.path.exists(PAGE) else SEED, encoding='utf-8').read()

# Anchors are matched whitespace-tolerantly: earlier cleanup passes can change
# the surrounding indentation.
m_start = re.search(r'[ \t]*<div itemprop="articleBody">', page)
m_end   = re.search(r'[ \t]*<ul class="pager pagenav">', page)
if not (m_start and m_end):
    raise SystemExit('could not locate articleBody / pager anchors')
start, end = m_start.start(), m_end.start()
page  = page[:start] + body + '\n\n\t\n' + page[end:]

# While this builds a draft page that is nonetheless publicly served, keep it
# out of search results. The directive disappears automatically once PAGE is
# switched to the live research.html.
DRAFT_META = ('\t<meta name="robots" content="noindex,nofollow" />\n'
              if os.path.basename(PAGE) != 'research.html' else '')
page = page.replace('\t<meta name="robots" content="noindex,nofollow" />\n', '')

anchor = '\t</head>\t<body>'
assert anchor in page
# idempotent: drop any stylesheet this script injected on a previous run
page = re.sub(r'\n\t<style type="text/css">\n\t/\* =+\n\t   Mallick Lab / research.*?\n\t</style>\n',
              '', page, flags=re.S)   # STYLE supplies its own leading newline
page = page.replace(anchor, DRAFT_META + STYLE + anchor, 1)

# tab behaviour, injected at end of body so markup exists when it runs
page = re.sub(r'\n\t<script type="text/javascript">\n\t/\* Research area tabs\..*?\n\t</script>\n',
              '', page, flags=re.S)
assert '</body>' in page
page = page.replace('</body>', SCRIPT + '</body>', 1)

open(PAGE, 'w', encoding='utf-8').write(page)
print(f'wrote {PAGE}  ({len(page):,} chars)')
