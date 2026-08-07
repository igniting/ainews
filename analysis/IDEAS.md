# What this archive can actually tell us

Notes on analyses worth building, beyond tag-counting. Every number below was
measured against `articles/` — these are validated extractions, not proposals in
the abstract.

## The thing that makes this corpus unusual

The news itself is available elsewhere. What isn't available elsewhere:

1. **It is a dated, never-revised record of what the field *believed* on each
   day.** Most AI history is written backwards, with the winners known. This is
   written forwards, wrong guesses intact.
2. **It carries three layers of structured data in-band that nobody has
   extracted** — Discord telemetry, a tweet attribution graph, and provenance
   for the model that wrote each summary.
3. **It is itself LLM output, produced daily by a documented and changing
   pipeline for 975 days.** That makes it a natural experiment on LLM behavior.

Point 3 is the one I'd chase hardest. It's the analysis nobody else can run,
because running it requires exactly this artifact.

---

## A. Embedded telemetry nobody has mined

### A1. Discord message counts as a builder-attention index

Every Discord channel heading carries its message volume:

```
### **Unsloth AI (Daniel Han) ▷ #[general](...)** (1123 messages🔥🔥🔥):
```

Extracted: **31,688 channel-day records, 2,149,819 messages, 56 servers**,
covering 418 issues from 2024-05-21 to 2026-03-09.

This is behavioral data, not coverage data. Headlines measure what journalists
found interesting; message volume measures where builders actually spent their
evenings. The two should diverge, and the divergences are the finding.

Concrete questions:
- **Does Discord activity lead the headlines?** If Cursor's server spiked weeks
  before Cursor entered the company tags, community telemetry is a leading
  indicator of what becomes news. Testable with cross-correlation at lag.
- **Migration flows.** Servers have birth and death dates in this data
  (`first_seen`/`last_seen` per server). Stability.ai fading while Cursor and
  Windsurf appear is the visible shape of an ecosystem reallocating.
- **Channel mix within a server.** A `#help`-to-`#research` ratio that climbs is
  a tool crossing from research toy to production dependency. That transition
  has a date, per tool.

### A2. Three-source propagation lag

Each issue has separate `AI Twitter Recap`, `AI Reddit Recap` and `AI Discord
Recap` sections covering the *same day*. So for any story you can ask which
surface broke it and which followed. Do open-weights releases break on Reddit
and closed releases on Twitter? Does Discord lead on tooling and lag on research?
This is a per-story measurement, and the corpus gives ~550 days of it.

---

## B. The corpus as a record of belief

### B2. Hype lead time — the gap between rumor and reality

Measuring first mention against peak-attention month:

| Model | First mentioned | Peak month | Lead |
|---|---|---|---|
| gpt-5 | 2023-12-07 | 2025-08 | **603 days** |
| claude-code | 2025-02-25 | 2026-03 | 369 days |
| codex | 2025-05-26 | 2026-05 | 340 days |
| gpt-4o | 2024-03-20 | 2024-12 | 256 days |
| llama-3 | 2023-12-11 | 2024-04 | 112 days |
| deepseek-r1 | 2024-11-22 | 2025-02 | 71 days |
| gemini-2.5-pro | 2025-03-26 | 2025-05 | 36 days |

GPT-5 was being discussed **20 months** before it landed. Note the pattern: lead
times for models that arrived unannounced (deepseek-r1, gemini-2.5-pro) are
short, while anticipated flagships accumulate years of speculation. The ratio is
a measure of how much of AI discourse is about things that do not yet exist.

### B3. Vaporware detection

The inverse of B2, and the more interesting half: models and companies discussed
persistently that *never shipped anything*. A tag with sustained mentions and no
release event is a dead-end the field spent real attention on. Nobody writes
retrospectives about these, because by definition nothing happened — but the
corpus recorded the attention as it was spent.

### B4. Consensus reversals

Find entities whose surrounding sentiment flips, then read what happened in
between. The Jan 2025 "DeepSeek ends NVIDIA" episode is the obvious test case —
the archive has NVIDIA at 19% of issues in 2025H1 with a stock-panic framing,
and the framing did not survive. Systematically: for each major entity, segment
the corpus by period and detect polarity flips. Each flip is a moment the field
was confidently wrong, with a date attached.

### B5. Scoring the archive's own predictions

