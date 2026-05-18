# Fetch Zoom Transcript

Pulls the VTT transcript of a CSOH meeting from your Zoom cloud recording, ready to hand to Claude (or another summarizer) for turning into a [`meetings.html`](../meetings.html) entry via [`add_meeting.py`](add_meeting.py).

## One-time setup

### 1. Create the Server-to-Server OAuth app

1. Go to <https://marketplace.zoom.us/develop/create> → **Build App** → **Server-to-Server OAuth**.
2. Give it a name (e.g. `CSOH Transcript Fetcher`).
3. Under **App Credentials** note the **Account ID**, **Client ID**, and **Client Secret**.
4. Under **Scopes**, add (minimum). Zoom migrated to granular scopes - use these exact names:
   - `cloud_recording:read:list_user_recordings` - list a user's cloud recordings (VTT transcripts tied to recordings)
   - `cloud_recording:read:recording` - read a specific recording's metadata/files
   - `user:read:user` - identify "me" (may show as `user:read` in older UIs)
   - `meeting:read:list_summaries:admin` - list AI Companion meeting summaries across the account (optional, needed only for summary backfill)
   - `meeting:read:list_meetings:admin` - list past meetings across the account (optional, pairs with the above)
   - `meeting:read:summary:admin` - fetch the full text of a meeting summary (optional, needed only for summary backfill)
5. Under **Activation**, click **Activate your app**.

### 2. Store the credentials

Copy `.env.example` to `.env` at the repo root and fill in the three values:

```bash
cp .env.example .env
# edit .env with your Account ID, Client ID, Client Secret
```

`.env` is gitignored - don't commit it.

### 3. Confirm Zoom has cloud recording + auto-transcription enabled

On Zoom → Settings → Recording:

- **Cloud recording** → on
- **Audio transcript** → on (this is what generates the VTT this tool downloads)

Transcripts appear a few minutes to a few hours after the meeting ends, not instantly.

## Usage

### List what's available

```bash
python3 tools/fetch_zoom_transcript.py --list
```

Shows every recording in the last 14 days, whether it has a transcript, duration, and meeting ID.

### Fetch the most recent one

```bash
python3 tools/fetch_zoom_transcript.py --last
```

Downloads to `/tmp/csoh-YYYY-MM-DD-transcript.vtt` and prints `OUTPUT=…` + meeting metadata.

### Fetch a specific date

```bash
python3 tools/fetch_zoom_transcript.py --date 2026-04-24
```

### Other flags

- `--days-back N` - widen the search window (default 14).
- `--output /path/to/file.vtt` - override the output path.
- `--user-id SOMEONE` - fetch a different user's recordings. Default `me` uses the S2S app's owner, i.e. **the Zoom account that created the app**.
- `--env-file /path/to/.env` - use a non-default `.env` location.

## End-to-end workflow (Saturday morning)

Inside a Claude Code session, just say something like:

> Pull last Friday's Zoom transcript and publish it to meetings.html.

Claude runs:

1. `python3 tools/fetch_zoom_transcript.py --last` → VTT file + meeting metadata.
2. Reads the VTT.
3. Writes a CSOH-style markdown recap (Quick recap + topic sections) to `/tmp/csoh-YYYY-MM-DD.md`.
4. Proposes `--tag` values from the existing tag vocabulary and runs `python3 tools/add_meeting.py /tmp/csoh-YYYY-MM-DD.md --tag …`.
5. Shows you the diff for review before commit.

If you prefer to run it by hand, stop after step 1 and paste the VTT into a chat for summarization.

## Troubleshooting

| Problem | Cause / Fix |
|---|---|
| `Missing env vars: ZOOM_*` | `.env` not present at repo root, or values blank. Run `cp .env.example .env` and fill in. |
| `Zoom OAuth failed: HTTP 400 invalid_request` | Account ID, Client ID, or Client Secret mismatch. Copy-paste from the app settings page again. |
| `Zoom OAuth failed: HTTP 400 unsupported_grant_type` | The app isn't **activated**. Go back to the Zoom Marketplace app settings and click Activate. |
| `HTTP 403` on recordings list | Missing scope. Add `recording:read` to the app and re-activate. |
| `No recording with a transcript found for YYYY-MM-DD` | Either the meeting wasn't cloud-recorded, transcription is off, or Zoom hasn't finished processing it. Try again later or run `--list` to see what's actually available. |
| `Selected meeting has no transcript file` | Transcription toggle was off for that specific meeting. Nothing to do retroactively - Zoom only transcribes during recording. |

## Requirements

- Python 3.9+ (standard library only - no `pip install` needed)
- A Zoom plan that supports cloud recording and audio transcription (Pro or higher)
