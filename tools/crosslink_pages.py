#!/usr/bin/env python3
"""Cross-link glossary terms across content pages.

For each content page, finds the first occurrence of each glossary term
and wraps it in <a class="glossary-link" href="glossary.html#term-...">.

Skip zones (no linking inside any of these):
  - existing <a>...</a> elements
  - <code>, <pre>, <script>, <style>
  - <h1>-<h6>
  - <header>, <footer>, <nav>
  - HTML comments
  - HTML attribute values
  - JSON-LD blocks

Idempotent: existing <a class="glossary-link" href="glossary.html#..."> links
are stripped and rebuilt on every run, so changing the rules or adding
glossary terms is safe.

Per-page rules:
  - Only the first occurrence per page (across the whole body) is linked,
    to keep prose readable.
  - Terms in DENYLIST (overlap with ordinary English) are skipped, just as
    in crosslink_glossary.py.
  - The glossary page itself is not processed (it has its own script).
"""

from __future__ import annotations

import re
import sys
from html import unescape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GLOSSARY_FILE = REPO_ROOT / "glossary.html"

# Pages we cross-link. The glossary is excluded (its own script handles it),
# and pages with no useful prose (404, sitemap, login forms) are excluded too.
TARGET_PAGES = [
    "index.html",
    "resources.html",
    "ctfs.html",
    "threat-research.html",
    "breach-timeline.html",
    "meetings.html",
    "presentations.html",
    "sessions.html",
    "faq.html",
    "rss.html",
    "chat-resources.html",
    "what-is-cloud-security.html",
    "learning-path.html",
    "cloud-security-certifications.html",
    "kevin-mitnick.html",
    "contribute.html",
    "contribute-resources.html",
    "code-of-conduct.html",
    "privacy.html",
    "security-policy.html",
]

# Single-word terms common enough in English that linking them is more
# distracting than helpful. Kept in sync with crosslink_glossary.py.
DENYLIST = {
    "public",
    "private",
    "hybrid",
    "image",
    "baseline",
    "registry",
    "principal",
    "first",
    # Extras for content pages where these words appear constantly:
    "cloud",
    "data",
    "policy",
    "policies",
    "control",
    "controls",
    "secret",
    "secrets",
    "key",
    "keys",
    "log",
    "logs",
    "audit",
    "scope",
    "session",
    "sessions",
    "tag",
    "tags",
    "role",
    "roles",
    "user",
    "users",
    "account",
    "accounts",
    # False-positive single-word remnants extracted from compound entries
    # like "Blue / Red Team" or "Kev / Kevin" — link the full phrase only.
    "blue",
    "red",
    "purple",
    "kev",
    "agent",      # too generic in prose; Agent (LLM) usually rendered with caps
    "container",  # generic English usage
    "drift",      # configuration drift only meaningful with context
    "subnet",     # plain networking term, common
    "functions",  # also common English
    "vault",      # ambiguous: HashiCorp/Azure Key Vault depending on context
    "blast",      # only useful in "blast radius"
    "ad",         # shell `ad`, ambiguous
}

# Sections of the file to skip wholesale (no links anywhere inside).
SKIP_BLOCK_TAGS = (
    "header",
    "footer",
    "nav",
    "script",
    "style",
    "code",
    "pre",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
)

GLOSSARY_LINK_HREF_PREFIX = "glossary.html#"


def slugify(text: str) -> str:
    text = unescape(text)
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return "term-" + text if text else "term-unknown"


def derive_keys(dt_inner_html: str) -> list[str]:
    """Same logic as crosslink_glossary.derive_keys."""
    text = re.sub(r"<[^>]+>", "", dt_inner_html)
    text = unescape(text).strip()
    parts = re.split(r"\s*[—–]\s*", text, maxsplit=1)
    lhs = parts[0]
    rhs = parts[1] if len(parts) > 1 else ""
    keys: list[str] = []

    def add_with_parens(s: str) -> None:
        base = re.sub(r"\s*\([^)]*\)", "", s).strip()
        for piece in re.split(r"\s*/\s*", base):
            piece = piece.strip()
            if piece:
                keys.append(piece)
        for m in re.finditer(r"\(([^)]+)\)", s):
            for piece in re.split(r"\s*/\s*", m.group(1)):
                piece = piece.strip()
                if piece:
                    keys.append(piece)

    add_with_parens(lhs)
    if rhs:
        for piece in re.split(r"\s*/\s*", rhs):
            piece = re.sub(r"\s*\([^)]*\)", "", piece).strip()
            if piece and 1 <= len(piece.split()) <= 6:
                keys.append(piece)

    seen: set[str] = set()
    unique: list[str] = []
    for k in keys:
        kl = k.lower()
        if not kl or kl in seen or kl in DENYLIST:
            continue
        seen.add(kl)
        unique.append(k)
    return unique


