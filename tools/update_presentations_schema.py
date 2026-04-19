#!/usr/bin/env python3
"""Regenerate VideoObject JSON-LD schema in presentations.html.

Parses each YouTube card in the presentations page (anchor → card-link to
youtube.com/watch?v=<id>) and emits a `<script type="application/ld+json">`
block with a VideoObject for each entry. The block is injected just before
`</head>`, replacing any prior block with the same marker comment.

Run whenever presentations are added/edited.
"""

import datetime as dt
import html as html_mod
import json
import re
import sys
from pathlib import Path

HTML_PATH = Path(__file__).resolve().parent.parent / "presentations.html"

MARKER = "<!-- Structured Data - Presentations (VideoObject) -->"

CARD_RE = re.compile(
    r'<a\s+href="(https://www\.youtube\.com/watch\?v=([^"]+))"[^>]*class="card-link"[^>]*>'
    r'(.*?)</a>',
    re.DOTALL,
)
H3_RE = re.compile(r"<h3[^>]*>(.*?)</h3>", re.DOTALL)
P_RE = re.compile(r"<p[^>]*>(.*?)</p>", re.DOTALL)
DATE_RE = re.compile(r"^([A-Z][a-z]+ \d{1,2}, \d{4}):\s*")


def strip_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", html_mod.unescape(text)).strip()


def parse_date(prefix: str) -> str | None:
    try:
        return dt.datetime.strptime(prefix, "%B %d, %Y").date().isoformat()
    except ValueError:
        return None


def extract_videos(html_text: str):
    for m in CARD_RE.finditer(html_text):
        url = m.group(1)
        video_id = m.group(2)
        card_body = m.group(3)
        h3m = H3_RE.search(card_body)
        pm = P_RE.search(card_body)
        if not h3m or not pm:
            continue
        title = strip_tags(h3m.group(1))
        desc = strip_tags(pm.group(1))
        date_match = DATE_RE.match(title)
        upload_date = parse_date(date_match.group(1)) if date_match else None
        name = DATE_RE.sub("", title) or title
        yield {
            "video_id": video_id,
            "url": url,
            "name": name,
            "description": desc,
            "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
            "upload_date": upload_date,
        }


def build_items(videos):
    items = []
    for v in videos:
        item = {
            "@type": "VideoObject",
            "name": v["name"],
            "description": v["description"],
            "thumbnailUrl": v["thumbnail"],
            "contentUrl": v["url"],
            "embedUrl": f"https://www.youtube.com/embed/{v['video_id']}",
            "publisher": {
                "@type": "Organization",
                "name": "Cloud Security Office Hours",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://csoh.org/banner.png",
                },
            },
        }
        if v["upload_date"]:
            item["uploadDate"] = v["upload_date"]
        items.append(item)
    return items


def render_block(items) -> str:
    schema = {"@context": "https://schema.org", "@graph": items}
    payload = json.dumps(schema, indent=2, ensure_ascii=False).replace("</", "<\\/")
    indented = "\n".join(("    " + line) if line else line for line in payload.split("\n"))
    return (
        f"    {MARKER}\n"
        f'    <script type="application/ld+json">\n'
        f"{indented}\n"
        f"    </script>\n"
    )


def inject(html_text: str, block: str) -> str:
    existing = re.compile(
        rf"\s*{re.escape(MARKER)}\s*<script type=\"application/ld\+json\">.*?</script>\n?",
        re.DOTALL,
    )
    if existing.search(html_text):
        return existing.sub("\n" + block, html_text, count=1)
    return html_text.replace("</head>", block + "</head>", 1)


def main() -> int:
    html_text = HTML_PATH.read_text(encoding="utf-8")
    videos = list(extract_videos(html_text))
    if not videos:
        print("No YouTube cards found", file=sys.stderr)
        return 1
    items = build_items(videos)
    block = render_block(items)
    new_text = inject(html_text, block)
    if new_text != html_text:
        HTML_PATH.write_text(new_text, encoding="utf-8")
        print(f"Updated presentations.html with {len(items)} VideoObject entries")
    else:
        print("presentations.html schema already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
