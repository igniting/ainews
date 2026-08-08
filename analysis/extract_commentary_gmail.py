#!/usr/bin/env python3
"""Recover the human commentary from the sent AI News emails.

WHY THIS EXISTS
---------------
Every issue of AI News opens with commentary written by a person, before any
machine-generated recap begins. Our corpus in `articles/` carries that
commentary for 2023 through most of 2025, but the upstream mirror degrades:
from March 2026 the pre-recap section is the boilerplate line `**a quiet
day.**` on 104 of 152 issues, and the stored `title` field collapses to "not
much happened today".

The sent email does not degrade. It carries the full commentary, a subtitle
that never made it into the mirror at all, and the real published subject
line. This script reconstructs the editorial layer from those emails.

WHAT IT READS
-------------
JSON dumps of Gmail messages, one per file, each an object with at least
`htmlBody`, `subject` and `date` — the shape returned by the Gmail MCP
`get_message` tool. Point `--src` at a directory of them; filenames are
ignored, the message id inside is used.

WHAT IT WRITES
--------------
One `YY-MM-DD.md` per issue into `--out`, named for the article in `articles/`
that the issue *is*, ready for `merge_commentary.py`, plus a `subjects.tsv` of
the published subject lines and subtitles.

Naming that file is the hard part, because neither date on offer is reliable.
The issue's own `AI News for 8/4/2026-8/5/2026` header goes stale — four
consecutive issues in late March 2026 all claim to cover 3/23-3/24. The send
timestamp is better but not authoritative either: the mirror files the
2026-04-07 "Anthropic @ $30B ARR" issue as `26-04-06` and the 2026-04-06
"Gemma 4" issue as `26-04-07`, swapping the pair. So the join is made on
content — the recaps are the same words in the email and in the article, and
comparing them identifies the issue outright. The send date, shifted into US
Pacific, only narrows the candidates and corroborates a weak match.

LINKS AND PRIVACY
-----------------
Substack rewrites every outbound link in the email as a `substack.com/redirect`
URL carrying a `?j=` parameter, and that parameter identifies the *recipient* —
it decodes to a subscriber id, identical on all 1,384 links in one mailbox. It
is stripped here, before anything is written, so that recovered commentary can
be committed without publishing who received it. The redirect path itself is
per-link, not per-reader, and is kept so the citations still resolve; resolving
them further would mean 20-odd HTTP requests per issue to a host this repo does
not need. Image sources are recovered from Substack's `data-attrs` blob, which
carries the original S3 URL rather than the CDN resize wrapper.

Nothing else in an email is retained: no headers, no recipient address, no
message body outside the published post, and no Gmail message id in the article.

Usage:
    python3 analysis/extract_commentary_gmail.py --src /tmp/gmail --out /tmp/commentary
    python3 analysis/merge_commentary.py --src /tmp/commentary --write
    python3 analysis/methods/editorial.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent

# The post body proper; everything before it is Substack's email chrome.
BODY_START = re.compile(r'<div class="body markup"', re.I)
# The editorial subtitle, which the GitHub mirror drops entirely.
SUBTITLE = re.compile(r'<h3 class="subtitle[^"]*"[^>]*>(.*?)</h3>', re.I | re.S)
# The standard "AI News for 8/4/2026-8/5/2026. We checked N subreddits..." blockquote.
# It names the days covered, and it is NOT a reliable end marker: on most issues the
# commentary runs above it, but on the ones that open "a quiet day lets us..." the
# blockquote comes first and several hundred words of commentary follow it. So it is
# excised wherever it sits rather than used as a cut point.
HEADER_BQ = re.compile(
    r"<blockquote[^>]*>(?:(?!</blockquote>).)*?AI News for.*?</blockquote>", re.I | re.S)
RECAP_H = re.compile(r"<h[12][^>]*>\s*(?:<[^>]+>\s*)*AI\s+(?:Twitter|Reddit|Discord)\s+Recap",
                     re.I)
COVERS = re.compile(r"AI News for\s*(\d{1,2})/(\d{1,2})/(\d{4})\s*[-–—]\s*"
                    r"(\d{1,2})/(\d{1,2})/(\d{4})", re.I)
# Substack stores the unresized original in a JSON blob on the img tag.
DATA_ATTRS = re.compile(r'data-attrs="([^"]*)"', re.I)
# `?j=<base64>` on a redirect link identifies the subscriber who was sent the
# email, not the link. It is removed from every URL before anything is written.
RECIPIENT_TOKEN = re.compile(r"([?&]amp;|[?&])j=[A-Za-z0-9_.\-]+")
# Quoted tweets are the editor's evidence, so they are kept as quotations rather
# than flattened into a link. Substack renders them as a nest of tables.
TWEET = re.compile(r'<table[^>]*data-component-name="Tweet[^"]*"[^>]*>', re.I)


def element_end(s: str, start: int, tag: str) -> int:
    """Index just past the element opened at `start`, honouring nesting."""
    depth = 0
    for m in re.finditer(rf"</?{tag}\b[^>]*>", s[start:]):
        depth += -1 if m.group(0).startswith("</") else 1
        if depth == 0:
            return start + m.end()
    return len(s)


def tweet(block: str) -> str:
    """A Substack tweet embed as a markdown blockquote: author, then the text."""
    href = re.search(r'<a\b[^>]*\shref="([^"]+)"', block, re.I)
    flat = re.sub(r"<img\b[^>]*>", "", block, flags=re.I)
    flat = re.sub(r"</(div|td|tr|table|p)>", "\n", flat, flags=re.I)
    lines = [html.unescape(ln).strip()
             for ln in re.sub(r"<[^>]+>", "", flat).split("\n")]
    lines = [ln for ln in lines if ln]
    if not lines:
        return ""
    handle = next((ln for ln in lines if ln.startswith("@") and " " not in ln), "")
    meta = next((ln for ln in lines if "·" in ln), "")
    skip = {handle, meta, lines[0]}
    text = max((ln for ln in lines if ln not in skip and "Replies" not in ln),
               key=len, default="")
    who = f"**{lines[0]}**" + (f" ({handle})" if handle else "")
    head = f"{who} — [{meta}]({href.group(1)})" if meta and href else who
    body = "\n".join("> " + ln for ln in text.split("\n"))
    return f"\n\n> {head}\n>\n{body}\n\n" if text else f"\n\n> {head}\n\n"


def unwrap_tweets(s: str) -> str:
    out, pos = [], 0
    while True:
        m = TWEET.search(s, pos)
        if not m:
            break
        end = element_end(s, m.start(), "table")
        out.append(s[pos:m.start()])
        out.append(tweet(s[m.start():end]))
        pos = end
    out.append(s[pos:])
    return "".join(out)


def sent_day(sent: str) -> dt.date:
    """The day an issue covers, estimated from when it was sent.

    Issues go out on the evening of the day they cover, US Pacific: observed send
    times run from 22:00 UTC through 08:50 UTC the next morning. Shifting back
    twelve hours puts that whole window on one day, which across the 134 issues
    here gives 134 distinct days with no collisions. It is only an estimate — see
    `match_article` for why the join is made on content instead.
    """
    return (dt.datetime.fromisoformat(sent.replace("Z", "+00:00"))
            - dt.timedelta(hours=12)).date()


def header_day(body_html: str) -> str:
    """`YY-MM-DD` the issue claims to cover. Frequently stale: four consecutive
    issues in late March 2026 all claim 3/23-3/24, and the 2026-08-04 issue
    titled "Qwen 3.8 Max" claims 7/25-7/27. Reported, never trusted."""
    m = COVERS.search(re.sub(r"<[^>]+>", "", body_html[:200000]))
    if not m:
        return ""
    return f"{m.group(6)[2:]}-{int(m.group(4)):02d}-{int(m.group(5)):02d}"


TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9._-]{5,}")


def fingerprint(text: str) -> set[str]:
    """Distinctive tokens from an issue's recaps, used to identify the issue."""
    return set(TOKEN.findall(re.sub(r"https?://\S+", " ", text).lower()))


