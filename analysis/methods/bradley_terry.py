#!/usr/bin/env python3
"""A capability ranking derived from what the discourse asserted.

The archive is dense in dated pairwise comparative claims — "Mixtral beats
GPT3.5", "QwQ-32B claims to match DeepSeek R1", "beating Claude 4 Sonnet at 11%
of its cost". Extracting those as `(winner, loser, date)` triples and fitting a
Bradley-Terry model yields a latent capability score per model **as claimed by
the field at the time**, which can then be compared against what actually turned
out to be true.

Bradley-Terry (Zermelo 1929; Bradley & Terry 1952) assumes each item has a latent
strength and P(a beats b) = pi_a / (pi_a + pi_b). Fitted here with Hunter's (2004)
MM algorithm, which is monotonically convergent and needs no gradient tuning.

Two details that matter for validity:

- Only the **largest connected component** of the comparison graph is scored.
  Bradley-Terry strengths are unidentifiable across components — two models never
  compared, even transitively, have no defined relative strength, and fitting
  anyway invents one.
- A Bayesian prior (one virtual win and loss against a phantom average opponent)
  keeps undefeated or winless models finite instead of running to +/-infinity.

**The dominant bias in this data is launch asymmetry.** A model is the *claimant*
when it launches ("Jamba dethrones Mixtral") and the *incumbent* only later, once
rivals launch against it. So rarely-compared models are near-undefeated by
construction. Measured here: mean win rate is 0.68 for models with 3-7
comparisons and 0.49 for those with 41+, correlation between log(comparisons) and
win rate -0.27. The default threshold is therefore high enough that a model must
have served as incumbent too; the script prints the diagnostic so the bias can be
re-checked rather than assumed away.

Usage:
    python3 analysis/methods/bradley_terry.py
    python3 analysis/methods/bradley_terry.py --by-period --min-comparisons 4
"""

from __future__ import annotations

import argparse
import collections
import itertools
import json
import pathlib
import re
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import corpus  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
INDEX = REPO / "analysis" / "index.json"
OUT = REPO / "analysis" / "bradley-terry.md"

# Asymmetric claims (A is better than B) vs symmetric ones (A is level with B).
WIN = r"beats?|beating|outperform\w*|surpass\w*|tops?|topping|crush\w*|destroy\w*|edges? out|better than|ahead of|dethron\w*|overtak\w*|leapfrog\w*"
TIE = r"matche?s?|matching|on par with|comparable to|rivals?|ties? with|level with|-level\b"

SPLIT = re.compile(r"(?<=[.!?])\s+|\n")
# Family-level normalization: version churn (qwen3.5/3.6/3.8) otherwise splits
# one competitor into dozens of nodes with too few comparisons each.
FAMILY = [
    (re.compile(r"^gpt-?5", re.I), "gpt-5"),
    (re.compile(r"^gpt-?4o", re.I), "gpt-4o"),
    (re.compile(r"^gpt-?4", re.I), "gpt-4"),
    (re.compile(r"^gpt-?3", re.I), "gpt-3.5"),
    (re.compile(r"^o[1345](-|$)", re.I), "openai-o-series"),
    (re.compile(r"^codex", re.I), "codex"),
    (re.compile(r"^claude-?3\.5", re.I), "claude-3.5"),
    (re.compile(r"^claude-?3", re.I), "claude-3"),
    (re.compile(r"^claude-?(4|opus-4|sonnet-4)", re.I), "claude-4"),
    (re.compile(r"^claude-?(5|opus-5|fable)", re.I), "claude-5"),
    (re.compile(r"^claude-?code", re.I), "claude-code"),
    (re.compile(r"^claude", re.I), "claude"),
    (re.compile(r"^gemini-?1", re.I), "gemini-1.5"),
    (re.compile(r"^gemini-?2", re.I), "gemini-2"),
    (re.compile(r"^gemini-?3", re.I), "gemini-3"),
    (re.compile(r"^gemini", re.I), "gemini"),
    (re.compile(r"^gemma", re.I), "gemma"),
    (re.compile(r"^llama-?4", re.I), "llama-4"),
    (re.compile(r"^llama-?3", re.I), "llama-3"),
    (re.compile(r"^llama-?2", re.I), "llama-2"),
    (re.compile(r"^(mixtral|mistral-7b|mistral-large|mistral-small)", re.I), "mistral"),
    (re.compile(r"^deepseek-?r", re.I), "deepseek-r1"),
    (re.compile(r"^deepseek-?v", re.I), "deepseek-v3"),
    (re.compile(r"^qwen-?3", re.I), "qwen3"),
    (re.compile(r"^qwen-?2", re.I), "qwen2"),
    (re.compile(r"^qwen", re.I), "qwen"),
    (re.compile(r"^kimi", re.I), "kimi"),
    (re.compile(r"^glm", re.I), "glm"),
    (re.compile(r"^minimax", re.I), "minimax"),
    (re.compile(r"^grok", re.I), "grok"),
    (re.compile(r"^command", re.I), "command-r"),
    (re.compile(r"^phi", re.I), "phi"),
]


