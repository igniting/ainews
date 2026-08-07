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
