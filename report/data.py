"""Measured series for the report figures. Every value traces to a file in analysis/."""

PERIODS = ["2023H2", "2024H1", "2024H2", "2025H1", "2025H2", "2026H1", "2026H2"]
P6 = PERIODS[1:]  # sections.py has no 2023H2 (no section headers that early)

# analysis/sections.md — share of issue words by source section (median %)
COMPOSITION = {
    "Discord": [96, 92, 86, 79, 0, 0],
    "Reddit":  [2, 6, 9, 15, 61, 70],
    "Twitter": [2, 2, 4, 5, 23, 28],
}

# analysis/sections.md — mentions per 10k words WITHIN a fixed recap section
TWITTER = {
    "agentic":      [12.7, 38.8, 67.4, 99.0, 138.5, 101.6],
    "China bloc":   [8.4, 13.3, 48.5, 51.1, 46.7, 72.0],
    "Meta+Mistral": [26.9, 32.9, 14.0, 7.9, 2.9, 1.3],
    "fine-tuning":  [34.9, 12.0, 8.0, 10.3, 4.9, 1.9],
    "RAG":          [22.5, 21.0, 5.6, 5.6, 2.6, 0.2],
    "reasoning":    [7.0, 23.4, 40.2, 35.8, 17.2, 14.3],
    "harness":      [1.8, 0.0, 0.2, 4.1, 22.6, 31.8],
    "MCP":          [0.0, 1.1, 10.1, 12.1, 8.1, 5.6],
}
REDDIT = {
    "agentic":      [15.3, 5.0, 11.4, 12.7, 18.5, 31.2],
    "China bloc":   [6.4, 31.3, 49.4, 36.9, 57.1, 97.8],
    "Meta+Mistral": [65.5, 43.4, 12.6, 6.3, 4.0, 2.4],
    "fine-tuning":  [19.2, 15.7, 11.0, 11.1, 4.9, 6.9],
    "RAG":          [12.5, 2.4, 2.3, 1.4, 1.4, 2.8],
    "reasoning":    [7.0, 18.0, 19.5, 11.0, 9.6, 9.8],
    "harness":      [0.3, 0.0, 0.2, 0.3, 1.4, 5.4],
    "MCP":          [0.0, 1.1, 2.3, 1.4, 2.3, 2.2],
}
# fold-change 2024H1 -> 2026H2 within each section
GAP = [
    ("agentic",      8.0, 2.0, "narrative"),
    ("harness",     17.9, 16.8, "field-wide"),
    ("China bloc",   8.6, 15.3, "field-wide"),
    ("reasoning",    2.0, 1.4, "mixed"),
    ("fine-tuning",  0.1, 0.4, "narrative"),
    ("RAG",          0.02, 0.2, "field-wide"),
]

# analysis/methods/changepoints.py --monthly, Meta Llama
LLAMA_MONTHLY = [
    ("2024-10", 17.2), ("2024-11", 11.7), ("2024-12", 12.9), ("2025-01", 8.0),
    ("2025-02", 6.9), ("2025-03", 5.9), ("2025-04", 19.7), ("2025-05", 4.7),
    ("2025-06", 4.0), ("2025-07", 4.2), ("2025-08", 2.0), ("2025-09", 1.7),
    ("2025-10", 2.4), ("2025-11", 1.7), ("2025-12", 1.6),
]
LLAMA_BREAKS = ["2024-10", "2025-08"]

# analysis/claims.md
CONTEXT_MEDIAN = [("2023H2", 24), ("2024H1", 128), ("2024H2", 128), ("2025H1", 100),
                  ("2025H2", 256), ("2026H1", 258), ("2026H2", 1000)]  # thousands of tokens
PRICE = [("2024H1", 0.42, 0.10, 22), ("2024H2", 4.00, 0.11, 26), ("2025H1", 8.00, 0.42, 35),
         ("2025H2", 2.50, 0.45, 25), ("2026H1", 3.00, 0.13, 28), ("2026H2", 3.00, 0.29, 15)]

# analysis/bradley-terry.md — (family, strength, comparisons)
BT = [("glm", 3.19, 36), ("kimi", 2.27, 21), ("qwen3", 1.67, 53), ("gemma", 1.61, 53),
      ("deepseek-v3", 1.45, 22), ("fable", 1.36, 22), ("qwen", 1.33, 94), ("gpt-5", 0.86, 84),
      ("mistral", 0.81, 107), ("phi", 0.79, 26), ("opus", 0.79, 102), ("grok", 0.76, 54),
      ("gemini", 0.70, 129), ("llama", 0.62, 91), ("claude", 0.46, 200),
      ("openai-o-series", 0.33, 42), ("chatgpt", 0.33, 28), ("gpt-3.5", 0.28, 34)]
BT_BIAS = [("3–7", 13, 0.68), ("8–15", 6, 0.55), ("16–40", 8, 0.56), ("41+", 13, 0.49)]

# analysis/survival.md — Kaplan-Meier medians
SURVIVAL = [("All models", 255, 217, 137), ("US frontier labs", 161, 141, 175),
            ("Chinese labs", 49, 40, 85), ("Open-weights families", 100, 90, 117)]

# analysis/methods/changepoints.py --format
REGIMES = [("2023-12-06", "2024-03-11", 75, "alpha"),
           ("2024-03-12", "2024-05-17", 50, "expansion"),
           ("2024-05-20", "2026-03-10", 460, "stable core"),
           ("2026-03-11", "2026-08-06", 105, "post-Discord")]

# Declared sampling effort, from each issue's own header line
SAMPLING = [("2024H1", 7, 384, 30), ("2024H2", 7, 433, 30), ("2025H1", 7, 433, 29),
            ("2025H2", 12, 544, 24), ("2026H1", 12, 544, 0), ("2026H2", 12, 544, 0)]

# analysis/semantic-drift.md, genre-controlled (Discord excluded). median drift 0.313
DRIFT = [
    ("skills", 0.590, "goals, abilities, experiences", "middleware, reusable, ide, filesystem", True),
    ("distillation", 0.448, "unet, dare, neuron, imagenet", "attacks, industrial-scale, copyrighted, laws", True),
    ("harness", 0.439, "lm-evaluation-harness, eval, lm-eval, helm", "orchestration, harnesses, ux, abstraction", True),
    ("agentic", 0.371, "empowers, augmenting, production-ready, devika, low-code", "long-horizon, tool-use, multi-step, computer-use, swe", True),
    ("prompt", 0.363, "prompts, engineering, crafting, promptfoo", "injection, adherence, caching, drafting", True),
    ("reasoning", 0.285, "multi-hop, chain-of-thought, abilities", "multilingual, spatial, instruction-following", False),
    ("safety", 0.272, "disclosure, copyright, legal, risk, regulatory", "political, mass, surveillance, misuse", False),
    ("context", 0.170, "window, length, contexts, yarn", "window, length, cache, kv, batch", False),
]

