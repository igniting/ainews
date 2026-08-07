#!/usr/bin/env python3
"""Measure how densely the issue bodies discuss a thing, over time.

Three measures disagree, and the disagreements are informative:

- **Headline share** (`arcs.py`) — was it the day's story? Editorially loaded.
- **Binary presence** — was it mentioned at all? Saturates uselessly; a 24,000-word
  issue that says "agent" once scores the same as one about nothing else.
- **Density** (here) — mentions per 10,000 words. The one to trust for "how much
  did the archive actually talk about this".

Where headline share and density diverge, that gap is the finding: OpenAI's
headline share fell 18% → 4% while its density held flat, which means it stopped
being the headline without being covered any less.

Usage:
    python3 analysis/density.py                 # the default entity/topic set
    python3 analysis/density.py --monthly --since 2024-10 --until 2025-12 'Meta Llama'
"""

from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
ARTICLES = REPO / "articles"
FRONT = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)

# "llama" appears constantly as /r/LocalLlama, llama.cpp, ollama and llamaindex —
# none of which are Meta. Strip them before any matching.
NOISE = re.compile(
    r"localllama|local_llama|\bollama\b|llama[-_.]?cpp|llama[-_]?index|llamaparse|llamafile",
    re.I,
)

PATTERNS: dict[str, str] = {
    # Labs and model families
    "Meta Llama": r"\bllama[ -]?[234](?:\.\d)?\b|meta-llama",
    "Mistral": r"mistral|mixtral|devstral|magistral|voxtral",
    "DeepSeek": r"deepseek",
    "Qwen": r"\bqwen\b",
    "Kimi/Moonshot": r"kimi|moonshot",
    "GLM/z.ai": r"\bglm-|zai-org",
    "MiniMax": r"minimax",
    "Claude": r"\bclaude\b",
    "GPT/OpenAI": r"\bgpt-|openai",
    "Gemini": r"\bgemini\b",
    # Themes
    "reasoning": r"\breasoning\b|\bthinking mode|chain[- ]of[- ]thought|test[- ]time compute",
    "RAG/retrieval": r"\bRAG\b|retrieval[- ]augmented|vector (?:db|database|store)",
    "fine-tuning": r"fine[- ]?tun|\bLoRA\b|\bPEFT\b",
    "agentic": r"\bagentic\b|\bagents?\b",
    "MCP": r"\bMCP\b",
}

BLOCS = {
    "CHINA bloc": ["DeepSeek", "Qwen", "Kimi/Moonshot", "GLM/z.ai", "MiniMax"],
    "Meta+Mistral": ["Meta Llama", "Mistral"],
}


def period(date: str, monthly: bool) -> str:
    return date[:7] if monthly else f"{date[:4]}H{1 if int(date[5:7]) <= 6 else 2}"


def measure(names: list[str], monthly: bool, since: str, until: str) -> tuple[dict, collections.Counter]:
    counts: dict[str, collections.Counter] = {n: collections.Counter() for n in names}
    words: collections.Counter = collections.Counter()
    compiled = {n: re.compile(PATTERNS[n], re.I) for n in names}

    for path in sorted(ARTICLES.glob("*.md")):
        date = f"20{path.name[:8]}"
        if not (since <= date[: len(since)] or since <= date) or date[: len(until)] > until:
            continue
        key = period(date, monthly)
        body = NOISE.sub(" ", FRONT.sub("", path.read_text(encoding="utf-8", errors="replace")))
        words[key] += len(body.split())
        for name, pattern in compiled.items():
            counts[name][key] += len(pattern.findall(body))
    return counts, words


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("names", nargs="*", help="entities to measure (default: all)")
    parser.add_argument("--monthly", action="store_true", help="monthly instead of half-yearly")
    parser.add_argument("--since", default="2023", help="YYYY or YYYY-MM")
    parser.add_argument("--until", default="2099", help="YYYY or YYYY-MM")
    parser.add_argument("--list", action="store_true", help="list known names")
    args = parser.parse_args(argv)

    if args.list:
        print("\n".join(sorted(PATTERNS)))
        return 0

    names = args.names or list(PATTERNS)
    unknown = [n for n in names if n not in PATTERNS]
    if unknown:
        print(f"unknown: {', '.join(unknown)} (see --list)", file=sys.stderr)
        return 1

    counts, words = measure(names, args.monthly, args.since, args.until)
    periods = sorted(words)
    if not periods:
        print("no issues in range", file=sys.stderr)
        return 1

    print("mentions per 10,000 words of body text\n")
    print(f"{'':<15}" + "".join(f"{p:>10}" for p in periods))
    for name in names:
        print(f"{name:<15}" + "".join(f"{counts[name][p]/words[p]*10000:>10.1f}" for p in periods))

    if not args.names:
        print()
        for bloc, members in BLOCS.items():
            row = "".join(
                f"{sum(counts[m][p] for m in members)/words[p]*10000:>10.1f}" for p in periods
            )
            print(f"{bloc:<15}{row}")
    print(f"\n{'words':<15}" + "".join(f"{words[p]/1e6:>9.1f}M" for p in periods))
    return 0


if __name__ == "__main__":
    sys.exit(main())
