#!/usr/bin/env python3
"""Generate per-page Open Graph (social-share) images.

Renders a CSOH-branded 1200×630 image for each page in PAGES, saves them
under ../img/og/<slug>.jpg, and rewrites each page's <meta property="og:image">
+ <meta name="twitter:image"> to point at the new file.

Idempotent — re-running regenerates images for any page whose content
might have changed; pages whose OG image is already set to the per-page
version won't get a redundant URL update.

Usage:
    python3 tools/generate_og_images.py
    python3 tools/generate_og_images.py --pages index.html ctfs.html
    python3 tools/generate_og_images.py --skip-html       # only regenerate jpgs
"""

from __future__ import annotations

import argparse
import http.server
import re
import socket
import socketserver
import sys
import threading
import urllib.parse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "tools" / "og" / "template.html"
OUT_DIR = REPO_ROOT / "img" / "og"
OG_VIEWPORT = {"width": 1200, "height": 630}

# (filename, title, subtitle, badge) — keep titles ≤ ~60 chars and subtitles
# ≤ ~140 chars so the template doesn't have to clamp aggressively. The
# subtitle prints under the headline; choose a one-line value prop, not
# the page meta description.
PAGES = [
    ("index.html",
     "Cloud Security, Vendor-Neutral",
     "2,000+ practitioners. 200+ resources. Free weekly Zoom. No marketing.",
     "Community"),
    ("what-is-cloud-security.html",
     "What is Cloud Security?",
     "Shared responsibility, the threats that matter, the tool landscape — explained by practitioners.",
     "Pillar Guide"),
    ("learning-path.html",
     "Cloud Security Learning Path",
     "Beginner → working practitioner. Roadmap, milestones, and the labs that actually teach.",
     "Roadmap"),
    ("cloud-security-best-practices.html",
     "Cloud Security Best Practices",
     "The controls that actually prevent breaches — ranked by what shows up as root cause in real incident reports.",
     "Practitioner Guide"),
    ("shared-responsibility-model.html",
     "The Shared Responsibility Model",
     "What the cloud provider secures vs. what you secure. Across IaaS, PaaS, SaaS, and serverless.",
     "Pillar Guide"),
    ("cspm-vs-cnapp.html",
     "CSPM vs CNAPP vs CWPP vs CIEM vs DSPM",
     "The acronym soup decoded. When you need each tool, where they overlap, and the open-source alternatives.",
     "Tool Comparison"),
    ("cloud-security-certifications.html",
     "Cloud Security Certifications Compared",
     "CCSK, CCSP, AWS, Azure, GCP, CKS — side by side, with recommended paths by role.",
     "Comparison"),
    ("github-actions.html",
     "How We Use GitHub Actions",
     "Learn CI/CD by reading our heavily commented production workflows. Triggers, secrets, gotchas, all real.",
     "Tutorial"),
    ("resources.html",
     "200+ Cloud Security Resources",
     "CTFs, labs, tools, certifications, and AI-security resources — curated by the CSOH community.",
     "Directory"),
    ("ctfs.html",
     "Cloud Security CTF Challenges",
     "Hands-on practice for AWS, Azure, GCP, Kubernetes and AI security. Free and open-source.",
     "Hands-On"),
    ("conferences.html",
     "Security & Hacker Conferences",
     "RSA, DEF CON, Black Hat, fwd:cloudsec, CCC, OffensiveCon, BSides — and which ones are worth attending.",
     "Directory"),
    ("glossary.html",
     "The Cloud Security Glossary",
     "230+ terms — IAM, CNAPP, CSPM, MITRE ATT&CK, AI security and more — in plain English.",
     "Reference"),
    ("breach-timeline.html",
     "Cloud Breach Kill Chains",
     "Step-by-step attack reconstructions mapped to MITRE ATT&CK Cloud. Capital One, SolarWinds, MGM, and more.",
     "Threat Library"),
    ("threat-research.html",
     "Cloud Threat Research Directory",
     "Vendor research teams, IOC feeds, MITRE ATT&CK Cloud mappings, government advisories — curated.",
     "Defender Resource"),
    ("meetings.html",
     "91 Weekly Cloud Security Recaps",
     "Topic-by-topic notes from every CSOH Friday session — 91 meetings searchable by speaker and topic.",
     "Archive"),
    ("faq.html",
     "Cloud Security Office Hours FAQ",
     "What CSOH is, how to join, what to expect at the Friday Zoom, and how to contribute.",
     "FAQ"),
    ("news.html",
     "Cloud Security News",
     "AWS, Azure, GCP, Kubernetes news — curated daily from 39 vendor-neutral sources.",
     "Daily News"),
    ("sessions.html",
     "Free Weekly Cloud Security Zoom",
     "Friday 7am PT. Expert talks, open discussion, Q&A. 2,000+ members. No marketing.",
     "Community"),
    ("presentations.html",
     "Cloud Security Talks Archive",
     "Recordings of past CSOH Zoom sessions — speakers, talks, and walkthroughs.",
     "Archive"),
    ("about-shawn-nunley.html",
     "About Shawn Nunley",
     "Founder of Cloud Security Office Hours. 25+ years across cloud, identity, infrastructure, and security.",
     "About"),
    ("contribute.html",
     "Contribute to CSOH",
     "Add resources, propose talks, fix typos, build tools. Open-source, by the community, for the community.",
     "Open Source"),
    ("contribute-resources.html",
     "How to Add a Resource",
     "Step-by-step guide for submitting CTFs, tools, certifications, and labs to CSOH. Beginner-friendly, no coding required.",
     "How-To"),
    ("privacy.html",
     "Privacy Policy",
     "No cookies, no trackers, no marketing pixels. CSOH's plain-English privacy policy in one short read.",
     "Policy"),
    ("security-policy.html",
     "Security Vulnerability Disclosure",
     "How to responsibly report security issues to CSOH — scope, response timeline, and recognition.",
     "Policy"),
    ("code-of-conduct.html",
     "Code of Conduct",
     "Community standards for CSOH Friday Zoom sessions, the mailing list, and the GitHub repo.",
     "Policy"),
    ("rss.html",
     "Subscribe to Cloud Security News",
     "RSS feed of curated cloud security news from 39 vendor-neutral sources — updated daily.",
     "Subscribe"),
    ("kevin-mitnick.html",
     "Kevin Mitnick — In Memoriam",
     "A personal tribute by Shawn Nunley. From adversaries to brothers — a story of justice, redemption, and friendship.",
     "Memorial"),
]


