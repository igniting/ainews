# What actually happened, 2023–2026

Read from the archive's headline timelines (`analysis/arcs.py`) and domain
tracking (`analysis/domains.py`). The title of each issue is the editor's verdict
on what mattered that day, so "headline days" — days a company *was* the story —
is the unit throughout. A company can be constantly present and rarely a
headline; that difference turns out to be the whole story for several of them.

---

## Part 1: Company arcs

### The distribution is brutally unequal

| Company | Headline days | Peak period | Headline share at peak |
|---|---|---|---|
| OpenAI | 94 | 2024H2–2025H1 | 18% |
| Google | 52 | 2025H1 | 12% |
| Anthropic | 42 | 2026H1 | 10% |
| Meta | 34 | 2024H2 | 9% |
| Mistral | 22 | 2023H2 | **33%** |
| DeepSeek | 20 | 2025H1 | 6% |
| Alibaba/Qwen | 14 | 2025H2 | 4% |
| NVIDIA | 11 | 2025H2 | 4% |
| xAI | 9 | 2025H1–2026H1 | 2% |
| Moonshot | 7 | 2025H2 | 3% |
| Cursor | 6 | 2025H1 | 2% |
| Stability | 4 | 2024H1 | 2% |

Twelve companies account for most of what the newsletter considered a story on
any given day. But the *shape* of each arc differs more than the totals suggest.

### Mistral: the fastest rise and the most complete fall

The single most dramatic arc in the corpus. In **2023H2, Mistral was the subject
of 33% of all issues** — a third of the newsletter, by far the highest
concentration any company ever achieved. December 2023 reads as a continuous
Mistral event: *"The Mixtral Rush"*, *"Mixtral beats GPT3.5 and Llama2-70B"*,
*"Mixtral-Instruct beats Gemini Pro"*, *"Dolphin Mixtral 8x7b is wild"*.

Then a two-year decay to zero: 4% → 2% → 2% → 2% → 0%. The headlines track the
mechanism precisely. First the model itself is displaced — *"Jamba: Mixture of
Architectures dethrones Mixtral"* (Mar 2024), *"DeepSeek-V2 beats Mixtral 8x22B
with >160 experts at HALF the cost"* (May 2024). Then Mistral is graded against
peers rather than setting the bar — *"Mistral Large disappoints"* (Feb 2024),
*"Pixtral 12B: Mistral beats Llama to Multimodality"* (a win, but framed as a
race against Meta). Mistral kept shipping through 2025 — Agents API, Magistral,
Voxtral, Mistral 3 — and the archive kept covering it, but never again as the
day's story.

**The lesson in the arc:** Mistral's fall wasn't a collapse in output. It was
the open-weights frontier moving to China. Mistral's decline and DeepSeek's rise
are the same event viewed from two sides.

### DeepSeek: the only company that moved a stock index

DeepSeek's arc has a genuinely unusual property — it escapes the AI press
entirely. The build-up is technical and gradual: *"DeepSeek-V2 beats Mixtral
8x22B at HALF the cost"* (May 2024), *"DeepSeek-R1 claims to beat o1-preview AND
will be open sourced"* (Nov 2024), *"DeepSeek v3: 671B finegrained MoE trained
for $5.5m USD of compute"* (Dec 2024). The cost figure is the through-line at
every step.

Then, in one week of January 2025: *"DeepSeek R1: o1-level open weights model"*
(Jan 21) → *"TinyZero: Reproduce DeepSeek R1-Zero for $30"* (Jan 25) → **"DeepSeek
#1 on US App Store, Nvidia stock tanks -17%"** (Jan 28). Seven days from a model
release to a mainstream financial event.

What makes it analytically interesting is the aftermath. DeepSeek's headline
share *fell* after its peak — 6% in 2025H1, 4%, then 2%. The company kept
shipping strong work (V3.1 "beating Claude 4 Sonnet at 11% of its cost",
DeepSeek-OCR, V3.2, v4). But its role changed from protagonist to **benchmark**:
it starts appearing in *other companies'* headlines as the thing to beat —
*"QwQ-32B claims to match DeepSeek R1-671B"*, *"Cohere's Command A claims #3 open
model spot (after DeepSeek and Gemma)"*, *"GLM-4.5: better than Kimi/Qwen/DeepSeek"*.
Becoming the unit of measurement is a kind of success that looks like decline in
the coverage data.

### Anthropic: the only major arc still rising at the end

Anthropic is the inverse of everyone else. Its headline share climbs across the
entire corpus — 4%, 5%, 4%, 5%, 8%, **10%** — peaking in the final full period
while OpenAI's collapses from 18% to 4%. It is the only company in the archive
whose best period is its last.

