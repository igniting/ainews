# Methods: what we were using, and what we should be

## The honest answer

**No, we were not using anything innovative.** Everything in `analysis/` before
this directory is term frequency with normalization:

| Script | Method | Sophistication |
|---|---|---|
| `analyze.py`, `domains.py` | count tags, group by regex | frequency counting |
| `arcs.py` | regex over titles | string matching |
| `density.py` | mentions ÷ words | frequency, normalized |

That is descriptive statistics. It is not news-corpus methodology. There is a
substantial literature on exactly this problem — temporal analysis of document
streams — and we were using none of it.

Two methods from that literature are now implemented here. Both worked. Both
immediately surfaced something more important than the results they produced,
covered in "The blocker" below.

---

## Implemented

### `logodds.py` — Log-odds ratio, informative Dirichlet prior

Monroe, Colaresi & Quinn (2008), *Fightin' Words*. The standard method for
"which words distinguish period A from period B", and a strict improvement on
the frequency differences used everywhere else in this repo.

Raw frequency differences fail two ways: common words dominate the rankings
(a 1pp move on a frequent word beats a 10x move on a rare one), and rare words
are unstable (3 occurrences vs 0 looks like an infinite ratio). Monroe et al.
shrink each word's log-odds toward a corpus-wide prior and divide by its
estimated standard deviation, producing a z-score comparable across frequency
ranges and interpretable at |z| > 1.96.

Result for 2024 vs 2026 — the content signal, once format tokens are filtered:

| Distinctive of 2024 | | Distinctive of 2026 | |
|---|---|---|---|
| llama | z=38.5 | claude | z=−65.9 |
| fine-tuning | z=30.2 | agent | z=−56.7 |
| rag | z=29.0 | opus | z=−56.4 |
| mistral | z=29.0 | qwen | z=−46.8 |
| langchain | z=26.6 | mcp | z=−38.4 |
| llamaindex | z=26.4 | kimi | z=−35.5 |

Same conclusions as the density work, now with confidence intervals rather than
eyeballed gaps. `kimi` at 0 occurrences in 2024 and 2,185 in 2026 is the cleanest
single statistic for the China-bloc finding.

### `novelty.py` — Novelty / Transience / Resonance

Barron, Huang, Spang & DeDeo (PNAS 2018), developed to find which speeches
actually changed the debate in the French National Constituent Assembly.

Each issue becomes an LDA topic distribution. Then:
- **Novelty** — KL divergence from the preceding *w* issues
- **Transience** — KL divergence to the following *w* issues
- **Resonance** = novelty − transience

The distinction matters more than either term. A product launch is high-novelty,
high-transience, zero-resonance: loud, then gone. A real turning point is
high-novelty and *low*-transience — the conversation changed and stayed changed.

**This is the method that should have caught my Llama 4 error.** I picked a
dramatic headline and called it an inflection; the body data showed the decline
had started six months earlier and that day was pure transience. Resonance
separates those automatically. Ranking by novelty finds press releases; ranking
by resonance finds turning points.

---

## The blocker: this corpus has at least three format regimes

Both methods, run naively, ranked **changes in the publishing pipeline** above
every news event in three years. This is the most important thing I learned, and
it constrains everything below.

| Regime change | Evidence | What it did to the analysis |
|---|---|---|
| Issue length expansion, Dec 2023 → Mar 2024 | median 8,040 → 26,850 words | Every one of the top 10 resonance days was in March 2024 |
| Discord sections dropped, Mar 2026 | `AI Discord Recap` in 20/20 Jan, 6/22 Mar, **0/22 Apr onward** | Second spurious cluster, March 2026 |
| Novelty regime shift | mean novelty 2.34 (2024H2) → 0.15 (2025H2), ~15x | Raw resonance is not comparable across eras; unstandardized rankings return only 2024 dates |

Format tokens did the same to log-odds: `div`, `class`, `linksmentioned`,
`commenters` and `description` all outranked real content on the first pass.

Mitigations now in the code: `corpus.py` strips markup and per-era template
wording; `novelty.py` defaults to 2024-04 onward and z-scores against a rolling
local baseline.

**The general lesson:** algorithmic sophistication does not fix confounds, it
finds them faster. A more powerful method applied to this corpus without regime
controls produces more confident wrong answers, not better ones. Format-regime
controls are prerequisite work for everything in the next section — not an
optional refinement.

---

## The menu we are not yet using

### Discovering topics instead of naming them

The deepest limitation of `domains.py` is that **I chose the 16 domains by hand
and wrote regexes for them.** The analysis can only find categories I already
thought of. That is backwards.

- **LDA / NMF** — baseline unsupervised topics. Already used inside `novelty.py`
  as a representation; never used for its own findings.
