# Report outline (v2 — engineering / scientific)

**Working title:** *Three Years of the Field Talking to Itself: A Quantitative
Study of 690 Daily AI Newsletters, 2023–2026*

**Format:** single-page HTML, typeset as a research paper — numbered sections,
numbered figures and tables with captions, inline citations, footnotes, monospace
for identifiers. ~10,000–12,000 words. Self-contained (inline CSS/SVG).

**Audience:** AI engineers. Assumes fluency in MoE, RAG, quantization, KV cache,
test-time compute, agent harnesses. Does *not* assume familiarity with corpus
linguistics, survival analysis or Bradley-Terry — those are introduced where used,
with enough detail to reimplement.

**Register:** measurement paper. Claims are stated as estimates with samples and
confounds. No prescription, no market commentary. Where the data cannot support a
question, that is reported as a result.

**What makes it worth an engineer's time:**
1. It measures the field's technical agenda instead of asserting it — the
   fine-tuning → RAG → long-context → agents transition gets dates and effect sizes.
2. It shows that several core terms (`harness`, `skills`, `prompt`) changed
   referent mid-corpus, which means naive keyword series over them are measuring
   two different things.
3. Every method is released with its failure mode on this corpus. The
   unit-of-observation problem generalises to anyone building evals, dashboards or
   retrieval over a drifting corpus.

---

## Abstract

~250 words. Corpus, methods, six principal quantitative results with effect sizes,
the three refuted hypotheses, and the methodological finding about instrument
artifacts. Written so it stands alone.

## Keywords

corpus linguistics · diachronic embeddings · technology forecasting · change point
detection · Bradley-Terry · LLM ecosystems

---

## 1. Introduction

**1.1 Motivation.** The history of a fast-moving technical field is normally
written backwards, once the winners are known. This corpus was written forwards,
daily, with the wrong guesses left intact. That makes it usable as a measurement
substrate for questions about the field's own trajectory that retrospective
sources cannot answer.

**1.2 Research questions.** Eight, stated explicitly; Section 5 is organised
around them one-to-one.

| RQ | Question | Section |
|---|---|---|
| RQ1 | How did the technical agenda shift, and when? | 5.1 |
| RQ2 | Did the open-weights frontier relocate, and by how much? | 5.2 |
| RQ3 | How long does a model remain in active discussion? | 5.3 |
| RQ4 | Do technical terms change referent, and can the change be dated? | 5.4 |
| RQ5 | What do the field's own asserted numbers show about cost, context and scale? | 5.5 |
| RQ6 | Can relative capability be recovered from discourse alone? | 5.6 |
| RQ7 | Is technical attention concentrating or fragmenting? | 5.7 |
| RQ8 | Which apparent signals are artifacts of the instrument? | 5.8 |
| RQ9 | Do the results survive holding the source surface fixed, and where do announcement-space and practitioner-space diverge? | 5.9 |

**1.3 Contributions.**
- C1. A cleaned, indexed 690-issue / 15.3M-word corpus with per-issue structured
  metadata, released with extraction code.
- C2. Dated quantification of the fine-tuning → retrieval → long-context → agents
  transition, with effect sizes from three independent measures.
- C3. Evidence of **referent drift** in core engineering vocabulary, with dates —
  and the consequence that keyword time-series over those terms are invalid.
- C4. A discourse-derived incumbency index from 801 extracted pairwise claims, plus
  measurement of the launch-asymmetry bias that makes the naive version wrong.
- C5. Extraction of 2,652 in-prose numeric claims (price, context, parameters,
  benchmark scores) into time series.
- C6. A catalogue of instrument artifacts — four publishing regimes and five
  distinct ways this corpus produces confident false signals.

**1.4 Scope and non-goals.** Not a benchmark study, not a market analysis, not a
claim about ground-truth capability. It measures *reported attention*.

---

## 2. Related work

