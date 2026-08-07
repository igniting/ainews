#!/usr/bin/env python3
"""Project entities onto interpretable semantic axes, per era.

`semantic_drift.py` trains one word2vec per half-year and reduces each word to a
single drift number. That throws away the geometry. This keeps it: define an axis
as the difference between two pole-word centroids (cheap ↔ expensive, open ↔
closed, research ↔ product), then project every entity onto it.

The output is a coordinate rather than a distance — "Qwen sat at the cheap end in
2025H1 and moved toward the frontier end by 2026H1" instead of "qwen moved 0.4".

Method notes:

- Poles are **centroids of several words**, not single words, so the axis does
  not hinge on one idiosyncratic vector.
- Projections are z-scored **within each era** against all vocabulary. Raw cosine
  values are not comparable between independently trained models, and the eras
  differ in size by 2x. A z-score answers "where does this entity sit relative to
  the rest of this era's vocabulary", which is the comparable question.
- No Procrustes alignment is needed: each projection is computed inside its own
  era's space, and only the standardized scores are compared across eras.

Usage:
    python3 analysis/methods/axes.py
    python3 analysis/methods/axes.py --axis cost --entities qwen claude
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import numpy as np
from gensim.models import Word2Vec

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import corpus  # noqa: E402
from semantic_drift import ERAS, sentences  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = REPO / "analysis" / "axes.md"

AXES: dict[str, tuple[list[str], list[str]]] = {
    "cost": (
        ["cheap", "cheaper", "affordable", "low-cost", "inexpensive", "budget", "free"],
        ["expensive", "costly", "pricey", "premium", "priciest"],
    ),
    "openness": (
        ["open-source", "open-weights", "open-weight", "oss", "permissive", "downloadable"],
        ["proprietary", "closed", "closed-source", "api-only", "gated"],
    ),
    "maturity": (
        ["production", "production-ready", "enterprise", "stable", "reliable", "ga"],
        ["experimental", "research", "preview", "prototype", "alpha", "beta"],
    ),
    "capability": (
        ["sota", "frontier", "state-of-the-art", "best-in-class", "flagship", "leading"],
        ["weak", "underwhelming", "disappointing", "mediocre", "lagging", "outdated"],
    ),
    "speed": (
        ["fast", "faster", "fastest", "quick", "low-latency", "realtime"],
        ["slow", "slower", "sluggish", "latency", "bottleneck"],
    ),
}

ENTITIES = [
    "qwen", "deepseek", "kimi", "glm", "minimax",
    "llama", "mistral", "gemma",
    "claude", "gpt-4o", "gemini", "grok", "codex",
]


def axis_vector(model: Word2Vec, positive: list[str], negative: list[str]) -> np.ndarray | None:
    pos = [model.wv[w] for w in positive if w in model.wv]
    neg = [model.wv[w] for w in negative if w in model.wv]
    if len(pos) < 2 or len(neg) < 2:
        return None
    return np.mean(pos, axis=0) - np.mean(neg, axis=0)


def project(model: Word2Vec, vector: np.ndarray, word: str) -> float | None:
    if word not in model.wv:
        return None
    v = model.wv[word]
    denom = np.linalg.norm(v) * np.linalg.norm(vector)
    return float(v @ vector / denom) if denom else None


def standardized(model: Word2Vec, vector: np.ndarray, words: list[str], sample: int = 3000):
    """z-score entity projections against the era's own vocabulary."""
    vocab = list(model.wv.key_to_index)[:sample]
    base = np.asarray([p for p in (project(model, vector, w) for w in vocab) if p is not None])
    mu, sd = base.mean(), base.std() or 1.0
    return {w: (project(model, vector, w) - mu) / sd for w in words if w in model.wv}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--axis", nargs="*", default=list(AXES))
    parser.add_argument("--entities", nargs="*", default=ENTITIES)
    parser.add_argument("--dim", type=int, default=150)
    parser.add_argument("--min-count", type=int, default=40)
    args = parser.parse_args(argv)

    print("training one word2vec per era…", file=sys.stderr)
    models = {}
    for era in ERAS:
        sents = sentences(era)
        print(f"  {era}: {len(sents):,} sentences", file=sys.stderr)
        models[era] = Word2Vec(
            sents, vector_size=args.dim, window=5, min_count=args.min_count, workers=4, epochs=5, seed=0, sg=1
        )

    lines = [
        "# Entities on interpretable semantic axes",
        "",
        "Computed by `analysis/methods/axes.py`. Each axis is the difference between two",
        "pole-word centroids; entities are projected onto it and **z-scored against that",
        "era's own vocabulary**, since raw cosines are not comparable between",
        "independently trained models.",
        "",
        "Positive = toward the first pole. Values are standard deviations, so ±1 is a",
        "meaningful displacement and ±0.2 is noise.",
        "",
    ]

    for axis in args.axis:
        if axis not in AXES:
            continue
        pos, neg = AXES[axis]
        lines += [
            f"## {axis}: {pos[0]} (+) ↔ {neg[0]} (−)",
            "",
            "| Entity | " + " | ".join(ERAS) + " |",
            "|---|" + "|".join(["---"] * len(ERAS)) + "|",
        ]
        scores: dict[str, dict[str, float]] = {}
        for era in ERAS:
            vector = axis_vector(models[era], pos, neg)
            scores[era] = standardized(models[era], vector, args.entities) if vector is not None else {}
        for entity in args.entities:
            row = [f"{scores[e][entity]:+.2f}" if entity in scores.get(e, {}) else "—" for e in ERAS]
            if all(cell == "—" for cell in row):
                continue
            lines.append(f"| `{entity}` | " + " | ".join(row) + " |")
        lines.append("")

        first = next((e for e in ERAS if scores.get(e)), None)
        last = next((e for e in reversed(ERAS) if scores.get(e)), None)
        if first and last:
            moves = [
                (scores[last][x] - scores[first][x], x)
                for x in args.entities
                if x in scores[first] and x in scores[last]
            ]
            moves.sort(reverse=True)
            if moves:
                up = ", ".join(f"`{m}` ({d:+.2f})" for d, m in moves[:3])
                down = ", ".join(f"`{m}` ({d:+.2f})" for d, m in moves[-3:])
                lines += [f"Largest moves toward **{pos[0]}**: {up}.", "", f"Toward **{neg[0]}**: {down}.", ""]

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    for axis in args.axis:
        if axis not in AXES:
            continue
        pos, neg = AXES[axis]
        vector = axis_vector(models[ERAS[-1]], pos, neg)
        if vector is None:
            continue
        sc = standardized(models[ERAS[-1]], vector, args.entities)
        top = sorted(sc.items(), key=lambda kv: -kv[1])[:4]
        print(f"  {axis:<11} {ERAS[-1]} most {pos[0]}: " + ", ".join(f"{k} {v:+.2f}" for k, v in top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
