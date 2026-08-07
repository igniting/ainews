# Semantic drift

Diachronic word embeddings with orthogonal Procrustes alignment
(Hamilton, Leskovec & Jurafsky 2016), via `analysis/methods/semantic_drift.py`.

One word2vec model per half-year, trained on this corpus rather than downloaded —
15.3M words of domain text gives better vectors for this vocabulary than a general
pretrained model would. Independent embedding spaces are only defined up to
rotation, so they are aligned before comparison.

**Drift** is cosine distance between a word's 2024H1 and 2026H1 vectors.
Median drift across 3,455 shared words is **0.365** — use that as
the baseline for 'this word did not really move'.

The neighbour lists are the actual finding; the drift score only ranks them.

## Watch list: 2024H1 → 2026H1

| Word | Drift | Nearest in 2024H1 | Nearest in 2026H1 |
|---|---|---|---|
| `agent` | 0.321 | agents, agent., agentic, flows, langgraph, react | multi-agent, agents, cognition, langsmith, agentic, orchestrator |
| `agents` | **0.425** | agent, agents., flows, langgraph, multi-agent, simulated | agents., agent, assistants, multi-agent, sandboxes, devin |
| `agentic` | **0.375** | agent, agents, jerryjliu0, retrieval-augmented, production-ready, multi-agent | long-horizon, multi-step, computer-use, swe, agent, long-running |
| `reasoning` | 0.310 | reasoning., context-aware, logical, abilities., chain-of-thought, linguistic | reasoning., multilingual, spatial, thinking, cot, coherence |
| `context` | 0.269 | window, length, contexts, lengths, context., length. | window, length, context., contexts, rot, kv |
| `memory` | 0.250 | memory., allocation, vram, peak, disk, bandwidth | memory., bandwidth, storage, kv, persistent, stores |
| `harness` | **0.568** | lm-evaluation-harness, eval, lm-eval-harness, lm-eval, evaluation, hailey | harnesses, vtrivedy10, orchestration, hwchase17, primitives, ux |
| `skills` | **0.524** | skill, knowledge., rewards, expertise, proficiency, collaborating | replit, harnesses, reusable, skill.md, primitives, langsmith |
| `tools` | 0.312 | tools., frameworks, apis, tool, integrations, workflows | assistants, tools., agents., workflows, apps, clients |
| `scaling` | **0.395** | laws, extrapolation, chinchilla, properties, scales, empirical | laws, continual, theory, scales, sparsity, gradient |
| `open` | 0.337 | source, open-source, oss, sourcing, powering, open-sourcing | open-weight, source, open-source, closed, open-weights, proprietary |
| `cheap` | 0.360 | expensive, pcs, super, pretty, affordable, h100s | viable, expensive, cost-effective, money, low-cost, usd |
| `fast` | **0.392** | memory-efficient, turboderp, fourier, cheap, dao-ailab, exllamav2 | cheap, lands, upgrades, easy, faster, default |
| `benchmark` | 0.317 | eq-bench, benchmarks, mmlu, benchmarking, needle, hellaswag | scores, benchmarks, methodology, verified, swe-bench, suite |
| `distillation` | **0.514** | masked, unsupervised, contrastive, svd, positional, bidirectional | attacks, persona, mhc, distill, innovations, continual |
| `alignment` | **0.452** | lab, aligning, general-chat, forum, rlhf, direction | similarity, safety, geometry, refusal, theory, regulatory |
| `safety` | 0.340 | regulation, risk, responsible, sb, california, bill | safeguards, measures, ethics, cyber, resistance, alignment |
| `inference` | 0.280 | inference., inferencing, turboderp, exllamav2, deployment., serving | serving, inference., multi-gpu, concurrency, ssd, distributed |
| `training` | 0.259 | training., pretraining, pretraining., fine-tuning, finetuning, train | pretraining, post-training, pre-training, training., fine-tuning, sft |
| `prompt` | 0.266 | prompts, prompts., engineering, meta-prompting, prompt., prompting | prompts, injection, prompt., jailbreaks, fortress, eni |