def article_fingerprints(articles: pathlib.Path) -> dict[str, set[str]]:
    md_recap = re.compile(r"^#\s+AI (Twitter|Reddit|Discord) Recap", re.M | re.I)
    front = re.compile(r"\A---\n.*?\n---\n", re.S)
    out: dict[str, set[str]] = {}
    for p in sorted(articles.glob("*.md")):
        body = front.sub("", p.read_text(encoding="utf-8", errors="replace"))
        m = md_recap.search(body)
        if m:
            out[p.name[:8]] = fingerprint(body[m.start():m.start() + 40000])
    return out


def match_article(body_html: str, guess: dt.date, arts: dict[str, set[str]],
                  window: int = 4) -> tuple[str, float, float]:
    """Find the article this issue *is*, by comparing recap text.

    Neither the send date nor the issue's own header reliably names the article:
    the mirror files the 2026-04-07 "Anthropic @ $30B ARR" issue as `26-04-06`
    and the 2026-04-06 "Gemma 4" issue as `26-04-07`, swapping the pair. The
    recaps, however, are the same words on both sides, so comparing them
    identifies the issue outright — that swap scores 0.84 and 0.59 against
    runners-up of 0.23 and 0.15.

    Returns (day, score, runner_up_score); day is "" when nothing matches well.
    """
    m = RECAP_H.search(body_html)
    if not m:
        return "", 0.0, 0.0
    mine = fingerprint(re.sub(r"<[^>]+>", " ", body_html[m.start():m.start() + 90000]))
    scored = []
    for off in range(-window, window + 1):
        key = (guess + dt.timedelta(days=off)).strftime("%y-%m-%d")
        if key in arts:
            other = arts[key]
            scored.append((len(mine & other) / max(len(mine | other), 1), key))
    if not scored:
        return "", 0.0, 0.0
    scored.sort(reverse=True)
    top, runner = scored[0], (scored[1] if len(scored) > 1 else (0.0, ""))
    return top[1], top[0], runner[0]


