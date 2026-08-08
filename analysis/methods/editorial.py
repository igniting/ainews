#!/usr/bin/env python3
"""The editorial layer — the only part of the corpus a human wrote.

Every issue opens with a short passage written by the editor before any machine
summary begins: a headline claim, a judgement, sometimes an argument with the
summaries below it. Everything else in this archive — the Twitter, Reddit and
Discord recaps — is model-generated from sampled sources.

That makes the lede a fourth measurement surface, and a different kind from the
other three. Twitter, Reddit and Discord each sample a *population*. The lede
samples one person's opinion, which is a confound when you are measuring the
field and a signal when you are measuring the coverage.

Extraction is fiddly because the issue format changed twice:

- Late 2023 / early 2024 issues run  lede -> "## <Server> Discord Summary".
- From 2024-03 onwards they run       lede -> "# AI Twitter Recap".
- On days the editor calls quiet, the "AI News for <dates>" blockquote comes
  first and the lede follows it, rather than the other way round.

So the cut point is whichever of those headings comes first, and the standard
"AI News for <dates>. We checked N subreddits..." blockquote is stripped, along
with images, Astro template tags and the table-of-contents marker.

A caution about what this measures. Until 2026-08 the corpus took its lede from
the GitHub mirror, where 104 of 152 issues in 2026 carry nothing but the
boilerplate line "**a quiet day.**" — which read as an editor going quiet, and
was nothing of the kind. The mirror was dropping the lede; the sent email still
had it. `analysis/extract_commentary_gmail.py` restored it for 2026-01-26
onward, and the 2026 median went from 3 words to 183. Anything measured on this
surface before that date is measuring the mirror.

Usage:
    python3 analysis/methods/editorial.py
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
OUT = REPO / "analysis" / "editorial.md"

# Total words in articles/, recomputed after the 2026 commentary was restored.
CORPUS_WORDS = 15_433_052

FRONT = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
RECAP = re.compile(r"^#\s+AI (Twitter|Reddit|Discord) Recap.*$", re.M | re.I)
SUMMARY = re.compile(r"^#{1,2}\s+.*(Recap|Discord Summary)", re.M | re.I)
BLOCKQUOTE = re.compile(r"^>.*(?:\n>.*)*\n?", re.M)
NOISE = [re.compile(r"<!--.*?-->", re.S), re.compile(r"\{%.*?%\}", re.S),
         re.compile(r"!\[[^\]]*\]\([^)]*\)"), re.compile(r"\[TOC\]"),
         re.compile(r"\*\*Table of Contents\*\*"), re.compile(r"^-{3,}\s*$", re.M)]

# The same patterns the other surfaces are measured with, plus one the other
# surfaces cannot carry: the editor's own promotional vocabulary.
PATTERNS = {
    "agentic": r"\bagentic\b|\bagents?\b",
    "China bloc": r"\bqwen\b|deepseek|kimi|moonshot|\bglm-|minimax",
    "fine-tuning": r"fine[- ]?tun|\bLoRA\b",
    "RAG": r"\bRAG\b|retrieval[- ]augmented",
    "reasoning": r"\breasoning\b",
    "evals": r"\beval(s|uation)?\b|benchmark",
    "promotional": r"\bhype\b|all you need|\bSOTA\b|game[- ]chang|revolution|\bbanger\b",
}

BOILERPLATE = re.compile(r"^\s*\*\*a quiet day\.?\*\*\s*$", re.I)


def lede(path: pathlib.Path) -> str:
    body = FRONT.sub("", path.read_text(encoding="utf-8", errors="replace"))
    cut = RECAP.search(body) or SUMMARY.search(body)
    text = body[:cut.start()] if cut else ""
    text = BLOCKQUOTE.sub("", text)
    for rx in NOISE:
        text = rx.sub("", text)
    return text.strip()


def half(name: str) -> str:
    return f"20{name[:2]}H{1 if int(name[3:5]) <= 6 else 2}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--min-words", type=int, default=8000,
                        help="skip half-years with less editorial text than this")
    args = parser.parse_args(argv)

    compiled = {k: re.compile(v, re.I) for k, v in PATTERNS.items()}
    words: collections.Counter = collections.Counter()
    hits: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    lengths: dict[str, list[int]] = collections.defaultdict(list)
    boiler: collections.Counter = collections.Counter()
    issues: collections.Counter = collections.Counter()

    for path in sorted(ARTICLES.glob("*.md")):
        text = lede(path)
        h = half(path.name)
        issues[h] += 1
        n = len(text.split())
        words[h] += n
        lengths[h].append(n)
        if BOILERPLATE.match(text.strip()):
            boiler[h] += 1
        for name, rx in compiled.items():
            hits[name][h] += len(rx.findall(text))

    periods = [p for p in sorted(words) if words[p] >= args.min_words]
    total = sum(words.values())

    lines = [
        "# The editorial layer",
        "",
        "Generated by `analysis/methods/editorial.py`. The lede is the only text in the",
        "corpus written by a person: everything under a recap heading is model-generated",
        "from sampled sources.",
        "",
        f"**{total:,} words across {sum(issues.values())} issues — "
        f"{100 * total / CORPUS_WORDS:.1f}% of the corpus.**",
        "",
        "| Half | Issues | Editorial words | Median per issue | Boilerplate-only |",
        "|---|---|---|---|---|",
    ]
    for h in sorted(issues):
        lines.append(f"| {h} | {issues[h]} | {words[h]:,} | "
                     f"{statistics.median(lengths[h]):.0f} | "
                     f"{boiler[h]} ({100 * boiler[h] // issues[h]}%) |")
    lines += ["", "## Density inside the editorial layer", "",
              "Mentions per 10⁴ words. Half-years with under "
              f"{args.min_words:,} editorial words are omitted.", "",
              "| Pattern | " + " | ".join(periods) + " |",
              "|---|" + "|".join(["---"] * len(periods)) + "|"]
    for name in PATTERNS:
        lines.append(f"| `{name}` | " + " | ".join(
            f"{hits[name][p] / words[p] * 10000:.1f}" for p in periods) + " |")
    lines += ["", "> **Caveat.** This layer is thin — 13,000 to 33,000 words per half-year",
              "> against 15.4M for the corpus — so a handful of issues can move a column.",
              "> The dip through 2025 is real; the far deeper 2026 dip this table used to",
              "> show was not, and came from the mirror dropping the lede rather than the",
              "> editor dropping it. See `analysis/extract_commentary_gmail.py`.", ""]

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    print(f"{total:,} editorial words, {100 * total / CORPUS_WORDS:.2f}% of the corpus")
    for h in sorted(issues):
        print(f"  {h}  {issues[h]:>3} issues  {words[h]:>7,} words  "
              f"median {statistics.median(lengths[h]):>5.0f}  boilerplate {boiler[h]:>3}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