## Largest drift overall (2024H1 → 2026H1)

Ranked over all shared vocabulary. Words that changed company, not just frequency.

| Word | Drift | Nearest in 2024H1 | Nearest in 2026H1 |
|---|---|---|---|
| `r1` | 0.921 | rabbit, shipping, purchase, ok.alex, o1 | mimo, v3.2, nemotron, vl, stepfun |
| `ibm` | 0.802 | granite, deepseek-v2, medusa, bilingual, bagel | employees, dod, corporate, leadership, technological |
| `axis` | 0.770 | dequantization, sum, fp32, integer, int4 | engram, persona, self-improvement, continual, sakana |
| `slide` | 0.737 | beautiful, elicit, apps., builder, children | turbo, omni, nano, table, klein |
| `description` | 0.722 | found, no, href, colaboratory, li | composition, precise, diagram, detail, descriptions |
| `stability` | 0.715 | emad, stability.ai, stable, stabilityai, membership | reliability., reliability, robustness, instability, oom |
| `replicate` | 0.715 | predibase, modal, fireworks, braintrust, credits | adapt, them., analyze, prioritize, produce |
| `falls` | 0.713 | priorities., believe, priorities, the..., motivation | flat, woes, glitches, troubles, crashes |
| `oobabooga` | 0.710 | text-generation-webui, open-webui, exl2, awq, llama-cpp-python | machinelearning, stablediffusion, singularity, chatgptcoding, aivideo |
| `magic` | 0.709 | powers, entertainment, wars, universe, adventure | string, thing, instead., referring, stuff |
| `codes` | 0.708 | client, surya, conversions, urls, typing | accidentally, telegram, banned, opening, refund |
| `activity` | 0.707 | surge, group., had, hacker, issued | presents, depicts, qwen3.6-35b-a3b, newly, goes |
| `stage` | 0.706 | panel, center, july, event, monday | shape, computation, intermediate, cold, scheduler |
| `class` | 0.705 | print, name, none, div, invoke | ryzen, fitting, m4, high-performance, halo |
| `shipping` | 0.704 | purchase, o1, r1, manufacturing, international | ainews, soon., thanks, form, ship |
| `side` | 0.703 | lighter, touch, humor, hands, light-hearted | kimmonismus, zhihufrontier, philschmid, googledeepmind, reality |
| `battle` | 0.700 | sentience, challenged, showdown, heated, giants | groups, veo, lmarena, mode, exclusively |
| `third` | 0.694 | n..., february, weekend, aiatmeta, tomorrow | another, criticizes, situation, expresses, party |
| `master` | 0.683 | mobiusml, pytorch-labs, mesozoic-egg, wip, tinygrad-notes | university, full-stack, lessons, distributed, nccl |
| `effort` | 0.682 | efforts, initiative, efforts., contributions, aims | xhigh, medium, levels, depth, thinking |
| `solar` | 0.680 | x7b, yi, ssm-transformer, b., stablelm | merits, practicality, purchase, savings, rising |
| `distribution` | 0.673 | rounding, distributions, probability, decay, divergence | signals, infra, etc., vendors, theturingpost |
| `deepseek` | 0.671 | coder, deepseek-v2, codestral, qwen, falcon | v4, v3.2, mhc, r1, anticipated |
| `seed` | 0.670 | seeds, epoch, token., rounding, element | open-model, enters, lab, qwen3.5-397b-a17b, movement |
| `comment` | 0.670 | singularity., llmdevs, artificialinteligence, crawling, stablediffusion | commenter, humorously, technology., situation, critiques |

## Trajectory of key terms across all eras

Nearest neighbours era by era — the clearest way to watch a concept move.

**`agent`**