def image(tag: str) -> str:
    """Markdown image from a Substack <img>, preferring the original source."""
    src, alt = "", ""
    blob = DATA_ATTRS.search(tag)
    if blob:
        try:
            d = json.loads(html.unescape(blob.group(1)))
            src, alt = d.get("src") or "", d.get("alt") or ""
        except (ValueError, AttributeError):
            pass
    if not src:
        m = re.search(r'\ssrc="([^"]+)"', tag)
        src = m.group(1) if m else ""
    return f"![{alt}]({src})" if src else ""


def to_markdown(fragment: str) -> str:
    """HTML -> markdown, keeping the structure the commentary actually uses:
    paragraphs, headings, lists, blockquotes, links, emphasis and images."""
    s = RECIPIENT_TOKEN.sub("", fragment)
    s = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", "", s, flags=re.S | re.I)
    s = unwrap_tweets(s)
    s = re.sub(r"<img\b[^>]*>", lambda m: "\n\n" + image(m.group(0)) + "\n\n", s, flags=re.I)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    for n in range(1, 7):
        s = re.sub(rf"<h{n}\b[^>]*>(.*?)</h{n}>", rf"\n\n{'#' * n} \1\n\n", s,
                   flags=re.S | re.I)
    s = re.sub(r"<blockquote\b[^>]*>(.*?)</blockquote>", lambda m: quote(m.group(1)), s,
               flags=re.S | re.I)
    s = re.sub(r"<li\b[^>]*>(.*?)</li>", r"\n- \1", s, flags=re.S | re.I)
    s = re.sub(r"<a\b[^>]*\shref=\"([^\"]+)\"[^>]*>(.*?)</a>", r"[\2](\1)", s,
               flags=re.S | re.I)
    s = re.sub(r"<(strong|b)\b[^>]*>(.*?)</\1>", r"**\2**", s, flags=re.S | re.I)
    s = re.sub(r"<(em|i)\b[^>]*>(.*?)</\1>", r"*\2*", s, flags=re.S | re.I)
    s = re.sub(r"</(p|div|figure|table|tr|ul|ol)>", "\n\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = s.replace(" ", " ").replace("͏", "").replace(" ", "")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\*\*\s*\*\*", "", s)          # emphasis left empty by a stripped tag
    s = re.sub(r"!\[\s*\]\(\s*\)", "", s)      # an image whose source did not survive
    # A linked image arrives as [ \n\n ![](src) \n\n ](href); put it back on one line.
    s = re.sub(r"\[\s*(!\[[^\]]*\]\([^)]*\))\s*\]\(([^)]*)\)", r"[\1](\2)", s)
    while True:                                # a link with nothing left to click on,
        t = re.sub(r"(?<!!)\[\s*\]\([^)]*\)", "", s)  # possibly nested a few deep
        if t == s:
            break
        s = t
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def quote(inner: str) -> str:
    text = to_markdown(inner)
    return "\n\n" + "\n".join("> " + ln if ln else ">" for ln in text.split("\n")) + "\n\n"


def commentary(body_html: str) -> str:
    """The human-written opening: everything in the post body before the first recap
    heading, less the standard header blockquote the article already carries."""
    start = BODY_START.search(body_html)
    if not start:
        return ""
    tail = body_html[start.start():]
    stop = RECAP_H.search(tail)
    return to_markdown(HEADER_BQ.sub("", tail[:stop.start()] if stop else tail))


