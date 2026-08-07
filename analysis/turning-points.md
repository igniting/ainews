# Turning points

Novelty / Transience / Resonance (Barron et al., PNAS 2018), computed by
`analysis/methods/novelty.py` over LDA topic distributions of the issue bodies.

- **Novelty** — how different an issue is from the preceding 20 issues.
- **Transience** — how fast the conversation reverts afterwards.
- **Resonance** = novelty − transience. High resonance means the change *stuck*.

Ranking by novelty finds loud days. Ranking by resonance finds the days the
field actually changed direction — which is the distinction that title-based
analysis cannot make.

*40 topics, window 20, 8000 vocabulary terms, 601 issues from 2024-04-01 to 2026-08-06.*

> Restricted to 2024-04 onward by default: median issue length grew from 8,040
> words (Dec 2023) to 26,850 (Mar 2024), and that structural expansion produces
> far larger KL divergences than any news event. Run with `--since 2023-12-01`
> to see it dominate the rankings.
>
> Novelty and transience are z-scored against a local baseline of +/-60 issues:
> raw novelty falls ~15x from 2024H2 to 2025H2 as the issues get more templated,
> so an unstandardized ranking returns a list of 2024 dates and nothing else.

## Highest resonance — the conversation changed and stayed changed

| Date | Issue | Novelty | Transience | Resonance |
|---|---|---|---|---|
| 2026-03-17 | not-much | 6.496 | 0.641 | **5.856** |
| 2025-11-25 | flux2 | 4.352 | 0.704 | **3.648** |
| 2026-03-10 | ami-labs | 2.890 | -0.036 | **2.927** |
| 2026-03-11 | not-much | 2.896 | -0.021 | **2.917** |
| 2026-03-18 | not-much | 2.448 | -0.006 | **2.453** |
| 2025-10-16 | claude-skills | 2.498 | 0.155 | **2.343** |
| 2025-02-26 | ainews-lots-of-small-launches | 1.505 | -0.704 | **2.208** |
| 2025-03-03 | ainews-anthropics-dollar615b-series-e | 1.610 | -0.580 | **2.190** |
| 2025-12-05 | not-much | 1.953 | -0.085 | **2.038** |
| 2025-12-02 | mistral-3 | 2.043 | 0.014 | **2.030** |
| 2025-02-28 | ainews-not-much-happened-today | 1.276 | -0.709 | **1.986** |
| 2026-03-19 | not-much | 1.858 | -0.102 | **1.960** |
| 2026-03-13 | not-much | 1.540 | -0.399 | **1.939** |
| 2026-03-16 | not-much | 2.098 | 0.217 | **1.881** |
| 2026-03-12 | not-much | 1.736 | -0.047 | **1.783** |
| 2025-11-18 | gemini-3 | 2.005 | 0.234 | **1.771** |
| 2024-05-21 | ainews-anthropics-llm-genome-project-learning-and-clamping-34m-features-on-claude-sonnet | 0.714 | -1.043 | **1.758** |
| 2024-05-22 | ainews-all-of-ai-engineering-in-one-place | 0.718 | -1.034 | **1.752** |
| 2025-02-25 | ainews-not-much-happened-today | 1.188 | -0.555 | **1.743** |
| 2026-03-26 | not-much | 1.987 | 0.247 | **1.739** |

## Highest novelty — loud days (many of which did not stick)

| Date | Issue | Novelty | Transience | Resonance |
|---|---|---|---|---|
| 2025-04-21 | not-much-resend | **7.415** | 6.133 | 1.282 |
| 2026-03-17 | not-much | **6.496** | 0.641 | 5.856 |
| 2025-08-12 | not-much | **6.404** | 7.619 | -1.215 |
| 2025-04-22 | not-much | **5.082** | 5.055 | 0.027 |
| 2025-11-25 | flux2 | **4.352** | 0.704 | 3.648 |
| 2024-08-15 | ainews-not-much-happened-today | **3.124** | 1.560 | 1.564 |
| 2024-08-16 | ainews-not-much-happened-today | **2.924** | 1.681 | 1.243 |
| 2024-08-13 | ainews-gemini-live | **2.909** | 2.352 | 0.557 |
| 2026-03-11 | not-much | **2.896** | -0.021 | 2.917 |
| 2026-03-10 | ami-labs | **2.890** | -0.036 | 2.927 |
| 2024-08-21 | ainews-ideogram-2-berkeley-function-calling-leaderboard-v2 | **2.717** | 1.507 | 1.209 |
| 2024-08-14 | ainews-grok-2-and-chatgpt-4o-latest-confuses-everybody | **2.711** | 2.558 | 0.153 |
| 2025-10-16 | claude-skills | **2.498** | 0.155 | 2.343 |
| 2024-08-19 | ainews-the-dspy-roadmap | **2.493** | 2.795 | -0.301 |
| 2026-03-18 | not-much | **2.448** | -0.006 | 2.453 |
| 2025-04-18 | ainews-grok-3-and-3-mini-now-api-available | **2.345** | 1.516 | 0.829 |
| 2024-09-05 | ainews-replit-agent-how-did-everybody-beat-devin-to-market | **2.199** | 2.302 | -0.103 |
| 2026-03-16 | not-much | **2.098** | 0.217 | 1.881 |
| 2024-08-02 | ainews-execuhires-tempting-the-wrath-of-khan | **2.073** | 1.538 | 0.535 |
| 2025-12-02 | mistral-3 | **2.043** | 0.014 | 2.030 |