- 2024H1: agents, agent., agentic, flows, langgraph, react, multi-agent
- 2024H2: agents, orchestration, langchainai, langgraph, react, llamaindex., composio
- 2025H1: agents, multi-agent, agent., langgraph, mastra, agents., handoff
- 2025H2: agents, agentic, agents., agent., langchainai, orchestrator, langsmith
- 2026H1: multi-agent, agents, cognition, langsmith, agentic, orchestrator, sandboxes

**`agents`**

- 2024H1: agent, agents., flows, langgraph, multi-agent, simulated, agentic
- 2024H2: agent, mooc-questions, agents., mooc, composio, assistants, swe
- 2025H1: agent, agents., multi-agent, mooc-lecture-discussion, mooc-questions, bots, agent.
- 2025H2: agents., agent, multi-agent, slack, autonomously, langgraph, assistants
- 2026H1: agents., agent, assistants, multi-agent, sandboxes, devin, orchestrator

**`agentic`**

- 2024H1: agent, agents, jerryjliu0, retrieval-augmented, production-ready, multi-agent, r2r
- 2024H2: event-driven, orchestration, llm-powered, agent, multi-agent, langchainai, langgraph
- 2025H1: jerryjliu0, rag, autonomous, retrieval-augmented, multi-agent, agents, llm-powered
- 2025H2: agent, swe, orchestrator, langchainai, autonomous, commerce, multi-agent
- 2026H1: long-horizon, multi-step, computer-use, swe, agent, long-running, multilingual

**`reasoning`**

- 2024H1: reasoning., context-aware, logical, abilities., chain-of-thought, linguistic, abilities
- 2024H2: reasoning., problem-solving, chain-of-thought, abilities, instruction-following, cot, mathematical
- 2025H1: reasoning., thinking, cot, abilities, math, mathematical, problem-solving
- 2025H2: thinking, chain-of-thought, reasoning., reasoner, cot, non-reasoning, multilingual
- 2026H1: reasoning., multilingual, spatial, thinking, cot, coherence, multi-step

**`context`**

- 2024H1: window, length, contexts, lengths, context., length., window.
- 2024H2: window, length, lengths, contexts, lengths., length., context.
- 2025H1: window, contexts, window., context., length., sequence, sliding
- 2025H2: window, context., window., contexts, sliding, length, contextual
- 2026H1: window, length, context., contexts, rot, kv, compact

**`memory`**

- 2024H1: memory., allocation, vram, peak, disk, bandwidth, gbps
- 2024H2: ram, memory., footprint, vram, oom, bandwidth, overhead.
- 2025H1: memory., bandwidth, coalescing, registers, ram., vram, bottlenecks
- 2025H2: memory., accesses, bandwidth, footprint, vram, completeness, nvme
- 2026H1: memory., bandwidth, storage, kv, persistent, stores, overhead

**`harness`**

- 2024H1: lm-evaluation-harness, eval, lm-eval-harness, lm-eval, evaluation, hailey, schoelkopf
- 2024H2: eval, lm-evaluation-harness, lm-eval, lm-eval-harness, eleutherai, lm, pruned
- 2025H1: eval, gsm8k, evaluation, methodology, gaia, evaluate, evaluations
- 2025H2: eval, standardized, lm-evaluation-harness, evals, evaluation, reproducible, metric
- 2026H1: harnesses, vtrivedy10, orchestration, hwchase17, primitives, ux, sandboxing

**`skills`**

- 2024H1: skill, knowledge., rewards, expertise, proficiency, collaborating, abilities
- 2024H2: skills., expertise, fundamentals, skill, proficiency, knowledge., vision.
- 2025H1: skills., proficiency, abilities., abilities, expertise, principles, knowledge.
- 2025H2: skills., coders, senior, hands-on, dl, problem-solving, interviews
- 2026H1: replit, harnesses, reusable, skill.md, primitives, langsmith, agents.

