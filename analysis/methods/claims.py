#!/usr/bin/env python3
"""Extract the numbers asserted in the prose and turn them into curves.

The bodies are dense with quantitative claims — "$1.25 / $4.25 per 1M input/output
tokens", "82.9% on Terminal-Bench 2.1", "1 million token context", "671B
parameters". None of it is in the front-matter tags, so every other analysis in
this repo is blind to it.

Normalizing those into `(date, metric, value, subject)` gives the field's own
price and capability curves **as claimed at the time**, which is one of the few
outputs here that can be checked against what actually happened.

Extraction is deliberately conservative. An earlier loose pass matched `35% on a
Sunday` and `0% on the first replay pass`; benchmark names are therefore required
to look like benchmarks (contain a digit, a hyphen, or match a known suffix), and
prices must carry explicit per-token units.

Usage:
    python3 analysis/methods/claims.py
"""

from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import corpus  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = REPO / "analysis" / "claims.md"

# $X per 1M tokens, or $X/1M, with optional input/output qualifier.
PRICE = re.compile(
    r"\$\s?(\d+(?:\.\d+)?)\s*(?:/|per\s+)\s*(?:1\s?)?M(?:illion)?\s*(?:input|output|in|out)?\s*tokens?",
    re.I,
)
# NN.N% on <benchmark>, where the benchmark has to look like one.
BENCH = re.compile(
    r"(\d{1,3}(?:\.\d+)?)\s?%\s+on\s+(?:the\s+)?([A-Za-z][\w\-\.\+]{2,24})",
    re.I,
)
BENCH_OK = re.compile(r"bench|eval|arc|mmlu|gpqa|aime|imo|ioi|swe|hle|gsm|humaneval|math|glue|agi|\d", re.I)
# Context windows: 1M / 200K token context.
CTX = re.compile(r"(\d+(?:\.\d+)?)\s?([MK])\s*(?:token|context)[\w\s-]{0,12}(?:context|window|length)?", re.I)
# Parameter counts: 671B parameters, 27B model.
PARAM = re.compile(r"(\d+(?:\.\d+)?)\s?([BTM])\s*(?:total\s+|active\s+)?param", re.I)


def scale(value: float, unit: str) -> float:
    return value * {"K": 1e3, "M": 1e6, "B": 1e9, "T": 1e12}[unit.upper()]


def collect() -> dict[str, list[tuple[str, float, str]]]:
    out: dict[str, list[tuple[str, float, str]]] = collections.defaultdict(list)
    for date, _, body in corpus.load(drop_discord=True):
        for m in PRICE.finditer(body):
            v = float(m.group(1))
            if 0.005 <= v <= 1000:
                out["price"].append((date, v, ""))
        for m in BENCH.finditer(body):
            name = m.group(2).strip(".").lower()
            v = float(m.group(1))
            if v <= 100 and BENCH_OK.search(name):
                out["benchmark"].append((date, v, name))
        for m in CTX.finditer(body):
            v = scale(float(m.group(1)), m.group(2))
            if 1e3 <= v <= 1e8:
                out["context"].append((date, v, ""))
        for m in PARAM.finditer(body):
            v = scale(float(m.group(1)), m.group(2))
            if 1e8 <= v <= 1e13:
                out["params"].append((date, v, ""))
    return out


