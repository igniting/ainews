# What reading the issues found that the methods did not

Two rounds of actually reading the articles — the last 30 days, then a stratified
sweep across the corpus. Both rounds found errors and artifacts that eleven
automated methods had missed, because every one of them measured fields nobody
had looked at.

---

## 1. The corpus inverted its own composition — the most serious confound found

Each issue declares its sampling effort in its header line. Extracting that from
571 issues:

| Period | Subreddits checked | Twitter accounts | Discord servers |
|---|---|---|---|
| 2024H1 | 7 | 384 | 30 |
| 2025H1 | 7 | 433 | 29 |
| 2025H2 | 12 | 544 | 24 |
| 2026H1 | 12 | 544 | **0** |

And the resulting share of each issue's words:

| Period | Twitter | Reddit | Discord |
|---|---|---|---|
| 2024H1 | 2% | 2% | **96%** |
| 2025H2 | 5% | 15% | 79% |
| 2026H1 | 23% | **61%** | **0%** |

**Every density figure in this repo was computed per 10,000 words of a document
whose source composition inverted.** A topic living in Discord help channels —
fine-tuning, local inference, quantization — declines mechanically once Discord
sampling stops. A topic living on Twitter — model launches — rises mechanically.
That threatens the three largest findings simultaneously.

### The control, and the result

`sections.py` measures density *inside* one recap section, holding the source
fixed. Twitter and Reddit are present throughout; Discord is not.

**All six headline findings survive.** Within the Twitter recap only, per 10⁴ words:

| | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 | 2026H2 |
|---|---|---|---|---|---|---|
| China bloc | 8.4 | 13.3 | 48.5 | 51.1 | 46.7 | **72.0** |
| Meta+Mistral | 26.9 | 32.9 | 14.0 | 7.9 | 2.9 | **1.3** |
| agentic | 12.7 | 38.8 | 67.4 | 99.0 | **138.5** | 101.6 |
| fine-tuning | 34.9 | 12.0 | 8.0 | 10.3 | 4.9 | **1.9** |
| RAG | 22.5 | 21.0 | 5.6 | 5.6 | 2.6 | **0.2** |
| reasoning | 7.0 | 23.4 | **40.2** | 35.8 | 17.2 | 14.3 |

The China rise and the Meta/Mistral fall reproduce independently in *both*
sections, which makes them the most robust results in the study.

---

## 2. The confound turned into a better finding: announcement-space vs practitioner-space

Twitter carries launches and claims. Reddit carries what people are running.
Splitting them measures the gap between the two.

| Pattern | Twitter change | Reddit change |
|---|---|---|
| `agentic` | **8.0×** | 2.0× |
| `fine-tuning` | **0.1×** (−90%) | 0.4× (−60%) |
| `RAG` | 0.0× | 0.2× |
| China bloc | 8.6× | 15.3× |
| `harness` | 17.9× | 16.8× |

Two readings that the whole-corpus numbers hid:

- **Agents are far more an announcement phenomenon than a practitioner one.** 8×
  on Twitter against 2× on Reddit. The whole-corpus figure of 7.5× was closer to
  the announcement number because Twitter's share of the text grew.
- **Practitioners kept fine-tuning after the discourse stopped.** Twitter drops
  90%, Reddit only 60%, and Reddit's `fine-tuning` density *rises* again in
  2026H2 (4.9 → 6.9). The technique did not die; its news value did.

The two surfaces agree almost exactly on `harness` (17.9× vs 16.8×) and on the
China bloc, which is what a genuine field-wide shift looks like as opposed to a
narrative one.

---

## 3. The lede is a dated one-line editorial thesis, and I never read it

690 issues carry an opening lede. **234 of them follow the form "X is all you
need"** — a compressed, human-written, dated call on what mattered:

| Date | Lede |
|---|---|
| 2024-09-12 | *Test-time reasoning is all you need.* |
| 2024-11-25 | *`claude_desktop_config.json` is all you need.* |
| 2024-12-23 | *o3 is all you need.* |
| 2025-01-27 | *DeepSeek is all you need.* |
| 2025-03-26 | *MCP is all you need.* |
| 2025-05-15 | *Agent Harnesses are all you need.* |
| 2025-06-25 | *Finely crafted context is all you need.* |
| 2025-10-29 | *Agentic coding is all you need.* |
| 2026-03-10 | *World Models are all you need.* |

This is an independent, human-authored ground truth to validate the automated
findings against, and the agreement is close:

| Automated result | Method-derived date | Lede date |
|---|---|---|
| MCP density peak | 2025-03 → 2025-07 (PELT) | **2025-03-26** |
| DeepSeek burst | 2025-W04 → W10 (Kleinberg) | **2025-01-27** |
| `harness` referent drift | between 2024H1 and 2026H1 (embeddings) | **2025-05-15** |
| Reasoning peak | 2025H1 (density) | **2024-09-12** |

The reasoning row is the interesting disagreement: the editor called test-time
reasoning on the day o1 shipped, roughly **two quarters before** density peaked.
The thesis leads the volume, which is what you would expect and what a
volume-only method cannot see.

### The corpus has three editorial layers, not one

Reading `25-05-15-alphaevolve.md` made the structure obvious: its lede is *"Agent
Harnesses are all you need"* while its filename and story are AlphaEvolve. So:

1. **Lede** — the editor's *thesis* (interpretation)
2. **Title / filename slug** — the day's *event*
3. **Body** — the source recaps

Every analysis in this repo used layers 2 and 3. Layer 1 is the most compressed,
the most human, and the only one that states an interpretation.

---

## 4. Title and lede templating (carried over from the first reading pass)

"not much happened today" is the title of 0% of 2023 issues, 18% of 2024, 42% of
2025 and **68% of 2026**, and it is boilerplate — the Claude Opus 5, GPT-5.6,
Qwen 3.8 Max and Kimi K3 launch issues all carry it, and all 23 issues in the
final month open with the lede "**a quiet day.**"

Conditioning on descriptive titles changes the headline-share result materially:
OpenAI runs 29% → 18% rather than 18% → 6%, and the Anthropic and China-bloc
rises are both stronger than first reported.

---

## 5. What this changes

| Claim | Status after reading |
|---|---|
| China bloc rise | **Strengthened** — reproduces in both sections independently |
| Meta + Mistral fall | **Strengthened** — same |
| Agents 4% → 86% | **Qualified** — 8× in announcement-space, 2× in practitioner-space |
| Fine-tuning collapse | **Qualified** — practitioners kept doing it; the news value fell |
| RAG collapse | Confirmed in both sections |
| Reasoning absorbed | Confirmed; the thesis led the volume by ~2 quarters |
| OpenAI headline decline | **Mostly artifact** — title templating, not fragmentation |
| "Quiet day" frequency | **Meaningless** — boilerplate, not a verdict |

## 6. The general lesson

Three rounds of correction, and every single error came from measuring a field
without reading it:

1. Titles were treated as verdicts — they became templates.
2. Density was normalized by words — the words changed source.
3. The lede was discarded as boilerplate — it is the most informative field in
   the corpus.

Eleven statistical methods, several of them sophisticated, none of which could
have found any of this. The failure mode is not the algorithm; it is measuring a
field whose semantics you have not checked. Reading a stratified sample of the
raw documents should precede the first line of analysis code, not follow the
eleventh method.
