#!/usr/bin/env python3
"""One-shot script: insert Degree Programs entry across all HTML pages,
sitemap, and the index resource grid.

Pattern follows the 2026-05-03 careers + home-lab additions:
- Insert nav <li> entry into the Learn dropdown after Learning Path.
- Insert footer <li> entry into the Learn footer section after Learning Path.
- Insert sitemap <url> entry near other pillar pages.
- Insert resource card on index.html after the Careers card.

Idempotent: skips files where the entry already exists. Skips the new page itself.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEW_PAGE = "cloud-security-degree-programs.html"

# --- Pattern 1: Learn dropdown nav ----------------------------------------
# Anchor: "<li><a href=\"learning-path.html\">Learning Path</a></li>"
# Insert after, preserving the same indentation.
NAV_RE = re.compile(
    r'(\n([ \t]*)<li><a href="learning-path\.html"[^>]*>Learning Path</a></li>)'
)


def nav_replacement(match: re.Match) -> str:
    indent = match.group(2)
    return (
        match.group(1)
        + f'\n{indent}<li><a href="cloud-security-degree-programs.html">Degree Programs</a></li>'
    )


# --- Pattern 2: footer Learn section --------------------------------------
# Anchor: "<li><a href=\"/learning-path.html\">Learning Path</a></li>"
FOOTER_RE = re.compile(
    r'(\n([ \t]*)<li><a href="/learning-path\.html"[^>]*>Learning Path</a></li>)'
)


def footer_replacement(match: re.Match) -> str:
    indent = match.group(2)
    return (
        match.group(1)
        + f'\n{indent}<li><a href="/cloud-security-degree-programs.html">Degree Programs</a></li>'
    )


def patch_html(path: Path) -> bool:
    if path.name == NEW_PAGE:
        return False
    text = path.read_text(encoding="utf-8")
    original = text

    # Skip if already inserted
    if "cloud-security-degree-programs.html" in text:
        return False

    text = NAV_RE.sub(nav_replacement, text, count=1)
    text = FOOTER_RE.sub(footer_replacement, text, count=1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


# --- Pattern 3: sitemap.xml ------------------------------------------------
SITEMAP_PATH = ROOT / "sitemap.xml"
SITEMAP_ANCHOR = re.compile(
    r'(  <!-- Cloud Security Careers - Pillar page -->\n  <url>\n    <loc>https://csoh\.org/cloud-security-careers\.html</loc>\n    <lastmod>[\d-]+</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0\.8</priority>\n  </url>\n)'
)
SITEMAP_INSERT = """
  <!-- Cloud Security Degree Programs - Pillar page -->
  <url>
    <loc>https://csoh.org/cloud-security-degree-programs.html</loc>
    <lastmod>2026-05-03</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
"""


def patch_sitemap() -> bool:
    text = SITEMAP_PATH.read_text(encoding="utf-8")
    if "cloud-security-degree-programs.html" in text:
        return False
    new_text, count = SITEMAP_ANCHOR.subn(
        lambda m: m.group(1) + SITEMAP_INSERT, text, count=1
    )
    if count == 0:
        print("ERROR: sitemap anchor not found", file=sys.stderr)
        return False
    SITEMAP_PATH.write_text(new_text, encoding="utf-8")
    return True


# --- Pattern 4: index.html resource grid ----------------------------------
INDEX_PATH = ROOT / "index.html"
# Insert before the Careers card so Degree Programs appears earlier (academic
# step before careers in the funnel).
INDEX_ANCHOR = re.compile(
    r'(        <a href="cloud-security-careers\.html" class="card-link">)'
)
INDEX_CARD = """        <a href="cloud-security-degree-programs.html" class="card-link">
          <div class="resource-card" data-no-preview>
            <h3>🎓 Cloud Security Degree Programs</h3>
            <p>Academic paths for cloud security: which degrees map to the work and which universities have strong reputations.</p>
            <div class="resource-tags">
              <span class="tag">Education</span>
              <span class="tag">University</span>
            </div>
          </div>
        </a>
"""


def patch_index_card() -> bool:
    text = INDEX_PATH.read_text(encoding="utf-8")
    # Already inserted as a card?
    if 'href="cloud-security-degree-programs.html" class="card-link"' in text:
        return False
    new_text, count = INDEX_ANCHOR.subn(
        lambda m: INDEX_CARD + m.group(1), text, count=1
    )
    if count == 0:
        print("ERROR: index resource grid anchor not found", file=sys.stderr)
        return False
    INDEX_PATH.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    html_files = sorted(ROOT.glob("*.html"))
    patched = []
    for f in html_files:
        if patch_html(f):
            patched.append(f.name)

    print(f"Patched {len(patched)} HTML files (nav + footer):")
    for name in patched:
        print(f"  {name}")

    if patch_sitemap():
        print("Patched sitemap.xml")
    else:
        print("sitemap.xml: no change")

    if patch_index_card():
        print("Patched index.html resource grid")
    else:
        print("index.html: no card change")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
