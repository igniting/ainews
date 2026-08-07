#!/usr/bin/env python3
"""Novelty / Transience / Resonance (Barron, Huang, Spang & DeDeo, PNAS 2018).

Originally applied to speeches in the French National Constituent Assembly to
find which interventions actually changed the debate. It answers the question I
got wrong by eyeballing headlines: **which days genuinely shifted the
conversation, as opposed to merely being loud?**

For each issue, represent it as a topic distribution, then measure:

- **Novelty** — mean KL divergence from the *preceding* w issues. How different
  was this day from what came right before?
- **Transience** — mean KL divergence to the *following* w issues. How quickly
  did the field go back to what it was doing?
- **Resonance** = novelty − transience. Did the new material *stick*?

The distinction is the whole point. A one-off release with a big launch spike is
high-novelty, high-transience, near-zero resonance: loud, then gone. A genuine
turning point is high-novelty *and* low-transience — the conversation changed and
stayed changed. Ranking by novelty alone finds press releases; ranking by
resonance finds inflection points.

This is what should have identified Meta's inflection instead of my picking a
dramatic headline (`VERIFICATION.md` — the decline had started six months
earlier, and the loud Llama 4 day was pure transience).

Usage:
    python3 analysis/methods/novelty.py --topics 40 --window 20
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import numpy as np
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import corpus  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = REPO / "analysis" / "turning-points.md"


def kl(p: np.ndarray, q: np.ndarray) -> float:
    """KL(p||q) for topic distributions, both already strictly positive."""
    return float(np.sum(p * np.log(p / q)))


def ntr(theta: np.ndarray, window: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Novelty, transience and resonance for every document."""
    n = len(theta)
    novelty = np.full(n, np.nan)
    transience = np.full(n, np.nan)
    for i in range(n):
        if i - window < 0 or i + window >= n:
            continue
        novelty[i] = np.mean([kl(theta[i], theta[j]) for j in range(i - window, i)])
        transience[i] = np.mean([kl(theta[i], theta[j]) for j in range(i + 1, i + window + 1)])
    return novelty, transience, novelty - transience


def _local_z(x: np.ndarray, span: int) -> np.ndarray:
    """z-score each point against the +/- span window around it."""
    out = np.full(len(x), np.nan)
    for i in range(len(x)):
        lo, hi = max(0, i - span), min(len(x), i + span + 1)
        w = x[lo:hi]
        w = w[~np.isnan(w)]
        if len(w) < 5 or np.isnan(x[i]):
            continue
        sd = w.std()
        if sd > 0:
            out[i] = (x[i] - w.mean()) / sd
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--topics", type=int, default=40)
    parser.add_argument("--window", type=int, default=20, help="issues before/after to compare against")
    parser.add_argument("--max-features", type=int, default=8000)
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument(
        "--since",
        default="2024-04-01",
        help="issue length grew 8k -> 27k words between Dec 2023 and Mar 2024, and that "
        "structural expansion swamps the KL signal; default skips it",
    )
    parser.add_argument("--until", default="2099-12-31")
    parser.add_argument(
        "--baseline", type=int, default=60, help="issues either side used as the local baseline"
    )
    parser.add_argument(
        "--raw", dest="standardize", action="store_false", help="skip local standardization"
    )
    args = parser.parse_args(argv)

    docs = [d for d in corpus.load() if args.since <= d[0] <= args.until]
    dates = [d for d, _, _ in docs]
    titles = {d: f for d, f, _ in docs}
    texts = [" ".join(corpus.tokens(b)) for _, _, b in docs]

    print(f"vectorizing {len(texts)} issues…", file=sys.stderr)
    vec = CountVectorizer(max_features=args.max_features, min_df=5, max_df=0.85)
    X = vec.fit_transform(texts)

    print(f"fitting LDA, {args.topics} topics…", file=sys.stderr)
    lda = LatentDirichletAllocation(
        n_components=args.topics, random_state=0, learning_method="online", max_iter=25, n_jobs=-1
    )
    theta = lda.fit_transform(X)
    theta = (theta + 1e-12) / (theta + 1e-12).sum(axis=1, keepdims=True)

    novelty, transience, resonance = ntr(theta, args.window)

    # Raw novelty falls ~15x across the corpus (2.34 in 2024H2 to 0.15 in 2025H2)
    # as the issues become more templated, so raw resonance is not comparable
    # across eras — an unstandardized ranking is just a list of 2024 dates.
    # Standardize within a rolling local baseline so a turning point is measured
    # against its own neighbourhood.
    if args.standardize:
        novelty = _local_z(novelty, args.baseline)
        transience = _local_z(transience, args.baseline)
        resonance = novelty - transience

    valid = ~np.isnan(resonance)

    order_res = np.argsort(np.where(valid, -resonance, np.inf))
    order_nov = np.argsort(np.where(valid, -novelty, np.inf))

    lines = [
        "# Turning points",
        "",
        "Novelty / Transience / Resonance (Barron et al., PNAS 2018), computed by",
        "`analysis/methods/novelty.py` over LDA topic distributions of the issue bodies.",
        "",
        "- **Novelty** — how different an issue is from the preceding "
        f"{args.window} issues.",
        "- **Transience** — how fast the conversation reverts afterwards.",
        "- **Resonance** = novelty − transience. High resonance means the change *stuck*.",
        "",
        "Ranking by novelty finds loud days. Ranking by resonance finds the days the",
        "field actually changed direction — which is the distinction that title-based",
        "analysis cannot make.",
        "",
        f"*{args.topics} topics, window {args.window}, {X.shape[1]} vocabulary terms, "
        f"{len(docs)} issues from {dates[0]} to {dates[-1]}.*",
        "",
        "> Restricted to 2024-04 onward by default: median issue length grew from 8,040",
        "> words (Dec 2023) to 26,850 (Mar 2024), and that structural expansion produces",
        "> far larger KL divergences than any news event. Run with `--since 2023-12-01`",
        "> to see it dominate the rankings.",
        ">",
        "> Novelty and transience are z-scored against a local baseline of "
        f"+/-{args.baseline} issues:",
        "> raw novelty falls ~15x from 2024H2 to 2025H2 as the issues get more templated,",
        "> so an unstandardized ranking returns a list of 2024 dates and nothing else.",
        "",
        "## Highest resonance — the conversation changed and stayed changed",
        "",
        "| Date | Issue | Novelty | Transience | Resonance |",
        "|---|---|---|---|---|",
    ]
    for i in order_res[: args.top]:
        lines.append(
            f"| {dates[i]} | {titles[dates[i]][9:-3]} | {novelty[i]:.3f} | "
            f"{transience[i]:.3f} | **{resonance[i]:.3f}** |"
        )

    lines += [
        "",
        "## Highest novelty — loud days (many of which did not stick)",
        "",
        "| Date | Issue | Novelty | Transience | Resonance |",
        "|---|---|---|---|---|",
    ]
    for i in order_nov[: args.top]:
        lines.append(
            f"| {dates[i]} | {titles[dates[i]][9:-3]} | **{novelty[i]:.3f}** | "
            f"{transience[i]:.3f} | {resonance[i]:.3f} |"
        )

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    print("\ntop resonance:")
    for i in order_res[:10]:
        print(f"  {dates[i]}  res={resonance[i]:+.3f}  {titles[dates[i]][9:-3][:58]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