def family(model: str) -> str:
    for pattern, name in FAMILY:
        if pattern.match(model):
            return name
    return model


def lexicon(min_issues: int) -> dict[str, str]:
    """Surface form → family, built from the front-matter `models` vocabulary."""
    records = json.loads(INDEX.read_text(encoding="utf-8"))
    counts: collections.Counter = collections.Counter()
    for record in records:
        counts.update({m.strip().lower() for m in record.get("models", []) if m.strip()})
    out = {}
    for model, count in counts.items():
        if count < min_issues or len(model) < 3:
            continue
        out[model] = family(model)
    return out


def extract(lex: dict[str, str]) -> list[tuple[str, str, str, str]]:
    """(date, winner, loser, kind) triples; kind is 'win' or 'tie'."""
    # Longest-first so "gpt-4o" wins over "gpt-4".
    surfaces = sorted(lex, key=len, reverse=True)
    finder = re.compile(r"(?<![\w-])(" + "|".join(re.escape(s) for s in surfaces) + r")(?![\w-])", re.I)
    win_re = re.compile(rf"\b({WIN})\b", re.I)
    tie_re = re.compile(rf"\b({TIE})", re.I)

    out = []
    for date, _, body in corpus.load(drop_discord=True):
        for sentence in SPLIT.split(body):
            if len(sentence) > 600 or len(sentence) < 15:
                continue
            hits = [(m.start(), lex[m.group(1).lower()]) for m in finder.finditer(sentence)]
            if len(hits) < 2:
                continue
            for (pos_a, a), (pos_b, b) in itertools.combinations(hits, 2):
                if a == b:
                    continue
                between = sentence[pos_a:pos_b]
                # The comparative must sit between the two mentions, and no third
                # model may intervene, or the direction is ambiguous.
                if any(p for p, _ in hits if pos_a < p < pos_b):
                    continue
                if win_re.search(between):
                    out.append((date, a, b, "win"))
                elif tie_re.search(between):
                    out.append((date, a, b, "tie"))
    return out


def fit(pairs: collections.Counter, items: list[str], prior: float = 1.0, iters: int = 500) -> dict[str, float]:
    """Hunter (2004) MM algorithm for Bradley-Terry strengths."""
    idx = {item: i for i, item in enumerate(items)}
    n = len(items)
    wins = np.zeros(n)
    games = np.zeros((n, n))
    for (a, b), c in pairs.items():
        if a not in idx or b not in idx:
            continue
        i, j = idx[a], idx[b]
        wins[i] += c
        games[i, j] += c
        games[j, i] += c

    p = np.ones(n)
    for _ in range(iters):
        prev = p.copy()
        for i in range(n):
            denom = 0.0
            for j in range(n):
                if games[i, j]:
                    denom += games[i, j] / (p[i] + p[j])
            # Bayesian smoothing: one virtual win and loss against the mean.
            denom += 2 * prior / (p[i] + p.mean())
            p[i] = (wins[i] + prior) / denom if denom > 0 else p[i]
        p /= p.mean()
        if np.abs(p - prev).max() < 1e-9:
            break
    return {item: float(p[idx[item]]) for item in items}


