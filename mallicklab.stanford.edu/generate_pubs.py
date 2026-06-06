#!/usr/bin/env python3
"""
generate_pubs.py
----------------
Reads publications.json and pubs.html (template) and writes a new pubs.html
with the publications section fully pre-rendered — no runtime JS fetch needed.

Usage:
    python3 generate_pubs.py
    python3 generate_pubs.py --json publications.json --template pubs_template.html --out pubs.html

Run this whenever publications.json changes.
"""

import json, re, argparse, html, os, sys
from collections import defaultdict
from datetime import date

CURRENT_YEAR = date.today().year

# ── CLI ───────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument('--json',     default='publications.json')
parser.add_argument('--template', default='pubs_template.html')
parser.add_argument('--out',      default='pubs.html')
args = parser.parse_args()

for f, label in [(args.json, 'JSON'), (args.template, 'template')]:
    if not os.path.exists(f):
        print(f"Error: {label} file not found: {f}", file=sys.stderr)
        sys.exit(1)

# ── Load data ─────────────────────────────────────────────────────────────
with open(args.json, encoding='utf-8') as f:
    pubs = json.load(f)

with open(args.template, encoding='utf-8') as f:
    template = f.read()

# ── Helpers ───────────────────────────────────────────────────────────────
MAX_AUTHORS = 6

def esc(s):
    return html.escape(str(s)) if s else ''

def parse_authors(author_str):
    """Parse 'Lastname, Firstname, Lastname, Firstname, ...' into ['Firstname Lastname', ...]"""
    if not author_str:
        return []
    parts = [p.strip() for p in author_str.split(',') if p.strip()]
    authors = []
    i = 0
    while i < len(parts):
        if i + 1 < len(parts):
            authors.append(f"{parts[i+1]} {parts[i]}")
            i += 2
        else:
            authors.append(parts[i])
            i += 1
    return authors

def build_authors(author_str):
    if not author_str:
        return ''
    authors = parse_authors(author_str)
    if len(authors) <= MAX_AUTHORS:
        return f'<span class="pub-authors">{esc(", ".join(authors))}</span>'
    short = ', '.join(authors[:MAX_AUTHORS]) + ' … '
    full  = ', '.join(authors)
    uid   = f'au-{abs(hash(author_str)) % 1000000:06d}'
    return (
        f'<span class="pub-authors truncated" id="{uid}">'
        f'<span class="authors-short">{esc(short)}'
        f'<button class="toggle-authors" onclick="toggleAuthors(\'{uid}\')">'
        f'+ {len(authors) - MAX_AUTHORS} more</button></span>'
        f'<span class="authors-full">{esc(full)} '
        f'<button class="toggle-authors" onclick="toggleAuthors(\'{uid}\')">'
        f'Show fewer</button></span>'
        f'</span>'
    )

def build_details(p):
    parts = []
    if p.get('journal'): parts.append(f'<span class="pub-journal">{esc(p["journal"])}</span>')
    year = p.get('year') or (CURRENT_YEAR if p.get('status') == 'in_press' else None)
    if year:             parts.append(str(year))
    if p.get('volume'):  parts.append(esc(p['volume']))
    if p.get('pages'):   parts.append(esc(p['pages']))
    return '; '.join(parts)

