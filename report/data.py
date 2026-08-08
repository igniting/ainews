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