def load_glossary_terms() -> tuple[dict[str, str], list[str]]:
    """Parse glossary.html and return:
      - key_to_slug:   lowercased-key -> slug
      - original_keys: original-case spellings (for is_acronym checks)
    """
    content = GLOSSARY_FILE.read_text(encoding="utf-8")
    key_to_slug: dict[str, str] = {}
    original_keys: list[str] = []
    pattern = re.compile(r"<dt(\s[^>]*)?>(.*?)</dt>", re.DOTALL)
    for m in pattern.finditer(content):
        attrs = m.group(1) or ""
        inner = m.group(2)
        keys = derive_keys(inner)
        if not keys:
            continue
        existing_id = re.search(r"\bid\s*=\s*[\"']([^\"']+)[\"']", attrs)
        slug = existing_id.group(1) if existing_id else slugify(keys[0])
        for k in keys:
            kl = k.lower()
            if kl and kl not in key_to_slug:
                key_to_slug[kl] = slug
                original_keys.append(k)
    return key_to_slug, original_keys


def is_acronym(key: str) -> bool:
    """All-uppercase, 2-8 chars, no spaces — require case-sensitive match
    so 'AI' (the acronym) matches but 'ai' (in 'aim', 'rain', etc.) doesn't."""
    return (
        2 <= len(key) <= 8
        and " " not in key
        and key == key.upper()
        and any(c.isalpha() for c in key)
    )


def build_term_regexes(keys: list[str]) -> list[tuple[re.Pattern[str], bool]]:
    """Returns (pattern, case_sensitive) pairs.

    Acronyms are matched case-sensitively to avoid linking 'cd' to CD or
    'Kev' to KEV. Everything else is case-insensitive.
    """
    case_sensitive_keys = [k for k in keys if is_acronym(k)]
    case_insensitive_keys = [k for k in keys if not is_acronym(k)]

    patterns: list[tuple[re.Pattern[str], bool]] = []
    if case_sensitive_keys:
        sorted_keys = sorted(case_sensitive_keys, key=lambda k: -len(k))
        pieces = [re.escape(k) for k in sorted_keys]
        patterns.append((
            re.compile(r"(?<![A-Za-z0-9])(" + "|".join(pieces) + r")(?![A-Za-z0-9])"),
            True,
        ))
    if case_insensitive_keys:
        sorted_keys = sorted(case_insensitive_keys, key=lambda k: -len(k))
        pieces = [re.escape(k) for k in sorted_keys]
        patterns.append((
            re.compile(
                r"(?<![A-Za-z0-9])(" + "|".join(pieces) + r")(?![A-Za-z0-9])",
                flags=re.IGNORECASE,
            ),
            False,
        ))
    return patterns


def unwrap_existing_links(content: str) -> tuple[str, int]:
    """Strip every existing <a class="glossary-link" href="glossary.html#...">
    so we can rebuild fresh."""
    pattern = re.compile(
        r'<a\s+class="glossary-link"\s+href="glossary\.html#[^"]+">([^<]+)</a>',
        re.IGNORECASE,
    )
    removed = 0

    def replace(m: re.Match) -> str:
        nonlocal removed
        removed += 1
        return m.group(1)

    return pattern.sub(replace, content), removed