def pub_html(p, is_featured_section=False):
    hl = p.get('highlight', '')
    status = p.get('status', '')

    if hl == 'featured':       hl_class = 'pub-featured'
    elif hl == 'highlighted':  hl_class = 'pub-highlighted'
    elif status == 'preprint': hl_class = 'pub-preprint'
    elif status == 'in_press': hl_class = 'pub-inpress'
    else:                      hl_class = 'pub-normal'

    # Title
    doi = p.get('doi') or ''
    title = esc(p.get('title', ''))
    title_inner = (f'<a href="https://doi.org/{esc(doi)}" target="_blank" rel="noopener">{title}</a>'
                   if doi else title)

    # Badges
    badges = []
    if not is_featured_section and hl == 'featured':
        badges.append('<span class="pub-badge pub-badge-featured">★ Selected</span>')
    if not is_featured_section and hl == 'highlighted':
        badges.append('<span class="pub-badge pub-badge-highlighted">◆</span>')
    if status == 'preprint':
        badges.append('<span class="pub-badge pub-badge-preprint">Preprint</span>')
    if status == 'in_press':
        badges.append('<span class="pub-badge pub-badge-inpress">In Press</span>')

    badges_html = (f'<span class="pub-badges-inline">{"".join(badges)}</span>'
                   if badges else '')

    # Links
    links = []
    if doi and status != 'preprint':
        links.append(f'<a class="pub-link" href="https://doi.org/{esc(doi)}" target="_blank" rel="noopener">DOI</a>')
    if p.get('pmid'):
        links.append(f'<a class="pub-link" href="https://pubmed.ncbi.nlm.nih.gov/{esc(p["pmid"])}/" target="_blank" rel="noopener">PubMed</a>')
    if p.get('biorxiv_doi') and status != 'preprint':
        links.append(f'<a class="pub-link" href="https://doi.org/{esc(p["biorxiv_doi"])}" target="_blank" rel="noopener">bioRxiv</a>')
    if status == 'preprint' and doi:
        links.append(f'<a class="pub-link" href="https://doi.org/{esc(doi)}" target="_blank" rel="noopener">bioRxiv</a>')
    if p.get('pdf'):
        links.append(f'<a class="pub-link pdf-link" href="{esc(p["pdf"])}" target="_blank" rel="noopener">PDF</a>')

    pid   = esc(p.get('id', ''))
    t_low = esc((p.get('title','') or '').lower())
    a_low = esc((p.get('authors','') or '').lower())
    j_low = esc((p.get('journal','') or '').lower())
    details = build_details(p)
    authors = build_authors(p.get('authors', ''))
    links_html = f'<div class="pub-links">{"".join(links)}</div>' if links else ''

    return (
        f'<li class="pub-entry {hl_class}" '
        f'data-id="{pid}" data-title="{t_low}" data-authors="{a_low}" data-journal="{j_low}">\n'
        f'  <span class="pub-title-text">{title_inner}{badges_html}</span>\n'
        f'  {authors}\n'
        f'  {"<span class=&quot;pub-details&quot;>" + details + "</span>" if details else ""}\n'
        f'  {links_html}\n'
        f'</li>'
    )

# ── Render featured section ───────────────────────────────────────────────
featured = [p for p in pubs if p.get('highlight') == 'featured']

if featured:
    items = '\n'.join(pub_html(p, is_featured_section=True) for p in featured)
    featured_html = (
        f'<div class="pubs-featured-section">\n'
        f'  <div class="pubs-section-title">★ Selected Publications '
        f'<span class="section-count">{len(featured)} papers</span></div>\n'
        f'  <ul style="padding:0;margin:0;list-style:none">\n{items}\n  </ul>\n</div>'
    )
else:
    featured_html = ''

# ── Render by-year section ────────────────────────────────────────────────
# in_press entries with no year default to the current year for grouping
def effective_year(p):
    return p.get('year') or (CURRENT_YEAR if p.get('status') == 'in_press' else None)

years = sorted({effective_year(p) for p in pubs if effective_year(p)}, reverse=True)
no_year = [p for p in pubs if not effective_year(p)]

year_blocks = [
    f'<div class="pubs-section-title">All Publications '
    f'<span class="section-count">{len(pubs)} papers</span></div>'
]

for yr in years:
    yr_pubs = [p for p in pubs if effective_year(p) == yr]
    items = '\n'.join(pub_html(p) for p in yr_pubs)
    year_blocks.append(
        f'<div class="year-group" data-year="{yr}">\n'
        f'  <div class="year-header" onclick="toggleYear(\'yr-{yr}\')">\n'
        f'    <span class="year-toggle">▼</span>\n'
        f'    <span class="year-label">{yr}</span>\n'
        f'    <span class="year-count">{len(yr_pubs)} paper{"s" if len(yr_pubs)!=1 else ""}</span>\n'
        f'  </div>\n'
        f'  <ul class="year-body" id="yr-{yr}" style="padding:0;margin:0;list-style:none">\n'
        f'{items}\n'
        f'  </ul>\n'
        f'</div>'
    )

