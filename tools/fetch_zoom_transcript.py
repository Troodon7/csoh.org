#!/usr/bin/env python3
"""Fetch a CSOH meeting transcript from Zoom cloud recordings.

Uses a Server-to-Server OAuth app (account-level). Credentials come from
environment variables, optionally loaded from a `.env` file at the repo root:

    ZOOM_ACCOUNT_ID=...
    ZOOM_CLIENT_ID=...
    ZOOM_CLIENT_SECRET=...

Usage:

    # Most recent transcript across the last 14 days
    python3 tools/fetch_zoom_transcript.py --last

    # Specific date
    python3 tools/fetch_zoom_transcript.py --date 2026-04-24

    # List what's available without downloading
    python3 tools/fetch_zoom_transcript.py --list

    # Override the output path
    python3 tools/fetch_zoom_transcript.py --last --output /tmp/x.vtt

By default transcripts land at `/tmp/csoh-YYYY-MM-DD-transcript.vtt`. On
success the script prints one machine-readable line per key:

    OUTPUT=/tmp/csoh-2026-04-24-transcript.vtt
    MEETING_DATE=2026-04-24
    MEETING_TOPIC=Cloud Security Office Hours
    MEETING_DURATION_MIN=62
    MEETING_ID=87654321098

so a calling process (or Claude) can easily pick up the next steps.

Required Zoom app scopes: `recording:read`, `user:read`, `meeting:read`.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ZOOM_API_BASE = "https://api.zoom.us/v2"
ZOOM_OAUTH_URL = "https://zoom.us/oauth/token"

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_dotenv(path: Path) -> None:
    """Populate os.environ from a KEY=VALUE file. Silent if missing."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, _, v = s.partition("=")
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        # Don't override already-set env vars.
        os.environ.setdefault(k, v)


