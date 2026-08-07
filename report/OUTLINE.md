# Report outline

**Working title:** *The Attention Ledger: What 690 Days of AI's Daily Record Reveals About Where the Market Actually Went*

**Format:** single-page analytical HTML report, ~8,000–10,000 words, ~14 embedded
visualisations, self-contained (inline CSS/SVG, no external assets).

**Audience:** investors with technical fluency. Assumes the reader knows what MoE,
RAG and inference cost are; does not assume they know what a Hill number or
rank-turbulence divergence is, and explains those inline where used.

**Editorial stance:** technical news reporting, not a vendor deck. Every headline
claim carries its measurement, its sample, and its confound. The three claims we
*refuted* are printed as prominently as the ones we confirmed — an investor
paying for research is buying the error bars, not just the conclusions.

**The central thesis, stated once and defended throughout:**
> This corpus is a *contemporaneous, never-revised record of what the AI builder
> ecosystem believed on each day*. It is not a market dataset — it has no revenue,
> no headcount, no funding rounds except as reported. What it has, and what no
> market dataset has, is **attention with a timestamp and no hindsight**. Attention
> leads capital. This report measures where attention went, how fast, and where
> the corpus's own record shows the consensus was wrong.

---

## Front matter

**F1. Masthead and provenance box**
Dataset one-liner, period covered, word count, method count, code location,
reproducibility statement. Establishes this is instrumented, not impressionistic.

**F2. How to read this report — the confidence ladder**
A three-tier badge used on every finding throughout:
- **Confirmed** — holds under two or more independent methods
- **Measured** — one method, stated sample, stated confound
- **Contested** — we tested it and it failed, or the corpus cannot answer it

This device is the report's credibility spine and should appear in the first
screen. It also lets us print negative results as content rather than as apology.

**F3. Executive summary — eight findings, one line each**
Each links to its section. Written so a partner can read only this page.

---

## Part I — The instrument

*Why this dataset can support the claims that follow, and where it cannot.*

**I.1 What the corpus is**
690 issues, 2023-12-06 → 2026-08-06, 15.3M words, ~5 issues/week, 70% of all
calendar days. Sourced from the site behind the Substack archive. Structure of an
issue: editorial lede, then parallel Twitter / Reddit / Discord recaps.

**I.2 What is in it that nobody has mined**
The three embedded layers, with counts: Discord telemetry (31,688 channel-days,
2.15M messages, 56 servers), the tweet attribution graph (18,854 links), and
in-prose numeric claims (1,335 context, 990 parameter, 176 benchmark, 151 price).

**I.3 The four publishing regimes — and why they matter to a reader**
The PELT-detected regimes, with the honest framing: *every unsupervised method we
ran ranked format changes above every news event in three years until controlled
for.* This is where we earn the reader's trust — we show the instrument's
calibration before showing its readings.
- Regime table + the 460-issue stable core
- Sidebar: **"Three ways to measure the wrong thing confidently"** — presence
  saturation, length-tracking counts, titles-as-attention. Short, punchy, and the
  reason to believe the rest.

**I.4 What this corpus is not**
One editorial viewpoint, builder- and tooling-weighted. Under-covers enterprise
deployment, hardware supply chains, non-English ecosystems. It is a summary layer
written by an LLM and edited by a human — so it measures *reported* attention,
one step removed from the field.

---

## Part II — Market structure

*The three findings with the clearest investment read-through.*

**II.1 The open-weights frontier changed hands — and it is the largest movement in the corpus**
The headline chart of the whole report: China bloc vs Meta+Mistral mention
density, 73:1 inverting to 42:1, crossing in 2025H1.
- Per-lab breakdown: Kimi/Moonshot 0.1 → 35.9 per 10k words (359x, steepest of
  anything measured); GLM, MiniMax, Qwen trajectories
- The price framing that recurs in nearly every mention: "8% of Claude Sonnet's
  price", "11% of its cost", "10x cheaper"
- **Investor read:** the substitution was visible in daily coverage roughly four
  quarters before it was a consensus market view.

**II.2 Attention fragmented ~5x — and that, not decline, is what happened to OpenAI**
- Hill-1 effective company count 21.7 → 101.8; top-3 share 36% → 16–22%; Gini falling
- The OpenAI paradox resolved: headline share 18% → 4% while mention density held
  flat (59.1 → 51.1). Two independent methods, same conclusion.
- **Investor read:** category leadership stopped being winner-take-all in
  *attention* terms well before it did in revenue terms. Distribution of mindshare
  is the leading edge of distribution of spend.

**II.3 The incumbency index — a new instrument**
Bradley-Terry over 801 extracted pairwise claims, with the launch-asymmetry bias
measured and shown (win rate 0.68 at 3–7 comparisons → 0.49 at 41+).
- The counter-intuitive ranking, and why it inverts: most-compared = lowest strength
- Claude with 200 comparisons and the lowest strength is the corpus's reference standard
- **Investor read:** "being the thing everyone benchmarks against" is a measurable,
  dateable market position, distinct from either share or capability. It is
  arguably the single best moat proxy this dataset produces.