if no_year:
    items = '\n'.join(pub_html(p) for p in no_year)
    year_blocks.append(
        f'<div class="year-group" data-year="none">\n'
        f'  <div class="year-header" onclick="toggleYear(\'yr-none\')">\n'
        f'    <span class="year-toggle">▼</span>\n'
        f'    <span class="year-label">No date</span>\n'
        f'    <span class="year-count">{len(no_year)} paper{"s" if len(no_year)!=1 else ""}</span>\n'
        f'  </div>\n'
        f'  <ul class="year-body" id="yr-none" style="padding:0;margin:0;list-style:none">\n'
        f'{items}\n'
        f'  </ul>\n'
        f'</div>'
    )

by_year_html = '\n'.join(year_blocks)

# ── Minimal JS (no fetch — just UI interactions) ──────────────────────────
minimal_js = """\
<script>
/* Publications page — pre-rendered, no fetch needed */
(function() {
  window.toggleYear = function(id) {
    var body   = document.getElementById(id);
    var header = body ? body.previousElementSibling : null;
    if (!body) return;
    body.classList.toggle('hidden');
    if (header) header.classList.toggle('collapsed');
  };
  window.pubsExpandAll = function() {
    document.querySelectorAll('.year-body').forEach(function(el) { el.classList.remove('hidden'); });
    document.querySelectorAll('.year-header').forEach(function(el) { el.classList.remove('collapsed'); });
  };
  window.pubsCollapseAll = function() {
    document.querySelectorAll('.year-body').forEach(function(el) { el.classList.add('hidden'); });
    document.querySelectorAll('.year-header').forEach(function(el) { el.classList.add('collapsed'); });
  };
  window.toggleAuthors = function(id) {
    var el = document.getElementById(id);
    if (el) el.classList.toggle('expanded');
  };
  window.pubsFilter = function() {
    var q = document.getElementById('pubSearch').value.toLowerCase().trim();
    document.querySelectorAll('.pub-entry').forEach(function(el) {
      var match = !q || el.dataset.title.includes(q) ||
                  el.dataset.authors.includes(q) || el.dataset.journal.includes(q);
      el.style.display = match ? '' : 'none';
    });
    document.querySelectorAll('.year-group').forEach(function(grp) {
      var vis = grp.querySelectorAll('.pub-entry:not([style*="display: none"])').length;
      grp.style.display = vis ? '' : 'none';
      if (q) {
        var b = grp.querySelector('.year-body');
        var h = grp.querySelector('.year-header');
        if (b) b.classList.remove('hidden');
        if (h) h.classList.remove('collapsed');
      }
    });
  };
})();
</script>"""

# ── Build the new pubs-root block ─────────────────────────────────────────
new_pubs_root = (
    f'<div id="pubs-root">\n'
    f'  <div class="pubs-controls">\n'
    f'    <input type="text" id="pubSearch" placeholder="Search publications…" oninput="pubsFilter()">\n'
    f'    <button onclick="pubsExpandAll()">Expand all years</button>\n'
    f'    <button onclick="pubsCollapseAll()">Collapse all years</button>\n'
    f'  </div>\n'
    f'  <div id="pubs-featured">\n{featured_html}\n  </div>\n'
    f'  <div id="pubs-by-year">\n{by_year_html}\n  </div>\n'
    f'</div>\n'
    f'\n{minimal_js}'
)

# ── Splice into template ──────────────────────────────────────────────────
# Replace everything from <div id="pubs-root"> through the closing </script>
# of the old dynamic renderer
old_start = template.find('<div id="pubs-root">')
old_end   = template.find('})();\n</script>') + len('})();\n</script>')

if old_start == -1 or old_end == -1:
    print("Error: could not find dynamic region in template", file=sys.stderr)
    sys.exit(1)

output = template[:old_start] + new_pubs_root + template[old_end:]

with open(args.out, 'w', encoding='utf-8') as f:
    f.write(output)

# ── Summary ───────────────────────────────────────────────────────────────
print(f"Generated {args.out}")
print(f"  {len(pubs)} publications | {len(featured)} featured | {len(years)} year groups")
print(f"  Output size: {len(output):,} chars")
