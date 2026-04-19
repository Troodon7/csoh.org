# Sitemap Lastmod Refresher

Refreshes `<lastmod>` dates in `sitemap.xml` so search engines see accurate modification times for each page.

## Quick Start

```bash
python3 tools/update_sitemap.py
```

Prints one line per URL whose `<lastmod>` changed. Exits 0 even when nothing changed.

## How It Picks Dates

For each `<url>` entry in `sitemap.xml`, the script maps `<loc>` to a local file (e.g. `https://csoh.org/news.html` → `news.html`; bare origin → `index.html`) and sets `<lastmod>` to, in order:

1. **Today's date**, if the file has uncommitted changes (working tree or index). This covers the case where `update_news.py` just rewrote `news.html` and the sitemap step runs before the commit.
2. **`git log -1 --format=%cs -- <file>`** — the last commit date of that file.
3. **File mtime**, if the file isn't tracked in git (rare).

## Where It Runs

- **`update_news.py`** calls it after writing `news.html` and `feed.xml`, so sitemap stays current with news updates.
- **`.github/workflows/site-update-deploy.yml`** runs it before every deploy and commits any change.
- The update-news auto-merge filter allows `sitemap.xml` alongside `news.html` and `feed.xml`.

## When To Run Manually

- After editing HTML pages locally, to preview the sitemap change before committing.
- If `sitemap.xml` drifts from actual page dates (e.g., after a bulk edit).

## Requirements

- Python 3.9+ (standard library only)
- Run from the repo root (the script resolves paths relative to its own location, so any CWD works)
- `git` available on PATH for commit date lookups
- In CI, the checkout step needs `fetch-depth: 0` so `git log` sees full history for every file.
