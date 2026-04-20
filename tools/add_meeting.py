#!/usr/bin/env python3
"""Append a new CSOH meeting recap section to meetings.html.

Input is an Apple Notes-style export of a "CSOH YYYY-MM-DD" note, saved to
a file (HTML or plain text). The script parses headings and paragraphs, then
injects a rendered <article class="section" id="meeting-YYYY-MM-DD"> block at
the top of the meetings list on meetings.html and a new entry into the
in-page index.

Supported input formats:

1. Apple Notes HTML export — `<div>`/`<h1>`/`<h2>` soup as returned by the
   Apple Notes MCP `get_note_content` tool.
2. Plain text / Markdown — lines beginning with `#` or `##` are treated as
   headings; everything else is a paragraph belonging to the most recent
   heading.

Expected content:
- An `<h1>` (or `# ...`) with the note title, e.g. `CSOH 2026-04-24`.
- An `<h2>` (or `## Quick recap`) followed by the recap paragraph.
- Any number of `<h2>` / `## ...` subsections followed by a paragraph each.

Usage:

    python3 tools/add_meeting.py path/to/note.html
    python3 tools/add_meeting.py path/to/note.txt --headline "Short headline"

The `--headline` flag lets you override the TOC entry's short headline. If
omitted, the headline is derived from the first subtopic heading.

Re-running the script for an existing date replaces the prior entry in place.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html as h
import re
import sys
from pathlib import Path


MEETINGS_HTML = Path(__file__).resolve().parent.parent / "meetings.html"

TITLE_RE = re.compile(r"CSOH\s+(\d{4}-\d{2}-\d{2})", re.IGNORECASE)
ENTITY_FIXES = [
    ("&quot;", '"'),
    ("&quot", '"'),
    ("&amp;", "&"),
    ("&amp", "&"),
    ("&#x27;", "'"),
    ("&#39;", "'"),
    ("&lt;", "<"),
    ("&gt;", ">"),
]


def clean_text(s: str) -> str:
    for before, after in ENTITY_FIXES:
        s = s.replace(before, after)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def strip_tags(fragment: str) -> str:
    return re.sub(r"<[^>]+>", "", fragment)


def parse_html_note(raw: str) -> dict:
    """Parse Apple Notes-style HTML into structured meeting data."""
    # Title (h1 or first CSOH date we find)
    title_match = TITLE_RE.search(raw)
    if not title_match:
        raise ValueError("Could not find a `CSOH YYYY-MM-DD` title in the note.")
    date_iso = title_match.group(1)

    # Normalize whitespace and remove line breaks between tags
    text = raw.replace("\r", "")

    # Find all h1/h2 headings and the content between them.
    pieces = re.split(
        r"<h([12])[^>]*>(.*?)</h\1>",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )
    # re.split with a capturing group returns: [before, lvl, heading, body, lvl, heading, body, ...]
    sections: list[tuple[str, str]] = []  # (heading, body_html)
    # Skip leading text; iterate in groups of 3
    for i in range(1, len(pieces), 3):
        lvl = pieces[i]
        heading_html = pieces[i + 1]
        body_html = pieces[i + 2] if i + 2 < len(pieces) else ""
        heading = clean_text(strip_tags(heading_html))
        if not heading:
            continue
        sections.append((heading, body_html))

    if not sections:
        # Fallback: maybe the note is plain text with h1 only
        raise ValueError("Note has no <h2> sections to parse.")

    # The first section with a CSOH date heading is the title; skip it.
    topics: list[tuple[str, str]] = []
    recap = ""
    for heading, body_html in sections:
        body_text = clean_text(strip_tags(body_html))
        if TITLE_RE.search(heading):
            continue
        if heading.lower() in ("quick recap", "summary") and not recap:
            if heading.lower() == "summary" and not body_text:
                # Some notes have an empty "Summary" heading that precedes topics.
                continue
            recap = body_text
            continue
        if body_text:
            topics.append((heading, body_text))

    if not recap:
        raise ValueError("Could not locate a 'Quick recap' paragraph in the note.")
    if not topics:
        raise ValueError("No topic sections with content found.")

    return {"date": date_iso, "recap": recap, "topics": topics}


def parse_markdown_note(raw: str) -> dict:
    """Parse markdown/plain-text note where lines start with # or ## headings."""
    title_match = TITLE_RE.search(raw)
    if not title_match:
        raise ValueError("Could not find a `CSOH YYYY-MM-DD` title in the note.")
    date_iso = title_match.group(1)

    lines = [ln.strip() for ln in raw.splitlines()]
    sections: list[tuple[str, list[str]]] = []
    current_heading: str | None = None
    current_body: list[str] = []
    for ln in lines:
        m = re.match(r"^(#{1,3})\s+(.*)$", ln)
        if m:
            if current_heading is not None:
                sections.append((current_heading, current_body))
            current_heading = m.group(2).strip()
            current_body = []
        else:
            if current_heading is not None and ln:
                current_body.append(ln)
    if current_heading is not None:
        sections.append((current_heading, current_body))

    recap = ""
    topics: list[tuple[str, str]] = []
    for heading, body in sections:
        body_text = clean_text(" ".join(body))
        if TITLE_RE.search(heading):
            continue
        if heading.lower() in ("quick recap", "summary") and not recap:
            if heading.lower() == "summary" and not body_text:
                continue
            recap = body_text
            continue
        if body_text:
            topics.append((heading, body_text))

    if not recap:
        raise ValueError("Could not locate a 'Quick recap' section in the note.")
    if not topics:
        raise ValueError("No topic sections with content found.")

    return {"date": date_iso, "recap": recap, "topics": topics}


