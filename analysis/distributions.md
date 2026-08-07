# Distributional structure of attention

Computed by `analysis/methods/distributions.py` over the front-matter company
tags.

## Diversity: is attention concentrating or fragmenting?

**Hill numbers** are entropies expressed as an *effective number of entities*,
which makes them directly readable: Hill-1 of 12 means the period's coverage was
equivalent to 12 equally-discussed companies. Hill-2 weights the dominant
entities more heavily.

| Period | Distinct | Hill-1 (effective) | Hill-2 | Shannon | Gini | Top-3 share |
|---|---|---|---|---|---|---|
| 2023H2 | 34 | **21.7** | 14.4 | 3.08 | 0.48 | 36% |
| 2024H1 | 184 | **64.5** | 29.7 | 4.17 | 0.65 | 25% |
| 2024H2 | 215 | **76.9** | 33.0 | 4.34 | 0.64 | 24% |
| 2025H1 | 212 | **75.5** | 32.9 | 4.32 | 0.64 | 22% |
| 2025H2 | 247 | **101.8** | 44.3 | 4.62 | 0.61 | 19% |
| 2026H1 | 207 | **88.1** | 37.2 | 4.48 | 0.59 | 22% |
| 2026H2 | 82 | **62.8** | 46.0 | 4.14 | 0.35 | 16% |

Effective number of companies moved **21.7 → 62.8** (2023H2 → 2026H2), against a raw count of 34 → 82.

## Rank-turbulence divergence: 2024H1 vs 2026H1

Total divergence **26.67** at alpha=0.33. Elements absent from one
side are ranked just past that side's last place, so absence contributes rather
than being dropped — the reason this complements the log-odds view.

| Entity | Rank 2024H1 | Rank 2026H1 | Contribution | Direction |
|---|---|---|---|---|
| mistral-ai | 2 | 66 | 0.635 | fell |
| hugging-face | 3 | 20 | 0.427 | fell |
| langchain | 12 | 3 | 0.367 | rose |
| cursor | 122 | 11 | 0.351 | rose |
| ollama | 22 | 6 | 0.310 | rose |
| github | — | 14 | 0.309 | new in 2026H1 |
| baseten | 122 | 14 | 0.309 | rose |
| stability-ai | 16 | — | 0.306 | gone by 2026H1 |
| artificial-analysis | — | 16 | 0.290 | new in 2026H1 |
| meta-ai-fair | 6 | 24 | 0.284 | fell |
| thebloke | 20 | — | 0.274 | gone by 2026H1 |
| groq | 21 | — | 0.267 | gone by 2026H1 |
| vllm | — | 20 | 0.265 | new in 2026H1 |
| cursor_ai | — | 20 | 0.265 | new in 2026H1 |
| openrouter | 122 | 20 | 0.265 | rose |
| cohere | 11 | 45 | 0.263 | fell |
| llamaindex | 14 | 66 | 0.262 | fell |
| anthropic | 4 | 2 | 0.257 | rose |
| scale-ai | 24 | 144 | 0.248 | fell |
| cognition | 49 | 13 | 0.243 | rose |

