# Method audit after the source-composition finding

Every method re-examined against the two artifacts found by reading: **title/lede
templating** and **source-composition inversion** (issue words go 96% Discord →
0%, Twitter 2% → 23%).

Verdicts: **Holds** (unaffected or re-verified), **Fixed** (control added and
re-run), **Weakened** (survives with reduced scope), **Invalid** (withdrawn).

| Method | Exposure | Verdict |
|---|---|---|
| `sections.py` | — (it *is* the control) | **Holds** |
| `leadlag.py` | already measured within sections | **Holds** |
| `bradley_terry.py` | already excluded Discord | **Holds** |
| `claims.py` | already excluded Discord | **Holds** (price n=151 still thin) |
| `topics.py` | already excluded Discord | **Holds**; early periods thin |
| `survival.py` | model tags could die when Discord sampling stopped | **Holds** — re-checked, no death spike at the cutoff |
| `changepoints.py` | format regimes | **Holds** — it *detected* the composition change (regime 4 = Discord removal) |
| `semantic_drift.py` | trained on 96% Discord (2024H1) vs 0% (2026H1) | **Fixed + Weakened** — re-run with genre control; 5 of 7 survive |
| `arcs.py` | title templating | **Fixed** — `--descriptive-only` |
| `density.py` | whole-issue normalization | **Weakened** — superseded by `sections.py` for cross-era claims |
| `bursts.py` | whole-issue rates across the composition change | **Weakened** — within-regime bursts only |
| `novelty.py` | KL tracks composition | **Weakened** — already restricted; do not read across regimes |
| `axes.py` | same embeddings as drift | **Needs re-run** with `--exclude-discord` |
| `distributions.py` | entity diversity vs sampling breadth | **Needs re-check** — see below |
| `analyze.py` quiet-day table | title/lede templating | **Invalid** — withdrawn |
| `logodds.py` | genre and URL drift | **Weakened** — see below |

---

## Re-run: semantic drift with the genre control

Retrained on lede + Twitter + Reddit only (`--exclude-discord`), so chat
transcripts are excluded from every era. Median drift 0.313.

| Term | Drift | 2024H1 | 2026H1 | Verdict |
|---|---|---|---|---|
| `skills` | **0.590** | goals, abilities, experiences | middleware, reusable, ide, filesystem | **Survives** |
| `distillation` | **0.448** | unet, dare, neuron, imagenet | attacks, **industrial-scale, copyrighted, laws** | **Survives, stronger** |
| `harness` | **0.439** | lm-evaluation-harness, eval, lm-eval, helm | orchestration, harnesses, ux, abstraction | **Survives** |
| `agentic` | **0.371** | empowers, augmenting, production-ready, devika, low-code | long-horizon, tool-use, multi-step, computer-use, swe | **Survives, refined** |
| `prompt` | **0.363** | prompts, engineering, crafting, promptfoo | injection, adherence, caching | **Survives** |
| `context` | 0.170 | window, length, contexts | window, length, cache, kv | **Weakened** |
| `safety` | 0.272 | disclosure, copyright, legal, regulatory | political, mass, surveillance, misuse | **Reinterpreted** |

Three changes worth stating plainly:

- **`context rot` was a Discord artifact.** Under the genre control `rot`
  disappears from `context`'s neighbours entirely. It was practitioners in chat
  naming a failure mode, not the field's news prose. Withdrawn as a headline
  finding, kept as a practitioner observation.
- **The `agentic` 2024 reading was wrong in its specifics.** I reported it sat
  next to *retrieval-augmented*, and inferred agents absorbed RAG. Genre-controlled,
  its 2024 neighbours are `low-code`, `devika`, `production-ready` — the early
  agent-framework hype, not RAG. The 2026 end (`long-horizon`, `computer-use`,
  `swe`) is unchanged, so the *direction* holds but the "agents absorbed retrieval"
  inference loses this piece of its support. The domain counts still support it;
  the embedding no longer does.
- **`safety` reinterprets.** Not "legislation → operational security" as I wrote,
  but legal/regulatory → **surveillance, misuse, political**. A societal framing,
  not an ops one.

`distillation` gets stronger: its 2026 neighbours are now explicitly
`industrial-scale, copyrighted, laws` — the language of the Anthropic accusation.

---

## Weakened: log-odds

Re-run within Twitter + Reddit only, so genre is fixed. The top 2026-distinctive
token is **`x.com` at z = −46.2** — the twitter.com → x.com domain migration —
followed by `status` (status IDs in URLs). `theme`, `highlights`, `discussions`,
`suggests`, `rather` are template words.

The content signal is there (`llama, rag, diffusion` vs `agent, opus, anthropic,
claude, code`) but sits below URL and template drift even after source control.
**Log-odds is the weakest method in the repo on this corpus** and needs URL
stripping plus template-word filtering before its output means anything.

---

## Needs re-check: the diversity result

`distributions.py` reports the effective number of companies rising 21.7 → 101.8
(Hill-1), which I presented as ~5x fragmentation.

**The declared sampling breadth rose over the same window** — 7 → 12 subreddits
and 384 → 544 Twitter accounts. More sources sampled mechanically yields more
distinct entities mentioned, which inflates richness and Hill numbers. The
fragmentation finding and the sampling-breadth increase are confounded, and I did
not control for it.

This is the largest open threat remaining. The fix is to compute diversity from
entities extracted *within a fixed section* rather than from whole-issue
front-matter tags. Until then the fragmentation magnitude should be treated as an
upper bound, and the cross-validation I claimed with the OpenAI headline result is
weaker than stated — both could partly reflect broader sampling.

---

## What survives unchanged

The load-bearing results are the ones `sections.py` already re-verified inside a
fixed source:

- **China bloc rise** — reproduces independently in Twitter (8.6×) and Reddit (15.3×)
- **Meta + Mistral fall** — reproduces in both (→ 0.0× in both)
- **RAG collapse** — both sections
- **Reasoning peak then decline** — both sections, peak 2025H1
- **`harness` referent drift** — survives the genre control, and both sections
  agree on the term's rise (17.9× vs 16.8×)
- **Meta's 2024-10 change point** — falls inside the stable regime, unaffected
- **Model half-life of 137 days** — no death clustering at the sampling cutoff

## Withdrawn

- The **"not much happened today" quiet-day series** (5% → 85%). Boilerplate.
- **`context rot`** as a corpus-level semantic finding.
- The **"agentic sat next to retrieval-augmented in 2024"** claim.
- **OpenAI's 18% → 4% headline collapse** as evidence of fragmentation.
