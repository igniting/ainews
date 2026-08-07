#!/usr/bin/env python3
"""Change point detection (PELT) for format regimes and content shifts.

Two jobs, and the first has to happen before any other method is trusted:

1. **Format regimes.** Runs PELT over structural features of each issue — length,
   which recap sections exist, link density — to date the publishing-pipeline
   changes. Every unsupervised method tried on this corpus ranked those changes
   above every news event, so they have to be located explicitly and controlled
   for rather than discovered by accident.

2. **Content shifts.** Runs PELT over an entity's mention-density series to date
   when its coverage actually changed. This is the mechanical version of the
   judgement call I got wrong in `VERIFICATION.md`: I read a dramatic headline as
   Meta's inflection point, when the decline had begun six months earlier.

PELT (Killick, Fearnhead & Eckley 2012) finds an exact optimal segmentation for a
penalized cost in linear time, so unlike a threshold or an eyeballed chart it has
no tuning beyond the penalty, and the penalty has a clear meaning: how much
improvement in fit a new segment must earn.

Usage:
    python3 analysis/methods/changepoints.py --format
    python3 analysis/methods/changepoints.py --content 'Meta Llama' 'Claude'
"""

from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sys

import numpy as np
import ruptures as rpt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import corpus  # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from density import NOISE, PATTERNS  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = REPO / "analysis" / "changepoints.md"

SECTION = re.compile(r"^#\s+AI (Twitter|Reddit|Discord) Recap", re.M | re.I)
LINK = re.compile(r"https?://")


def structural_features() -> tuple[list[str], np.ndarray, list[str]]:
    """Per-issue structural signal: what the pipeline was doing, not what it said."""
    dates, rows = [], []
    for date, _, body in corpus.load():
        words = max(len(body.split()), 1)
        present = {m.group(1).lower() for m in SECTION.finditer(body)}
        rows.append(
            [
                np.log10(words),
                1.0 if "twitter" in present else 0.0,
                1.0 if "reddit" in present else 0.0,
                1.0 if "discord" in present else 0.0,
                len(LINK.findall(body)) / words * 1000,
                body.count("\n#") / words * 1000,
            ]
        )
        dates.append(date)
    names = ["log10(words)", "has_twitter", "has_reddit", "has_discord", "links/1k", "headings/1k"]
    X = np.asarray(rows)
    # Standardize so no single feature's scale dominates the cost function.
    X = (X - X.mean(axis=0)) / np.where(X.std(axis=0) > 0, X.std(axis=0), 1)
    return dates, X, names


def density_series(name: str, by_month: bool = True) -> tuple[list[str], np.ndarray]:
    """Mentions per 10k words for one entity, aggregated by month."""
    pattern = re.compile(PATTERNS[name], re.I)
    hits: collections.Counter = collections.Counter()
    words: collections.Counter = collections.Counter()
    for date, _, body in corpus.load():
        key = date[:7] if by_month else date
        body = NOISE.sub(" ", body)
        words[key] += len(body.split())
        hits[key] += len(pattern.findall(body))
    keys = sorted(words)
    return keys, np.asarray([hits[k] / words[k] * 10000 for k in keys])


def segment(signal: np.ndarray, penalty: float, model: str = "rbf", min_size: int = 4) -> list[int]:
    if signal.ndim == 1:
        signal = signal.reshape(-1, 1)
    algo = rpt.Pelt(model=model, min_size=min_size).fit(signal)
    return algo.predict(pen=penalty)[:-1]  # drop the trailing endpoint


def describe(keys: list[str], values: np.ndarray, breaks: list[int]) -> list[tuple[str, str, float]]:
    """Mean level of each segment between change points."""
    bounds = [0, *breaks, len(keys)]
    out = []
    for lo, hi in zip(bounds, bounds[1:]):
        out.append((keys[lo], keys[hi - 1], float(np.mean(values[lo:hi]))))
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", action="store_true", help="detect publishing-format regimes")
    parser.add_argument("--content", nargs="*", default=[], help="entities to segment (see density.py --list)")
    parser.add_argument("--pen-format", type=float, default=25.0)
    parser.add_argument("--pen-content", type=float, default=8.0)
    args = parser.parse_args(argv)

    if not args.format and not args.content:
        args.format = True
        args.content = ["Meta Llama", "Mistral", "Claude", "GPT/OpenAI", "DeepSeek", "Qwen", "agentic", "MCP"]

    lines = ["# Change points", "", "Detected with PELT via `analysis/methods/changepoints.py`.", ""]

    if args.format:
        dates, X, names = structural_features()
        breaks = segment(X, args.pen_format, model="rbf", min_size=10)
        lines += [
            "## Publishing-format regimes",
            "",
            f"PELT over standardized structural features ({', '.join(names)}) —",
            "what the pipeline was doing, independent of the news.",
            "",
            "| Regime | From | To | Issues |",
            "|---|---|---|---|",
        ]
        bounds = [0, *breaks, len(dates)]
        for i, (lo, hi) in enumerate(zip(bounds, bounds[1:]), 1):
            lines.append(f"| {i} | {dates[lo]} | {dates[hi-1]} | {hi-lo} |")
        lines += [
            "",
            "**Any cross-regime comparison needs these controlled for.** Unsupervised",
            "methods rank these boundaries above every news event in the corpus.",
            "",
        ]
        print("format regimes:")
        for i, (lo, hi) in enumerate(zip(bounds, bounds[1:]), 1):
            print(f"  {i}: {dates[lo]} .. {dates[hi-1]}  ({hi-lo} issues)")

    for name in args.content:
        if name not in PATTERNS:
            print(f"unknown entity {name!r}", file=sys.stderr)
            continue
        keys, values = density_series(name)
        breaks = segment(values, args.pen_content, model="l2", min_size=3)
        segments = describe(keys, values, breaks)
        lines += [
            f"## {name}",
            "",
            "| From | To | Mean density (per 10k words) | Change |",
            "|---|---|---|---|",
        ]
        prev = None
        for start, end, mean in segments:
            delta = "—" if prev is None else f"{(mean-prev)/prev*100:+.0f}%" if prev > 0.01 else "new"
            lines.append(f"| {start} | {end} | {mean:.1f} | {delta} |")
            prev = mean
        lines.append("")
        print(f"\n{name}: " + "  ".join(f"{s}→{e}:{m:.1f}" for s, e, m in segments))

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nwrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
