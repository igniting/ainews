#!/usr/bin/env python3
"""Kleinberg burst detection for document streams (Kleinberg 2002).

The canonical algorithm for "when did this actually spike", and better than a
threshold in two ways that matter here. It models the stream as a hidden automaton
with a baseline state and a burst state, so a burst is defined by the data's own
rate rather than a number I pick. And the state sequence is decoded by Viterbi
with a transition cost, so entering a burst has to be *paid for* — brief noise
cannot trigger one, and a burst has a principled start and end date rather than a
crossing point.

The batch formulation: on day *t*, `d_t` issues were published and `r_t` of them
mentioned the target. The baseline state emits at the corpus-wide rate
`p0 = sum(r)/sum(d)`; the burst state at `s * p0`. Cost of a state is its negative
log-likelihood; the cost of *entering* a burst is `gamma * ln(n)`. Viterbi finds
the cheapest explanation of the whole series.

Usage:
    python3 analysis/methods/bursts.py
    python3 analysis/methods/bursts.py --entities MCP Qwen --s 2.5
"""

from __future__ import annotations

import argparse
import collections
import datetime
import math
import pathlib
import re
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import corpus  # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from density import NOISE, PATTERNS  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = REPO / "analysis" / "bursts.md"


def weekly_counts(pattern: re.Pattern) -> tuple[list[str], np.ndarray, np.ndarray]:
    """(week, mentions, words published).

    Trials are *words*, successes are *mentions*, so the binomial becomes a
    Poisson-rate model on the text itself. Two coarser choices both failed:
    issues-mentioning-X saturates (most entities appear in 80-97% of issues,
    giving meaningless 100-week bursts), and kilowords-as-trials makes r > d for
    frequently-named entities, clamping the rate to 1.
    """
    hit: collections.Counter = collections.Counter()
    tot: collections.Counter = collections.Counter()
    for date, _, body in corpus.load():
        # ISO week keeps the bins even; the newsletter skips weekends.
        year, week, _ = datetime.date.fromisoformat(date).isocalendar()
        key = f"{year}-W{week:02d}"
        body = NOISE.sub(" ", body)
        tot[key] += max(len(body.split()), 1)
        hit[key] += len(pattern.findall(body))
    keys = sorted(tot)
    r = np.asarray([hit[k] for k in keys])
    d = np.asarray([tot[k] for k in keys])
    return keys, np.minimum(r, d), d


def viterbi(r: np.ndarray, d: np.ndarray, s: float, gamma: float) -> np.ndarray:
    """Two-state Kleinberg automaton; returns the decoded state per bin (0 or 1)."""
    n = len(r)
    p0 = r.sum() / max(d.sum(), 1)
    p0 = min(max(p0, 1e-6), 1 - 1e-6)
    p1 = min(p0 * s, 1 - 1e-6)
    tau = gamma * math.log(max(n, 2))  # cost of entering the burst state

    def cost(p: float, i: int) -> float:
        # -log binomial likelihood, dropping the state-independent coefficient
        return -(r[i] * math.log(p) + (d[i] - r[i]) * math.log(1 - p))

    total = np.full((n, 2), np.inf)
    back = np.zeros((n, 2), dtype=int)
    total[0] = [cost(p0, 0), cost(p1, 0) + tau]
    for i in range(1, n):
        for state, p in ((0, p0), (1, p1)):
            options = [
                total[i - 1][0] + (tau if state == 1 else 0.0),
                total[i - 1][1] + 0.0,  # leaving a burst is free
            ]
            best = int(np.argmin(options))
            total[i][state] = options[best] + cost(p, i)
            back[i][state] = best

    states = np.zeros(n, dtype=int)
    states[-1] = int(np.argmin(total[-1]))
    for i in range(n - 1, 0, -1):
        states[i - 1] = back[i][states[i]]
    return states


def runs(keys: list[str], states: np.ndarray, r: np.ndarray, d: np.ndarray) -> list[tuple]:
    out = []
    i = 0
    while i < len(states):
        if states[i] == 0:
            i += 1
            continue
        j = i
        while j + 1 < len(states) and states[j + 1] == 1:
            j += 1
        weeks = j - i + 1
        rate = r[i : j + 1].sum() / max(d[i : j + 1].sum(), 1)
        out.append((keys[i], keys[j], weeks, rate))
        i = j + 1
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--entities", nargs="*", default=list(PATTERNS))
    parser.add_argument("--s", type=float, default=2.0, help="burst state rate multiplier")
    parser.add_argument("--gamma", type=float, default=1.0, help="cost of entering a burst")
    parser.add_argument("--min-weeks", type=int, default=2)
    args = parser.parse_args(argv)

    lines = [
        "# Bursts",
        "",
        "Kleinberg (2002) two-state burst detection, via `analysis/methods/bursts.py`.",
        "",
        "Weekly bins. Trials are words and successes are mentions, so the rate is a Poisson",
        "intensity on the text. Coarser units fail: issues-mentioning-X saturates at 80-97%,",
        "and kilowords-as-trials clamps frequently-named entities to a rate of 1.",
        f"Burst state emits at {args.s}x the baseline rate; entering a burst",
        f"costs gamma·ln(n) with gamma={args.gamma}, so short noise cannot trigger one.",
        "Unlike a threshold, the start and end dates are decoded, not chosen.",
        "",
        "| Entity | Burst | Weeks | Mentions/10k words in burst | Baseline |",
        "|---|---|---|---|---|",
    ]
    found = []
    for name in args.entities:
        if name not in PATTERNS:
            continue
        pattern = re.compile(PATTERNS[name], re.I)
        keys, r, d = weekly_counts(pattern)
        base = r.sum() / max(d.sum(), 1)
        states = viterbi(r, d, args.s, args.gamma)
        for start, end, weeks, rate in runs(keys, states, r, d):
            if weeks >= args.min_weeks:
                found.append((name, start, end, weeks, rate, base))

    for name, start, end, weeks, rate, base in sorted(found, key=lambda x: x[1]):
        lines.append(f"| {name} | {start} → {end} | {weeks} | {rate*10000:.1f} | {base*10000:.1f} |")
    lines.append("")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}  ({len(found)} bursts)")
    for name, start, end, weeks, rate, base in sorted(found, key=lambda x: x[1]):
        print(f"  {start} → {end}  ({weeks:>2}w)  {name:<15} {rate*10000:>5.1f} vs {base*10000:>5.1f} base")
    return 0


if __name__ == "__main__":
    sys.exit(main())
