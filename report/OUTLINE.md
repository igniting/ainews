# Report outline (v3 — post-audit)

**Working title:** *Announcement Space and Practice Space: A Source-Controlled
Study of 690 Daily AI Newsletters, 2023–2026*

**Format:** single-page HTML typeset as a research paper — numbered sections,
captioned figures and tables, inline citations, monospace identifiers.
~9,000–11,000 words. Self-contained (inline CSS/SVG).

**Audience:** AI engineers. Assumes MoE, RAG, quantization, KV cache, test-time
compute, agent harnesses. Introduces Bradley-Terry, Kaplan-Meier, PELT and
diachronic embeddings where used, at reimplementable depth.

---

## What changed from v2, and why the paper is shaped differently now

v2 was structured as *twelve methods produce findings*. Then reading a stratified
sample of the actual documents invalidated four findings, weakened three, and
exposed a confound that threatened the three largest results at once.

The paper now has **two co-equal contributions**, and pretending otherwise would
misrepresent the work:

1. **Substantive.** A source-controlled measurement of the field's technical
   agenda — whose most novel result, the gap between announcement space and
   practice space, only became visible *because* of the confound.
2. **Methodological.** A corpus where eleven statistical methods could not surface
   artifacts that reading a hundred documents found immediately. Transferable to
   anyone measuring a drifting corpus: evals, monitoring, retrieval, trend tooling.

Every result carries an **evidence tier**:

| Tier | Meaning |
|---|---|
| **A** | Reproduces independently in two source sections |
| **B** | Single method, source- or genre-controlled, confound stated |
| **C** | Measured but confounded; reported as bounded |
| **✗** | Tested and withdrawn |

---

## Abstract (~250 words)

Corpus; the source-composition inversion; the Tier-A results with effect sizes;
the announcement/practice gap; the four withdrawals; the methodological finding.
Stands alone.

## 1. Introduction

**1.1 Motivation.** A fast-moving field's history is normally written backwards,
once the winners are known. This corpus was written forwards, daily, wrong
guesses intact.

**1.2 Research questions.**

| RQ | Question | § |
|---|---|---|
| RQ1 | Does the technical agenda shift survive holding the source surface fixed? | 6.1 |
| RQ2 | Where do announcement space and practice space diverge? | 6.2 |
| RQ3 | Did the open-weights frontier relocate? | 6.3 |
| RQ4 | Do core engineering terms change referent, and does it survive a genre control? | 6.4 |
| RQ5 | How long does a model stay in active discussion? | 6.5 |
| RQ6 | What do the field's own asserted numbers show? | 6.6 |
| RQ7 | Can relative standing be recovered from discourse alone? | 6.7 |
| RQ8 | Which apparent signals are artifacts, and which claims do not survive? | 7 |

**1.3 Contributions.**
- C1. Indexed 690-issue / 15.3M-word corpus with per-issue metadata and extraction code.
- C2. **The announcement/practice gap**, quantified per topic by measuring inside
  parallel Twitter and Reddit recaps of the same day.
- C3. Six source-controlled results reproducing in two independent surfaces.
- C4. Referent drift in core vocabulary, genre-controlled, with the two cases that
  did *not* survive reported alongside the five that did.
- C5. An instrument-artifact catalogue: four publishing regimes, a source-composition
  inversion, title/lede templating, and six ways this corpus yields confident
  false signals.
- C6. A full method audit with four withdrawals.

**1.4 Non-goals.** Not a benchmark study, not market analysis, no claim about
ground-truth capability. Measures *reported* attention.

## 2. Related work

One page: diachronic embeddings (Hamilton 2016); burst and change point detection
(Kleinberg 2002; Killick 2012); novelty/resonance (Barron 2018); distinctive
vocabulary (Monroe 2008); rank divergence (Dodds 2020); paired comparisons
(Bradley & Terry 1952; Hunter 2004). Gap: these are applied to news, politics and
literature, rarely to a technical field's own trade press, and rarely with the
source surface controlled.

