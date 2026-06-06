#!/usr/bin/env python3
"""
generate_peeps.py
-----------------
Reads people.json and peeps_template.html and writes a fully pre-rendered peeps.html.

Usage:
    python3 generate_peeps.py
    python3 generate_peeps.py --json people.json --template peeps_template.html --out peeps.html

Run this whenever people.json changes.
"""

import json, html, argparse, os, sys

parser = argparse.ArgumentParser()
parser.add_argument('--json',     default='people.json')
parser.add_argument('--template', default='peeps_template.html')
parser.add_argument('--out',      default='peeps.html')
args = parser.parse_args()

for f, label in [(args.json, 'JSON'), (args.template, 'template')]:
    if not os.path.exists(f):
        print(f"Error: {label} file not found: {f}", file=sys.stderr)
        sys.exit(1)

with open(args.json, encoding='utf-8') as f:
    data = json.load(f)

with open(args.template, encoding='utf-8') as f:
    template = f.read()

def esc(s):
    return html.escape(str(s)) if s else ''

# ── PI section ────────────────────────────────────────────────────────────
pi = data.get('pi', {})
bio_link = (f' [<a href="{esc(pi["bioLink"])}">Bio and Headshot</a>]'
            if pi.get('bioLink') else '')
pi_html = f"""
    <h2 class="peeps-section-title">Me</h2>
    <hr class="peeps-rule">
    <div class="pi-section">
      <img class="pi-img" src="{esc(pi.get('img',''))}" alt="{esc(pi.get('name',''))}" width="250">
      <div class="pi-bio">
        <p><strong>{esc(pi.get('name',''))}</strong></p>
        <p>{esc(pi.get('bio',''))}{bio_link}</p>
      </div>
    </div>"""

# ── Current members ───────────────────────────────────────────────────────
current = data.get('current', [])
if current:
    rows = ''
    for m in current:
        role_html = (f', <span class="member-role">{esc(m["role"])}</span>'
                     if m.get('role') else '')
        bio_html = f'<p>{esc(m["bio"])}</p>' if m.get('bio') else ''
        rows += f"""
        <tr>
          <td><img class="member-img" src="{esc(m.get('img',''))}" alt="{esc(m.get('name',''))}" width="150"></td>
          <td>
            <p><span class="member-name">{esc(m.get('name',''))}</span>{role_html}</p>
            {bio_html}
          </td>
        </tr>"""
    current_html = f'<table class="members-table"><tbody>{rows}\n</tbody></table>'
else:
    current_html = '<p class="peeps-empty">No current members listed.</p>'

# ── Alumni grid ───────────────────────────────────────────────────────────
alumni = data.get('alumni', [])
if alumni:
    cards = ''
    for a in alumni:
        pos_html = (f'<div class="alumni-pos">{esc(a["position"])}</div>'
                    if a.get('position') else '')
        cards += f"""
        <div class="alumni-card">
          <img src="{esc(a.get('img',''))}" alt="{esc(a.get('name',''))}" width="175" height="220">
          <div class="alumni-desc">
            <div class="alumni-name">{esc(a.get('name',''))}</div>
            {pos_html}
          </div>
        </div>"""
    alumni_html = f'<div class="alumni-grid">{cards}\n</div>'
else:
    alumni_html = '<p class="peeps-empty">No alumni listed yet.</p>'

# ── Interns ───────────────────────────────────────────────────────────────
interns = data.get('interns', [])
if interns:
    items = ''
    for i in interns:
        detail_html = (f'<span class="intern-detail"> — {esc(i["detail"])}</span>'
                       if i.get('detail') else '')
        items += f"""
        <div class="intern-item">
          <span class="intern-name">{esc(i.get('name',''))}</span>{detail_html}
        </div>"""
    interns_html = f'<div class="interns-list">{items}\n</div>'
else:
    interns_html = ('<p class="peeps-empty">No interns listed yet — '
                    'add entries to the <code>interns</code> array in people.json.</p>')

# ── Assemble peeps-root ───────────────────────────────────────────────────
new_root = f"""<div id="peeps-root">
{pi_html}

  <h2 class="peeps-section-title">Current Stanford Peeps</h2>
  <hr class="peeps-rule">
  {current_html}

  <hr class="peeps-rule">
  <h2 class="peeps-section-title">Alumn Types and CAMM Folks</h2>
  <hr class="peeps-rule">
  {alumni_html}

  <hr class="peeps-rule">
  <h2 class="peeps-section-title">Past Interns</h2>
  <hr class="peeps-rule">
  {interns_html}
</div>"""

# ── Splice into template ──────────────────────────────────────────────────
old_root_start = template.find('<div id="peeps-root">')
old_script_end = template.find('</script>', template.find("fetch('people.json')")) + len('</script>')

if old_root_start == -1 or old_script_end == -1:
    print("Error: could not find dynamic region in template", file=sys.stderr)
    sys.exit(1)

output = template[:old_root_start] + new_root + template[old_script_end:]

with open(args.out, 'w', encoding='utf-8') as f:
    f.write(output)

print(f"Generated {args.out}")
print(f"  PI: {pi.get('name','?')} | Current: {len(current)} | Alumni: {len(alumni)} | Interns: {len(interns)}")
print(f"  Output size: {len(output):,} chars")
