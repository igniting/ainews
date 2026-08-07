# Semantic drift

Diachronic word embeddings with orthogonal Procrustes alignment
(Hamilton, Leskovec & Jurafsky 2016), via `analysis/methods/semantic_drift.py`.

One word2vec model per half-year, trained on this corpus rather than downloaded —
15.3M words of domain text gives better vectors for this vocabulary than a general
pretrained model would. Independent embedding spaces are only defined up to
rotation, so they are aligned before comparison.

**Drift** is cosine distance between a word's 2024H1 and 2026H1 vectors.
Median drift across 4,183 shared words is **0.313** — use that as
the baseline for 'this word did not really move'.

The neighbour lists are the actual finding; the drift score only ranks them.

## Watch list: 2024H1 → 2026H1

| Word | Drift | Nearest in 2024H1 | Nearest in 2026H1 |
|---|---|---|---|
| `harness` | **0.439** | lm-evaluation-harness, eval, lm-eval, megatron-deepspeed, deadlock, helm | orchestration, harnesses, ux, dbreunig, hwchase17, abstraction |
| `agentic` | **0.371** | empowers, augmenting, agents., production-ready, devika, low-code | long-horizon, tool-use, multi-step, computer-use, swe, browsing |
| `agents` | 0.289 | agents., agent, empowers, sleeper, profound, react | agent, agents., skills, ops, cognition, multi-agent |
| `prompt` | **0.363** | prompts, engineering, crafting, promptfoo, prompts., prompttools | injection, prompt., desired, adherence, drafting, caching |
| `skills` | **0.590** | skills., goals, coding., experiences., abilities, continuously | middleware, reusable, execution., ide, filesystem, decomposition |
| `context` | 0.170 | window, length, contexts, context., yarn, lengths | window, length, context., cache, kv, batch |
| `reasoning` | 0.285 | multi-hop, knowledge., chain-of-thought, abilities, context-aware, reasoning. | multilingual, reasoning., spatial, instruction-following, instruction, configurable |
| `distillation` | **0.448** | unet, ties, dare, neuron, u-net, imagenet | attacks, industrial-scale, copyrighted, teacher, legitimate, laws |
| `safety` | 0.272 | measures, disclosure, copyright, legal, risk, regulatory | measures, concerns., political, mass, surveillance, misuse |
| `open` | 0.249 | source, open-source, sourcing, whisper., huggingchat, powering | open-weight, open-weights, permissive, foundation, closed, open-model |

## Largest drift overall (2024H1 → 2026H1)

Ranked over all shared vocabulary. Words that changed company, not just frequency.

| Word | Drift | Nearest in 2024H1 | Nearest in 2026H1 |
|---|---|---|---|
| `r1` | 0.786 | rabbit, aravsrinivas, purchase, srinivas, advertised | v3, deepseek-v4, ernie, v3.2, m2.7 |
| `horizon` | 0.782 | celebrates, excitedly, teased, imminent, tease | metr, jumps, polynoamial, flat, variance |
| `side` | 0.779 | lighter, events., ai-related, direction., keep | dive, liteparse, llamaindex, philschmid, clip |
| `main` | 0.723 | src, master, readme.md, helpers, w2v2 | key, differentiator, unresolved, set., caveat |
| `stability` | 0.718 | japan, mostaque, stability.ai, midjourney, emad | scalability, robustness, techniques., applicability, specifying |
| `thinking` | 0.717 | hide, fight, lie, trees, mad | effort, disable, xhigh, lite, haiku |
| `lighter` | 0.713 | events., reflections, industries, vibrant, cryptocurrency | devstral, b-a10b, favored, q1, balanced |
| `spark` | 0.708 | sparks, surrounding, quandaries, unfolds, stir | dgx, ultra, muse, gb10, m3 |
| `meeting` | 0.698 | attending, schedule, session., attendance, event. | samsung, advocating, raspberry, food, showcased |
| `description` | 0.680 | found, no, gemma-2b-it-gguf, v0.10.13, kquant03 | diagram, artistic, text., animation, voting |
| `epoch` | 0.677 | trainable, epochs, digit, decreasing, dropout | frontiermath, arc-agi-3, prize, metr, epochairesearch |
| `positions` | 0.674 | implicitly, out-of-distribution, ignore, texts., singular | positioned, positioning, leader, competitor, presented |
| `class` | 0.671 | whitespace-normal, pre, type, serialization, name | gx10, gb10, lt, totaling, geforce |
| `effort` | 0.667 | efforts, encourage, volunteer, readiness, reinforcing | xhigh, disable, adaptive, thinking, extended |
| `following` | 0.664 | submitting, matter., conflicting, continuation, timeline | instruction, strength, cutoff, imagine, physics |
| `contribute` | 0.659 | deepseek-moe, irl., lwm, tinygrad-notes, mesozoic-egg | encourage, abilities, evolve, ones., hinder |
| `channel` | 0.655 | channel., channels., etiquette, redirected, off-topic | swap, persistence, delegation, comms, loop. |
| `surfaced` | 0.648 | quandaries, centered, arose, surrounding, arises | follow-on, writeup, zhihufrontier, swyx, cwolferesearch |
| `oobabooga` | 0.642 | text-generation-webui, tabbyapi, koboldcpp, webui, llama-cpp-python | machinelearning, singularity, stablediffusion, chatgptcoding, aivideo |
| `hits` | 0.638 | debuts, strikes, celebrating, drops, ignites | cached, ttft, bytes, min, tg |
| `color` | 0.637 | font-family, underline, rgb, symbol, segoe | depicted, anime, realism., animated, light |
| `stable` | 0.636 | diffusion, xl, civitai, sd3, cascade | regular, usable, scoped, smarter, lossless |
| `discover` | 0.635 | gif, gifs, oh, click, smile | aim, databases, compress, groups, conflicts |
| `tag` | 0.633 | redirect, smol, astraliteheart, social, checked | exposed, revealed, boris, sees, wrapper |
| `conversations` | 0.632 | discussions, conversation, debates, dialogue, discourse | sessions., cot, sleep, retrieve, iteratively |

