#!/usr/bin/env python3
"""Diachronic word embeddings with Procrustes alignment (Hamilton et al. 2016).

Everything else in this repo counts *whether* a word appeared. This asks what it
**meant**, and how that changed.

The method: train a separate word2vec model on each era, then align the vector
spaces. Embedding spaces from independent runs are only defined up to rotation,
so raw vectors are not comparable across eras; orthogonal Procrustes finds the
rotation that best superimposes the shared vocabulary, after which a word's
displacement between eras is meaningful. Large displacement with stable frequency
is the signature of genuine semantic change.

The corpus is trained on itself. That is a feature, not a limitation: 15.3M words
of domain-specific text produces far better vectors *for this vocabulary* than a
general pretrained model would, and needs no downloads.

Two outputs per word:
- **Drift** — cosine distance between its aligned vectors in two eras.
- **Neighbours** — the words nearest it in each era, which is what actually
  shows the meaning change rather than merely scoring it.

Usage:
    python3 analysis/methods/semantic_drift.py
    python3 analysis/methods/semantic_drift.py --words agent reasoning context
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import numpy as np
from gensim.models import Word2Vec

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import corpus  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = REPO / "analysis" / "semantic-drift.md"

# Half-years give ~1.6-3.6M words each, comfortably enough to train on.
ERAS = ["2024H1", "2024H2", "2025H1", "2025H2", "2026H1"]

WATCH = [
    "agent", "agents", "agentic", "reasoning", "context", "memory", "harness",
    "skills", "tools", "scaling", "open", "cheap", "fast", "benchmark",
    "distillation", "alignment", "safety", "inference", "training", "prompt",
]


def sentences(era: str, drop_discord: bool = False) -> list[list[str]]:
    """Sentences for one era.

    `drop_discord` is the genre control. The corpus goes from 96% Discord text in
    2024H1 to 0% in 2026H1, so a model trained on whole issues learns partly the
    difference between chat transcripts and news prose. Excluding Discord holds
    the genre roughly fixed at the cost of much less text early on.
    """
    out = []
    for date, _, body in corpus.load(drop_discord=drop_discord):
        if corpus.half(date) != era:
            continue
        for line in body.split("\n"):
            toks = corpus.tokens(line, drop_stop=False)
            if len(toks) >= 5:
                out.append(toks)
    return out


def train(era: str, dim: int, min_count: int, seed: int = 0, drop_discord: bool = False) -> Word2Vec:
    sents = sentences(era, drop_discord)
    print(f"  {era}: {len(sents):,} sentences", file=sys.stderr)
    return Word2Vec(
        sents, vector_size=dim, window=5, min_count=min_count, workers=4, epochs=5, seed=seed, sg=1
    )


def procrustes(base: Word2Vec, other: Word2Vec) -> tuple[np.ndarray, list[str]]:
    """Rotate `other` into `base`'s space over their shared vocabulary."""
    shared = sorted(set(base.wv.key_to_index) & set(other.wv.key_to_index))
    A = np.asarray([other.wv[w] for w in shared])
    B = np.asarray([base.wv[w] for w in shared])
    # Orthogonal Procrustes: R = argmin ||A R - B||_F  =>  R = U V^T from SVD(A^T B)
    U, _, Vt = np.linalg.svd(A.T @ B)
    R = U @ Vt
    return R, shared


def cosine(u: np.ndarray, v: np.ndarray) -> float:
    denom = np.linalg.norm(u) * np.linalg.norm(v)
    return float(u @ v / denom) if denom else 0.0


def neighbours(model: Word2Vec, word: str, k: int = 8) -> list[str]:
    if word not in model.wv:
        return []
    return [w for w, _ in model.wv.most_similar(word, topn=k)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--words", nargs="*", default=WATCH)
    parser.add_argument("--dim", type=int, default=150)
    parser.add_argument("--min-count", type=int, default=40)
    parser.add_argument("--top-drift", type=int, default=25)
    parser.add_argument(
        "--exclude-discord",
        action="store_true",
        help="genre control: train on lede+Twitter+Reddit only",
    )
    args = parser.parse_args(argv)

    print("training one word2vec per era…", file=sys.stderr)
    models = {era: train(era, args.dim, args.min_count, drop_discord=args.exclude_discord) for era in ERAS}

    first, last = ERAS[0], ERAS[-1]
    R, shared = procrustes(models[first], models[last])
    print(f"shared vocabulary: {len(shared):,} words", file=sys.stderr)

    # Drift for every shared word, so the watch-list can be put in context.
    drift = {}
    for word in shared:
        a = models[first].wv[word]
        b = models[last].wv[word] @ R
        drift[word] = 1 - cosine(a, b)

    ranked = sorted(drift.items(), key=lambda kv: -kv[1])
    median = float(np.median(list(drift.values())))

    lines = [
        "# Semantic drift",
        "",
        "Diachronic word embeddings with orthogonal Procrustes alignment",
        "(Hamilton, Leskovec & Jurafsky 2016), via `analysis/methods/semantic_drift.py`.",
        "",
        "One word2vec model per half-year, trained on this corpus rather than downloaded —",
        "15.3M words of domain text gives better vectors for this vocabulary than a general",
        "pretrained model would. Independent embedding spaces are only defined up to",
        "rotation, so they are aligned before comparison.",
        "",
        f"**Drift** is cosine distance between a word's {first} and {last} vectors.",
        f"Median drift across {len(shared):,} shared words is **{median:.3f}** — use that as",
        "the baseline for 'this word did not really move'.",
        "",
        "The neighbour lists are the actual finding; the drift score only ranks them.",
        "",
        f"## Watch list: {first} → {last}",
        "",
        "| Word | Drift | Nearest in " + first + " | Nearest in " + last + " |",
        "|---|---|---|---|",
    ]
    for word in args.words:
        if word not in drift:
            continue
        na = ", ".join(neighbours(models[first], word, 6))
        nb = ", ".join(neighbours(models[last], word, 6))
        flag = "**" if drift[word] > median else ""
        lines.append(f"| `{word}` | {flag}{drift[word]:.3f}{flag} | {na} | {nb} |")

    lines += [
        "",
        f"## Largest drift overall ({first} → {last})",
        "",
        "Ranked over all shared vocabulary. Words that changed company, not just frequency.",
        "",
        "| Word | Drift | Nearest in " + first + " | Nearest in " + last + " |",
        "|---|---|---|---|",
    ]
    for word, d in ranked[: args.top_drift]:
        na = ", ".join(neighbours(models[first], word, 5))
        nb = ", ".join(neighbours(models[last], word, 5))
        lines.append(f"| `{word}` | {d:.3f} | {na} | {nb} |")

    lines += [
        "",
        "## Trajectory of key terms across all eras",
        "",
        "Nearest neighbours era by era — the clearest way to watch a concept move.",
        "",
    ]
    for word in args.words[:8]:
        if word not in drift:
            continue
        lines += [f"**`{word}`**", ""]
        for era in ERAS:
            ns = neighbours(models[era], word, 7)
            if ns:
                lines.append(f"- {era}: {', '.join(ns)}")
        lines.append("")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    print(f"\nmedian drift {median:.3f}; watch-list movers:")
    for word in args.words:
        if word in drift and drift[word] > median:
            print(f"  {drift[word]:.3f}  {word}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