# Editorial lede theses vs method-derived dates
LEDE_VALIDATION = [
    ("MCP", "2025-03 → 07", "PELT change point", "2025-03-26", "MCP is all you need."),
    ("DeepSeek R1", "2025-W04 → W10", "Kleinberg burst", "2025-01-27", "DeepSeek is all you need."),
    ("Agent harnesses", "2024H1 → 2026H1", "embedding drift", "2025-05-15", "Agent Harnesses are all you need."),
    ("Test-time reasoning", "2025H1 peak", "section density", "2024-09-12", "Test-time reasoning is all you need."),
]

# Chronology, from descriptive titles (analysis/index.json)
CHRONOLOGY = [
    ("2023 Q4", "Open weights arrive", [
        ("2023-12-09", "The Mixtral Rush"),
        ("2023-12-11", "Mixtral beats GPT3.5 and Llama2-70B"),
        ("2023-12-13", "Towards LangChain 0.1"),
    ]),
    ("2024 Q1–Q2", "Architecture and training", [
        ("2024-01-08", "LlaMA Pro — an alternative to PEFT/RAG??"),
        ("2024-04-05", "Mixture of Depths: dynamically allocating compute"),
        ("2024-04-19", "Meta Llama 3 (8B, 70B)"),
        ("2024-05-13", "GPT-4o: the new SOTA-everything frontier model"),
    ]),
    ("2024 Q3–Q4", "Test-time compute", [
        ("2024-07-03", "GraphRAG: knowledge graphs and RAG"),
        ("2024-09-12", "o1: OpenAI's new general reasoning models"),
        ("2024-11-26", "Anthropic launches the Model Context Protocol"),
        ("2024-12-21", "o3 solves AIME, GPQA, Codeforces; 11 years of ARC-AGI progress"),
    ]),
    ("2025 Q1", "The R1 shock", [
        ("2025-01-21", "DeepSeek R1: o1-level open weights model"),
        ("2025-01-25", "TinyZero: reproduce DeepSeek R1-Zero for $30"),
        ("2025-01-28", "DeepSeek #1 on US App Store, Nvidia stock tanks −17%"),
        ("2025-03-27", "OpenAI adopts MCP"),
    ]),
    ("2025 Q2–Q3", "Harnesses and coding agents", [
        ("2025-04-08", "Llama 4's Controversial Weekend Release"),
        ("2025-05-15", "AlphaEvolve — “Agent Harnesses are all you need”"),
        ("2025-06-20", "The Quiet Rise of Claude Code vs Codex"),
        ("2025-07-11", "Kimi K2 — Muon scales to 15T tokens / 1T params"),
        ("2025-08-07", "GPT-5 rolls out to >1B users"),
    ]),
    ("2025 Q4 – 2026 Q1", "Skills, ASICs, agent labs", [
        ("2025-10-13", "OpenAI Titan XPU: 10GW of self-designed chips"),
        ("2025-10-16", "Claude Agent Skills — glorified AGENTS.md? or MCP killer?"),
        ("2026-01-13", "Anthropic Labs: Cowork, Claude Code, MCP, Skills incubator"),
        ("2026-01-27", "Kimi K2.5 beats Sonnet 4.5 at half the cost"),
    ]),
    ("2026 Q2–Q3", "Open frontier, agent security", [
        ("2026-02-24", "Anthropic accuses DeepSeek, Moonshot, MiniMax of distillation attacks"),
        ("2026-04-24", "DeepSeek v4"),
        ("2026-07-16", "Moonshot launches Kimi K3 as frontier-class open weights"),
        ("2026-07-21", "OpenAI–Hugging Face cyber incident: capability → containment"),
        ("2026-08-03", "Qwen 3.8 Max"),
    ]),
]

WITHDRAWN = [
    ("The “quiet day” series", "5% → 85% of issues",
     "The title and lede are templates. All 23 issues in the final month open “a quiet day”, including the Opus 5, GPT-5.6 and Qwen 3.8 Max launches."),
    ("“context rot” as a corpus finding", "semantic drift",
     "Disappears entirely under the genre control. It was practitioners in Discord naming a failure mode, not the field's news prose."),
    ("“agentic sat next to retrieval-augmented in 2024”", "embedding neighbours",
     "Genre artifact. Controlled, its 2024 neighbours are low-code and devika. The agents-absorbed-RAG inference loses this support; the domain counts still hold."),
    ("OpenAI's 18% → 4% headline collapse", "as evidence of fragmentation",
     "Title templating. Conditioned on descriptive titles it is 29% → 18%."),
]

AUDIT = [
    ("sections.py", "source-controlled density", "hold", "is the control"),
    ("leadlag.py", "Granger / cross-correlation", "hold", "already within sections"),
    ("bradley_terry.py", "paired comparison", "hold", "already excluded Discord"),
    ("claims.py", "numeric extraction", "hold", "already excluded Discord"),
    ("topics.py", "NMF topic discovery", "hold", "already excluded Discord"),
    ("survival.py", "Kaplan-Meier", "hold", "re-checked: no death spike at the cutoff"),
    ("changepoints.py", "PELT", "hold", "detected the composition change itself"),
    ("semantic_drift.py", "diachronic word2vec", "fixed", "genre control added; 5 of 7 survive"),
    ("arcs.py", "headline share", "fixed", "--descriptive-only conditioning"),
    ("density.py", "whole-issue density", "weak", "superseded for cross-era claims"),
    ("bursts.py", "Kleinberg", "weak", "within-regime only"),
    ("novelty.py", "novelty / resonance", "weak", "within-regime only"),
    ("logodds.py", "Fightin' Words", "weak", "top 2026 token is x.com at z = −46.2"),
    ("distributions.py", "diversity / RTD", "open", "confounded with sampling breadth"),
    ("analyze.py (quiet-day)", "title frequency", "out", "boilerplate, withdrawn"),
]

# ---- content added for the restructure ---------------------------------

