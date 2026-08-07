# How long models stay in the conversation

Kaplan-Meier survival estimates from `analysis/methods/survival.py`.

A model is **dead** if it has not been mentioned in the last 90 days of
the corpus, and **right-censored** (still alive) otherwise. Censoring is the point:
a model first seen recently and still discussed has an unfinished life, and
averaging raw spans would understate exactly the newest models you most want to
compare.

| Cohort | Models | Died | Still alive | Median lifespan | 25% gone by | 75% gone by |
|---|---|---|---|---|---|---|
| All models | 255 | 217 | 38 | 137 d | 54 d | 293 d |
| Chinese labs | 49 | 40 | 9 | 85 d | 35 d | 178 d |
| US frontier labs | 161 | 141 | 20 | 175 d | 77 d | 325 d |
| Open-weights families | 100 | 90 | 10 | 117 d | 37 d | 237 d |
| Other / closed | 155 | 127 | 28 | 146 d | 58 d | 317 d |

## Longest-lived models

| Model | Days from first to last mention | Status |
|---|---|---|
| gemini | 973 | still active |
| chatgpt | 964 | still active |
| gpt-4 | 959 | still active |
| claude-3-sonnet | 848 | still active |
| copilot | 845 | ended |
| claude | 779 | still active |
| opus | 749 | ended |
| claude-3 | 735 | ended |
| gpt-5 | 734 | ended |
| qwen | 712 | still active |
| mistral | 701 | ended |
| gpt-4.5 | 699 | ended |
| llama-3 | 683 | ended |
| gemini-1.5-pro | 677 | ended |
| claude-opus | 671 | ended |
| grok | 664 | ended |
| gemma | 657 | ended |
| mixtral-8x7b | 640 | ended |
| mistral-7b | 590 | ended |
| claude-3-haiku | 590 | ended |

