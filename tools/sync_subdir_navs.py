#!/usr/bin/env python3
"""Bring subdir nav/footer in breaches/ and meetings/ up to date with current top-level pages.

Inserts the missing entries:
  Learn dropdown nav (after Learning Path):
    - Degree Programs
    - Careers
    - Home Lab
    - Portfolio Projects
    - Reading List
  Attend dropdown nav (after Zoom Sessions):
    - Community & Signal
  Footer Learn section (after Learning Path):
    - Degree Programs
    - Careers
    - Home Lab
    - Portfolio Projects
    - Reading List
  Footer Attend section (after Zoom Sessions):
    - Community & Signal
  Footer Community section (after Contact Us):
    - Signal Chat

All inserts are idempotent — checks for existing entry before adding.
"""
import os
import re
import sys
from pathlib import Path

REPO = Path('/Users/shawn/csoh.org')

# Entries to add to nav (using ../ relative paths) — slug, label
NEW_LEARN = [
    ('cloud-security-degree-programs.html', 'Degree Programs'),
    ('cloud-security-careers.html', 'Careers'),
    ('cloud-security-home-lab.html', 'Home Lab'),
    ('cloud-security-portfolio-projects.html', 'Portfolio Projects'),
    ('cloud-security-reading-list.html', 'Reading List'),
]
NEW_ATTEND_NAV = [('community.html', 'Community &amp; Signal')]


def insert_after(content, anchor_pattern, items, prefix):
    """Insert <li> entries after the line matching anchor_pattern, using same indentation.

    Idempotent: skips items whose href is already present in the section.
    Returns (new_content, count_inserted).
    """
    inserted = 0
    new_content = content
    m = anchor_pattern.search(new_content)
    if not m:
        return new_content, 0
    indent = m.group(1)
    insert_pos = m.end()
    # Scope the idempotency check to the current <ul>...</ul> block so a hit in a
    # different section (e.g., footer Community) doesn't suppress an insertion in
    # this section (e.g., footer Attend).
    end_ul = new_content.find('</ul>', insert_pos)
    if end_ul == -1:
        end_ul = len(new_content)
    section = new_content[m.start():end_ul]
    additions = []
    for slug, label in items:
        href_attr = f'href="{prefix}{slug}"'
        if href_attr in section:
            continue
        additions.append(f'\n{indent}<li><a href="{prefix}{slug}">{label}</a></li>')
        inserted += 1
    if additions:
        new_content = new_content[:insert_pos] + ''.join(additions) + new_content[insert_pos:]
    return new_content, inserted


def insert_signal_chat_in_community_footer(content):
    """Insert Signal Chat <li> after Contact Us in the footer Community section."""
    if '<li><a href="/community.html">Signal Chat</a></li>' in content:
        return content, 0
    pattern = re.compile(
        r'(?P<indent>[ \t]*)<li><a href="mailto:admin@csoh\.org">Contact Us</a></li>'
    )
    m = pattern.search(content)
    if not m:
        return content, 0
    indent = m.group('indent')
    insertion = f'\n{indent}<li><a href="/community.html">Signal Chat</a></li>'
    return content[:m.end()] + insertion + content[m.end():], 1


def update_file(path):
    """Apply all six insertions to a single file. Returns dict of counts."""
    content = path.read_text()
    original = content
    counts = {}

    # 1. Nav Learn dropdown — anchor on Learning Path with ../
    nav_learn_anchor = re.compile(
        r'(?m)^([ \t]+)<li><a href="\.\./learning-path\.html"[^>]*>Learning Path</a></li>'
    )
    content, counts['nav_learn'] = insert_after(content, nav_learn_anchor, NEW_LEARN, '../')

    # 2. Nav Attend dropdown — anchor on Zoom Sessions with ../
    nav_attend_anchor = re.compile(
        r'(?m)^([ \t]+)<li><a href="\.\./sessions\.html"[^>]*>Zoom Sessions</a></li>'
    )
    content, counts['nav_attend'] = insert_after(content, nav_attend_anchor, NEW_ATTEND_NAV, '../')

    # 3. Footer Learn — anchor on Learning Path with /
    footer_learn_anchor = re.compile(
        r'(?m)^([ \t]+)<li><a href="/learning-path\.html">Learning Path</a></li>'
    )
    content, counts['footer_learn'] = insert_after(content, footer_learn_anchor, NEW_LEARN, '/')

    # 4. Footer Attend — anchor on Zoom Sessions with /
    footer_attend_anchor = re.compile(
        r'(?m)^([ \t]+)<li><a href="/sessions\.html">Zoom Sessions</a></li>'
    )
    content, counts['footer_attend'] = insert_after(content, footer_attend_anchor, NEW_ATTEND_NAV, '/')

    # 5. Footer Community — Signal Chat after Contact Us
    content, counts['footer_signal'] = insert_signal_chat_in_community_footer(content)

    if content != original:
        path.write_text(content)
        return counts
    return None


def main():
    targets = []
    for sub in ('breaches', 'meetings'):
        d = REPO / sub
        if not d.exists():
            continue
        targets.extend(sorted(d.glob('*.html')))

    print(f'Scanning {len(targets)} subdir HTML files...\n')
    totals = {'nav_learn': 0, 'nav_attend': 0, 'footer_learn': 0, 'footer_attend': 0, 'footer_signal': 0}
    files_changed = 0

    for path in targets:
        counts = update_file(path)
        if counts is not None:
            files_changed += 1
            for k, v in counts.items():
                totals[k] += v

    print(f'Files changed: {files_changed}')
    print('Total insertions:')
    for k, v in totals.items():
        print(f'  {k}: {v}')


if __name__ == '__main__':
    main()