---

## 3. The corpus

**3.1** Provenance and reconstruction (two-directory merge required for full text).
**3.2** Descriptive statistics — Table 1.
**3.3** Anatomy of an issue.
**3.4** Embedded structured layers — Table 2: Discord telemetry (31,688
channel-days, 2.15M messages, 56 servers), tweet attribution (18,854 links),
Reddit engagement (3,070), front-matter tags, in-prose numeric claims (2,652).
**3.5 The three editorial layers.** Lede (thesis) / title-slug (event) / body
(recaps). 234 issues carry an "X is all you need" lede — a dated human call, used
in §6.8 as independent validation. *Only layers 2 and 3 were used before reading.*

## 4. The instrument and its artifacts

Promoted ahead of Methods, because every method depends on it.

**4.1 Publishing regimes.** PELT over structural features → four regimes;
460-issue stable core. Figure 1.

**4.2 Source-composition inversion — the central artifact.** Each issue declares
its own sampling effort. Discord 30 → **0** servers; Twitter 384 → 544 accounts;
subreddits 7 → 12. Resulting share of issue words:

| | 2024H1 | 2025H2 | 2026H1 |
|---|---|---|---|
| Twitter | 2% | 5% | **23%** |
| Reddit | 2% | 15% | **61%** |
| Discord | **96%** | 79% | **0%** |

Figure 2. Consequence: whole-issue density conflates topic prevalence with
sampled surface. Everything downstream must be re-derived inside a fixed section.

**4.3 Title and lede templating.** "not much happened today" as title: 0% of 2023
issues → **68%** of 2026, carried by the Opus 5, GPT-5.6, Qwen 3.8 Max and Kimi K3
launches alike. All 23 issues in the final month open "**a quiet day.**"

**4.4 The unit-of-observation table.** Six measures that fail here, each with its
evidence — Table 3.

**4.5 Provenance.** LLM-drafted, human-edited, mix changing over time.

## 5. Methods

**5.1** Method catalogue — Table 4: thirteen methods, each with citation,
estimand, unit of observation, parameters, **and its audited verdict**.
**5.2** The section-controlled density estimator (`sections.py`) — the paper's
primary instrument.
**5.3** Preprocessing, each step justified by the artifact it removed.
**5.4** Reproducibility: seeds, runtimes, one command per figure.

---

## 6. Results

### 6.1 RQ1 — The agenda shift survives source control **[Tier A]**

Density inside the Twitter recap only, per 10⁴ words:

| | 2024H1 | 2025H1 | 2026H2 |
|---|---|---|---|
| `agentic` | 12.7 | 67.4 | 101.6 (peak 138.5, 2026H1) |
| `fine-tuning` | 34.9 | 8.0 | 1.9 |
| `RAG` | 22.5 | 5.6 | 0.2 |
| `reasoning` | 7.0 | **40.2** | 14.3 |

Figure 3, with the Reddit series in parallel. The training-time → inference-time
→ orchestration trajectory holds in both surfaces.

### 6.2 RQ2 — Announcement space vs practice space **[Tier A]** — *lead result*

| Pattern | Twitter | Reddit |
|---|---|---|
| `agentic` | **8.0×** | 2.0× |
| `fine-tuning` | 0.1× (−90%) | 0.4× (−60%) |
| `harness` | 17.9× | 16.8× |
| China bloc | 8.6× | 15.3× |

Two readings the whole-corpus numbers hid:
- **Agents are far more an announcement phenomenon than a practice one** (8× vs 2×).
- **Practitioners kept fine-tuning after the discourse stopped** — Reddit density
  *recovers* in the final period (4.9 → 6.9).

Where the surfaces agree closely (`harness`, China bloc), that is the signature of
a field-wide shift rather than a narrative one. Figure 4. **The paper's most
useful result for a practitioner, and it exists only because the confound forced
the split.**