Short and honest — one page. Positions the study against:
- diachronic word embeddings and semantic change (Hamilton et al. 2016)
- burst and change point detection in document streams (Kleinberg 2002; Killick et al. 2012)
- novelty/resonance in historical corpora (Barron et al. 2018)
- distinctive-vocabulary methods (Monroe et al. 2008); rank divergence (Dodds et al. 2020)
- paired comparison models (Bradley & Terry 1952; Hunter 2004)
- technology hype and diffusion measurement

Explicit gap: these methods are usually applied to news, politics or literature.
Applying them to a *technical field's own trade press* is uncommon, and the
embedded structured layers (community telemetry, attribution links, in-prose
numbers) are unusual.

---

## 3. The corpus

**3.1 Provenance and construction.** Source, the two-directory reconstruction
required for full text, filename and front-matter schema.

**3.2 Descriptive statistics.** Table 1: issues per year, words, cadence, coverage
of calendar days, gaps. Distribution of issue length.

**3.3 Internal structure.** Anatomy of an issue — editorial lede, then parallel
Twitter / Reddit / Discord recaps; Discord split into per-server summaries and
per-channel transcripts.

**3.4 Embedded structured layers.** Table 2, with counts:
- Discord telemetry: 31,688 channel-day records, 2.15M messages, 56 servers
- Tweet attribution: 18,854 (handle, status-ID) links
- Reddit engagement scores: 3,070
- Front-matter tags: companies / models / topics / people, coverage per field
- In-prose numeric claims: 1,335 context, 990 parameter, 176 benchmark, 151 price

**3.5 Publishing regimes.** Figure 1: PELT segmentation of structural features
into four regimes; the 460-issue stable core (2024-05-20 → 2026-03-10). Stated up
front because it constrains every result that follows.

**3.6 Source composition and declared sampling effort.** The single largest
confound in the study, and it is declared in-band: each issue states how many
subreddits, Twitter accounts and Discords it checked. Discord sampling falls 30 →
0 servers while Twitter rises 384 → 544, and the resulting share of issue words
goes from 96% Discord / 2% Twitter (2024H1) to 0% / 23% (2026H1). Figure 1b.
Every whole-issue density series must be re-derived inside a fixed section; §5.9
reports the controlled results.

**3.7 Title and lede templating.** A distinct artifact from the format regimes and
worth its own subsection: both the title field and the opening lede converge on
placeholders ("not much happened today", "**a quiet day.**") independently of
whether anything happened. All 23 issues in the final month carry the placeholder
lede, three of them major launches. Any measure keyed on either field needs
conditioning.

**3.8 The three editorial layers.** Lede (thesis), title/slug (event), body
(source recaps). 234 issues carry an "X is all you need" lede — a dated,
human-authored one-line call used in §5.9 as independent validation.

**3.9 Provenance caveats.** LLM-drafted, human-edited; the mix changes over time.
Coverage bias toward open models, tooling and the sampled Discord ecosystems.

---

## 4. Methods

**4.1 The unit-of-observation problem.** The paper's methodological spine, stated
before any method. Five measures that fail on this corpus and why:

| Measure | Failure | Evidence |
|---|---|---|
| Issue mentions entity (binary) | saturates | 80–97% for most tracked entities |
| Raw mention counts | tracks document length | median issue 28k → 5.8k words |
| Title/headline share | tracks editorial framing **and title templating** | title is a placeholder in 0% of 2023 issues → 68% of 2026 |
| KL over topic distributions | tracks format regimes | top-10 novelty days all in one regime change |
| Raw co-occurrence | tracks marginal frequency | resolved with PPMI |
| **Whole-issue density** | **tracks source composition** | **issue words go 96% Discord → 0%; Twitter 2% → 23%** |

Resolution used throughout: **mentions per 10⁴ words**, ranks, or PPMI, with
regime controls.

