# Findings from the corpus-analysis methods

Results from `analysis/methods/`: change point detection, diachronic word
embeddings, and unsupervised topic discovery. These read the article bodies, and
they answer questions the counting methods structurally could not.

---

## 1. Change points: dating shifts mechanically

`changepoints.py`, PELT (Killick, Fearnhead & Eckley 2012).

### The format regimes, found without being told to look

Run over structural features only — length, which recap sections exist, link and
heading density — PELT recovered four publishing regimes:

| Regime | From | To | Issues |
|---|---|---|---|
| 1 | 2023-12-06 | 2024-03-11 | 75 |
| 2 | 2024-03-12 | 2024-05-17 | 50 |
| 3 | **2024-05-20** | **2026-03-10** | **460** |
| 4 | 2026-03-11 | 2026-08-06 | 105 |

Regime 3 is the comparable core: 460 issues, two years, one stable format. Any
cross-era claim should either live inside it or control for the boundaries.

### Meta: the mechanical verdict

I claimed Llama 4 (2025-04-08) was Meta's inflection. `VERIFICATION.md` corrected
that by eye. PELT settles it:

| Segment | Mean density (per 10k words) | Change |
|---|---|---|
| 2023-12 → 2024-04 | 8.3 | — |
| 2024-05 → 2024-09 | 20.2 | +143% |
| **2024-10 → 2025-02** | **8.9** | **−56%** |
| 2025-03 → 2025-07 | 6.5 | −27% |
| **2025-08 → 2026-08** | **1.2** | **−81%** |

The structural breaks are **2024-10** and **2025-08**. April 2025 falls *inside* a
segment — Llama 4 is not a change point at all. The decline began six months
before it and the collapse came four months after.

### Other arcs, dated

- **MCP** — 0 → 5.9 → **22.4** (2025-03→07) → 10.8 → 4.8. A clean rise-and-fall
  with the peak dated to a five-month window.
- **GPT/OpenAI** — 37.0, 35.0, 28.1, 31.6, 43.5, 31.5, 36.2. Oscillation around a
  flat level, no trend. Independent confirmation that OpenAI's coverage never
  declined.
- **Claude** — 6.7 → 11.3 → 17.6 → 13.4 → **34.7** (2026-01 on). Still rising.
- **Qwen** — 1.3 → 6.0 → 7.8 → 15.2 → **23.3**. Five segments, every one higher.

---

## 2. Semantic drift: what words *meant*

`semantic_drift.py`, diachronic word2vec with orthogonal Procrustes alignment
(Hamilton, Leskovec & Jurafsky 2016). One model per half-year, trained on this
corpus — 15.3M words of domain text beats a general pretrained model for this
vocabulary, and needs no downloads.

**This is the method that found things nothing else could.** Every other approach
counts whether a word appeared. Words whose *frequency* barely moved turn out to
have changed meaning completely.

Median drift across 3,455 shared words is 0.365 — the "did not really move" line.

### The clearest case: `harness` (drift 0.568)

| Era | Nearest neighbours |
|---|---|
| 2024H1 | lm-evaluation-harness, eval, lm-eval-harness, lm-eval, evaluation |
| 2026H1 | harnesses, orchestration, primitives, ux, hwchase17 |

The word changed referent entirely: an **evaluation** harness in 2024, an **agent**
harness in 2026. Frequency analysis sees one word used throughout and reports
continuity. It is two different concepts.

### `agentic` (0.375) — and what it says about the retrieval story

| Era | Nearest neighbours |
|---|---|
| 2024H1 | retrieval-augmented, production-ready, multi-agent, jerryjliu0 |
| 2026H1 | long-horizon, multi-step, computer-use, swe, long-running |

In 2024 "agentic" sat next to *retrieval-augmented* and the LlamaIndex founder's
handle. By 2026 it sits next to long-horizon autonomous work. This is direct
semantic evidence for the claim that agents absorbed retrieval — not inferred
from two counts moving in opposite directions, but visible in the word's company.

### Others worth reading

| Word | Drift | 2024H1 | 2026H1 | Reading |
|---|---|---|---|---|
| `skills` | 0.524 | skill, knowledge, expertise, proficiency | skill.md, harnesses, reusable, primitives | Abstract noun → **file format** |
| `distillation` | 0.514 | masked, unsupervised, contrastive, svd | attacks, persona, distill | Training technique → **accusation** |
| `prompt` | 0.266 | engineering, meta-prompting, prompting | injection, jailbreaks, fortress | Craft → **attack surface** |
| `safety` | 0.340 | regulation, risk, sb, california, bill | safeguards, cyber, resistance | Legislation → **operational security** |
| `open` | 0.337 | source, oss, sourcing | open-weight, **closed**, **proprietary** | Now used contrastively |
| `context` | 0.269 | window, length, contexts | window, length, **rot**, kv | "Context rot" is new vocabulary |

`safety` independently confirms the U-shape noted in `NEWS-ANALYSIS.md`: it left
as legislation (SB-1047, California) and came back as agent security.

### The unsupervised top movers

Ranked over all shared vocabulary, no watch list:

