# Entity co-occurrence networks

Built by `analysis/methods/network.py`. Edges are **PPMI**, not raw
co-occurrence: raw counts merely rediscover the most-mentioned entities, since
OpenAI co-occurs with everything. Communities are Louvain, so the groupings are
the data's rather than mine.

## 2024H1

24 entities, 84 edges

1. openai, nvidia, meta-ai-fair, google-deepmind, perplexity-ai, lmsys, groq
2. mistral-ai, cohere, langchain, llamaindex, alibaba
3. anthropic, microsoft, stability-ai, scale-ai, amazon
4. hugging-face, nous-research, thebloke, ollama
5. google, apple, deepseek

## 2024H2

27 entities, 83 edges

1. openai, nvidia, langchain, microsoft, x-ai, lmsys
2. anthropic, google-deepmind, groq, scale-ai, cerebras, amazon
3. mistral-ai, deepseek, llamaindex, alibaba, togethercompute
4. google, perplexity-ai, cohere, weights-biases, stability-ai
5. meta-ai-fair, hugging-face, apple, sambanova, salesforce

## 2025H1

22 entities, 75 edges

1. openai, hugging-face, meta-ai-fair, nvidia, bytedance, x-ai, gemini
2. anthropic, google-deepmind, google, mistral-ai, perplexity-ai, togethercompute
3. deepseek, alibaba, microsoft, cohere, runway
4. langchain, ollama, llamaindex, sakana-ai

## 2025H2

33 entities, 96 edges

1. openai, anthropic, microsoft, meta-ai-fair, langchain, perplexity-ai, llamaindex, gemini, claude
2. google, nvidia, ollama, baseten, togethercompute, arena, vllm
3. deepseek, mistral-ai, x-ai, moonshot-ai, zhipu-ai, groq
4. hugging-face, openrouter, together-ai, vllm-project
5. alibaba, runway, cognition, tencent

## 2026H1

32 entities, 65 edges

1. openai, anthropic, langchain, nous-research, hugging-face, cursor, microsoft, cognition, github, artificial-analysis, cursor_ai, meta-ai-fair
2. ollama, alibaba, nvidia, baseten, openrouter, vllm, unsloth, togethercompute
3. vllm_project, xiaomi
4. google-deepmind, google
5. deepseek, x-ai

## Brokers (betweenness centrality, whole corpus)

Entities sitting on the most shortest paths between others — the connective
tissue of the ecosystem rather than its biggest names.

| Entity | Betweenness | Issues |
|---|---|---|
| google | 0.086 | 127 |
| hugging-face | 0.075 | 216 |
| alibaba | 0.073 | 115 |
| nvidia | 0.064 | 119 |
| ollama | 0.057 | 56 |
| langchain | 0.050 | 112 |
| mistral-ai | 0.047 | 122 |
| deepseek | 0.045 | 127 |
| meta-ai-fair | 0.045 | 139 |
| microsoft | 0.043 | 92 |
| anthropic | 0.037 | 246 |
| openai | 0.035 | 397 |
| google-deepmind | 0.018 | 155 |
| cognition | 0.015 | 27 |
| llamaindex | 0.014 | 50 |