**4.2 Method catalogue.** Table 3 — twelve methods, each with: citation, what it
estimates, unit of observation, parameters, and known failure mode here.
Grouped as:
- *Frequency and distinctiveness*: density, log-odds w/ Dirichlet prior, rank-turbulence divergence
- *Temporal structure*: PELT change points, Kleinberg bursts, novelty/transience/resonance
- *Semantics*: diachronic word2vec + Procrustes, semantic axis projection
- *Structure*: NMF topics, PPMI co-occurrence + Louvain
- *Lifecycle and ranking*: Kaplan-Meier, Bradley-Terry (MM)
- *Extraction*: numeric claim patterns, pairwise comparison patterns

**4.3 Preprocessing.** Boilerplate and markup removal; transcript exclusion for
topic models; handle blocklisting; alias folding. Each justified by the artifact
it removed — e.g. NMF returned topics composed of Discord usernames before handle
blocklisting.

**4.4 Reproducibility.** Determinism, seeds, runtimes, dependency set, one command
per figure.

---

## 5. Results

### 5.1 RQ1 — The technical agenda moved from training-time to inference-time to orchestration

The paper's core empirical section. Three independent measures agreeing:

| Theme | 2023H2 | 2025H1 | 2026H2 | Change |
|---|---|---|---|---|
| `agentic` | 7.0 | 30.4 | **52.8** | 7.5× |
| `fine-tuning` | 39.7 | 13.9 | **5.3** | 7.5× ↓ |
| `RAG/retrieval` | 7.6 | 5.3 | **2.0** | 8× ↓ from peak |
| `reasoning` | 3.1 | **21.1** | 11.4 | peak then absorb |

(mentions per 10⁴ words)

- Figure 2: domain heatmap, 16 domains × 7 half-years
- Figure 3: the four theme trajectories with regime bands
- **5.1.1 The absorption pattern.** Reasoning, retrieval and multimodality all
  peak then decline while remaining ubiquitous in prose. Distinguishing *absorbed*
  from *abandoned* requires the peak: capabilities that won peak first, then fade
  as they become substrate. Robotics never exceeds 12% — the shape of a
  non-arrival.
- **5.1.2 Vendor survival is not category survival.** RAG as a domain falls
  31%→4%, but LangChain reaches its maximum coverage (24% of issues, 2026H1) while
  LlamaIndex falls to 2%. Figure 4.
- **5.1.3 An unanticipated category.** Unsupervised NMF surfaces a
  defense/national-security topic rising 0.6% → 8.0%, absent from a hand-built
  16-domain taxonomy — a demonstration that supervised category schemes cannot
  find what they did not anticipate.

### 5.2 RQ2 — The open-weights frontier relocated, and it is the largest measured movement

- Figure 5: China bloc (DeepSeek+Qwen+Kimi+GLM+MiniMax) vs Meta+Mistral density;
  1.3 vs 94.8 inverting to 89.2 vs 2.1 per 10⁴ words; crossover in 2025H1
- Table: per-lab trajectories; Kimi/Moonshot 0.1 → 35.9 (steepest in the corpus)
- 5.2.1 Meta's decline dated by PELT to **2024-10**, six months before Llama 4;
  Llama 4 produces a one-month spike inside an existing decline and is *not* a
  detected change point (Figure 6)
- 5.2.2 Log-odds significance: `kimi` at 0 occurrences (2024) vs 2,185 (2026)

### 5.3 RQ3 — Median model half-life is 137 days

Kaplan-Meier with right-censoring; why censoring is required (recent models have
unfinished lives, and naive averaging biases against exactly the newest cohort).

| Cohort | n | Died | Median lifespan |
|---|---|---|---|
| All models | 255 | 217 | **137 d** |
| US frontier | 161 | 141 | 175 d |
| Chinese labs | 49 | 40 | 85 d |

- Figure 7: KM curves
- 5.3.1 The cohort gap is partly a naming artifact — faster version churn splits a
  persistent family into short-lived tags. Family-level grouping is future work.