- **`r1`** (0.921, highest in the corpus) — 2024H1 neighbours: `rabbit, shipping,
  purchase, o1`. 2026H1: `mimo, v3.2, nemotron, stepfun`. The token meant the
  **Rabbit R1 gadget** and now means **DeepSeek R1**. A name collision resolved by
  history, and the single largest semantic move in three years.
- **`stability`** (0.715) — `emad, stability.ai, stableai` → `reliability,
  robustness, instability, oom`. A company name decayed back into a common noun.
  Stability AI's disappearance is legible in the geometry.
- **`effort`** (0.682) — `efforts, initiative, contributions` → `xhigh, medium,
  levels, depth, thinking`. A generic noun became an **API parameter**
  (`reasoning_effort`).

*Caveat:* the unsupervised ranking also surfaces polysemy and residual format
noise (`description`, `class`, `activity`). The watch list is the more reliable
read; the top-movers list needs eyes on each entry.

---

## 3. Topics the corpus chose for itself

`topics.py`, NMF over TF-IDF. `domains.py` could only find categories I thought
of in advance. This one proposes its own.

Two preprocessing lessons, both learned the hard way: the first run returned
topics made of **Discord usernames** (`solbus`, `noobmaster29`,
`poltronsuperstar`) — NMF was clustering on *who was talking*, not what about.
Dropping the Discord recap and blocklisting handles from the front-matter
`people` tags fixed it.

### The category I missed entirely

| Topic | 2023H2 | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 | 2026H2 |
|---|---|---|---|---|---|---|---|
| pentagon, military, dod, defense, surveillance, weapons, government | 0.2 | 0.6 | 1.5 | 1.1 | 1.2 | **8.0** | 3.5 |

A **defense and national-security topic**, near-absent until 2025 and then a 7x
jump in 2026H1. My 16 hand-chosen domains had "Policy & business" and nothing
that would have separated this out. It is exactly the failure mode I flagged:
the taxonomy could not find what it did not anticipate.

### Other topics no hand-built taxonomy would produce

- **`humanoid, robot, robots, robotics, suicide, hospital, crises, mental`**
  (peak 2025H2, 9.9%) — robotics and AI-mental-health coverage fused into one
  cluster because they co-occur in the same issues. Analytically messy, but it is
  a real property of the corpus my taxonomy would have split apart and hidden.
- **`wan, i2v, wan2, video, ltx, workflow, comfyui, realism, animation`**
  (peak 2025H1) — the open video-generation *tooling* stack, distinct from the
  Sora/Veo topic (13). My single "Video" domain merged two different worlds.
- **`xlam, phi, minference, salesforce, 1b, rubra, function, calling`**
  (peak 2024H2, 16.8%) — the small-model / function-calling era, which peaked and
  vanished. It has no counterpart in my domain list at all.

---

---

## 4. Bursts: dating the spikes without a threshold

`bursts.py`, Kleinberg (2002) two-state automaton.

Getting the units right took three attempts, and the failures are the reusable
lesson. Issues-mentioning-X **saturates** — most tracked entities appear in 80-97%
of issues, so the algorithm returned 118-week "bursts". Kilowords-as-trials made
mentions exceed trials for frequently-named entities, clamping the rate to 1.
Only words-as-trials with mentions-as-successes gives a valid Poisson intensity.

With that fixed the bursts land where they should:

| Entity | Burst | Rate vs baseline | What it is |
|---|---|---|---|
| Mistral | 2023-W49 → 2024-W13 | 42.9 vs 9.5 (4.5x) | The Mixtral rush |
| Meta Llama | 2024-W16 → 2024-W22 | 28.8 vs 9.1 (3.2x) | Llama 3 |
| DeepSeek | 2025-W04 → 2025-W10 | 45.8 vs 9.8 (**4.7x**) | R1 |
| reasoning | 2025-W04 → 2025-W11 | 27.5 vs 11.5 (2.4x) | fires in the *same weeks* as R1 |
| GPT/OpenAI | 2025-W32 → 2025-W33 | 115.1 vs 34.0 (3.4x) | GPT-5 |
| Kimi/Moonshot | 2026-W29 → 2026-W32 | 39.0 vs 4.4 (**8.9x**) | largest relative burst in the corpus |

The `reasoning` burst coinciding exactly with the DeepSeek R1 burst is the
cleanest evidence in the corpus that R1 was what made reasoning a general topic
rather than an OpenAI product feature.

---

## 5. Lead-lag between sources: a negative result

`leadlag.py`, cross-correlation plus Granger causality over the parallel
Twitter / Reddit / Discord recaps, restricted to the 2024-05 → 2026-03 regime
where all three exist.

33 significant Granger relationships, and the **median best lag is +0 for every
pair**. The sources move together, not in sequence.

| Direction | Entities significant at p<0.05 | Median lag |
|---|---|---|
| discord → twitter | 14 | +0 |
| discord → reddit | 12 | +0 |
| reddit → twitter | 7 | +0 |