# Architecture / technique density, per 10k words, within a fixed recap section
TECH_TW = {
    "MoE / routing":        [13.8, 7.8, 5.3, 15.3, 9.1, 9.2],
    "attention variants":   [2.3, 2.4, 2.9, 4.7, 4.2, 1.9],
    "quantization":         [10.0, 9.2, 5.9, 12.3, 8.0, 5.6],
    "KV cache / serving":   [1.2, 3.1, 8.6, 34.2, 26.8, 27.6],
    "RL post-training":     [7.0, 2.4, 6.6, 8.5, 3.6, 0.9],
    "distributed training": [4.6, 2.6, 3.4, 4.0, 3.3, 1.9],
    "state-space (Mamba)":  [12.8, 4.3, 0.8, 1.9, 1.5, 0.0],
    "multi-token predict":  [0.4, 0.9, 0.2, 0.7, 1.6, 1.7],
}
TECH_RD = {
    "MoE / routing":        [5.5, 6.5, 7.5, 7.3, 9.2, 15.2],
    "attention variants":   [1.0, 1.9, 1.7, 1.1, 1.7, 1.6],
    "quantization":         [22.6, 33.7, 22.7, 20.0, 25.0, 30.8],
    "KV cache / serving":   [1.0, 5.5, 3.2, 3.3, 8.5, 6.6],
    "RL post-training":     [1.0, 0.5, 1.5, 2.1, 0.5, 0.1],
    "distributed training": [3.6, 2.7, 1.7, 2.0, 1.1, 0.9],
    "state-space (Mamba)":  [1.6, 2.8, 0.3, 0.4, 0.1, 0.4],
    "multi-token predict":  [0.0, 0.3, 0.3, 0.3, 6.4, 5.0],
}

# Benchmarks: (name, claims, first, last, median score, era)
BENCHMARKS = [
    ("swe-bench", 20, "2024-04", "2026-06", 55, "spans the whole corpus"),
    ("aime", 15, "2025-01", "2026-06", 63, "arrives with reasoning models"),
    ("mmlu", 13, "2024-03", "2026-03", 78, "saturating"),
    ("math", 13, "2024-04", "2025-10", 84, "saturated, retired"),
    ("arc-agi-2", 10, "2025-10", "2026-08", 52, "the 2026 frontier"),
    ("terminal-bench", 8, "2026-05", "2026-08", 80, "agent-era benchmark"),
    ("gpqa", 7, "2024-03", "2025-11", 60, "faded"),
    ("frontiermath", 7, "2024-12", "2026-05", 31, "still unsaturated"),
    ("gsm8k", 4, "2024-02", "2024-07", 44, "dead by mid-2024"),
    ("humaneval", 4, "2024-04", "2024-09", 59, "dead by late 2024"),
    ("alpacaeval", 4, "2024-06", "2024-07", 65, "dead in two months"),
]

# The local stack, per 10k words of Reddit recap
STACK = {
    "llama.cpp":       [9.1, 6.0, 7.5, 11.4, 13.0],
    "Unsloth":         [2.4, 4.8, 3.4, 5.5, 6.0],
    "ollama":          [6.8, 3.8, 1.6, 2.0, 0.0],
    "ComfyUI":         [5.1, 5.0, 4.6, 0.8, 2.0],
    "vLLM":            [3.0, 1.7, 1.9, 3.1, 1.3],
    "exllama":         [3.8, 0.4, 0.1, 0.1, 1.5],
    "OpenRouter":      [0.9, 0.7, 1.0, 1.0, 4.1],
}
STACK_P = ["2024H2", "2025H1", "2025H2", "2026H1", "2026H2"]
HARDWARE = {
    "consumer GPU": [10.9, 5.8, 3.9, 6.3, 5.8],
    "Apple silicon": [6.2, 3.3, 2.9, 5.8, 4.7],
    "datacenter GPU": [3.1, 2.2, 1.6, 2.0, 1.9],
    "CPU / RAM offload": [0.8, 1.2, 1.5, 1.9, 2.3],
}

# Domain shares — analysis/domains.md, 16 domains x 7 half-years
DOMAIN_P = ["2023H2", "2024H1", "2024H2", "2025H1", "2025H2", "2026H1", "2026H2"]
DOMAINS = [
    ("Agents & tool use", [4, 23, 35, 41, 62, 86, 85]),
    ("Evaluation", [71, 55, 64, 69, 61, 56, 73]),
    ("Efficiency & hardware", [58, 75, 58, 61, 68, 67, 58]),
    ("Coding", [25, 20, 25, 38, 39, 43, 42]),
    ("Context & memory", [25, 35, 38, 37, 50, 48, 42]),
    ("Architecture", [33, 42, 32, 25, 45, 37, 38]),
    ("Reasoning & RL", [8, 25, 39, 66, 57, 35, 31]),
    ("Open source", [17, 17, 20, 33, 24, 18, 38]),
    ("Safety & security", [21, 27, 30, 15, 15, 32, 27]),
    ("Policy & business", [8, 16, 17, 19, 20, 17, 27]),
    ("Vision & image", [38, 49, 61, 55, 44, 25, 46]),
    ("Training & data", [46, 76, 60, 50, 43, 24, 23]),
    ("Video", [8, 11, 17, 17, 16, 5, 12]),
    ("Audio & speech", [21, 11, 19, 23, 13, 6, 8]),
    ("Robotics & embodied", [0, 5, 12, 7, 6, 2, 8]),
    ("Retrieval & search", [8, 31, 27, 14, 15, 6, 4]),
]

# The field's own agenda, in its own words: dated "X is all you need" theses
THESES = [
    ("2024-05-27", "RLHF is all you need."),
    ("2024-05-29", "SSMs are all you need."),
    ("2024-06-17", "MCTS is all you need."),
    ("2024-07-23", "Synthetic Data is all you need."),
    ("2024-08-23", "Pruning and Distillation are all you need."),
    ("2024-09-12", "Test-time reasoning is all you need."),
    ("2024-11-25", "claude_desktop_config.json is all you need."),
    ("2024-11-26", "Reinforcement Learning with Verifiable Rewards is all you need."),
    ("2024-12-23", "o3 is all you need."),
    ("2025-01-20", "GRPO is all you need."),
    ("2025-01-27", "DeepSeek is all you need."),
    ("2025-02-14", "smolagents are all you need."),
    ("2025-03-26", "MCP is all you need."),
    ("2025-05-15", "Agent Harnesses are all you need."),
    ("2025-05-27", "The LLM OS is all you need."),
    ("2025-06-25", "Finely crafted context is all you need."),
    ("2025-07-21", "General-purpose RL is all you need."),
    ("2025-10-13", "ASICs are all you need."),
    ("2025-10-29", "Agentic coding is all you need."),
    ("2025-12-18", "Skills are going the way of MCP!"),
    ("2026-01-21", "Agent Labs are all you need."),
    ("2026-03-10", "World Models are all you need."),
]

