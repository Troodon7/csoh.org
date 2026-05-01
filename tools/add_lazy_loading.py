#!/usr/bin/env python3
"""Add loading="lazy" to below-the-fold <img> tags across the site.

Rules:
  - The hero <img> at the top of the page (the banner) gets loading="eager"
    so Largest Contentful Paint isn't delayed for above-the-fold users.
  - Every other <img> gets loading="lazy" — browsers defer fetching until
    the image is near the viewport, cutting initial payload massively on
    card-heavy pages (resources.html: 199 imgs, chat-resources.html: 438).
  - Idempotent — already-set loading attributes are left alone.

Usage:
    python3 tools/add_lazy_loading.py            # all HTML files
    python3 tools/add_lazy_loading.py index.html # specific files
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Match every <img ...> tag (single line OR multi-line attribute split)
IMG_RE = re.compile(r'<img\b([^>]*)>', re.DOTALL | re.IGNORECASE)
# Inside an <img> tag, does it have a loading=... attribute?
LOADING_RE = re.compile(r'\bloading\s*=', re.IGNORECASE)
# Hero banner detection — these should stay eager so first paint is fast.
# Class name `hero-img` is consistent across all pillar/index/card pages.
HERO_RE = re.compile(r'class\s*=\s*["\'][^"\']*\bhero-img\b[^"\']*["\']', re.IGNORECASE)


def process_file(path: Path) -> tuple[int, int]:
    """Returns (lazy_added, eager_added)."""
    s = path.read_text(encoding="utf-8")
    original = s
    lazy_added = 0
    eager_added = 0

    def replace(m: re.Match) -> str:
        nonlocal lazy_added, eager_added
        attrs = m.group(1)
        if LOADING_RE.search(attrs):
            return m.group(0)  # already set, don't touch
        # Hero gets eager so LCP isn't delayed; everything else gets lazy.
        if HERO_RE.search(attrs):
            new_attr = ' loading="eager"'
            eager_added += 1
        else:
            new_attr = ' loading="lazy"'
            lazy_added += 1
        # Place the new attribute right before the closing >. Strip trailing
        # whitespace / "/" so output stays clean for both <img> and <img/>.
        attrs = attrs.rstrip()
        if attrs.endswith("/"):
            attrs = attrs[:-1].rstrip()
            return f"<img{attrs}{new_attr} />"
        return f"<img{attrs}{new_attr}>"

    s = IMG_RE.sub(replace, s)
    if s != original:
        path.write_text(s, encoding="utf-8")
    return lazy_added, eager_added


def main() -> int:
    if len(sys.argv) > 1:
        paths = [REPO_ROOT / p for p in sys.argv[1:]]
    else:
        paths = (
            list(REPO_ROOT.glob("*.html"))
            + list(REPO_ROOT.glob("breaches/*.html"))
            + list(REPO_ROOT.glob("meetings/*.html"))
        )

    total_lazy, total_eager, files_changed = 0, 0, 0
    for p in sorted(paths):
        if not p.exists():
            print(f"  - skip (missing): {p.relative_to(REPO_ROOT)}")
            continue
        if p.name == "google66d489593949bd4c.html":
            continue
        lazy, eager = process_file(p)
        if lazy or eager:
            files_changed += 1
            total_lazy += lazy
            total_eager += eager
            print(f"  ✓ {p.relative_to(REPO_ROOT)}: +{lazy} lazy, +{eager} eager")

    print(f"\nUpdated {files_changed} file(s). Total: +{total_lazy} lazy, +{total_eager} eager.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