- **Dynamic Topic Models** (Blei & Lafferty 2006) — topics that *evolve*, so
  "agents" in 2024 and "agents" in 2026 are the same topic with changed content
  rather than two unrelated clusters. Directly suited to this corpus.
- **Structural Topic Model** (Roberts, Stewart & Tingley) — topic prevalence as a
  function of covariates. Here the covariates are free: date, and which of the
  Twitter / Reddit / Discord sections the text came from. That single model would
  answer the source-bias question outright.
- **BERTopic / Top2Vec** — best-in-class, but needs sentence embeddings, and
  `huggingface.co` is blocked in this environment. A locally trained `doc2vec`
  is the available substitute.

### Detecting when things changed

- **Kleinberg burst detection** (2002) — the canonical algorithm for bursts in
  document streams, using an infinite-state automaton rather than a threshold.
  Would date every hype cycle in the corpus objectively.
- **Change point detection** (PELT, Bayesian online) — `ruptures` is installed.
  Would have dated Meta's decline mechanically instead of my picking a headline,
  and would locate the format regimes above so they can be controlled for.

### Semantic change — the one I would most want

**Diachronic word embeddings with Procrustes alignment** (Hamilton, Leskovec &
Jurafsky 2016). Train word2vec on each era separately, align the vector spaces,
and measure how a word's *meaning* moved.

Everything in this repo so far counts whether a word appeared. This asks what it
meant. What were "agents" near in 2024 (chatbots? RAG pipelines?) versus 2026
(harnesses, worktrees, sandboxes)? When did "reasoning" stop meaning
chain-of-thought prompting and start meaning test-time compute?

Crucially this needs **no downloads** — gensim is installed and 15.3M words of
domain text is plenty to train on. A corpus-specific model is *better* here than
a general pretrained one. This is the highest-value unexploited method available.

### Diffusion and causality

- **Hawkes processes** — self-exciting point processes, the standard model for
  news cascades. Fits the "does Discord lead the headlines" question properly,
  rather than by eyeballed correlation.
- **Granger causality / transfer entropy** — lead-lag between the Twitter,
  Reddit and Discord sections, which cover the same day in the same document.

### Structure and lifecycle

- **Co-occurrence networks + Leiden community detection** — find the blocs
  empirically rather than my asserting "the China bloc". Temporal centrality
  would show which entities became brokers between clusters.
- **Survival analysis** — model lifespan as a hazard problem. How long does a
  model stay relevant, and what predicts it? Turns the arcs into estimates rather
  than anecdotes.

---

## Status

| Method | Script | State |
|---|---|---|
| Log-odds, Dirichlet prior | `logodds.py` | done |
| Novelty / transience / resonance | `novelty.py` | done |
| Change point detection (PELT) | `changepoints.py` | done |
| Diachronic embeddings + Procrustes | `semantic_drift.py` | done |
| Unsupervised topics (NMF) | `topics.py` | done |
| Kleinberg burst detection | `bursts.py` | done |
| Granger causality / lead-lag | `leadlag.py` | done (negative result) |
| Co-occurrence networks + Louvain | `network.py` | done |
| Survival analysis (Kaplan-Meier) | `survival.py` | done |
| Bradley-Terry from "beats" claims | `bradley_terry.py` | done |
| Semantic axis projection | `axes.py` | done |
| Numeric claim extraction | `claims.py` | done |
| Rank-turbulence divergence + diversity | `distributions.py` | done |
| CausalImpact / BSTS | — | outstanding |
| Dynamic topic model | — | outstanding |
| Hawkes processes | — | outstanding |

Findings are in [`../DEEPER-FINDINGS.md`](../DEEPER-FINDINGS.md).
What to apply next, ranked, is in [`ROADMAP.md`](ROADMAP.md);
results from those in [`../ROADMAP-FINDINGS.md`](../ROADMAP-FINDINGS.md).

All scoped methods are implemented. Hawkes processes were dropped in favour of
Granger: `leadlag.py` establishes that the three source sections move at lag 0 by
construction, so there is no cascade for a self-exciting model to fit.

## Recommended order

1. **Change point detection** — cheap, `ruptures` is installed, and it does
   double duty: dates the real inflections *and* locates the format regimes that
   every other method needs controlled for. Prerequisite.
2. **Diachronic embeddings** — highest insight per unit effort, no downloads
   needed, and answers a question nothing here has touched: what words *meant*.
3. **Dynamic or structural topic models** — removes my hand-chosen domains, which
   is the biggest remaining bias in the analysis.
4. **Kleinberg bursts + Hawkes** — only after 1, since both are sensitive to the
   regime changes.

All of it is now implemented; see the status table. The recurring lesson across
every method was the same: get the unit of observation right first. Binary
presence saturates, raw counts follow issue length, and titles measure editorial
framing — three different ways to measure the wrong thing confidently.