# Dated disagreements the corpus records
DEBATES = [
    ("2025-06-13", "Multi-agent systems",
     "Cognition published <em>Don't Build Multi-Agents</em> and Anthropic published how it builds "
     "multi-agents — on the same day. The newsletter ran both under one headline.",
     "Unresolved. Multi-agent framing keeps rising through 2026."),
    ("2026-02-24", "Distillation ethics",
     "Anthropic accused DeepSeek, Moonshot and MiniMax of “industrial-scale distillation attacks”. "
     "The word <code>distillation</code> moves in the embedding space from <code>unet, dare, "
     "imagenet</code> to <code>attacks, copyrighted, laws</code>.",
     "A training technique became a legal category."),
    ("2025-04-08", "Benchmark integrity",
     "Llama 4's release drew immediate accusations of benchmark-specific tuning; the corpus had "
     "already run “Did Nvidia's Nemotron 70B train on test?” six months earlier.",
     "Evaluation moved toward held-out and agentic benchmarks (Table 3)."),
    ("2025-10-17", "AGI timelines",
     "The Karpathy–Dwarkesh interview is recorded in the archive as <em>delaying</em> timelines — "
     "notable in a corpus whose ledes are otherwise relentlessly forward-leaning.",
     "Followed by a visible turn toward containment and security framing."),
]

# ---- future-work items now completed -----------------------------------

# Three-surface gradient, fold change 2024H1 -> 2026H1 (Discord coverage ends 2026-03)
GRADIENT = [
    ("agentic", 10.9, 3.5, 1.2, "announcement → community → practice"),
    ("reasoning", 2.5, 1.9, 1.4, "announcement → community → practice"),
    ("China bloc", 5.6, 12.2, 8.9, "practice led announcement"),
    ("fine-tuning", 0.1, 0.3, 0.3, "falls hardest in announcement"),
    ("RAG", 0.1, 0.2, 0.1, "falls everywhere"),
    ("quantization", 0.8, 0.5, 1.1, "rises only in practice"),
]
DISCORD_P = ["2024H1", "2024H2", "2025H1", "2025H2", "2026H1"]
DISCORD = {
    "agentic":      [11.0, 15.5, 31.2, 32.3, 38.5],
    "China bloc":   [3.6, 9.8, 38.7, 36.3, 43.8],
    "fine-tuning":  [34.3, 22.1, 14.3, 12.8, 9.7],
    "quantization": [17.9, 14.1, 12.6, 11.8, 9.4],
    "RAG":          [13.6, 10.9, 5.0, 4.1, 2.3],
    "reasoning":    [4.8, 9.1, 19.4, 10.5, 9.3],
}
# (server, messages, first, last) — 2.14M messages, 56 servers, 31,607 channel-days
COMMUNITIES = [
    ("Unsloth AI", 302248, "2024-05", "2026-03", "fine-tuning"),
    ("Perplexity AI", 253114, "2024-05", "2026-03", "product"),
    ("LMArena", 209662, "2025-03", "2026-03", "evaluation"),
    ("OpenAI", 157818, "2024-05", "2026-03", "frontier"),
    ("LM Studio", 134890, "2024-05", "2026-03", "local inference"),
    ("Cursor Community", 127021, "2025-03", "2026-03", "coding agents"),
    ("BASI Jailbreaking", 95310, "2025-11", "2026-03", "security"),
    ("HuggingFace", 90759, "2024-05", "2026-03", "infrastructure"),
]
# Source-controlled entity diversity (Hill-1), closing the fragmentation threat
DIVERSITY = {
    "twitter": [("2024H1", 22.1), ("2024H2", 24.5), ("2025H1", 30.1),
                ("2025H2", 33.2), ("2026H1", 27.4), ("2026H2", 24.9)],
    "reddit":  [("2024H1", 12.4), ("2024H2", 18.9), ("2025H1", 18.0),
                ("2025H2", 17.9), ("2026H1", 16.2), ("2026H2", 16.5)],
}
# Kaplan-Meier at model level vs family level
SURVIVAL_FAMILY = [
    ("All models", 255, 137, 140, 254),
    ("US frontier labs", 161, 175, 49, 315),
    ("Chinese labs", 49, 85, 21, 398),
    ("Open-weights families", 100, 117, 43, 273),
]

# ---- book -------------------------------------------------------------

# analysis/index.json — issues per quarter and median issue length (kilowords)
CADENCE = [
    ("23Q4", 24, 8), ("24Q1", 65, 20), ("24Q2", 66, 29), ("24Q3", 64, 27),
    ("24Q4", 66, 27), ("25Q1", 60, 32), ("25Q2", 66, 25), ("25Q3", 64, 25),
    ("25Q4", 63, 21), ("26Q1", 62, 24), ("26Q2", 64, 5), ("26Q3", 26, 6),
]

# Chapter 4 — density inside each recap section, mentions per 10^4 words.
# Counts are in analysis/; cells below n=10 are flagged in the text.
FATES_TW = {
    "state-space":   [12.13, 4.25, 0.84, 1.94, 1.51, 0.00],
    "1-bit":         [6.96, 2.59, 0.08, 0.28, 0.56, 1.71],
    "model merging": [1.08, 2.59, 0.69, 0.14, 0.00, 0.00],
    "world model":   [0.31, 0.37, 0.53, 2.15, 4.59, 5.34],
    "MoE":           [12.83, 6.84, 4.95, 13.93, 8.12, 7.69],
}
FATES_RD = {
    "state-space":   [1.62, 2.67, 0.24, 0.38, 0.11, 0.39],
    "1-bit":         [1.94, 2.46, 1.08, 0.46, 0.95, 4.71],
    "model merging": [0.97, 0.26, 0.05, 0.08, 0.10, 0.00],
    "world model":   [0.32, 0.05, 0.48, 0.52, 0.29, 0.10],
    "MoE":           [4.85, 5.33, 6.76, 6.45, 7.94, 11.08],
}
# Discord ends 2026-03: DISCORD_P periods
FATES_DC = {
    "state-space":   [2.38, 2.05, 0.99, 0.86, 0.43],
    "1-bit":         [1.99, 1.76, 0.57, 0.42, 0.28],
    "model merging": [1.09, 1.09, 0.15, 0.12, 0.50],
    "world model":   [0.04, 0.16, 0.46, 0.53, 1.22],
    "MoE":           [2.56, 1.30, 3.34, 3.93, 4.39],
}
# (idea, 2024H1 announcement, 2026 announcement, 2024H1 practice, 2026 practice, verdict)
FATES = [
    ("state-space models", 12.13, 0.00, 1.62, 0.39, "absorbed (below the vocabulary)"),
    ("model merging", 1.08, 0.00, 0.97, 0.00, "gone"),
    ("1-bit / ternary", 6.96, 1.71, 1.94, 4.71, "deferred, revived in practice"),
    ("mixture-of-experts", 12.83, 7.69, 4.85, 11.08, "absorbed (into infrastructure)"),
    ("world models", 0.31, 5.34, 0.32, 0.10, "undecided"),
]