def subtitle(body_html: str) -> str:
    m = SUBTITLE.search(body_html)
    return to_markdown(m.group(1)) if m else ""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True, help="directory of Gmail message JSON dumps")
    ap.add_argument("--out", required=True, help="directory to write YY-MM-DD.md into")
    ap.add_argument("--articles", default=str(REPO / "articles"),
                    help="corpus the issues are matched against")
    ap.add_argument("--min-score", type=float, default=0.35,
                    help="lowest recap overlap accepted as an identification")
    ap.add_argument("--min-ratio", type=float, default=1.5,
                    help="how far the best match must beat the runner-up")
    ap.add_argument("--weak-score", type=float, default=0.15,
                    help="lowest overlap accepted when the send date agrees anyway")
    ap.add_argument("--min-words", type=int, default=15,
                    help="report, but still write, issues shorter than this")
    args = ap.parse_args(argv)

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    arts = article_fingerprints(pathlib.Path(args.articles))

    # day -> (words, score, rendered file text), so a contested day keeps the better match
    picked: dict[str, tuple[int, float, str]] = {}
    subjects: dict[str, tuple[str, str, str]] = {}
    short = stale = moved = unmatched = 0
    for path in sorted(pathlib.Path(args.src).iterdir()):
        if not path.is_file():
            continue
        try:
            msg = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        except ValueError:
            continue
        body = msg.get("htmlBody") or ""
        subject = (msg.get("subject") or "").strip()
        sent = msg.get("date") or ""
        if not body or not sent or not subject.startswith("[AINews]"):
            continue

        guess = sent_day(sent)
        day, score, runner = match_article(body, guess, arts)
        # Confident on its own, or merely the best of a weak field but corroborated
        # by the send date — two independent signals agreeing is enough. Some issues
        # carry short recaps, which drags every overlap down without making the
        # identification wrong (26-04-23 "GPT 5.5" tops out at 0.29).
        agrees = bool(day) and day == guess.strftime("%y-%m-%d")
        confident = score >= args.min_score and score >= args.min_ratio * runner
        if not day or not (confident or (agrees and score >= args.weak_score)):
            unmatched += 1
            print(f"  ?? no article matches {subject[:52]} (sent {sent[:10]}, "
                  f"best {day or '-'} {score:.2f} vs {runner:.2f})", file=sys.stderr)
            continue
        if day != guess.strftime("%y-%m-%d"):
            moved += 1
        claimed = header_day(body)
        if claimed and claimed != day:
            stale += 1

        text = commentary(body)
        words = len(text.split())
        if words < args.min_words:
            short += 1
            print(f"  .. {day} only {words}w: {subject[:56]}", file=sys.stderr)
        rendered = (
            f"<!-- source: gmail {msg.get('id', '')} | sent: {sent[:10]} | "
            f"covers: 20{day} | words: {words} | recap match {score:.2f}"
            + (f" | issue header claims 20{claimed}" if claimed and claimed != day else "")
            + f"\n     subject: {subject}\n     subtitle: {subtitle(body)}\n-->\n\n{text}\n")
        if day in picked and picked[day][1] >= score:
            print(f"  !! {day} already claimed by a better match; dropping "
                  f"{subject[:44]}", file=sys.stderr)
            continue
        picked[day] = (words, score, rendered)
        subjects[day] = (sent[:10], subject, subtitle(body))

    for day, (_, _, rendered) in picked.items():
        (out / f"{day}.md").write_text(rendered, encoding="utf-8")

    # The subject line and subtitle never reached the mirror at all: its `title`
    # field reads "not much happened today" on days the email went out as
    # "[AINews] Qwen 3.8 Max(2.4T) and 27B...". Keep them beside the commentary so
    # the templating of titles can be measured against what was actually published.
    (out / "subjects.tsv").write_text(
        "covers\tsent\tsubject\tsubtitle\n" + "".join(
            f"20{d}\t{s}\t{sub}\t{st}\n" for d, (s, sub, st) in sorted(subjects.items())),
        encoding="utf-8")

    total = sum(w for w, _, _ in picked.values())
    print(f"wrote {len(picked)} files to {out} · {total:,} commentary words "
          f"({total // max(len(picked), 1)} mean) · {short} under {args.min_words}w · "
          f"{moved} filed under a different day than the send date implies · "
          f"{stale} with a stale in-issue date header · {unmatched} unmatched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
