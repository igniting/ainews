# ainews

A local mirror of the [Latent Space AI News](https://www.latent.space/s/ainews/archive?sort=new)
daily newsletter, plus scripts to analyze it.

## Contents

| Path | What it is |
| --- | --- |
| `articles/` | 690 issues as markdown, `YY-MM-DD-slug.md`, 2023-12-06 → 2026-08-06 |
| `analysis/build_index.py` | Parses every issue's YAML front matter into `analysis/index.json` |
| `analysis/analyze.py` | Turns that index into `analysis/report.md` |
| `analysis/index.json` | One record per issue: date, title, tags, body size |
| `analysis/report.md` | Generated coverage/trend report |
| `analysis/arcs.py` | Per-company headline timelines → `analysis/ARCS.md` |
| `analysis/domains.py` | Topic tags grouped into domains → `analysis/domains.md` |
| **`analysis/NEWS-ANALYSIS.md`** | **The written analysis: company arcs and domain evolution** |
| `analysis/IDEAS.md` | Further analyses the corpus can support |
| `analysis/VERIFICATION.md` | The arcs checked against the article bodies |
| **`analysis/DEEPER-FINDINGS.md`** | **Results from the corpus-analysis methods** |
| **`analysis/ROADMAP-FINDINGS.md`** | **Results from the Bradley-Terry, axis, claims and diversity methods** |
| `analysis/methods/` | Change points, semantic drift, topic discovery, log-odds, novelty |

## Where the articles came from

Sourced from [`smol-ai/ainews-web-2025`](https://github.com/smol-ai/ainews-web-2025),
which is the site backing the Substack archive. Issues live in two directories
there and both are needed for full text:

- `src/content/frozen-issues/` — 538 issues, 2023-12-06 → 2025-12-31
- `src/content/issues/` — 690 issues, but the pre-2026 ones are stubs pointing at
  static HTML; only the 152 from 2026 carry their own body

So `articles/` is `frozen-issues/` plus the 152 issues-only files from 2026.

Each issue keeps its upstream front matter, which is the useful part for
analysis — it tags every issue with the `companies`, `models`, `topics` and
`people` it covered:

```yaml
title: 'DeepSeek #1 on US App Store, Nvidia stock tanks -17%'
date: '2025-01-28T05:28:32.064176Z'
companies: [deepseek, openai, nvidia, langchain]
models: [deepseek-r1, deepseek-v3, qwen2.5-vl, o1]
topics: [moe-architecture, chain-of-thought, fp8-precision, ...]
people: [sama, mervenoyann, omarasar0, ...]
```

Tag coverage is near-total: `companies` and `topics` on all 690 issues, `models`
on 682, `people` on 607.

## Running the analysis

```bash
pip install -r requirements.txt
python3 analysis/build_index.py    # articles/ -> analysis/index.json
python3 analysis/analyze.py        # index.json -> analysis/report.md
python3 analysis/domains.py        # index.json -> analysis/domains.md
python3 analysis/arcs.py openai anthropic deepseek --out analysis/ARCS.md
```

`arcs.py --list` shows the companies it knows surface forms for. Start with
[`analysis/NEWS-ANALYSIS.md`](analysis/NEWS-ANALYSIS.md) — the other files are
its inputs.

`analyze.py` folds a handful of tags that the archive spells two ways
(`huggingface`/`hugging-face`, `deepseek-ai`/`deepseek`, handles with and without
a leading underscore) via the `ALIASES` map at the top of the file — extend it
there if you spot more.

All counts are *issues mentioning a tag*, not raw mention counts, so an issue
that names OpenAI six times still counts once.