- **Engineering consequence**, stated plainly: any system pinned to a specific
  model checkpoint faces a median four-and-a-half-month relevance window in the
  field's discussion, which bounds how long integration-specific tuning holds value.

### 5.4 RQ4 — Core engineering terms changed referent, and the change is dateable

Highest-novelty section. Diachronic word2vec + Procrustes; median drift across
3,455 shared terms = 0.365 defines the null.

| Term | Drift | 2024H1 neighbours | 2026H1 neighbours | Referent change |
|---|---|---|---|---|
| `harness` | 0.568 | lm-evaluation-harness, eval, lm-eval | harnesses, orchestration, primitives | eval harness → agent harness |
| `skills` | 0.524 | skill, expertise, proficiency | skill.md, reusable, primitives | capability → file format |
| `agentic` | 0.375 | retrieval-augmented, production-ready | long-horizon, computer-use, swe | RAG pipeline → autonomous loop |
| `prompt` | 0.266 | engineering, meta-prompting | injection, jailbreaks | craft → attack surface |
| `distillation` | 0.514 | masked, unsupervised, contrastive | attacks, persona | technique → accusation |
| `safety` | 0.340 | regulation, sb, california, bill | safeguards, cyber, resistance | legislation → operational security |
| `context` | 0.269 | window, length | window, length, **rot**, kv | new failure mode named |

- Figure 8: neighbour-set evolution for `harness` and `agentic` across five eras
- 5.4.1 Highest drift in corpus: `r1` (0.921), from the Rabbit device to DeepSeek
- 5.4.2 `stability` decays from a company name back to a common noun
- **5.4.3 Consequence for measurement.** Any keyword time series over these terms
  aggregates two different concepts. This is a concrete failure mode for
  dashboards, trend tooling and retrieval corpora that span the drift date.

### 5.5 RQ5 — What the field asserted about cost, context and scale

- 5.5.1 **The cheap frontier is flat.** Median claimed $/1M tokens swings
  $0.42 → $8.00 → $3.00 while the 10th percentile holds at $0.10–$0.45 throughout
  (Figure 9). The median tracks *which models were newsworthy* — the 2025H1 spike
  coincides with the o1/o3/R1 period — not the cost of inference.
- 5.5.2 **Context windows 40×**: median claimed 24K → 1M (Figure 10), with the
  vocabulary consequence in 5.4 (`context rot`).
- 5.5.3 Parameter-count distributions and the shift toward active-parameter and
  cost-per-task framing.
- 5.5.4 **Benchmark lifecycle.** First/last claimed score per benchmark dates its
  useful life; benchmarks stop being cited when saturated. Table.
- Caveat: claim subjects are unresolved, so these are field-level distributions,
  not per-model results.

### 5.6 RQ6 — Relative capability from discourse alone: partially, once bias is removed

- 5.6.1 Extraction: 801 dated pairwise claims over a 95-family lexicon
- 5.6.2 **Launch asymmetry, measured**: mean win rate 0.68 at 3–7 comparisons →
  0.49 at 41+; correlation with log(comparisons) −0.27. A model is claimant at
  launch and incumbent only later. Table + Figure 11.
- 5.6.3 The fitted ranking, and why it inverts: most-compared families score
  lowest. Claude has the most comparisons in the corpus (200) and the lowest
  strength (0.46).
- 5.6.4 **Reinterpretation.** The estimand is not capability but *incumbency* —
  the degree to which a model serves as the field's reference point. Stated as a
  reinterpretation of a failed measurement, not a success.

### 5.7 RQ7 — Attention fragmented roughly fivefold

| Period | Distinct | Hill-1 (effective) | Gini | Top-3 share |
|---|---|---|---|---|
| 2023H2 | 34 | 21.7 | 0.48 | 36% |
| 2025H2 | 247 | **101.8** | 0.61 | 19% |
| 2026H1 | 207 | 88.1 | 0.59 | 22% |