This is a real answer, and it is mostly a limit on the question. The three recaps
are written **from the same issue on the same day**, so a same-day story appears
in all three at lag 0 by construction. What this can detect is only a source
dwelling on something for days longer than the others — not who published first
in the world. `IDEAS.md` proposed this as a way to find which surface breaks
stories; the corpus cannot answer that, and it is better to say so than to report
the lag-0 correlations as if they meant sequence.

The one exception worth noting: Meta Llama shows discord → twitter at **lag +2**
with r=0.51, the only entity with a consistent multi-issue lead. Local-model
communities discussed Llama releases before the Twitter recap caught up — which
fits Llama's distinctive position as the model people actually ran themselves.

---

## 6. Networks: the blocs I asserted are not the blocs in the data

`network.py`, PPMI-weighted co-occurrence with Louvain community detection.
Edges are PPMI rather than raw co-occurrence because raw counts merely rediscover
the most-mentioned entities — OpenAI co-occurs with everything.

I asserted a "China bloc" and grouped its members myself. Louvain, given no
grouping, returns something different for 2026H1:

1. `openai, anthropic, langchain, nous-research, hugging-face, cursor, microsoft, cognition, github`
2. `ollama, nvidia, baseten, openrouter, vllm, unsloth, togethercompute`
3. `google-deepmind, google, deepseek, alibaba, x-ai, z-ai`

Two corrections fall out. **The Chinese labs do not form their own community** —
they cluster with Google, presumably because they co-occur in the same
model-release comparison stories. And there is a **serving-infrastructure
community** (ollama, vLLM, Baseten, OpenRouter, Together, Unsloth) that I never
identified as a bloc at all, despite it being one of the three main structures in
the data.

My bloc was defensible as a *market* grouping. It is not the grouping the
coverage produces, and I presented it as though the data had found it.

### Brokers

Betweenness centrality over the whole corpus:

`google, hugging-face, alibaba, nvidia, ollama, langchain, mistral-ai, deepseek`

Hugging Face ranking second is the notable one — it is not a frontier lab, and by
`density.py` it was fading. Structurally it is the connective tissue: the place
where every other actor's work meets. Prominence and centrality are different
things, and only the network sees the second one.

---

## 7. Survival analysis: models die faster than the arcs suggest

`survival.py`, Kaplan-Meier with right-censoring. Censoring matters here: a model
first seen recently and still discussed has an *unfinished* life, and averaging
raw spans would understate exactly the newest models you most want to compare.

| Cohort | Models | Died | Still alive | Median lifespan |
|---|---|---|---|---|
| All models | 255 | 217 | 38 | **137 days** |
| US frontier labs | 161 | 141 | 20 | **175 days** |
| Chinese labs | 49 | 40 | 9 | **85 days** |
| Open-weights families | 100 | 90 | 10 | 117 days |

The median model has **about four and a half months** between its first and last
mention. That is the quantitative version of what the arcs showed anecdotally.

Chinese-lab models have roughly **half the shelf life** of US frontier models
(85 vs 175 days). Read carefully, though: this is at least partly a *naming*
artifact rather than a relevance one. Chinese labs version-bump far more often —
`qwen3.5`, `qwen3.6`, `qwen3.8` are three tags — so each named model is shorter-
lived by construction while the *family* persists and grows. The honest reading
is that the China bloc iterates faster, not that its models are forgotten faster.
Distinguishing those two properly needs family-level grouping, which this does
not do.

---

## What changed in the conclusions

Nothing in `NEWS-ANALYSIS.md` or `VERIFICATION.md` is overturned. The methods
**confirm** the corrected picture — Meta's decline predating Llama 4, OpenAI's
coverage staying flat, Claude and Qwen rising through every segment — and add
three things the counting could not reach:

1. **Words changed meaning while their frequency held.** `harness`, `skills`,
   `prompt`, `distillation` and `safety` all describe different things in 2026
   than in 2024. Any frequency-based series over those terms is measuring two
   concepts and reporting one.
2. **The `agentic` neighbourhood shift is direct evidence** for agents absorbing
   retrieval, replacing an inference drawn from two counts moving oppositely.
3. **Unsupervised topics found a domain I had no category for** — defense and
   national security, rising 7x into 2026.
4. **The community structure is not the one I asserted.** Louvain puts the
   Chinese labs with Google and surfaces a serving-infrastructure bloc I never
   named; Hugging Face is the corpus's top broker despite fading in density.
5. **One question the corpus cannot answer.** The Twitter/Reddit/Discord lead-lag
   is lag-0 by construction, so "which surface breaks a story" is out of reach
   here — a negative result worth recording, since `IDEAS.md` proposed it.
6. **The median model lives ~137 days** between first and last mention, which
   puts a number on the churn the arcs described.

## Method notes

- Format regimes must be controlled for. Every unsupervised method here ranked
  pipeline changes above news events until told not to; see
  `methods/README.md`.
- Topic modelling excludes the Discord recap; drift and log-odds do not. The
  Discord sections are person-dense, which distorts topics but not embeddings.
- word2vec is trained per half-year on 1.6–3.6M words each. Smaller slices would
  be noisier; the 2026H2 slice is deliberately excluded from drift for this
  reason.
- Drift is only interpretable relative to the corpus median (0.365 here), since
  absolute cosine distances depend on model hyperparameters.