# Chapter 5 — the reasoning turn, monthly, inside the Discord recap (the
# largest surface in this window: ~500k words/month).
REASON_M_P = ["24-06", "24-07", "24-08", "24-09", "24-10", "24-11", "24-12",
              "25-01", "25-02", "25-03", "25-04"]
REASON_M = {
    "o1 / o3":            [0.7, 0.9, 1.4, 20.4, 8.4, 8.6, 20.0, 13.8, 17.3, 6.5, 7.9],
    "reasoning":          [4.2, 7.4, 5.8, 10.4, 8.1, 6.4, 10.4, 16.3, 28.8, 20.8, 14.6],
    "test-time compute":  [0.0, 0.0, 0.0, 0.4, 0.4, 0.9, 1.4, 0.7, 1.9, 0.7, 0.7],
}
# raw counts for "test-time compute" in the Discord recap, with monthly word totals
TTC_COUNTS = [("2024-05", 703846, 0), ("2024-06", 484082, 0), ("2024-07", 611680, 1),
              ("2024-08", 476031, 2), ("2024-09", 556662, 22), ("2024-10", 594242, 24),
              ("2024-11", 497759, 43), ("2024-12", 547511, 77), ("2025-01", 546486, 40)]
# What the turn left behind — announcement space unless noted
LEGACY_TW = {
    "reasoning":            [6.26, 20.33, 37.71, 34.52, 16.80, 14.10],
    "reasoning as a knob":  [0.00, 1.29, 11.20, 6.17, 2.93, 3.20],
    "verifiable rewards":   [0.00, 0.74, 1.22, 2.29, 1.87, 2.35],
    "RLHF / DPO / PPO":     [8.04, 2.22, 5.10, 7.35, 2.47, 0.85],
    "distillation":         [1.08, 2.77, 5.33, 2.91, 3.99, 6.62],
}
LEGACY_RD = {
    "reasoning":            [6.79, 15.21, 18.41, 10.69, 9.39, 9.22],
    "reasoning as a knob":  [0.00, 1.36, 3.30, 1.32, 1.22, 0.49],
    "verifiable rewards":   [0.00, 0.10, 0.18, 0.10, 0.27, 0.20],
    "RLHF / DPO / PPO":     [0.97, 0.57, 1.14, 1.95, 0.36, 0.10],
    "distillation":         [0.97, 1.15, 3.06, 0.80, 4.02, 9.42],
}
# (idea, announcement start, end, practice start, end, verdict)
LEGACY = [
    ("reasoning (the word)", 6.26, 14.10, 6.79, 9.22, "peaked, then absorbed"),
    ("reasoning as a knob", 0.00, 3.20, 0.00, 0.49, "became an API parameter"),
    ("verifiable rewards", 0.00, 2.35, 0.00, 0.20, "replaced the old objective"),
    ("RLHF / DPO / PPO", 8.04, 0.85, 0.97, 0.10, "displaced"),
    ("distillation", 1.08, 6.62, 0.97, 9.42, "grows toward practice"),
]

# Chapter 6 — DeepSeek R1. Daily density inside the Discord recap (the largest
# surface in this window), by covered day. Pattern: deepseek|R1|r1-zero.
R1_DAILY = [
    ("01-06", 12.3), ("01-07", 12.9), ("01-08", 17.4), ("01-09", 7.3), ("01-10", 8.3),
    ("01-13", 7.5), ("01-14", 19.5), ("01-15", 17.2), ("01-16", 9.8), ("01-17", 16.1),
    ("01-20", 219.9), ("01-21", 135.5), ("01-22", 128.8), ("01-23", 85.9), ("01-24", 121.4),
    ("01-27", 205.9), ("01-28", 215.3), ("01-29", 207.6), ("01-30", 159.6), ("02-01", 155.1),
    ("02-03", 129.6), ("02-04", 62.9), ("02-05", 63.1), ("02-06", 78.5), ("02-07", 95.6),
    ("02-10", 38.3), ("02-11", 31.6), ("02-12", 48.2), ("02-13", 72.1), ("02-14", 50.0),
    ("02-17", 53.0), ("02-18", 33.5), ("02-19", 53.7),
]
R1_EVENTS = [(10, "R1 ships"), (12, "distilled reproductions"), (14, "$30 reproduction"),
             (15, "#1 on the App Store")]
# The step and the spike, monthly, inside the Discord recap
BLOC_M_P = ["24-08", "24-09", "24-10", "24-11", "24-12", "25-01", "25-02", "25-03", "25-04",
            "25-05", "25-06", "25-07", "25-08", "25-09", "25-10", "25-11", "25-12",
            "26-01", "26-02", "26-03"]
BLOC_M = {
    "China bloc": [3, 9, 4, 14, 21, 73, 46, 31, 29, 21, 20, 33, 40, 38, 35, 33, 40, 40, 49, 38],
    "DeepSeek":   [3, 5, 2, 5, 16, 58, 40, 24, 18, 12, 10, 9, 15, 10, 10, 5, 12, 8, 8, 2],
}
# Quarterly, all three surfaces — (label, pre-R1 2024Q4, peak 2025Q1, latest)
BLOC_Q = [
    ("Announcement (Twitter)", "China bloc", 17, 65, 72),
    ("Announcement (Twitter)", "DeepSeek alone", 16, 52, 10),
    ("Community (Discord)", "China bloc", 13, 50, 44),
    ("Community (Discord)", "DeepSeek alone", 7, 41, 7),
    ("Practice (Reddit)", "China bloc", 40, 87, 98),
    ("Practice (Reddit)", "DeepSeek alone", 17, 73, 26),
]

