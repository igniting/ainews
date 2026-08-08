#!/usr/bin/env python3
"""Recover commentary and published subjects from raw `.eml` files.

The Gmail connector caps a message body at roughly 1 MB, which reached about
10% of a forwarded archive. Raw `.eml` files have no such limit, and they carry
two things the mirror lost: the human-written opening of each issue, and the
subject line it was actually published under.

The newsletter changed provider twice, so three HTML layouts appear:

    AI News <ainews@buttondown.email>     <h1 id="ai-twitter-recap">
    AINews <news@smol.ai>                 <h1 ...><span>AI Twitter Recap</span>
    AINews <swyx+ainews@substack.com>     <div class="body markup">

All three put the commentary before the first recap heading, with the standard
`AI News for 3/4/2025-3/5/2025` blockquote somewhere in it — sometimes above the
commentary, sometimes below. So the rule is the same everywhere: take everything
before the first recap heading, remove the header blockquote wherever it sits,
and strip the provider's chrome.

Issues are matched to `articles/` on recap text, not on dates, for the reasons
set out in `extract_commentary_gmail.py`: the in-issue date header goes stale and
the mirror's filenames are occasionally swapped.

Usage:
    python3 analysis/extract_commentary_eml.py --src ./eml --out /tmp/commentary
    python3 analysis/merge_commentary.py --src /tmp/commentary --write
"""

from __future__ import annotations

import argparse
import email
import email.utils
import pathlib
import re
import sys
from email import policy

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from extract_commentary_gmail import (  # noqa: E402
    BODY_START, HEADER_BQ, RECAP_H, RECIPIENT_LINK, RECIPIENT_TOKEN, TRACKING_PIXEL,
    article_fingerprints,
    carries_address, header_day, match_article, to_markdown,
)

REPO = pathlib.Path(__file__).resolve().parent.parent

# Provider chrome that sits above or below the commentary in the same region.
CHROME = [
    re.compile(r"^\s*view this post on the web at.*$", re.I | re.M),
    re.compile(r"^\s*read (this )?(online|in browser|on the web).*$", re.I | re.M),
    re.compile(r"^\s*this is a free preview.*$", re.I | re.M),
    re.compile(r"^\s*\[?AI ?News\]?\s*$", re.I | re.M),
    re.compile(r"^\s*(subscribe|unsubscribe|manage your subscription).*$", re.I | re.M),
    re.compile(r"^\s*\*?\*?table of contents\*?\*?\s*$", re.I | re.M),
    re.compile(r"^\s*\[TOC\]\s*$", re.M),
    re.compile(r"^\s*\[?view (in browser|this email in your browser)\]?.*$", re.I | re.M),
    re.compile(r"^\s*\[[^\]]{0,60}\]\(\s*\)\s*$", re.M),
    re.compile(r"^#{1,6}\s*\[?\[AINews\].*$", re.M),
]


def html_part(msg) -> str:
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            try:
                return part.get_content()
            except Exception:                                  # noqa: BLE001
                return ""
    return ""


