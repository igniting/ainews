#!/usr/bin/env python3
"""Entity co-occurrence networks with Louvain community detection.

Elsewhere in this repo I asserted there is a "China bloc" and grouped its members
myself. That is the same bias as the hand-written domains: the grouping is mine,
so of course the data fits it. This lets the communities fall out of the
co-occurrence structure instead, era by era, and then checks whether my bloc
survives.

Edges are weighted by **PPMI** rather than raw co-occurrence. Raw counts just
rediscover the most-mentioned entities — OpenAI co-occurs with everything because
OpenAI is in most issues. Pointwise mutual information asks whether two entities
appear together *more than their individual rates predict*, which is what
"associated" should mean.

Betweenness centrality on the same graph identifies brokers: entities that sit on
paths between communities. In this corpus those turn out to be the interop layers.

Usage:
    python3 analysis/methods/network.py
    python3 analysis/methods/network.py --min-issues 15
"""

from __future__ import annotations

import argparse
import collections
import itertools
import json
import math
import pathlib
import sys

import networkx as nx
from networkx.algorithms.community import louvain_communities

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
INDEX = REPO / "analysis" / "index.json"
OUT = REPO / "analysis" / "network.md"

ALIASES = {
    "huggingface": "hugging-face",
    "deepseek-ai": "deepseek",
    "deepseek_ai": "deepseek",
    "langchainai": "langchain",
    "langchain-ai": "langchain",
    "meta": "meta-ai-fair",
    "meta-ai": "meta-ai-fair",
    "deepmind": "google-deepmind",
    "qwen": "alibaba",
    "mistral": "mistral-ai",
    "xai": "x-ai",
}


def half(date: str) -> str:
    return f"{date[:4]}H{1 if int(date[5:7]) <= 6 else 2}"


def entities(record: dict) -> set[str]:
    out = set()
    for tag in record.get("companies", []):
        tag = tag.strip().lower()
        if tag:
            out.add(ALIASES.get(tag, tag))
    return out


def build(records: list[dict], min_issues: int) -> nx.Graph:
    counts: collections.Counter = collections.Counter()
    pairs: collections.Counter = collections.Counter()
    for record in records:
        ents = entities(record)
        counts.update(ents)
        for a, b in itertools.combinations(sorted(ents), 2):
            pairs[(a, b)] += 1

    keep = {e for e, c in counts.items() if c >= min_issues}
    n = len(records)
    graph = nx.Graph()
    for entity in keep:
        graph.add_node(entity, issues=counts[entity])
    for (a, b), c in pairs.items():
        if a not in keep or b not in keep or c < 3:
            continue
        # PPMI: log( P(a,b) / (P(a)P(b)) ), clipped at zero.
        pmi = math.log((c / n) / ((counts[a] / n) * (counts[b] / n)))
        if pmi > 0:
            graph.add_edge(a, b, weight=pmi, count=c)
    return graph


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--min-issues", type=int, default=10)
    parser.add_argument("--resolution", type=float, default=1.0)
    args = parser.parse_args(argv)

    records = json.loads(INDEX.read_text(encoding="utf-8"))
    periods = sorted({half(r["date"]) for r in records})

    lines = [
        "# Entity co-occurrence networks",
        "",
        "Built by `analysis/methods/network.py`. Edges are **PPMI**, not raw",
        "co-occurrence: raw counts merely rediscover the most-mentioned entities, since",
        "OpenAI co-occurs with everything. Communities are Louvain, so the groupings are",
        "the data's rather than mine.",
        "",
    ]

    for period in periods:
        subset = [r for r in records if half(r["date"]) == period]
        if len(subset) < 25:
            continue
        graph = build(subset, max(args.min_issues // 2, 4))
        if graph.number_of_edges() < 5:
            continue
        communities = louvain_communities(graph, weight="weight", seed=0, resolution=args.resolution)
        communities = sorted(communities, key=len, reverse=True)
        lines += [f"## {period}", "", f"{graph.number_of_nodes()} entities, {graph.number_of_edges()} edges", ""]
        for i, community in enumerate(communities[:5], 1):
            members = sorted(community, key=lambda e: -graph.nodes[e]["issues"])
            lines.append(f"{i}. {', '.join(members[:12])}")
        lines.append("")

    # Brokers over the whole corpus.
    whole = build(records, args.min_issues)
    between = nx.betweenness_centrality(whole, weight=None)
    top = sorted(between.items(), key=lambda kv: -kv[1])[:15]
    lines += [
        "## Brokers (betweenness centrality, whole corpus)",
        "",
        "Entities sitting on the most shortest paths between others — the connective",
        "tissue of the ecosystem rather than its biggest names.",
        "",
        "| Entity | Betweenness | Issues |",
        "|---|---|---|",
    ]
    for entity, score in top:
        lines.append(f"| {entity} | {score:.3f} | {whole.nodes[entity]['issues']} |")
    lines.append("")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    print("top brokers:", ", ".join(e for e, _ in top[:8]))

    last = periods[-2] if len(periods) > 1 else periods[-1]
    subset = [r for r in records if half(r["date"]) == last]
    graph = build(subset, 4)
    if graph.number_of_edges() >= 5:
        print(f"\n{last} communities:")
        for community in sorted(louvain_communities(graph, weight="weight", seed=0), key=len, reverse=True)[:5]:
            members = sorted(community, key=lambda e: -graph.nodes[e]["issues"])
            print(f"  {', '.join(members[:10])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