The recaps contain dated forecasts. Later issues contain the outcomes. That's a
closed loop: extract forward-looking claims, match them to subsequent reporting,
and produce a calibration score for the field's collective forecasting. To my
knowledge no one has a corpus that permits this cleanly.

---

## C. The corpus as an LLM evaluation set

**This is the strongest idea here.** The archive is a 975-day record of one LLM
pipeline doing one task, and it embeds its own ground truth.

### C1. Attribution fidelity over time

Tweets are cited as `[@DisplayName](https://twitter.com/handle/status/ID)`. The
URL is ground truth; the display name is the model's recall. Measured across
**18,854 attributed tweets in 554 issues**:

| Year | Mismatched attributions | Rate |
|---|---|---|
| 2024 | 169 / 3,174 | 5.3% |
| 2025 | 449 / 9,739 | 4.6% |
| 2026 | 77 / 5,940 | **1.3%** |

A 4x drop in attribution error on a fixed task over two years. There are also
**23 cases of one status ID attributed to two different handles inside a single
issue** — unambiguous errors, since a tweet has one author.

*Caveat:* some mismatches are legitimate (quote-tweets, display name genuinely
differing from handle), so the absolute rate is an upper bound. The methodology
is constant across years, so the **trend** is sound even though the level isn't.

### C2. The natural experiment

The recaps state which model wrote them:

| Summarizer | Issues |
|---|---|
| Claude 3.5 Sonnet, best of 4 runs | 142 |
| Claude 3 Opus, best of 4 runs | 82 |
| Gemini 2.0 Flash | 1 |
| Claude 3 Opus, lightly edited by swyx | 2 |

Combine with C1 and you get error rates **per summarizer model on identical
work** — a real-world hallucination benchmark on a messy production task, with
ground truth embedded in the artifact, spanning several model generations. The
attribution notes even document the pipeline's intent ("We are working on
antihallucination, NER, and context addition pipelines"), so pipeline changes are
datable too.

This is a genuinely novel eval. It is not a synthetic benchmark; it is three
years of a production summarizer being graded against links it had to get right.

### C3. Metadata drift

The front-matter tags are themselves LLM-generated. Sample issues, hand-check the
tags against the body, and measure whether the tagging layer got more accurate —
and whether it inherits the biases of whichever model produced it. This also
tells us how much to trust every tag-based number in `report.md`, including my
own.

---

## D. Structural questions

### D1. Attention concentration

Compute an HHI or Gini over the company tags per period. Is AI news consolidating
onto fewer players or fragmenting? The raw counts hint at fragmentation — OpenAI
slid from 67% of issues to 42% — but concentration needs the whole distribution,
not the top line.

### D2. Co-occurrence graph over time

Build a graph where entities are linked by shared issues, then watch its
community structure evolve. The interesting hypothesis is a splitting of the
open-weights bloc from the frontier-lab bloc, and the timing of any bridge
entities (Hugging Face, OpenRouter, vLLM) that hold the two together.

### D3. Extractable numeric claims

The prose is dense with figures — "236B model 42% faster", "671B parameters",
"1.58bit", "80% size reduction", "-17%". Parsing these gives claimed parameter
counts, context windows, benchmark scores and $/token *as asserted at the time*.
The inference-cost deflation curve built from in-band claims would be a strong
artifact, and it is checkable against what actually happened.

---

## Honest limits

- The recaps are **LLM summaries, not primary sources**. Every entity count is
  filtered through a summarizer with its own biases — which is exactly why C3
  matters before leaning hard on B and D.
- **Discord telemetry covers 418 of 690 issues** (2024-05-21 → 2026-03-09). The
  format changed at both ends; don't read the boundaries as activity collapse.
- **Issue length collapses in 2026** (28k → 5.8k words). Any raw-volume metric
  will show a 2026 cliff that is a format change, not a change in the world.
  Normalize per-issue, always.
- Coverage is **the newsletter's attention, not the field's**. It is one
  editorial viewpoint, heavily weighted toward open models, tooling and the
  Discord ecosystems it samples.

## Where I'd start

**C1 + C2** — the LLM fidelity benchmark. Highest novelty, ground truth is
already in the file, and the extraction is validated above.

**A1** — the Discord attention index. 2.1M messages of behavioral data is the
largest untouched asset here, and the lead-indicator question is genuinely
open.

**B2 + B3** — hype lead time and its vaporware inverse. Cheap (the index already
supports it) and the framing is one people will argue about, which is a point in
its favor.
