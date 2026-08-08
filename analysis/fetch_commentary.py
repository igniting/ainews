#!/usr/bin/env python3
"""Fetch the human commentary that the GitHub mirror is missing, from Substack.

WHY THIS EXISTS
---------------
Each issue of AI News opens with commentary written by a person, before any
machine-generated recap. Our corpus in `articles/` has that commentary for
2023-2025, but for 2026 the upstream mirror (smol-ai/ainews-web-2025) carries
only the boilerplate line `**a quiet day.**` — 104 of 152 issues. The sent
email and the Substack post both carry the real commentary; the mirror does
not. Verified: all 363 files in the mirror's `buttondown-emails/` are
byte-identical to ours, so nothing is being lost on our side.

This script closes that gap. It cannot run in the sandbox that produced the
book — news.smol.ai, swyx.substack.com and www.latent.space are all refused by
the egress proxy with 403 CONNECT — so run it somewhere with normal network
access and commit the result.

WHAT IT DOES
------------
1. Pages Substack's public archive JSON for the publication.
2. Keeps posts whose slug looks like an AI News issue.
3. Fetches each post and pulls the HTML body.
4. Cuts everything before the first "AI Twitter/Reddit/Discord Recap" heading —
   that prefix is the commentary — and converts it to markdown-ish text.
5. Writes one file per issue into `--out`, named by the covered day, so
   `merge_commentary.py` can splice them into `articles/` without touching the
   recaps.

Paid posts return truncated bodies for anonymous callers. If the run reports
many short results, pass a subscriber cookie with --cookie; get it from your
browser's devtools (Application -> Cookies -> substack.sid).

Usage:
    python3 analysis/fetch_commentary.py --pub www.latent.space --out /tmp/commentary
    python3 analysis/fetch_commentary.py --pub www.latent.space --out /tmp/commentary \\
        --since 2026-01-01 --cookie "substack.sid=..."
"""

from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

ARCHIVE = "https://{pub}/api/v1/archive?sort=new&search=&offset={offset}&limit={limit}"
POST = "https://{pub}/api/v1/posts/{slug}"
UA = "Mozilla/5.0 (compatible; ainews-commentary-fetch/1.0)"

# Slugs of AI News issues look like "ainews-<something>"; the newsletter has
# used a couple of prefixes over its life.
ISSUE_SLUG = re.compile(r"^(ainews|ai-news)[-_]", re.I)
RECAP_H = re.compile(r"<h[12][^>]*>\s*(?:<[^>]+>\s*)*AI\s+(?:Twitter|Reddit|Discord)\s+Recap",
                     re.I)


def get(url: str, cookie: str | None, retries: int = 3) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    if cookie:
        req.add_header("Cookie", cookie)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < retries - 1:
                time.sleep(2 ** attempt * 3)
                continue
            raise
        except urllib.error.URLError:
            if attempt < retries - 1:
                time.sleep(2 ** attempt * 3)
                continue
            raise
    raise RuntimeError("unreachable")


def to_text(fragment: str) -> str:
    """HTML -> readable markdown-ish text, keeping links and emphasis."""
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", fragment, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</(p|div|h[1-6]|li|blockquote)>", "\n\n", s, flags=re.I)
    s = re.sub(r"<li[^>]*>", "- ", s, flags=re.I)
    s = re.sub(r"<a[^>]+href=\"([^\"]+)\"[^>]*>(.*?)</a>", r"[\2](\1)", s, flags=re.S | re.I)
    s = re.sub(r"<(strong|b)>(.*?)</\1>", r"**\2**", s, flags=re.S | re.I)
    s = re.sub(r"<(em|i)>(.*?)</\1>", r"*\2*", s, flags=re.S | re.I)
    s = re.sub(r"<img[^>]*alt=\"([^\"]*)\"[^>]*>", r"![\1]()", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def commentary(body_html: str) -> str:
    """Everything before the first recap heading."""
    m = RECAP_H.search(body_html)
    return to_text(body_html[:m.start()] if m else body_html)


def covered_day(post: dict) -> str:
    """The issue covers the day before it was sent; the header says so, but the
    post date is the reliable field. Return YY-MM-DD of the day covered."""
    import datetime as dt
    iso = (post.get("post_date") or post.get("published_at") or "")[:10]
    if not iso:
        return ""
    d = dt.date.fromisoformat(iso) - dt.timedelta(days=1)
    return d.strftime("%y-%m-%d")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pub", required=True, help="publication host, e.g. www.latent.space")
    ap.add_argument("--out", required=True, help="directory to write commentary files into")
    ap.add_argument("--since", default="2026-01-01", help="only posts on/after this date")
    ap.add_argument("--limit", type=int, default=50, help="archive page size (Substack caps at 50)")
    ap.add_argument("--cookie", default=None, help="subscriber cookie, if posts are gated")
    ap.add_argument("--sleep", type=float, default=1.0, help="seconds between post fetches")
    args = ap.parse_args(argv)

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    slugs: list[dict] = []
    offset = 0
    while True:
        url = ARCHIVE.format(pub=args.pub, offset=offset, limit=args.limit)
        page = json.loads(get(url, args.cookie))
        if not page:
            break
        for p in page:
            if (p.get("post_date") or "")[:10] < args.since:
                page = []          # archive is newest-first; we have gone past the window
                break
            if ISSUE_SLUG.match(p.get("slug", "")):
                slugs.append(p)
        if not page:
            break
        offset += args.limit
        print(f"  archive: {offset} scanned, {len(slugs)} issues matched", file=sys.stderr)
        time.sleep(args.sleep)

    print(f"{len(slugs)} issues to fetch", file=sys.stderr)
    written = short = 0
    for p in slugs:
        day = covered_day(p)
        if not day:
            continue
        dest = out / f"{day}.md"
        if dest.exists():
            continue
        try:
            full = json.loads(get(POST.format(pub=args.pub, slug=p["slug"]), args.cookie))
        except Exception as e:                                   # noqa: BLE001
            print(f"  !! {p['slug']}: {e}", file=sys.stderr)
            continue
        body = full.get("body_html") or ""
        text = commentary(body)
        words = len(text.split())
        if words < 30:
            short += 1
        dest.write_text(
            f"<!-- slug: {p['slug']} | sent: {(p.get('post_date') or '')[:10]} | "
            f"covers: 20{day} | words: {words} -->\n\n{text}\n", encoding="utf-8")
        written += 1
        time.sleep(args.sleep)

    print(f"wrote {written} files to {out}", file=sys.stderr)
    if short:
        print(f"WARNING: {short} had under 30 words of commentary — if that is most of them, "
              f"the bodies are probably gated; retry with --cookie", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
