#!/usr/bin/env python3
"""Pull matching passages out of the issue bodies, with date and section context.

Everything else in analysis/ works from titles and front-matter tags, which is
0.6% of the corpus. This reads the other 99.4%.

Each issue body is split on its `# AI Twitter Recap` / `# AI Reddit Recap` /
`# AI Discord Recap` headings so a hit can be attributed to the surface it came
from — the same story often appears on all three, and which one carried it first
is itself a finding.

Usage:
    python3 analysis/passages.py 'mistral' --since 2024-07-01 --until 2025-06-30
    python3 analysis/passages.py 'llama.?4' --section twitter --context 1
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
ARTICLES = REPO / "articles"

SECTION_RE = re.compile(r"^#\s+(AI (?:Twitter|Reddit|Discord) Recap.*|PART \d.*)$", re.M | re.I)
FRONT_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)


def sections(body: str) -> list[tuple[str, str]]:
    """Split a body into (section name, text). Text before any heading is 'lede'."""
    marks = list(SECTION_RE.finditer(body))
    if not marks:
        return [("lede", body)]
    out = [("lede", body[: marks[0].start()])]
    for i, mark in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        name = mark.group(1).lower()
        for key in ("twitter", "reddit", "discord", "part"):
            if key in name:
                name = key
                break
        out.append((name, body[mark.end() : end]))
    return out


def paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pattern", help="regex to search for, case-insensitive")
    parser.add_argument("--since", default="2000-01-01", help="YYYY-MM-DD")
    parser.add_argument("--until", default="2999-12-31", help="YYYY-MM-DD")
    parser.add_argument(
        "--section",
        choices=["lede", "twitter", "reddit", "discord", "part", "any"],
        default="any",
        help="restrict to one surface (default: any)",
    )
    parser.add_argument("--max-per-issue", type=int, default=2, help="cap paragraphs per issue")
    parser.add_argument("--width", type=int, default=400, help="characters of each paragraph to print")
    parser.add_argument("--count", action="store_true", help="only report per-issue hit counts")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    pattern = re.compile(args.pattern, re.I)

    hits = 0
    for path in sorted(ARTICLES.glob("*.md")):
        date = f"20{path.name[:8]}"
        if not (args.since <= date <= args.until):
            continue
        body = FRONT_RE.sub("", path.read_text(encoding="utf-8", errors="replace"))

        found = []
        for name, text in sections(body):
            if args.section not in ("any", name):
                continue
            for para in paragraphs(text):
                if pattern.search(para):
                    found.append((name, para))

        if not found:
            continue
        hits += len(found)
        if args.count:
            print(f"{date}  {len(found):>3} hits  ({path.name})")
            continue
        print(f"\n{'=' * 78}\n{date}  {path.name}\n{'=' * 78}")
        for name, para in found[: args.max_per_issue]:
            flat = re.sub(r"\s+", " ", para)
            print(f"  [{name}] {flat[: args.width]}")
        if len(found) > args.max_per_issue:
            print(f"  … {len(found) - args.max_per_issue} more in this issue")

    print(f"\ntotal paragraphs matched: {hits:,}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
