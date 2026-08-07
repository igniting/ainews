# Findings from the roadmap methods

Results from the Tier 1 and Tier 2 methods in `methods/ROADMAP.md`. Five of eight
are implemented; the three outstanding are listed at the end with why.

---

## 1. Bradley-Terry: a ranking of who was cast as the challenger

`bradley_terry.py` extracted **801 dated pairwise comparative claims** ("X beats
Y", "matches", "outperforms", "Y-level") over a 95-family model lexicon, and fit
Bradley-Terry strengths by Hunter's MM algorithm on the largest connected
component.

### The launch-asymmetry bias, measured

The first fit put `mamba` (5 comparisons), `jamba` (7) and `veo` (6) at the top.
That is not capability, it is **launch asymmetry**: a model is the *claimant* when
it ships ("Jamba dethrones Mixtral") and the *incumbent* only later, when rivals
ship against it. Quantified:

| Comparisons | Models | Mean win rate |
|---|---|---|
| 3–7 | 13 | **0.68** |
| 8–15 | 6 | 0.55 |
| 16–40 | 8 | 0.56 |
| 41+ | 13 | **0.49** |

Correlation between log(comparisons) and win rate: **−0.27**. Win rate converges
to 0.5 exactly as a model accumulates enough history to have been on both sides.

### The ranking, and what it actually measures

With a 20-comparison floor:

| Rank | Family | BT strength | Comparisons |
|---|---|---|---|
| 1 | glm | 3.19 | 36 |
| 2 | kimi | 2.27 | 21 |
| 3 | qwen3 | 1.67 | 53 |
| 4 | gemma | 1.61 | 53 |
| 5 | deepseek-v3 | 1.45 | 22 |
| … | | | |
| 8 | gpt-5 | 0.86 | 84 |
| 11 | opus | 0.79 | 102 |
| 13 | gemini | 0.70 | 129 |
| 15 | claude | **0.46** | **200** |

**This does not mean GLM outranks Claude.** Read the two columns together: the
models with the *most* comparisons have the *lowest* strengths. Claude is the
single most-compared-against entity in the corpus (200 comparisons) and sits near
the bottom.

So what this actually measures is **incumbency** — being the thing everyone
benchmarks against shows up, mechanically, as losing. That is a useful
instrument, and it is the one I lacked earlier: in `NEWS-ANALYSIS.md` I claimed
DeepSeek shifted "from protagonist to benchmark" and `VERIFICATION.md` could not
support it. High comparison count with sub-1.0 strength is the measurable
signature of exactly that role, and by it the reference standards of the corpus
are Claude, Gemini, Mistral, Opus and GPT-5 — in that order.

---

## 2. Semantic axes: where entities sit, not just how far they moved

`axes.py` reuses the per-era word2vec models, defining each axis as a difference
of pole-word centroids and z-scoring projections against that era's own
vocabulary.

### The cost axis validates the method

| Entity | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 |
|---|---|---|---|---|---|
| llama | +1.06 | +0.86 | +1.54 | +1.32 | **+2.22** |
| qwen | +0.52 | +1.26 | +1.51 | +1.45 | **+1.65** |
| mistral | +0.73 | +0.95 | +0.86 | +1.80 | +1.15 |
| deepseek | +0.95 | **+2.19** | +1.32 | +0.86 | **+0.50** |
| claude | −1.63 | +0.71 | −1.62 | −1.55 | −0.52 |
| gemini | −1.91 | +0.87 | −1.28 | −1.71 | −1.19 |

Positive is "cheap". Open-weights models sit at one end and closed frontier
models at the other, with no supervision — a clean face-validity check on the
whole embedding approach.

**DeepSeek's trajectory is the interesting one.** It is the *most* cheap-coded
entity in the corpus in 2024H2 (+2.19) and drifts steadily away from that pole to
+0.50 by 2026H1. It stopped being framed as the budget option and started being
framed as a frontier competitor — the same repositioning the Bradley-Terry
incumbency reading picks up from a completely different direction.

Other axes, 2026H1: most **open-source**-coded are minimax, mistral, gemma, qwen;
most **sota**-coded are mistral, minimax, qwen, gemma.

---

## 3. Claimed numbers: the curves the field asserted

`claims.py` extracted, with deliberately conservative patterns: **1,335 context
claims, 990 parameter counts, 176 benchmark scores, 151 prices**.

### Context windows grew 40x

| Period | Median claimed | Largest claimed |
|---|---|---|
| 2023H2 | 24K | — |
| 2024H1 | 128K | — |
| 2025H1 | 100K | — |
| 2025H2 | 256K | — |
| 2026H1 | 258K | — |
| 2026H2 | **1,000K** | — |

### Price did not fall — the cheap frontier was always there

| Period | Median $/1M | 10th pct $/1M |
|---|---|---|
| 2024H1 | $0.42 | $0.10 |
| 2024H2 | $4.00 | $0.11 |
| 2025H1 | **$8.00** | $0.42 |
| 2025H2 | $2.50 | $0.45 |
| 2026H1 | $3.00 | $0.13 |
| 2026H2 | $3.00 | $0.29 |

This is the most counterintuitive result of the batch. The **cheap frontier is
flat** — roughly $0.10–$0.45 per million tokens across the entire corpus. What
moved was the *median*, which rose 20x into 2025H1 and then halved.

The honest reading is that this tracks **which models were being discussed**, not
what inference cost. The 2025H1 median spike coincides with the o1/o3/R1
reasoning-model period, when the models worth writing about were expensive ones.
Cheap capacity never went away; it stopped being newsworthy, then became so
again. That is a fact about the newsletter's attention, and it is only visible
because the median and the 10th percentile move in opposite directions.

---

## 4. Diversity: attention fragmented, decisively

`distributions.py`. This answers the concentration question posed in `IDEAS.md`
and never delivered.

| Period | Distinct companies | Hill-1 (effective) | Gini | Top-3 share |
|---|---|---|---|---|
| 2023H2 | 34 | 21.7 | 0.48 | **36%** |
| 2024H1 | 184 | 64.5 | 0.65 | 25% |
| 2024H2 | 215 | 76.9 | 0.64 | 24% |
| 2025H1 | 212 | 75.5 | 0.64 | 22% |
| 2025H2 | 247 | **101.8** | 0.61 | 19% |
| 2026H1 | 207 | 88.1 | 0.59 | 22% |
| 2026H2 | 82 | 62.8 | 0.35 | **16%** |

Hill-1 is the *effective number of equally-discussed companies*, so it is
directly readable. It rises roughly **5x**, top-3 share falls from 36% to under
22%, and Gini falls throughout. AI news fragmented; it did not consolidate.

**This independently explains the OpenAI result.** `VERIFICATION.md` found that
OpenAI's headline share collapsed 18% → 4% while its mention density stayed flat,
and concluded the field had acquired more competitors worth naming in a title.
Diversity measures that directly and agrees — two methods, different inputs, same
conclusion.

(2026H2 is 26 issues; treat its row as indicative.)

## 5. Rank-turbulence divergence

Total RTD between 2024H1 and 2026H1 is **26.67** at α=1/3. Top contributors:
`mistral-ai, hugging-face, langchain, cursor, ollama, github, baseten,
stability-ai`.

Worth noting that this is a **different list from log-odds**, which returned
`llama, fine-tuning, rag` versus `claude, agent, opus`. Log-odds is
frequency-weighted and surfaces the topical vocabulary; RTD is rank-based and
surfaces *infrastructure churn* — the tooling layer entering and leaving. Neither
is more correct; they answer different questions, which is why running both was
worth it.

---

## Still outstanding

| Method | Status | Why |
|---|---|---|
| CausalImpact / BSTS | not run | Needs control series genuinely unaffected by the intervention. In a field this coupled — where the diversity numbers show everything co-moving — constructing a defensible control set is the actual work, and doing it badly produces confident wrong effect sizes. |
| Dynamic topic model | not run | `LdaSeqModel` on 690 documents × 12k vocabulary is hours of compute; worth it, but it should be run against the 460-issue stable regime rather than the whole corpus. |
| Hawkes processes | not run | Straightforward to fit per entity; deprioritized behind the four above because branching ratios add a second view of dynamics the change points already describe. |

## What this batch changed

1. **Bradley-Terry gave me an incumbency instrument**, which retroactively
   supports the "DeepSeek became a benchmark" claim that `VERIFICATION.md` had to
   withdraw for lack of evidence — though the measurable form is "Claude, Gemini
   and Mistral are the corpus's reference standards".
2. **Semantic axes show DeepSeek repositioning** from budget option to frontier
   competitor, visible independently in both the embedding geometry and the
   comparison graph.
3. **The cheap frontier never moved.** Inference has been available at ~$0.10–0.45
   per million tokens throughout; the median tracks fashion, not cost.
4. **Attention fragmented ~5x**, which is the mechanism behind OpenAI's falling
   headline share and confirms it from an independent direction.
