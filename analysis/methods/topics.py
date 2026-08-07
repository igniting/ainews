#!/usr/bin/env python3
"""Discover topics from the corpus instead of naming them by hand.

`analysis/domains.py` has a structural bias I could not fix from inside it: I
chose its 16 domains myself and wrote regexes for them, so it can only find
categories I already thought of. This lets the corpus propose its own.

NMF on a TF-IDF matrix, which for this corpus beats LDA on two counts: it gives
sharper, less overlapping topics on medium-sized vocabularies, and it is
deterministic given a seed, so the topic set is stable across reruns.

Topics are then tracked as **mean document-topic weight per period** — a within-
document proportion, so it is not distorted by issue length falling from ~28k to
~5.8k words. Trend is measured as the slope of that share over periods, which
surfaces steadily-rising and steadily-fading topics rather than one-off spikes.

Usage:
    python3 analysis/methods/topics.py --topics 24
    python3 analysis/methods/topics.py --topics 30 --since 2024-05-20
"""

from __future__ import annotations

import argparse
import collections
import pathlib
import sys

import numpy as np
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import corpus  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = REPO / "analysis" / "topics.md"


def label(terms: list[str]) -> str:
    return ", ".join(terms[:6])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--topics", type=int, default=24)
    parser.add_argument("--max-features", type=int, default=12000)
    parser.add_argument("--since", default="2023-12-01")
    parser.add_argument("--until", default="2099-12-31")
    args = parser.parse_args(argv)

    docs = [d for d in corpus.load(drop_discord=True) if args.since <= d[0] <= args.until]
    dates = [d for d, _, _ in docs]
    texts = [" ".join(corpus.tokens(b, drop_handles=True)) for _, _, b in docs]
    print(f"{len(docs)} issues, {dates[0]}..{dates[-1]}", file=sys.stderr)

    vec = TfidfVectorizer(max_features=args.max_features, min_df=8, max_df=0.7, sublinear_tf=True)
    X = vec.fit_transform(texts)
    vocab = np.asarray(vec.get_feature_names_out())

    print(f"fitting NMF, {args.topics} topics over {X.shape[1]} terms…", file=sys.stderr)
    nmf = NMF(n_components=args.topics, random_state=0, init="nndsvda", max_iter=600)
    W = nmf.fit_transform(X)
    H = nmf.components_

    # Normalize each document's topic weights to a proportion, so long and short
    # issues contribute equally.
    W = W / np.where(W.sum(axis=1, keepdims=True) > 0, W.sum(axis=1, keepdims=True), 1)

    periods = sorted({corpus.half(d) for d in dates})
    idx = collections.defaultdict(list)
    for i, d in enumerate(dates):
        idx[corpus.half(d)].append(i)
    share = np.asarray([[W[idx[p], k].mean() * 100 for p in periods] for k in range(args.topics)])

    terms = [list(vocab[np.argsort(-H[k])[:12]]) for k in range(args.topics)]

    # Slope of share across periods = steady trend, not a one-off spike.
    x = np.arange(len(periods))
    slope = np.asarray([np.polyfit(x, share[k], 1)[0] for k in range(args.topics)])
    order = np.argsort(-slope)

    lines = [
        "# Topics the corpus proposed for itself",
        "",
        "NMF over TF-IDF of the issue bodies, via `analysis/methods/topics.py`.",
        "No category list was supplied — unlike `domains.py`, whose 16 domains I chose",
        "by hand and which therefore could only find things I had already thought of.",
        "",
        "Values are mean document-topic share per period (%), a within-document",
        "proportion, so the 2026 collapse in issue length does not distort them.",
        "",
        f"*{args.topics} topics, {len(docs)} issues, {dates[0]} to {dates[-1]}.*",
        "",
        "## Rising topics",
        "",
        "| Trend | Top terms | " + " | ".join(periods) + " |",
        "|---|---|" + "|".join(["---"] * len(periods)) + "|",
    ]
    for k in order[:8]:
        lines.append(
            f"| **{slope[k]:+.2f}** | {label(terms[k])} | "
            + " | ".join(f"{v:.1f}" for v in share[k])
            + " |"
        )

    lines += [
        "",
        "## Fading topics",
        "",
        "| Trend | Top terms | " + " | ".join(periods) + " |",
        "|---|---|" + "|".join(["---"] * len(periods)) + "|",
    ]
    for k in order[-8:][::-1]:
        lines.append(
            f"| **{slope[k]:+.2f}** | {label(terms[k])} | "
            + " | ".join(f"{v:.1f}" for v in share[k])
            + " |"
        )

    lines += ["", "## All topics", "", "| # | Top terms | Peak period | Peak share |", "|---|---|---|---|"]
    for k in range(args.topics):
        peak = int(np.argmax(share[k]))
        lines.append(f"| {k} | {', '.join(terms[k][:10])} | {periods[peak]} | {share[k][peak]:.1f}% |")
    lines.append("")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    print("\nrising:")
    for k in order[:6]:
        print(f"  {slope[k]:+.2f}  {label(terms[k])}")
    print("fading:")
    for k in order[-6:][::-1]:
        print(f"  {slope[k]:+.2f}  {label(terms[k])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
