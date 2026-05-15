#!/usr/bin/env python3
"""Regenerate the canonical site navigation across every HTML page.

Replaces every <nav>...</nav> menu block (NOT breadcrumb-nav, which has a
class attribute) with the structure defined in DROPDOWNS below. Sets
aria-current="page" on the matching link and `active` on its dropdown
toggle. Handles `../` path prefixing for files in breaches/ and meetings/.

Run from repo root: python3 tools/sync_navs.py
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Order here is the order shown in the header.
DROPDOWNS = [
    ('Learn', [
        ('what-is-cloud-security.html', 'What is Cloud Security?'),
        ('learning-path.html', 'Learning Path'),
        ('ai-learning.html', 'AI Learning'),
        ('cloud-security-degree-programs.html', 'Degree Programs'),
        ('cloud-security-careers.html', 'Careers'),
        ('cloud-security-home-lab.html', 'Home Lab'),
        ('cloud-security-portfolio-projects.html', 'Portfolio Projects'),
        ('cloud-security-certifications.html', 'Certifications'),
        ('resources.html', 'Resources'),
    ]),
    ('Topics', [
        ('cloud-security-best-practices.html', 'Best Practices'),
        ('shared-responsibility-model.html', 'Shared Responsibility'),
        ('cspm-vs-cnapp.html', 'CSPM vs CNAPP'),
        ('landing-zones.html', 'Landing Zones'),
        ('containers.html', 'Containers'),
        ('kubernetes.html', 'Kubernetes'),
        ('ci-cd.html', 'CI/CD'),
        ('cloud-security-reading-list.html', 'Reading List'),
    ]),
    ('Threat Research', [
        ('threat-research.html', 'Threat Research'),
        ('breach-timeline.html', 'Breach Kill Chains'),
        ('ctfs.html', 'CTFs'),
    ]),
    ('Attend', [
        ('sessions.html', 'Zoom Sessions'),
        ('community.html', 'Community &amp; Signal'),
        ('conferences.html', 'Conferences'),
        ('meetings.html', 'Meeting Recaps'),
        ('presentations.html', 'Presentations'),
        ('chat-resources.html', 'Chat Resources'),
    ]),
    ('Contribute', [
        ('contribute.html', 'Contribute Overview'),
        ('contribute-resources.html', 'Add a Resource'),
    ]),
    ('About', [
        ('glossary.html', 'Glossary'),
        ('faq.html', 'FAQ'),
        ('github-actions.html', 'How We Use GitHub Actions'),
        ('cloud-deployment.html', 'How We Deploy to GCP'),
    ]),
]

# slug -> (dropdown_index, item_index)
SLUG_LOOKUP: dict[str, tuple[int, int]] = {}
for di, (_dname, items) in enumerate(DROPDOWNS):
    for ii, (slug, _label) in enumerate(items):
        SLUG_LOOKUP[slug] = (di, ii)

# Match the menu nav (open `<nav>` with no class attr) — breadcrumb-nav uses
# `<nav class="breadcrumb-nav">` so it won't match. Also consumes the
# leading indentation so the replacement controls the indent fully.
NAV_PATTERN = re.compile(
    r'(?m)^[ \t]*<nav>\s*<ul>[\s\S]*?</ul>\s*</nav>',
)


def determine_active(path: Path) -> tuple[int, int] | None:
    """Return (dropdown_idx, item_idx) for the page's nav highlight, or None."""
    name = path.name
    parent = path.parent.name
    if parent == 'breaches':
        return SLUG_LOOKUP['breach-timeline.html']
    if parent == 'meetings':
        return SLUG_LOOKUP['meetings.html']
    return SLUG_LOOKUP.get(name)


def build_nav(path: Path) -> str:
    name = path.name
    parent = path.parent.name
    prefix = '../' if parent in ('breaches', 'meetings') else ''

    active = determine_active(path)
    home_active = parent != 'breaches' and parent != 'meetings' and name == 'index.html'
    news_active = parent not in ('breaches', 'meetings') and name == 'news.html'

    out: list[str] = []
    out.append('            <nav>')
    out.append('                <ul>')

    home_attr = ' aria-current="page"' if home_active else ''
    out.append(f'                    <li><a href="{prefix}index.html"{home_attr}>Home</a></li>')

    news_attr = ' aria-current="page"' if news_active else ''
    out.append(f'                    <li><a href="{prefix}news.html"{news_attr}>News</a></li>')

    for di, (dname, items) in enumerate(DROPDOWNS):
        is_active = active is not None and active[0] == di
        toggle_class = 'dropdown-toggle active' if is_active else 'dropdown-toggle'
        expanded = 'true' if is_active else 'false'
        out.append('                    <li class="has-dropdown">')
        out.append(
            f'                      <button class="{toggle_class}" '
            f'aria-expanded="{expanded}" aria-haspopup="true">{dname} '
            f'<span class="caret" aria-hidden="true">▾</span></button>'
        )
        out.append('                      <ul class="dropdown-menu">')
        for ii, (slug, label) in enumerate(items):
            cur = ' aria-current="page"' if active == (di, ii) else ''
            out.append(f'                        <li><a href="{prefix}{slug}"{cur}>{label}</a></li>')
        out.append('                      </ul>')
        out.append('                    </li>')

    out.append('                </ul>')
    out.append('            </nav>')
    return '\n'.join(out)


def process(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if '<nav>' not in text:
        return False
    replacement = build_nav(path)
    new_text, n = NAV_PATTERN.subn(replacement, text, count=1)
    if n == 0 or new_text == text:
        return False
    path.write_text(new_text, encoding='utf-8')
    return True


def main() -> None:
    paths: list[Path] = []
    paths.extend(REPO.glob('*.html'))
    paths.extend((REPO / 'breaches').glob('*.html'))
    paths.extend((REPO / 'meetings').glob('*.html'))

    updated = 0
    skipped = 0
    for p in sorted(paths):
        if process(p):
            updated += 1
        else:
            skipped += 1
    print(f'updated={updated} skipped={skipped}')


if __name__ == '__main__':
    main()