def by_period(rows: list[tuple[str, float, str]], fn) -> dict[str, float]:
    buckets: dict[str, list[float]] = collections.defaultdict(list)
    for date, value, _ in rows:
        buckets[corpus.half(date)].append(value)
    return {p: float(fn(v)) for p, v in sorted(buckets.items()) if len(v) >= 5}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--top-benchmarks", type=int, default=15)
    args = parser.parse_args(argv)

    data = collect()
    lines = [
        "# Numbers the archive asserted",
        "",
        "Extracted by `analysis/methods/claims.py` from the issue bodies. None of this is",
        "in the front-matter tags, so every tag-based analysis in this repo is blind to it.",
        "",
        "| Claim type | Extracted |",
        "|---|---|",
    ]
    for key in ("price", "benchmark", "context", "params"):
        lines.append(f"| {key} | {len(data.get(key, [])):,} |")
    lines.append("")

    # --- Price -----------------------------------------------------------
    med = by_period(data["price"], np.median)
    p10 = by_period(data["price"], lambda v: np.percentile(v, 10))
    lines += [
        "## Claimed price per 1M tokens",
        "",
        "Median and 10th percentile of every `$X per 1M tokens` claim in each period.",
        "The 10th percentile tracks the cheap frontier — the budget option available at",
        "the time — while the median tracks what was typically being discussed.",
        "",
        "| Period | Claims | Median $/1M | 10th pct $/1M |",
        "|---|---|---|---|",
    ]
    counts = collections.Counter(corpus.half(d) for d, _, _ in data["price"])
    for period in sorted(med):
        lines.append(f"| {period} | {counts[period]} | ${med[period]:.2f} | ${p10[period]:.2f} |")
    if len(med) >= 2:
        first, last = min(med), max(med)
        lines += [
            "",
            f"Median claimed price moved **${med[first]:.2f} → ${med[last]:.2f}** "
            f"({first} → {last}), and the cheap frontier "
            f"**${p10[first]:.2f} → ${p10[last]:.2f}**.",
            "",
        ]

    # --- Context ---------------------------------------------------------
    ctx_med = by_period(data["context"], np.median)
    ctx_max = by_period(data["context"], np.max)
    lines += [
        "## Claimed context windows",
        "",
        "| Period | Claims | Median | Largest claimed |",
        "|---|---|---|---|",
    ]
    ctx_counts = collections.Counter(corpus.half(d) for d, _, _ in data["context"])
    for period in sorted(ctx_med):
        lines.append(
            f"| {period} | {ctx_counts[period]} | {ctx_med[period]/1000:,.0f}K | {ctx_max[period]/1e6:,.1f}M |"
        )
    lines.append("")

    # --- Params ----------------------------------------------------------
    par_med = by_period(data["params"], np.median)
    par_max = by_period(data["params"], np.max)
    lines += ["## Claimed parameter counts", "", "| Period | Claims | Median | Largest |", "|---|---|---|---|"]
    par_counts = collections.Counter(corpus.half(d) for d, _, _ in data["params"])
    for period in sorted(par_med):
        lines.append(
            f"| {period} | {par_counts[period]} | {par_med[period]/1e9:,.0f}B | {par_max[period]/1e9:,.0f}B |"
        )
    lines.append("")

    # --- Benchmarks ------------------------------------------------------
    names = collections.Counter(n for _, _, n in data["benchmark"])
    lines += [
        "## Benchmarks by how often a score was claimed",
        "",
        "Each benchmark's first and last claimed score dates its era. A benchmark that",
        "stops being cited has usually been saturated.",
        "",
        "| Benchmark | Claims | First | Last | Median score |",
        "|---|---|---|---|---|",
    ]
    for name, count in names.most_common(args.top_benchmarks):
        rows = [(d, v) for d, v, n in data["benchmark"] if n == name]
        lines.append(
            f"| {name} | {count} | {min(d for d, _ in rows)} | {max(d for d, _ in rows)} | "
            f"{np.median([v for _, v in rows]):.0f}% |"
        )
    lines += [
        "",
        "*Caveat:* subjects are not resolved — a claimed score is not attributed to the",
        "model it belongs to, so these are field-level distributions, not per-model",
        "results. Attribution needs the sentence parsed, not just matched.",
        "",
    ]

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    for key in ("price", "benchmark", "context", "params"):
        print(f"  {key:<10} {len(data.get(key, [])):>6,}")
    if med:
        print("\nmedian $/1M by period:", ", ".join(f"{p}=${v:.2f}" for p, v in sorted(med.items())))
    if ctx_med:
        print("median context:", ", ".join(f"{p}={v/1000:.0f}K" for p, v in sorted(ctx_med.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
