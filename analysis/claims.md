# Numbers the archive asserted

Extracted by `analysis/methods/claims.py` from the issue bodies. None of this is
in the front-matter tags, so every tag-based analysis in this repo is blind to it.

| Claim type | Extracted |
|---|---|
| price | 151 |
| benchmark | 176 |
| context | 1,335 |
| params | 990 |

## Claimed price per 1M tokens

Median and 10th percentile of every `$X per 1M tokens` claim in each period.
The 10th percentile tracks the cheap frontier — the budget option available at
the time — while the median tracks what was typically being discussed.

| Period | Claims | Median $/1M | 10th pct $/1M |
|---|---|---|---|
| 2024H1 | 22 | $0.42 | $0.10 |
| 2024H2 | 26 | $4.00 | $0.11 |
| 2025H1 | 35 | $8.00 | $0.42 |
| 2025H2 | 25 | $2.50 | $0.45 |
| 2026H1 | 28 | $3.00 | $0.13 |
| 2026H2 | 15 | $3.00 | $0.29 |

Median claimed price moved **$0.42 → $3.00** (2024H1 → 2026H2), and the cheap frontier **$0.10 → $0.29**.

## Claimed context windows

| Period | Claims | Median | Largest claimed |
|---|---|---|---|
| 2023H2 | 32 | 24K | 2.0M |
| 2024H1 | 405 | 128K | 100.0M |
| 2024H2 | 149 | 128K | 100.0M |
| 2025H1 | 194 | 100K | 100.0M |
| 2025H2 | 230 | 256K | 100.0M |
| 2026H1 | 286 | 258K | 100.0M |
| 2026H2 | 39 | 1,000K | 50.0M |

## Claimed parameter counts

| Period | Claims | Median | Largest |
|---|---|---|---|
| 2023H2 | 11 | 7B | 11B |
| 2024H1 | 282 | 70B | 1,800B |
| 2024H2 | 135 | 12B | 1,800B |
| 2025H1 | 258 | 12B | 5,000B |
| 2025H2 | 177 | 27B | 3,000B |
| 2026H1 | 106 | 22B | 10,000B |
| 2026H2 | 21 | 975B | 2,800B |

## Benchmarks by how often a score was claimed

Each benchmark's first and last claimed score dates its era. A benchmark that
stops being cited has usually been saturated.

| Benchmark | Claims | First | Last | Median score |
|---|---|---|---|---|
| swe-bench | 20 | 2024-04-02 | 2026-06-03 | 55% |
| aime | 15 | 2025-01-20 | 2026-06-03 | 63% |
| mmlu | 13 | 2024-03-04 | 2026-03-20 | 78% |
| math | 13 | 2024-04-12 | 2025-10-13 | 84% |
| arc | 10 | 2025-08-07 | 2026-07-09 | 50% |
| arc-agi-2 | 10 | 2025-10-09 | 2026-08-06 | 52% |
| terminal-bench | 8 | 2026-05-04 | 2026-08-05 | 80% |
| gpqa | 7 | 2024-03-04 | 2025-11-11 | 60% |
| frontiermath | 7 | 2024-12-20 | 2026-05-12 | 31% |
| gsm8k | 4 | 2024-02-03 | 2024-07-15 | 44% |
| cifar10 | 4 | 2024-02-22 | 2024-02-23 | 95% |
| humaneval | 4 | 2024-04-09 | 2024-09-25 | 59% |
| alpacaeval | 4 | 2024-06-11 | 2024-07-03 | 65% |
| arc-agi | 4 | 2024-10-30 | 2025-12-29 | 65% |
| arc-agi-1 | 4 | 2025-07-23 | 2026-08-06 | 56% |

*Caveat:* subjects are not resolved — a claimed score is not attributed to the
model it belongs to, so these are field-level distributions, not per-model
results. Attribution needs the sentence parsed, not just matched.