Hill numbers introduced properly (effective count interpretation). Figure 12.
Cross-validates the OpenAI result in 5.8: fragmentation, not decline.

### 5.8 RQ8 — Instrument artifacts, and three refuted hypotheses

Full section, not a footnote.
- 5.8.1 **"OpenAI's coverage declined."** Refuted twice. Headline share fell
  18%→4% while density held flat (59.1→51.1, Figure 13). The first correction
  attributed the gap to fragmentation; reading the recent issues showed the
  dominant cause is simpler — **the title field became a template**. "not much
  happened today" is 0% of 2023 titles and 68% of 2026, and it is carried by the
  Opus 5, GPT-5.6 and Kimi K3 launch issues alike. Conditioned on descriptive
  titles, OpenAI runs 29%→18%, Anthropic rises to 29% and the China bloc to 24%.
  A worked example of an artifact surviving one round of correction.
- 5.8.2 **"Llama 4 was the inflection."** Refuted: PELT places no change point
  there; decline began 2024-10.
- 5.8.3 **"The Chinese labs are a second tier."** Refuted: 14 headline days for
  Alibaba against Qwen appearing in 95% of 2026 issues.
- 5.8.4 **The asserted "China bloc" is not a community in the data.** Louvain
  groups those labs with Google and surfaces an unnamed serving-infrastructure
  community (Ollama, vLLM, Baseten, OpenRouter, Together). Figure 14.
- 5.8.5 **A question the corpus cannot answer.** Source lead-lag: 33 significant
  Granger relations, all at median lag 0, because the three recaps are written from
  the same issue on the same day. Reported as a negative result.

---

### 5.9 RQ9 — Source-controlled results, and the announcement/practice gap

The validation section, and the strongest part of the study.

- 5.9.1 **The control.** Density recomputed inside the Twitter and Reddit recaps
  separately, holding the sampled surface fixed. All six headline results survive;
  the China rise and Meta/Mistral fall reproduce in *both* sections independently,
  making them the most robust findings in the paper.
- 5.9.2 **The announcement/practice gap.** Where the two surfaces disagree, the
  gap is the result: `agentic` rises 8.0× on Twitter but 2.0× on Reddit;
  `fine-tuning` falls 90% on Twitter but 60% on Reddit and *recovers* in Reddit's
  final period. Practitioners kept fine-tuning after it stopped being news.
  Table + Figure 15.
- 5.9.3 **Independent validation from the editorial lede.** 234 dated "X is all
  you need" theses checked against the automated dates: MCP peak 2025-03 (PELT) vs
  lede 2025-03-26; DeepSeek burst 2025-W04 (Kleinberg) vs lede 2025-01-27;
  `harness` drift vs lede 2025-05-15. The one disagreement is informative — the
  reasoning thesis was called 2024-09-12, roughly two quarters before density
  peaked, so interpretation leads volume in a way volume-only methods cannot see.

---

## 6. Discussion

**6.1 What the trajectory implies about system design.** The measured sequence —
fine-tuning collapsing, retrieval absorbed by long context and then by tool calls,
orchestration becoming dominant — is an architectural argument with dates attached.
Where the scarce resource moved: from model quality, to context, to orchestration
and cost.

**6.2 Read the documents before measuring the fields.** Three rounds of
correction in this study, each from a field measured without being read: titles
that became templates, density normalized by words whose source inverted, and a
lede discarded as boilerplate that turned out to be the most informative field in
the corpus. None of eleven statistical methods could surface any of it.

**6.3 Referent drift as a practical hazard.** Concrete implications for eval
suites, keyword monitoring and retrieval corpora spanning a drift boundary.

**6.4 Incumbency as an observable.** What "being the reference model" looks like
in text, and why it is measurable independently of benchmarks.

**6.5 Why supervised taxonomies under-detect.** The defense-topic miss as a
generalisable warning for anyone maintaining a category scheme over a moving field.

**6.6 Generalisation.** Which findings are about AI and which are about this
newsletter. Stated conservatively.

