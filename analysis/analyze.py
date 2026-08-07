#!/usr/bin/env python3
"""Summarize the AI News archive from analysis/index.json into a markdown report.

Every issue is tagged with the companies, models, topics and people it covered,
so counting how those tags move over time gives a reasonable proxy for what the
newsletter's attention was on in any given stretch.
"""

from __future__ import annotations

import collections
import datetime as dt
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
INDEX = REPO / "analysis" / "index.json"
OUT = REPO / "analysis" / "report.md"

# The archive spells a handful of tags two ways; fold them together so the
# counts don't split across spellings.
ALIASES = {
    "huggingface": "hugging-face",
    "hugging-face-inc": "hugging-face",
    "openai-inc": "openai",
    "meta": "meta-ai-fair",
    "meta-ai": "meta-ai-fair",
    "google-brain": "google-deepmind",
    "deepmind": "google-deepmind",
    "xai": "x-ai",
    "mistral": "mistral-ai",
    "alibaba-cloud": "alibaba",
    "qwen": "alibaba",
    "deepseek-ai": "deepseek",
    "deepseek_ai": "deepseek",
    "langchainai": "langchain",
    "langchain-ai": "langchain",
    "perplexity": "perplexity-ai",
    "cursor_ai": "cursor",
    "moonshot": "moonshot-ai",
    "sakana-ai-labs": "sakana-ai",
    "vllm_project": "vllm",
    "vllm-project": "vllm",
    "minimax-ai": "minimax",
    "lm-studio": "lmstudio",
    "uc-berkeley": "berkeley",
}

TAG_FIELDS = ("companies", "models", "topics", "people")
SINGULAR = {"companies": "Company", "models": "Model", "topics": "Topic", "people": "Person"}


def normalize(tag: str, field: str) -> str:
    tag = tag.strip().lower()
    if field == "people":
        # Handles are tagged with and without their leading underscore.
        tag = tag.lstrip("_")
        return tag
    return ALIASES.get(tag, tag)


def tags(record: dict, field: str) -> set[str]:
    return {normalize(t, field) for t in record.get(field, []) if t.strip()}


def half(date: str) -> str:
    year, month = date[:4], int(date[5:7])
    return f"{year}H{1 if month <= 6 else 2}"


def counts(records: list[dict], field: str) -> collections.Counter:
    counter: collections.Counter = collections.Counter()
    for record in records:
        counter.update(tags(record, field))
    return counter


def table(rows: list[tuple], headers: tuple) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    lines += ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
    return lines + [""]


# --------------------------------------------------------------------------- #
# Sections
# --------------------------------------------------------------------------- #


def section_coverage(records: list[dict]) -> list[str]:
    dates = [dt.date.fromisoformat(r["date"]) for r in records]
    first, last = min(dates), max(dates)
    span_days = (last - first).days + 1
    by_year = collections.Counter(r["date"][:4] for r in records)
    words = sum(r["body_words"] for r in records)

    seen = set(dates)
    gaps = []
    run_start = None
    day = first
    while day <= last:
        if day not in seen:
            run_start = run_start or day
        elif run_start:
            gaps.append((run_start, day - dt.timedelta(days=1)))
            run_start = None
        day += dt.timedelta(days=1)
    if run_start:
        gaps.append((run_start, last))
    long_gaps = sorted((g for g in gaps if (g[1] - g[0]).days + 1 >= 5), key=lambda g: g[0])

    lines = [
        "## Corpus",
        "",
        f"- **{len(records)} issues**, {first} to {last} ({span_days} days, {len(seen)} distinct dates)",
        f"- **{words/1e6:.1f}M words** of body text, median {sorted(r['body_words'] for r in records)[len(records)//2]:,} words per issue",
        f"- Publishing cadence: {len(records)/span_days*7:.1f} issues per week on average",
        "",
        "Issues per year:",
        "",
    ]
    rows = []
    for year, count in sorted(by_year.items()):
        # 2023 and 2026 are partial, so measure against the days actually in range.
        start = max(first, dt.date(int(year), 1, 1))
        end = min(last, dt.date(int(year), 12, 31))
        in_range = (end - start).days + 1
        rows.append((year, count, in_range, f"{count/in_range*100:.0f}%"))
    lines += table(rows, ("Year", "Issues", "Days in range", "Days with an issue"))
    if long_gaps:
        lines += ["Gaps of 5+ days with no issue:", ""]
        lines += table(
            [(str(a), str(b), (b - a).days + 1) for a, b in long_gaps[:15]],
            ("From", "To", "Days"),
        )
    return lines