---

## Part III — Category dynamics

*What grew, what died, and the pattern that distinguishes the two.*

**III.1 Agents: the one-way door**
4% → 86% of issues; agentic mention density 7.0 → 52.8 per 10k words (7.5x). Never
retraces. Coding rises alongside (20% → 43%) because coding is where agents first
worked.

**III.2 Retrieval: the sharpest decline in the corpus — and the vendor split that matters**
- RAG domain 31% → 4%; density 16.3 → 2.0
- The mechanism, shown two ways: context windows ate it (context & memory 25% →
  48%) and agents absorbed it
- **The LangChain/LlamaIndex divergence**, which is the section's real payload:
  LangChain hits its *all-time high* (24% of issues, 2026H1) while its home domain
  collapses; LlamaIndex falls to 2%. The vendor that followed the workload into
  agents kept its coverage.
- **Investor read:** category death and vendor death are different events. The
  domain counts alone would have gotten this exactly backwards.

**III.3 The absorption pattern — why declining coverage usually means victory**
Retrieval, reasoning (66% → 31%) and multimodality (49% → 25%) all fell hard after
peaking, and all three won — they became infrastructure. Genuine failures look
different: they never peak. Robotics never exceeds 12%.
- The semantic proof: `agentic` sat next to *retrieval-augmented* in 2024 and next
  to *long-horizon, computer-use, swe* by 2026
- **Investor read:** the diligence question is not "is coverage falling" but "did
  it peak first". A category that peaked and faded is a solved problem with a
  shrinking premium; one that never peaked is a thesis that did not land.

**III.4 The categories the taxonomy missed**
Unsupervised NMF surfaced a **defense and national-security topic** rising 7x into
2026 (0.6% → 8.0%) that no hand-built category anticipated. Also: open
video-tooling as distinct from Sora/Veo; the small-model/function-calling era that
peaked in 2024H2 and vanished.
- **Investor read:** the hand-built taxonomy is the failure mode of most thematic
  research. Stated as a method warning, with our own miss as the example.

---

## Part IV — The economics the field asserted

**IV.1 The cheap frontier never moved**
The most counterintuitive chart in the report: median claimed $/1M tokens swings
$0.42 → $8.00 → $3.00 while the **10th percentile stays flat at $0.10–$0.45
throughout**.
- Why: the median tracks *which models were newsworthy*, not what inference cost.
  The 2025H1 spike is the o1/o3/R1 reasoning-model period.
- **Investor read:** "inference is collapsing in price" and "the cheap tier is
  newly available" are different claims, and only the first is true. Budget
  capacity was continuously available across the whole window.

**IV.2 Context windows: 40x, and the vocabulary that followed**
Median claimed context 24K → 1M. Paired with the semantic finding that `context`
acquired the neighbour `rot` — the field invented a failure mode for its own new
capability.

**IV.3 Parameter counts and what stopped being said**
Distribution over time; the shift from parameter count as headline metric to
active-parameter and cost-per-task framing.

---

## Part V — Positioning, measured from language

*The section with the most novel method and the most defensible per-company read.*

**V.1 How to read a semantic axis** (short methods explainer with a validation)
The cost axis separates open-weights from closed frontier models with no
supervision — printed as the method's own face-validity check before any
conclusion is drawn from it.

**V.2 DeepSeek's repositioning, visible from two directions**
Most cheap-coded entity in the corpus in 2024H2 (+2.19) drifting to +0.50 by
2026H1 — it stopped being framed as the budget option. The Bradley-Terry
incumbency reading shows the same repositioning from a completely independent
input.

**V.3 The vocabulary shifts that reprice categories**
Words whose frequency barely moved but whose meaning changed completely:
- `harness`: evaluation harness → agent harness
- `skills`: expertise → `skill.md`, a file format
- `prompt`: engineering → injection, jailbreaks (a craft became an attack surface)
- `distillation`: training technique → accusation
- `safety`: legislation (SB-1047, California) → agent security
- `r1`: the Rabbit gadget → DeepSeek (highest drift in the corpus, 0.921)
- `stability`: a company name decaying back into a common noun
- **Investor read:** each of these is a category boundary moving. "Prompt
  engineering" and "prompt security" are different markets, and the corpus dates
  the moment the word changed hands.

---

## Part VI — Timing and lifecycle

*The section a fund would use operationally.*

**VI.1 Hype lead time — how long the field talks about things that do not exist**
GPT-5 first mentioned 2023-12-07, peak 2025-08: **603 days**. Contrast with
unannounced arrivals: deepseek-r1 71 days, gemini-2.5-pro 36. The ratio is a
measure of how much discourse concerns unshipped product.