def parse_note(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    looks_like_html = "<" in raw and re.search(r"<(div|h1|h2|p|br)\b", raw, re.IGNORECASE)
    parser = parse_html_note if looks_like_html else parse_markdown_note
    return parser(raw)


def human_date(iso: str) -> str:
    d = dt.date.fromisoformat(iso)
    return d.strftime("%A, %B %-d, %Y")


def render_meeting_block(meeting: dict) -> str:
    iso = meeting["date"]
    human = human_date(iso)
    topics = meeting["topics"]
    topic_html = "\n".join(
        f'            <h3>{h.escape(heading)}</h3>\n            <p>{h.escape(body)}</p>'
        for heading, body in topics
    )
    # Month tag is always present; topical tags come from --tag / parsed input.
    month = iso[:7]
    tags = [month] + list(dict.fromkeys(meeting.get("tags") or []))  # dedupe, preserve order
    tag_spans = "".join(f'<span class="tag">{h.escape(t)}</span>' for t in tags)
    tags_block = f'            <div class="resource-tags meeting-tags">{tag_spans}</div>\n'
    n = len(topics)
    summary_label = f"Show {n} discussion topics" if n != 1 else "Show discussion topic"
    return (
        f'        <article class="section" id="meeting-{iso}">\n'
        f'            <h2>CSOH {iso}</h2>\n'
        f'            <p><time datetime="{iso}"><em>{human}</em></time></p>\n'
        f'            <p><strong>Quick recap.</strong> {h.escape(meeting["recap"])}</p>\n'
        f'{tags_block}'
        f'            <details class="meeting-topics">\n'
        f'                <summary>{summary_label}</summary>\n'
        f'{topic_html}\n'
        f'            </details>\n'
        f'            <p class="small"><a href="#table-of-contents">↑ Back to index</a></p>\n'
        f'        </article>\n'
    )


def render_toc_item(meeting: dict, headline: str) -> str:
    return (
        f'                <li><a href="#meeting-{meeting["date"]}">'
        f'<strong>CSOH {meeting["date"]}</strong> — {h.escape(headline)}</a></li>'
    )


def replace_or_insert_article(html_text: str, meeting: dict) -> str:
    new_block = render_meeting_block(meeting)
    article_re = re.compile(
        rf'        <article class="section" id="meeting-{re.escape(meeting["date"])}">.*?</article>\n',
        re.DOTALL,
    )
    if article_re.search(html_text):
        return article_re.sub(new_block.rstrip("\n") + "\n", html_text, count=1)

    # Insert after the </section> that closes the TOC (#table-of-contents).
    toc_close = re.compile(
        r'(<section class="section" id="table-of-contents">.*?</section>\s*\n)',
        re.DOTALL,
    )
    m = toc_close.search(html_text)
    if not m:
        raise RuntimeError("Could not locate the table-of-contents section in meetings.html.")
    insert_at = m.end()
    return html_text[:insert_at] + "\n" + new_block + html_text[insert_at:]


def replace_or_insert_toc(html_text: str, meeting: dict, headline: str) -> str:
    item = render_toc_item(meeting, headline)
    existing_re = re.compile(
        rf'                <li><a href="#meeting-{re.escape(meeting["date"])}">.*?</a></li>',
        re.DOTALL,
    )
    if existing_re.search(html_text):
        return existing_re.sub(item, html_text, count=1)

    # Insert as the new first item inside the #table-of-contents ul.
    ul_open = re.compile(
        r'(<section class="section" id="table-of-contents">.*?<ul>\n)',
        re.DOTALL,
    )
    m = ul_open.search(html_text)
    if not m:
        raise RuntimeError("Could not locate the TOC <ul> in meetings.html.")
    insert_at = m.end()
    return html_text[:insert_at] + item + "\n" + html_text[insert_at:]


def bump_toc_count(html_text: str) -> str:
    # Count current article entries AFTER insertion and reflect in TOC heading.
    count = len(re.findall(r'<article class="section" id="meeting-', html_text))
    if count == 0:
        return html_text
    return re.sub(
        r'<h2>All meetings \(\d+\)</h2>',
        f'<h2>All meetings ({count})</h2>',
        html_text,
        count=1,
    )


def default_headline(meeting: dict) -> str:
    if meeting["topics"]:
        return meeting["topics"][0][0]
    return "Meeting recap"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Add a CSOH meeting recap to meetings.html")
    parser.add_argument("note", type=Path, help="Path to the Apple Notes export (HTML or text)")
    parser.add_argument(
        "--headline",
        type=str,
        default=None,
        help="Short headline for the table of contents (default: first topic heading).",
    )
    parser.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Topical tag to attach (repeatable). Example: --tag AI --tag Conferences",
    )
    parser.add_argument(
        "--meetings-file",
        type=Path,
        default=MEETINGS_HTML,
        help="Path to meetings.html (default: repo-root meetings.html).",
    )
    args = parser.parse_args(argv)

    if not args.note.exists():
        print(f"Error: {args.note} not found", file=sys.stderr)
        return 1
    if not args.meetings_file.exists():
        print(f"Error: {args.meetings_file} not found", file=sys.stderr)
        return 1

    try:
        meeting = parse_note(args.note)
    except ValueError as exc:
        print(f"Error parsing note: {exc}", file=sys.stderr)
        return 1

    meeting["tags"] = [t.strip() for t in args.tag if t.strip()]

    headline = args.headline or default_headline(meeting)
    html_text = args.meetings_file.read_text(encoding="utf-8")

    updated = replace_or_insert_article(html_text, meeting)
    updated = replace_or_insert_toc(updated, meeting, headline)
    updated = bump_toc_count(updated)

    if updated == html_text:
        print("No changes (meeting already present with identical content).")
        return 0

    args.meetings_file.write_text(updated, encoding="utf-8")
    action = "Replaced" if html_text.count(f'id="meeting-{meeting["date"]}"') else "Inserted"
    print(
        f"{action} CSOH {meeting['date']} "
        f"({len(meeting['topics'])} topics) in {args.meetings_file.name}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
