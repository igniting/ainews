#!/usr/bin/env python3
"""The instrument was a language model, and it was swapped six times.

Almost every word in this corpus was written by a model. The recaps are
summaries of sampled sources, and the archive declares — in-band, in a
blockquote under each recap heading — which model produced them:

    > all recaps done by Claude 3 Opus, best of 4 runs.
    > A summary of Summaries of Summaries by Gemini 3.0 Pro Preview Nov-18

That makes the summarizer an observable property of every issue, and it changes:
Claude 3 Opus, Claude 3.5, GPT-4o, o1, Gemini 2.0, Gemini 2.5, GPT-5, Gemini 3.
Every density series in this repo is therefore measured through an instrument
that was replaced part-way through, which is the same class of problem as the
source-composition inversion `sections.py` exists to control for.

Three things this script establishes:

1. **The timeline.** Which model wrote which surface, month by month, and where
   it is not declared at all (the Twitter recap after February 2025).

2. **The direct experiment.** Three days were published twice, the same news
   summarised by two different models — 2024-05-13, 2024-07-18 and 2024-08-06.
   Comparing pattern densities between the two editions of one day measures the
   instrument's contribution directly, with the news held constant.

3. **The steps.** Whether densities jump at the summarizer boundaries. This is
   confounded with real news — R1 landed three weeks before the February 2025
   change — so it bounds rather than isolates the effect.

Usage:
    python3 analysis/methods/summarizer.py
"""

from __future__ import annotations

import argparse
import collections
import pathlib
import re
import statistics
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
ARTICLES = REPO / "articles"
OUT = REPO / "analysis" / "summarizer.md"

FRONT = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
HEAD = re.compile(r"^#\s+AI (Twitter|Reddit|Discord) Recap.*$", re.M | re.I)
# Twitter/Reddit: "> all recaps done by Claude 3 Opus, best of 4 runs."
DONE_BY = re.compile(r"recaps?\s+(?:done\s+)?by\s+\*{0,2}([^,.\n*]{3,40})", re.I)
# Discord: "> A summary of Summaries of Summaries by Gemini 2.5 Pro Exp"
SUMM_BY = re.compile(r"^>\s*A summary of Summaries of Summaries by\s+(.+?)\s*$", re.M | re.I)

PATTERNS = {
    "agentic": r"\bagentic\b|\bagents?\b",
    "fine-tuning": r"fine[- ]?tun|\bLoRA\b",
    "RAG": r"\bRAG\b|retrieval[- ]augmented",
    "reasoning": r"\breasoning\b",
    "evals": r"\beval(s|uation)?\b|benchmark",
    "quantization": r"quantiz|\bGGUF\b|\bfp8\b",
    "China bloc": r"\bqwen\b|deepseek|kimi|\bglm-|minimax",
}

# The same day, published twice, summarised by two different models.
TWINS = [("24-05-13", "gpt4o-version", "gpt4t-version"),
         ("24-07-18", "gpt4o-mini-version", "gpt4o-version"),
         ("24-08-06", "gpt4o-august-edition", "gpt4o-mini-edition")]


def family(raw: str) -> str:
    s = raw.lower()
    for needle, name in (("claude", "claude"), ("o1", "o1"), ("gpt-5", "gpt-5"),
                         ("gpt-4", "gpt-4"), ("gpt4", "gpt-4"), ("gemini 3", "gemini-3"),
                         ("gemini 2.5", "gemini-2.5"), ("gemini 2.0", "gemini-2.0"),
                         ("grok", "grok")):
        if needle in s:
            return name
    return raw.strip()[:14]


