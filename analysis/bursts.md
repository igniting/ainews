# Bursts

Kleinberg (2002) two-state burst detection, via `analysis/methods/bursts.py`.

Weekly bins. Trials are words and successes are mentions, so the rate is a Poisson
intensity on the text. Coarser units fail: issues-mentioning-X saturates at 80-97%,
and kilowords-as-trials clamps frequently-named entities to a rate of 1.
Burst state emits at 2.5x the baseline rate; entering a burst
costs gamma·ln(n) with gamma=1.5, so short noise cannot trigger one.
Unlike a threshold, the start and end dates are decoded, not chosen.

| Entity | Burst | Weeks | Mentions/10k words in burst | Baseline |
|---|---|---|---|---|
| Mistral | 2023-W49 → 2024-W13 | 17 | 42.9 | 9.5 |
| fine-tuning | 2023-W50 → 2023-W52 | 3 | 39.5 | 18.1 |
| fine-tuning | 2024-W02 → 2024-W04 | 3 | 35.9 | 18.1 |
| RAG/retrieval | 2024-W04 → 2024-W15 | 12 | 17.7 | 8.1 |
| fine-tuning | 2024-W06 → 2024-W08 | 3 | 33.7 | 18.1 |
| Claude | 2024-W10 → 2024-W11 | 2 | 38.5 | 13.6 |
| fine-tuning | 2024-W12 → 2024-W14 | 3 | 31.5 | 18.1 |
| Mistral | 2024-W15 → 2024-W16 | 2 | 28.0 | 9.5 |
| Meta Llama | 2024-W16 → 2024-W22 | 7 | 28.8 | 9.1 |
| RAG/retrieval | 2024-W17 → 2024-W18 | 2 | 17.2 | 8.1 |
| fine-tuning | 2024-W21 → 2024-W25 | 5 | 40.7 | 18.1 |
| RAG/retrieval | 2024-W27 → 2024-W29 | 3 | 16.7 | 8.1 |
| Meta Llama | 2024-W28 → 2024-W35 | 8 | 26.1 | 9.1 |
| Mistral | 2024-W29 → 2024-W30 | 2 | 25.2 | 9.5 |
| RAG/retrieval | 2024-W32 → 2024-W34 | 3 | 15.5 | 8.1 |
| Meta Llama | 2024-W39 → 2024-W40 | 2 | 25.4 | 9.1 |
| Qwen | 2024-W46 → 2024-W47 | 2 | 14.7 | 5.6 |
| DeepSeek | 2024-W52 → 2025-W01 | 2 | 35.6 | 9.8 |
| DeepSeek | 2025-W04 → 2025-W10 | 7 | 45.8 | 9.8 |
| reasoning | 2025-W04 → 2025-W11 | 8 | 27.5 | 11.5 |
| MCP | 2025-W04 → 2025-W29 | 26 | 21.3 | 7.7 |
| Claude | 2025-W09 → 2025-W10 | 2 | 43.4 | 13.6 |
| DeepSeek | 2025-W13 → 2025-W16 | 4 | 21.3 | 9.8 |
| Gemini | 2025-W13 → 2025-W23 | 11 | 30.2 | 12.9 |
| reasoning | 2025-W13 → 2025-W14 | 2 | 19.8 | 11.5 |
| Qwen | 2025-W18 → 2025-W19 | 2 | 15.4 | 5.6 |
| Claude | 2025-W21 → 2025-W22 | 2 | 29.3 | 13.6 |
| agentic | 2025-W23 → 2025-W25 | 3 | 43.2 | 22.8 |
| MiniMax | 2025-W25 → 2025-W26 | 2 | 4.1 | 0.9 |
| Gemini | 2025-W25 → 2025-W26 | 2 | 27.3 | 12.9 |
| Kimi/Moonshot | 2025-W28 → 2025-W39 | 12 | 13.4 | 4.4 |
| agentic | 2025-W29 → 2025-W30 | 2 | 44.5 | 22.8 |
| Qwen | 2025-W30 → 2025-W37 | 8 | 11.8 | 5.6 |
| GLM/z.ai | 2025-W31 → 2025-W34 | 4 | 3.5 | 1.0 |
| MCP | 2025-W31 → 2025-W32 | 2 | 13.0 | 7.7 |
| GPT/OpenAI | 2025-W32 → 2025-W33 | 2 | 115.1 | 34.0 |
| reasoning | 2025-W34 → 2025-W35 | 2 | 20.4 | 11.5 |
| MCP | 2025-W38 → 2025-W39 | 2 | 15.2 | 7.7 |
| Qwen | 2025-W39 → 2025-W41 | 3 | 12.6 | 5.6 |
| GLM/z.ai | 2025-W40 → 2025-W41 | 2 | 4.1 | 1.0 |
| Kimi/Moonshot | 2025-W41 → 2026-W03 | 15 | 13.2 | 4.4 |
| MiniMax | 2025-W44 → 2025-W46 | 3 | 6.7 | 0.9 |
| Gemini | 2025-W47 → 2025-W52 | 6 | 37.6 | 12.9 |
| GLM/z.ai | 2025-W50 → 2026-W32 | 35 | 5.1 | 1.0 |
| MCP | 2025-W50 → 2025-W51 | 2 | 14.0 | 7.7 |
| MiniMax | 2025-W52 → 2026-W03 | 4 | 3.9 | 0.9 |
| Claude | 2026-W03 → 2026-W04 | 2 | 24.0 | 13.6 |
| agentic | 2026-W04 → 2026-W06 | 3 | 42.7 | 22.8 |
| Kimi/Moonshot | 2026-W05 → 2026-W10 | 6 | 22.6 | 4.4 |
| MiniMax | 2026-W07 → 2026-W32 | 26 | 5.0 | 0.9 |
| Gemini | 2026-W07 → 2026-W09 | 3 | 24.4 | 12.9 |
| Qwen | 2026-W08 → 2026-W32 | 25 | 16.5 | 5.6 |
| Claude | 2026-W08 → 2026-W32 | 25 | 35.8 | 13.6 |
| agentic | 2026-W08 → 2026-W32 | 25 | 49.8 | 22.8 |
| Kimi/Moonshot | 2026-W12 → 2026-W13 | 2 | 15.5 | 4.4 |
| DeepSeek | 2026-W17 → 2026-W18 | 2 | 32.3 | 9.8 |
| Kimi/Moonshot | 2026-W29 → 2026-W32 | 4 | 39.0 | 4.4 |
| DeepSeek | 2026-W31 → 2026-W32 | 2 | 31.8 | 9.8 |