### 6.3 RQ3 — The open-weights frontier relocated **[Tier A]**

Reproduces independently in both sections. Per-lab trajectories; Kimi/Moonshot
0.1 → 35.9 whole-corpus. Meta's PELT change point at **2024-10**, six months
before Llama 4 — which is *not* a detected change point. Figures 5, 10.

### 6.4 RQ4 — Referent drift, genre-controlled **[Tier B]**

Retrained excluding Discord. Median drift 0.313.

| Term | Drift | 2024H1 | 2026H1 |
|---|---|---|---|
| `skills` | 0.590 | goals, abilities | middleware, reusable, ide, filesystem |
| `distillation` | 0.448 | unet, dare, imagenet | attacks, industrial-scale, copyrighted, laws |
| `harness` | 0.439 | lm-evaluation-harness, eval | orchestration, harnesses, abstraction |
| `agentic` | 0.371 | low-code, devika, production-ready | long-horizon, computer-use, swe |
| `prompt` | 0.363 | engineering, crafting, promptfoo | injection, adherence, caching |

**6.4.1 The two that did not survive**, in the same table style: `context rot`
disappears entirely under the control (a Discord practitioner artifact); `safety`
reinterprets as surveillance/misuse rather than operational security.

**6.4.2 Consequence.** Keyword series spanning these dates aggregate two concepts
— a concrete hazard for eval suites, monitoring and retrieval corpora.

### 6.5 RQ5 — Model half-life **[Tier B]**

Kaplan-Meier, right-censored. Median **137 days**; US frontier 175, Chinese labs
85 (partly a version-naming artifact). Re-checked: no death clustering at the
sampling cutoff. Figure 6.

### 6.6 RQ6 — The numbers the field asserted **[Tier B / C]**

- Context windows: median claimed 24K → **1M** — Figure 7 **[B]**
- Price: median swings $0.42 → $8.00 → $3.00 while the 10th percentile holds
  $0.10–$0.45 **[C — n = 151, thin]**. The median tracks which models were
  newsworthy, not inference cost. Figure 12.
- Benchmark lifecycle: first/last claimed score dates each benchmark's useful life.

### 6.7 RQ7 — Discourse-derived standing **[Tier B]**

801 extracted pairwise claims. **Launch asymmetry measured**: win rate 0.68 at
3–7 comparisons → 0.49 at 41+, ρ = −0.27 with log(comparisons). The fitted
ranking inverts — Claude has the most comparisons (200) and the lowest strength
(0.46). **Reinterpreted**: the estimand is incumbency, not capability. Figure 8.

### 6.8 Independent validation from the editorial lede **[Tier A]**

234 dated "X is all you need" theses against method-derived dates:

| Result | Method date | Lede date |
|---|---|---|
| MCP peak | 2025-03 → 07 (PELT) | **2025-03-26** |
| DeepSeek burst | 2025-W04 (Kleinberg) | **2025-01-27** |
| `harness` drift | 2024H1→2026H1 (embeddings) | **2025-05-15** |
| Reasoning peak | 2025H1 (density) | **2024-09-12** |

The disagreement is the finding: the reasoning thesis was called on o1's launch
day, ~two quarters before density peaked. **Interpretation leads volume**, which
volume-only methods structurally cannot see. Figure 9.

---

## 7. RQ8 — Artifacts, withdrawals and the method audit

Its own section, not an appendix.

**7.1 Withdrawn [✗]**
1. The quiet-day series (5% → 85%) — boilerplate, not a verdict.
2. `context rot` as a corpus-level finding — Discord artifact.
3. "`agentic` sat next to *retrieval-augmented* in 2024" — genre artifact; the
   agents-absorbed-RAG inference loses this support (domain counts still hold).
4. OpenAI's 18% → 4% headline collapse as evidence of fragmentation — title
   templating. Conditioned on descriptive titles it is 29% → 18%.

