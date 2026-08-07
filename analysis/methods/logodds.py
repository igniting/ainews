#!/usr/bin/env python3
"""Log-odds ratio with an informative Dirichlet prior (Monroe, Colaresi & Quinn 2008).

The standard method for "which words distinguish corpus A from corpus B", and a
strict improvement on the frequency differences used elsewhere in this repo.

Raw frequency differences have two failure modes that matter badly here:

1. **Frequent words dominate.** A 1pp move on a common word outranks a 10x move
   on a rare one, so the top of the list fills with vocabulary that is merely
   common rather than distinctive.
2. **Rare words are unstable.** A word appearing 3 times in one period and 0 in
   another looks like an infinite ratio, so naive ratios surface noise.

Monroe et al. fix both by shrinking each word's log-odds toward a prior built
from the *whole* corpus, then dividing by the estimated standard deviation. The
result is a z-score: how confidently is this word distinctive, given how often we
had the chance to observe it. Words are comparable across frequency ranges, and
the score is interpretable (|z| > 1.96 ≈ p < 0.05).

Usage:
    python3 analysis/methods/logodds.py 2024 2026
    python3 analysis/methods/logodds.py 2024H1 2026H1 --top 30
"""

from __future__ import annotations

import argparse
import collections
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import corpus  # noqa: E402


def bucket_of(date: str, spec: str) -> str:
    """Match a date against a period spec: '2024', '2024H1' or '2024Q3'."""
    if "H" in spec:
        return corpus.half(date)
    if "Q" in spec:
        return corpus.quarter(date)
    return date[:4]


def counts_for(spec: str) -> collections.Counter:
    counter: collections.Counter = collections.Counter()
    for date, _, body in corpus.load():
        if bucket_of(date, spec) == spec:
            counter.update(corpus.tokens(body))
    return counter


def log_odds(a: collections.Counter, b: collections.Counter, prior: collections.Counter, alpha: float = 0.01):
    """z-scores for every word: positive means over-represented in `a`."""
    n_a, n_b = sum(a.values()), sum(b.values())
    n_prior = sum(prior.values())
    a0 = alpha * n_prior  # total prior mass

    scores = {}
    for word, prior_count in prior.items():
        # Prior pseudo-count for this word, scaled to a0.
        ap = a0 * prior_count / n_prior
        ya, yb = a.get(word, 0), b.get(word, 0)
        if ya + yb == 0:
            continue
        # log-odds in each corpus, smoothed by the prior
        la = math.log((ya + ap) / (n_a + a0 - ya - ap))
        lb = math.log((yb + ap) / (n_b + a0 - yb - ap))
        delta = la - lb
        var = 1.0 / (ya + ap) + 1.0 / (yb + ap)
        scores[word] = delta / math.sqrt(var)
    return scores


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("period_a", help="e.g. 2024, 2024H1, 2025Q3")
    parser.add_argument("period_b", help="the period to contrast against")
    parser.add_argument("--top", type=int, default=25, help="words to show per side")
    parser.add_argument("--min-count", type=int, default=20, help="ignore words rarer than this overall")
    args = parser.parse_args(argv)

    a, b = counts_for(args.period_a), counts_for(args.period_b)
    if not a or not b:
        print("one of the periods matched no issues", file=sys.stderr)
        return 1

    prior: collections.Counter = collections.Counter()
    for _, _, body in corpus.load():
        prior.update(corpus.tokens(body))
    prior = collections.Counter({w: c for w, c in prior.items() if c >= args.min_count})

    scores = log_odds(a, b, prior)
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])

    n_a, n_b = sum(a.values()), sum(b.values())
    print(f"Log-odds z-scores, informative Dirichlet prior (Monroe et al. 2008)")
    print(f"{args.period_a}: {n_a:,} tokens   vs   {args.period_b}: {n_b:,} tokens")
    print(f"|z| > 1.96 is significant at p < 0.05\n")

    print(f"--- distinctive of {args.period_a} ---")
    for word, z in ranked[: args.top]:
        print(f"  {z:7.1f}  {word:<28} ({a.get(word,0):>6,} vs {b.get(word,0):>6,})")
    print(f"\n--- distinctive of {args.period_b} ---")
    for word, z in ranked[-args.top :][::-1]:
        print(f"  {z:7.1f}  {word:<28} ({a.get(word,0):>6,} vs {b.get(word,0):>6,})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