def strip_chrome(text: str, subject: str) -> str:
    """Drop the provider's boilerplate and the subject echoed as a link."""
    for rx in CHROME:
        text = rx.sub("", text)
    # Providers pad and re-space the echoed subject, so compare on a whitespace-
    # insensitive form rather than the literal string.
    text = re.sub(r"[ \t\xa0]+", " ", text)
    bare = re.sub(r"\s+", " ", re.sub(r"^\[AINews\]\s*", "", subject)).strip()
    if bare:
        # every provider echoes the subject above the commentary, as a heading
        # (Substack) or as a link to the web copy (buttondown, smol.ai)
        esc = re.escape(bare[:60])
        text = re.sub(rf"^.{{0,80}}{esc}.{{0,6}}$", "", text, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def commentary(html: str, subject: str) -> str:
    body = TRACKING_PIXEL.sub("", html)
    body = RECIPIENT_LINK.sub("", body)
    body = RECIPIENT_TOKEN.sub(r"\1", body)
    stop = RECAP_H.search(body)
    if not stop:
        return ""
    region = body[:stop.start()]
    # Substack wraps the post proper in <div class="body markup">; everything above
    # it is the masthead, the echoed subject, the subtitle and the date line. The
    # other two providers have no such marker and need the regex sweep instead.
    start = BODY_START.search(region)
    if start:
        region = region[start.start():]
    return strip_chrome(to_markdown(HEADER_BQ.sub("", region)), subject)


def recap_html(html: str) -> str:
    m = RECAP_H.search(html)
    return html[m.start():] if m else ""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True, help="directory of .eml files (searched recursively)")
    ap.add_argument("--out", required=True, help="directory to write YY-MM-DD.md into")
    ap.add_argument("--articles", default=str(REPO / "articles"))
    ap.add_argument("--min-score", type=float, default=0.35)
    ap.add_argument("--min-ratio", type=float, default=1.5)
    ap.add_argument("--weak-score", type=float, default=0.15)
    args = ap.parse_args(argv)

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    arts = article_fingerprints(pathlib.Path(args.articles))

    picked: dict[str, tuple[int, float, str]] = {}
    subjects: dict[str, tuple[str, str, str]] = {}
    skipped = unmatched = 0

    for path in sorted(pathlib.Path(args.src).rglob("*.eml")):
        try:
            msg = email.message_from_bytes(path.read_bytes(), policy=policy.default)
        except Exception:                                      # noqa: BLE001
            skipped += 1
            continue
        subject = (msg.get("Subject") or "").replace("\n", " ").strip()
        if not subject.startswith("[AINews]"):
            skipped += 1                     # AIEWF dispatches, interviews, etc.
            continue
        html = html_part(msg)
        if not html or not RECAP_H.search(html):
            skipped += 1
            continue
        try:
            sent = email.utils.parsedate_to_datetime(msg.get("Date"))
        except Exception:                                      # noqa: BLE001
            skipped += 1
            continue

        guess = (sent - __import__("datetime").timedelta(hours=12)).date()
        day, score, runner = match_article(recap_html(html), guess, arts)
        agrees = bool(day) and day == guess.strftime("%y-%m-%d")
        confident = score >= args.min_score and score >= args.min_ratio * runner
        if not day or not (confident or (agrees and score >= args.weak_score)):
            unmatched += 1
            print(f"  ?? unmatched {sent.date()} {subject[:52]} "
                  f"(best {day or '-'} {score:.2f} vs {runner:.2f})", file=sys.stderr)
            continue

        sender = msg.get("From", "")
        provider = ("buttondown" if "buttondown" in sender else
                    "smol.ai" if "smol.ai" in sender else
                    "substack" if "substack" in sender else "other")
        text = commentary(html, subject)
        words = len(text.split())
        claimed = header_day(html)
        rendered = (
            f"<!-- source: eml {path.name} | sent: {sent.date()} | covers: 20{day} | "
            f"words: {words} | recap match {score:.2f}"
            + (f" | issue header claims 20{claimed}" if claimed and claimed != day else "")
            + f"\n     provider: {provider}\n     subject: {subject}\n-->\n\n{text}\n")
        if day in picked and picked[day][1] >= score:
            continue
        picked[day] = (words, score, rendered)
        subjects[day] = (str(sent.date()), subject, provider)

    # Nothing that could identify the recipient may reach disk, let alone a commit.
    # An address the newsletter itself published is not recipient data — the
    # 2024-12-31 issue prints an ad-sales contact — and the test for that is
    # simply whether it is already in the corpus we are adding to.
    corpus = "\n".join(f.read_text(encoding="utf-8", errors="replace")
                       for f in pathlib.Path(args.articles).glob("*.md"))
    leaked = {}
    for d, (_, _, r) in picked.items():
        found = carries_address(r)
        if found and found.split(" (")[0] not in corpus:
            leaked[d] = found
    if leaked:
        for d, what in sorted(leaked.items())[:5]:
            print(f"  !! {d} still carries {what}", file=sys.stderr)
        print(f"REFUSING to write: {len(leaked)} issues carry recipient data",
              file=sys.stderr)
        return 1

    for day, (_, _, rendered) in picked.items():
        (out / f"{day}.md").write_text(rendered, encoding="utf-8")
    (out / "subjects.tsv").write_text(
        "covers\tsent\tsubject\tprovider\n" + "".join(
            f"20{d}\t{s}\t{sub}\t{fr}\n" for d, (s, sub, fr) in sorted(subjects.items())),
        encoding="utf-8")

    total = sum(w for w, _, _ in picked.values())
    days = sorted(picked)
    print(f"wrote {len(picked)} issues to {out} · {total:,} commentary words · "
          f"{skipped} skipped · {unmatched} unmatched"
          + (f" · span 20{days[0]}..20{days[-1]}" if days else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
