#!/usr/bin/env python3
"""Trace one company's arc through the archive.

Two different signals, deliberately kept apart:

- **Headline days** — the company is named in the issue title. The title is the
  editor's verdict on what mattered that day, so these are the company's moments.

  **The title field went generic over time** — "not much happened today" is 0% of
  2023 titles, 18% of 2024, 42% of 2025 and 68% of 2026 — and it is boilerplate,
  not a verdict: the Claude Opus 5, GPT-5.6, Kimi K3 and Thinking Machines
  Inkling launches all carry it. No company can be named in a generic title, so
  raw headline share falls mechanically as the template spreads. Use
  `--descriptive-only` to condition on issues whose title actually says something;
  without it, any cross-year comparison measures the template, not the coverage.
- **Presence** — the company is tagged in the front matter but not in the title.
  Background coverage: it came up, it wasn't the story.

A company can be constantly present and rarely a headline (infrastructure), or
spike into headlines and vanish (a single release). The ratio is informative.

Usage:
    python3 analysis/arcs.py openai anthropic deepseek
    python3 analysis/arcs.py --list
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
INDEX = REPO / "analysis" / "index.json"

# Title text rarely matches the tag slug, so each company needs its own surface
# forms. Word-boundary anchored to keep "meta" out of "metadata".
SURFACE: dict[str, str] = {
    "openai": r"openai|gpt-?[45]|\bo[134]\b|chatgpt|sora|codex|dall-?e|sam altman",
    "anthropic": r"anthropic|claude",
    "google": r"google|gemini|deepmind|gdm\b|gemma|notebooklm|\btpu\b",
    "meta": r"\bmeta\b|llama|\bfair\b|muse spark|muse code",
    "deepseek": r"deepseek",
    "alibaba": r"alibaba|qwen",
    "mistral": r"mistral|mixtral|codestral",
    "nvidia": r"nvidia|cuda|blackwell|\bh100\b|\bh800\b|gb200",
    "xai": r"\bx\.?ai\b|grok",
    "microsoft": r"microsoft|copilot|\bphi-?\d",
    "hugging-face": r"hugging ?face|\bhf\b",
    "cursor": r"cursor",
    "moonshot": r"moonshot|kimi",
    "apple": r"apple|\bmlx\b",
    "perplexity": r"perplexity",
    "cohere": r"cohere|command-?r",
    "stability": r"stability|stable diffusion|\bsdxl\b",
}


def half(date: str) -> str:
    return f"{date[:4]}H{1 if int(date[5:7]) <= 6 else 2}"


def load() -> list[dict]:
    return json.loads(INDEX.read_text(encoding="utf-8"))


GENERIC = ("not much", "a quiet day", "a quiet weekend", "nothing much")


def is_generic(title: str) -> bool:
    """True if the title is the newsletter's placeholder rather than a verdict."""
    t = title.strip().lower()
    return any(t.startswith(g) or t == g for g in GENERIC)


def tagged(record: dict, company: str) -> bool:
    """Front-matter tag match, tolerating the archive's spelling variants."""
    stem = company.split("-")[0]
    return any(stem in t.lower() for t in record.get("companies", []))


def arc(records: list[dict], company: str, descriptive_only: bool = False) -> dict:
    pattern = re.compile(SURFACE[company], re.I)
    if descriptive_only:
        records = [r for r in records if not is_generic(r["title"])]
    headlines, presence = [], []
    for record in records:
        title = record["title"]
        if pattern.search(title):
            headlines.append(record)
        elif tagged(record, company) or pattern.search(record.get("description", "")):
            presence.append(record)
    return {"headlines": headlines, "presence": presence}


def render(records: list[dict], company: str, descriptive_only: bool = False) -> list[str]:
    if descriptive_only:
        records = [r for r in records if not is_generic(r["title"])]
    data = arc(records, company)
    heads, pres = data["headlines"], data["presence"]
    periods = sorted({half(r["date"]) for r in records})
    buckets = {p: sum(1 for r in records if half(r["date"]) == p) for p in periods}

    lines = [f"## {company}", ""]
    lines += [
        f"**{len(heads)} headline days**, {len(pres)} further days present but not the story "
        f"({(len(heads) + len(pres)) / len(records) * 100:.0f}% of all issues).",
        "",
    ]

    head_by = collections.Counter(half(r["date"]) for r in heads)
    pres_by = collections.Counter(half(r["date"]) for r in pres)
    lines += ["| Period | " + " | ".join(periods) + " |", "|" + "|".join(["---"] * (len(periods) + 1)) + "|"]
    lines += ["| Headline days | " + " | ".join(str(head_by.get(p, 0)) for p in periods) + " |"]
    lines += [
        "| Headline share | "
        + " | ".join(f"{head_by.get(p, 0)/buckets[p]*100:.0f}%" for p in periods)
        + " |"
    ]
    lines += ["| Also present | " + " | ".join(str(pres_by.get(p, 0)) for p in periods) + " |", ""]

    lines += ["<details><summary>Headline days</summary>", ""]
    for record in heads:
        lines.append(f"- `{record['date']}` {record['title']}")
    lines += ["", "</details>", ""]
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("companies", nargs="*", help="companies to trace")
    parser.add_argument("--list", action="store_true", help="list known companies")
    parser.add_argument("--out", type=pathlib.Path, help="write markdown here instead of stdout")
    parser.add_argument(
        "--descriptive-only",
        action="store_true",
        help="drop issues with placeholder titles; required for any cross-year comparison",
    )
    args = parser.parse_args(argv)

    if args.list or not args.companies:
        print("known companies:", ", ".join(sorted(SURFACE)))
        return 0

    records = load()
    unknown = [c for c in args.companies if c not in SURFACE]
    if unknown:
        print(f"unknown: {', '.join(unknown)} (see --list)", file=sys.stderr)
        return 1

    lines = ["# Company arcs", "", "Generated by `analysis/arcs.py`.", ""]
    if args.descriptive_only:
        kept = sum(1 for r in records if not is_generic(r["title"]))
        lines += [
            f"Conditioned on descriptive titles: {kept} of {len(records)} issues. "
            "Placeholder titles carry no company name, so raw shares fall as the template spreads.",
            "",
        ]
    for company in args.companies:
        lines += render(records, company, args.descriptive_only)

    text = "\n".join(lines) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
