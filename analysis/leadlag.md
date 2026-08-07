# Lead and lag between sources

Computed by `analysis/methods/leadlag.py` over the parallel Twitter / Reddit /
Discord recaps, which cover the same day in the same issue.

Window 2024-05-20 → 2026-03-10 — the format regime where all three sections
are reliably present (see `changepoints.md`). Lag is in issues, not days, since
the newsletter skips weekends.

`k > 0` means the first source leads. Granger p-values below 0.05 are bolded.

| Entity | Pair | Best lag | Corr | Granger p |
|---|---|---|---|---|
| Meta Llama | discord → twitter | +2 | +0.51 | **0.000** |
| Meta Llama | discord → reddit | +0 | +0.56 | **0.000** |
| Meta Llama | reddit → twitter | +1 | +0.37 | **0.000** |
| Mistral | discord → twitter | +0 | +0.47 | **0.000** |
| Mistral | discord → reddit | +0 | +0.33 | **0.000** |
| Mistral | reddit → twitter | +0 | +0.37 | 0.373 |
| DeepSeek | discord → twitter | +0 | +0.73 | **0.000** |
| DeepSeek | discord → reddit | +0 | +0.75 | **0.000** |
| DeepSeek | reddit → twitter | +0 | +0.70 | **0.032** |
| Qwen | discord → twitter | +0 | +0.41 | **0.004** |
| Qwen | discord → reddit | +0 | +0.30 | **0.003** |
| Qwen | reddit → twitter | +0 | +0.22 | 0.334 |
| Kimi/Moonshot | discord → twitter | +0 | +0.62 | **0.016** |
| Kimi/Moonshot | discord → reddit | +1 | +0.50 | **0.000** |
| Kimi/Moonshot | reddit → twitter | -1 | +0.60 | **0.000** |
| GLM/z.ai | discord → twitter | +4 | +0.39 | **0.000** |
| GLM/z.ai | discord → reddit | +0 | +0.32 | **0.026** |
| GLM/z.ai | reddit → twitter | +0 | +0.38 | **0.000** |
| MiniMax | discord → twitter | +0 | +0.51 | **0.000** |
| MiniMax | discord → reddit | +0 | +0.58 | **0.000** |
| MiniMax | reddit → twitter | +0 | +0.34 | **0.000** |
| Claude | discord → twitter | -7 | -0.14 | **0.016** |
| Claude | discord → reddit | +0 | +0.39 | **0.002** |
| Claude | reddit → twitter | +0 | +0.20 | 0.595 |
| GPT/OpenAI | discord → twitter | +0 | +0.40 | **0.008** |
| GPT/OpenAI | discord → reddit | +0 | +0.27 | 0.273 |
| GPT/OpenAI | reddit → twitter | -6 | -0.07 | 0.665 |
| Gemini | discord → twitter | +0 | +0.49 | **0.010** |
| Gemini | discord → reddit | +0 | +0.47 | **0.001** |
| Gemini | reddit → twitter | +0 | +0.46 | **0.002** |
| reasoning | discord → twitter | +0 | +0.31 | **0.027** |
| reasoning | discord → reddit | +0 | +0.26 | **0.014** |
| reasoning | reddit → twitter | +0 | +0.21 | **0.033** |
| RAG/retrieval | discord → twitter | -9 | +0.29 | **0.010** |
| RAG/retrieval | discord → reddit | +7 | +0.14 | 0.059 |
| RAG/retrieval | reddit → twitter | +10 | +0.15 | 0.183 |
| fine-tuning | discord → twitter | +8 | +0.28 | **0.000** |
| fine-tuning | discord → reddit | +2 | +0.24 | **0.000** |
| fine-tuning | reddit → twitter | -3 | +0.22 | 0.087 |
| agentic | discord → twitter | -1 | +0.35 | **0.024** |
| agentic | discord → reddit | +5 | +0.22 | **0.046** |
| agentic | reddit → twitter | -6 | +0.11 | 0.549 |
| MCP | discord → twitter | +0 | +0.22 | 0.083 |
| MCP | discord → reddit | -4 | +0.14 | 0.142 |
| MCP | reddit → twitter | +0 | +0.17 | 0.783 |

## Significant Granger relationships

| Direction | Entities with p < 0.05 | Median best lag |
|---|---|---|
| discord → twitter | 14 | +0 |
| discord → reddit | 12 | +0 |
| reddit → twitter | 7 | +0 |

**Caveat that limits all of this:** the three recaps are written *from the same
issue on the same day*, so a same-day story appears in all three at lag 0 by
construction. What can be detected is only a source discussing something for
days before or after the others — not who published first in the real world.

