# Verifying the arcs against the article bodies

`NEWS-ANALYSIS.md` was written from issue titles and front-matter tags — 0.58% of
the corpus. This checks those claims against the other 99.4%, using
`analysis/density.py` (mentions per 10,000 words of body text) and
`analysis/passages.py` (reading what the issues actually said).

**Four of eleven claims survive intact, three need real correction, two were
wrong, and the exercise turned up a finding bigger than anything in the original.**

---

## The measurement problem, first

Three ways to ask "how much did the archive cover X" disagree badly:

| Measure | What it captures | Failure mode |
|---|---|---|
| Headline share | Was it the day's story? | Editorially loaded; a company can matter enormously and rarely headline |
| Binary presence | Mentioned at all? | Saturates — a 24,000-word issue saying "agent" once scores 100% |
| **Density** | Mentions per 10k words | The one to trust |

Binary presence is useless here: `reasoning` appears in 98–100% of issues in
every period since 2024, and `agents` in 100% since 2024H1. That measure says
nothing changed, which is plainly false.

Density is the referee below. Where density and headline share **diverge**, the
gap is itself the finding.

---

## Claim-by-claim

### ✅ CONFIRMED — "The open-weights frontier moved to China"

This was my most speculative claim. It is the most strongly confirmed, and the
magnitude is far beyond what the headlines showed.

Mentions per 10,000 words:

| | 2023H2 | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 | 2026H2 |
|---|---|---|---|---|---|---|---|
| **China bloc** (DeepSeek+Qwen+Kimi+GLM+MiniMax) | 1.3 | 4.0 | 10.9 | 40.2 | 37.4 | 48.7 | **89.2** |
| **Meta + Mistral** | 94.8 | 48.0 | 29.9 | 14.4 | 6.5 | 4.3 | **2.1** |

A **73:1 Western advantage inverts to 42:1 the other way**, crossing over in
2025H1. This is the largest single movement anywhere in the corpus.

### ❌ WRONG — "Headline days show the China bloc as minor"

My own table listed Alibaba at 14 headline days and Moonshot at 7, next to
OpenAI's 94, and I treated them as second tier. Density says otherwise:

| Share of 2026 issues mentioning | |
|---|---|
| Qwen | 95% |
| DeepSeek | 83% |
| Kimi/Moonshot | 82% |
| GLM/z.ai | 74% |
| MiniMax | 65% |

Kimi/Moonshot goes from **0.1 to 35.9** mentions per 10k words — a 359x rise, the
steepest of any entity measured. These labs are close to omnipresent in the body
while almost never being the headline.

This is exactly the "constantly present, rarely the story" pattern I built
`arcs.py` to detect — and then failed to apply to the companies where it mattered
most. Being covered daily without ever being the day's story is a *distinct
market position*, and the headline-only analysis is blind to it.

### ❌ WRONG — "Llama 4's Controversial Weekend Release was the inflection"

I dated Meta's fall to a single headline, 2025-04-08. Monthly density says the
decline was already six months old:

```
2024-10   17.2  #################
2024-11   11.7  ###########
2024-12   12.9  ############
2025-01    8.0  ########
2025-02    6.9  ######
2025-03    5.9  #####
2025-04   19.7  ###################   <-- Llama 4
2025-05    4.7  ####
2025-06    4.0  ####
2025-08    2.0  ##
2025-12    1.6  #
```

Llama fell 17.2 → 5.9 **before** Llama 4 shipped. Llama 4 produced a one-month
spike to 19.7 — briefly back to peak — after which it collapsed to 4.7 and never
recovered.

The truer story: **Llama 4 was a failed rescue of a decline already underway**,
not the cause of one. Picking a dramatic headline and calling it a turning point
is exactly the error that title-only analysis invites.

### ⚠️ NEEDS CORRECTION — "Mistral fell to 0%, Meta's arc ends"

Headline share genuinely reaches 0% for both. But they have not vanished:
**Mistral appears in 47% of 2026 issues, Llama in 36%.**

And the passages show Mistral was still competitive at the end. From 2025-12-02:

> **Mistral is back!** … after raising 1.7B at a 11.7B valuation

From 2025-12-09, on Devstral 2:

> "Sonnet 4.3 level" but 10x cheaper by API and open weights, winning or tying
> with DeepSeek v3.2 **71% of the time** in third party human evals

A company beating DeepSeek in third-party human evals in December 2025 is not a
company that lost on merit. The decline is real in density (90.9 → 1.5) but
"the arc that ends" overstated it. Mistral stopped being *news* well before it
stopped being *good* — which is a different and more interesting claim than the
one I made.

### ❌ WRONG — "OpenAI's coverage declined"

I wrote that OpenAI's headline share fell 18% → 4% because its news migrated to
infrastructure finance. The first half is true; the conclusion isn't.

| | 2023H2 | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 | 2026H2 |
|---|---|---|---|---|---|---|---|
| Headline share | 8% | 12% | 18% | 18% | 16% | 6% | 4% |
| **Density** | 59.1 | 41.1 | 34.5 | 37.1 | 48.7 | 34.2 | **51.1** |