The arc has three distinct phases:

1. **Research curiosity (2023–2024H1).** *"Anthropic says 'skill issue'"*,
   *"Anthropic coins Sleeper Agents"*, *"Anthropic's 'LLM Genome Project':
   learning & clamping 34m features"*. Interpretability and safety work — respected,
   niche.
2. **Product breakout (2024H2–2025).** *"Claude 3 just destroyed GPT 4"*,
   *"Claude Crushes Code — 92% HumanEval and Claude.ai Artifacts"*, *"Claude 3.5
   Sonnet (New) gets Computer Use"*, and critically *"Anthropic launches the Model
   Context Protocol"* (Nov 2024). MCP is the highest-leverage item in the arc —
   by Mar 2025 the archive reports *"OpenAI adopts MCP"*, a competitor
   standardizing on a rival's protocol.
3. **Platform and capital (2025H2–2026).** The headlines stop being about models
   and become about scale: $61.5B Series E → $13B at $183B → $30B at $380B →
   *"$65B in Series H at a $965B post-money valuation"*, alongside *"Anthropic @
   $30B ARR"* and a *"300MW/$5B/yr"* compute deal.

The Claude Code sub-arc is worth isolating: *"The Quiet Rise of Claude Code vs
Codex"* (Jun 2025) → *"Claude Code 2.0"* (Sep) → *"Claude Agent Skills — glorified
AGENTS.md? or MCP killer?"* (Oct) → *"Claude Code Anniversary"* (Feb 2026) →
*"The Claude Code Source Leak"* (Mar 2026). The newsletter caught the coding-agent
shift about nine months before it became the field's dominant story.

### OpenAI: still the largest, no longer the default

94 headline days, more than double anyone else. But the trajectory is a clean
inverted-U: 8% → 12% → 18% → 18% → 16% → 6% → 4%.

