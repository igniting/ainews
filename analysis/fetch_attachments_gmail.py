#!/usr/bin/env python3
"""Download email attachments from Gmail. Run this on your own machine.

WHY THIS EXISTS
---------------
The AI News archive was forwarded to a mailbox as 426 `.eml` files spread across
nine messages. Those attachments are the only complete copy of the newsletter's
human-written commentary for 2024-11 through 2026-01, and they cannot be read
through the Gmail connector this repository's analysis normally uses: that
connector returns roughly 1 MB of message body per call regardless of how much
is attached, which reaches about 10% of the issues, and it exposes no attachment
endpoint at all.

The Gmail REST API does expose one — `users.messages.attachments.get` — but it
needs a Google OAuth credential, which belongs on your machine and not in a
disposable cloud container. Hence a script you run yourself.

SETUP (about five minutes, once)
--------------------------------
1. https://console.cloud.google.com → create or pick a project.
2. APIs & Services → Library → enable **Gmail API**.
3. APIs & Services → OAuth consent screen → External → add yourself as a test
   user. No verification or review is needed for your own account.
4. Credentials → Create credentials → **OAuth client ID** → Desktop app →
   download the JSON as `credentials.json` next to this script.
5. pip install google-api-python-client google-auth-oauthlib

The scope requested is `gmail.readonly`. Nothing is sent anywhere; the script
only writes files to --out.

USAGE
-----
    python3 analysis/fetch_attachments_gmail.py \\
        --query 'subject:"[AINews] Part"' --out ainews-eml

    # anything matching a Gmail search works, e.g. a label:
    python3 analysis/fetch_attachments_gmail.py \\
        --query 'from:swyx+ainews@substack.com' --out ainews-eml

Then commit the directory (or hand it over however you like) and the analysis
scripts can read every issue at full fidelity:

    git add ainews-eml && git commit -m "add raw newsletter export"

PRIVACY
-------
Substack rewrites every link in a sent email with a `?j=` parameter identifying
the *subscriber*. `--strip-tokens` (on by default) removes it from `.eml` files
before they are written, so the export can be committed without publishing who
received it. Nothing else is altered.
"""

from __future__ import annotations

import argparse
import base64
import os
import pathlib
import re
import sys

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
# `?j=<base64>` on a Substack redirect identifies the recipient, not the link.
RECIPIENT_TOKEN = re.compile(rb"([?&])j=[A-Za-z0-9_.\-]+")
SAFE = re.compile(r"[^A-Za-z0-9 ._@()\[\]{}+,'-]")


def service():
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        sys.exit("pip install google-api-python-client google-auth-oauthlib")

    here = pathlib.Path(__file__).resolve().parent
    token, secrets = here / "token.json", here / "credentials.json"
    creds = Credentials.from_authorized_user_file(str(token), SCOPES) if token.exists() else None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not secrets.exists():
                sys.exit(f"missing {secrets} — see SETUP in this file's docstring")
            creds = InstalledAppFlow.from_client_secrets_file(str(secrets), SCOPES) \
                .run_local_server(port=0)
        token.write_text(creds.to_json())
        os.chmod(token, 0o600)
    return build("gmail", "v1", credentials=creds)


def walk(part, out):
    """Yield every (filename, attachment_id) in a payload, however nested."""
    if part.get("filename") and part.get("body", {}).get("attachmentId"):
        out.append((part["filename"], part["body"]["attachmentId"]))
    for child in part.get("parts", []) or []:
        walk(child, out)
    return out


def unique(dest: pathlib.Path) -> pathlib.Path:
    """`a.eml`, then `a (2).eml` — the archive has genuinely repeated subjects."""
    if not dest.exists():
        return dest
    stem, suffix, n = dest.stem, dest.suffix, 2
    while (cand := dest.with_name(f"{stem} ({n}){suffix}")).exists():
        n += 1
    return cand


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--query", required=True, help="Gmail search, e.g. 'subject:\"[AINews]\"'")
    ap.add_argument("--out", required=True, help="directory to write attachments into")
    ap.add_argument("--strip-tokens", action="store_true", default=True,
                    help="remove the per-recipient ?j= parameter (default on)")
    ap.add_argument("--keep-tokens", dest="strip_tokens", action="store_false")
    args = ap.parse_args(argv)

    api = service()
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    ids, page = [], None
    while True:
        r = api.users().messages().list(userId="me", q=args.query,
                                        pageToken=page, maxResults=500).execute()
        ids += [m["id"] for m in r.get("messages", [])]
        page = r.get("nextPageToken")
        if not page:
            break
    print(f"{len(ids)} messages match {args.query!r}", file=sys.stderr)

    written = skipped = 0
    for i, mid in enumerate(ids, 1):
        msg = api.users().messages().get(userId="me", id=mid, format="full").execute()
        found = walk(msg.get("payload", {}), [])
        for filename, aid in found:
            name = SAFE.sub("_", filename).strip() or f"{mid}-{aid[:8]}"
            dest = unique(out / name)
            blob = api.users().messages().attachments().get(
                userId="me", messageId=mid, id=aid).execute()
            data = base64.urlsafe_b64decode(blob["data"].encode())
            if args.strip_tokens:
                data = RECIPIENT_TOKEN.sub(rb"\1", data)
            dest.write_bytes(data)
            written += 1
        if not found:
            skipped += 1
        print(f"  [{i}/{len(ids)}] {len(found)} attachments", file=sys.stderr)

    print(f"\nwrote {written} attachments to {out}/ "
          f"({skipped} messages had none)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
