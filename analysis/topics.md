# Topics the corpus proposed for itself

NMF over TF-IDF of the issue bodies, via `analysis/methods/topics.py`.
No category list was supplied — unlike `domains.py`, whose 16 domains I chose
by hand and which therefore could only find things I had already thought of.

Values are mean document-topic share per period (%), a within-document
proportion, so the 2026 collapse in issue length does not distort them.

*24 topics, 690 issues, 2023-12-06 to 2026-08-06.*

## Rising topics

| Trend | Top terms | 2023H2 | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 | 2026H2 |
|---|---|---|---|---|---|---|---|---|
| **+6.46** | fable, roughly, sol, framed, argued, mythos | 0.2 | 0.3 | 0.4 | 0.3 | 0.7 | 9.9 | 53.9 |
| **+3.32** | mtp, qwen3, codex, tok, roughly, turboquant | 0.7 | 0.5 | 0.7 | 1.3 | 3.5 | 22.3 | 16.3 |
| **+1.73** | banana, nano, arc, indicating, humorously, reflects | 1.0 | 0.7 | 1.6 | 1.5 | 21.0 | 10.5 | 4.1 |
| **+1.28** | glm, opus, qwen3, discusses, openclaw, k2 | 0.4 | 0.4 | 1.1 | 0.9 | 1.6 | 17.5 | 0.8 |
| **+0.95** | edit, redd, banana, edits, identity, pipeline | 0.4 | 0.7 | 0.3 | 0.7 | 19.0 | 1.9 | 2.3 |
| **+0.88** | pentagon, military, dod, defense, surveillance, qwen3 | 0.2 | 0.6 | 1.5 | 1.1 | 1.2 | 8.0 | 3.5 |
| **+0.79** | skills, argues, engineering, mcp, minimax, framing | 0.5 | 1.0 | 1.3 | 3.3 | 5.3 | 7.3 | 2.4 |
| **+0.49** | score, qwen3, referencing, regarding, 235b, advances | 0.1 | 0.4 | 0.7 | 13.5 | 11.7 | 1.0 | 0.6 |

## Fading topics

| Trend | Top terms | 2023H2 | 2024H1 | 2024H2 | 2025H1 | 2025H2 | 2026H1 | 2026H2 |
|---|---|---|---|---|---|---|---|---|
| **-8.99** | mixtral, axolotl, asked, caseus, noobmaster29, inquired | 81.0 | 5.2 | 1.0 | 0.8 | 0.5 | 0.4 | 0.4 |
| **-2.39** | gif, amp, gifs, axolotl, quot, discover | 3.7 | 28.5 | 0.7 | 0.7 | 0.3 | 0.4 | 0.2 |
| **-1.49** | x22b, crawling, png, rag, artificialinteligence, diffusion | 1.0 | 19.8 | 4.5 | 1.2 | 1.3 | 0.6 | 0.9 |
| **-1.31** | twitters, wpm, checked, you, email, saved | 0.4 | 15.3 | 6.7 | 0.7 | 0.2 | 0.4 | 0.3 |
| **-1.00** | score, theme, email, flux, contents, png | 0.8 | 1.2 | 26.3 | 1.8 | 0.4 | 0.6 | 0.5 |
| **-0.71** | xlam, phi, minference, salesforce, 1b, rubra | 0.9 | 1.9 | 16.8 | 2.5 | 0.6 | 0.8 | 0.5 |
| **-0.67** | member, gtc, triton, quot, interconnects, ring | 1.1 | 9.1 | 0.8 | 0.6 | 0.8 | 0.8 | 0.5 |
| **-0.16** | granite, imagen, veo, notebooklm, sora, o1 | 0.8 | 1.2 | 4.9 | 1.8 | 1.1 | 0.9 | 0.8 |

## All topics

| # | Top terms | Peak period | Peak share |
|---|---|---|---|
| 0 | glm, opus, qwen3, discusses, openclaw, k2, kimi, codex, indicating, might | 2026H1 | 17.5% |
| 1 | gif, amp, gifs, axolotl, quot, discover, contribute, thebloke, sought, eleuther | 2024H1 | 28.5% |
| 2 | score, theme, email, flux, contents, png, llmdevs, qwen2, o1, developments | 2024H2 | 26.3% |
| 3 | fable, roughly, sol, framed, argued, mythos, technically, frontier, cyber, framing | 2026H2 | 53.9% |
| 4 | edit, redd, banana, edits, identity, pipeline, nano, implying, see, reproducibility | 2025H2 | 19.0% |
| 5 | skills, argues, engineering, mcp, minimax, framing, tweet, vibe, engagement, acquisition | 2026H1 | 7.3% |
| 6 | mixtral, axolotl, asked, caseus, noobmaster29, inquired, sought, mistral, swyxio, suggested | 2023H2 | 81.0% |
| 7 | score, qwen3, referencing, regarding, 235b, advances, notably, centers, direct, o4 | 2025H1 | 13.5% |
| 8 | deepseek, theme, score, r1, discussions, china, highlight, email, express, advancements | 2025H1 | 15.5% |
| 9 | qwq, 32b, theme, deepseek, sonnet, score, langgraph, r1, o3, grok | 2025H1 | 14.9% |
| 10 | pentagon, military, dod, defense, surveillance, qwen3, a10b, weapons, government, department | 2026H1 | 8.0% |
| 11 | twitters, wpm, checked, you, email, saved, discords, estimated, lots, png | 2024H1 | 15.3% |
| 12 | dia, o4, moral, ling, v2, constitutional, kijai, skywork, lectures, eagle | 2025H1 | 5.1% |
| 13 | granite, imagen, veo, notebooklm, sora, o1, erosion, sdks, exp, insanely | 2024H2 | 4.9% |
| 14 | wan, i2v, wan2, video, ltx, workflow, comfyui, realism, animation, sora | 2025H1 | 8.3% |
| 15 | mtp, qwen3, codex, tok, roughly, turboquant, framed, cpp, cache, harness | 2026H1 | 22.3% |
| 16 | member, gtc, triton, quot, interconnects, ring, members, rocm, qlora, galore | 2024H1 | 9.1% |
| 17 | banana, nano, arc, indicating, humorously, reflects, thinking, bench, opus, reflect | 2025H2 | 21.0% |
| 18 | humanoid, robot, robots, robotics, suicide, hospital, crises, figure, crisis, mental | 2025H2 | 9.9% |
| 19 | unitree, redd, neuralink, keyframe, mercury, smartphone, motor, sensory, marketplace, toe | 2025H2 | 5.3% |
| 20 | xlam, phi, minference, salesforce, 1b, rubra, function, personas, calling, mini | 2024H2 | 16.8% |
| 21 | windsurf, webdev, 06, acquisition, comfyui, music, kilo, acquire, versioning, ace | 2025H1 | 6.0% |
| 22 | scout, maverick, tariffs, o3, believes, mini, poster, email, deepseek, believe | 2025H1 | 10.4% |
| 23 | x22b, crawling, png, rag, artificialinteligence, diffusion, mixtral, lots, mistral, stable | 2024H1 | 19.8% |