def mask_skip_zones(content: str) -> tuple[str, list[str]]:
    """Replace every protected region with a placeholder so the linker
    never touches it. Returns (masked, placeholders)."""
    placeholders: list[str] = []

    def stash(m: re.Match) -> str:
        placeholders.append(m.group(0))
        return f"\x00P{len(placeholders) - 1}\x00"

    # 1. HTML comments
    content = re.sub(r"<!--.*?-->", stash, content, flags=re.DOTALL)

    # 2. Block-level skip tags (script, style, code, pre, headings,
    #    header, footer, nav). DOTALL across multiple lines.
    for tag in SKIP_BLOCK_TAGS:
        content = re.sub(
            rf"<{tag}(\s[^>]*)?>.*?</{tag}>",
            stash,
            content,
            flags=re.DOTALL | re.IGNORECASE,
        )

    # 3. Existing anchors anywhere
    content = re.sub(
        r"<a\b[^>]*>.*?</a>",
        stash,
        content,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # 4. Any remaining HTML tag (so we never touch attribute values).
    #    Tags don't get mutated; we only modify text between tags.

    return content, placeholders


def unmask(content: str, placeholders: list[str]) -> str:
    def restore(m: re.Match) -> str:
        return placeholders[int(m.group(1))]

    return re.sub(r"\x00P(\d+)\x00", restore, content)


def link_text_segments(
    content: str,
    patterns: list[tuple[re.Pattern[str], bool]],
    key_to_slug: dict[str, str],
) -> tuple[str, list[str]]:
    """Walk masked content, only inserting links in text-between-tags.
    Records which slugs got linked (one per slug max — first per page)."""
    out: list[str] = []
    cursor = 0
    linked_slugs: set[str] = set()
    linked_words: list[str] = []

    tag_re = re.compile(r"<[^>]+>")
    for tm in tag_re.finditer(content):
        if tm.start() > cursor:
            text_chunk = content[cursor : tm.start()]
            new_chunk = _link_chunk(
                text_chunk, patterns, key_to_slug, linked_slugs, linked_words
            )
            out.append(new_chunk)
        out.append(tm.group(0))
        cursor = tm.end()
    if cursor < len(content):
        out.append(
            _link_chunk(
                content[cursor:], patterns, key_to_slug, linked_slugs, linked_words
            )
        )
    return "".join(out), linked_words


def _link_chunk(
    text: str,
    patterns: list[tuple[re.Pattern[str], bool]],
    key_to_slug: dict[str, str],
    linked_slugs: set[str],
    linked_words: list[str],
) -> str:
    """Find the earliest match across all patterns; iterate left-to-right."""
    if not text:
        return text
    out: list[str] = []
    cursor = 0
    while cursor < len(text):
        # Find the earliest match across all patterns from the cursor.
        best: tuple[int, int, str, str] | None = None  # (start, end, word, slug)
        for pat, _case_sensitive in patterns:
            m = pat.search(text, cursor)
            if not m:
                continue
            word = m.group(1)
            slug = key_to_slug.get(word.lower())
            if not slug or slug in linked_slugs:
                # Try the next match within this pattern beyond this one.
                # We'll handle skipped slugs by just looking further with
                # iterative finditer below in a fallback loop.
                continue
            if best is None or m.start() < best[0]:
                best = (m.start(), m.end(), word, slug)

        if best is None:
            # No more linkable matches — but a pattern may have matched a
            # slug that was already linked. We need to skip past those too.
            next_skip = _next_match_anywhere(text, cursor, patterns, key_to_slug)
            if next_skip is None:
                out.append(text[cursor:])
                break
            # Just emit text up through the unlinkable match and continue.
            out.append(text[cursor : next_skip])
            cursor = next_skip
            # Step at least one char so we don't loop.
            out.append(text[cursor])
            cursor += 1
            continue

        start, end, word, slug = best
        out.append(text[cursor:start])
        out.append(
            f'<a class="glossary-link" href="{GLOSSARY_LINK_HREF_PREFIX}{slug}">{word}</a>'
        )
        linked_slugs.add(slug)
        linked_words.append(word)
        cursor = end
    return "".join(out)


def _next_match_anywhere(
    text: str,
    cursor: int,
    patterns: list[tuple[re.Pattern[str], bool]],
    key_to_slug: dict[str, str],
) -> int | None:
    """Earliest position where any pattern matches, regardless of slug
    state. Used to advance the cursor past already-linked slug occurrences
    so we don't infinite-loop."""
    earliest: int | None = None
    for pat, _ in patterns:
        m = pat.search(text, cursor)
        if not m:
            continue
        if earliest is None or m.start() < earliest:
            earliest = m.start()
    return earliest


def crosslink_page(
    path: Path,
    patterns: list[tuple[re.Pattern[str], bool]],
    key_to_slug: dict[str, str],
) -> dict:
    raw = path.read_text(encoding="utf-8")
    cleaned, removed = unwrap_existing_links(raw)
    masked, placeholders = mask_skip_zones(cleaned)
    linked, linked_words = link_text_segments(masked, patterns, key_to_slug)
    final = unmask(linked, placeholders)
    if final != raw:
        path.write_text(final, encoding="utf-8")
    return {
        "file": path.name,
        "stripped": removed,
        "linked": len(linked_words),
        "words": linked_words,
        "changed": final != raw,
    }


def main() -> int:
    if not GLOSSARY_FILE.exists():
        print(f"glossary not found: {GLOSSARY_FILE}", file=sys.stderr)
        return 1

    key_to_slug, original_keys = load_glossary_terms()
    if not key_to_slug:
        print("No glossary terms found.", file=sys.stderr)
        return 1
    print(
        f"Loaded {len({v for v in key_to_slug.values()})} unique glossary terms "
        f"({len(key_to_slug)} aliases)."
    )

    patterns = build_term_regexes(original_keys)

    total_linked = 0
    total_pages_changed = 0
    for name in TARGET_PAGES:
        page = REPO_ROOT / name
        if not page.exists():
            print(f"  - skip (missing): {name}")
            continue
        result = crosslink_page(page, patterns, key_to_slug)
        marker = "✓" if result["changed"] else " "
        print(
            f"  {marker} {result['file']}: stripped {result['stripped']}, "
            f"linked {result['linked']}"
            + (f" ({', '.join(result['words'])})" if result["words"] else "")
        )
        total_linked += result["linked"]
        if result["changed"]:
            total_pages_changed += 1

    print(
        f"\nDone. Linked {total_linked} term mentions across "
        f"{total_pages_changed} pages."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
