#!/usr/bin/env python3
"""Generate .webp siblings for every JPEG image under img/og/ and img/previews/.

Why .webp: modern browsers send `Accept: image/webp`; serving WebP saves
~25-35% bandwidth at equivalent quality. The `.htaccess` rule we add does
content negotiation transparently — no HTML changes needed.

Idempotent: skips files whose .webp sibling is newer than the .jpg source.

Requires Pillow (pip install Pillow). On the deploy runner Pillow is
already installed alongside Playwright for the preview generator.

Usage:
    python3 tools/generate_webp.py             # all dirs
    python3 tools/generate_webp.py img/og      # specific dir
    python3 tools/generate_webp.py --force     # regenerate even if up-to-date
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIRS = [REPO_ROOT / "img" / "og", REPO_ROOT / "img" / "previews"]
# Quality 82 is the sweet spot: indistinguishable from JPEG at the same
# perceived quality, but ~30% smaller. 75 is too soft on text; 90 starts
# bloating without visible benefit.
WEBP_QUALITY = 82


def convert(src: Path, force: bool) -> tuple[bool, int, int]:
    """Returns (converted, src_bytes, dst_bytes)."""
    dst = src.with_suffix(".webp")
    if not force and dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return False, src.stat().st_size, dst.stat().st_size

    from PIL import Image
    with Image.open(src) as img:
        # If the source has a palette or transparency mode, convert to RGB
        # so WebP encoding doesn't drop information unpredictably.
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")
        img.save(
            dst,
            "WEBP",
            quality=WEBP_QUALITY,
            method=6,    # slowest/best compression
        )
    return True, src.stat().st_size, dst.stat().st_size


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate WebP siblings for JPEGs.")
    parser.add_argument("dirs", nargs="*", help="Subset of dirs to process")
    parser.add_argument("--force", action="store_true",
                        help="Regenerate even if .webp is up to date")
    args = parser.parse_args()

    targets = [Path(d) if Path(d).is_absolute() else REPO_ROOT / d for d in args.dirs] or DEFAULT_DIRS

    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("Pillow not installed. pip install Pillow", file=sys.stderr)
        return 2

    total_src = 0
    total_dst = 0
    converted = 0
    skipped = 0
    failed = 0

    for d in targets:
        if not d.exists():
            print(f"  - skip (missing): {d.relative_to(REPO_ROOT)}")
            continue
        jpgs = sorted(list(d.glob("*.jpg")) + list(d.glob("*.jpeg")))
        if not jpgs:
            continue
        print(f"📁 {d.relative_to(REPO_ROOT)} — {len(jpgs)} source JPEGs")
        for src in jpgs:
            try:
                did, src_b, dst_b = convert(src, force=args.force)
            except Exception as e:
                print(f"  ✗ {src.name}: {e}")
                failed += 1
                continue
            total_src += src_b
            total_dst += dst_b
            if did:
                converted += 1
            else:
                skipped += 1

    if total_src:
        savings_pct = 100 * (total_src - total_dst) / total_src
        print(
            f"\n✓ {converted} converted, {skipped} up-to-date, {failed} failed."
            f" Total: {total_src/1024:.0f}KB → {total_dst/1024:.0f}KB"
            f" ({savings_pct:.0f}% smaller)."
        )
    else:
        print("\nNothing to do.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