## Trajectory of key terms across all eras

Nearest neighbours era by era — the clearest way to watch a concept move.

**`harness`**

- 2024H1: lm-evaluation-harness, eval, lm-eval, megatron-deepspeed, deadlock, helm, lm-eval-harness
- 2025H2: harnesses, scaffolds, durable, long-running, orchestrating, matter, sandbox
- 2026H1: orchestration, harnesses, ux, dbreunig, hwchase17, abstraction, model-agnostic

**`agentic`**

- 2024H1: empowers, augmenting, agents., production-ready, devika, low-code, llm-based
- 2024H2: workflows, multi-agent, langgraph, omarsar0, jerryjliu0, building, retrieval-augmented
- 2025H1: multi-agent, llm-based, ai-assisted, end-to-end, multi-step, debugging, automating
- 2025H2: coding, vibe, gui, jerryjliu0, swe, rag, orchestrating
- 2026H1: long-horizon, tool-use, multi-step, computer-use, swe, browsing, sustained

**`agents`**

- 2024H1: agents., agent, empowers, sleeper, profound, react, nextjs
- 2024H2: langchainai, langgraph, qdrant, agentic, agent, rag, assistants
- 2025H1: agents., computer, automate, building, swarm, langsmith, multi-agent
- 2025H2: agents., subagents, scaffolds, skills, long-running, langgraph, orchestration
- 2026H1: agent, agents., skills, ops, cognition, multi-agent, devin

**`prompt`**

- 2024H1: prompts, engineering, crafting, promptfoo, prompts., prompttools, darthgustav.
- 2024H2: prompts, system, instructions, proposing, multi-turn, experience., contextual
- 2025H1: adherence, prompts, scene, extended, structure, rendering, photorealistic
- 2025H2: prompts, templates, adherence, injection, structure, guidance, directory
- 2026H1: injection, prompt., desired, adherence, drafting, caching, noise

**`skills`**

- 2024H1: skills., goals, coding., experiences., abilities, continuously, candidates
- 2024H2: workflows., flow, enhancement, pdfs, precise, agents., voices
- 2025H1: cognitive, domain-specific, problems., principles, validation, fundamental, oversight
- 2025H2: agents., review, long-running, reusable, subagents, agent., scaffolds
- 2026H1: middleware, reusable, execution., ide, filesystem, decomposition, langchain

**`context`**

- 2024H1: window, length, contexts, context., yarn, lengths, self-extend
- 2024H2: window, length, lengths, token, long, windows, default
- 2025H1: window, length, maximum, token, context., query, lengths
- 2025H2: window, sliding, memory, contexts, token, window., tokens.
- 2026H1: window, length, context., cache, kv, batch, contexts

**`reasoning`**

- 2024H1: multi-hop, knowledge., chain-of-thought, abilities, context-aware, reasoning., planning
- 2024H2: mathematical, abilities, math, chain-of-thought, cot, mathematics, medical
- 2025H1: chain-of-thought, generalization, cot, math, excelling, translation, mathematical
- 2025H2: cot, non-reasoning, scoring, sota, chain-of-thought, reasoning., long-context
- 2026H1: multilingual, reasoning., spatial, instruction-following, instruction, configurable, math

**`distillation`**

- 2024H1: unet, ties, dare, neuron, u-net, imagenet, progressive
- 2024H2: entirely, scratch, mechanism, built-in, raw, reward, post-training
- 2025H1: post-training, pretraining, cwolferesearch, recipe, generalization, combination, zero
- 2025H2: lms, pretrain, qat, inference-time, ppo, corpus, frozen
- 2026H1: attacks, industrial-scale, copyrighted, teacher, legitimate, laws, accused