**Density is flat to rising.** OpenAI is discussed as much in 2026H2 as in
2023H2. It stopped being the *headline* without being covered any less — the
field got more competitors worth naming in a title, not less OpenAI.

This is the clearest case of headline share measuring editorial framing rather
than attention, and I read it as the latter.

### ❌ NOT SUPPORTED — "DeepSeek's role changed from protagonist to benchmark"

Testable: how often DeepSeek appears in comparative framing ("beats", "matches",
"X-level", "vs") versus at all.

| | 2024H2 | 2025H1 | 2025H2 | 2026H1 | 2026H2 |
|---|---|---|---|---|---|
| Yardstick framing, share of issues | 6% | **56%** | 28% | 12% | 15% |

The yardstick ratio **peaks at DeepSeek's protagonist moment** (2025H1, the R1
week) and declines afterward — the opposite of a shift from subject to
benchmark. DeepSeek was both at once during R1, then faded on both measures
before recovering in density (20.9 in 2026H2, on v4).

The regex is crude, so treat this as "unsupported" rather than "refuted". But it
does not show what I claimed.

### ✅ CONFIRMED — "Reasoning was absorbed, not abandoned"

Tag data showed Reasoning & RL peaking at 66% then falling to 31%, which could
equally mean the field moved on. Density resolves it:

| reasoning | 2023H2 | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 | 2026H2 |
|---|---|---|---|---|---|---|---|
| per 10k words | 3.1 | 4.7 | 10.1 | **21.1** | 12.6 | 10.8 | 11.4 |

It retreats from the o1/R1 peak but settles at **3.5x its 2024H1 baseline** and
holds there. That is absorption — a capability that became routine, still
discussed constantly, no longer announced.

### ✅ CONFIRMED — Agents, retrieval and fine-tuning

The three biggest domain claims all survive at density, independent of the tags:

| per 10k words | 2023H2 | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 | 2026H2 |
|---|---|---|---|---|---|---|---|
| agentic | 7.0 | 10.5 | 15.3 | 30.4 | 32.4 | 44.2 | **52.8** |
| RAG/retrieval | 7.6 | **16.3** | 11.5 | 5.3 | 4.1 | 2.3 | **2.0** |
| fine-tuning | **39.7** | 34.4 | 21.7 | 13.9 | 12.5 | 7.5 | **5.3** |

Agents up 7.5x, retrieval down 8x from peak, fine-tuning down 7.5x. The tag-based
domain analysis was sound on all three.

### ✅ CONFIRMED — "Anthropic is the only major arc still rising"

Claude density: 2.9 → 8.8 → 9.2 → 17.4 → 14.8 → 32.1 → **33.2**. An 11x rise,
still climbing at the end of the corpus. Holds on both measures.

### 🆕 NEW — MCP is a textbook hype curve

Not in the original analysis at all, and only visible in the body:

| MCP | 2024H2 | 2025H1 | 2025H2 | 2026H1 | 2026H2 |
|---|---|---|---|---|---|
| per 10k words | 0.7 | **23.3** | 13.3 | 6.2 | 3.3 |

Zero to 23.3 in two quarters, then a 7x fall. I called MCP "the highest-leverage
item" in Anthropic's arc on the strength of one headline (*"OpenAI adopts MCP"*).
By density its discussion peaked in 2025H1 and has fallen ever since — even as
Claude's own density doubled. Adoption and discussion decoupled: plausibly the
signature of a protocol that won and became plumbing, but the original claim
outran its evidence.

---

## What this changes

**The pattern in my errors is consistent.** Every wrong call came from treating
the *title* as a measure of attention. Titles are an editor choosing one story
from a day with many. They are excellent for "what was the story" and actively
misleading for "how much did this matter":

- OpenAI: headline share collapsed, coverage didn't.
- China bloc: barely headlined, nearly omnipresent.
- Meta: the dramatic headline was six months late to its own decline.
- Mistral: headline zero, still in half of all issues, still shipping wins.

**The corrected headline finding** is stronger than the original: the
open-weights frontier moved from Meta and Mistral to a five-lab Chinese bloc, a
73:1 advantage inverting to 42:1 in roughly two years, crossing over in 2025H1 —
and the newsletter's *titles* barely register it, because those labs ship
constantly without producing the kind of single-day event that earns a headline.

## Method notes

- Density is mentions per 10k words on the body with front matter stripped.
  `/r/LocalLlama`, `llama.cpp`, `ollama`, `llamaindex` are removed before Llama
  matching — without that, "Llama" scores 100% in every period.
- Regexes are surface matches and will over-count on ambiguous strings (`agent`
  catches "user agent"; `minimax` catches the game-tree algorithm). Trends over a
  fixed pattern are sound; absolute levels are upper bounds.
- 2023H2 (0.2M words) and 2026H2 (0.2M words) are thin. Density normalizes for
  length but not for sample size — treat the end columns as indicative.
- Issue length fell from ~28k to ~5.8k words in 2026, which is exactly why
  density rather than raw counts is used throughout.