def get_access_token(account_id: str, client_id: str, client_secret: str) -> str:
    creds = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    body = urllib.parse.urlencode({
        "grant_type": "account_credentials",
        "account_id": account_id,
    }).encode()
    req = urllib.request.Request(
        ZOOM_OAUTH_URL,
        data=body,
        headers={
            "Authorization": f"Basic {creds}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return data["access_token"]


def api_get(path: str, token: str, params: dict | None = None) -> dict:
    url = f"{ZOOM_API_BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def list_recordings(token: str, user_id: str, start: dt.date, end: dt.date) -> list[dict]:
    data = api_get(
        f"/users/{user_id}/recordings",
        token,
        params={"from": start.isoformat(), "to": end.isoformat(), "page_size": 50},
    )
    return data.get("meetings", [])


def transcript_file(meeting: dict) -> dict | None:
    """Return the best transcript file for a meeting, or None."""
    candidates = []
    for f in meeting.get("recording_files", []):
        if f.get("file_type") == "TRANSCRIPT" or f.get("file_extension", "").upper() == "VTT":
            candidates.append(f)
    if not candidates:
        return None
    # Prefer TRANSCRIPT file_type; fall back to whatever VTT.
    candidates.sort(key=lambda f: 0 if f.get("file_type") == "TRANSCRIPT" else 1)
    return candidates[0]


def download_file(url: str, token: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def find_for_date(meetings: list[dict], target: dt.date) -> dict | None:
    for m in meetings:
        start = m.get("start_time", "")
        if start[:10] == target.isoformat() and transcript_file(m):
            return m
    return None


def find_most_recent(meetings: list[dict]) -> dict | None:
    meetings_with_transcript = [m for m in meetings if transcript_file(m)]
    if not meetings_with_transcript:
        return None
    return sorted(meetings_with_transcript, key=lambda m: m.get("start_time", ""), reverse=True)[0]


def print_listing(meetings: list[dict]) -> None:
    if not meetings:
        print("No recordings in range.", file=sys.stderr)
        return
    print("Recordings in range (most recent first):")
    for m in sorted(meetings, key=lambda m: m.get("start_time", ""), reverse=True):
        has_vtt = transcript_file(m) is not None
        tag = "transcript ✓" if has_vtt else "no transcript"
        topic = m.get("topic", "").replace("\n", " ").strip() or "(untitled)"
        print(
            f"  {m.get('start_time', '')[:16]}  {tag:14}  "
            f"{m.get('duration', 0):>3}min  {topic}  [id={m.get('id')}]"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch a CSOH meeting transcript from Zoom.")
    parser.add_argument("--date", type=str, help="Meeting date YYYY-MM-DD.")
    parser.add_argument("--last", action="store_true", help="Use most recent recording with a transcript.")
    parser.add_argument("--list", action="store_true", dest="list_only", help="List recordings in range without downloading.")
    parser.add_argument("--days-back", type=int, default=14, help="How many days back to search (default 14).")
    parser.add_argument("--output", type=Path, help="Output file path (default /tmp/csoh-DATE-transcript.vtt).")
    parser.add_argument("--user-id", type=str, default="me", help="Zoom user ID (default: me = the S2S app's owner).")
    parser.add_argument("--env-file", type=Path, default=REPO_ROOT / ".env", help="Path to a .env file (default: repo .env).")
    args = parser.parse_args()

    load_dotenv(args.env_file)

    account_id = os.environ.get("ZOOM_ACCOUNT_ID")
    client_id = os.environ.get("ZOOM_CLIENT_ID")
    client_secret = os.environ.get("ZOOM_CLIENT_SECRET")
    missing = [
        n for n, v in [
            ("ZOOM_ACCOUNT_ID", account_id),
            ("ZOOM_CLIENT_ID", client_id),
            ("ZOOM_CLIENT_SECRET", client_secret),
        ] if not v
    ]
    if missing:
        print(f"Missing env vars: {', '.join(missing)}", file=sys.stderr)
        print(f"Set them in {args.env_file} or export them in your shell.", file=sys.stderr)
        return 1

    try:
        token = get_access_token(account_id, client_id, client_secret)
    except urllib.error.HTTPError as exc:
        print(f"Zoom OAuth failed: HTTP {exc.code} {exc.reason}", file=sys.stderr)
        try:
            body = exc.read().decode()
            print(body, file=sys.stderr)
        except Exception:
            pass
        return 1

    today = dt.date.today()
    start_date = today - dt.timedelta(days=args.days_back)
    if args.date:
        try:
            target = dt.date.fromisoformat(args.date)
        except ValueError:
            print("Invalid --date, expected YYYY-MM-DD.", file=sys.stderr)
            return 1
        start_date = min(start_date, target)
        end_date = max(today, target)
    else:
        end_date = today

    try:
        meetings = list_recordings(token, args.user_id, start_date, end_date)
    except urllib.error.HTTPError as exc:
        print(f"Zoom recordings list failed: HTTP {exc.code} {exc.reason}", file=sys.stderr)
        try:
            print(exc.read().decode(), file=sys.stderr)
        except Exception:
            pass
        return 1

    if args.list_only:
        print_listing(meetings)
        return 0

    if args.date:
        meeting = find_for_date(meetings, dt.date.fromisoformat(args.date))
        if not meeting:
            print(f"No recording with a transcript found for {args.date}.", file=sys.stderr)
            print("Try --list to see what's available, or --days-back to widen the search window.", file=sys.stderr)
            return 1
    else:
        meeting = find_most_recent(meetings)
        if not meeting:
            print("No recordings with transcripts in the search window.", file=sys.stderr)
            print("Try --list or --days-back to widen the window.", file=sys.stderr)
            return 1

    transcript = transcript_file(meeting)
    if not transcript:
        print("Selected meeting has no transcript file.", file=sys.stderr)
        return 1

    start_iso = meeting.get("start_time", "")
    date_str = start_iso[:10] if start_iso else "unknown"
    download_url = transcript.get("download_url")
    if not download_url:
        print("Transcript file has no download_url.", file=sys.stderr)
        return 1

    try:
        content = download_file(download_url, token)
    except urllib.error.HTTPError as exc:
        print(f"Transcript download failed: HTTP {exc.code} {exc.reason}", file=sys.stderr)
        return 1

    out = args.output or Path(f"/tmp/csoh-{date_str}-transcript.vtt")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(content)

    # Machine-readable summary for downstream callers.
    print(f"OUTPUT={out}")
    print(f"MEETING_DATE={date_str}")
    print(f"MEETING_TOPIC={meeting.get('topic', '').strip()}")
    print(f"MEETING_DURATION_MIN={meeting.get('duration', 0)}")
    print(f"MEETING_ID={meeting.get('id', '')}")
    print(f"TRANSCRIPT_BYTES={len(content)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