# Chapter 7 — the software around the model. Mentions per 10^4 words in section.
STACK_TW = {
    "harness":             [1.78, 0.00, 0.15, 4.09, 22.66, 31.83],
    "coding agents":       [2.55, 5.17, 19.43, 44.78, 54.60, 38.66],
    "orchestration":       [0.93, 5.17, 5.94, 10.61, 21.34, 17.73],
    "sandboxing":          [1.24, 0.37, 0.91, 3.26, 9.54, 10.68],
    "MCP":                 [0.00, 1.29, 11.50, 12.55, 8.12, 5.55],
    "context engineering": [0.00, 0.00, 2.06, 4.64, 1.97, 1.07],
    "prompt engineering":  [2.86, 2.40, 1.68, 0.90, 0.25, 0.43],
    "evals":               [28.05, 39.73, 35.65, 51.30, 60.15, 67.93],
}
STACK_RD = {
    "harness":             [0.32, 0.00, 0.16, 0.25, 1.35, 5.39],
    "coding agents":       [7.11, 2.82, 10.04, 8.84, 22.22, 15.30],
    "orchestration":       [0.00, 0.63, 2.32, 2.94, 4.46, 6.08],
    "sandboxing":          [0.65, 1.25, 1.40, 1.13, 1.58, 6.57],
    "MCP":                 [0.00, 1.78, 2.48, 1.72, 2.42, 2.26],
    "context engineering": [0.00, 0.00, 0.03, 0.19, 0.29, 0.10],
    "prompt engineering":  [2.26, 2.35, 2.75, 2.54, 1.70, 0.39],
    "evals":               [34.90, 28.64, 35.19, 35.69, 28.73, 60.12],
}
# MCP monthly in community space — a ramp, not a spike
MCP_M_P = ["24-10", "24-11", "24-12", "25-01", "25-02", "25-03", "25-04", "25-05", "25-06",
           "25-07", "25-08", "25-09", "25-10", "25-11", "25-12", "26-01", "26-02", "26-03"]
MCP_M = [0.0, 2.3, 3.6, 13.3, 22.7, 38.8, 32.1, 33.1, 34.6, 25.3, 19.5, 14.3, 15.7, 10.4,
         13.4, 11.1, 6.6, 8.8]
MCP_EVENTS = [(1, "Anthropic publishes MCP"), (5, "OpenAI adopts it")]

# Chapter 7 — fold change 2024H1 -> 2026H2 within each surface
STACK_GAP = [
    ("orchestration", 19.1, 9.7, "field-wide"),
    ("harness", 17.9, 16.8, "field-wide"),
    ("coding agents", 15.2, 2.2, "announcement-led"),
    ("sandboxing", 8.6, 10.1, "practice leads"),
    ("evals", 2.4, 1.7, "field-wide"),
    ("prompt engineering", 0.15, 0.17, "gone, everywhere"),
]

# Chapter 8 — the handover, per lab, mentions per 10^4 words in section.
# Llama-tooling noise (localllama, llama.cpp, ollama, llamaindex) stripped first.
LABS_TW = {
    "Meta / Llama":  [20.3, 34.5, 15.4, 4.3, 1.4, 1.1],
    "Mistral":       [15.2, 10.3, 8.7, 7.9, 2.3, 1.3],
    "DeepSeek":      [3.9, 11.3, 34.5, 10.9, 8.6, 10.0],
    "Qwen":          [4.3, 1.8, 10.7, 11.5, 6.9, 6.4],
    "Kimi / Moonshot": [0.0, 0.2, 1.7, 19.8, 15.7, 40.8],
    "GLM / Zhipu":   [0.2, 0.0, 0.2, 9.5, 12.6, 12.4],
    "MiniMax":       [0.0, 0.0, 1.5, 5.7, 6.7, 6.8],
}
LABS_RD = {
    "Meta / Llama":  [55.6, 37.7, 12.5, 4.6, 2.9, 2.6],
    "Mistral":       [17.3, 15.1, 8.1, 5.7, 3.8, 1.7],
    "DeepSeek":      [5.1, 13.3, 36.1, 7.7, 14.6, 26.1],
    "Qwen":          [1.3, 17.1, 11.3, 18.7, 21.4, 22.8],
    "Kimi / Moonshot": [0.0, 0.0, 0.4, 7.0, 8.8, 34.1],
    "GLM / Zhipu":   [0.0, 0.6, 0.6, 7.8, 12.1, 10.0],
    "MiniMax":       [0.0, 0.3, 1.0, 0.2, 5.6, 10.9],
}
# Three ways of asking "is Mistral still around", all correct, all different
MISTRAL_THREE = [
    ("Named anywhere in the issue body", "100%", "99%", "87%", "48%"),
    ("Tagged as a subject in front matter", "54%", "33%", "15%", "2%"),
    ("Density in announcement space", "—", "12.8", "8.3", "1.8"),
]

# Chapter 9 — the security turn. Mentions per 10^4 words in section.
SEC_TW = {
    "agent permissions": [0.93, 1.11, 1.60, 3.67, 9.59, 9.40],
    "CVE / exploit":     [0.77, 0.74, 0.46, 1.18, 3.08, 4.06],
    "prompt injection":  [0.08, 0.00, 0.46, 0.55, 0.86, 0.85],
    "alignment":         [7.19, 7.21, 3.43, 4.30, 3.03, 1.28],
    "regulation":        [1.47, 14.60, 2.82, 1.04, 0.86, 1.71],
    "existential risk":  [1.00, 1.85, 2.06, 1.04, 0.50, 1.28],
    "jailbreak":         [2.32, 1.11, 1.52, 0.62, 0.81, 1.28],
}
SEC_RD = {
    "agent permissions": [0.32, 0.68, 0.71, 2.08, 1.64, 6.08],
    "CVE / exploit":     [3.55, 1.10, 1.14, 0.97, 3.70, 5.98],
    "prompt injection":  [1.29, 0.21, 0.21, 0.42, 0.40, 0.88],
    "alignment":         [4.20, 1.62, 2.48, 4.14, 1.32, 2.26],
    "regulation":        [8.72, 6.22, 3.67, 3.21, 1.68, 4.41],
    "existential risk":  [1.94, 0.26, 1.16, 1.09, 0.34, 0.78],
    "jailbreak":         [5.49, 1.78, 1.53, 2.23, 2.99, 2.94],
}
# Old vocabulary vs new, fold change 2024H1 -> 2026H2 in each surface
SEC_GAP = [
    ("agent permissions", 10.1, 19.0, "new vocabulary"),
    ("prompt injection", 10.6, 0.68, "announcement-led"),
    ("CVE / exploit", 5.3, 1.7, "field-wide"),
    ("jailbreak", 0.55, 0.54, "flat, never large"),
    ("alignment", 0.18, 0.54, "old vocabulary"),
    ("regulation", 1.2, 0.51, "spiked, then reverted"),
]

# Interlude II — what the wrong instrument did to one series.
# (pattern, whole-issue fold, twitter fold, reddit fold, discord fold), 2024H1 -> end
MIXTURE = [
    ("consumer-GPU / VRAM", "+39%", "−81%", "+51%", "+6%"),
    ("quantization", "+27%", "−51%", "+29%", "−48%"),
    ("hallucination", "+54%", "−63%", "−32%", "+90%"),
    ("fine-tuning", "−84%", "−95%", "−64%", "−72%"),
]
# Issues carrying a Discord recap, by half-year
DISCORD_PRESENT = [("2024H1", 64, 130), ("2024H2", 129, 130), ("2025H1", 124, 126),
                   ("2025H2", 126, 127), ("2026H1", 46, 126), ("2026H2", 0, 26)]

