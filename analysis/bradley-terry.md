# Capability ranking as the discourse asserted it

Bradley-Terry strengths fitted by `analysis/methods/bradley_terry.py` to
**801 dated pairwise comparative claims** extracted from the issue
bodies ("X beats Y", "matches", "outperforms", "on par with", "Y-level").

This is *not* a benchmark. It measures what the field said about relative
capability, which is exactly why it is worth comparing against what was
actually true.

Scores are normalized to mean 1. Only the largest connected component of the
comparison graph is scored (60 families, 20 with 20+ comparisons) — strengths are unidentifiable across
components, and fitting anyway would invent them.

| Rank | Model family | BT strength | Comparisons |
|---|---|---|---|
| 1 | glm | 3.19 | 36 |
| 2 | kimi | 2.27 | 21 |
| 3 | qwen3 | 1.67 | 53 |
| 4 | gemma | 1.61 | 53 |
| 5 | deepseek-v3 | 1.45 | 22 |
| 6 | fable | 1.36 | 22 |
| 7 | qwen | 1.33 | 94 |
| 8 | gpt-5 | 0.86 | 84 |
| 9 | mistral | 0.81 | 107 |
| 10 | phi | 0.79 | 26 |
| 11 | opus | 0.79 | 102 |
| 12 | grok | 0.76 | 54 |
| 13 | gemini | 0.70 | 129 |
| 14 | llama | 0.62 | 91 |
| 15 | claude | 0.46 | 200 |
| 16 | openai-o-series | 0.33 | 42 |
| 17 | chatgpt | 0.33 | 28 |
| 18 | gpt-3.5 | 0.28 | 34 |
| 19 | gpt-4 | 0.21 | 174 |
| 20 | gpt-4o | 0.18 | 57 |

## Launch-asymmetry diagnostic

A model is the claimant when it launches and the incumbent only later, so
rarely-compared models are near-undefeated by construction. Win rate should
fall towards 0.5 as comparisons accumulate, and it does:

| Comparisons | Models | Mean win rate |
|---|---|---|
| 3-7 | 13 | 0.61 |
| 8-15 | 6 | 0.49 |
| 16-40 | 8 | 0.42 |
| 41+ | 13 | 0.39 |

This is why the ranking below uses a high comparison threshold. Read the
strengths as *what the field asserted about models it argued about repeatedly*,
not as a benchmark.


## By period

Strength within each half-year, refitted from that period's claims only.

| Model | 2023H2 | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 | 2026H2 |
|---|---|---|---|---|---|---|---|
| glm | — | — | — | — | — | 1.74 | 1.40 |
| kimi | — | — | — | — | 0.48 | 2.64 | 1.86 |
| qwen3 | — | — | — | 1.36 | 1.39 | 0.72 | 1.67 |
| gemma | — | 1.73 | 1.58 | 0.57 | — | 0.65 | — |
| deepseek-v3 | — | — | 0.87 | 0.74 | 2.53 | 0.64 | 1.34 |
| fable | — | — | — | — | — | 1.73 | 0.63 |
| qwen | — | 4.41 | 2.92 | 0.94 | 1.08 | 0.37 | 0.49 |
| gpt-5 | — | — | — | 0.25 | 1.19 | 0.66 | 1.09 |
| mistral | 2.00 | 0.46 | 1.70 | 1.03 | — | 3.03 | — |
| phi | — | 0.79 | 0.31 | 2.21 | — | — | — |
| opus | — | 0.94 | — | 1.60 | 1.87 | 0.30 | 0.33 |
| grok | — | 0.61 | 1.63 | 0.54 | 0.60 | — | 0.75 |
| gemini | 0.95 | 0.29 | 2.13 | 0.51 | 1.42 | 0.62 | — |
| llama | — | 0.70 | 0.77 | 0.63 | 1.02 | — | — |

