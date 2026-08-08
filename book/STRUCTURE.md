# Book structure

## What changes when it stops being a report

The report is 9,500 words for people who already work in AI, organised to defend
claims. A book for *any* software engineer has to do three different things:

1. **Teach as it goes.** It cannot assume MoE, KV cache, GRPO or test-time
   compute. Every technical idea has to be introduced at the moment the field
   introduced it — which the corpus makes natural, because the archive *also*
   introduces each idea the day it appears.
2. **Have an argument, not a findings list.** A report presents results. A book
   needs one claim it is making, that the reader carries out with them.
3. **Have scenes.** The corpus contains genuinely good ones — a seven-day week in
   January 2025, two companies publishing opposite advice on the same morning, an
   architecture dying without a single obituary. A report flattens those into
   effect sizes. A book should not.

## The argument

> **The distance between what a field announces and what it actually runs is
> measurable — and knowing how to measure it is the most useful skill you can
> have in a field moving faster than you can read.**

Three years of AI is the worked example. Every chapter is a case study in that
argument, and the reader should finish able to apply it to whatever replaces
AI as the thing they cannot keep up with.

This is why the book works for a general software engineer. The subject is AI;
the transferable skill is reading a fast-moving field without being played by it.

## Title

**Recommended:** *Written Forwards*
Subtitle: *Three years of AI, as the field saw it happen — and how to tell what
was real*

The concept does the work: history is written backwards, once winners are known;
this archive was written forwards, with the wrong guesses intact. That distinction
is the whole reason the data is worth anything, and it is a book title.

Alternatives considered: *The Hype Gradient* (leads with utility, but narrower);
*Six Hundred and Ninety Days* (evocative, says nothing).

## Voice

First person singular. The book has a narrator who reads an archive, forms
readings, and is repeatedly corrected by it. That is honest to how the work
actually went, it gives the reader someone to travel with, and it makes the
methodology chapters bearable — "here is how I fooled myself" reads, "here is a
threat to validity" does not.

## Shape

Chronological middle, thematic ends. Pure chronology becomes a list of releases;
pure theme loses the story. So: establish the instrument, tell the history
straight, then extract the patterns from a history the reader now knows.

The three **interludes** are the spine of the book's honesty. Each sits at a part
boundary and recounts one thing I got confidently wrong and how the archive
corrected me. They are short — 600–900 words — and they teach more than the
chapters around them.

---

# Contents

Each chapter has a driving question and a payoff the reader can use.

## Part I — The record  *(~4,000 words)*

**1. A field talking to itself**
*What is this thing, and why would anyone read three years of a newsletter?*
The artifact: 690 issues, 15.3M words, published on 70% of days for two years and
eight months. Why forwards-written sources are rare and what they can tell you
that retrospectives cannot. What this data is not — attention, not deployment.
Ends by setting the reader's expectations honestly.

**2. Three surfaces**
*Why does everything in this field feel like hype?*
The book's thesis, stated early rather than saved for the end. Each issue
summarises the same day from Twitter, Reddit and Discord separately — announcement
space, practice space, community space. Measuring the same idea in all three gives
a gradient. Agents rise 10.9× in announcement space, 3.5× in community, 1.2× in
practice. The Chinese open-weights bloc runs the *other* way. That asymmetry is
the tool the rest of the book uses.
**Payoff:** a test the reader can apply — if a shift shrinks as you approach the
people doing the work, it is a narrative; if it grows, it is an adoption the
coverage has not caught up with.

> **Interlude I — The day I measured the newsletter instead of the field**
> Headline share said OpenAI collapsed from 18% to 4%. It hadn't. The title field
> had quietly become a template — "not much happened today" is 0% of 2023 titles
> and 68% of 2026's, and it sits on top of the Claude Opus 5 and GPT-5.6 launches.
> The first lesson: check what the field you are counting actually contains.

## Part II — What happened  *(~13,000 words, the bulk)*

**3. Everyone is fine-tuning** *(Dec 2023 – mid 2024)*
*What did the field think the job was?*
The opening state: making models. Fine-tuning at 34.9 mentions per 10⁴ words, the
densest any theme reaches until agents. Retrieval as the default architecture.
LoRA, synthetic data, model merging, quantization — each introduced as the archive
introduced it. Mistral as the most concentrated presence in the corpus's history:
a third of all issues in one half-year. Llama 3 making open weights competitive.
*Scene:* December 2023, the Mixtral rush, eight issues in a row.

