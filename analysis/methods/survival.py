#!/usr/bin/env python3
"""How long does a model stay in the conversation? Kaplan-Meier survival curves.

The arcs in `NEWS-ANALYSIS.md` are anecdotes: I picked companies and described
what happened to them. This turns "how long does a model stay relevant" into an
estimate over every model in the corpus, with the censoring handled properly.

Handling censoring is the whole reason to use survival analysis rather than
averaging lifespans. A model first mentioned last month and still discussed today
has *not* had a one-month life — its life is unfinished. Averaging raw spans
systematically understates lifespan, and understates it worst for the newest
models, which is exactly the comparison you want to make. Kaplan-Meier uses the
censored cases for the periods they were observed and stops counting them after.

- **Birth** — first issue mentioning the model.
- **Death** — last mention, if that is more than `--silence` days before the
  corpus ends. Otherwise the model is treated as alive and right-censored.

Lifelines does not build in this environment, so the estimator is implemented
directly; it is a product-limit formula and short.

Usage:
    python3 analysis/methods/survival.py
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import pathlib
import re
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
INDEX = REPO / "analysis" / "index.json"
OUT = REPO / "analysis" / "survival.md"

CHINA = re.compile(r"qwen|deepseek|kimi|glm|minimax|hunyuan|yi-|ernie|baichuan|intern|step-|zhipu|moonshot|wan|seed", re.I)
US_LAB = re.compile(r"^(gpt|claude|gemini|llama|grok|^o[134]|codex|phi|command|dall|sora|gemma|mistral|mixtral|nemotron)", re.I)
OPENISH = re.compile(r"llama|qwen|deepseek|mistral|mixtral|gemma|olmo|phi|glm|kimi|minimax|falcon|nemotron|smol", re.I)


# Strip version and size suffixes so a persistent family is one subject rather than
# a dozen short-lived tags: qwen3.5-235b-a22b, qwen3.6, qwen3.8-max -> qwen3.
VERSION = re.compile(r"[-_]?\d+(\.\d+)*([bkm]\b)?", re.I)
SIZE = re.compile(r"[-_](\d+x)?\d+[bkm](-a\d+[bkm])?\b|[-_](mini|nano|small|medium|large|max|pro|ultra|"
                  r"flash|turbo|instruct|base|chat|thinking|preview|exp|it|vl|coder|reasoner)\b", re.I)


def collapse(model: str) -> str:
    """Reduce a model tag to its family stem."""
    s = model.lower().strip()
    prev = None
    while prev != s:
        prev = s
        s = SIZE.sub("", s)
    s = VERSION.sub("", s).strip("-_. ")
    return s or model.lower()


def kaplan_meier(durations: np.ndarray, observed: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Product-limit estimator. Returns (times, survival probability)."""
    order = np.argsort(durations)
    durations, observed = durations[order], observed[order]
    times, surv = [0.0], [1.0]
    at_risk = len(durations)
    s = 1.0
    for t in np.unique(durations):
        deaths = int(((durations == t) & (observed == 1)).sum())
        censored = int(((durations == t) & (observed == 0)).sum())
        if at_risk > 0 and deaths > 0:
            s *= 1 - deaths / at_risk
            times.append(float(t))
            surv.append(s)
        at_risk -= deaths + censored
    return np.asarray(times), np.asarray(surv)


def median_survival(times: np.ndarray, surv: np.ndarray) -> float:
    below = np.where(surv <= 0.5)[0]
    return float(times[below[0]]) if len(below) else float("nan")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--silence", type=int, default=90, help="days without a mention before a model counts as dead")
    parser.add_argument("--min-issues", type=int, default=3, help="ignore models mentioned fewer times")
    parser.add_argument(
        "--family",
        action="store_true",
        help="group version variants into families (qwen3.5/3.6/3.8 -> qwen3) before fitting; "
        "tests whether the Chinese-cohort gap is a naming artifact of faster version churn",
    )
    args = parser.parse_args(argv)

    records = json.loads(INDEX.read_text(encoding="utf-8"))
    seen: dict[str, list[str]] = collections.defaultdict(list)
    for record in records:
        for model in {m.strip().lower() for m in record.get("models", []) if m.strip()}:
            seen[collapse(model) if args.family else model].append(record["date"])

    end = dt.date.fromisoformat(max(r["date"] for r in records))
    rows = []
    for model, dates in seen.items():
        if len(dates) < args.min_issues:
            continue
        birth = dt.date.fromisoformat(min(dates))
        last = dt.date.fromisoformat(max(dates))
        dead = (end - last).days > args.silence
        rows.append((model, (last - birth).days, 1 if dead else 0))

    def group(pred) -> tuple[np.ndarray, np.ndarray, int]:
        sel = [r for r in rows if pred(r[0])]
        return (
            np.asarray([r[1] for r in sel], dtype=float),
            np.asarray([r[2] for r in sel]),
            len(sel),
        )

    groups = {
        "All models": group(lambda m: True),
        "Chinese labs": group(lambda m: bool(CHINA.search(m))),
        "US frontier labs": group(lambda m: bool(US_LAB.search(m)) and not CHINA.search(m)),
        "Open-weights families": group(lambda m: bool(OPENISH.search(m))),
        "Other / closed": group(lambda m: not OPENISH.search(m)),
    }

    lines = [
        "# How long models stay in the conversation",
        "",
        "Kaplan-Meier survival estimates from `analysis/methods/survival.py`.",
        "",
        f"A model is **dead** if it has not been mentioned in the last {args.silence} days of",
        "the corpus, and **right-censored** (still alive) otherwise. Censoring is the point:",
        "a model first seen recently and still discussed has an unfinished life, and",
        "averaging raw spans would understate exactly the newest models you most want to",
        "compare.",
        "",
        "| Cohort | Models | Died | Still alive | Median lifespan | 25% gone by | 75% gone by |",
        "|---|---|---|---|---|---|---|",
    ]
    for name, (dur, obs, n) in groups.items():
        if n < 10:
            continue
        times, surv = kaplan_meier(dur, obs)
        med = median_survival(times, surv)
        q25 = next((t for t, s in zip(times, surv) if s <= 0.75), float("nan"))
        q75 = next((t for t, s in zip(times, surv) if s <= 0.25), float("nan"))
        lines.append(
            f"| {name} | {n} | {int(obs.sum())} | {n-int(obs.sum())} | "
            f"{med:.0f} d | {q25:.0f} d | {q75:.0f} d |"
        )

    longest = sorted(rows, key=lambda r: -r[1])[:20]
    lines += [
        "",
        "## Longest-lived models",
        "",
        "| Model | Days from first to last mention | Status |",
        "|---|---|---|",
    ]
    for model, days, dead in longest:
        lines.append(f"| {model} | {days} | {'ended' if dead else 'still active'} |")
    lines.append("")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    for name, (dur, obs, n) in groups.items():
        if n < 10:
            continue
        times, surv = kaplan_meier(dur, obs)
        print(f"  {name:<24} n={n:<4} median={median_survival(times, surv):.0f}d  died={int(obs.sum())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
