#!/usr/bin/env python3
"""Splice fetched commentary into articles/, without touching the recaps.

Takes the directory written by `fetch_commentary.py` (one `YY-MM-DD.md` per
issue) and inserts each file's text into the matching article, replacing
whatever currently sits between the front matter and the first recap heading.

The recaps themselves are never modified, so every density measurement in
`analysis/` stays reproducible; only the editorial layer changes, and it
changes from boilerplate to the real thing.

Safety:
  * dry-run by default — pass --write to modify files
  * refuses to shorten an article's commentary unless --force
  * prints a per-file diff summary so you can see exactly what changed

Usage:
    python3 analysis/merge_commentary.py --src /tmp/commentary            # dry run
    python3 analysis/merge_commentary.py --src /tmp/commentary --write
    python3 analysis/methods/editorial.py                                 # re-measure
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
ARTICLES = REPO / "articles"

FRONT = re.compile(r"\A(---\n.*?\n---\n)", re.DOTALL)
RECAP = re.compile(r"^#\s+AI (Twitter|Reddit|Discord) Recap.*$", re.M | re.I)
SUMMARY = re.compile(r"^#{1,2}\s+.*(Recap|Discord Summary)", re.M | re.I)
HEADER_BQ = re.compile(r"^>\s*AI News for .*(?:\n>.*)*\n?", re.M)
META = re.compile(r"\A<!--.*?-->\n*", re.DOTALL)


def split(path: pathlib.Path) -> tuple[str, str, str]:
    """front matter, pre-recap section, rest."""
    t = path.read_text(encoding="utf-8", errors="replace")
    m = FRONT.match(t)
    front, body = (m.group(1), t[m.end():]) if m else ("", t)
    cut = RECAP.search(body) or SUMMARY.search(body)
    i = cut.start() if cut else len(body)
    return front, body[:i], body[i:]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True, help="directory of YY-MM-DD.md commentary files")
    ap.add_argument("--write", action="store_true", help="actually modify articles/")
    ap.add_argument("--force", action="store_true", help="allow replacing longer with shorter")
    args = ap.parse_args(argv)

    src = pathlib.Path(args.src)
    by_day: dict[str, list[pathlib.Path]] = {}
    for p in ARTICLES.glob("*.md"):
        by_day.setdefault(p.name[:8], []).append(p)

    changed = skipped = missing = shorter = 0
    for f in sorted(src.glob("*.md")):
        day = f.stem
        targets = by_day.get(day)
        if not targets:
            missing += 1
            print(f"  no article for {day}")
            continue
        new = META.sub("", f.read_text(encoding="utf-8", errors="replace")).strip()
        if len(new.split()) < 15:
            skipped += 1
            continue
        for path in targets:
            front, pre, rest = split(path)
            # keep the "AI News for ... We checked N subreddits" header blockquote,
            # which is data the analysis scripts rely on
            keep = "".join(HEADER_BQ.findall(pre))
            old_words = len(HEADER_BQ.sub("", pre).split())
            if old_words > len(new.split()) and not args.force:
                shorter += 1
                print(f"  {path.name[:34]:<36} existing {old_words}w > new "
                      f"{len(new.split())}w — skipped (use --force)")
                continue
            rebuilt = f"{front}\n{new}\n\n{keep.strip()}\n\n---\n\n{rest.lstrip()}"
            print(f"  {path.name[:34]:<36} {old_words:>5}w -> {len(new.split()):>5}w")
            if args.write:
                path.write_text(rebuilt, encoding="utf-8")
            changed += 1

    verb = "updated" if args.write else "would update"
    print(f"\n{verb} {changed} articles · {skipped} sources too short · "
          f"{shorter} already longer · {missing} with no matching article")
    if not args.write:
        print("dry run — pass --write to apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
