# Entities on interpretable semantic axes

Computed by `analysis/methods/axes.py`. Each axis is the difference between two
pole-word centroids; entities are projected onto it and **z-scored against that
era's own vocabulary**, since raw cosines are not comparable between
independently trained models.

Positive = toward the first pole. Values are standard deviations, so ±1 is a
meaningful displacement and ±0.2 is noise.

## cost: cheap (+) ↔ expensive (−)

| Entity | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 |
|---|---|---|---|---|---|
| `qwen` | +0.52 | +1.26 | +1.51 | +1.45 | +1.65 |
| `deepseek` | +0.95 | +2.19 | +1.32 | +0.86 | +0.50 |
| `kimi` | — | — | +1.49 | -0.04 | +0.88 |
| `glm` | — | — | — | +0.50 | +0.92 |
| `minimax` | — | — | +1.05 | +1.25 | +0.68 |
| `llama` | +1.06 | +0.86 | +1.54 | +1.32 | +2.22 |
| `mistral` | +0.73 | +0.95 | +0.86 | +1.80 | +1.15 |
| `gemma` | +0.44 | -0.25 | +0.80 | +1.05 | +1.13 |
| `claude` | -1.63 | +0.71 | -1.62 | -1.55 | -0.52 |
| `gpt-4o` | -0.74 | +1.60 | -0.99 | -0.71 | -0.55 |
| `gemini` | -1.91 | +0.87 | -1.28 | -1.71 | -1.19 |
| `grok` | +0.34 | +1.45 | -0.22 | -0.93 | +0.32 |
| `codex` | — | — | -0.79 | -1.74 | -0.35 |

Largest moves toward **cheap**: `llama` (+1.16), `qwen` (+1.13), `claude` (+1.11).

Toward **expensive**: `gpt-4o` (+0.19), `grok` (-0.02), `deepseek` (-0.46).

## openness: open-source (+) ↔ proprietary (−)

| Entity | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 |
|---|---|---|---|---|---|
| `qwen` | +1.01 | +0.22 | +0.26 | +2.48 | +1.05 |
| `deepseek` | +0.54 | +0.80 | +0.47 | +0.66 | +0.03 |
| `kimi` | — | — | +1.14 | +0.23 | +0.66 |
| `glm` | — | — | — | +0.75 | +0.19 |
| `minimax` | — | — | +2.35 | +2.07 | +1.47 |
| `llama` | +1.18 | +0.75 | +1.16 | +0.95 | +0.60 |
| `mistral` | +1.75 | -0.10 | +1.41 | +2.27 | +1.28 |
| `gemma` | +0.89 | +0.56 | +0.18 | +2.02 | +1.27 |
| `claude` | -1.53 | -1.56 | +0.18 | +0.19 | +0.16 |
| `gpt-4o` | -0.38 | -1.98 | -0.29 | +0.05 | -0.52 |
| `gemini` | -0.62 | -1.13 | -0.76 | -0.67 | +0.04 |
| `grok` | -0.73 | -1.48 | -0.35 | +0.31 | +0.19 |
| `codex` | — | — | +0.93 | +0.76 | +1.04 |

Largest moves toward **open-source**: `claude` (+1.69), `grok` (+0.92), `gemini` (+0.65).

Toward **proprietary**: `mistral` (-0.47), `deepseek` (-0.50), `llama` (-0.58).

## maturity: production (+) ↔ experimental (−)