**4. The road not taken**
*What does it look like when a good idea simply does not arrive?*
State-space models — Mamba, RWKV, Hyena — at 12.8 mentions per 10⁴ words in
2024H1, level with MoE. The lede on 2024-05-29: *"SSMs are all you need."* By
2026: **0.0**. No failure, no retraction, no obituary. Contrasted with retrieval,
which fell just as hard and *won*. This chapter teaches the distinction the rest
of the book depends on: absorption versus non-arrival, and how to tell them apart
before the fact.
**Payoff:** the diagnostic is the peak. Things that win peak first, then fade into
substrate. Things that never arrive never peak.

**5. Learning to think** *(Sept 2024 – Jan 2025)*
*How does a whole field change its mind in four months?*
o1 ships; the editor calls it the same day — *"Test-time reasoning is all you
need."* Reasoning goes 7.0 → 23.4 → 40.2. What test-time compute means, explained
for a reader who has never trained anything. Then the two months where every lab
reorients.
*Scene:* 2024-11-25, a lede that reads *"claude_desktop_config.json is all you
need"* — MCP arriving to almost no notice.

**6. Seven days in January**
*What does it look like when something actually breaks through?*
A whole short chapter on one week. 21st: DeepSeek R1 ships at o1 level, open
weights. 25th: someone reproduces R1-Zero for $30. 28th: DeepSeek is the top free
app in the US and NVIDIA falls 17%. Burst detection puts DeepSeek at 4.7× baseline
across those weeks — and puts *reasoning* at a simultaneous burst, which is the
cleanest evidence in the archive that R1 is what turned reasoning from one
company's product feature into everyone's research programme.

**7. The harness** *(2025)*
*When did the field stop talking about models and start talking about the software
around them?*
The word `harness` means an evaluation harness in 2024 and an agent harness in
2026 — the same word, two different things, and the corpus dates the handover.
Claude Code, Codex, Cursor, MCP. Serving infrastructure rises 23×, the largest
move of any technical concern. Context engineering. The lede on 2025-05-15:
*"Agent Harnesses are all you need."*
*Scene:* 2025-06-13, Cognition publishes *Don't Build Multi-Agents* and Anthropic
publishes how it builds multi-agents. Same morning. The newsletter runs both under
one headline and takes no side.

**8. The handover** *(2025–2026)*
*How does a technological lead change hands?*
Qwen, DeepSeek, Kimi, GLM, MiniMax displace Meta and Mistral so completely the
ratio inverts by two orders of magnitude — and it reproduces independently in all
three surfaces, which almost nothing else does. Price as the recurring frame: *8%
of Claude Sonnet's price*, *11% of its cost*, *10× cheaper*. Meta's decline dated
to October 2024, six months before the Llama 4 release everyone blames. Mistral
raising $1.7B and beating DeepSeek in human evals in the same month its coverage
hit zero.
**Payoff:** ceasing to be news and ceasing to be good are different events.

**9. Containment** *(2026)*
*What happens after the capability race?*
Security moves from periphery to centre. `distillation` stops being a training
technique and becomes a legal accusation — the word's nearest neighbours shift
from `unet, dare, imagenet` to `attacks, copyrighted, laws`. Agent sandboxing,
prompt injection, supply-chain risk. A defense and national-security topic rising
sevenfold. The BASI Jailbreaking community appearing in November 2025 and
accumulating 95,000 messages in five months — the turn showing up as community
formation before it shows up as coverage.

> **Interlude II — The day the corpus changed shape underneath me**
> Every density number I had computed was per 10,000 words of a document whose
> source composition had inverted: 96% Discord transcript in 2024, 0% by 2026.
> Three of my four largest findings were exposed at once. Fixing it produced the
> book's central idea, which is the only reason this interlude is not simply an
> apology.

## Part III — What it means  *(~9,000 words)*

**10. How ideas die**
*Retrieval fell 99%. So did things that failed. How do you tell?*
Consolidates chapter 4's diagnostic across the whole archive. Retrieval, reasoning
and multimodality all peaked and fell and all three won. The LangChain/LlamaIndex
split as the sharpest case: the category collapsed while one of its two flagship
frameworks reached its all-time high coverage. Category death and vendor death are
different events.

**11. How the field keeps score**
*Which benchmarks are worth believing, and for how long?*
Benchmarks have lifespans, and the archive dates them. GSM8K, HumanEval and
AlpacaEval dead within months. MATH saturating at 84% and retiring. AIME arriving
in January 2025 *with* the reasoning models. Terminal-Bench arriving in 2026 *with*
the harnesses. SWE-bench spanning the entire corpus. FrontierMath at 31%, still
unsaturated.
**Payoff:** a benchmark set is a trailing indicator of what models can newly do,
and saturation kills a benchmark within about two quarters of everyone clearing it.

