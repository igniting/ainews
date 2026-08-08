#!/usr/bin/env python3
"""Pull verbatim passages out of the corpus, with their date and surface.

Every quotation in the book has to come from here rather than from memory. The
first edition quoted by hand and got three dates wrong, because the archive
carries two of them — the day an issue covers (its filename) and the day it was
published (its front matter) — and they differ by one.

What this returns is a passage, the day it covers, and which surface it came
from, so a citation can be written without going back to the file. Sections are
split by `recaps.py`, so a quote attributed to announcement space really is from
the Twitter recap and not from the Discord summary that follows it.

Four surfaces are searchable:

    lede      the editor's own opening — the only human-written text
    twitter   announcement space
    reddit    practice space
    discord   community space

Usage:
    # what did the editor say about fine-tuning in the first half of 2024?
    python3 analysis/quotes.py 'fine[- ]?tun' --sec lede --from 24-01 --to 24-07

    # longest passages, for block quotes
    python3 analysis/quotes.py '\\bMCP\\b' --sec twitter --min-words 40 --n 5

    # every surface at once, to compare how a thing was described
    python3 analysis/quotes.py 'prompt injection' --sec all --n 12
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "methods"))
from recaps import FRONT, sections_of  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent
ARTICLES = REPO / "articles"

RECAP = re.compile(r"^#\s+AI (Twitter|Reddit|Discord) Recap", re.M | re.I)
SUMMARY = re.compile(r"^#{1,2}\s+.*(Recap|Discord Summary)", re.M | re.I)
HEADER_BQ = re.compile(r"^>\s*AI News for .*(?:\n>.*)*\n?", re.M)
NOISE = [re.compile(r"<!--.*?-->", re.S), re.compile(r"\{%.*?%\}", re.S),
         re.compile(r"!\[[^\]]*\]\([^)]*\)"), re.compile(r"^-{3,}\s*$", re.M)]
# Markdown that adds nothing when a passage is read as prose.
LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")


def lede_of(body: str) -> str:
    cut = RECAP.search(body) or SUMMARY.search(body)
    text = body[:cut.start()] if cut else ""
    text = HEADER_BQ.sub("", text)
    for rx in NOISE:
        text = rx.sub("", text)
    return text.strip()


def passages(text: str) -> list[str]:
    """Split into quotable units: paragraphs, and bullets within them."""
    out = []
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block:
            continue
        if block.count("\n- ") >= 1 or block.startswith("- "):
            out += [b.strip(" -") for b in block.split("\n- ") if b.strip(" -")]
        else:
            out.append(block)
    return out


def clean(s: str) -> str:
    s = LINK.sub(r"\1", s)
    s = re.sub(r"[*_`>#]+", "", s)
    return re.sub(r"\s+", " ", s).strip()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pattern", help="regex to search for")
    ap.add_argument("--sec", default="lede",
                    choices=["lede", "twitter", "reddit", "discord", "all"])
    ap.add_argument("--from", dest="lo", default="23-01", help="YY-MM inclusive")
    ap.add_argument("--to", dest="hi", default="27-01", help="YY-MM exclusive")
    ap.add_argument("--min-words", type=int, default=12)
    ap.add_argument("--max-words", type=int, default=120)
    ap.add_argument("--n", type=int, default=8, help="how many to print")
    ap.add_argument("--sort", default="date", choices=["date", "length"])
    args = ap.parse_args(argv)

    rx = re.compile(args.pattern, re.I)
    wanted = ("twitter", "reddit", "discord") if args.sec == "all" else (args.sec,)
    hits: list[tuple[str, str, str]] = []

    for path in sorted(ARTICLES.glob("*.md")):
        day = path.name[:8]
        if not (args.lo <= day[:5] < args.hi):
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        body = FRONT.sub("", raw)
        pools: dict[str, str] = {}
        if args.sec in ("lede", "all"):
            pools["lede"] = lede_of(body)
        if args.sec != "lede":
            secs = sections_of(body)
            for name in wanted:
                if name in secs:
                    pools[name] = secs[name]
        for surface, text in pools.items():
            for p in passages(text):
                if not rx.search(p):
                    continue
                c = clean(p)
                if args.min_words <= len(c.split()) <= args.max_words:
                    hits.append((day, surface, c))

    hits.sort(key=(lambda h: -len(h[2])) if args.sort == "length" else (lambda h: h[0]))
    seen: set[str] = set()
    shown = 0
    for day, surface, text in hits:
        key = text[:70].lower()
        if key in seen:
            continue
        seen.add(key)
        print(f"\n[20{day} · {surface}]\n{text}")
        shown += 1
        if shown >= args.n:
            break
    print(f"\n— {len(hits)} passages matched, {shown} shown —", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
