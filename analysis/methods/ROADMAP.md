# Method roadmap: what to apply next, in priority order

Seven methods are implemented (see `README.md`). This is the ranked list of what
to do next, chosen against what the corpus has actually turned out to contain
rather than from a general menu.

## What the corpus is, now that we know

Ranking is driven by these structural facts, established over the previous
passes:

| Property | Detail | Why it matters for method choice |
|---|---|---|
| Dated pairwise claims | "Mixtral beats GPT3.5", "matches DeepSeek R1", "beating Claude 4 Sonnet at 11% of its cost" — everywhere | Enables tournament-ranking methods almost nothing else has the data for |
| Numeric claims in prose | 527 `X% on BENCHMARK`, 279 `$/token`, 2,033 context-window | Supports real price/performance curves |
| Trained per-era embeddings | 5 word2vec models, aligned, 3,455 shared words | Axis projection is nearly free |
| Format regimes | 4, with 2024-05-20 → 2026-03-10 the 460-issue core | Every method needs this controlled |
| Parallel source sections | Twitter/Reddit/Discord, same day | **Lag-0 by construction** — kills cascade methods |
| Entity lifespans | 255 models, median 137 days | Supports diffusion and survival extensions |
| Discord telemetry | 31,688 channel-days, 2.1M messages, 56 servers | Behavioural series, still barely used |
| Unit-of-observation trap | presence saturates; counts track length | Density or rank, never raw presence |

---

## Tier 1 — highest value, and specific to this corpus

### 1. Bradley-Terry over extracted "beats" claims

