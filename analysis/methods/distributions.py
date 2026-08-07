#!/usr/bin/env python3
"""Rank-turbulence divergence and diversity metrics over the entity distribution.

Two questions the frequency work could not answer properly.

**Which entities most distinguish two periods?** `logodds.py` answers this by
frequency, which needs a prior to cope with zeros and understates the case where
something is simply absent from one side. Rank-turbulence divergence (Dodds et
al. 2020, EPJ Data Science) is rank-based and handles absence natively — exactly
the `kimi: 0 → 2,185` case, the cleanest statistic in the whole analysis and the
one log-odds handles least gracefully. The alpha parameter tunes whether the head
or the tail of the distribution dominates.

**Is attention concentrating or fragmenting?** Promised in `IDEAS.md` and never
delivered. Treating entities as species makes the ecology toolkit apply directly:
Shannon entropy, Gini, and Hill numbers, which are entropies converted into an
"effective number of entities" and therefore actually interpretable — Hill-1 of 12
means the period's coverage was equivalent to 12 equally-discussed entities.

Usage:
    python3 analysis/methods/distributions.py
    python3 analysis/methods/distributions.py --alpha 0.5 --compare 2024H1 2026H1
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import corpus  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
INDEX = REPO / "analysis" / "index.json"
OUT = REPO / "analysis" / "distributions.md"


def entity_counts() -> dict[str, collections.Counter]:
    """Company mentions per period, from the front-matter tags."""
    records = json.loads(INDEX.read_text(encoding="utf-8"))
    out: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for record in records:
        period = corpus.half(record["date"])
        for company in {c.strip().lower() for c in record.get("companies", []) if c.strip()}:
            out[period][company] += 1
    return dict(out)


def ranks(counter: collections.Counter) -> dict[str, float]:
    """Competition ranking with ties averaged; rank 1 is most frequent."""
    items = sorted(counter.items(), key=lambda kv: -kv[1])
    out: dict[str, float] = {}
    i = 0
    while i < len(items):
        j = i
        while j + 1 < len(items) and items[j + 1][1] == items[i][1]:
            j += 1
        shared = (i + j) / 2 + 1
        for k in range(i, j + 1):
            out[items[k][0]] = shared
        i = j + 1
    return out


def rtd(a: collections.Counter, b: collections.Counter, alpha: float = 1 / 3):
    """Rank-turbulence divergence with per-element contributions.

    Elements missing from one side are placed at a 'last place' rank just beyond
    that side's observed maximum — the exclusive-type convention from the paper,
    which is what lets absence be scored rather than dropped.
    """
    ra, rb = ranks(a), ranks(b)
    last_a = max(ra.values(), default=1) + 1
    last_b = max(rb.values(), default=1) + 1
    contributions = {}
    for element in set(ra) | set(rb):
        x = ra.get(element, last_a)
        y = rb.get(element, last_b)
        contributions[element] = abs(x ** (-alpha) - y ** (-alpha)) ** (1 / (alpha + 1))
    total = sum(contributions.values())
    return total, contributions, ra, rb


def diversity(counter: collections.Counter) -> dict[str, float]:
    counts = np.asarray(list(counter.values()), dtype=float)
    p = counts / counts.sum()
    shannon = float(-(p * np.log(p)).sum())
    simpson = float((p**2).sum())
    order = np.sort(p)[::-1]
    n = len(order)
    # Gini over the mention distribution: 0 = perfectly even, 1 = one entity takes all.
    idx = np.arange(1, n + 1)
    gini = float((2 * (idx * np.sort(p)).sum()) / (n * p.sum()) - (n + 1) / n)
    return {
        "richness": float(n),
        "shannon": shannon,
        "hill1": float(np.exp(shannon)),
        "hill2": float(1 / simpson),
        "gini": gini,
        "top3_share": float(order[:3].sum() * 100),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--alpha", type=float, default=1 / 3, help="RTD tuning; lower emphasises the tail")
    parser.add_argument("--compare", nargs=2, default=["2024H1", "2026H1"])
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args(argv)

    periods = entity_counts()
    order = sorted(periods)

    lines = [
        "# Distributional structure of attention",
        "",
        "Computed by `analysis/methods/distributions.py` over the front-matter company",
        "tags.",
        "",
        "## Diversity: is attention concentrating or fragmenting?",
        "",
        "**Hill numbers** are entropies expressed as an *effective number of entities*,",
        "which makes them directly readable: Hill-1 of 12 means the period's coverage was",
        "equivalent to 12 equally-discussed companies. Hill-2 weights the dominant",
        "entities more heavily.",
        "",
        "| Period | Distinct | Hill-1 (effective) | Hill-2 | Shannon | Gini | Top-3 share |",
        "|---|---|---|---|---|---|---|",
    ]
    for period in order:
        d = diversity(periods[period])
        lines.append(
            f"| {period} | {d['richness']:.0f} | **{d['hill1']:.1f}** | {d['hill2']:.1f} | "
            f"{d['shannon']:.2f} | {d['gini']:.2f} | {d['top3_share']:.0f}% |"
        )

    first, last = order[0], order[-1]
    d0, d1 = diversity(periods[first]), diversity(periods[last])
    lines += [
        "",
        f"Effective number of companies moved **{d0['hill1']:.1f} → {d1['hill1']:.1f}** "
        f"({first} → {last}), against a raw count of {d0['richness']:.0f} → {d1['richness']:.0f}.",
        "",
    ]

    # --- RTD -------------------------------------------------------------
    a_name, b_name = args.compare
    if a_name in periods and b_name in periods:
        total, contrib, ra, rb = rtd(periods[a_name], periods[b_name], args.alpha)
        ranked = sorted(contrib.items(), key=lambda kv: -kv[1])
        lines += [
            f"## Rank-turbulence divergence: {a_name} vs {b_name}",
            "",
            f"Total divergence **{total:.2f}** at alpha={args.alpha:.2f}. Elements absent from one",
            "side are ranked just past that side's last place, so absence contributes rather",
            "than being dropped — the reason this complements the log-odds view.",
            "",
            f"| Entity | Rank {a_name} | Rank {b_name} | Contribution | Direction |",
            "|---|---|---|---|---|",
        ]
        for entity, score in ranked[: args.top]:
            x = f"{ra[entity]:.0f}" if entity in ra else "—"
            y = f"{rb[entity]:.0f}" if entity in rb else "—"
            if entity not in ra:
                direction = f"new in {b_name}"
            elif entity not in rb:
                direction = f"gone by {b_name}"
            else:
                direction = "rose" if rb[entity] < ra[entity] else "fell"
            lines.append(f"| {entity} | {x} | {y} | {score:.3f} | {direction} |")
        lines.append("")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    print(f"{'period':<9}{'distinct':>9}{'Hill-1':>9}{'Gini':>7}{'top3':>7}")
    for period in order:
        d = diversity(periods[period])
        print(f"{period:<9}{d['richness']:>9.0f}{d['hill1']:>9.1f}{d['gini']:>7.2f}{d['top3_share']:>6.0f}%")
    if a_name in periods and b_name in periods:
        total, contrib, _, _ = rtd(periods[a_name], periods[b_name], args.alpha)
        top = sorted(contrib.items(), key=lambda kv: -kv[1])[:8]
        print(f"\nRTD {a_name} vs {b_name} = {total:.2f}; top: " + ", ".join(k for k, _ in top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