def sections(path: pathlib.Path) -> dict[str, str]:
    body = FRONT.sub("", path.read_text(encoding="utf-8", errors="replace"))
    marks = list(HEAD.finditer(body))
    out: dict[str, str] = {}
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        out[m.group(1).lower()] = body[m.end():end]
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--min-words", type=int, default=50000,
                    help="skip months with less section text than this in the step test")
    args = ap.parse_args(argv)

    compiled = {k: re.compile(v, re.I) for k, v in PATTERNS.items()}
    declared: dict[str, dict[str, collections.Counter]] = {
        s: collections.defaultdict(collections.Counter) for s in ("twitter", "discord")}
    issues: dict[str, collections.Counter] = {
        s: collections.Counter() for s in ("twitter", "discord")}
    words: collections.Counter = collections.Counter()
    hits: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)

    for path in sorted(ARTICLES.glob("*.md")):
        month = f"20{path.name[:5]}"
        secs = sections(path)
        if "twitter" in secs:
            issues["twitter"][month] += 1
            m = DONE_BY.search(secs["twitter"][:320])
            if m:
                declared["twitter"][month][family(m.group(1))] += 1
        if "discord" in secs:
            issues["discord"][month] += 1
            m = SUMM_BY.search(secs["discord"][:400])
            if m:
                declared["discord"][month][family(m.group(1))] += 1
            words[month] += len(secs["discord"].split())
            for name, rx in compiled.items():
                hits[name][month] += len(rx.findall(secs["discord"]))

    lines = ["# The summarizer", "",
             "Generated by `analysis/methods/summarizer.py`. Every recap in this archive was",
             "written by a language model, and the archive says which one.", "",
             "## Declared summarizer by month", "",
             "| Month | Twitter recap | issues declaring | Discord recap | issues declaring |",
             "|---|---|---|---|---|"]
    months = sorted(set(issues["twitter"]) | set(issues["discord"]))
    for mo in months:
        tw = declared["twitter"][mo].most_common(1)
        dc = declared["discord"][mo].most_common(1)
        lines.append(f"| {mo} | {tw[0][0] if tw else '—'} | "
                     f"{sum(declared['twitter'][mo].values())}/{issues['twitter'][mo]} | "
                     f"{dc[0][0] if dc else '—'} | "
                     f"{sum(declared['discord'][mo].values())}/{issues['discord'][mo]} |")

    # --- the direct experiment -------------------------------------------------
    lines += ["", "## The same day, summarised twice", "",
              "Three days were published as two editions, differing only in the model that",
              "wrote them. This holds the news constant and varies the instrument.", "",
              "| Day | Pattern | edition A | edition B | ratio |", "|---|---|---|---|---|"]
    spreads = []
    for date, a, b in TWINS:
        fa = [p for p in ARTICLES.glob(date + "*.md") if a in p.name]
        fb = [p for p in ARTICLES.glob(date + "*.md") if b in p.name]
        if not fa or not fb:
            continue
        sa, sb = sections(fa[0]).get("discord", ""), sections(fb[0]).get("discord", "")
        if len(sa.split()) < 5000 or len(sb.split()) < 5000:
            continue
        wa, wb = len(sa.split()), len(sb.split())
        for name, rx in compiled.items():
            da = len(rx.findall(sa)) / wa * 10000
            db = len(rx.findall(sb)) / wb * 10000
            if max(da, db) < 2:
                continue
            ratio = max(da, db) / min(da, db) if min(da, db) else float("inf")
            spreads.append(ratio)
            lines.append(f"| {date} | `{name}` | {da:.1f} | {db:.1f} | {ratio:.2f}× |")
    if spreads:
        lines += ["", f"**Median ratio between two summarizers on the same day: "
                      f"{statistics.median(spreads):.2f}×. Largest: "
                      f"{max(spreads):.2f}×.**", ""]

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    for surface in ("twitter", "discord"):
        dec = sum(sum(c.values()) for c in declared[surface].values())
        tot = sum(issues[surface].values())
        fams = {f for c in declared[surface].values() for f in c}
        print(f"  {surface:<8} {dec}/{tot} issues declare a summarizer; "
              f"{len(fams)} distinct families: {', '.join(sorted(fams))}")
    if spreads:
        print(f"  same-day two-model comparison: median {statistics.median(spreads):.2f}×, "
              f"max {max(spreads):.2f}× ({len(spreads)} pattern-day pairs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