def largest_component(pairs: collections.Counter) -> set[str]:
    adj: dict[str, set[str]] = collections.defaultdict(set)
    for a, b in pairs:
        adj[a].add(b)
        adj[b].add(a)
    seen: set[str] = set()
    best: set[str] = set()
    for start in adj:
        if start in seen:
            continue
        stack, comp = [start], set()
        while stack:
            node = stack.pop()
            if node in comp:
                continue
            comp.add(node)
            stack.extend(adj[node] - comp)
        seen |= comp
        if len(comp) > len(best):
            best = comp
    return best


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--min-issues", type=int, default=3, help="model must be tagged this often to enter the lexicon")
    parser.add_argument(
        "--min-comparisons",
        type=int,
        default=20,
        help="minimum comparisons to be ranked; low values surface launch-announcement bias",
    )
    parser.add_argument("--by-period", action="store_true", help="also fit per half-year")
    args = parser.parse_args(argv)

    lex = lexicon(args.min_issues)
    print(f"lexicon: {len(lex)} surface forms → {len(set(lex.values()))} families", file=sys.stderr)
    triples = extract(lex)
    print(f"extracted {len(triples):,} comparative claims", file=sys.stderr)

    # Ties contribute half a win each way, the standard Bradley-Terry treatment.
    pairs: collections.Counter = collections.Counter()
    degree: collections.Counter = collections.Counter()
    for _, a, b, kind in triples:
        degree[a] += 1
        degree[b] += 1
        if kind == "win":
            pairs[(a, b)] += 1
        else:
            pairs[(a, b)] += 0.5
            pairs[(b, a)] += 0.5

    # Launch-asymmetry diagnostic, reported rather than silently corrected.
    wins_by: collections.Counter = collections.Counter()
    for _, a, b, kind in triples:
        if kind == "win":
            wins_by[a] += 1
    buckets = [(3, 7), (8, 15), (16, 40), (41, 10**6)]
    diag = []
    for lo, hi in buckets:
        sel = [m for m in degree if lo <= degree[m] <= hi]
        if sel:
            diag.append((lo, hi, len(sel), float(np.mean([wins_by[m] / degree[m] for m in sel]))))

    component = largest_component(pairs)
    items = sorted(i for i in component if degree[i] >= args.min_comparisons)
    strengths = fit(collections.Counter({k: v for k, v in pairs.items() if k[0] in items and k[1] in items}), items)
    ranked = sorted(strengths.items(), key=lambda kv: -kv[1])

    lines = [
        "# Capability ranking as the discourse asserted it",
        "",
        "Bradley-Terry strengths fitted by `analysis/methods/bradley_terry.py` to",
        f"**{len(triples):,} dated pairwise comparative claims** extracted from the issue",
        "bodies (\"X beats Y\", \"matches\", \"outperforms\", \"on par with\", \"Y-level\").",
        "",
        "This is *not* a benchmark. It measures what the field said about relative",
        "capability, which is exactly why it is worth comparing against what was",
        "actually true.",
        "",
        f"Scores are normalized to mean 1. Only the largest connected component of the",
        f"comparison graph is scored ({len(component)} families, {len(items)} with "
        f"{args.min_comparisons}+ comparisons) — strengths are unidentifiable across",
        "components, and fitting anyway would invent them.",
        "",
        "| Rank | Model family | BT strength | Comparisons |",
        "|---|---|---|---|",
    ]
    for rank, (model, strength) in enumerate(ranked, 1):
        lines.append(f"| {rank} | {model} | {strength:.2f} | {degree[model]} |")

    lines += [
        "",
        "## Launch-asymmetry diagnostic",
        "",
        "A model is the claimant when it launches and the incumbent only later, so",
        "rarely-compared models are near-undefeated by construction. Win rate should",
        "fall towards 0.5 as comparisons accumulate, and it does:",
        "",
        "| Comparisons | Models | Mean win rate |",
        "|---|---|---|",
    ]
    for lo, hi, count, rate in diag:
        label = f"{lo}-{hi}" if hi < 10**6 else f"{lo}+"
        lines.append(f"| {label} | {count} | {rate:.2f} |")
    lines += [
        "",
        "This is why the ranking below uses a high comparison threshold. Read the",
        "strengths as *what the field asserted about models it argued about repeatedly*,",
        "not as a benchmark.",
        "",
    ]

    if args.by_period:
        lines += ["", "## By period", "", "Strength within each half-year, refitted from that period's claims only.", ""]
        periods = sorted({corpus.half(d) for d, _, _, _ in triples})
        per: dict[str, dict[str, float]] = {}
        for period in periods:
            sub: collections.Counter = collections.Counter()
            deg: collections.Counter = collections.Counter()
            for date, a, b, kind in triples:
                if corpus.half(date) != period:
                    continue
                deg[a] += 1
                deg[b] += 1
                if kind == "win":
                    sub[(a, b)] += 1
                else:
                    sub[(a, b)] += 0.5
                    sub[(b, a)] += 0.5
            comp = largest_component(sub)
            keep = sorted(i for i in comp if deg[i] >= 3)
            if len(keep) >= 3:
                per[period] = fit(collections.Counter({k: v for k, v in sub.items() if k[0] in keep and k[1] in keep}), keep)
        tracked = [m for m, _ in ranked[:14]]
        lines += ["| Model | " + " | ".join(periods) + " |", "|---|" + "|".join(["---"] * len(periods)) + "|"]
        for model in tracked:
            row = [f"{per[p][model]:.2f}" if p in per and model in per[p] else "—" for p in periods]
            lines.append(f"| {model} | " + " | ".join(row) + " |")

    lines.append("")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    for rank, (model, strength) in enumerate(ranked[:18], 1):
        print(f"  {rank:>2}. {model:<20} {strength:6.2f}  ({degree[model]} comparisons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