# Chapter 10 — the name/machinery test. Announcement space, mentions per 10^4 words.
NAME_MACH_TW = {
    "RAG (the name)":       [22.57, 21.07, 5.64, 5.61, 2.57, 0.21],
    "retrieval machinery":  [14.22, 12.38, 4.49, 12.76, 13.37, 7.48],
    "memory":               [12.91, 6.28, 7.54, 12.20, 20.74, 16.45],
    "merging (the name)":   [1.16, 2.40, 0.69, 0.14, 0.00, 0.00],
    "merging machinery":    [0.00, 0.37, 0.00, 0.07, 0.00, 0.00],
}
# (idea, name start, name end, machinery start, machinery end, verdict)
NAME_MACH = [
    ("RAG", 22.57, 0.21, 14.22, 7.48, "absorbed"),
    ("fine-tuning", 26.35, 1.50, 16.07, 9.83, "absorbed"),
    ("prompt engineering", 1.78, 0.21, 1.55, 2.56, "absorbed, machinery grew"),
    ("MMLU / HumanEval / GSM8K", 4.33, 0.21, 0.77, 9.40, "replaced"),
    ("model merging", 1.16, 0.00, 0.00, 0.00, "dead"),
]

# Chapter 11 — benchmarks. Announcement space, mentions per 10^4 words.
BENCH_TW = {
    "MMLU":           [2.63, 1.48, 0.76, 0.83, 0.15, 0.00],
    "HumanEval":      [1.16, 0.55, 0.15, 0.00, 0.15, 0.00],
    "LMSYS Arena":    [2.63, 8.32, 12.04, 6.93, 0.56, 0.43],
    "SWE-bench":      [0.08, 3.70, 2.97, 2.43, 4.69, 2.14],
    "ARC-AGI":        [0.00, 1.29, 1.07, 2.29, 2.27, 1.92],
    "Terminal-Bench": [0.00, 0.00, 0.08, 0.76, 2.67, 3.84],
    "GPQA":           [0.15, 0.74, 2.36, 1.46, 0.66, 0.64],
    "AIME":           [0.00, 0.00, 2.06, 1.94, 0.40, 0.00],
    "contamination":  [0.39, 0.00, 0.53, 1.18, 0.56, 1.92],
    "LLM-as-judge":   [1.08, 1.66, 1.52, 1.11, 1.97, 4.27],
}
# (benchmark, what it asks, first seen, peak quarter, quarter it fell below 25% of peak, quarters)
BENCH_LIFE = [
    ("MT-Bench", "rated answers", "2024Q2", "2024Q2", "2024Q3", "1"),
    ("MMLU", "multiple-choice recall", "2024Q1", "2024Q2", "2024Q4", "2"),
    ("HumanEval", "fixed coding problems", "2024Q1", "2024Q2", "2024Q4", "2"),
    ("LMSYS Arena", "human preference", "2024Q1", "2025Q1", "2025Q4", "3"),
    ("FrontierMath", "fixed maths problems", "2024Q4", "2025Q4", "2026Q3", "3"),
    ("GPQA", "graduate-level recall", "2024Q2", "2025Q1", "2026Q1", "4"),
    ("AIME", "fixed maths problems", "2025Q1", "2025Q1", "2026Q1", "4"),
    ("SWE-bench", "fix a real repository", "2024Q2", "2026Q1", "—", "still rising"),
    ("ARC-AGI", "solve unseen puzzles", "2024Q3", "2026Q1", "—", "still rising"),
    ("Terminal-Bench", "drive a shell to a goal", "2025Q2", "2026Q3", "—", "still rising"),
]

# Chapter 13 — the Discord census. Message counts are declared in the channel
# headings themselves, so these are counts rather than summaries.
DISCORD_KIND = [
    ("general chat", 1785284, 83.3),
    ("uncategorised", 221304, 10.3),
    ("help / support", 68106, 3.2),
    ("research / papers", 40330, 1.9),
    ("announcements", 14402, 0.7),
    ("builds / showcase", 12601, 0.6),
]
DISCORD_CHAN = [("general", 1397089), ("ai-discussions", 130924), ("off-topic", 58840),
                ("general-chat", 50927), ("hardware-discussion", 46273), ("help", 46132),
                ("research", 32006), ("windsurf", 29373), ("jailbreaking", 25992)]
# (server, messages, first, last, months, messages per active month)
DISCORD_SERVERS = [
    ("Unsloth AI", 302248, "2024-05", "2026-03", 23, 13141),
    ("Perplexity AI", 253114, "2024-05", "2026-03", 23, 11005),
    ("LMArena", 209662, "2025-03", "2026-03", 13, 16128),
    ("OpenAI", 157818, "2024-05", "2026-03", 23, 6862),
    ("LM Studio", 134890, "2024-05", "2026-03", 23, 5865),
    ("Cursor Community", 127021, "2025-03", "2026-03", 13, 9771),
    ("BASI Jailbreaking", 95310, "2025-11", "2026-03", 5, 19062),
    ("HuggingFace", 90759, "2024-05", "2026-03", 21, 4322),
    ("Nous Research AI", 68783, "2024-05", "2026-03", 23, 2991),
    ("aider", 59431, "2024-08", "2026-03", 20, 2972),
    ("Eleuther", 51763, "2024-05", "2026-03", 23, 2251),
    ("Stability.ai", 38429, "2024-05", "2025-04", 12, 3202),
]
# Servers sampled per month — the frame shrinks by a quarter in September 2025
DISCORD_SAMPLE_P = ["24-05", "24-07", "24-09", "24-11", "25-01", "25-03", "25-05",
                    "25-07", "25-09", "25-11", "26-01", "26-03"]
DISCORD_SAMPLE = [28, 31, 32, 30, 33, 32, 29, 30, 23, 23, 23, 23]
DISCORD_PER_SERVER = [1665, 2430, 2145, 384, 2459, 3288, 4346, 4043, 3842, 5200, 4685, 2259]

