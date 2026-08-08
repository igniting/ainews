# How long models stay in the conversation

Kaplan-Meier survival estimates from `analysis/methods/survival.py`.

A model is **dead** if it has not been mentioned in the last 90 days of
the corpus, and **right-censored** (still alive) otherwise. Censoring is the point:
a model first seen recently and still discussed has an unfinished life, and
averaging raw spans would understate exactly the newest models you most want to
compare.

| Cohort | Models | Died | Still alive | Median lifespan | 25% gone by | 75% gone by |
|---|---|---|---|---|---|---|
| All models | 140 | 99 | 41 | 254 d | 98 d | 642 d |
| Chinese labs | 21 | 13 | 8 | 398 d | 143 d | nan d |
| US frontier labs | 49 | 31 | 18 | 315 d | 168 d | 731 d |
| Open-weights families | 43 | 33 | 10 | 273 d | 88 d | 678 d |
| Other / closed | 97 | 66 | 31 | 231 d | 101 d | 623 d |

## Longest-lived models

| Model | Days from first to last mention | Status |
|---|---|---|
| gemini | 973 | still active |
| gpt | 966 | still active |
| chatgpt | 964 | still active |
| glm | 939 | still active |
| claude | 931 | still active |
| qwen | 917 | still active |
| mamba | 895 | still active |
| claude-opus | 882 | still active |
| gemma | 873 | still active |
| grok | 861 | still active |
| deepseek | 855 | still active |
| claude-sonnet | 848 | still active |
| eagle | 847 | still active |
| copilot | 845 | ended |
| opus | 826 | still active |
| deepseek-v | 820 | still active |
| mai | 757 | still active |
| mistral | 731 | ended |
| llama | 730 | ended |
| hermes | 725 | ended |