**7.2 Weakened.** Whole-issue density (superseded); bursts and novelty
(within-regime only); log-odds — its top 2026-distinctive token is **`x.com` at
z = −46.2**, the twitter.com→x.com migration, making it the weakest method here.

**7.3 The open threat [Tier C].** The ~5× fragmentation result is confounded with
sampling breadth (7→12 subreddits, 384→544 accounts). Reported as an upper bound;
the cross-validation with the OpenAI result is correspondingly weaker.

**7.4 Audit table.** All thirteen methods × verdict — Figure 13.

---

## 8. Discussion

**8.1 Read the documents before measuring the fields.** Three rounds of
correction, each from a field measured without being read: titles that became
templates, density normalized by words whose source inverted, and a lede
discarded as boilerplate that turned out to be the corpus's most informative
field. None of eleven methods could surface any of it. Generalises to evals,
monitoring and retrieval over drifting corpora.

**8.2 What the trajectory implies for system design.** Where the scarce resource
moved: model quality → context → orchestration and cost.

**8.3 The announcement/practice gap as a diligence tool.** Two surfaces
disagreeing is a measurable signal that a shift is narrative rather than adopted.

**8.4 Referent drift as a practical hazard.**

**8.5 Why supervised taxonomies under-detect** — the defense-topic miss.

**8.6 Generalisation.** Which findings are about AI and which about this newsletter.

## 9. Threats to validity

Construct (reported attention ≠ activity ≠ deployment); internal (regimes,
composition, templating, LLM-drafted provenance, regex surface matching,
unresolved claim subjects); external (one viewpoint, builder-weighted,
under-covers enterprise/hardware/non-English); statistical (thin end periods,
multiple comparisons, BT identifiability, survival naming artifacts).

## 10. Limitations and future work

Per-section entity extraction to close the fragmentation threat; CausalImpact
(blocked on control-set construction); dynamic topic models; Hawkes;
family-level survival grouping; claim-subject resolution; the untouched
2.15M-message Discord telemetry.

## 11. Conclusion

The Tier-A results; the announcement/practice gap; the four withdrawals; the
methodological finding given equal weight.

## References · Appendices

A. Method parameters and runtimes · B. Extraction patterns verbatim ·
C. Domain composition · D. Corpus reconstruction · E. Reproducibility

---

## Figures

| # | Content | § |
|---|---|---|
| 1 | Publishing regimes (PELT over structural features) | 4.1 |
| 2 | **Source composition + declared sampling effort** | 4.2 |
| 3 | Four themes, Twitter and Reddit in parallel | 6.1 |
| 4 | **Announcement/practice gap — paired bars** | 6.2 |
| 5 | Monthly Llama density with PELT breakpoints | 6.3 |
| 6 | Kaplan-Meier, three cohorts | 6.5 |
| 7 | Claimed context windows (log) | 6.6 |
| 8 | BT strength vs comparison count | 6.7 |
| 9 | **Lede thesis dates vs method dates** | 6.8 |
| 10 | China bloc vs Meta+Mistral, both sections | 6.3 |
| 11 | Neighbour-set evolution, `harness` / `agentic` | 6.4 |
| 12 | Claimed price: median vs 10th percentile | 6.6 |
| 13 | Method audit heatmap (13 methods × verdict) | 7.4 |

Regime bands and the source-composition ribbon appear on every time-series
figure, so instrument boundaries stay visible alongside the data.

---

## Open decisions

1. **Does the fragmentation section stay?** Tier C with a live confound. Cut,
   keep bounded, or do the per-section entity extraction first. I would keep it
   bounded and flagged — it is honest, and the threat is itself instructive.
2. **Length.** ~10k as scoped. The artifact and audit sections are now ~25% of the
   paper, which is the right proportion given what they changed.
3. **Discord telemetry** — 2.15M messages still unanalysed, and now clearly
   valuable as the *practice-space* counterpart to the Twitter/Reddit split. New
   analysis rather than write-up: include, or defer to future work?