# Chapter 14 — Kaplan-Meier survival, % still discussed, sampled every 30 days to 720.
# Death = 90 days of silence before the corpus ends; live models are right-censored.
KM_DAYS = list(range(0, 721, 30))
KM = {
    "tags_all": [100.0, 83.5, 71.4, 61.8, 54.5, 46.4, 40.9, 31.8, 28.9, 28.0, 24.5, 21.6,
                 21.1, 19.1, 15.6, 14.5, 14.0, 13.5, 12.4, 11.9, 9.7, 9.7, 8.7, 6.5, 5.4],
    "fams_all": [96.4, 87.1, 82.0, 76.7, 72.9, 68.2, 60.2, 55.5, 50.7, 49.9, 46.7, 45.9,
                 45.9, 44.2, 39.8, 38.1, 37.2, 36.2, 31.4, 29.4, 27.4, 26.4, 24.3, 23.3, 23.3],
    "tags_cn": [100.0, 79.6, 59.0, 50.6, 42.0, 32.6, 24.8, 16.1, 12.9, 12.9, 12.9, 12.9,
                12.9, 12.9, 12.9, 6.4, 6.4, 6.4, 6.4, 6.4, 6.4, 6.4, 6.4, 6.4, 6.4],
    "fams_cn": [95.2, 85.7, 81.0, 76.2, 76.2, 66.7, 66.7, 61.9, 57.1, 57.1, 52.4, 52.4,
                52.4, 52.4, 46.6, 39.9, 39.9, 39.9, 39.9, 31.9, 31.9, 31.9, 31.9, 31.9, 31.9],
}
# still-discussed probability at fixed horizons: (label, checkpoint %, family %)
KM_HORIZON = [("1 month", 84, 87), ("3 months", 62, 77), ("6 months", 41, 60),
              ("1 year", 21, 45), ("18 months", 12, 30), ("2 years", 5, 21)]
# (cohort, tags, tag median days, families, family median days)
KM_COHORT = [("All models", 255, 137, 140, 254), ("US frontier labs", 161, 175, 49, 315),
             ("Open-weights families", 100, 117, 43, 273), ("Chinese labs", 49, 85, 21, 398)]
# Why the reversal: naming granularity and cohort age, inside the survival cohort
KM_WHY = [("Chinese labs", "5.44", "2025-07-29", "77 d"),
          ("US frontier labs", "4.03", "2024-09-13", "138 d")]

# Interlude III — the consolidated ledger of withdrawn or reversed findings.
# (what was published, what was true, root cause)
LEDGER = [
    ("OpenAI's share of headlines fell from 18% to 4%",
     "Templated titles rose from 8% to 68% of issues, so every company falls. The template "
     "was the mirror's, not the newsletter's: 8% of issues were sent that way.",
     "copy"),
    ("Quiet-day language rose sharply, so the field was slowing",
     "The stored title and lede are placeholders. 80 of 133 recoverable issues went out "
     "under a real headline, including several major launches.",
     "copy"),
    ("The editorial layer thinned to nothing — a median of 3 words per issue by 2026",
     "The mirror had stopped carrying it. Restored from the sent emails the 2026 median is "
     "183 words, close to the 2024 peak of 190.",
     "copy"),
    ("<code>context rot</code> was a rising concern across the field",
     "A Discord idiom. It disappears entirely once chat logs are excluded from the corpus.",
     "document"),
    ("<code>agentic</code> sat next to <code>retrieval-augmented</code> in 2024, so agents "
     "absorbed retrieval",
     "A genre artifact of mixing chat and prose in one embedding. Controlled, the 2024 "
     "neighbours are <code>low-code</code> and <code>devika</code>.",
     "document"),
    ("The effective number of companies discussed rose 4.7×, so the field fragmented",
     "1.1× inside the Twitter recap and 1.3× inside the Reddit recap. The rest was the "
     "sampling frame widening from 7 to 12 subreddits and 384 to 544 accounts.",
     "document"),
    ("Models from Chinese labs have half the shelf life — 85 days against 175",
     "At family level they are the longest-lived cohort measured, 398 days against 315.",
     "unit"),
]
LEDGER_KIND = {"copy": "the archive was a copy, and the copy was lossy",
               "document": "the document stopped being the document",
               "unit": "the unit of observation was wrong"}
# Share of issues opening with a templated non-title, by year
# Share of issues whose stored `title` field is a template rather than a description.
# This series measures the GitHub mirror, not the newsletter: on the 133 issues recoverable
# from the sent emails (2026-01-26 on), only 8.3% were actually published under a templated
# subject line, against the 68% the mirror stores. See analysis/methods/titles.py.
TEMPLATED = [("2023", 8), ("2024", 16), ("2025", 42), ("2026", 68)]
TEMPLATED_PUBLISHED = 8.3
TEMPLATED_EVENT = [(3, "as actually sent: 8%")]

# Chapter 15 — one question, six defensible units. Fine-tuning, 2024H1 → 2026H2.
# (unit, what one row is, start, end, change)
UNIT_ANSWERS = [
    ("Raw mentions per issue", "an issue", "84.4", "3.1", "−96%"),
    ("Mentions per 10⁴ words, announcement space", "a word of the Twitter recap",
     "34.9", "1.9", "−94%"),
    ("Mentions per 10⁴ words, whole issue", "a word of the issue", "33.0", "5.3", "−84%"),
    ("Mentions per 10⁴ words, practice space", "a word of the Reddit recap",
     "19.4", "7.0", "−64%"),
    ("Share of issues mentioning it at all", "an issue", "100%", "65%", "−35%"),
    ("Messages per month, busiest fine-tuning community", "a Discord message",
     "7,208", "19,400", "+169%"),
]

# The editorial layer — analysis/methods/editorial.py. The lede is the only text
# in the corpus written by a person; everything under a recap heading is generated.
EDITORIAL_P = ["2024H1", "2024H2", "2025H1", "2025H2", "2026H1"]
EDITORIAL = {
    "agentic":     [13.1, 17.9, 59.7, 65.1, 47.1],
    "China bloc":  [12.1, 15.0, 72.3, 88.1, 68.2],
    "fine-tuning": [21.5, 9.3, 9.9, 6.1, 0.0],
    "RAG":         [10.4, 6.8, 2.0, 0.0, 0.0],
    "reasoning":   [4.9, 9.7, 21.9, 12.3, 13.4],
    "evals":       [29.7, 32.9, 19.2, 35.2, 35.5],
    "promotional": [15.3, 45.1, 62.3, 43.7, 24.0],
}
# (half, issues, editorial words, median per issue, issues that are boilerplate only)
EDITORIAL_SIZE = [
    ("2023H2", 25, 1158, 42, 0), ("2024H1", 130, 30650, 158, 0),
    ("2024H2", 130, 27956, 193, 0), ("2025H1", 126, 15079, 94, 0),
    ("2025H2", 127, 13052, 72, 1), ("2026H1", 126, 10411, 3, 77),
    ("2026H2", 26, 78, 3, 26),
]