The 2024–2025 peak is dense with genuine firsts — *"GPT-4o: the new
SOTA-EVERYTHING Frontier model"*, *"o1: OpenAI's new general reasoning models"*,
*"o3 solves AIME, GPQA, Codeforces, makes 11 years of progress in ARC-AGI"*.
During this stretch OpenAI defines the axis everyone else is measured on; note
how often rivals appear in OpenAI-framed headlines (*"Llama-3-70b is GPT-4-level
Open Model"*, *"DeepSeek R1: o1-level open weights model"*).

After mid-2025 the *content* of OpenAI headlines changes character. Compare:

- 2024: models and capabilities — Sora, o1, Canvas, Realtime API, Advanced Voice.
- 2026: capital and distribution — *"Oracle jumps +36% after winning $300B OpenAI
  contract"*, *"NVIDIA to invest $100B in OpenAI"*, *"OpenAI Titan XPU: 10GW of
  self-designed chips with Broadcom"*, *"ChatGPT starts testing ads on free
  tier"*, *"closes $110B raise… largest startup fundraise in history"*.

The declining headline share isn't OpenAI mattering less. It's that OpenAI's news
migrated from a domain the newsletter covers intensively (models) to one it
covers thinly (infrastructure finance) — while the number of credible rivals
producing model news roughly tripled.

### Meta: the arc that ends

Meta is the clearest fall after Mistral, and it ends harder. Headline share:
8% → 8% → 9% → 6% → 1% → 1% → 0%.

Through 2024 Meta *is* open weights. *"Meta Llama 3 (8B, 70B)"*, *"Llama-3-70b is
GPT-4-level Open Model"*, *"Llama 3.1: The Synthetic Data Model"*, *"Llama 3.2:
On-device 1B/3B, and Multimodal"*, *"Meta Llama 3.3: 405B/Nova Pro performance at
70B price"* — plus genuine research risk in *"Meta BLT: Tokenizer-free, Byte-level
LLM"* and *"Chameleon"*.

The inflection is a single dated headline: **"Llama 4's Controversial Weekend
Release"** (2025-04-08). After it, Llama essentially stops appearing as a
headline subject. Meta's later appearances are about *organization*, not models —
*"Execuhires Round 2: Scale-Meta"*, *"Meta Superintelligence Labs acquires Manus
AI for over $2B"*. By 2026 Meta re-enters via an entirely different product line
(Muse Spark / Muse Code, in the coding-agent race) — a rebuild, not a
continuation.

**Cross-arc observation:** Mistral and Meta, the two 2023–24 open-weights
champions, both fell. Open source as a *domain* did not fall (17% → 38%). The
banner moved: Qwen, DeepSeek, Moonshot/Kimi, GLM, MiniMax. That substitution is
the single most consequential shift in the corpus.

### The China bloc: the aggregate nobody tracks as one thing

Individually these look minor — Alibaba 14 headline days, Moonshot 7, DeepSeek
20. Together they are the story of 2025–26, and the headlines increasingly treat
them as a single competitive front rather than separate companies:

- *"GLM-4.5: Deeper, Headier, & better than Kimi/Qwen/DeepSeek (SOTA China LLM?)"*
- *"Chinese Models Launch — MiniMax-M1, Hailuo 2 'Kangaroo', Moonshot Kimi-Dev-72B"*
- *"MiniMax M2 230BA10B — 8% of Claude Sonnet's price, ~2x faster, new SOTA open model"*
- *"Anthropic accuses DeepSeek, Moonshot, and MiniMax of 'industrial-scale distillation attacks'"*

That last one (2026-02-24) is the clearest marker of arrival: a US frontier lab
naming three Chinese labs together as a competitive threat. Note also the pricing
framing that recurs in nearly every one — *8% of Claude Sonnet's price*, *11% of
its cost*, *HALF the cost*. Price is the axis this bloc competes on in the
archive's telling, consistently, for two years.

---

## Part 2: Domain evolution

Share of each period's issues touching a domain (domains overlap, so columns
don't sum to 100%):

| Domain | 2023H2 | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 | 2026H2 |
|---|---|---|---|---|---|---|---|
| **Agents & tool use** | 4% | 23% | 35% | 41% | 62% | **86%** | 85% |
| Evaluation | 71% | 55% | 64% | 69% | 61% | 56% | 73% |
| Efficiency & hardware | 58% | 75% | 58% | 61% | 68% | 67% | 58% |
| **Training & data** | 46% | **76%** | 60% | 50% | 43% | 24% | 23% |
| Vision & image | 38% | 49% | 61% | 55% | 44% | 25% | 46% |
| Context & memory | 25% | 35% | 38% | 37% | 50% | 48% | 42% |
| Reasoning & RL | 8% | 25% | 39% | **66%** | 57% | 35% | 31% |
| Coding | 25% | 20% | 25% | 38% | 39% | 43% | 42% |
| Architecture | 33% | 42% | 32% | 25% | 45% | 37% | 38% |
| Safety & security | 21% | 27% | 30% | 15% | 15% | 32% | 27% |
| Open source | 17% | 17% | 20% | 33% | 24% | 18% | 38% |
| Policy & business | 8% | 16% | 17% | 19% | 20% | 17% | 27% |
| **Retrieval & search** | 8% | **31%** | 27% | 14% | 15% | 6% | 4% |
| Audio & speech | 21% | 11% | 19% | 23% | 13% | 6% | 8% |
| Video | 8% | 11% | 17% | 17% | 16% | 5% | 12% |
| Robotics & embodied | 0% | 5% | 12% | 7% | 6% | 2% | 8% |

### The one-way door: agents

**4% → 86%.** No other domain in the corpus moves like this, and it never
retraces. Agents go from a curiosity in late 2023 to touching **six of every
seven issues** by 2026. It is the closest thing to a phase change the archive
records.

The company arcs corroborate it independently: Claude Code, Codex, Cursor,
Devin/Cognition, Windsurf, Manus, Muse Code, Prime Agent. Coding rises alongside
(20% → 43%) because coding is where agents first actually worked.

### The domain that died: retrieval

**31% → 4%.** RAG peaked in 2024H1 and is now nearly absent. This is the
sharpest fall in the corpus and worth being careful about, because RAG didn't
stop being *used* — it stopped being *news*. Two mechanisms are visible in the
data:

1. **Context windows ate it.** Context & memory rises (25% → 48%) as retrieval
   falls. When a model holds a million tokens, retrieving chunks is an
   implementation detail, not an architecture.
2. **Agents absorbed it.** Retrieval became a tool call inside an agent loop.

The two big RAG frameworks then **split**, and this is the most instructive
detail in the domain data:

| | 2023H2 | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 | 2026H2 |
|---|---|---|---|---|---|---|---|
| LangChain | 8% | 10% | 18% | 17% | 13% | **24%** | 19% |
| LlamaIndex | 4% | 9% | 11% | 8% | 8% | **2%** | 4% |

LangChain's coverage *rose* to its all-time high in 2026H1, while its home domain
fell to 6%. LlamaIndex fell to near-zero over exactly the same period. The
difference is that LangChain followed the workload into agents (LangGraph,
LangSmith, gateway/observability) while LlamaIndex stayed closer to the
retrieval/indexing framing.

So the honest version of the story is not "RAG died and took its vendors with
it." It is that the *problem* was redefined, and the vendor that redefined itself
with it kept its coverage. That is a distinction the domain counts alone would
have hidden — the domain fell 31% → 4%, but one of its two flagship projects had
its best year afterward.

### The domain that inverted: training → inference

**Training & data 76% → 23%** is the second-largest fall. In 2024H1 the field's
attention was overwhelmingly on *making* models — fine-tuning, synthetic data,
model merging, distillation, LoRA. By 2026 that is a quarter of issues.

Meanwhile Efficiency & hardware holds steady at 58–75% throughout — the single
most *stable* domain in the corpus. Nothing else stays flat for three years. The
economics of running models never stopped being the story, even as everything
about what was being run changed.

This is the field's center of gravity moving from **training-time to
inference-time**: the `fine-tuning` tag alone goes 44% of 2024 issues → 24% of
2025 → **7% of 2026**, while reasoning/test-time compute spikes, then agents
consume everything.

### The spike that receded: reasoning

Reasoning & RL runs 8% → 25% → 39% → **66%** → 57% → 35% → 31%. The 2025H1 peak
is o1/o3/R1 — the entire field pivoting to test-time compute at once.

The retreat afterwards is not a reversal. It's absorption: reasoning stopped
being a separate topic and became a property models simply have. The archive
shows this in its language — 2025 headlines announce reasoning models as events
(*"Reasoning Models are Near-Superhuman Coders"*, *"Reasoning Price War 2"*);
2026 headlines mention thinking modes as routine features (*"GPT 5.1… adaptive
thinking"*, *"Gemini 3 Deep Think"*).

**This absorption pattern is the archive's most repeated structure.** A
capability arrives as news, peaks, then disappears into the substrate:
multimodality (49% → 25%), reasoning (66% → 31%), retrieval (31% → 4%). Declining
coverage in this corpus more often means *won and absorbed* than *failed*.
Distinguishing the two requires the headlines, not the counts — which is why the
arcs and the domains have to be read together.

### The domains that never arrived

**Robotics peaks at 12% and settles near 2–8%.** For a field with enormous
investment and constant "embodied AI is next" claims, the archive records it as
persistently marginal. Same for audio & speech (23% → 8%) and video (17% → 5%)
— both had moments (Sora, ElevenLabs, Voxtral, Hailuo) that never became
sustained coverage.

Worth stating plainly: this is a newsletter with a builder/LLM-tooling
readership, so this may measure *its* blind spot rather than the field's. But if
you want the corpus's honest answer to "did robotics arrive in this period" —
the answer is no, and it is not close.

### Safety: the U-shape

21% → 27% → 30% → **15% → 15%** → 32% → 27%. Safety coverage halves across 2025
— the period of maximum capability racing — then recovers in 2026. The 2026
recovery reads differently in the headlines: less alignment research, more
security and operational concerns (prompt injection, sandboxing, agent
permissions, the "first model too dangerous" framing, distillation-attack
accusations). Safety came back as **agent security**, which is a different
discipline than what it left as.

---

## What this adds up to

Three claims the data supports:

1. **The open-weights frontier changed hands, and that's the biggest story in
   the corpus.** Mistral (33% → 0%) and Meta (9% → 0%) fell while open source as
   a domain grew (17% → 38%). The banner moved to Qwen, DeepSeek, Moonshot,
   GLM, MiniMax, competing explicitly and consistently on price.

2. **The field moved from building models to operating them.** Training & data
   76% → 23%, agents 4% → 86%, efficiency flat at ~65% throughout. What was
   scarce stopped being model quality and started being orchestration, context
   and cost.

3. **Declining coverage usually means victory, not failure.** Retrieval,
   reasoning, and multimodality all fell hard after peaking, and all three won —
   they became infrastructure. The genuine failures look different: they never
   peak at all.

## Caveats

- Headline days measure **the editor's judgment of the day's story**, which is
  one viewpoint — builder-facing, LLM-tooling-weighted, and light on enterprise
  deployment, hardware supply chains and non-English ecosystems.
- Domain assignment is regex over topic tags (`analysis/domains.py`); tags are
  themselves a generated layer. Composition lists in `domains.md` show what
  matched, for auditing.
- 2026H2 is 26 issues (through 2026-08-06). Treat its column as indicative.
- The title-matching in `arcs.py` uses per-company surface forms — Meta matches
  `llama`, OpenAI matches `gpt`/`o1`/`codex`. A shared headline credits every
  company named in it, which is correct for "who was the story" but means the
  columns don't sum to the issue count.
