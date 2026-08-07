#!/usr/bin/env python3
"""Generate report/index.html — the full analytical report, self-contained."""
from __future__ import annotations
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import data as D
import charts as C

OUT = pathlib.Path(__file__).resolve().parent / "index.html"

CSS = """
:root{
  --ground:#F6F7F8; --panel:#FFFFFF; --sunk:#EDEFF2;
  --ink:#14171C; --body:#2C323B; --muted:#6E747F; --faint:#9AA1AC;
  --rule:#DFE3E8; --rule-strong:#C6CCD4;
  --sig:#8C2F39; --sig-soft:#8C2F3922; --sig-line:#8C2F3955;
  --bench:#2F6D7A; --bench-soft:#2F6D7A22; --bench-line:#2F6D7A55;
  --r1:#C6CCD4; --r2:#A9B2BD; --r3:#2F6D7A; --r4:#8C2F39;
  --measure:34rem;
  --serif:Charter,"Bitstream Charter","Sitka Text",Cambria,Georgia,"Times New Roman",serif;
  --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,"SF Mono","Cascadia Mono",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#0E1116; --panel:#151A21; --sunk:#1B212A;
    --ink:#EEF1F4; --body:#C3CAD3; --muted:#8B939E; --faint:#6B737E;
    --rule:#252C36; --rule-strong:#39424E;
    --sig:#E0808A; --sig-soft:#E0808A22; --sig-line:#E0808A55;
    --bench:#6FBCC9; --bench-soft:#6FBCC922; --bench-line:#6FBCC955;
    --r1:#39424E; --r2:#4B5663; --r3:#6FBCC9; --r4:#E0808A;
  }
}
:root[data-theme="dark"]{
  --ground:#0E1116; --panel:#151A21; --sunk:#1B212A;
  --ink:#EEF1F4; --body:#C3CAD3; --muted:#8B939E; --faint:#6B737E;
  --rule:#252C36; --rule-strong:#39424E;
  --sig:#E0808A; --sig-soft:#E0808A22; --sig-line:#E0808A55;
  --bench:#6FBCC9; --bench-soft:#6FBCC922; --bench-line:#6FBCC955;
  --r1:#39424E; --r2:#4B5663; --r3:#6FBCC9; --r4:#E0808A;
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--body);
  font-family:var(--serif);font-size:17px;line-height:1.62;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
.wrap{max-width:66rem;margin:0 auto;padding:0 1.5rem 6rem}
.col{max-width:var(--measure);margin-left:0}
p{margin:0 0 1.05em}
a{color:inherit;text-decoration:none;border-bottom:1px solid var(--rule-strong)}
a:hover{border-bottom-color:var(--sig)}
a:focus-visible,summary:focus-visible{outline:2px solid var(--bench);outline-offset:3px;border-radius:2px}
strong{color:var(--ink);font-weight:600}
em{font-style:italic}
code,.mono{font-family:var(--mono);font-size:.86em;color:var(--ink)}
code{background:var(--sunk);padding:.08em .34em;border-radius:3px}

/* masthead */
.mast{border-bottom:2px solid var(--ink);padding:3.4rem 0 1.5rem;margin-bottom:2.2rem}
.kicker{font-family:var(--mono);font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;
  color:var(--sig);margin:0 0 1.5rem}
h1{font-family:var(--sans);font-weight:800;letter-spacing:-.035em;line-height:1.02;
  font-size:clamp(2.3rem,6.2vw,4.1rem);color:var(--ink);margin:0 0 .5rem;text-wrap:balance;max-width:22ch}
.sub{font-size:1.18rem;color:var(--muted);max-width:46ch;margin:0 0 2rem;line-height:1.45}
.meta{display:flex;flex-wrap:wrap;gap:0 2.4rem;font-family:var(--mono);font-size:.72rem;
  letter-spacing:.05em;color:var(--muted);text-transform:uppercase}
.meta b{color:var(--ink);font-weight:600}

/* headings */
h2{font-family:var(--sans);font-weight:750;letter-spacing:-.022em;line-height:1.12;
  font-size:1.95rem;color:var(--ink);margin:0 0 1rem;text-wrap:balance}
h3{font-family:var(--sans);font-weight:700;letter-spacing:-.012em;font-size:1.16rem;
  color:var(--ink);margin:2.4rem 0 .7rem;text-wrap:balance}
h4{font-family:var(--mono);font-weight:600;font-size:.76rem;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted);margin:2rem 0 .6rem}
section{padding:3.2rem 0;border-top:1px solid var(--rule)}
section:first-of-type{border-top:none}
.secnum{font-family:var(--mono);font-size:.72rem;letter-spacing:.14em;color:var(--sig);
  text-transform:uppercase;display:block;margin-bottom:.7rem}
.lede{font-size:1.1rem;color:var(--ink);line-height:1.5}

/* evidence tier chips */
.tier{display:inline-block;font-family:var(--mono);font-size:.62rem;font-weight:600;
  letter-spacing:.1em;text-transform:uppercase;padding:.2em .5em;border-radius:3px;
  vertical-align:.18em;margin-left:.5rem;white-space:nowrap}
.tier.a{background:var(--ink);color:var(--ground)}
.tier.b{border:1px solid var(--rule-strong);color:var(--muted)}
.tier.c{border:1px dashed var(--sig);color:var(--sig)}
.tier.x{border:1px solid var(--rule);color:var(--faint);text-decoration:line-through}

/* figures */
figure{margin:2.4rem 0;max-width:62rem;margin-left:0}
figure svg{width:100%;height:auto;display:block;background:var(--panel);
  border:1px solid var(--rule);border-radius:3px;padding:.5rem}
figcaption{font-family:var(--sans);font-size:.83rem;line-height:1.5;color:var(--muted);
  margin-top:.75rem;max-width:50rem}
figcaption b{font-family:var(--mono);font-size:.72rem;letter-spacing:.1em;
  text-transform:uppercase;color:var(--ink);display:block;margin-bottom:.25rem}
.grid{stroke:var(--rule);stroke-width:1}
.ref{stroke:var(--rule-strong);stroke-width:1}
.ref.dash{stroke-dasharray:3 3}
.ln{fill:none;stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.ln.sig,.dot.sig,.serlab.sig{stroke:var(--sig)}
.ln.bench,.dot.bench,.serlab.bench{stroke:var(--bench)}
.ln.ink{stroke:var(--ink)}
.ln.ink2{stroke:var(--ink);stroke-dasharray:5 3}
.dot.ink,.dot.ink2{fill:var(--ink)}
.serlab.ink2{fill:var(--ink)}
.dot{stroke:none}
.dot.sig{fill:var(--sig)} .dot.bench{fill:var(--bench)}
.bar.sig{fill:var(--sig-line)} .bar.bench{fill:var(--sig)}
.band.disc{fill:var(--rule-strong);opacity:.55}
.band.redd{fill:var(--bench-soft);stroke:var(--bench-line)}
.band.twit{fill:var(--sig-soft);stroke:var(--sig-line)}
.band.gap{fill:var(--rule);opacity:.5;stroke:none}
.conn{stroke:var(--rule-strong);stroke-width:2}
text{font-family:var(--mono);fill:var(--muted)}
.tick{font-size:10.5px} .tick.tiny{font-size:9px}
.axlab{font-size:9.5px;letter-spacing:.09em;text-transform:uppercase;fill:var(--faint)}
.serlab{font-size:11px;font-weight:600;stroke:none}
.serlab.sig{fill:var(--sig)} .serlab.bench{fill:var(--bench)} .serlab.ink{fill:var(--ink)}
.rowlab{font-size:12px;fill:var(--ink)}
.gaplab{font-size:10px;fill:var(--faint);letter-spacing:.06em;text-transform:uppercase}
.ptlab{font-size:10.5px;fill:var(--ink)}
.bandlab{font-size:11px;font-weight:600;fill:var(--ink)}
.reg.r1{fill:var(--r1)} .reg.r2{fill:var(--r2)} .reg.r3{fill:var(--r3)} .reg.r4{fill:var(--r4)}
.regname{font-size:10.5px;font-weight:600;fill:var(--ground);text-anchor:middle;letter-spacing:.04em}

/* tables */
.tw{overflow-x:auto;margin:1.8rem 0;max-width:62rem;border:1px solid var(--rule);border-radius:3px;background:var(--panel)}
table{border-collapse:collapse;width:100%;font-family:var(--mono);font-size:.79rem;
  font-variant-numeric:tabular-nums}
th{text-align:left;font-weight:600;color:var(--ink);letter-spacing:.05em;text-transform:uppercase;
  font-size:.67rem;padding:.7rem .8rem;border-bottom:1px solid var(--rule-strong);white-space:nowrap}
td{padding:.55rem .8rem;border-bottom:1px solid var(--rule);color:var(--body);vertical-align:top}
tr:last-child td{border-bottom:none}
td.n,th.n{text-align:right}
td b{color:var(--ink)}
.hi{color:var(--sig);font-weight:600}
.hib{color:var(--bench);font-weight:600}
caption{caption-side:top;text-align:left;font-family:var(--mono);font-size:.7rem;
  letter-spacing:.1em;text-transform:uppercase;color:var(--muted);padding:.8rem .8rem .2rem}

/* callouts */
.note{border-left:2px solid var(--bench);padding:.1rem 0 .1rem 1.1rem;margin:1.6rem 0;
  color:var(--body);font-size:.96rem}
.warn{border-left:2px solid var(--sig);padding:.1rem 0 .1rem 1.1rem;margin:1.6rem 0;font-size:.96rem}
.pull{font-family:var(--sans);font-weight:650;font-size:1.28rem;line-height:1.32;color:var(--ink);
  letter-spacing:-.015em;margin:2.2rem 0;padding-left:1.1rem;border-left:3px solid var(--sig);
  text-wrap:balance}

/* era chronology */
.eras{display:grid;gap:0;margin:2rem 0;border-top:1px solid var(--rule-strong)}
.era{display:grid;grid-template-columns:9.5rem 1fr;gap:1.6rem;padding:1.3rem 0;
  border-bottom:1px solid var(--rule)}
.era-when{font-family:var(--mono);font-size:.73rem;letter-spacing:.08em;text-transform:uppercase;
  color:var(--sig);padding-top:.15rem}
.era-what{font-family:var(--sans);font-weight:700;font-size:1.02rem;color:var(--ink);
  margin:0 0 .5rem;letter-spacing:-.01em}
.era ul{margin:0;padding:0;list-style:none;display:grid;gap:.3rem}
.era li{font-family:var(--mono);font-size:.775rem;color:var(--muted);line-height:1.45;
  display:grid;grid-template-columns:5.4rem 1fr;gap:.7rem}
.era li span{color:var(--faint)}

/* legend */
.legend{display:flex;flex-wrap:wrap;gap:1.4rem;font-family:var(--mono);font-size:.72rem;
  color:var(--muted);margin:.9rem 0 0;letter-spacing:.03em}
.legend i{display:inline-block;width:1.5rem;height:2px;vertical-align:.25em;margin-right:.45rem}
.legend .s{background:var(--sig)} .legend .b{background:var(--bench)} .legend .k{background:var(--ink)}

/* audit */
.audit{display:grid;gap:0;margin:1.6rem 0;border-top:1px solid var(--rule-strong)}
.arow{display:grid;grid-template-columns:12rem 1fr 5.5rem;gap:1rem;padding:.62rem 0;
  border-bottom:1px solid var(--rule);align-items:baseline;font-size:.83rem}
.arow code{background:none;padding:0;font-size:.78rem}
.arow .why{color:var(--muted);font-family:var(--sans);font-size:.83rem}
.vd{font-family:var(--mono);font-size:.63rem;letter-spacing:.1em;text-transform:uppercase;
  text-align:right;font-weight:600}
.vd.hold{color:var(--bench)} .vd.fixed{color:var(--ink)}
.vd.weak{color:var(--muted)} .vd.open{color:var(--sig)} .vd.out{color:var(--faint);text-decoration:line-through}

/* withdrawn */
.wd{border:1px solid var(--rule);border-radius:3px;padding:1rem 1.2rem;margin:1rem 0;background:var(--panel)}
.wd h5{margin:0 0 .3rem;font-family:var(--sans);font-size:.98rem;color:var(--faint);
  font-weight:650;text-decoration:line-through}
.wd .was{font-family:var(--mono);font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;
  color:var(--sig);display:block;margin-bottom:.5rem}
.wd p{margin:0;font-size:.9rem;color:var(--body)}

ol.refs{font-size:.84rem;color:var(--muted);padding-left:1.3rem;line-height:1.55}
ol.refs li{margin-bottom:.5rem}
ul.plain{padding-left:1.15rem;margin:0 0 1.05em}
ul.plain li{margin-bottom:.42rem}
hr{border:none;border-top:1px solid var(--rule);margin:2.6rem 0}
.foot{font-family:var(--mono);font-size:.72rem;color:var(--faint);letter-spacing:.05em;
  border-top:1px solid var(--rule);padding-top:1.4rem;margin-top:3rem;line-height:1.7}
@media (max-width:640px){
  body{font-size:16px}
  .era{grid-template-columns:1fr;gap:.5rem}
  .era li{grid-template-columns:4.6rem 1fr;gap:.5rem}
  .arow{grid-template-columns:1fr;gap:.15rem}
  .vd{text-align:left}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""


def tier(t):
    names = {"a": "Tier A", "b": "Tier B", "c": "Tier C", "x": "Withdrawn"}
    return f'<span class="tier {t}">{names[t]}</span>'


def table(headers, rows, caption="", numcols=()):
    th = "".join(f'<th class="{"n" if i in numcols else ""}">{C.esc(h)}</th>' for i, h in enumerate(headers))
    body = []
    for r in rows:
        tds = "".join(f'<td class="{"n" if i in numcols else ""}">{c}</td>' for i, c in enumerate(r))
        body.append(f"<tr>{tds}</tr>")
    cap = f"<caption>{C.esc(caption)}</caption>" if caption else ""
    return f'<div class="tw"><table>{cap}<thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def fig(svg, num, title, body):
    return (f'<figure><figcaption><b>Figure {num} — {C.esc(title)}</b>{body}</figcaption>'
            f'{svg}</figure>')


def figtop(svg, num, title, body):
    return (f'<figure>{svg}<figcaption><b>Figure {num} — {C.esc(title)}</b>{body}</figcaption></figure>')


# ---------------------------------------------------------------- document
def build() -> str:
    P6 = D.P6
    comp = C.stacked(P6, [("Discord", D.COMPOSITION["Discord"], "disc"),
                          ("Reddit", D.COMPOSITION["Reddit"], "redd"),
                          ("Twitter", D.COMPOSITION["Twitter"], "twit")],
                     [0, 25, 50, 75, 100], "share of issue words")
    themes_tw = C.lines(P6, [("agentic", D.TWITTER["agentic"], "sig"),
                             ("reasoning", D.TWITTER["reasoning"], "bench"),
                             ("fine-tuning", D.TWITTER["fine-tuning"], "ink"),
                             ("RAG", D.TWITTER["RAG"], "ink2")],
                        [0, 50, 100, 150], "mentions / 10⁴ words")
    themes_rd = C.lines(P6, [("agentic", D.REDDIT["agentic"], "sig"),
                             ("reasoning", D.REDDIT["reasoning"], "bench"),
                             ("fine-tuning", D.REDDIT["fine-tuning"], "ink"),
                             ("RAG", D.REDDIT["RAG"], "ink2")],
                        [0, 10, 20, 30], "mentions / 10⁴ words")
    cross_tw = C.lines(P6, [("China bloc", D.TWITTER["China bloc"], "sig"),
                            ("Meta + Mistral", D.TWITTER["Meta+Mistral"], "bench")],
                       [0, 25, 50, 75], "mentions / 10⁴ words")
    cross_rd = C.lines(P6, [("China bloc", D.REDDIT["China bloc"], "sig"),
                            ("Meta + Mistral", D.REDDIT["Meta+Mistral"], "bench")],
                       [0, 30, 60, 90], "mentions / 10⁴ words")

    H = []
    A = H.append

    # ---------------------------------------------------------- masthead
    A(f'''<div class="wrap"><header class="mast">
<p class="kicker">Corpus study · 690 issues · 15.3M words · 2023–2026</p>
<h1>Announcement space and practice space</h1>
<p class="sub">A source-controlled study of three years of AI's daily trade press —
what the field actually did, and how nearly every naive way of measuring it goes wrong.</p>
<div class="meta">
<span><b>690</b> daily issues</span><span><b>15.3M</b> words</span>
<span><b>13</b> methods</span><span><b>4</b> findings withdrawn</span>
<span>2023-12-06 → 2026-08-06</span>
</div>
</header>''')

    # ---------------------------------------------------------- abstract
    A(f'''<section><div class="col">
<span class="secnum">Abstract</span>
<p class="lede">We analyse 690 consecutive daily issues of an AI newsletter (15.3M words,
December 2023 – August 2026) as a contemporaneous, never-revised record of what the field
believed on each day. The corpus turns out to invert its own source composition — issue text
moves from 96% Discord transcript to 0%, with Twitter rising from 2% to 23% — which
confounds every whole-document frequency measure. Re-deriving all results <em>inside</em> a
fixed source section both preserves six principal findings and produces the study's most
useful one: a measurable gap between <strong>announcement space</strong> and
<strong>practice space</strong>. Agent discourse rises 8.0× in the Twitter recap but only
2.0× in the Reddit recap; fine-tuning falls 90% in announcement space but only 60% in
practice, and recovers at the end. Where the two surfaces agree — agent harnesses (17.9×
vs 16.8×), the Chinese open-weights bloc (8.6× vs 15.3×) — the shift is field-wide rather
than narrative. We further show that five core engineering terms changed referent
mid-corpus (<code>harness</code>, <code>skills</code>, <code>prompt</code>,
<code>distillation</code>, <code>agentic</code>), which invalidates naive keyword series
over them. A full method audit withdraws four earlier findings and bounds a fifth. The
methodological result is the transferable one: eleven statistical methods, several of them
sophisticated, could not surface artifacts that reading a hundred documents found
immediately.</p>
</div></section>''')

    # ---------------------------------------------------------- 1. intro
    A(f'''<section><div class="col">
<span class="secnum">§ 1 — Introduction</span>
<h2>A field's history, written forwards</h2>
<p>The history of a fast-moving technical field is normally written backwards. Retrospectives
are composed once the winners are known, which makes them excellent at explaining what
happened and structurally incapable of telling you what the field <em>believed</em> while it
was happening. Dead ends get compressed to a sentence. Things that felt inevitable and
weren't are quietly dropped.</p>
<p>This corpus was written forwards. It is a newsletter that published on roughly 70% of all
calendar days for two years and eight months, summarising what the AI community was
discussing on Twitter, Reddit and Discord. Wrong guesses are left intact. Enthusiasms that
went nowhere are recorded at the same volume as the ones that became infrastructure. That
makes it usable as a measurement substrate for questions retrospective sources cannot
answer.</p>
<p>It is also, as it turns out, an object lesson in how such a substrate misleads. Roughly
half of this report is about the field. The other half is about the instrument, because we
could not trust the first half until we understood the second.</p>

<h4>What this study measures</h4>
<p>Attention, as reported. Not deployment, not revenue, not capability. When we say
fine-tuning fell, we mean the newsletter's sources discussed it less — a claim about
discourse, which is interesting precisely because discourse and practice turn out to
diverge measurably.</p>

<h4>Evidence tiers</h4>
<p>Every result below carries a tier, because "we measured it" stopped being sufficient
partway through this work.</p>
<div class="tw"><table>
<thead><tr><th>Tier</th><th>Meaning</th></tr></thead><tbody>
<tr><td><b>A</b></td><td>Reproduces independently in two source sections</td></tr>
<tr><td><b>B</b></td><td>Single method, source- or genre-controlled, confound stated</td></tr>
<tr><td><b>C</b></td><td>Measured but confounded — reported as a bound, not a value</td></tr>
<tr><td><b>✗</b></td><td>Tested and withdrawn</td></tr>
</tbody></table></div>
</div></section>''')

    # ---------------------------------------------------------- 2. how the field evolved
    eras = []
    for when, what, items in D.CHRONOLOGY:
        lis = "".join(f'<li><span>{C.esc(d)}</span>{C.esc(t)}</li>' for d, t in items)
        eras.append(f'<div class="era"><div class="era-when">{C.esc(when)}</div>'
                    f'<div><p class="era-what">{C.esc(what)}</p><ul>{lis}</ul></div></div>')

    A(f'''<section><div class="col">
<span class="secnum">§ 2 — The field</span>
<h2>How AI actually evolved, 2023–2026</h2>
<p>Before any methodology, the substance. What follows is the trajectory the corpus records,
stated as a narrative and then measured in §6. Every claim here is one the source-controlled
analysis supports; the ones that did not survive are in §7.</p>

<p class="pull">The scarce resource moved three times: from model quality, to context, to
orchestration and cost.</p>

<h3>2023–24: open weights arrive, and the agenda is training</h3>
<p>The corpus opens in December 2023 in the middle of the Mixtral release, and for its first
six months the field's centre of gravity is unambiguously <em>making models</em>. The
vocabulary of the period is fine-tuning, LoRA, synthetic data, model merging, distillation,
mixture-of-experts routing, quantization. In announcement space <code>fine-tuning</code>
runs at 34.9 mentions per 10⁴ words — the highest any theme reaches in the entire corpus
until agents arrive two years later. Retrieval sits alongside it at 22.5: RAG is the
default architecture for making a model useful, and LangChain and LlamaIndex are the
frameworks everyone is arguing about.</p>
<p>Open weights are the other story. Mistral is the single most concentrated presence in the
corpus's history — in the first half-year it is the subject of a third of all issues — and
Meta's Llama 3 in April 2024 makes open weights genuinely competitive with the frontier. If
you had read only 2024, you would have concluded the open ecosystem was European and
American.</p>

<h3>Late 2024: test-time compute changes the axis</h3>
<p>The inflection is September 2024. OpenAI's o1 ships, and the newsletter's editor calls it
the same day with a one-line lede — <em>"Test-time reasoning is all you need."</em> In
announcement space <code>reasoning</code> goes 7.0 → 23.4 → 40.2 across three half-years.
The interesting detail, which we return to in §6.8, is that the <em>thesis</em> was stated
roughly two quarters before the <em>volume</em> peaked.</p>
<p>Two months later Anthropic ships the Model Context Protocol, to almost no immediate
notice — the lede that day is <em>"<code>claude_desktop_config.json</code> is all you
need."</em> It becomes one of the fastest-moving items in the corpus.</p>

<h3>January 2025: the R1 shock</h3>
<p>The single densest week in the archive. DeepSeek R1 ships on the 21st as an open-weights
model at o1 level; by the 25th someone has reproduced R1-Zero for $30; by the 28th DeepSeek
is the top free app in the US App Store and Nvidia has fallen 17%. Burst detection places a
statistically significant DeepSeek burst at 4.7× baseline across weeks 4–10 of 2025 — and
places a <code>reasoning</code> burst in <em>exactly the same weeks</em>. That coincidence
is the cleanest evidence in the corpus that R1 is what converted reasoning from an OpenAI
product feature into a field-wide research programme.</p>

<h3>2025: harnesses, and the frontier changes passport</h3>
<p>From spring 2025 the corpus stops being about models and starts being about the software
around them. The editor's lede on 15 May 2025 is <em>"Agent Harnesses are all you
need"</em>; by 25 June it is <em>"Finely crafted context is all you need."</em> Claude Code
and Codex appear, then Cursor, Devin, Windsurf. In announcement space <code>harness</code>
goes from effectively absent to 31.8 per 10⁴ words — a 17.9× rise that is matched almost
exactly in practice space (16.8×), which is what a genuine field-wide shift looks like.</p>
<p>Simultaneously the open-weights frontier changes hands. Qwen, DeepSeek, Kimi/Moonshot,
GLM and MiniMax displace Meta and Mistral so completely that the ratio between the two blocs
inverts by more than two orders of magnitude. Mistral did not stop shipping — in December
2025 its Devstral 2 beat DeepSeek v3.2 in 71% of third-party human evaluations — it stopped
being <em>news</em>. Meta's decline, contrary to the obvious reading, begins in October 2024,
six months <em>before</em> the poorly-received Llama 4.</p>

<h3>2026: open frontier, agent security, and price as the axis</h3>
<p>By the final year the pattern is stable and fast. Kimi K3, Qwen 3.8 Max, DeepSeek v4,
GLM, MiniMax and Thinking Machines' Inkling all ship frontier-class open weights within
months of each other, and nearly every one is framed on price: <em>8% of Claude Sonnet's
price</em>, <em>11% of its cost</em>, <em>10× cheaper</em>. Distillation stops being a
training technique and becomes a legal accusation. And security moves from the periphery to
the centre — the OpenAI–Hugging Face incident runs across four consecutive issues under the
framing "from capability to containment", while agent sandboxing, prompt injection and
supply-chain risk become recurring structural topics rather than occasional ones.</p>

</div>
{table(["Era", "What was scarce", "Dominant vocabulary", "agentic", "fine-tuning", "RAG", "reasoning"],
 [["2024H1", "model quality", "LoRA · synthetic data · MoE · merging", "12.7", "<b>34.9</b>", "22.5", "7.0"],
  ["2024H2", "model quality", "distillation · pruning · long context", "38.8", "12.0", "21.0", "23.4"],
  ["2025H1", "reasoning depth", "GRPO · verifiable rewards · test-time compute", "67.4", "8.0", "5.6", "<b>40.2</b>"],
  ["2025H2", "orchestration", "harness · MCP · context engineering", "99.0", "10.3", "5.6", "35.8"],
  ["2026H1", "orchestration + cost", "long-horizon · computer-use · skills", "<b>138.5</b>", "4.9", "2.6", "17.2"],
  ["2026H2", "cost + containment", "sandboxing · injection · price/perf", "101.6", "1.9", "0.2", "14.3"]],
 "Table 3 · The agenda by era. Mentions per 10⁴ words inside the Twitter recap", (3,4,5,6))}
<div class="col">
<h3>What the numbers say the eras were</h3>
<p>Reading the four series across the table gives the transition its shape. Through 2024 the
field's effort goes into <em>producing</em> a model: fine-tuning is the single densest theme in
the corpus at that point, and retrieval is the standard way of making the result useful. By
2025H1 both have collapsed to roughly a fifth of their peak while reasoning has multiplied
sixfold — the field has moved from training-time to inference-time. By 2026 reasoning has
itself receded to about twice its baseline, not because it failed but because it stopped being
remarkable, and the entire remaining slope belongs to orchestration.</p>
<p>The absorption pattern repeats often enough to be worth stating as a rule. Retrieval,
reasoning and multimodality all peak and then decline sharply while remaining ubiquitous in the
prose. Each of the three won. Things that genuinely did not arrive look different: they never
peak. Robotics does not exceed 12% of issues in any period of the corpus, and audio and video
generation both had moments — Sora, ElevenLabs, Veo, Voxtral — that never converted into
sustained coverage on either surface.</p>

<h3>Three specific transitions worth naming</h3>
<p><strong>RAG did not die; it was absorbed twice.</strong> Retrieval falls 22.5 → 0.2 in
announcement space, the sharpest decline of any theme. Two mechanisms are visible. Context
windows ate part of it — when a model holds a million tokens, chunk retrieval is an
implementation detail rather than an architecture. Agents ate the rest — retrieval became a
tool call inside a loop. The vendor evidence is the sharpest version: over the same window
LangChain reached its highest coverage of the whole corpus while LlamaIndex fell to near zero.
The framework that followed the workload into orchestration survived; the one that stayed with
indexing did not. <em>Category death and vendor death are different events</em>, and the
category counts alone would have got this exactly backwards.</p>
<p><strong>MCP is the cleanest complete hype cycle in the archive.</strong> From zero in 2024H2
to 12.1 mentions per 10⁴ words in 2025H2 and back to 5.6 by 2026H2, with the peak dated by
change point detection to a five-month window in 2025 — and the editor's lede naming it on
2025-03-26, inside that window. Notably its discussion fell while Anthropic's own density
doubled, which is what adoption looks like once a protocol becomes plumbing.</p>
<p><strong>Security arrived late and changed shape.</strong> Safety coverage roughly halves
across 2025 — the period of maximum capability racing — then recovers through 2026 as something
different. The embedding evidence is direct: in 2024 the word <code>safety</code> sits beside
<code>disclosure</code>, <code>copyright</code>, <code>legal</code> and <code>regulatory</code>;
by 2026 it sits beside <code>surveillance</code>, <code>misuse</code>, <code>political</code>
and <code>mass</code>. It left as a legislative topic and returned as an operational and
societal one, and by the final month agent sandboxing and prompt injection are running across
consecutive issues.</p>
<h3>The chronology</h3>
<div class="eras">{"".join(eras)}</div>
<p style="font-family:var(--sans);font-size:.83rem;color:var(--muted);margin-top:-.4rem">
Chronology drawn from issues with descriptive titles. 68% of 2026 titles are the placeholder
"not much happened today" — including several of the launches above — which is itself a
finding (§4.3).</p>
</div></section>''')

    # ---------------------------------------------------------- 3. corpus
    A(f'''<section><div class="col">
<span class="secnum">§ 3 — The corpus</span>
<h2>What the archive is made of</h2>
<p>690 issues, 2023-12-06 to 2026-08-06, 15.3M words of body text, published on roughly five
days a week and covering about 70% of all calendar days in the window. Reconstructing it
required merging two directories of the publisher's site: the pre-2026 issues are stubs in
one and full text in the other.</p>
<p>Each issue has a consistent internal anatomy, and recognising it is what eventually made
the analysis tractable:</p>
<ul class="plain">
<li><strong>An editorial lede</strong> — one line, human-written, stating a thesis.</li>
<li><strong>A metadata header</strong> declaring how many subreddits, Twitter accounts and
Discord servers were checked that day.</li>
<li><strong>Parallel recaps</strong> of Twitter, Reddit and Discord, each summarising the
same 24 hours from a different surface.</li>
<li><strong>Front-matter tags</strong> — generated lists of companies, models, topics and
people.</li>
</ul>
</div>
{table(["Layer", "Extracted", "What it supports"],
 [["Discord telemetry", "31,688 channel-days · 2.15M messages · 56 servers", "community activity series (unused)"],
  ["Tweet attribution", "18,854 (handle, status-ID) pairs", "attribution-fidelity checks"],
  ["Reddit engagement", "3,070 scored posts", "practice-space weighting"],
  ["Numeric claims in prose", "1,335 context · 990 parameter · 176 benchmark · 151 price", "§6.6"],
  ["Editorial ledes", "234 “X is all you need” theses", "§6.8 validation"],
  ["Declared sampling effort", "571 issues", "§4.2 — the central control"]],
 "Table 1 · Structured layers embedded in the prose", (1,))}
<div class="col">
<h3>Three editorial layers, not one</h3>
<p>The issue of 15 May 2025 is titled <code>alphaevolve</code> and its lede reads
<em>"Agent Harnesses are all you need."</em> The two are not the same claim. The title names
the day's <strong>event</strong>; the lede states the editor's <strong>thesis</strong>; the
body carries the <strong>sources</strong>. Our first several months of analysis used layers
two and three and discarded layer one as boilerplate. It is in fact the most compressed and
most human field in the corpus, and §6.8 uses it as independent ground truth.</p>
</div></section>''')

    # ---------------------------------------------------------- 4. instrument
    A(f'''<section><div class="col">
<span class="secnum">§ 4 — The instrument</span>
<h2>Four regimes, one inversion, and a template</h2>
<p>This section comes before Methods because every method depends on it. A daily publication
is not a stationary instrument: its format, its sources and its editorial conventions all
changed during the window, and each change produces a signal that looks exactly like news.</p>

<h3>4.1 Publishing regimes</h3>
<p>Change point detection (PELT) run over structural features alone — issue length, which
recap sections exist, link and heading density, with no access to content — recovers four
regimes. The third is the comparable core: 460 issues over nearly two years with a stable
format.</p>
</div>
{figtop(C.ribbon(D.REGIMES), 1, "Publishing regimes, recovered from structure alone",
  "PELT segmentation over standardised structural features. Regime 3 (teal) is the 460-issue "
  "stable core; regime 4 begins when the Discord recap is dropped. These boundaries appear "
  "on every time-series figure in this report.")}
<div class="col">
<h3>4.2 The source-composition inversion</h3>
<p>The central artifact, and the one that nearly invalidated this study. Each issue declares
its own sampling effort in its header. Over the window, Discord coverage falls from 30
servers to <strong>zero</strong>, while Twitter rises from 384 to 544 accounts and
subreddits from 7 to 12.</p>
<p>The effect on the text is dramatic. In early 2024 an issue is 96% Discord transcript. By
2026 it is 0% Discord, 61% Reddit, 23% Twitter.</p>
</div>
{figtop(comp, 2, "Source composition of issue text inverts completely",
  "Share of each issue's words by recap section. Discord (grey) goes from dominant to absent; "
  "Reddit (teal) and Twitter (oxblood) expand to fill it. Any measure normalised by total "
  "issue words therefore conflates topic prevalence with which surface was being sampled.")}
<div class="col">
<div class="warn"><p><strong>Consequence.</strong> A theme that lives in Discord help
channels — fine-tuning, local inference, quantization — declines mechanically once Discord
sampling stops. A theme that lives on Twitter — model launches — rises mechanically. Three
of our four largest findings were exposed to this simultaneously.</p></div>

<h3>4.3 Title and lede templating</h3>
<p>Two fields converge on placeholders independently of whether anything happened. The title
"not much happened today" appears in 0% of 2023 issues, 18% of 2024, 42% of 2025 and
<strong>68% of 2026</strong> — carried by the Claude Opus 5, GPT-5.6, Qwen 3.8 Max and Kimi
K3 launch issues alike. All 23 issues in the final month open with the lede "a quiet day",
three of them major launches.</p>
<p>Since no company can be named in a placeholder title, any headline-share measure falls
mechanically as the template spreads. This produced one of our four withdrawn findings
(§7.1).</p>

<h3>4.4 Six ways to measure the wrong thing</h3>
</div>
{table(["Measure", "What it actually tracks", "Evidence"],
 [["Issue mentions entity (binary)", "nothing — saturates", "80–97% for most tracked entities"],
  ["Raw mention counts", "document length", "median issue 28k → 5.8k words"],
  ["Whole-issue density", "<span class='hi'>source composition</span>", "96% Discord → 0%"],
  ["Title / headline share", "<span class='hi'>editorial templating</span>", "placeholder titles 0% → 68%"],
  ["KL over topic distributions", "format regimes", "top novelty days cluster on regime edges"],
  ["Raw co-occurrence", "marginal frequency", "resolved with PPMI"]],
 "Table 2 · Failure modes observed on this corpus")}
<div class="col">
<p>The resolution used throughout: <strong>mentions per 10⁴ words within a fixed recap
section</strong>, or ranks, or PPMI — never raw presence, never whole-document
normalisation across regimes.</p>
</div></section>''')

    # ---------------------------------------------------------- 5. methods
    method_rows = []
    for name, what, verdict, why in D.AUDIT:
        method_rows.append([f"<code>{C.esc(name)}</code>", C.esc(what), C.esc(why)])
    A(f'''<section><div class="col">
<span class="secnum">§ 5 — Methods</span>
<h2>Thirteen methods, each with its failure mode</h2>
<p>Methods are grouped by what they estimate. Every one is released with the way it breaks on
this corpus, because on a non-stationary instrument that is as load-bearing as the citation.</p>
<ul class="plain">
<li><strong>Frequency and distinctiveness</strong> — section-controlled density; log-odds
with an informative Dirichlet prior <a href="#r4">[4]</a>; rank-turbulence divergence
<a href="#r5">[5]</a>.</li>
<li><strong>Temporal structure</strong> — PELT change points <a href="#r2">[2]</a>;
Kleinberg burst detection <a href="#r1">[1]</a>; novelty / transience / resonance
<a href="#r3">[3]</a>.</li>
<li><strong>Semantics</strong> — diachronic word2vec with orthogonal Procrustes alignment
<a href="#r6">[6]</a>; semantic axis projection.</li>
<li><strong>Structure</strong> — NMF topic discovery; PPMI co-occurrence with Louvain
communities.</li>
<li><strong>Lifecycle and ranking</strong> — Kaplan-Meier survival; Bradley-Terry paired
comparison fitted by Hunter's MM algorithm <a href="#r7">[7]</a>.</li>
<li><strong>Extraction</strong> — numeric claim patterns; pairwise comparative patterns.</li>
</ul>
<h3>The primary instrument</h3>
<p>Section-controlled density is the estimator the rest of the paper leans on. For a pattern
<em>p</em> and a recap section <em>s</em>, we count matches of <em>p</em> within <em>s</em>
and divide by the word count of <em>s</em>, per period. Because Twitter and Reddit recaps
are present throughout the corpus while Discord is not, those two are the usable controls —
and running both gives two independent estimates of every result.</p>
<p>Preprocessing is justified by the artifact it removes rather than by convention. Discord
handles are blocklisted from topic modelling because the first NMF run returned topics
composed of usernames. <code>/r/LocalLlama</code>, <code>llama.cpp</code>,
<code>ollama</code> and <code>llamaindex</code> are stripped before any Llama match, because
without that "Llama" scores 100% in every period.</p>
</div></section>''')

    # ---------------------------------------------------------- 6. results
    gap_rows = [[f"<code>{C.esc(n)}</code>",
                 f"<span class='hi'>{a:g}×</span>", f"<span class='hib'>{b:g}×</span>",
                 C.esc(v)] for n, a, b, v in D.GAP]
    drift_rows = []
    for w, d, a, b, surv in D.DRIFT:
        mark = f"<b>{d:.3f}</b>" if surv else f"{d:.3f}"
        row = [f"<code>{C.esc(w)}</code>", mark, C.esc(a), C.esc(b),
               "survives" if surv else "<span class='hi'>does not</span>"]
        drift_rows.append(row)
    bt_rows = [[C.esc(n), f"{s:.2f}", str(c)] for n, s, c in D.BT[:8]] + \
              [["…", "", ""]] + \
              [[C.esc(n), f"{s:.2f}", f"<b>{c}</b>"] for n, s, c in D.BT if n in ("gemini", "claude")]
    surv_rows = [[C.esc(n), str(t), str(d), f"<b>{m} d</b>"] for n, t, d, m in D.SURVIVAL]
    val_rows = [[C.esc(w), f"{C.esc(m)} <span style='color:var(--faint)'>({C.esc(src)})</span>",
                 f"<b>{C.esc(ld)}</b>", f"<em>{C.esc(q)}</em>"] for w, m, src, ld, q in D.LEDE_VALIDATION]

    A(f'''<section><div class="col">
<span class="secnum">§ 6 — Results</span>
<h2>What survives when the source is held fixed</h2>

<h3>6.1 The agenda shift is real {tier("a")}</h3>
<p>Measured inside the Twitter recap only, the training-time → inference-time → orchestration
trajectory is unambiguous. <code>fine-tuning</code> falls 34.9 → 1.9 per 10⁴ words, RAG 22.5
→ 0.2, while <code>agentic</code> climbs 12.7 → 138.5 and <code>reasoning</code> peaks at
40.2 in 2025H1 before settling at roughly three times its 2024 baseline — the signature of a
capability absorbed into the substrate rather than abandoned.</p>
</div>
{figtop(themes_tw, 3, "Announcement space — four themes inside the Twitter recap",
  "Mentions per 10⁴ words of Twitter-recap text only, so the source is constant. "
  "Agents (oxblood) rise as fine-tuning (solid) and RAG (dashed) collapse; reasoning (teal) peaks in "
  "2025H1 and settles well above baseline.")}
{figtop(themes_rd, 4, "Practice space — the same four themes inside the Reddit recap",
  "Same patterns, same periods, different surface. Note the y-axis: practice space moves over "
  "a much narrower range. Agents rise 2.0× here against 8.0× in announcement space, and "
  "fine-tuning recovers in the final period rather than continuing to fall.")}
<div class="col">
<h3>6.2 Announcement space and practice space diverge {tier("a")}</h3>
<p>This is the study's most useful result, and it exists only because the confound in §4.2
forced us to split the corpus by surface. Twitter carries launches and claims; Reddit carries
what people are running. Comparing fold-change within each gives a per-topic measure of how
far discourse has run ahead of practice.</p>
</div>
{table(["Pattern", "Announcement (Twitter)", "Practice (Reddit)", "Reading"], gap_rows,
 "Table 4 · Fold-change 2024H1 → 2026H2, computed inside each section", (1, 2))}
{figtop(C.paired(D.GAP), 5, "The gap between what is announced and what is run",
  "Each row is one topic; the oxblood dot is announcement space, the teal dot practice space, "
  "on a log scale about no-change. A long connector means the surfaces disagree — the shift is "
  "narrative. A short one means they agree — the shift is field-wide.")}
<div class="col">
<div class="legend"><span><i class="s"></i>announcement space (Twitter recap)</span>
<span><i class="b"></i>practice space (Reddit recap)</span></div>
<p>Two readings that the whole-corpus numbers hid entirely:</p>
<ul class="plain">
<li><strong>Agents are far more an announcement phenomenon than a practice one.</strong> 8.0×
against 2.0×. The whole-corpus figure of 7.5× sat close to the announcement number only
because Twitter's share of the text was growing at the same time.</li>
<li><strong>Practitioners kept fine-tuning after the discourse stopped.</strong> Announcement
space drops 90%; practice space drops 60% and then <em>recovers</em> in the final period,
4.9 → 6.9. The technique did not die. Its news value did.</li>
</ul>
<p class="pull">Where two independent surfaces agree, you are looking at a field-wide shift.
Where they diverge, you are looking at a narrative.</p>
<p>The asymmetry is worth dwelling on because it is not what the aggregate suggests. Read on
whole-issue text, agents look like the most complete transformation in the corpus — a clean
7.5× with no retracement. Split by surface, that number decomposes into an announcement layer
running away at 8× and a practitioner layer moving at 2×. Both are real. They are simply not
the same claim, and only one of them is evidence that the work people do every day has
changed.</p>
<p>Fine-tuning inverts the same logic. In announcement space it is close to extinct by the end
of the window — 34.9 down to 1.9, a 95% fall — which read alone would suggest the technique
had been superseded. In practice space it falls to 4.9 and then climbs back to 6.9 in the
final period, while the announcement layer keeps falling. The most economical reading is that
fine-tuning became unremarkable rather than obsolete: still done, no longer written about.
Anyone sizing a market or planning a roadmap from the announcement signal alone would have
drawn the wrong conclusion twice.</p>
<p>The terms where the surfaces converge are correspondingly more trustworthy.
<code>harness</code> moves 17.9× and 16.8× — the tightest agreement of anything we measured —
which is why we treat the shift toward agent scaffolding as the single best-evidenced
structural change in the study, better evidenced than "agents" as a category.</p>
<p>By that test, agent <em>harnesses</em> (17.9× vs 16.8×) and the Chinese open-weights bloc
(8.6× vs 15.3×) are real structural changes; the broader "agentic" framing is substantially
narrative; and RAG's collapse is genuine in both.</p>

<h3>6.3 The open-weights frontier relocated {tier("a")}</h3>
<p>The largest movement in the corpus, and the only one that reproduces independently in both
surfaces with the same sign and comparable magnitude. In announcement space the Chinese bloc
(DeepSeek, Qwen, Kimi/Moonshot, GLM, MiniMax) goes 8.4 → 72.0 per 10⁴ words while Meta and
Mistral together go 26.9 → 1.3. In practice space, 6.4 → 97.8 against 65.5 → 2.4.</p>
</div>
{figtop(cross_tw, 6, "Announcement space — the crossover",
  "Chinese open-weights bloc (oxblood) against Meta + Mistral (teal), inside the Twitter recap. "
  "The crossover falls in 2025H1.")}
{figtop(cross_rd, 7, "Practice space — the same crossover, steeper",
  "Inside the Reddit recap the substitution is larger still: 15.3× against 8.6×. Practitioners "
  "moved to the Chinese open-weights stack faster than the announcement layer did.")}
<div class="col">
<p>Two details make this more than a swap of names. First, the substitution is
<em>steeper in practice space than in announcement space</em> — 15.3× against 8.6× — which is
the opposite of the agents pattern and suggests practitioners adopted the Chinese open-weights
stack ahead of the coverage rather than behind it. Second, nearly every mention carries a price
frame: <em>8% of Claude Sonnet's price</em>, <em>11% of its cost</em>, <em>10× cheaper</em>.
Price is the axis this bloc competes on in the corpus's telling, consistently, for two years.</p>
<p>The losing side did not lose on capability. Mistral raised $1.7B at an $11.7B valuation in
late 2025, and its Devstral 2 was reported beating DeepSeek v3.2 in 71% of third-party human
evaluations that December. It appears in 47% of 2026 issues. What collapsed was not its output
but its news value — a distinction the headline-level view cannot make and the density view
can.</p>
<p>Meta's decline is the case where a dramatic headline misleads. The obvious reading dates it
to the poorly-received Llama 4 in April 2025. Change point detection disagrees: the structural
breaks are <strong>October 2024</strong> and <strong>August 2025</strong>, and April 2025
falls <em>inside</em> a segment rather than on a boundary.</p>
</div>
{figtop(C.monthly_bars(D.LLAMA_MONTHLY, D.LLAMA_BREAKS), 8,
  "Llama 4 was a failed rescue, not an inflection",
  "Monthly Llama mention density. The decline from 17.2 to 5.9 predates Llama 4 by six months; "
  "the release produces a single-month spike back to 19.7, after which the collapse resumes and "
  "does not recover. PELT places no change point in April 2025.")}
<div class="col">
<h3>6.4 Core engineering terms changed referent {tier("b")}</h3>
<p>Every measure so far counts whether a word appeared. This one asks what it meant. Training
one word2vec model per half-year and aligning the spaces with orthogonal Procrustes gives a
displacement per word; the median across 4,183 shared terms is 0.313, which is the "did not
really move" line.</p>
<p>Because the corpus's genre changes with its source composition, these models are retrained
on lede + Twitter + Reddit only — Discord chat excluded from every era. Five of seven watch-list
terms survive that control; two do not, and both are reported.</p>
</div>
{table(["Term", "Drift", "Neighbours 2024H1", "Neighbours 2026H1", "Genre control"], drift_rows,
 "Table 5 · Referent drift, genre-controlled. Median drift 0.313", (1,))}
<div class="col">
<p><code>harness</code> is the clearest case: an <em>evaluation</em> harness in 2024, an
<em>agent</em> harness in 2026. A frequency series over that token sees one word used
throughout and reports continuity. It is two different concepts.</p>
<p><code>distillation</code> is the one the control strengthened — its 2026 neighbours become
explicitly <code>industrial-scale</code>, <code>copyrighted</code> and <code>laws</code>, the
vocabulary of the distillation-attack accusations of early 2026. A training technique became
a legal allegation.</p>
<div class="note"><p><strong>Practical consequence.</strong> Any keyword time series that
spans these dates aggregates two concepts and reports the sum as one trend. This is a concrete
hazard for eval suites, monitoring dashboards and retrieval corpora that live across a drift
boundary — which, in this field, most of them do.</p></div>

<h3>6.5 The median model stays in discussion for 137 days {tier("b")}</h3>
<p>Treating each model's first and last mention as a lifespan, with models still discussed at
the corpus edge right-censored, gives a Kaplan-Meier estimate over 255 models. Censoring is
the reason to use survival analysis rather than averaging: a model first seen recently and
still active has an <em>unfinished</em> life, and naive averaging would understate exactly the
newest cohort.</p>
</div>
{table(["Cohort", "Models", "Died", "Median lifespan"], surv_rows,
 "Table 6 · Kaplan-Meier survival, right-censored at 90 days of silence", (1, 2, 3))}
{figtop(C.km(D.SURVIVAL), 9, "How long a model stays in the conversation",
  "Survival curves by cohort. The Chinese-lab median of 85 days against 175 for US frontier "
  "labs is partly a naming artifact — faster version churn splits a persistent family into "
  "shorter-lived tags — so it should be read as faster iteration, not faster obsolescence.")}
<div class="col">
<p>For anything pinned to a specific checkpoint, the engineering consequence is direct: the
median relevance window in the field's own discussion is about four and a half months. That
bounds how long integration-specific tuning holds its value.</p>

<h3>6.6 The numbers the field asserted {tier("b")} {tier("c")}</h3>
<p>The prose is dense with quantitative claims that appear nowhere in the structured metadata.
Extracting them conservatively yields 1,335 context-window claims, 990 parameter counts, 176
benchmark scores and 151 prices.</p>
</div>
{figtop(C.context(D.CONTEXT_MEDIAN), 10, "Claimed context windows grew 40×",
  "Median claimed context per period, log scale. 24K to 1M tokens over the window. The "
  "vocabulary followed: by 2026 the word 'context' sits next to 'cache' and 'kv' rather than "
  "merely 'window' and 'length'.")}
{figtop(C.price(D.PRICE), 11, "The cheap frontier never moved",
  "Median claimed price per 1M tokens (oxblood) against the 10th percentile (teal); the shaded "
  "gap is the spread. The median swings 20× and back while the cheap frontier stays flat at "
  "$0.10–$0.45 throughout. Tier C: n = 151 claims, 15–35 per period.")}
<div class="col">
<p>This is the most counterintuitive result in the study and the most heavily caveated. The
median tracks <em>which models were newsworthy</em> — the 2025H1 spike coincides exactly with
the o1/o3/R1 reasoning-model period, when the models worth writing about were expensive ones —
not what inference cost. Budget capacity was continuously available across the entire window.
"Inference collapsed in price" and "a cheap tier became available" are different claims, and
only the first is contested by this data.</p>

<h3>6.7 Discourse-derived standing measures incumbency, not capability {tier("b")}</h3>
<p>The archive contains 801 dated pairwise comparative claims — "Mixtral beats GPT-3.5",
"QwQ-32B claims to match DeepSeek R1". Fitting Bradley-Terry to those gives a latent strength
per model family as asserted by the field.</p>
<p>The naive fit is dominated by <strong>launch asymmetry</strong>: a model is the claimant
when it ships and the incumbent only later, once rivals ship against it. Mean win rate is 0.68
for families with 3–7 comparisons and 0.49 for those with 41 or more, with correlation −0.27
against log comparisons.</p>
</div>
{figtop(C.scatter_bt(D.BT), 12, "The most-compared models score lowest",
  "Bradley-Terry strength against comparison count, log x-axis. Families with many comparisons "
  "(teal) cluster below strength 1.0. Claude has the most comparisons in the corpus (200) and "
  "nearly the lowest strength (0.46).")}
<div class="col">
<p>Read the two axes together and the estimand becomes clear. This is not a capability
ranking — it is an <strong>incumbency index</strong>. Being the thing everyone benchmarks
against shows up, mechanically, as losing. By this measure the corpus's reference standards
are Claude, Gemini, Mistral, Opus and GPT-5, in that order. We report it as a reinterpreted
failed measurement rather than a leaderboard.</p>

<h3>6.8 The editor called it first {tier("a")}</h3>
<p>234 issues carry a one-line "X is all you need" lede — a dated, human-written thesis. Since
none of our methods touch that field, it is independent ground truth for the automated dates.</p>
</div>
{table(["Result", "Method-derived date", "Lede date", "The lede"], val_rows,
 "Table 7 · Automated dates against the editor's own dated theses")}
<div class="col">
<p>Three of four agree closely. The disagreement is the informative one: the test-time
reasoning thesis was stated on the day o1 shipped, roughly two quarters before mention density
peaked. <strong>Interpretation leads volume</strong> — which is precisely what a volume-based
method cannot see, and a reason to keep a human-authored field in any corpus you intend to
measure.</p>
</div></section>''')

    # ---------------------------------------------------------- 7. audit
    wds = "".join(
        f'<div class="wd"><h5>{C.esc(t)}</h5><span class="was">was: {C.esc(w)}</span>'
        f'<p>{C.esc(why)}</p></div>' for t, w, why in D.WITHDRAWN)
    arows = "".join(
        f'<div class="arow"><code>{C.esc(n)}</code>'
        f'<span class="why">{C.esc(what)} — {C.esc(why)}</span>'
        f'<span class="vd {v}">{v}</span></div>' for n, what, v, why in D.AUDIT)

    A(f'''<section><div class="col">
<span class="secnum">§ 7 — Audit</span>
<h2>What did not survive</h2>
<p>A study that runs thirteen methods and withdraws none is not reporting honestly. Four
findings from earlier passes of this work were tested against the artifacts in §4 and did not
hold. They are printed here at the same weight as the results, because the pattern connecting
them is the paper's second contribution.</p>

<h3>7.1 Withdrawn</h3>
{wds}
<p>The pattern is exact: <strong>every one came from measuring a field without reading it.</strong>
Titles were treated as verdicts and turned out to be templates. Density was normalised by words
whose source inverted. A lede was discarded as boilerplate and turned out to be the most
informative field in the corpus.</p>

<h3>7.2 Weakened</h3>
<p>Whole-issue density is superseded by the section-controlled estimator for any cross-era
claim. Burst detection and novelty/resonance are restricted to within-regime comparison.
Log-odds is the weakest method here: re-run inside fixed sections, its most 2026-distinctive
token is <code>x.com</code> at z = −46.2 — the twitter.com → x.com domain migration — followed
by <code>status</code> from URL paths. The content signal exists beneath that, but URL and
template drift dominate even after source control.</p>

<h3>7.3 The open threat {tier("c")}</h3>
<div class="warn"><p>We measured the effective number of companies discussed rising roughly
fivefold (Hill-1: 21.7 → 101.8) and presented it as fragmentation. <strong>Declared sampling
breadth rose over the same window</strong> — 7 → 12 subreddits, 384 → 544 Twitter accounts.
More sources sampled mechanically yields more distinct entities. The two are confounded and we
did not control for it. The magnitude is reported as an upper bound, and the cross-validation
we previously claimed with the OpenAI headline result is correspondingly weaker. Closing this
requires per-section entity extraction rather than whole-issue tags.</p></div>

<h3>7.4 Full audit</h3>
<div class="audit">{arows}</div>
</div></section>''')

    # ---------------------------------------------------------- 8-11
    A(f'''<section><div class="col">
<span class="secnum">§ 8 — Discussion</span>
<h2>What we would tell an engineer</h2>

<h3>Read the documents before measuring the fields</h3>
<p>Three rounds of correction in this study, and none of them came from a better algorithm.
They came from opening the files. Eleven statistical methods — several of them genuinely
sophisticated, with citations reaching back to 1952 — could not surface artifacts that reading
a hundred documents found in an afternoon.</p>
<p>The failure mode generalises well beyond newsletters. If you maintain an eval suite, a
monitoring dashboard, a retrieval corpus or a trend tool over a source that changes — and
sources always change — the question that matters is not which method you run. It is whether
you have checked the semantics of the field you are counting, recently, by looking at it.</p>

<h3>Two surfaces beat one</h3>
<p>The single most valuable structural property of this corpus is that it summarises the same
day from multiple surfaces. That redundancy converted a fatal confound into the study's lead
result. If you are building a measurement pipeline, the design implication is direct: prefer
two partial views you can cross-check over one comprehensive view you cannot.</p>

<h3>Declining coverage usually means victory</h3>
<p>Retrieval, reasoning and multimodality all fell sharply after peaking, and all three won —
they became substrate. Genuine non-arrivals look different: they never peak at all. The
diligence question for any technology in this corpus is not "is coverage falling" but "did it
peak first".</p>

<h3>Absorption has a signature, and it is the peak</h3>
<p>The hardest interpretive problem in this corpus is that winning and losing look identical in
a falling line. Retrieval fell 99%; so did several things that simply did not work. The
discriminator turns out to be whether the line peaked first, and how the vocabulary around it
behaves afterwards. Reasoning peaked at 40.2 and settled near 14 — but the word's embedding
neighbours in 2026 are <code>multilingual</code>, <code>spatial</code> and
<code>instruction-following</code>, which are the neighbours of a property models are assumed
to have, not of a research frontier. That is what absorption looks like from the inside.</p>

<h3>Where the scarce resource sits now</h3>
<p>Read as a whole, the trajectory is an argument about system design with dates attached.
Model quality stopped being the binding constraint somewhere in 2024; context became the
constraint through 2025; orchestration and cost are the constraint at the end of the window.
The rise of <code>harness</code> — matched almost exactly across both surfaces, the strongest
agreement of any term we measured — is the clearest single signal of where engineering effort
actually moved.</p>
</div></section>

<section><div class="col">
<span class="secnum">§ 9 — Threats to validity</span>
<h2>What could still be wrong</h2>
<h4>Construct</h4>
<p>Reported attention is not field activity, and neither is deployment. The corpus measures one
publication's summary of three social surfaces.</p>
<h4>Internal</h4>
<p>Four publishing regimes; the source-composition inversion; title and lede templating; a
pipeline that is LLM-drafted and human-edited in a mix that changes over time; regex surface
matching throughout; claim subjects unresolved, so §6.6 reports field-level distributions
rather than per-model values.</p>
<h4>External</h4>
<p>One editorial viewpoint, weighted toward builders and open-model tooling. Enterprise
deployment, hardware supply chains and non-English ecosystems are systematically under-covered.
Robotics never exceeds 12% of issues in any period, which we read as a limit of the instrument
as much as a fact about the field.</p>
<h4>Statistical</h4>
<p>Thin end periods (2023H2 and 2026H2 are ~0.2M words each); multiple comparisons across many
entities without correction; Bradley-Terry strengths identifiable only within the largest
connected component; survival cohorts affected by version-naming conventions.</p>
</div></section>

<section><div class="col">
<span class="secnum">§ 10 — Future work</span>
<h2>What is left</h2>
<ul class="plain">
<li><strong>Per-section entity extraction</strong> to close the fragmentation confound in §7.3.
This is the highest-priority open item.</li>
<li><strong>The Discord telemetry.</strong> 2.15M messages across 56 servers with per-channel
daily counts, entirely unanalysed. It is the natural third surface for the announcement/practice
split — a deeper practice space than Reddit — for the periods where it exists.</li>
<li><strong>Causal impact estimation</strong> for discrete events such as R1. Blocked on
constructing a control set that is genuinely unaffected, which in a field this coupled is the
actual work.</li>
<li><strong>Dynamic topic models</strong> chained through time, which could represent a topic's
vocabulary turning over while the topic persists — the formal version of the absorption claim.</li>
<li><strong>Family-level survival grouping</strong> and claim-subject resolution.</li>
</ul>
</div></section>

<section><div class="col">
<span class="secnum">§ 11 — Conclusion</span>
<h2>Two results, equally load-bearing</h2>
<p>Substantively: over 690 days the field's agenda moved from training to inference to
orchestration; the open-weights frontier relocated so completely that the ratio between the
Chinese bloc and Meta-plus-Mistral inverted by two orders of magnitude in both independent
surfaces; five core engineering terms changed referent; and the median model holds the field's
attention for about 137 days. Most usefully, announcement space and practice space can be
measured separately, and they disagree by a factor of four on agents while agreeing almost
exactly on harnesses.</p>
<p>Methodologically: this corpus produced four confident, wrong findings from measures that
looked entirely reasonable, and no amount of algorithmic sophistication caught any of them.
Reading the documents did. We would not have trusted the first paragraph without the second,
and we would suggest no one else does either.</p>
</div></section>

<section><div class="col">
<span class="secnum">References</span>
<ol class="refs">
<li id="r1">Kleinberg, J. (2002). Bursty and hierarchical structure in streams. <em>KDD</em>.</li>
<li id="r2">Killick, R., Fearnhead, P., &amp; Eckley, I. (2012). Optimal detection of changepoints
with a linear computational cost. <em>JASA</em>.</li>
<li id="r3">Barron, A., Huang, J., Spang, R., &amp; DeDeo, S. (2018). Individuals, institutions
and innovation in the debates of the French Revolution. <em>PNAS</em>.</li>
<li id="r4">Monroe, B., Colaresi, M., &amp; Quinn, K. (2008). Fightin' words: lexical feature
selection for identifying content. <em>Political Analysis</em>.</li>
<li id="r5">Dodds, P. et al. (2020). Allotaxonometry and rank-turbulence divergence.
<em>EPJ Data Science</em>.</li>
<li id="r6">Hamilton, W., Leskovec, J., &amp; Jurafsky, D. (2016). Diachronic word embeddings
reveal statistical laws of semantic change. <em>ACL</em>.</li>
<li id="r7">Bradley, R., &amp; Terry, M. (1952). Rank analysis of incomplete block designs.
<em>Biometrika</em>. Fitted by Hunter, D. (2004), <em>Annals of Statistics</em>.</li>
</ol>
<div class="foot">
Corpus: 690 issues, 2023-12-06 → 2026-08-06, reconstructed from the publisher's site.<br>
All figures generated from measured series; every value traces to a file under
<code>analysis/</code>. Code and intermediate outputs are in the repository.<br>
Evidence tiers: A = reproduces in two independent source sections · B = single method,
controlled · C = confounded, reported as a bound · ✗ = withdrawn.
</div>
</div></section>
</div>''')
    return "".join(H)


TITLE = ("Announcement Space and Practice Space — "
         "690 days of AI's daily record, source-controlled")
DESC = ("A source-controlled study of 690 daily AI newsletters, 2023-2026: how the field "
        "evolved, and how four confident findings turned out to be measurement artifacts.")

# The Artifact host supplies its own <!doctype>/<head>/<body>, so the default build emits a
# fragment. GitHub Pages needs a complete document, hence --standalone.
SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="light dark">
<meta property="og:type" content="article">
<meta property="og:title" content="Announcement Space and Practice Space">
<meta property="og:description" content="{desc}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20viewBox%3D%270%200%2016%2016%27%3E%3Ctext%20y%3D%2713%27%20font-size%3D%2713%27%3E%F0%9F%93%B0%3C%2Ftext%3E%3C%2Fsvg%3E">
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""


if __name__ == "__main__":
    standalone = "--standalone" in sys.argv
    body = build()
    if standalone:
        html = SHELL.format(title=TITLE, desc=DESC, css=CSS, body=body)
        out = pathlib.Path(__file__).resolve().parent.parent / "site" / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
    else:
        html = f"<title>{TITLE}</title>\n<style>{CSS}</style>\n{body}"
        out = OUT
    out.write_text(html, encoding="utf-8")
    kind = "standalone document" if standalone else "artifact fragment"
    print(f"wrote {out} — {len(html):,} bytes ({kind})")