**12. When words change meaning**
*Is `agent` in your 2026 dashboard the same `agent` you started counting in 2024?*
Referent drift, and why it is a practical hazard rather than a curiosity. `harness`,
`skills`, `prompt` (engineering → injection), `distillation`, `agentic`. Any
keyword series spanning these dates is aggregating two concepts and reporting one
trend. This is the chapter most directly useful to an engineer maintaining an eval
suite, a monitoring dashboard or a retrieval corpus.

**13. What people actually ran**
*If announcements are unreliable, what does the ground truth look like?*
The practitioner stack. `llama.cpp` as the only tool that grows across the whole
window. Quantization rising in practice while falling in announcements — the
sharpest single split in the book. Consumer GPUs outnumbering datacenter GPUs two
to three times throughout. CPU offload climbing as models outgrew consumer VRAM.
And the busiest community in the entire archive: Unsloth, a fine-tuning toolchain,
at 302,248 messages, during the period when announcement coverage of fine-tuning
fell 90%.

**14. The half-life of a dependency**
*You are about to build on a model. How long will it stay relevant?*
Survival analysis, explained without jargon. The median model holds the field's
attention for 137 days; the median *family* for 254. Why censoring matters and why
the naive average misleads. The Chinese-lab cohort looking short-lived at the tag
level and turning out to be the longest-lived at family level — a worked example of
a measurement artifact reversing a conclusion.

> **Interlude III — The four things I got wrong**
> Consolidated: the templated titles, the inverted source composition, a Discord
> artifact I mistook for a field-wide vocabulary shift, and a fivefold
> "fragmentation" that turned out to be the newsletter sampling more accounts.
> Every one came from measuring a field without reading it.

## Part IV — Reading forwards  *(~4,000 words)*

**15. The unit of observation**
*Why did none of this get caught by better statistics?*
The transferable lesson, generalised past AI. Six ways to measure the wrong thing
confidently: presence saturates, counts track length, titles track framing, KL
tracks format, co-occurrence tracks frequency, diversity tracks sampling breadth.
Thirteen methods, several sophisticated, none of which surfaced any of it. Reading
a hundred documents did.

**16. How to read a field**
*What do you do on Monday?*
The practical close. A short method the reader can actually run: find the surfaces,
check what the fields contain, prefer two partial views you can cross-check over
one comprehensive view you cannot, watch for the peak, and treat declining coverage
as a question rather than an answer. Ends by pointing at whatever is next — the
book's subject is AI, but its method outlives it.

## Back matter
- **The corpus** — provenance, reconstruction, schema, how to get it
- **Methods** — the thirteen methods, each with citation, estimand and known failure
- **Numbers** — the full data tables behind every figure
- **Reproducing this book** — one command per figure

---

# Craft decisions worth flagging

**Every technical concept is introduced where the field introduced it.** MoE lands
in chapter 3, test-time compute in chapter 5, harnesses in chapter 7. A general
software engineer reads them in the order the field encountered them, which is the
order that makes them easiest to understand — and it means the book teaches the
subject rather than assuming it.

**The interludes are not appendices.** They sit at part boundaries and are part of
the argument. A book that runs thirteen analyses and admits nothing is not
credible; a book that quarantines its errors in a validity section is not honest
either.

**Figures are illustrations, not evidence.** In the report they carry the proof.
In the book they should be readable in three seconds and make one point each. That
means fewer, larger, more annotated — roughly 20 across the book rather than 18 in
9,000 words. Several report figures become tables or prose.

**Scenes get room.** Chapter 6 is one week. That is a deliberate change of pace and
the book needs it around the two-thirds mark of Part II.

# Scope

~30,000 words across 16 chapters and 3 interludes — roughly three times the
report. Realistically several sessions of writing.

**Format:** a multi-page site — contents page plus one page per chapter, with
previous/next navigation and a persistent chapter list. GitHub Pages already
builds from `report/`, so the same generator can emit `site/` as a book instead of
a single page. A single-page reader's edition can also be produced for the
artifact.

**Reuse:** roughly 60% of the report's prose survives into the book, mostly
redistributed and re-voiced. The new writing is the narrative connective tissue,
the teaching passages, the scenes, and Part IV.