def section_leaderboard(records: list[dict], field: str, title: str, top: int) -> list[str]:
    counter = counts(records, field)
    total = len(records)
    lines = [f"## {title}", "", f"{len(counter):,} distinct tags across {total} issues.", ""]
    lines += table(
        [(rank, tag, count, f"{count/total*100:.1f}%") for rank, (tag, count) in enumerate(counter.most_common(top), 1)],
        ("#", SINGULAR[field], "Issues", "Share"),
    )
    return lines


def section_trend(records: list[dict], field: str, title: str, top: int) -> list[str]:
    """Share of issues mentioning each tag, per half-year."""
    periods = sorted({half(r["date"]) for r in records})
    per_period = {p: [r for r in records if half(r["date"]) == p] for p in periods}
    leaders = [tag for tag, _ in counts(records, field).most_common(top)]

    rows = [tuple(["*(issues in period)*"] + [f"*{len(per_period[p])}*" for p in periods])]
    for tag in leaders:
        row = [tag]
        for period in periods:
            bucket = per_period[period]
            hits = sum(1 for r in bucket if tag in tags(r, field))
            row.append(f"{hits/len(bucket)*100:.0f}%" if bucket else "-")
        rows.append(tuple(row))
    return [f"## {title}", "", "Share of that period's issues mentioning the tag.", ""] + table(
        rows, tuple([SINGULAR[field]] + periods)
    )


def section_movers(records: list[dict], field: str, title: str) -> list[str]:
    """Biggest swings in share between the first and last full year of coverage."""
    early = [r for r in records if r["date"][:4] == "2024"]
    late = [r for r in records if r["date"][:4] in ("2025", "2026") and r["date"] >= "2025-08-01"]
    early_counts, late_counts = counts(early, field), counts(late, field)

    deltas = []
    for tag in set(early_counts) | set(late_counts):
        a = early_counts.get(tag, 0) / len(early) * 100
        b = late_counts.get(tag, 0) / len(late) * 100
        if max(early_counts.get(tag, 0), late_counts.get(tag, 0)) >= 8:
            deltas.append((b - a, tag, a, b))
    deltas.sort(reverse=True)

    lines = [f"## {title}", "", "Share of issues in 2024 vs. the last 12 months (Aug 2025 onward).", ""]
    lines += ["**Rising**", ""]
    lines += table(
        [(tag, f"{a:.0f}%", f"{b:.0f}%", f"+{d:.0f}pp") for d, tag, a, b in deltas[:12]],
        (SINGULAR[field], "2024", "Last 12mo", "Change"),
    )
    lines += ["**Fading**", ""]
    lines += table(
        [(tag, f"{a:.0f}%", f"{b:.0f}%", f"{d:.0f}pp") for d, tag, a, b in deltas[-12:][::-1]],
        (SINGULAR[field], "2024", "Last 12mo", "Change"),
    )
    return lines


def section_slow_days(records: list[dict]) -> list[str]:
    """The newsletter titles quiet days "not much happened"; count them per half."""
    periods = sorted({half(r["date"]) for r in records})
    rows = []
    for period in periods:
        bucket = [r for r in records if half(r["date"]) == period]
        quiet = [r for r in bucket if "not much" in r["title"].lower() or "not much" in r["file"].lower()]
        avg_words = sum(r["body_words"] for r in bucket) / len(bucket)
        rows.append((period, len(bucket), len(quiet), f"{len(quiet)/len(bucket)*100:.0f}%", f"{avg_words:,.0f}"))
    return ['## "Not much happened today"', "", "The newsletter's own label for a slow news day.", ""] + table(
        rows, ("Period", "Issues", "Quiet days", "Share", "Avg words")
    )


def main() -> int:
    if not INDEX.exists():
        print(f"missing {INDEX}; run analysis/build_index.py first", file=sys.stderr)
        return 1
    records = json.loads(INDEX.read_text(encoding="utf-8"))

    lines = [
        "# AI News archive analysis",
        "",
        "Generated by `analysis/analyze.py` from `analysis/index.json`.",
        "Counts are *issues mentioning a tag*, not raw mentions, so an issue that",
        "names OpenAI six times still counts once.",
        "",
    ]
    lines += section_coverage(records)
    lines += section_leaderboard(records, "companies", "Most-covered companies", 25)
    lines += section_trend(records, "companies", "Company coverage over time", 12)
    lines += section_movers(records, "companies", "Companies: rising and fading")
    lines += section_leaderboard(records, "models", "Most-covered models", 25)
    lines += section_trend(records, "models", "Model coverage over time", 12)
    lines += section_leaderboard(records, "topics", "Most-covered topics", 25)
    lines += section_movers(records, "topics", "Topics: rising and fading")
    lines += section_leaderboard(records, "people", "Most-mentioned people", 25)
    lines += section_slow_days(records)

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)} ({len(lines)} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