**VI.2 Bursts — dating the spikes without a threshold**
Kleinberg results table. The finding worth the section: **`reasoning` bursts in the
exact weeks as DeepSeek R1** (2025-W04→W10/W11), which is the cleanest evidence in
the corpus that R1 generalised reasoning from an OpenAI product feature into a
field-wide topic.

**VI.3 Model half-life**
Kaplan-Meier: median model **137 days** between first and last mention; US frontier
175 days, Chinese labs 85 — flagged as partly a naming artifact of faster version
churn.
- **Investor read:** a defensibility clock. Any thesis that depends on a specific
  model staying relevant has a median of four and a half months.

**VI.4 The MCP curve — a full hype cycle in 24 months**
0 → 23.3 → 3.3 per 10k words, peaking 2025H1, falling 7x even as Claude's own
density doubled. Adoption and discussion decoupled. Presented as the canonical
shape for protocol-layer bets.

---

## Part VII — What we got wrong

*Deliberately its own part, not an appendix. This is the section that makes the
rest credible.*

Three claims built from titles and tags, then refuted against the article bodies:
1. **"OpenAI's coverage declined"** — headline share fell, density did not
2. **"Llama 4 was Meta's inflection"** — the decline began six months earlier;
   Llama 4 was a one-month spike inside an existing slide, and PELT places no
   change point there at all
3. **"The China bloc is second-tier"** — 14 headline days for Alibaba vs Qwen in
   95% of 2026 issues

Plus the one the network refuted: **the "China bloc" is not a community in the
data** — Louvain groups those labs with Google, and surfaces a
serving-infrastructure bloc (Ollama, vLLM, Baseten, OpenRouter, Together) that no
hand-grouping named.

**The general lesson, stated for the investor:** every error came from reading
*editorial framing* as *attention*. Headlines are one story chosen from a crowded
day. Most thematic AI research is built on exactly that signal.

---

## Part VIII — Leading indicators and open questions

**VIII.1 Where the corpus was early**
Coding agents caught ~9 months before dominance; the China substitution ~4
quarters before consensus; MCP's peak dated before its decline was visible.

**VIII.2 What the corpus cannot tell you**
Named limits, with the negative results: no source lead-lag (the three recaps are
lag-0 by construction); no revenue or deployment data; no non-English ecosystem;
robotics and enterprise systematically under-covered.

**VIII.3 The three analyses still open**
CausalImpact (blocked on constructing a defensible control set in a field where
everything co-moves), dynamic topic models, Hawkes processes.

---

## Appendix — Methods

**A.1 Method table** — 12 implemented methods, each with citation, what it
measures, and its known failure mode on this corpus.
**A.2 The unit-of-observation problem** — the report's methodological through-line,
collected: presence saturates, counts track length, titles track framing, KL
tracks format, co-occurrence tracks frequency.
**A.3 Reproducibility** — repo layout, how to regenerate every figure.
**A.4 Extraction caveats** — regex surface matching, unresolved claim subjects,
launch asymmetry, naming artifacts in survival.

---

## Visualisation plan

| # | Figure | Type | Section |
|---|---|---|---|
| 1 | China bloc vs Meta+Mistral crossover | dual line, annotated crossover | II.1 |
| 2 | Per-lab density small multiples | 6-panel sparkline grid | II.1 |
| 3 | Hill-1 effective company count | line + top-3 share bars | II.2 |
| 4 | OpenAI: headline share vs density | dual-axis line, divergence shaded | II.2 |
| 5 | Bradley-Terry incumbency scatter | strength vs comparisons, log-x | II.3 |
| 6 | Domain heatmap | 16 domains × 7 periods | III.1–III.3 |
| 7 | LangChain vs LlamaIndex divergence | two lines against RAG domain area | III.2 |
| 8 | Price: median vs 10th percentile | line pair, divergence shaded | IV.1 |
| 9 | Context window growth | step/log line | IV.2 |
| 10 | Cost-axis trajectories | slope chart, 2024H1 → 2026H1 | V.2 |
| 11 | Semantic drift neighbour table | annotated before/after | V.3 |
| 12 | Burst timeline | Gantt-style bands, regime overlay | VI.2 |
| 13 | Kaplan-Meier survival curves | stepped KM, 3 cohorts | VI.3 |
| 14 | MCP hype curve | single line, annotated peak | VI.4 |

All inline SVG, theme-aware, one accent colour plus a neutral ramp; the format
regimes appear as consistent background bands on every time-series chart so the
reader can always see when a change is instrumental rather than real.

---

## Open decisions for the author

1. **Length** — the outline supports 8–10k words. A tighter 5k "partner memo" cut
   is possible by dropping Parts IV and VIII into the appendix.
2. **Anonymity of the source** — currently named throughout (Latent Space / AI
   News / smol.ai). Worth confirming that attribution is wanted this prominently.
3. **Whether to finish the three open methods first.** CausalImpact in particular
   would materially strengthen Part II.1 by turning "R1 preceded the shift" into an
   effect size. It is the only outstanding item that changes a headline claim.