def find_free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args, **_kwargs):
        pass


def serve_repo(port: int) -> socketserver.ThreadingTCPServer:
    def handler(*args, **kwargs):
        return Handler(*args, directory=str(REPO_ROOT), **kwargs)
    server = socketserver.ThreadingTCPServer(("127.0.0.1", port), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def slug_for(filename: str) -> str:
    """index.html → index, ctfs.html → ctfs, breach-timeline.html → breach-timeline."""
    return filename[:-5] if filename.endswith(".html") else filename


def update_html_meta(filename: str, og_path: str) -> bool:
    """Rewrite og:image and twitter:image meta tags to point at the new
    per-page asset. Returns True if the file was modified."""
    full_path = REPO_ROOT / filename
    if not full_path.exists():
        return False
    s = full_path.read_text(encoding="utf-8")
    original = s

    # Absolute URL because OG/Twitter scrapers fetch by URL, not path.
    abs_url = f"https://csoh.org/{og_path}"

    s = re.sub(
        r'(<meta\s+property="og:image"\s+content=")[^"]+(")',
        rf'\1{abs_url}\2',
        s,
        count=1,
    )
    s = re.sub(
        r'(<meta\s+name="twitter:image"\s+content=")[^"]+(")',
        rf'\1{abs_url}\2',
        s,
        count=1,
    )

    if s != original:
        full_path.write_text(s, encoding="utf-8")
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate per-page OG images.")
    parser.add_argument("--pages", nargs="*",
                        help="Subset of filenames to regenerate (default: all)")
    parser.add_argument("--skip-html", action="store_true",
                        help="Only regenerate JPGs, don't rewrite the meta tags")
    args = parser.parse_args()

    if not TEMPLATE_PATH.exists():
        print(f"missing template: {TEMPLATE_PATH}", file=sys.stderr)
        return 1

    targets = PAGES
    if args.pages:
        targets = [p for p in PAGES if p[0] in args.pages]
        if not targets:
            print("No matching pages in PAGES list", file=sys.stderr)
            return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Install playwright: pip install playwright && playwright install chromium",
              file=sys.stderr)
        return 2

    port = find_free_port()
    server = serve_repo(port)
    template_url = f"http://127.0.0.1:{port}/tools/og/template.html"
    print(f"🎨 Generating {len(targets)} OG images at {OG_VIEWPORT['width']}x{OG_VIEWPORT['height']}...\n")

    generated = 0
    html_updated = 0

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        try:
            context = browser.new_context(
                viewport=OG_VIEWPORT,
                device_scale_factor=2,    # crisp on retina
            )
            page = context.new_page()

            for filename, title, subtitle, badge in targets:
                slug = slug_for(filename)
                params = urllib.parse.urlencode({
                    "title": title,
                    "subtitle": subtitle,
                    "badge": badge,
                })
                url = f"{template_url}?{params}"
                page.goto(url, wait_until="networkidle")
                page.wait_for_timeout(120)

                out_path = OUT_DIR / f"{slug}.jpg"
                page.screenshot(
                    path=str(out_path),
                    type="jpeg",
                    quality=88,
                    full_page=False,
                    clip={"x": 0, "y": 0, "width": OG_VIEWPORT["width"], "height": OG_VIEWPORT["height"]},
                )
                generated += 1

                rel = out_path.relative_to(REPO_ROOT).as_posix()
                if not args.skip_html:
                    if update_html_meta(filename, rel):
                        html_updated += 1
                        print(f"  ✓ {filename} → {rel} (meta updated)")
                    else:
                        print(f"    {filename} → {rel} (meta already set)")
                else:
                    print(f"  ✓ {rel}")
        finally:
            browser.close()

    server.shutdown()
    print(f"\nGenerated {generated} images. Updated {html_updated} HTML files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