| Entity | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 |
|---|---|---|---|---|---|
| `qwen` | -1.24 | -1.56 | -0.94 | -0.00 | -1.30 |
| `deepseek` | -1.34 | -0.98 | -1.42 | -1.39 | -1.79 |
| `kimi` | — | — | -2.96 | -1.02 | -1.40 |
| `glm` | — | — | — | +0.07 | -0.78 |
| `minimax` | — | — | -2.49 | -0.32 | -0.53 |
| `llama` | -0.06 | -1.00 | -1.11 | -1.02 | -1.51 |
| `mistral` | +0.02 | -0.71 | -0.89 | -0.37 | -1.83 |
| `gemma` | -1.27 | -1.11 | -1.45 | -1.26 | -1.68 |
| `claude` | -0.65 | -1.02 | -1.14 | -0.45 | -0.97 |
| `gpt-4o` | -0.50 | -1.05 | -1.51 | -0.08 | -0.90 |
| `gemini` | -0.25 | -1.15 | -2.20 | -1.38 | -2.06 |
| `grok` | -1.60 | -1.46 | -2.18 | -2.00 | -1.60 |
| `codex` | — | — | -1.27 | +0.61 | -0.44 |

Largest moves toward **production**: `grok` (-0.00), `qwen` (-0.06), `claude` (-0.32).

Toward **experimental**: `llama` (-1.45), `gemini` (-1.81), `mistral` (-1.85).

## capability: sota (+) ↔ weak (−)

| Entity | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 |
|---|---|---|---|---|---|
| `qwen` | +1.42 | +0.38 | +0.59 | +0.52 | +1.52 |
| `deepseek` | +1.50 | +0.42 | +0.09 | +0.58 | +0.99 |
| `kimi` | — | — | +3.01 | +0.55 | +0.81 |
| `glm` | — | — | — | +0.11 | +0.80 |
| `minimax` | — | — | +2.13 | +2.31 | +1.74 |
| `llama` | +1.39 | +0.52 | +0.80 | +0.30 | +1.18 |
| `mistral` | +1.25 | +0.82 | +0.59 | +0.51 | +1.97 |
| `gemma` | +1.39 | -0.21 | +0.42 | +0.21 | +1.50 |
| `claude` | +1.51 | -0.32 | -0.64 | +0.76 | -0.13 |
| `gpt-4o` | +1.27 | +0.99 | +0.36 | -0.42 | +1.10 |
| `gemini` | +1.29 | +0.61 | -0.33 | -0.30 | +0.61 |
| `grok` | +0.94 | +1.06 | -1.58 | -0.19 | +1.00 |
| `codex` | — | — | -0.07 | +0.54 | +0.32 |

Largest moves toward **sota**: `mistral` (+0.73), `gemma` (+0.10), `qwen` (+0.10).

Toward **weak**: `deepseek` (-0.50), `gemini` (-0.68), `claude` (-1.64).

## speed: fast (+) ↔ slow (−)

| Entity | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 |
|---|---|---|---|---|---|
| `qwen` | -0.24 | +0.55 | +0.22 | +0.15 | +0.54 |
| `deepseek` | +0.14 | +0.60 | -0.06 | +0.31 | -0.19 |
| `kimi` | — | — | +1.33 | +0.05 | -0.37 |
| `glm` | — | — | — | -0.16 | -0.17 |
| `minimax` | — | — | +1.56 | +0.99 | -0.16 |
| `llama` | +0.22 | +0.42 | +0.09 | +0.51 | +0.06 |
| `mistral` | -0.02 | +0.79 | +1.09 | +0.40 | +2.07 |
| `gemma` | +0.54 | +0.68 | +0.43 | +0.58 | +1.00 |
| `claude` | -0.26 | +0.91 | +0.38 | +1.19 | +1.06 |
| `gpt-4o` | -0.82 | +0.91 | -0.10 | -0.19 | +0.69 |
| `gemini` | +0.17 | +1.19 | -0.22 | +0.73 | +0.80 |
| `grok` | +0.45 | +0.54 | -0.35 | +0.30 | +1.69 |
| `codex` | — | — | +0.55 | +0.18 | +1.55 |

Largest moves toward **fast**: `mistral` (+2.09), `gpt-4o` (+1.51), `claude` (+1.32).

Toward **slow**: `gemma` (+0.46), `llama` (-0.16), `deepseek` (-0.32).