**The single best idea available.** The archive is saturated with dated pairwise
comparative claims. Extract `(winner, loser, date)` triples from comparative
constructions and fit a [Bradley-Terry model](https://arxiv.org/html/2601.14727v1)
for latent capability — then the
[dynamic / time-varying variant](https://arxiv.org/pdf/2003.00083) for how the
implied ranking moved week by week.

What it produces: **a capability leaderboard derived purely from what the
discourse asserted**, with dates. Then compare it against real benchmark
leaderboards. Where they diverge, you have measured the field being collectively
early, late, or wrong — which is the question `IDEAS.md` posed as "consensus
reversals" and never answered.

Cheap: extraction is pattern-based over a closed vocabulary of comparative verbs,
and the MM algorithm for Bradley-Terry is about thirty lines. Nothing else in the
roadmap has this ratio of novelty to effort.

### 2. Semantic axis projection on the embeddings already trained

`semantic_drift.py` produced five aligned era models and used them only for a
scalar drift score. Define interpretable axes as differences between pole-word
centroids — cheap↔expensive, open↔closed, research↔product, capable↔safe — and
project every entity onto them per era.

That turns "this word moved 0.52" into "Qwen moved from the cheap end toward the
frontier end between 2025H1 and 2026H1", which is an interpretable coordinate
system rather than a distance. Pair with **WEAT** (word-embedding association
tests) for significance rather than eyeballed positions.

Nearly free — the models exist and the alignment is done.

### 3. Numeric claim extraction → price/performance frontier

Normalize the in-prose numbers into `(model, metric, value, date)` and build the
cost-per-capability curve **as claimed at the time**. The corpus's own repeated
framing is price ("8% of Claude Sonnet's price", "11% of its cost", "10x cheaper"),
so this measures the thing the field itself said mattered.

Checkable against what actually happened, which makes it one of the few outputs
here that can be validated externally.

---

## Tier 2 — strong, standard, and not yet used

### 4. CausalImpact / Bayesian structural time series

[Brodersen et al.](https://research.google/pubs/inferring-causal-impact-using-bayesian-structural-time-series-models/)
builds a synthetic control from correlated untreated series and estimates the
counterfactual. Applied here: what did R1 (2025-01-21) *cause* in NVIDIA's
coverage? What did GPT-5 cause in Claude's?

This replaces assertions I made with estimates. **The catch is real and must be
stated**: the method assumes controls were unaffected by the intervention, and in
a field this coupled, genuinely unaffected series are scarce. Candidate controls
would have to come from unrelated domains (video tooling, robotics) and be
justified explicitly.

### 5. Rank-turbulence divergence (allotaxonometry)

[Dodds et al. 2020](https://arxiv.org/abs/2002.09770), with a
[reference implementation](https://github.com/jkbren/rank-turbulence-divergence).
A rank-based instrument for comparing two ranked lists, tunable by α to weight
head versus tail.

It complements `logodds.py` rather than duplicating it. Log-odds is
frequency-based and needs a prior to handle zeros; RTD is rank-based and handles
"present in one list only" natively — which is exactly the `kimi: 0 → 2,185`
case, the cleanest statistic in the whole analysis and the one log-odds handles
least gracefully.

### 6. Attention concentration: entropy, Hill numbers, Gini

Promised in `IDEAS.md`, never delivered. Is AI news consolidating onto fewer
players or fragmenting? Shannon entropy and Gini over the entity distribution per
period answer it directly.

Worth doing properly with **ecological diversity metrics** — richness, evenness,
Hill numbers, beta-diversity between periods. Treating entities as species is a
legitimate and underused framing, and it gives a principled answer to "did the
field get more crowded" that the top-line shares cannot.

### 7. A real dynamic topic model

`topics.py` fits NMF per corpus and slices afterwards, so topics are not linked
across time. [Dynamic Topic Models](https://www.emergentmind.com/topics/dynamic-topic-model-dtm)
(gensim's `LdaSeqModel`) chain topics through a state-space model, and
**Dynamic Embedded Topic Models** (D-ETM) fit trajectories of topic embeddings
with a random walk for better coherence on emergent topics.

This matters for a claim I already made: that reasoning and retrieval were
*absorbed* rather than abandoned. A chained topic model can show a topic's
vocabulary turning over while the topic persists — which is what absorption
actually means, and which per-period NMF cannot represent.

### 8. Hawkes processes on entity mentions

I dropped Hawkes after `leadlag.py` showed the source sections move at lag 0.
That was right for *sections* and wrong as a general dismissal. Self-excitation
within a single entity's mention stream is a different question: does coverage of
X beget more coverage of X, and with what decay?

The **branching ratio** is an interpretable per-entity "virality", and the
cross-excitation matrix gives an empirical contagion structure between entities —
a better-founded version of the co-occurrence network.

---

## Tier 3 — valuable, heavier

9. **Targeted / aspect-based sentiment and stance.** The missing ingredient for
   consensus reversals: polarity *toward an entity*, not of a document. Offline
   lexicon methods are feasible; the hard part is target attribution in dense
   comparative prose.
10. **Temporal community tracking** — birth, death, merge and split of network
    communities (Greene, Doyle & Cunningham) instead of `network.py`'s
    independent per-era snapshots. Would date when the blocs reorganized.
11. **Open IE → temporal knowledge graph.** Subject-relation-object triples with
    dates; the substrate for storyline construction and claim verification.
12. **Storyline / event-chain construction.** Cluster mentions into narrative
    chains so "the R1 story" becomes an object with a start, participants and an
    end, rather than a density curve.
13. **Term birth and adoption curves.** Fit logistic/Bass diffusion to
    first-appearance→saturation. `MCP`, `context rot`, `skill.md` and `harness`
    all have clean adoption curves and known birth dates.
14. **Graph embeddings (node2vec) aligned over time** — entity trajectories in
    relational space, the network counterpart to word-level drift.

---

## Tier 4 — deprioritized, with reasons

| Method | Why not |
|---|---|
| BERTopic / Top2Vec | Needs sentence-transformer downloads; `huggingface.co` is blocked. Locally trained doc2vec is the substitute. |
| Transfer entropy | Granger already returned lag-0 across all pairs; nonlinearity is unlikely to rescue a structural artifact. |
| Wavelet coherence | Same limitation — the lag-0 finding caps what any cross-source timing method can add. |
| SIR / epidemic models | Term-adoption S-curves (13) capture most of the value far more simply. |
| LLM-as-judge extraction at corpus scale | 15.3M words. Viable for targeted subsets, not as a default. |

---

## The constraint that applies to all of it

Every method tried so far failed first on the **unit of observation**, not on the
algorithm:

- binary presence saturates at 80–97%
- raw counts track issue length, which fell 5x
- titles measure editorial framing, not attention
- KL on topic distributions tracks format regimes before news
- co-occurrence counts rediscover whoever is most frequent

Each was fixed by changing the unit — to density, to rank, to PPMI, to a
locally-standardized score. **Nothing on this roadmap should be started before
deciding what its unit of observation is and what would saturate or confound
it.** That decision has mattered more than the choice of algorithm every single
time.

## Sources

- [Recent advances in the Bradley–Terry Model](https://arxiv.org/html/2601.14727v1)
- [Nonparametric Estimation in the Dynamic Bradley-Terry Model](https://arxiv.org/pdf/2003.00083)
- [Allotaxonometry and rank-turbulence divergence](https://arxiv.org/abs/2002.09770)
  ([implementation](https://github.com/jkbren/rank-turbulence-divergence))
- [Inferring causal impact using Bayesian structural time-series models](https://research.google/pubs/inferring-causal-impact-using-bayesian-structural-time-series-models/)
  ([CausalImpact](https://google.github.io/CausalImpact/CausalImpact.html))
- [Dynamic Topic Model overview](https://www.emergentmind.com/topics/dynamic-topic-model-dtm)
- [Event-based news embedding: leveraging entities, themes, and historical context](https://link.springer.com/article/10.1007/s00521-026-12021-2)
- [Temporal analysis of topic modeling output by machine learning techniques](https://link.springer.com/article/10.1007/s41060-024-00583-0)
