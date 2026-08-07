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
