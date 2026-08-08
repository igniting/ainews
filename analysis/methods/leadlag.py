#!/usr/bin/env python3
"""Which surface breaks a story first: Twitter, Reddit or Discord?

Each issue covers one day and carries a separate recap for each of the three
sources, so the corpus contains three parallel observations of the same events —
an unusually clean setup for lead-lag analysis.

Two tests, because they answer slightly different questions:

- **Cross-correlation at lag** — at what offset *k* is source A's series most
  correlated with source B's? A positive peak means A leads.
- **Granger causality** — does adding A's past values to an autoregression of B
  significantly reduce residual error? Stricter, since it conditions on B's own
  history, so it does not credit A for a trend B was already on.

Restricted by default to the 2024-05-20 → 2026-03-10 format regime (from
`changepoints.py`), the only stretch where all three sections are reliably
present. Outside it the Discord recap is missing entirely and any lag is an
artifact of the format.

Usage:
    python3 analysis/methods/leadlag.py
    python3 analysis/methods/leadlag.py --entities Qwen MCP --max-lag 8
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import corpus  # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from density import NOISE, PATTERNS  # noqa: E402

from recaps import sections_of  # one shared, tested recap splitter

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = REPO / "analysis" / "leadlag.md"

HEAD = re.compile(r"^#\s+AI (Twitter|Reddit|Discord) Recap.*$", re.M | re.I)
SOURCES = ["twitter", "reddit", "discord"]


def split_sections(body: str) -> dict[str, str]:
    """Body → {source: text}. Discord includes its PART 1/2 tail."""
    return sections_of(body)


def raw_bodies() -> list[tuple[str, str]]:
    """(date, body) with only front matter removed.

    `corpus.clean()` strips the recap headings as boilerplate, which is right for
    the frequency methods and fatal here — those headings *are* the section
    boundaries. So this reads the files directly.
    """
    out = []
    for path in sorted(corpus.ARTICLES.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        out.append((f"20{path.name[:8]}", corpus.FRONT.sub("", text)))
    return out


def series(pattern: re.Pattern, since: str, until: str) -> tuple[list[str], dict[str, np.ndarray]]:
    """Per-issue mention density (per 10k words) for each source section."""
    dates: list[str] = []
    rows: dict[str, list[float]] = {s: [] for s in SOURCES}
    for date, body in raw_bodies():
        if not (since <= date <= until):
            continue
        sections = split_sections(body)
        if not all(s in sections for s in SOURCES):
            continue
        dates.append(date)
        for source in SOURCES:
            text = NOISE.sub(" ", sections[source])
            words = max(len(text.split()), 1)
            rows[source].append(len(pattern.findall(text)) / words * 10000)
    return dates, {s: np.asarray(v) for s, v in rows.items()}


def zscore(x: np.ndarray) -> np.ndarray:
    sd = x.std()
    return (x - x.mean()) / sd if sd > 0 else x * 0.0


def xcorr(a: np.ndarray, b: np.ndarray, max_lag: int) -> tuple[int, float]:
    """Best lag k and its correlation, where k>0 means `a` leads `b`."""
    a, b = zscore(a), zscore(b)
    best = (0, 0.0)
    for k in range(-max_lag, max_lag + 1):
        if k > 0:
            u, v = a[:-k], b[k:]
        elif k < 0:
            u, v = a[-k:], b[:k]
        else:
            u, v = a, b
        if len(u) < 20:
            continue
        c = float(np.corrcoef(u, v)[0, 1]) if u.std() and v.std() else 0.0
        if abs(c) > abs(best[1]):
            best = (k, c)
    return best


def granger(cause: np.ndarray, effect: np.ndarray, lags: int) -> float:
    """p-value that `cause` Granger-causes `effect`. Lower means stronger evidence."""
    n = len(effect) - lags
    if n < 30:
        return 1.0
    y = effect[lags:]
    own = np.column_stack([effect[lags - i - 1 : -i - 1] for i in range(lags)] + [np.ones(n)])
    both = np.column_stack(
        [effect[lags - i - 1 : -i - 1] for i in range(lags)]
        + [cause[lags - i - 1 : -i - 1] for i in range(lags)]
        + [np.ones(n)]
    )
    rss = []
    for X in (own, both):
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        rss.append(float(((y - X @ beta) ** 2).sum()))
    rss_r, rss_u = rss
    df1, df2 = lags, n - both.shape[1]
    if df2 <= 0 or rss_u <= 0:
        return 1.0
    f = ((rss_r - rss_u) / df1) / (rss_u / df2)
    return float(1 - stats.f.cdf(f, df1, df2)) if f > 0 else 1.0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--entities", nargs="*", default=list(PATTERNS))
    parser.add_argument("--since", default="2024-05-20")
    parser.add_argument("--until", default="2026-03-10")
    parser.add_argument("--max-lag", type=int, default=10)
    parser.add_argument("--lags", type=int, default=3, help="lags for the Granger regression")
    args = parser.parse_args(argv)

    lines = [
        "# Lead and lag between sources",
        "",
        "Computed by `analysis/methods/leadlag.py` over the parallel Twitter / Reddit /",
        "Discord recaps, which cover the same day in the same issue.",
        "",
        f"Window {args.since} → {args.until} — the format regime where all three sections",
        "are reliably present (see `changepoints.md`). Lag is in issues, not days, since",
        "the newsletter skips weekends.",
        "",
        "`k > 0` means the first source leads. Granger p-values below 0.05 are bolded.",
        "",
        "| Entity | Pair | Best lag | Corr | Granger p |",
        "|---|---|---|---|---|",
    ]

    tally: dict[str, list[int]] = {}
    for name in args.entities:
        if name not in PATTERNS:
            continue
        pattern = re.compile(PATTERNS[name], re.I)
        dates, ser = series(pattern, args.since, args.until)
        if len(dates) < 60:
            continue
        for a, b in (("discord", "twitter"), ("discord", "reddit"), ("reddit", "twitter")):
            if ser[a].std() == 0 or ser[b].std() == 0:
                continue
            k, c = xcorr(ser[a], ser[b], args.max_lag)
            p = granger(ser[a], ser[b], args.lags)
            mark = f"**{p:.3f}**" if p < 0.05 else f"{p:.3f}"
            lines.append(f"| {name} | {a} → {b} | {k:+d} | {c:+.2f} | {mark} |")
            if p < 0.05:
                tally.setdefault(f"{a} → {b}", []).append(k)

    lines += ["", "## Significant Granger relationships", ""]
    if tally:
        lines += ["| Direction | Entities with p < 0.05 | Median best lag |", "|---|---|---|"]
        for pair, ks in sorted(tally.items(), key=lambda kv: -len(kv[1])):
            lines.append(f"| {pair} | {len(ks)} | {int(np.median(ks)):+d} |")
    else:
        lines.append("None — see the caveat below.")
    lines += [
        "",
        "**Caveat that limits all of this:** the three recaps are written *from the same",
        "issue on the same day*, so a same-day story appears in all three at lag 0 by",
        "construction. What can be detected is only a source discussing something for",
        "days before or after the others — not who published first in the real world.",
        "",
    ]

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    for pair, ks in sorted(tally.items(), key=lambda kv: -len(kv[1])):
        print(f"  {pair}: {len(ks)} significant, median lag {int(np.median(ks)):+d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