---

## 7. Threats to validity

- **Construct.** Reported attention ≠ field activity ≠ deployment.
- **Internal.** Four format regimes; LLM-drafted, human-edited provenance with a
  changing mix; regex surface matching; unresolved claim subjects.
- **External.** One editorial viewpoint; builder- and tooling-weighted;
  under-covers enterprise, hardware supply chains, non-English ecosystems.
- **Statistical.** Thin end periods (2023H2, 2026H2); multiple comparisons across
  entities; survival naming artifacts; BT identifiability restricted to the
  largest connected component.

---

## 8. Limitations and future work

The three unimplemented methods and what each would add: CausalImpact (blocked on
constructing a defensible control set where all series co-move), dynamic topic
models, Hawkes processes. Plus: family-level survival grouping, claim-subject
resolution, and the untouched 2.15M-message Discord telemetry.

## 9. Conclusion

Six results restated with effect sizes; the methodological finding given equal
weight.

---

## References

~15 entries, formal citation style.

## Appendices

- **A.** Method parameters and runtimes
- **B.** Extraction patterns (comparative verbs, numeric claim regexes) verbatim
- **C.** Full domain composition — the raw tags matched into each of 16 domains
- **D.** Corpus reconstruction procedure and schema
- **E.** Reproducibility: repo layout, commands per figure

---

## Figures and tables

| # | Content | Type | §|
|---|---|---|---|
| Fig 1 | Publishing regimes from PELT over structural features | segmented timeline | 3.5 |
| Fig 2 | Domain heatmap, 16 × 7 | heatmap | 5.1 |
| Fig 3 | Four theme trajectories with regime bands | multi-line | 5.1 |
| Fig 4 | LangChain vs LlamaIndex against RAG domain | line + area | 5.1.2 |
| Fig 5 | China bloc vs Meta+Mistral crossover | dual line, annotated | 5.2 |
| Fig 6 | Monthly Llama density with PELT breakpoints | bar + markers | 5.2.1 |
| Fig 7 | Kaplan-Meier survival, three cohorts | stepped KM | 5.3 |
| Fig 8 | Neighbour-set evolution, `harness` / `agentic` | annotated small-multiple | 5.4 |
| Fig 9 | Claimed price: median vs 10th percentile | line pair, shaded gap | 5.5.1 |
| Fig 10 | Claimed context windows | log step | 5.5.2 |
| Fig 11 | BT strength vs comparison count | scatter, log-x | 5.6.2 |
| Fig 12 | Hill-1 and top-3 share | line + bars | 5.7 |
| Fig 13 | OpenAI headline share vs density | dual axis, shaded divergence | 5.8.1 |
| Fig 14 | Co-occurrence network, 2026H1, Louvain communities | force layout | 5.8.4 |
| Fig 1b | Source composition of issue words + declared sampling effort | stacked area + line | 3.6 |
| Fig 15 | Twitter vs Reddit density for six patterns | paired small-multiple | 5.9.2 |
| Fig 16 | Lede thesis dates against method-derived dates | dumbbell/timeline | 5.9.3 |
| Tab 1–3 | Corpus statistics · embedded layers · method catalogue | tables | 3, 4 |

Format regimes appear as consistent background bands on every time-series figure,
so instrument boundaries are always visible alongside the data.

---

## Open decisions

1. **Depth of the methods section.** Full reimplementable detail (adds ~1,500
   words) versus catalogue-plus-appendix. Default: full detail, since the
   unit-of-observation material is a genuine contribution.
2. **Discord telemetry.** 2.15M messages of behavioural data remain unanalysed. It
   is the largest untouched asset and could carry its own results subsection —
   but it is new analysis, not write-up.
3. **Whether §5.6 stays.** The Bradley-Terry result is a reinterpreted failure. It
   is honest and interesting; it is also the weakest section. Keep, shorten, or
   move to an appendix.
