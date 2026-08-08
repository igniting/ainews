#!/usr/bin/env python3
"""Split an issue into its recap sections. One implementation, used everywhere.

WHY THIS IS ITS OWN MODULE
--------------------------
Five scripts each had their own copy of "find the `# AI X Recap` headings and
slice between them", and all five were wrong in the same way. The newsletter's
heading grammar is not one pattern, it is six, and it changed twice in the first
four months of the corpus:

    # AI Twitter Recap                              595 issues
    # PART X: AI Twitter Recap                       17 issues   (March 2024)
    # AI Reddit Recap                               596 issues
    # AI Discord Recap                              489 issues
    # AI Discords                                    91 issues
    # PART 0: Summary of Summaries of Summaries      26 issues
    # Discord: High level Discord summaries         216 issues
    # PART 1: High level Discord summaries          322 issues

Slicing only between `AI (Twitter|Reddit|Discord) Recap` headings gets two
things wrong. It misses the March 2024 Twitter recaps entirely, because they are
prefixed `PART X:`. And where the Discord section opens with `PART 0` or
`AI Discords` instead of `AI Discord Recap`, the whole Discord summary — tens of
thousands of words — is silently appended to whichever section came before it.
On 2024-03-28, 2024-03-29 and 2024-04-01 that section was Twitter, which
inflated the 2024H1 Twitter baseline from 38k words to 129k. Every fold-change
in the book measured against that baseline was wrong.

The fix is not "cut at the next top-level heading" either, because for Discord
the `PART 1` and `PART 2` headings are its own continuation, not a new section.
A section ends at the next heading belonging to a *different* source.

Usage:
    from recaps import sections_of, split
    secs = sections_of(body)          # {"twitter": ..., "reddit": ..., "discord": ...}
    secs = split(path)                # same, reading and stripping front matter

    python3 analysis/methods/recaps.py --check     # regression fixtures
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
ARTICLES = REPO / "articles"

FRONT = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)

# Every way a section can begin, mapped to the source it belongs to. Order
# matters only in that the first alternative to match at a position wins.
STARTS: list[tuple[str, re.Pattern[str]]] = [
    ("twitter", re.compile(r"^#\s+(?:PART\s+\w+:\s*)?AI\s+Twitter\s+Recap.*$", re.M | re.I)),
    ("reddit", re.compile(r"^#\s+(?:PART\s+\w+:\s*)?AI\s+Reddit\s+Recap.*$", re.M | re.I)),
    ("discord", re.compile(
        r"^#\s+(?:AI\s+Discord\s+Recap"
        r"|AI\s+Discords?\s*$"
        r"|PART\s+\d+\s*:.*$"
        r"|Discord\s*:.*$).*$", re.M | re.I)),
]

# Kept for callers that only want to know whether an issue has recaps at all.
ANY_START = re.compile("|".join(f"(?:{p.pattern})" for _, p in STARTS), re.M | re.I)


def boundaries(body: str) -> list[tuple[int, int, str]]:
    """(start, end_of_heading, source) for every section heading, in order."""
    found: dict[int, tuple[int, str]] = {}
    for source, pattern in STARTS:
        for m in pattern.finditer(body):
            # A position already claimed by an earlier, more specific pattern wins;
            # "PART X: AI Twitter Recap" must not also register as a Discord start.
            if m.start() not in found:
                found[m.start()] = (m.end(), source)
    return [(s, e, k) for s, (e, k) in sorted(found.items())]


def sections_of(body: str) -> dict[str, str]:
    """Body (front matter already stripped) -> {source: text}.

    A section runs until the next heading belonging to a different source, so
    Discord keeps its `PART 1`/`PART 2` tail while Twitter does not inherit it.
    Repeated sections are concatenated rather than overwritten.
    """
    marks = boundaries(body)
    out: dict[str, str] = {}
    for i, (_, head_end, source) in enumerate(marks):
        end = len(body)
        for start_j, _, source_j in marks[i + 1:]:
            if source_j != source:
                end = start_j
                break
        chunk = body[head_end:end]
        out[source] = (out[source] + "\n" + chunk) if source in out else chunk
    return out


def split(path: pathlib.Path) -> dict[str, str]:
    return sections_of(FRONT.sub("", path.read_text(encoding="utf-8", errors="replace")))


# --- regression fixtures ---------------------------------------------------
# One issue per heading style that used to be mis-parsed. The test is not "is
# the section a plausible length" — 2024-03-28's Twitter recap really does read
# "TO BE COMPLETED" — but "did Discord's text end up in Discord".
LEAKED = re.compile(r"Summary of Summaries|Detailed by-Channel|High level Discord", re.I)

FIXTURES = [
    ("24-03-28", "Discord opens with `# PART 0`"),
    ("24-03-29", "Discord opens with `# PART 0`"),
    ("24-04-01", "Discord opens with `# AI Discords`"),
    ("24-03-05", "Twitter is headed `# PART X: AI Twitter Recap`"),
    ("25-06-20", "ordinary issue, all three headings standard"),
]


def check() -> int:
    bad = 0
    for prefix, why in FIXTURES:
        matches = sorted(ARTICLES.glob(prefix + "*.md"))
        if not matches:
            print(f"  FAIL  no article {prefix}*")
            bad += 1
            continue
        secs = split(matches[0])
        problems = []
        if "twitter" not in secs:
            problems.append("no twitter section")
        for source in ("twitter", "reddit"):
            if LEAKED.search(secs.get(source, "")):
                problems.append(f"Discord text leaked into {source}")
        if len(secs.get("discord", "").split()) < 3000:
            problems.append("discord lost its PART 1/2 tail")
        counts = " ".join(f"{k[:2]}={len(v.split()):,}" for k, v in sorted(secs.items()))
        print(f"  {'ok  ' if not problems else 'FAIL'}  {prefix}  {counts:<34} {why}")
        for p in problems:
            print(f"        - {p}")
        bad += bool(problems)
    print("all fixtures pass" if not bad else f"{bad} fixture failures")
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="run the regression fixtures")
    args = ap.parse_args(argv)
    if args.check:
        return check()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
