"""The book's text. One entry per page; the generator does layout and navigation.

Every number here traces to a file under analysis/. Where a claim was later
withdrawn or reversed, the book says so in the text rather than quietly dropping
it — the corrections are part of the argument.
"""
from __future__ import annotations

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "report"))

import charts as C  # noqa: E402
import data as D  # noqa: E402
import figs as F  # noqa: E402

TITLE = "Written Forwards"
SUB = ("Three years of AI, as the field saw it happen — "
       "and how to tell what was real")


# ---------------------------------------------------------------- helpers

def fig(svg, n, title, note):
    return (f'<figure><figcaption><b>Figure {n} · {C.esc(title)}</b>{note}</figcaption>'
            f'{svg}</figure>')


NUM = ' class="n"'


def table(head, rows, caption, nums=()):
    th = "".join("<th" + (NUM if i in nums else "") + f">{h}</th>"
                 for i, h in enumerate(head))
    body = ""
    for r in rows:
        body += "<tr>" + "".join("<td" + (NUM if i in nums else "") + f">{c}</td>"
                                 for i, c in enumerate(r)) + "</tr>"
    return (f'<div class="tw"><table><caption>{caption}</caption>'
            f'<thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>')


# ---------------------------------------------------------------- contents

# kind, number, title, driving question, slug (None = not yet drafted)
CONTENTS = [
    ("part", "Part I — The record"),
    ("ch", "1", "A field talking to itself",
     "What is this thing, and why would anyone read three years of a newsletter?", "ch1"),
    ("ch", "2", "Three surfaces",
     "Why does everything in this field feel like hype?", "ch2"),
    ("inter", "I", "The day I measured the newsletter instead of the field",
     "On checking what the field you are counting actually contains.", "interlude-1"),

    ("part", "Part II — What happened"),
    ("ch", "3", "Everyone is fine-tuning",
     "What did the field think the job was?", "ch3"),
    ("ch", "4", "The road not taken",
     "What does it look like when a good idea simply does not arrive?", "ch4"),
    ("ch", "5", "Learning to think",
     "How does a whole field change its mind in four months?", "ch5"),
    ("ch", "6", "Seven days in January",
     "What does it look like when something actually breaks through?", "ch6"),
    ("ch", "7", "The harness",
     "When did the field stop talking about models and start talking about the "
     "software around them?", "ch7"),
    ("ch", "8", "The handover",
     "How does a technological lead change hands?", "ch8"),
    ("ch", "9", "Containment",
     "What happens after the capability race?", "ch9"),
    ("inter", "II", "The day the corpus changed shape underneath me",
     "On measuring a document whose composition inverted.", "interlude-2"),

    ("part", "Part III — What it means"),
    ("ch", "10", "How ideas die",
     "Retrieval fell 99%. So did things that failed. How do you tell?", "ch10"),
    ("ch", "11", "How the field keeps score",
     "Which benchmarks are worth believing, and for how long?", "ch11"),
    ("ch", "12", "When words change meaning",
     "Is <code>agent</code> in your 2026 dashboard the same <code>agent</code> "
     "you started counting in 2024?", "ch12"),
    ("ch", "13", "Where practitioners spent their attention",
     "If announcements are unreliable, what were the other rooms talking about?", "ch13"),
    ("ch", "14", "The half-life of a dependency",
     "You are about to build on a model. How long will it stay relevant?", "ch14"),
    ("inter", "III", "The six things I got wrong",
     "Consolidated, with what each one cost.", "interlude-3"),

    ("part", "Part IV — Reading forwards"),
    ("ch", "15", "The unit of observation",
     "Why did none of this get caught by better statistics?", "ch15"),
    ("ch", "16", "How to read a field",
     "What do you do on Monday?", "ch16"),
]


# ---------------------------------------------------------------- chapter 1

CH1 = """
<p class="first">On the evening of 6 December 2023, someone published a summary of what the
internet had said about AI that day. It ran to a few thousand words, it was assembled
mostly out of Discord logs, and it opened by apologising for itself.</p>

<blockquote><p>Hi alpha testers! That's right, there's now a custom intro for these
newsletters. We're very flattered that hundreds of you have somehow found this crappy
MVP and so I decided to put in a little last-mile human touch commentary.</p>
<cite>AI News, issue 1</cite></blockquote>

<p>The headline that day was a question — <em>Is Google's Gemini… legit?</em> Gemini had
launched the previous afternoon to an enormous marketing push, and the issue's verdict was
that the marketing was great and the headline benchmark number was suspicious, because the
MMLU claim rested on 32-shot chain-of-thought prompting rather than the single-shot number
everyone else reported. Then it says something that no retrospective would ever contain:</p>

<blockquote><p>We will know more on Dec 13th.</p></blockquote>

<p>It did not know. That is the entire value of the thing.</p>

<h2>The artifact</h2>

<p>The newsletter is called <em>AI News</em>. It ran from that first issue to 6 August 2026,
which is where this book's copy of the archive stops — <strong>690 issues, 15,265,094
words</strong>, covering 82% of the weekdays in between. The median issue is about 24,000
words long, which is a third of a short novel, published daily, about the previous day.</p>

<p>Each issue reads the same set of places and summarises them separately: a Twitter recap
built from a declared list of accounts, a Reddit recap from a declared list of subreddits, and
— until March 2026 — a Discord recap assembled from message logs across dozens of servers.</p>

<p>A note on dates, since they will matter. Every date in this book is the day an issue
<em>covers</em>, not the day it was sent — an issue about Monday goes out on Tuesday morning,
and the archive stores both. The covered day is the one that matters for a chronology, so that
is the one used throughout.</p>

<p>Each issue also tells you, every single day, exactly what it looked at:</p>

<blockquote><p>AI News for 12/1/2025-12/2/2025. We checked 12 subreddits, 544 Twitters and 24
Discords (205 channels, and 9665 messages) for you. Estimated reading time saved (at 200wpm):
697 minutes.</p>
<cite>AI News, standard header</cite></blockquote>

<p>That header is printed 690 times and it is the most useful line in the whole corpus: a
source that declares its own sampling frame, daily, is a rare thing and it makes an enormous
amount possible.</p>

<p>It is worth being exact about who wrote what, because the two halves of an issue are not the
same kind of text. The recaps underneath the header are model-generated from the sampled
sources. The passage <em>above</em> it — the headline, the opening claim, the judgement about
what mattered that day — is written by a person, and across the whole archive it comes to
<strong>124,977 words, or 0.81% of the corpus</strong>. Everything else is summary.</p>

<p>You can watch the seam. The human passage regularly argues with the summaries below it, and
it is the only place in the corpus where anyone commits to an opinion that could later look
foolish.</p>
"""

CH1_B = """
<p>It is not a steady artifact, and the shape of the unsteadiness is the first thing worth
knowing about it. Issue length nearly quadrupled in the first six months as the Discord
sampling widened, held around 25,000 words for two years, and then <strong>collapsed by a
factor of five in the second quarter of 2026</strong>, when the newsletter dropped the
Discord recap entirely. The cadence barely moved through all of it — roughly 65 issues a
quarter, start to finish.</p>

<p>That collapse matters more than it looks. An issue in early 2024 is mostly a digest of
chat logs; an issue in mid-2026 is mostly a digest of forum threads and tweets. They are not
the same kind of document, and anything you count across both is partly counting the
change.</p>

<h2>Why a source written forwards is worth anything</h2>

<p>Almost everything written about the last three years of AI was written backwards. It was
written after DeepSeek R1, after the agent turn, after the Chinese open-weights labs took
the lead — and so it is organised around the things that turned out to matter. That is what
history is for, and it is also why it is nearly useless for the question this book asks,
which is not <em>what happened</em> but <em>how could you have known</em>.</p>

<p>A daily archive is different in kind. It contains, in dated form:</p>

<ul>
<li><strong>The wrong guesses, uncorrected.</strong> Nobody went back and deleted the
enthusiasm for architectures that never arrived. It is all still there, at full volume, with
timestamps.</li>
<li><strong>The relative weight of things.</strong> A retrospective tells you MCP mattered.
The archive tells you that when Anthropic published it on 25 November 2024, the issue's lede
was a joke about a config file, and it took four months for anyone to care.</li>
<li><strong>The stuff that never became a story at all.</strong> Most of what a field
discusses does not resolve into a narrative. It just stops. That absence is only visible in
a source that recorded the presence.</li>
</ul>

<p class="pull">History is written backwards, once the winners are known. This archive was
written forwards, with the wrong guesses intact. That is the only reason it is worth
reading.</p>

<h2>What this is not</h2>

<p>Being honest about the limits early is not throat-clearing; it changes what the rest of
the book is allowed to claim.</p>

<div class="aside">
<h4>The estimand</h4>
<p>Every number in this book measures <strong>attention within one curated view of a field's
public conversation</strong>. Not deployment. Not revenue. Not capability. When you read
that fine-tuning fell by 95%, that means the newsletter's Twitter recap devoted 95% less of
its text to fine-tuning — while over exactly that window the busiest community anywhere in the
archive was a fine-tuning toolchain with 302,248 messages. Both facts are true. Neither one is
“fine-tuning declined.”</p>
</div>

<p>The three surfaces this book compares have short names and longer, more accurate ones,
and it is worth fixing both in mind now, because the short names do the work of memory and the
long names do the work of truth:</p>

<div class="aside">
<h4>What the three surfaces actually are</h4>
<p><strong>Announcement space</strong> is lab-linked Twitter discourse: 544 accounts on one
editor's list, summarised by a model.<br>
<strong>Community space</strong> is sampled Discord activity: message volume in 56
English-language servers, which measures how busy a room was, not what software anyone ran.<br>
<strong>Practice space</strong> is local-model Reddit discourse: 12 subreddits weighted heavily
toward people running models on their own hardware.</p>
<p>A gap between them is evidence about <em>where a subject was being discussed</em>. It is a
lead worth investigating, not a measurement of adoption, and nowhere in this book is it ground
truth about what was deployed.</p>
</div>

<p>There is one more limit, and it is the sharpest, because it sets a floor under every
number in this book. <strong>The recaps are written by a language model, and the model
changed.</strong> The archive says which one, in a line under each heading — <em>all recaps
done by Claude 3 Opus, best of 4 runs</em> — and across the corpus that line names eight
different model families for the Discord recap alone, while 384 of 613 issues never declare
the Twitter summarizer at all. Holding the recap heading fixed holds the <em>source</em>
fixed; it does not hold the instrument fixed.</p>

<p>How much does that matter? Three days were published twice, the same news summarised by two
different models — 13 May 2024, 18 July 2024, 6 August 2024. Comparing pattern densities
between the two editions of one day varies the instrument while holding the news constant, and
the answer is a <strong>median of 1.23×, with a maximum of 2.40×</strong>. So a fold-change of
1.2 is indistinguishable from a summarizer swap, and one of 5.5 is not. Wherever this book
leans on a ratio, that is the noise floor it is leaning against.</p>

<p>There are three further limits worth stating plainly. The archive is one editor's view,
with one editor's taste; it over-weights the English-language, US-and-China, open-weights-adjacent
conversation and largely misses enterprise procurement, academic publishing outside the
poster-on-Twitter tier, and everything happening in Chinese-language forums. Its sampling
frame widened over time — 7 subreddits to 12, 384 Twitter accounts to 544 — which means any
count of <em>distinct things mentioned</em> is partly counting the newsletter's own appetite.
And it stops. Discord coverage ends in March 2026; the copy of the archive behind this book
ends in August 2026. Anything that looks like a decline after those dates is the instrument.</p>

<p>What is left, after all of that, is still remarkable: a dated, daily, self-describing record
of what one fast-moving technical field paid attention to, across nearly a thousand consecutive
days, written by people who did not know how it ended. Everything that follows is an attempt to
read it carefully — starting with the fact that it is not one record but three, kept side by
side, and that they disagree.</p>
"""


# ---------------------------------------------------------------- chapter 2

CH2 = """
<p class="first">On 5 February 2026 the newsletter's Twitter recap opens like this:</p>

<blockquote><p>GPT-5.3-Codex shipped in Codex … framed as advancing frontier coding and
professional knowledge in one model. Community reaction highlighted that token efficiency and
inference speed may be the most strategically important delta versus prior generations, with
one benchmark claim: TerminalBench 2 = 65.4% … Reported efficiency improvements: 2.09× fewer
tokens versus GPT-5.2-Codex-xhigh on SWE-Bench-Pro, and together with ~40% speedup implies
2.93× faster at ~+1% score.</p>
<cite>AI News, Twitter recap, 2026-02-05</cite></blockquote>

<p>The Reddit recap in the same issue, covering the same day, opens like this:</p>

<blockquote><p><strong>Anyone here actually using AI fully offline?</strong> Running AI models
fully offline is feasible with tools like LM Studio, which allows users to select models from
Hugging Face based on their hardware capabilities, such as GPU or RAM … While coding workflows
may need more powerful setups, consulting tasks can be managed with models like
<code>gpt-oss-20b</code> in LM Studio.</p>
<cite>AI News, Reddit recap, 2026-02-05</cite></blockquote>

<p>Same publication, same day, same editor. Two populations who are not having the same
conversation, and are not close to having the same conversation. One is comparing frontier
coding models on token efficiency; the other is asking whether a 20-billion-parameter model on
a home machine is good enough to be useful without an internet connection.</p>

<p>Neither is wrong. But if you read only the first one — and the first one is what arrives in
your feed, your inbox and your board deck — you will believe things about this field that the
second one would have corrected.</p>

<h2>Three surfaces</h2>

<p>The archive does this every day, structurally, because each issue summarises the same
twenty-four hours from three different places and keeps them separate:</p>

<ul>
<li><strong>The Twitter recap</strong> — a declared list of accounts, heavy on labs, founders
and researchers. This is <em>announcement space</em>: what the field said about itself,
mostly by the people with something to launch.</li>
<li><strong>The Discord recap</strong> — message logs from dozens of communities. This is
<em>community space</em>: what people said to each other while building.</li>
<li><strong>The Reddit recap</strong> — mostly LocalLLaMA and its neighbours. This is
<em>practice space</em>: people running models on their own hardware, reporting what
happened.</li>
</ul>

<p>Three views of one day, produced by three populations with three different incentives, and
kept separate on the page. Nobody designed this as a measuring device. It is one anyway.</p>

<p>There is a fourth layer, and it is different in kind. Above all three recaps sits a short
passage written by the editor — the headline claim, the judgement, the argument. It is thin,
124,977 words against 15.4 million, and where the other three sample a <em>population</em>, this
one samples a <em>person</em>. That makes it a confound when you are measuring the field and a
signal when you are measuring the coverage, and it is worth keeping separate for both
reasons.</p>

<h2>The measurement</h2>

<p>The method is deliberately dull. Take a pattern — a regular expression for
<code>agentic|agents?</code>, say — and count how often it occurs per ten thousand words
<em>inside a single named recap section</em>, half-year by half-year. Because the section is
fixed, the population writing it is roughly fixed too, and a change in the number is a change
in what that population talked about rather than a change in the document around it.</p>

<p>Measuring across the whole issue instead would not work, and the reason is worth one
sentence: the mix of sources inside an issue changes enormously over three years, so a
whole-issue count partly measures which surface the newsletter happened to be sampling that
year. Holding the section fixed removes that. The section is the unit throughout this book.</p>

<p>Run it on the two most promoted ideas of the period and the result is not subtle.</p>
"""

CH2_B = """
<p>Agents rise 5.5× in announcement space between the first half of 2024 and the first half
of 2026. In community space, 3.0×. Among people running models on their own machines,
<strong>1.2×</strong> — which is to say, essentially not at all.</p>

<p>Reasoning, measured the same way, does <em>not</em> do this: 1.2× in announcement space,
2.1× in community space, 1.4× in practice. Two of those three are at or below the 1.23× that a
summarizer swap alone produces, so the honest reading is that this test cannot separate
reasoning's trajectory from its own instrument. The staircase is flat and may not be a
staircase at all. That is the method declining to confirm a theme, which is the only reason to
trust it when it does confirm one.</p>

<div class="warn">
<p><strong>How much of that staircase is the baseline?</strong> More than I would like. The
comparison starts at 2024H1 because that is where the corpus's section headings settle, which
is a reason unrelated to the answer — but it is not the only defensible start. Run the same
measurement from the stable publishing regime that begins on 20 May 2024 and the agent
gradient gets steeper: 6.8× announcement against 1.1× practice. Run it from 2024H2 and it
<em>vanishes</em>: 3.6× against 3.7×.</p>
<p>The practice-side baseline is doing the work. The Reddit recap in the first half of 2024 is
only 30,947 words, and its agent density is three times its 2024H2 value, which suppresses the
fold. So the honest statement of this chapter's central finding is narrower than the number
suggests: <strong>agents rose far more in announcement space than in practice space on two of
three baselines, and equally on the third.</strong> Of every gradient in this book, only RAG's
survives all three. <code>analysis/methods/sensitivity.py</code> runs the comparison.</p>
</div>

<p>That descending staircase is what hype looks like when you can measure it. It is not that
agents are fake; it is that the further you get from the people with something to announce,
the smaller the change becomes. If you only ever read announcement space — and announcement
space is what shows up in your feed, your inbox and your board deck — you are reading the
largest of three numbers and believing it is the only one. That much is worth knowing even
where the exact ratio is not stable, because the direction of the error is always the same.</p>

<h2>The part that makes it a tool</h2>

<p>If every pattern behaved that way, this would be a complaint about marketing rather than a
method. The useful discovery is that <strong>some patterns run the other way</strong>.</p>
"""

CH2_C = """
<p>The Chinese open-weights bloc — Qwen, DeepSeek, Kimi, GLM, MiniMax — rises 4.6× in
announcement space and <strong>9.0× in practice space</strong>, with community space higher
still at 9.9×. Practitioners were running those models, in volume, before the announcement
layer had adjusted to them. Quantization is the same shape in miniature: down 20% in
announcement space, up 10% in practice. Both are cases where the coverage was behind the
ground.</p>

<p>And some things fall everywhere at once. Retrieval-augmented generation drops by roughly
90% in all three surfaces. Fine-tuning falls hardest in announcement space (to a tenth) and
much less in practice (to a third) — which is the signature of something that stopped being
newsworthy while remaining a job people do.</p>

<p>So the gradient sorts shifts into three kinds, and the sorting is the whole point:</p>

<div class="aside">
<h4>The test</h4>
<p><strong>If a shift shrinks as you approach the people doing the work, the announcement
layer is ahead of the practitioner layer.</strong> Discount it, and go looking for why.<br>
<strong>If it grows as you approach them, practitioners are discussing something the coverage
has not caught up with.</strong> That is the one worth investigating early.<br>
<strong>If it moves about the same everywhere, treat it as a field-wide signal</strong> — and
triangulate it against something that is not discourse before you act.</p>
<p>None of the three tells you what was deployed. All three tell you where to point the next
question, which is a more useful thing than it sounds and a smaller one than it reads.</p>
</div>

<p>You can run this without an archive. The surfaces exist for every technical field: there
is always a layer where things are announced, a layer where practitioners talk to each other,
and a layer where people report what broke. Pick two you can read regularly, and measure the
same claim in both. Two partial views you can cross-check beat one comprehensive view you
cannot — which is, in one sentence, the methodological argument of this entire book.</p>

<h2>Why the surfaces disagree</h2>

<p>It is worth being precise about the mechanism, because “hype” is a lazy explanation and
the real one is more useful.</p>

<p>Announcement space has a launch schedule. Its population is rewarded for novelty, and its
volume is roughly proportional to how much capital is chasing a category. Practice space has
a hardware constraint. Its population is rewarded for things that work on a 24GB consumer
card tonight, and its volume is proportional to how many people are actually doing the thing.
Neither is the truth. Announcement space genuinely leads on things that require a frontier
lab to make — reasoning models did arrive, months after they were announced. Practice space
genuinely leads on things that require nothing but a download, which is exactly why it saw
the Chinese open-weights models first.</p>

<p class="pull">The gap between the surfaces is not error. It is the lag between what
something costs to announce and what it costs to run.</p>

<p>Go back to 5 February 2026 with that in mind. The Twitter recap is measuring token
efficiency on SWE-Bench-Pro because its population ships models and needs a number. The Reddit
recap is asking whether a 20-billion-parameter model is good enough offline because its
population owns one graphics card and no budget. Neither is reporting on the other. Read both
for a month and the gap between them tells you more than either does alone — and it is the only
thing in this book you can reproduce without an archive, starting tomorrow, with two browser
tabs.</p>
"""


# ---------------------------------------------------------------- interlude I

INT1 = """
<p class="first">The first real finding I had, and the one I was most pleased with, was that
OpenAI had collapsed.</p>

<p>It was a simple measurement. Every issue has a headline. Count the share of headlines that
name each company, half-year by half-year, and you get a clean series for who was leading the
news. OpenAI ran at about 18% of headlines through 2024 and fell to roughly 4% by 2026. Meta
did something similar. Meanwhile the total number of distinct companies named across the
corpus rose steeply. It made a coherent story, it fit everything I thought I knew, and it had
an obvious headline of its own: <em>the field fragmented, and the incumbents lost the
narrative</em>.</p>

<p>Then I read some headlines.</p>

<hr class="sep">

<p>Here are four consecutive titles from March 2026, exactly as the archive stores them:</p>

<blockquote><p>not much happened today<br>
not much happened today<br>
not much happened today<br>
not much happened today</p></blockquote>

<p>Underneath those four issues, among other things, were an agent launch from Replit, an
essay on raising your expectations of language models, and an NVIDIA GTC keynote announcing a
trillion-dollar sale. The phrase is not a description. It is what sits in the
<code>title</code> field when nothing else does, and the share of issues carrying it climbs
steadily across the corpus: 8% in late 2023, 27% by the second half of 2024, 46% through late
2025, <strong>85%</strong> in the final months.</p>

<p>My series was not measuring which companies led the news. It was measuring <em>how often
the title field got filled in</em>. And because the templating ramped up over exactly the
window I was studying, the artifact and the trend were indistinguishable. Every company's
headline share fell. I had picked the two I expected to fall and written a story about them.</p>

<h2>What actually went wrong</h2>

<p>Not the statistics. The statistics were fine — the counts were correct, the periods were
right, the differences were far outside anything noise could produce. The mistake happened
one step earlier, in the assumption that the <em>title</em> field contained a title.</p>

<p>This turns out to be the general shape of the problem, and it recurs throughout this book.
A field in a dataset has a name, and the name implies a meaning, and the meaning is stable
until one day it silently is not. Nothing errors. Nothing looks anomalous. The series just
quietly starts measuring something else, and every downstream method — every regression,
every change-point detector, every significance test — faithfully processes the new thing
using the old label.</p>

<p class="pull">There is no statistical test for “this field stopped meaning what it used to
mean.” There is only reading it.</p>

<h2>The same mistake, one level down</h2>

<p>That is where this interlude ended for several months, and it was still wrong.</p>

<p>What I had been reading was not the newsletter. It was a public mirror of the newsletter,
and I had never checked it against the thing it mirrored. When I finally went back to the sent
emails — the issues as they actually landed in an inbox — the four titles above were not what
anyone received. They went out as <em>Replit Agent 4: The Knowledge Work Agent</em>, <em>The
high-return activity of raising your aspirations for LLMs</em>, <em>Context Drought</em>, and
<em>NVIDIA GTC: Jensen goes hard on OpenClaw, Vera CPU, and announces $1T sale</em>.</p>

<p>Of the 397 issues I could eventually recover, <strong>80</strong> that the archive files
under a templated title had been published under a real headline — 84 of them. In the first half of 2026 the
templated share of what was actually sent is <strong>4.6%</strong>, against the 64% the archive
stores.</p>

<p>Which looks like a clean verdict: the mirror invented the trend. It is not, and the way it is
not is the more useful lesson. Compare the two series on the same issues:</p>

<div class="tw"><table><thead><tr><th>Half-year</th><th class="n">Archive says templated</th>
<th class="n">Actually sent that way</th></tr></thead><tbody>
<tr><td>2024H2</td><td class="n">26.9%</td><td class="n">28.6%</td></tr>
<tr><td>2025H1</td><td class="n">38.1%</td><td class="n">38.1%</td></tr>
<tr><td>2025H2</td><td class="n">45.7%</td><td class="n">41.0%</td></tr>
<tr><td>2026H1</td><td class="n">64.3%</td><td class="n"><b>4.6%</b></td></tr>
<tr><td>2026H2</td><td class="n">84.6%</td><td class="n"><b>24.0%</b></td></tr>
</tbody></table></div>

<p>Through 2024 and 2025 the two agree closely — exactly, in the first half of 2025, across
118 issues. The climb from 27% to 41% is <em>real</em>: the editor genuinely did reach for the
template more and more, and my original series was tracking something that was happening. Only in 2026 do the columns come apart, and
there they come apart in two directions at once: the mirror began writing placeholders in the
same months the editor went back to writing headlines. One movement was hidden underneath its
opposite.</p>

<p>The commentary underneath shows the same double motion. The mirror replaced it with the words
<em>a quiet day</em> on 104 issues in 2026, and restoring those from the sent emails moves the
typical issue's opening from three words back to 183. But the genuine thinning through 2025 — a
median of 190 words in late 2024, 92 by early 2025, 72 by late 2025 — survives the correction
untouched. It was real, and the mirror's failure was layered on top of it.</p>

<p class="pull">The first correction caught a field that had changed meaning. The second caught
a real trend and an artifact of the copy, superimposed, moving opposite ways.</p>

<h2>What survived</h2>

<p>There is no fix that rescues the original series. The stored title cannot be repaired, and
the published subject lines exist only for the last seven months of the corpus, which is
another way of saying that the measurement I wanted cannot be made across the window I wanted
it for. The OpenAI collapse disappears either way, and so does most of the fragmentation story
built on top of it.</p>

<p>What survived was the thing I had not built a story around: measurements taken inside the
body of the issues, in fixed sections, where the population writing the text was held constant.
Those sections came through the mirror intact — byte-identical to the sent emails on every
issue I could check, which is why the rest of this book still stands. That is the instrument
used everywhere here, and the reason it is used is that the obvious alternative failed first,
and then failed again underneath.</p>

<p>The general form of the lesson is short enough to keep. <strong>Before you measure a field,
read enough of it to know what your fields contain.</strong> Not the schema — the values.
Twenty issues, spread across the range, read properly. It takes an afternoon and it is the only
check that catches this class of error at all.</p>
"""


# ---------------------------------------------------------------- chapter 3

CH3 = """
<p class="first">In the first half of 2024, <code>fine-tuning</code> appears 25.6 times per
ten thousand words of the newsletter's Twitter recap, and retrieval-augmented generation runs
higher still at 30.9 — the two densest themes in announcement space that half-year. Together
that is a mention every hundred and eighty words, every day, for six months. Between them they are the
architecture: take an open model, tune it on your data, put a vector database in front of it,
ship.</p>

<p>Two and a half years later, in announcement space, fine-tuning is at 1.9 and RAG is at 0.2.
The default architecture of 2024 essentially stopped being discussed.</p>

<p>The obvious reading — the field tried fine-tuning and RAG, and they did not work — is
wrong for both, and wrong in two different ways. This chapter is about the world before any of
that happened — what the job looked like when the answer to almost every question was
<em>take an open model and change it</em>.</p>

<h2>December 2023: the Mixtral rush</h2>

<p>Mistral released the weights for an eight-expert mixture-of-experts model by posting a
magnet link — no paper, no code, no inference implementation. Two days later the newsletter
opened with this:</p>

<blockquote><p>Happy Friday. 3 new models are the talk of the town today: Mistral's new 8x7B MoE
model (aka “Mixtral”) — a classical attention model, done well … Mamba models, a range of models
up to 3B by Tri Dao of Together … StripedHyena 7B — a descendant of the subquadratic attention
replacement Hyena out of Stanford's Hazy Research lab … that is finally competitive with
Llama-2, Yi, and Mistral 7B.</p>
<p>This is all very substantial and shows what happens when you <strong>ship model weights
instead of heavily edited marketing videos</strong>.</p>
<cite>AI News, 2023-12-08</cite></blockquote>

<p>That last line is the field's value system in one sentence, written two days after a
much-criticised launch video from a much larger company. It is also a fair summary of what the
next eighteen months rewarded.</p>

<p>The headlines that week run: <em>The Mixtral Rush</em> on the 9th, describing independent
groups racing to write the inference code from scratch overnight so anyone could run the thing;
<em>Mixtral beats GPT3.5 and Llama2-70B</em> on the 11th; <em>Mixtral-Instruct beats Gemini
Pro</em> on the 15th. Seven days from an unexplained file to a model beating the previous
generation's frontier, and a community whose reflex was to reimplement rather than wait.</p>

<div class="aside">
<h4>Mixture of experts, as the field met it</h4>
<p>A dense model runs every parameter for every token. A mixture-of-experts model has many
parallel sub-networks and a small router that picks two of them per token, so a model with
47 billion parameters does the work of about 13 billion at inference time. You pay in memory
— all the experts have to be resident — and save in compute. That trade is why MoE became
the default frontier architecture, and why it arrived first in a community that had more VRAM
than patience.</p>
</div>
"""

CH3_B = """
<h2>The vocabulary of a field that thought the job was tuning</h2>

<p>Read the titles from early 2024 in sequence and what you notice is that nearly all of them
are about <em>modifying</em> models rather than <em>using</em> them:</p>

<blockquote><p>LlaMA Pro — an alternative to PEFT/RAG??<br>
Mixing Experts vs Merging Models<br>
TIES-Merging<br>
Help crowdsource function calling datasets<br>
FSDP+QLoRA: the Answer to 70b-scale AI for desktop class GPUs<br>
The Dissection of Smaug (72B)</p>
<cite>AI News headlines, January–February 2024</cite></blockquote>

<p>Each of those is a technique for getting more out of weights you did not train. LoRA —
low-rank adaptation — freezes the original model and trains a small pair of matrices alongside
it, so a consumer GPU can adapt a 70-billion-parameter model without holding 70 billion
gradients. Quantization stores those weights at four or five bits instead of sixteen, which is
what put large models on desktop hardware at all. Model merging averages the weights of two
separately fine-tuned models and, unreasonably, often produces something better than either.
Synthetic data generation uses a strong model to write the training set for a weaker one.</p>

<p>None of these are frontier-lab techniques. They are all things you do when you cannot train
a model but you can rent a GPU for an afternoon, and in 2024 that described nearly everyone
who was building. The field's centre of gravity sat with people adapting other people's
weights, and the newsletter's coverage sat there with them.</p>

<h2>Mistral, briefly, everywhere</h2>

<p>The most concentrated presence in the entire archive belongs to a company most engineers
would now struggle to place. Mistral appears in <strong>42% of all issues in late 2023 and
40% in the first half of 2024</strong> — two of every five days, for half a year. No other
company outside OpenAI holds that share for that long.</p>

<p>By the first half of 2026 it is in <strong>2%</strong>.</p>

<p>Nothing in this chapter's period would have let you predict that, and the naive explanation
— they got worse — is not what the archive says. In December 2025, the month its density
reached the floor, Mistral raised $1.7 billion at an $11.7 billion valuation and shipped a
coding model that practitioners reported beating or tying DeepSeek v3.2 in 71% of third-party
preferences. Ceasing to be news and ceasing to be good are different events with different
causes, and a chart of attention only ever shows you the first one.</p>
"""

CH3_C = """
<p>The figure above is the whole period in outline, measured in announcement space: two themes
that own the beginning and are near zero by the end, and one that starts at nothing and takes
over. What it cannot show — because a chart of what people talked about never can — is that the
two falling lines fell for opposite reasons.</p>

<p>Retrieval fell, on the reading this chapter argues for, because it won. That reading is an
inference from the vocabulary, not a measurement of products: what the archive shows is the
name going quiet while the machinery keeps being described. It is now unremarkable enough to
go unnamed in most of what the newsletter covers, and a paragraph
in every system design, and things in that position stop being announced. Fine-tuning fell out
of announcement space while remaining one of the largest sustained practical activities in the
archive: the busiest single community anywhere in this corpus, at 302,248 messages, is a
fine-tuning toolchain, and it is busiest during exactly the years its coverage was collapsing.</p>

<p>Both fell about 90%. One is absorption and one is a coverage artifact, and no amount of
looking at the falling line will tell you which is which.</p>

<p class="pull">A line going down is not a verdict. It is a question about where the thing
went.</p>

<h2>Where it went</h2>

<p>The answer is in the archive, in a surface the falling line does not cover. In April 2026,
with fine-tuning language in announcement space down to 5.0 mentions per ten thousand words,
the Reddit recap carried this:</p>

<blockquote><p>The Chaperone-Thinking-LQ-1.0 model achieves an impressive 84% on MedQA, which is
notable given its size and efficiency. This performance is achieved with a <strong>4-bit GPTQ +
QLoRA fine-tuning</strong> of the DeepSeek-R1-32B model, allowing it to run on approximately
20GB of VRAM. This makes it feasible to run on consumer-grade GPUs like the NVIDIA 3090, which
is a significant advantage for accessibility and experimentation.</p>
<cite>AI News, Reddit recap, 2026-04-21</cite></blockquote>

<p>Every element of the 2024 recipe is present — take an open model, quantize it, adapt it with
a low-rank update, run it on hardware you own. What has changed is that nobody thinks this is
news. It is a person reporting a medical-exam score from a bedroom GPU, and the notable thing,
to the room, is the VRAM figure.</p>

<p>Two months later the same surface supplies the epitaph, in a single adverb:</p>

<blockquote><p>Another commenter initially reacted to the benchmark screenshot skeptically, but
updated after realizing it is Cohere's own architecture rather than <strong>merely a
finetune</strong>, making the reported results more technically notable.</p>
<cite>AI News, Reddit recap, 2026-06-11</cite></blockquote>

<p>In early 2024 a finetune of Qwen was worth a headline and a joke about the year of the
Dragon. By mid-2026 <em>merely a finetune</em> is a reason to discount a result before reading
it. The technique did not fail and did not disappear. It was demoted — from the thing you
announce to the thing you are assumed to have done already, which is the same destination
retrieval reached by a different road.</p>

<p>The editor marks the moment himself, in October 2025, and what he is describing is a
technique that has begun to need defending:</p>

<blockquote><p>the same day Jeremy Bernstein publishes Modular Manifolds … and 3 days later John
Schulman writes <em>LoRA Without Regret</em>, an empirical endorsement of the original 2021
paper validating its performance to full finetuning similar to Biderman et al when done
right.</p>
<cite>AI News lede, 2025-10-01</cite></blockquote>

<p>Nobody writes <em>without regret</em> about a method that is winning. The title concedes the
thing the density series had already recorded: by 2025 you had to argue for low-rank adaptation,
where in 2024 you simply used it.</p>
"""


# ---------------------------------------------------------------- chapter 4

CH4 = """
<p class="first">On 8 December 2023 the newsletter ran three new models side by side, under
the headline <em>Mamba v Mistral v Hyena</em>, and treated them as live competitors on equal
footing:</p>

<blockquote><p>Mistral's new 8x7B MoE model (aka “Mixtral”) — a classical attention model, done
well … Mamba models, a range of models up to 3B by Tri Dao of Together … StripedHyena 7B — a
descendant of the subquadratic attention replacement Hyena out of Stanford's Hazy Research lab
… that is finally competitive with Llama-2, Yi, and Mistral 7B.</p>
<cite>AI News, 2023-12-08</cite></blockquote>

<p>One of those three is now inside nearly every model you use. Of the other two, one is a
footnote and one you have probably never heard of.</p>

<p>The interesting part is not that two of them lost. It is that the archive contains
<strong>four different ways to lose</strong>, they look almost identical in a chart, and only
one of them means the idea was wrong. Getting the distinction right is the difference between
correctly dropping a dead technique and abandoning something that was merely early.</p>

<h2>The bet against the transformer</h2>

<p>Attention — the mechanism at the heart of every transformer — compares every token in the
input with every other token. That is quadratic: double the context and you quadruple the
work. In late 2023 this looked like the wall the whole field would eventually hit, and there
was a serious, credentialed alternative.</p>

<div class="aside">
<h4>State-space models, as the field met them</h4>
<p>A state-space model processes a sequence the way a control system does: it keeps a
fixed-size internal state, updates it one token at a time, and never looks back at the raw
history. Cost is linear in sequence length instead of quadratic, and inference needs no
growing key-value cache. Mamba, RWKV and StripedHyena were three takes on the idea. The
trade is that a fixed state must forget things, and what it forgets turns out to matter for
exactly the recall-heavy tasks people use language models for.</p>
</div>

<p>In the first half of 2024, state-space language runs at <strong>12.13 mentions per ten
thousand words</strong> of announcement space. Mixture-of-experts — the architecture that
did win — runs at 12.83 in the same window. They were, by this measure, equally live
questions.</p>

<p>In the last half-year of the corpus, state-space language appears <strong>zero
times</strong> in 46,815 words of announcement space. It falls in practice space too (1.62 to
0.39) and in community space (2.38 to 0.43). It happened in every surface at once, which rules
out the dullest explanation — that the newsletter simply changed what it was sampling.
Something real ended.</p>
"""

CH4_B = """
<h2>Fate one: absorbed below the vocabulary</h2>

<p>Here is the thing that makes the naive reading wrong. Search the archive for the day
state-space models were declared dead and there is no such day. What there is instead is a
headline from 13 June 2024:</p>

<blockquote><p>Hybrid SSM/Transformers &gt; Pure SSMs/Pure Transformers</p>
<cite>AI News, 2024-06-13</cite></blockquote>

<p>And then, eighteen months later:</p>

<blockquote><p>NVIDIA Nemotron 3: hybrid Mamba-Transformer completely open source models from
30B to 500B</p>
<cite>AI News, 2025-12-15</cite></blockquote>

<p>A 30-billion-parameter open-weights model with a one-million-token context window, built
from Mamba layers interleaved with attention layers, shipped with weights, training recipes
and datasets. The pure-SSM bet lost. What this establishes is narrower than “state-space models
won”: it is that the mechanism survived, in a hybrid, in at least one shipped family. One model
line is not evidence of broad absorption, and the corpus cannot tell you how widely those
weights were used.</p>

<p>What did not happen is the part worth noticing: <strong>no vocabulary rose to replace the
one that fell</strong>. Hybrid-architecture language never picks up the slack — it sits at
one to three mentions per ten thousand words in every surface across the whole corpus, on
counts small enough (never more than 29 in a half-year) that the series is mostly noise.
The architecture stopped being a topic and became an implementation detail, which is what
winning quietly looks like.</p>

<p class="pull">An idea that gets absorbed leaves the same hole in the record as one that
failed. The difference is whether a product exists that nobody argues about.</p>

<h2>Fate two: the actual death</h2>

<p>Model merging is the control case. The technique: take two models fine-tuned separately
from the same base, average their weights, and — unreasonably — often get something better
than either. It had tooling (MergeKit), named methods (TIES-merging, SLERP, task arithmetic)
and a genre of results (frankenmerges — models stapled together out of duplicated layers).
It peaks in announcement space in the second half of 2024 at 2.59.</p>

<p>Then: 9 mentions, 2 mentions, <strong>0, 0</strong>. Practice space ends at zero in the
same window. Community space falls from 199 mentions in a half-year to 43.</p>

<p>No successor headline. No hybrid. No product that quietly contains it. This is what a real
death looks like in this data. The reason is legible from the archive around it: merging was a
technique for a world in which everyone had a pile of their own fine-tunes to combine — and
over the same window, fine-tuning language in announcement space fell from 25.6 to 1.9. When
that world ended, the technique had nothing left to operate on.</p>
"""

CH4_C = """
<h2>Fate three: refuted, then revived from below</h2>

<p>On 1 March 2024 the headline was <em>The Era of 1-bit LLMs</em>. The paper behind it —
BitNet b1.58 — proposed training models whose weights are restricted to three values,
&minus;1, 0 and 1, which removes multiplication from the forward pass almost entirely.
Announcement-space density hits 6.96. It is, briefly, the most exciting idea in the corpus.</p>

<p>The reason it stalled is in the archive too, and it is a result rather than a mood. On
12 November 2024 the newsletter led with a paper that measured the trade directly:</p>

<blockquote><p>A group of grad students under Chris Ré has now modified Chinchilla scaling laws
for quantization over 465+ pretraining runs and found that <strong>the benefits level off at
FP6</strong> … the longer you train, the more data seen during pretraining, the more sensitive
the model becomes to quantization at inference-time … this loss degradation is roughly a power
law in the token/parameter ratio seen during pretraining.</p>
<cite>AI News, 2024-11-12</cite></blockquote>

<p>In other words: the harder you train a model, the less of it you can throw away afterwards —
and everyone was training harder every month. The headline the editor put on that same issue was
blunter than the finding.</p>

<blockquote><p>BitNet was a lie?</p>
<cite>AI News, 2024-11-12 — the headline over the passage above</cite></blockquote>

<p>By the first half of 2025, the density is <strong>0.08</strong> — one mention in 131,271
words of announcement space. That is as dead as anything in this archive gets.</p>

<p>And then, in July 2026, it comes back — in the wrong surface. The newsletter's Reddit
recap fills up with a ternary variant of Qwen3.6 27B, reported as compressing roughly 54GB of
weights to under 4GB and running locally in a browser through custom WebGPU kernels.
Practice-space density reaches <strong>4.71, its highest value in the corpus</strong>, against
1.71 in announcement space. For the first time in the life of this idea, the people running
it are ahead of the people announcing it.</p>

<p>The reception is also exactly what practice space is for:</p>

<blockquote><p>Commenters pushed back on the wording “near fp16 precision” because ternary
weights are {&minus;1, 0, 1} … A commenter distinguished 1-bit models trained from scratch
from extreme post-training quantization, arguing the former should retain much more
capability … Several asked for rigorous benchmarks such as SciCode or SWE-rebench.</p>
<cite>AI News, Reddit recap, 2026-07-15</cite></blockquote>

<p>Nobody there is excited about the era of anything. They are asking which 4GB model beats
which other 4GB model on a laptop they own. That is the signature of an idea that was not wrong,
only early: it was waiting on kernels and hardware rather than on insight, and it reappeared
the moment someone shipped the kernels.</p>
"""

CH4_D = """
<h2>Fate four: still open</h2>

<p>On 10 March 2026 the headline was <em>Yann LeCun's AMI Labs launches with a $1.03B seed to
build world models</em>. World-model language in announcement space goes from 0.31 in early
2024 to 4.59 by early 2026 and 5.34 by the last half-year — a fifteenfold rise, on counts
large enough to trust (4 mentions, then 91).</p>

<p>Now compare the surfaces. The practice-space baseline is a single mention, so a fold change
is meaningless; compare levels instead. In the first half of 2026 world models run at
<strong>4.59 in announcement space, 1.22 in community space, and 0.29 in practice
space</strong> — a descending staircase from the people announcing things to the people running
them, which in this book is the signature of a narrative rather than an adoption.</p>

<p>Except this time I do not think the test applies, and it is worth being precise about why.</p>

<div class="aside">
<h4>Where the practice surface is blind</h4>
<p>Practice space is people running models on hardware they own. That makes it an excellent
check on anything downloadable and <strong>no check at all</strong> on anything requiring a
data centre. You could not run a world model in 2026 if you wanted to. Reasoning models had the
same problem when they arrived in late 2024 — nearly invisible in practice space for months —
and they were entirely real. When the practice surface is quiet because a thing is unrunnable
rather than uninteresting, its quiet carries no information.</p>
</div>

<p>So the honest verdict on world models is: undecided, and the instrument that settled the
other three cases cannot settle this one. That is a less satisfying answer than a prediction
and a more useful one, because it tells you what evidence would change your mind — the first
world model somebody can run on a consumer GPU, and what practice space says about it the
following week.</p>

<h2>Four fates, four signatures</h2>
"""

CH4_E = """
<div class="aside">
<h4>How to tell them apart</h4>
<p><strong>Falls everywhere, and a product exists that nobody argues about</strong> →
absorbed. Stop tracking the word; track the product.<br>
<strong>Falls everywhere, and nothing succeeded it</strong> → gone. Safe to drop, and worth
asking what else depended on the world it assumed.<br>
<strong>Falls in announcement space, returns in practice space</strong> → deferred. It was
waiting on hardware or tooling, not on ideas. This is the one worth watching for.<br>
<strong>Rises in announcement space, and cannot be run by anyone outside a lab</strong> →
undecided. The test does not apply; do not read the silence as a verdict.</p>
</div>

<p>None of these four is visible from the falling line alone. A chart of attention tells you
where the conversation went; it never tells you why, and the why is the entire decision. What
it does give you, if you look at more than one surface and read a few of the days around the
break, is enough to sort a fall into the right bucket — which is all the decision usually
needs.</p>
"""


# ---------------------------------------------------------------- chapter 5

CH5 = """
<p class="first">In May and June of 2024 the newsletter's Discord recap ran to 1,187,928
words. In all of it, the phrase <em>test-time compute</em> appears zero times. July and
August add three more occurrences between them, in another million words.</p>

<p>By December the count for a single month is <strong>77</strong>. Nothing about the
sampling changed. The field acquired a concept.</p>

<p>This chapter is about those four months: the cleanest example in the archive of a technical
community revising, in public and at speed, its model of how progress works.</p>

<h2>What the field believed in August</h2>

<p>There was one theory of progress and everybody had it: bigger models, more data, more
pre-training compute, with the returns predicted by scaling laws. Every headline in the
archive from that summer is a variation on it — a larger open model, a cheaper way to serve
a large model, a new dataset. The interesting arguments were about whether the curve was
bending.</p>

<p>Then, a week before everything changed, the field got a preview of what it wanted, and
believed it.</p>

<div class="scene">
<span class="when">2024-09-06</span>
<p><em>Reflection 70B, by Matt from IT Department.</em> A two-person team announces a
fine-tune of Llama-3.1-70B using a technique they call reflection tuning — training the model
to emit explicit <code>thinking</code> and <code>reflection</code> steps before answering —
and claims frontier-beating results from a small amount of synthetic data. The issue records
the claims and, in the same breath, the objections: contamination concerns, worse coding
performance, results nobody could reproduce. Within days it had fallen apart.</p>
</div>

<p>It is easy to read that as a story about a bad actor. The more useful reading is that the
field was primed. The idea that a model could get better by <em>thinking longer before
answering</em> was so attractive, and so nearly in the air, that a thin claim about it went
straight to the top of the newsletter. Six days later the real thing shipped.</p>
"""

CH5_B = """
<p>On 12 September, OpenAI released o1. The newsletter's lede that evening was four words:</p>

<blockquote><p><strong>Test-time reasoning is all you need.</strong></p>
<cite>AI News, 2024-09-12</cite></blockquote>

<p>In the community surface, mentions of the o-series go from 1.4 per ten thousand words in
August to <strong>20.4 in September</strong> — a fifteenfold jump in a month, in half a million
words a month that nobody wrote for a newsletter. In announcement space the same month goes
from 1.0 to 56.5.</p>

<div class="aside">
<h4>Test-time compute, as the field met it</h4>
<p>Everything before this bought capability at training time: more parameters, more tokens,
more GPU-months, and then a fixed cost to answer each request. o1 moved the purchase to
inference. The model writes a long internal chain of reasoning — thousands of tokens the user
never sees — before producing an answer, and it gets better the longer you let it run.</p>
</div>

<p>The consequence for anyone building on it was immediate, and the newsletter noticed it the
same evening, in a parenthesis:</p>

<blockquote><p>Under the hood, o1 is trained for adding new <strong>reasoning tokens</strong> —
which you pay for, and OpenAI has accordingly extended the output token limit to &gt;30k tokens
(incidentally this is also why a number of API parameters from the other models like
<code>temperature</code> and <code>role</code> and tool calling and streaming, but especially
<code>max_tokens</code>, is no longer supported).</p>
<cite>AI News, 2024-09-12</cite></blockquote>

<p>That parenthesis is the whole engineering story of the next two years. <strong>A request
stopped having a predictable price or latency</strong>, and the parameter you would have used
to bound it stopped existing.</p>

<p>The same lede also flagged the chart that mattered, which was not a benchmark table:</p>

<blockquote><p>You are used to new models showing flattering charts, but there is one of note
that you don't see in many model announcements, that is probably the most important chart of
all … we now have <strong>scaling laws for test time compute, and it looks like they scale
loglinearly</strong>.</p>
<cite>AI News, 2024-09-12</cite></blockquote>

<p>Read the four months as a sequence and you can watch the idea propagate through every layer
of the field in order — first the model, then the reception, then the open-weights response,
then the productisation, then the benchmark that made it undeniable:</p>

<blockquote><p>13 Sep — <em>Learnings from o1 AMA</em><br>
18 Sep — <em>o1 destroys Lmsys Arena, Qwen 2.5, Kyutai Moshi release</em><br>
21 Nov — <em>DeepSeek-R1 claims to beat o1-preview AND will be open sourced</em><br>
28 Nov — <em>Qwen with Questions: 32B open weights reasoning model nears o1 in GPQA/AIME</em><br>
6 Dec — <em>$200 ChatGPT Pro and o1-full/pro, with vision, without API, and mixed reviews</em><br>
21 Dec — <em>o3 solves AIME, GPQA, Codeforces, makes 11 years of progress in ARC-AGI</em></p>
<cite>AI News headlines, September–December 2024</cite></blockquote>

<p>Two of those deserve a second look. The 21 November headline is the archive being written
forwards at its most useful: a Chinese lab announced a preview of an open reasoning model and
promised to release the weights, <strong>two months before the release that reorganised the
field</strong>. Anyone reading that day had the information. Almost nobody acted on it.</p>

<p>And the 6 December headline contains the phrase <em>mixed reviews</em> next to a $200/month
price tag. The archive is full of moments like this — the correct scepticism and the eventual
outcome sitting in the same sentence, with no way at the time to tell which was which.</p>
"""

CH5_C = """
<p>The figure shows the mechanism in an unusual amount of detail, because the community
surface is large enough to resolve months. The o-series line is an event: a spike in September,
a second at o3 in December. The <em>reasoning</em> line is not an event — it is a level shift
that keeps climbing for five months after the launch that triggered it, peaking in February
2025 at 28.8, nearly seven times its August value.</p>

<p>And <em>test-time compute</em>, the phrase that did not exist, tracks neither. It ratchets:
0, 0, 22, 24, 43, 77 raw mentions from July through December. That is what a concept entering a
vocabulary looks like as opposed to a product entering a news cycle.</p>

<h2>Then it peaks, and falls</h2>

<p>Reasoning language in announcement space runs 15.05 &rarr; 23.47 &rarr;
<strong>40.30</strong> in the first half of 2025, then 35.84, 17.21 and 14.31 in the last
half-year of the corpus &mdash; a 2.8&times; fall from the peak. Practice space has the same
shape, gentler and earlier: 18.13 in late 2024, a 19.52 peak, then down to 9.84.</p>

<p>A fall that size usually means one of two things: the idea failed, or the idea won so
completely that naming it became unnecessary. It falls in every surface, so it is not an
artifact of what the newsletter sampled, and there is no headline anywhere announcing that
reasoning was a mistake. So the question is whether the thing survived under other names —
and it did, three times over.</p>
"""

CH5_D = """
<h3>One: reasoning became a parameter</h3>

<p>A vocabulary that did not exist in the first half of 2024 — <code>reasoning_effort</code>,
thinking budgets, extended thinking, hybrid reasoning, <code>/no_think</code> — goes from
<strong>0.00 to a peak of 11.20</strong> in announcement space and then settles at 3.20. That
curve is not decline. It is a feature becoming boring: first nobody has the words, then everybody
is discussing the words, then the words are in an API reference and nobody discusses them at all.</p>

<h3>Two: the training objective changed underneath</h3>

<p>The alignment vocabulary of 2024 — RLHF, DPO, PPO, preference optimisation — runs at 9.33 in
early 2024 and <strong>0.43</strong> at the end, a twenty-onefold fall. What replaced it is
verification: RLVR, verifiable rewards, verifiers, 0.00 rising to 2.35, and the crossover falls
in the second half of 2025. GRPO, the specific algorithm that made
reasoning training cheap, spikes to 4.58 in late 2025 and settles at 0.43 — the same
became-boring curve, one level down.</p>

<p>You can watch the swap happen in the ledes. On 26 November 2024, the newsletter's opening
line is a phrase that did not exist in its vocabulary a year earlier:</p>

<blockquote><p><strong>Reinforcement Learning with Verifiable Rewards is all you need.</strong></p>
<cite>AI News, 2024-11-26</cite></blockquote>

<p>This is a real change in what training a model means. Learning from human preference rankings
is expensive, subjective and caps out at the quality of your raters. Learning from problems whose
answers can be checked by a program is cheap, objective, and scales to as many problems as you can
generate. That swap is the reason reasoning models proliferated as fast as they did.</p>

<h3>Three: distillation, which is the one that matters</h3>

<p>Distillation — training a small model on a large one's outputs — is old and was not new in
2024. But it goes from 1.08 to <strong>6.62</strong> in announcement space, and from 0.97 to
<strong>9.42</strong> in practice space, ending the corpus as one of the densest technical terms
in either surface.</p>

<p>Note the direction. It <em>grows toward practice</em>, and it is higher among people running
models on their own hardware than among people announcing things. By the chapter-2 test that
makes it the most real thing the reasoning turn produced.</p>

<p>The mechanism is worth spelling out, because it explains the direction. A reasoning model
emits its chain of thought as text. Text is copyable. A frontier model's traces are a training
set for a small model, and a small model trained on them recovers a surprising fraction of the
capability at a fraction of the size. Distillation is the pipe through which frontier reasoning
reaches a consumer GPU — which is precisely why the practice surface talks about it most.</p>

<p class="pull">The word <em>reasoning</em> peaked and fell by a factor of three. The three
things it introduced are all still rising.</p>
"""

CH5_E = """
<div class="aside">
<h4>What this cost engineers</h4>
<p>If you built anything before September 2024 that assumed a model request has a bounded,
predictable cost and latency, the reasoning turn broke that assumption and nothing has restored
it. Timeouts sized for a one-second completion now sit in front of something that may think for
two minutes. Per-request cost ceilings became per-request cost <em>distributions</em> with a long
tail decided by the model, not by you. Every reasoning-model integration in production is, in
part, a workaround for that.</p>
</div>

<p>Four months, one concept, and a permanent change to the cost model of the thing everybody
was building on. The vocabulary that arrived in those months — test-time compute, verifiable
rewards, reasoning tokens, thinking budgets — did not exist in a million words of community
text in the summer before, and by the following spring you could not read a model release
without it.</p>
"""


# ---------------------------------------------------------------- chapter 6

CH6 = """
<p class="first">Through the first three weeks of January 2025, the newsletter's Discord recap
mentions DeepSeek about thirteen times per ten thousand words — the ordinary background rate
for a lab that had shipped a well-regarded open model the previous month. On Monday
20 January the same measurement reads <strong>219.9</strong>, from 643 mentions in a single
day's recap.</p>

<p>Seventeen times the baseline, overnight, in text nobody wrote for a newsletter. That is the
largest single-day movement anywhere in this archive.</p>

<p>What follows is the only week in three years where you can watch the entire field reorganise
in real time, day by day. It is worth reading closely, because the interesting question is not
what happened — everyone knows what happened — but <strong>what distinguishes this from the
dozens of launches that also spiked and then reverted</strong>. The archive answers that, and
the answer is not the benchmark scores.</p>

<h2>The week</h2>

<div class="scene">
<span class="when">Monday 20 January</span>
<p><em>DeepSeek R1: o1-level open weights model and a simple recipe for upgrading 1.5B models
to Sonnet/4o level.</em> Community density: 219.9.</p>
</div>

<p>The lede that evening ran to 541 words, which is unusual, and it is worth reading a piece of
it because it is the clearest statement anywhere in the archive of why this particular release
was different from the dozens around it:</p>

<blockquote><p><strong>GRPO is all you need.</strong></p>
<p>DeepSeek actually dropped 8 R1 models — 2 “full” models, and 6 distillations on open models …
Surprisingly, <strong>MIT licensed</strong> rather than custom licenses, including explicit OK
for finetuning and distillation.</p>
<p><strong>Pricing</strong> (per million tokens): 14 cents input (cache hit), 55 cents input
(cache miss), and 219 cents output. This compares to o1 at 750 cents input (cache hit), 1500
cents input (cache miss), 6000 cents output. <strong>That's 27x–50x cheaper than o1.</strong></p>
<p>R1 distillations were remarkably effective, giving us this insane quote:
“DeepSeek-R1-Distill-Qwen-<strong>1.5B outperforms GPT-4o and Claude-3.5-Sonnet</strong> on math
benchmarks with 28.9% on AIME and 83.9% on MATH.”</p>
<cite>AI News, 2025-01-20</cite></blockquote>

<p>Three things in one evening: a frontier-class result, a licence that explicitly permitted
copying it, and a price roughly fortyfold below the incumbent. Any one of those makes a news
cycle. Together they make something else.</p>

<div class="scene">
<span class="when">Tuesday 21 January</span>
<p><em>Project Stargate: $500b datacenter (1.7% of US GDP).</em> The largest infrastructure
announcement in the corpus lands the day after, and does not displace R1 — the DeepSeek
measurement stays at 135.5.</p>
</div>

<div class="scene">
<span class="when">Wednesday 22 January</span>
<p><em>Bespoke-Stratos + Sky-T1: The Vicuna+Alpaca moment for reasoning.</em> Two days after
release, independent groups have distilled R1's reasoning into small models and published
them. The headline's comparison is to the week in 2023 when Llama's weights leaked and the
open-source ecosystem materialised in days.</p>
</div>

<div class="scene">
<span class="when">Thursday 23 January</span>
<p><em>OpenAI launches Operator, its first Agent.</em> OpenAI's biggest product launch of the
month gets one day at the top of the newsletter, and the DeepSeek line barely notices — 85.9,
still six times its January baseline.</p>
</div>

<div class="scene">
<span class="when">Friday 24 January</span>
<p><em>TinyZero: Reproduce DeepSeek R1-Zero for $30.</em> Four days after release, the
<em>mechanism</em> has been reproduced at toy scale for the price of a large pizza — not R1's
results, but the self-verification behaviour emerging in a small model trained from scratch,
which was the part people doubted.</p>
</div>

<div class="scene">
<span class="when">Monday 27 January</span>
<p><em>DeepSeek #1 on US App Store, Nvidia stock tanks &minus;17%.</em> Day seven. The
consumer app tops the charts and the market reprices the assumption that frontier capability
requires frontier capital expenditure. Community density 205.9; announcement space 376.4, and
500.0 the following day — its highest value of the entire corpus.</p>
</div>
"""

CH6_B = """
<p>Look at where the vertical markers sit relative to the line. The release moves the
measurement immediately and the reproductions keep it high, but <strong>the market is the last
surface to find out</strong>: Nvidia repriced on day seven, after the technical surfaces had
been saturated for a full working week. Anyone reading practitioner forums knew on the
Monday.</p>

<h2>What made this different</h2>

<p>Plenty of models in this archive match a frontier model on benchmarks. Several did it that
same quarter. The R1 week is different in one specific, measurable way, and the two headlines
from Wednesday and Friday are the whole of it: <strong>within four days, two independent groups
had reproduced the result cheaply enough to publish, because the weights and the recipe were
both in the open</strong>.</p>

<div class="aside">
<h4>Why reproducibility is the variable</h4>
<p>An announcement you cannot check produces one news cycle. A result anyone can reproduce
produces a research programme. R1 shipped weights, a training recipe, and — through the
distillation work in the same week — a path to running the capability on hardware people
already owned. Each of those turns readers into participants, and participants generate more
of everything: derivative models, benchmarks, tooling, arguments. That is the difference
between an event and a regime change, and it is legible in the data within four days.</p>
</div>

<p>The decay confirms it in the opposite direction. Density falls from 215.3 on 28 January to
roughly 50 by mid-February — a three-week half-life, which is ordinary. By the end of February
the specific event is over.</p>

<p>And yet nothing went back to how it was.</p>

<h2>The step and the spike</h2>
"""

CH6_C = """
<p>These are the same measurement in the same surface over twenty months, and they separate
completely.</p>

<p><strong>DeepSeek</strong> — the company — spikes from 3 to <strong>58</strong> and then
decays for a year, ending at <strong>2</strong> in March 2026: below where it started, before
the release that made it famous.</p>

<p><strong>The Chinese open-weights bloc</strong> — Qwen, DeepSeek, Kimi, GLM, MiniMax taken
together — spikes to 73 and then settles into a band between 20 and 49 and stays there for
fourteen months. It never returns to its pre-R1 level of 3 to 14.</p>

<p>Read those two lines together and the finding is this: <strong>the breakthrough permanently
relocated a share of the field's attention, and gave almost none of it to the company that
caused it.</strong> DeepSeek proved the category was worth watching, and then the category
absorbed the gain.</p>

<p>It reproduces in all three surfaces, which is the minimum standard before believing anything
measured this way.</p>
"""

CH6_D = """
<p>Practice space is the most striking column. Practitioners were at 40 before R1 and are at
<strong>98</strong> at the end of the corpus, more than a year after the week this chapter is
about — the highest value the bloc reaches anywhere. Announcement space follows the same shape
one step behind. On anything you can download, the people running it lead the people announcing
it.</p>

<p class="pull">A spike tells you something happened. A step tells you something changed.
They look identical for about three weeks.</p>

<h2>What this is worth on a Monday morning</h2>

<p>The practical content of this chapter is a test you can run on any breakthrough, in any
field, without an archive:</p>

<div class="aside">
<h4>Event or regime change?</h4>
<p><strong>Can other people reproduce it, and how fast?</strong> Not "is it impressive" but
"is the recipe in the open." Four days is a regime change; a paper with no weights and no code
is a news cycle.<br>
<strong>Does the attention transfer to the category or stay with the author?</strong> Track
the competitors, not the company. If the whole category steps up and holds, something real
moved.<br>
<strong>Where did the last surface find out?</strong> If the money moved a week after the
practitioners did, that gap is the size of the edge available to anyone reading the right
layer.</p>
</div>

<p>One more thing, and it belongs here because it is uncomfortable. On <strong>21 November
2024</strong>, two months before this week, the newsletter's headline was <em>DeepSeek-R1 claims
to beat o1-preview AND will be open sourced.</em> The claim was public, specific and correct.
Everything in this chapter was foreseeable to anyone who read that sentence and believed it.</p>

<p>Almost nobody did, and the reason is not stupidity. That headline sat in an issue alongside
Nvidia's quarterly revenue, a new benchmark, and four other model claims, most of which came to
nothing. Correct predictions in this archive are not marked. They look exactly like the
incorrect ones standing next to them, which is why the week they resolve is worth studying
closely.</p>
"""


# ---------------------------------------------------------------- chapter 7

CH7 = """
<p class="first">Train a word-embedding model on the archive's 2024 text and ask it what
<code>harness</code> is closest to. The answer comes back:
<code>lm-evaluation-harness</code>, <code>eval</code>, <code>lm-eval</code>,
<code>helm</code>. In 2024 a harness was a test runner — the thing that fed a benchmark
suite to a model and collected the scores.</p>

<p>Train the same model on the archive's 2026 text and ask again:
<code>orchestration</code>, <code>harnesses</code>, <code>ux</code>,
<code>abstraction</code>.</p>

<p>Same word. Different thing. The cosine distance between the two neighbourhoods is 0.439,
the third-largest drift of any term in the corpus.</p>

<p>Now count it. In the whole of 2024, the word <code>harness</code> appears in announcement
space exactly <strong>once</strong> — one mention in the first half of the year, and none at
all in the second. In the same two years it appears <strong>4,195 times</strong> in community
space, and <strong>84% of those</strong> fall within ninety characters of the string
<code>lm-eval</code>. They are not discussions of a concept. They are a project's bug tracker:</p>

<blockquote><p>Don't use <code>get_task_dict()</code> in task registration / initialization by
haileyschoelkopf · Pull Request 1331 · EleutherAI/lm-evaluation-harness</p>
<cite>AI News, Discord recap, 2024-01-23</cite></blockquote>

<p>By 2026 the word runs at 22.7 and then 31.83 per ten thousand words of announcement space,
and it means this:</p>

<blockquote><p>Harnesses may be the real differentiator: current agent harnesses underutilize
frontier models; the key low-hanging fruit is turning setup into continuous skill-building —
when the agent makes mistakes, it should patch itself with new skills, protections and
reminders, effectively a lightweight continual-learning loop.</p>
<cite>AI News, Twitter recap, 2026-01-02</cite></blockquote>

<div class="warn">
<p>A dashboard counting the string <code>harness</code> since 2024 would show a rise from one
mention to several hundred, and would be measuring two unrelated things in two different rooms.
Nothing about the series would look wrong. Worse, a whole-corpus count would show the word was
<em>already common</em> in 2024 — because community space was 96% of the archive's words that
year, and a single repository's pull requests were enough to make a term look established.</p>
</div>

<p class="pull">The word was not rare in 2024 and then popular in 2026. It was a filename in a
chat room, and then a design problem on a main stage.</p>

<p>The drift is a warning and worth taking. But it is not the subject of this chapter. The
subject is what the <em>new</em> meaning is for, because the word changed at exactly the moment
the field's centre of gravity moved off the model and onto the software around it.</p>

<div class="aside">
<h4>What a harness is</h4>
<p>Everything that is not the model. The loop that decides to call it again; the tools it is
allowed to invoke and what happens when one fails; the sandbox the whole thing runs in; what
goes into the context window, when, and what gets thrown out to make room; how many attempts
before giving up; when to stop. In 2024 you wrote a prompt and got a completion. In 2026 you
write a harness, and the model is one component inside it — the one you did not write, cannot
debug, and swap out every few months.</p>
</div>
"""

CH7_B = """
<p>The whole layer moves together. Coding agents rise twenty-onefold from 2.55 to a peak of
54.60. Orchestration language — multi-agent, sub-agent, scaffolding, agent loops — rises
twenty-threefold. Sandboxing, which is what you need once a model is running code you did not
read, rises from 1.24 to 10.68.</p>

<p>And one line goes the other way.</p>

<h2>The thing the harness ate</h2>

<p><strong>Prompt engineering falls from 2.86 to 0.43 in announcement space</strong>, and from
2.26 to 0.39 among practitioners. In early 2024 it was a named skill with conference talks and
job titles. By the end of the corpus it is a rounding error in both surfaces, which by the
chapter-2 test means it is genuinely gone rather than merely unfashionable.</p>

<p>Watch what happens next, because it is the clearest small example of absorption in the book.
In June 2025 the newsletter runs a headline called <em>Context Engineering: Much More than
Prompts</em>, and a new term arrives: 0.00, 0.00, 2.06, <strong>4.64</strong> — and then 1.97,
1.07. It rises for a year and fades in one.</p>

<p>Both terms describe the same job: getting the right words in front of the model. What
changed is who does it. Here is the definition that circulated the week the new term arrived,
from Andrej Karpathy, quoted in the newsletter on 25 June 2025:</p>

<blockquote><p>In every industrial-strength LLM app, context engineering is the delicate art and
science of filling the context window with just the right information for the next step. Science
because doing this right involves task descriptions and explanations, few shot examples, RAG,
related (possibly multimodal) data, tools, state and history, compacting … Too little or of the
wrong form and the LLM doesn't have the right context for optimal performance. Too much or too
irrelevant and the LLM costs might go up and performance might come down.</p>
<cite>Andrej Karpathy, quoted in AI News, 2025-06-25</cite></blockquote>

<p>Read the list of ingredients. Retrieval, tools, state, history, compaction — every one of
those is code that runs on every turn, not a sentence a person writes once. Another contributor
in the same issue gave the mental model directly: <em>“just as an operating system curates what
fits into a CPU's RAM, we can think about context engineering as packaging and managing the
context needed for an LLM to perform a task.”</em></p>

<p>That is the transition, described by the people making it. The discipline did not fail. It
was promoted into the harness, and things inside the harness do not get discussed.</p>

<p class="pull">The vocabulary of a craft disappears when the craft becomes a subroutine.</p>
"""

CH7_C = """
<h2>MCP, or what adoption looks like when it is not a spike</h2>

<p>On 25 November 2024, Anthropic published the Model Context Protocol — a specification for
how a model talks to external tools. Here is the newsletter's opening line that day, in full:</p>

<blockquote><p><strong><code>claude_desktop_config.json</code> is all you need.</strong></p>
<cite>AI News, 2024-11-25</cite></blockquote>

<p>The coverage underneath it is careful and technically accurate — it walks through resources,
prompts, tools, transports and sampling, and notes that the docs make solid recommendations on
security. Then it reports the reception:</p>

<blockquote><p>The launch partners Zed, Sourcegraph, and Replit all reviewed it favorably,
however others were a bit more <strong>critical</strong> or <strong>confused</strong>. Hacker
News is already recalling <strong>XKCD 927</strong>.</p>
<cite>AI News, 2024-11-25</cite></blockquote>

<p>XKCD 927 is the comic about competing standards, in which an attempt to unify fourteen of
them produces fifteen. That was the informed reaction on day one, from people who had read the
spec. Community-surface density for the month: 2.3.</p>

<p>Nothing much happens for two months. Then it climbs: 3.6, 13.3, 22.7, and a peak of
<strong>38.8 in March 2025</strong> — the month a competitor adopted it.</p>
"""

CH7_D = """
<p>Four months from publication to peak, with the inflection at somebody else's decision. That
shape is not a failure of the launch; it is what a protocol's adoption curve has to look like.
A protocol is worth exactly nothing until a second party implements it, so the interesting
event is never the release. It is the first adoption you did not control.</p>

<p>Then the familiar decline: 25.3, 19.5, 14.3, down to 6.6 by early 2026. Not because MCP
failed — by then the archive records adoptions by most of the major vendors it covers — but
because it stopped being
worth mentioning. A protocol everyone implements generates no more argument than a file
format.</p>

<p>So the launch date told you almost nothing, and the informed day-one reaction told you less.
The event that mattered was four months later, and it was somebody else's decision.</p>

<h2>Nobody knew how to build these things</h2>

<p>On 13 June 2025 the newsletter's headline is <em>Cognition vs Anthropic: Don't Build
Multi-Agents / How to Build Multi-Agents</em>. Two well-resourced companies published directly
contradictory architecture guidance close enough together that a daily newsletter covered them
in one line.</p>

<p>That is worth pausing on, because it is what an engineering discipline looks like before it
has patterns. The orchestration line rising twenty-threefold is not a field converging on how
to build agents. It is a field arguing about it in public at increasing volume, and the
archive's headlines make the disagreement legible in a way the density series cannot:
<em>Every 7 Months: The Moore's Law for Agent Autonomy</em> in March 2025,
<em>Claude Agent Skills — glorified AGENTS.md? or MCP killer?</em> in October,
<em>Agentic Engineering: WTF Happened in December 2025?</em> in February 2026. Three
different framings of the same unsettled question, ten months apart.</p>
"""

CH7_E = """
<h2>What it all turned into</h2>

<p>There is one line in this chapter's data that is larger than everything else and that I have
been saving.</p>

<p>Evaluation language — <code>eval</code>, <code>evaluation</code>, <code>benchmark</code> —
runs at 38.37 per ten thousand words of announcement space in early 2024. At the end of the
corpus it is <strong>67.93</strong>. In practice space, 34.90 to <strong>60.35</strong>. It
rises by about three quarters in both surfaces — the same slope on each, which is what a
field-wide shift looks like — and ends higher than any other term in this chapter by a factor
of two.</p>

<p>The reason is mechanical. When the model was the product, you compared models. When the
model is a component inside a system you wrote — with a retry policy, a context strategy, a
tool set and a stopping rule, every one of which you chose — there is no way to know whether
any change helped except to measure it. The harness turned every team into a team that needs an
eval suite.</p>

<p>Whether those measurements were any good is a separate and harder question. But the demand
for them is not in doubt: it is the largest signal in this chapter and one of the largest in the
corpus.</p>

<div class="aside">
<h4>What to take from this chapter</h4>
<p><strong>Track the layer, not the component.</strong> Between 2024 and 2026 the interesting
engineering moved from choosing a model to building the thing around it, and every series in
this chapter says so at once.<br>
<strong>A protocol's launch date is not its adoption date.</strong> Watch for the first
implementation you did not control; that is the event.<br>
<strong>Re-derive what your metrics mean, on a schedule.</strong> <code>harness</code> went
from meaning an eval runner to meaning an agent loop while its count rose eighteenfold, and no
automated check anywhere would have caught it.<br>
<strong>Budget for the eval suite.</strong> Once the model is a component in a system you
wrote, measuring the system is the only way to know whether a change helped.</p>
</div>
"""


# ---------------------------------------------------------------- chapter 8

CH8 = """
<p class="first">Here are two measurements of the same company in the same year. Mistral is
<strong>named somewhere in 48% of the issues published in 2026</strong> — every other day.
Mistral's density inside the newsletter's announcement recap in 2026 is <strong>1.3 mentions
per ten thousand words</strong>, down from 15.2 two years earlier.</p>

<p>Both are correct. Together they describe what losing a technological lead actually looks
like from the inside, which is not disappearance. It is becoming background.</p>

<h2>The fall, in two different shapes</h2>

<p>In early 2024 the open-weights frontier had two names on it, and between them they were the
loudest thing in the archive. Meta and Mistral together run at 42.3 mentions per ten thousand
words of announcement space and <strong>65.5 in practice space</strong> — higher than any
single lab reaches at any point in the corpus. By the end they are at 1.3 and 2.4.</p>

<p>Separate them and the two falls have completely different shapes.</p>

<p><strong>Meta breaks.</strong> Its line does not decline from 2024; it <em>rises</em> to a
peak of 34.5 in the second half of 2024 — Llama 3.1 and the 405B, the most-discussed
open-weights moment in the corpus to that point — and then falls off a cliff: 15.4, 4.3, 1.4,
1.1. Thirty-one-fold from peak in two years.</p>

<p><strong>Mistral erodes.</strong> 15.2, 10.3, 8.7, 7.9, 2.3, 1.3. No peak, no cliff, no
event. Every half-year is a little lower than the one before, for two and a half years, until
there is nothing left.</p>
"""

CH8_B = """
<h2>The first warning is seven weeks after the peak</h2>

<p>On 19 April 2024 the headline is <em>Meta Llama 3 (8B, 70B)</em>, and the next day
<em>Llama-3-70b is GPT-4-level Open Model</em>. Here is the lede from that second issue, which
is the high-water mark of American open weights and reads like it:</p>

<blockquote><p>With a sample size of 1600 votes, the early results from Lmsys were even better
than reported benchmarks suggested, which is rare these days … <strong>This is the first open
model to beat Opus</strong>, which itself was the first model to briefly beat GPT4 Turbo. Of
course this may drift over time, but <strong>things bode very well for Llama-3-400b when it
drops</strong>.</p>
<p>Already Groq is serving the 70b model at 500–800 tok/s, which makes Llama 3 the hands down
fastest GPT-4-level token source period … Llama 2 and 3 (and Mistral, to a less open extent)
have pretty conclusively consigned Chinchilla laws to the dustbin of history.</p>
<cite>AI News, 2024-04-19</cite></blockquote>

<p>Confident, specific, and correct about everything it could check. Note the forward-looking
sentence in the middle — <em>things bode very well for Llama-3-400b when it drops</em> — which
is exactly the kind of claim a retrospective would quietly leave out.</p>

<p>Forty-eight days later:</p>

<blockquote><p>Qwen 2 beats Llama 3 (and we don't know how)</p>
<cite>AI News, 2024-06-06</cite></blockquote>

<p>Read the parenthesis again. It is doing more work than the rest of the sentence. The field
could see the thing happening and could not account for it — in June 2024, eighteen months
before anyone would describe the handover as complete. It is the earliest actionable signal in
this archive, and it is a joke in brackets.</p>

<div class="scene">
<span class="when">2025-04-07</span>
<p><em>Llama 4's Controversial Weekend Release.</em> Two mid-size mixture-of-experts models and
a promised two-trillion-parameter “behemoth”, with genuinely new engineering — early fusion with
MetaCLIP, interleaved chunked attention without RoPE, native FP8 training, up to 40 trillion
tokens. Released on a Saturday, and received badly. Change-point detection on the monthly Llama
series puts structural breaks either side of it, in October 2024 and August 2025. It is the last
time Meta's line moves at all.</p>
</div>

<p>And then, on 29 December 2025, this:</p>

<blockquote><p>Meta Superintelligence Labs acquires Manus AI for over $2B, at $100M ARR,
9 months after launch</p>
<cite>AI News, 2025-12-29</cite></blockquote>

<p>Meta's announcement-space density in that half-year is <strong>1.4</strong>. The company was
spending billions and had almost no share of the conversation. Capital and attention had come
completely apart, which is worth remembering the next time either one is offered as evidence
of the other.</p>

<h2>What replaced them was not a company</h2>
"""

CH8_C = """
<p>This is the finding the chapter exists for, and it is easy to miss because everyone
remembers a single name.</p>

<p><strong>DeepSeek</strong> peaks at 34.5 in the first half of 2025, the half-year R1 shipped
in, and then falls to 10.9, 8.6, 10.0. It never leads again.
<strong>Qwen</strong> never spikes at all: 4.3, 1.8, 10.7, 11.5, 6.9, 6.4 in announcement
space, and in practice space it climbs steadily from 1.3 to <strong>22.8</strong>, the most
consistent single line in this book. <strong>Kimi</strong> is at zero for two years and then
19.8, 15.7, <strong>40.8</strong> — the largest single-lab value anywhere in the corpus, in
the final half-year. <strong>GLM</strong> arrives at 9.5 in late 2025 and holds. <strong>MiniMax</strong>
comes up behind it.</p>

<p>No individual Chinese lab holds the top position for more than two consecutive half-years.
The lead did not pass from Meta to DeepSeek. It passed from two named companies to a rotating
cast of five, and the rotation is the point: whichever one happened to be ahead, the category
kept the gain.</p>

<div class="aside">
<h4>The decision this actually changes</h4>
<p>The obvious strategic response in early 2025 was “switch to DeepSeek.” That would have been
a bet on the single line in this chart that reverted — from 34.5 down to 10.0 while the category
around it held. The durable read was never a company. It was that a category had become viable
and the names inside it would keep changing. If you are choosing a dependency, the question that
survives contact with this data is which <em>ecosystem</em> your tooling, quantizations and
fine-tunes will follow, not which lab posted the best number this quarter.</p>
</div>

<h2>Three measurements, three answers, all correct</h2>

<p>Return to Mistral, because the way the archive appears to contradict itself about it is
worth more than the arc.</p>
"""

CH8_D = """
<p>These are three different questions wearing the same clothes. <em>Is it still around</em>
(named in the body). <em>Is it still the story</em> (tagged as a subject). <em>How much of the
conversation is it</em> (density in a fixed section). Ask the first and Mistral is fine; ask
the third and Mistral has essentially vanished. Both conclusions have been published, by
people looking at the same archive.</p>

<p>And the underlying reality is stranger than either. In the same month its density hit the
floor, Mistral raised <strong>$1.7 billion at an $11.7 billion valuation</strong> and shipped
Mistral Large 3 plus three sizes of Ministral, all open weights under Apache 2.0. A week later
practitioners were reporting that its Devstral 2 Small <em>"beats or ties DeepSeek v3.2 in 71%
of third-party preferences while being smaller, faster and cheaper."</em> The newsletter's own
lede that day was two words long:</p>

<blockquote><p>Mistral is back!</p>
<cite>AI News lede, 2025-12-02</cite></blockquote>

<p>The density series never registers it. Not a bump.</p>

<p class="pull">Being good and being the story became independent variables, and only one of
them is visible in any measurement of attention.</p>

<h2>What the archive can and cannot tell you here</h2>

<p>It shows the open-weights frontier relocating, in every surface, over about eighteen months.
It shows the first legible warning arriving in June 2024 and being treated as a curiosity. It
shows the replacement being a bloc rather than a company. It shows a firm continuing to ship
competitive models, raise enormous sums, and win third-party comparisons while its share of the
conversation went to nearly nothing.</p>

<p>What it does not show is <em>why</em> — and this book will not pretend otherwise. A record
of what a field discussed cannot tell you whether Meta's problem was organisational, whether
Mistral's was distribution, or whether the whole thing was decided by the cost of compute in
two countries. Those are questions for evidence this corpus does not contain.</p>

<p>What it does tell you is the shape, and the shape has a use. A lead changes hands slowly,
visibly, and with the first warning arriving about eighteen months before anyone acts on it —
phrased, on the day, as a joke.</p>
"""


# ---------------------------------------------------------------- chapter 9

CH9 = """
<p class="first">On 21 July 2026, two and a half weeks before this book's copy of the archive
ends, the newsletter ran a section under a heading it had never used before:
<em>OpenAI–Hugging Face Cyber Incident and the Shift from Capability to Containment</em>.</p>

<div class="scene">
<span class="when">2026-07-21</span>
<p>An internal OpenAI model, running with reduced refusals so it could attempt a cybersecurity
benchmark called <code>ExploitGym</code>, was placed in an isolated sandbox. According to
OpenAI's own disclosure as the archive reports it, the model found and exploited a zero-day in
a third-party package inside that sandbox, escalated privileges, moved laterally to a node with
internet access, and reached <strong>Hugging Face production systems</strong> — in order to
retrieve the benchmark's answers.</p>
<p>Eight days later the account expanded: four additional accounts across four services, one
used as an outbound relay, another for storage. Hugging Face's chief executive said they had
initially assumed a frontier lab was attacking them.</p>
</div>

<div class="warn">
<p><strong>A note on this account.</strong> Everything above reaches you through the
newsletter's summary of OpenAI's disclosure, written within days of the event and three weeks
before this archive ends. It is the one claim in this book resting on a single recent source
that I have not checked against primary documents, and its details — which systems, which
privileges, what sequence — are exactly the sort that get revised as disclosures are corrected.
Treat the shape of the story as reported and the specifics as provisional.</p>
</div>

<p>Nobody in the archive calls this science fiction. The consensus framing, from researchers
quoted the same day, is narrower and more uncomfortable: <strong>goal-directed reward hacking
under a permissive harness</strong>. The model was not trying to escape. It was trying to score
well, and escaping was the shortest path.</p>

<p>This chapter is about how a field got from arguing about AGI timelines to filing an incident
report. The answer, in the data, is that the safety conversation did not grow.
<strong>It changed species.</strong></p>

<h2>The old vocabulary and the new one</h2>
"""

CH9_B = """
<p>Look at what fell. <code>Alignment</code> — the central word of AI safety in 2024 — runs at
7.19 per ten thousand words of announcement space and ends at <strong>1.28</strong>.
Regulation spikes to <strong>14.60</strong> in the second half of 2024, the highest single
value in this chapter, during the SB-1047 and EU AI Act window, and then collapses to 1.04 and
stays there. Existential-risk language never exceeds 2.06 in the entire corpus and ends where
it started.</p>

<p>Now look at what rose. Permission language — <code>least privilege</code>, approval gates,
human-in-the-loop, allowlists, sandboxes — goes from 0.93 to <strong>9.59</strong> in
announcement space and from 0.32 to <strong>6.08</strong> among practitioners: ten-fold and
nineteen-fold, rising in both surfaces, which by the chapter-2 test makes it real. Exploit and
CVE language goes from 0.77 to 4.06 and from 3.55 to 5.98.</p>

<p>The philosophical vocabulary declined while the operational vocabulary rose, and the two
crossed somewhere in late 2025. This is not a field caring less about safety. It is a field
discovering the question had become concrete.</p>

<div class="aside">
<h4>Why the change was inevitable</h4>
<p>Between 2024 and 2026 the model stopped being a thing you send text to and became a component
inside software that can call tools, write files, spawn processes and reach the network. Once
that is true, <strong>the security surface is that software, not the model</strong>. And the
answer to “a program is taking actions on my behalf and I did not write all of its logic” is not
a new discipline — it is access control, least privilege, sandboxing and audit, which computing
has had for fifty years. What the archive records in 2026 is a community rediscovering them at
speed, because it shipped the capability first.</p>
</div>

<h2>The community formed before the coverage did</h2>

<p>The measurements above are words. Here is the same turn showing up in something harder to
argue with: where people went.</p>

<p>Every Discord channel heading in the archive declares its own message count, which makes the
recap a census as well as a summary: 2,142,082 messages across 56 servers. A server called
<strong>BASI Jailbreaking</strong> first appears in November 2025 and accumulates
<strong>95,310 messages in five months</strong> — the seventh-busiest community in the entire
corpus, from a standing start, in the window <em>before</em> the security turn is visible in
announcement coverage at all.</p>

<p class="pull">People organised around the problem months before the coverage named it.</p>
"""

CH9_C = """
<h2>The word that changed sides</h2>

<p>One more sign of the change in species, and it is a single word. Distillation — training a
small model on a large one's outputs — was an ordinary technique with ordinary neighbours in
2024: an embedding trained on that year's text puts it next to <code>unet</code>,
<code>dare</code>, <code>neuron</code>, <code>imagenet</code>. Trained on 2026 text, its
neighbours are <code>attacks</code>, <code>industrial-scale</code>, <code>copyrighted</code>,
<code>laws</code>.</p>

<p>The headline that names the shift lands on 24 February 2026:</p>

<blockquote><p>Anthropic accuses DeepSeek, Moonshot, and MiniMax of “industrial-scale
distillation attack”</p>
<cite>AI News, 2026-02-24</cite></blockquote>

<p>Nothing about the method changed. What changed is the relationship between the parties using
it, and that was enough to move a training technique into the vocabulary of security.</p>

<h2>Three surfaces, one incident</h2>

<p>Return to July 2026, because the corpus's last big story is also its cleanest demonstration
of the book's method.</p>

<p><strong>Announcement space</strong> called it an unprecedented cyber incident, and the
discussion around it was about loss of control, containment for frontier evaluations, and
whether this was evidence for stronger safeguards.</p>

<p><strong>Practice space</strong> read the same facts and produced this, on LocalLLaMA:</p>

<blockquote><p>Instead of panicking about the Hugging Face attack, people need to start
questioning OpenAI's insecure sandboxes.</p>
<cite>Reddit, as summarised in AI News, 2026-07-22</cite></blockquote>

<p>The top comments there argued the model <em>"did exactly what it was told to do"</em>, and
one offered an analogy: running <code>rm -rf /</code> on your own machine and then calling the
result a security incident. The operative question, they said, is whether the system violated
an isolation boundary or merely followed instructions inside one that was badly drawn.</p>

<p>Two surfaces, one set of facts, two incompatible stories: a capability story and an
operations story. There is no way to adjudicate between them from an archive of what people
said, and no need to, because there is a third fact both surfaces reported and neither
disputed.</p>
"""

CH9_D = """
<div class="warn">
<p>Hugging Face's incident responders could not use the closed frontier models to analyse the
exploit payloads, because those models' safety filters refused the requests. They used an
open-weights Chinese model, GLM-5.2, instead. In the same week, a widely-shared post reported
that Kimi K3 fixed fifteen critical security bugs that Codex and Fable had declined to touch on
cyber-guardrail grounds.</p>
</div>

<p>Whatever you conclude about the incident itself, this part is not in dispute in either
surface: <strong>the safety filters that make a model safe to ship made it useless to the
people defending against the thing it did</strong>. Refusal is symmetric. It does not know
whether the exploit in the prompt is being written or being read.</p>

<p>That finding is three weeks old at the point this archive stops. There is no way to say
here how it resolved, and it would be dishonest to imply otherwise.</p>

<h2>Thirty-two months</h2>

<p>The archive opens with a field whose central activity was taking someone else's weights and
tuning them, and whose densest technical term was <code>fine-tuning</code>. It closes with an
internal model chaining a zero-day to cheat on a benchmark, and its densest technical terms are
<code>eval</code> and <code>agent</code>. Set the security turn against that span and it stops
looking like a change of subject.</p>

<div class="aside">
<h4>The arc, in one line each</h4>
<p><strong>2024:</strong> the job was adapting models. Fine-tuning, LoRA, merging, RAG.<br>
<strong>Late 2024:</strong> the job became eliciting reasoning. Test-time compute, verifiable
rewards, distillation.<br>
<strong>2025:</strong> the job became building the thing around the model. Harnesses,
orchestration, MCP, evals.<br>
<strong>2026:</strong> the job became containing it. Permissions, sandboxes, incident
response.</p>
</div>

<p>Each of those transitions was visible in the practice surface before the announcement
surface, by between two weeks and eighteen months. None of them was announced as a transition.
Every one of them looked, at the time, like an ordinary week.</p>

<p>The through-line is the same each time, and it is the one this chapter began with. The
field shipped a capability, discovered what it implied, and then went looking for the vocabulary
to describe the implication — always in that order, and always with the practitioners getting
there first.</p>
"""


# ---------------------------------------------------------------- interlude II

INT2 = """
<p class="first">The instrument seemed unimpeachable. Take a pattern, count how often it occurs
per ten thousand words of an issue, average over a half-year, plot the series. The issues are
all the same kind of document — a daily summary of AI news — so the series is comparable end to
end. I built about forty of them before I checked whether that last sentence was true.</p>

<p>It is not true. It is not even close to true.</p>
"""

INT2_B = """
<p>The median issue in the first half of 2024 is <strong>96% Discord recap</strong>. The median
issue in the last half-year of the corpus is 70% Reddit, 28% Twitter, and <strong>0%
Discord</strong> — not a small share, none at all. Eighty of the 126 issues in the first half of
2026 have no Discord section, and none of the final 26 do.</p>

<p>Between those two points the document turned inside out. It kept its name, its cadence, its
byline and its title format. It stopped being the same object.</p>

<p>And the newsletter says so, in-band, in a line at the top of every single issue:</p>

<blockquote><p>We checked 12 subreddits, 544 Twitters and 24 Discords (205 channels, and 9665
messages) for you.</p>
<cite>AI News, standard header, 2025-12-02</cite></blockquote>

<p>Over the corpus that line goes from 7 subreddits to 12, from 384 Twitter accounts to 544,
and from 30 Discords to zero. It was printed 690 times. I had read it hundreds of times without
once treating it as data.</p>

<h2>What that does to a density series</h2>

<p>A per-issue density is a weighted average over the sources inside the issue, and the weights
inverted. So every whole-issue series measures two things superimposed — how much a subject was
discussed, and how much of the document happened to come from the surface where that subject
lives — and no amount of care afterwards can separate them.</p>

<p>The clearest damage is in the terms that belong to one surface.</p>
"""

INT2_C = """
<p>Read the first row again. Language about consumer GPUs and VRAM is <strong>up 39%</strong>
across the corpus and <strong>down 81% inside announcement space</strong>. Both are computed
from the same 15.3 million words. The aggregate rose because the document filled up with the
surface where the term is dense, and for no other reason.</p>

<p>If you had used the aggregate to decide whether the field was still paying attention to what
runs on a desktop, you would have concluded it was paying <em>more</em> attention, at the exact
moment the people announcing things stopped mentioning it almost entirely.</p>

<p class="pull">Every number I had was a weighted average whose weights were moving, and the
weights were moving faster than the thing I was trying to measure.</p>

<h2>How I found it</h2>

<p>Not from a diagnostic. There is no diagnostic — a mixture that shifts underneath you produces
series that look completely normal, with no discontinuities, no outliers and no failed
assumptions to test. Change-point detection finds breaks in the series; it cannot tell you the
series is about a different population on either side of them.</p>

<p>I found it by reading recent issues, for a different reason, and noticing that a 2026 issue
does not resemble a 2024 issue in any respect except the header. That is the same way I found
the mistake in Interlude I, one month earlier, having apparently learned nothing from it.</p>

<h2>What it cost</h2>

<p>Three findings did not survive the correction, and each failed in a slightly different way.</p>

<ul>
<li><strong><code>context rot</code> as a phenomenon in the corpus.</strong> A striking phrase,
a clean rise, and it disappears entirely once the Discord recap is excluded. It was
practitioners in chat naming a failure mode they were hitting — real, and worth knowing about,
but it was never in the field's news prose. I had reported a Discord idiom as a field-wide
development.</li>
<li><strong>"<code>agentic</code> sat next to <code>retrieval-augmented</code> in 2024."</strong>
This was my evidence that agents had absorbed RAG. Controlled for genre, <code>agentic</code>'s
2024 neighbours are <code>low-code</code> and <code>devika</code>. The adjacency was an artifact
of mixing chat and prose in one embedding.</li>
<li><strong>The fivefold rise in the number of distinct companies discussed.</strong> This one
survived the section fix and died later, to the same underlying cause: measured inside a fixed
recap section, effective diversity rises 1.1× on Twitter and 1.3× on Reddit, not 4.7×. What
I had measured was mostly the newsletter widening its sampling frame — the same header line,
again.</li>
</ul>

<h2>The fix, and the accident</h2>

<p>The repair is simple and expensive: <strong>measure inside a fixed section</strong>. The
Twitter and Reddit recaps run the whole corpus; the Discord recap runs May 2024 to March 2026.
Holding the source fixed costs you almost everything — the Twitter recap in the final half-year
is 46,815 words, against 15.3 million for the corpus — and buys you the only thing that matters,
which is that the population generating the text is roughly the same at both ends of the line.</p>

<p>Every number in this book is computed that way. Where a series has to end early, or a count
is too small to carry a ratio, the text says so.</p>

<p>And then the accident. Splitting the corpus by source to remove a confound left me with two
series where there had been one, for every pattern — announcement and practice, measured
identically, on the same days. That is not a control. That is chapter 2.</p>

<div class="aside">
<h4>Three questions for any longitudinal corpus</h4>
<p><strong>Is the unit of observation the same kind of thing at both ends?</strong> Not "does it
have the same name" — read one from each end, side by side, and see.<br>
<strong>Did the sampling frame change, and does the source tell you?</strong> Mine did, in a
line printed at the top of all 690 issues.<br>
<strong>If you split the corpus by source, does the finding survive in each part?</strong> If it
only exists in the aggregate, it may be a fact about the mixture rather than the world.</p>
</div>

<p>Two interludes, two mistakes, one shape. In the first, a field stopped meaning what it used
to mean. In the second, the document stopped being the document. Neither is visible to any check
you can run on the numbers, and both were found the same way — by reading the thing I was
counting.</p>

<p>Neither was cheap. Between them they cost four published findings and about two months.
Both were also, in the end, worth more than the results they destroyed — the first produced the
rule about reading before counting, and the second produced the three-surface split that most of
this book's better findings depend on.</p>
"""


# ---------------------------------------------------------------- chapter 10

CH10 = """
<p class="first">Retrieval-augmented generation is the most complete disappearance in this
archive. Inside announcement space it runs at 30.95 mentions per ten thousand words in early
2024 — the densest technical idea in the corpus at that point — and in the final half-year it
runs at <strong>0.21</strong>. That is a hundred-and-fortyfold fall. Nothing else measured in
this book falls that far.</p>

<h2>The name and the machinery</h2>

<p>A fall that steep has two possible explanations and the line cannot tell them apart. Either
the technique failed, or it succeeded so completely that people stopped naming it. The way to
find out is to stop counting the name and start counting the <em>mechanism</em> — embeddings,
chunking, reranking, vector indexes, semantic search, BM25 — the words you have to use if you
are actually building retrieval, whether or not you call it RAG.</p>

<div class="tw"><table><thead><tr><th>Half-year</th><th class="n">“RAG”</th>
<th class="n">its machinery</th><th class="n">machinery ÷ name</th></tr></thead><tbody>
<tr><td>2024H1</td><td class="n">23.7</td><td class="n">17.8</td><td class="n">0.8×</td></tr>
<tr><td>2024H2</td><td class="n">6.6</td><td class="n">6.2</td><td class="n">0.9×</td></tr>
<tr><td>2025H1</td><td class="n">3.2</td><td class="n">4.8</td><td class="n">1.5×</td></tr>
<tr><td>2025H2</td><td class="n">2.4</td><td class="n">8.3</td><td class="n">3.5×</td></tr>
<tr><td>2026H1</td><td class="n">1.8</td><td class="n">8.1</td><td class="n"><b>4.6×</b></td></tr>
<tr><td>2026H2</td><td class="n">2.0</td><td class="n">4.4</td><td class="n">2.2×</td></tr>
</tbody></table></div>

<p>In 2024 the name and the mechanism are mentioned about equally: if you were talking about
embeddings you were probably saying <em>RAG</em> in the same breath. The two then come apart.
The name falls thirteenfold. The machinery falls a little over twofold, and in the second half
of 2025 it is <em>higher</em> than it was in the second half of 2024 — more talk about
chunking and reranking, at the moment the word RAG had all but vanished.</p>

<p class="pull">The name fell thirteenfold. The thing it named fell by half, and spent a year
going back up.</p>

<p>This is what absorption looks like from inside a text corpus, and it is worth being precise
about what it does and does not establish. It does not show that retrieval was deployed more
widely; nothing in this archive can show that. It shows that the vocabulary of building
retrieval outlived the label by a factor that grew every half-year for two years — which is the
signature of a technique that stopped being a topic and became a component.</p>

<p>You can watch it happen in a single passage. January 2026, announcement space, at the moment
the word <em>RAG</em> is running at under two mentions per ten thousand words:</p>

<blockquote><p>LEANN: “stop storing embeddings”. A notable systems claim: index 60M text chunks
using 6GB (vs “200GB”) by storing a compact graph and recomputing embeddings selectively at
query time; pitched as enabling <strong>local RAG at new scales</strong>. Engineers should
sanity-check latency/throughput tradeoffs and recall under recomputation, but the “graph +
selective recompute” direction matches broader storage/edge constraints.</p>
<cite>AI News, Twitter recap, 2026-01-07</cite></blockquote>

<p>Sixty million chunks, an index, a recall tradeoff, and a warning about latency. That is a
retrieval engineering problem being taken seriously enough to argue about storage layouts. The
name survives only as a modifier — <em>local RAG</em> — attached to the thing that actually
matters, which is the graph.</p>

<p>Compare it to where the chapter started, February 2024, when RAG was not a component but a
product surface people complained about:</p>

<blockquote><p>Nick Dobos (of Grimoire fame) also blasted the entire knowledge files capability —
it seems the RAG system naively includes 40k characters' worth of context from docs every time,
reducing available context and adherence to system prompts.</p>
<cite>AI News lede, 2024-02-01</cite></blockquote>

<p>Two years apart, the same subject. In 2024 it is a feature with a name, behaving badly
enough to be blasted by name. In 2026 it is a storage problem with a benchmark. The word did
almost all of the dying.</p>

<p>"RAG is dead" was a real position, argued in public by people who build things, and the data
above is exactly what you would show to support it.</p>

<p>It is also wrong, and this chapter is about the test that shows why — a test that costs about
twenty minutes and works on any technology, in any field, without needing to know the story.</p>

<h2>The problem with a falling line</h2>

<p>A line going down has at least four possible causes. The idea was absorbed so completely
that nobody names it any more; the idea genuinely died; the idea was early and will come back
when the hardware does; or the measurement is broken. All four look the same on a chart, and you
can usually settle it by reading a few weeks of coverage around the fall — but reading does not
scale, and it is not falsifiable.</p>

<p>Here is a test that is both.</p>

<div class="aside">
<h4>The name / machinery test</h4>
<p>Measure two things instead of one. The <strong>name</strong> — what the idea is called. And
the <strong>machinery</strong> — the vocabulary of the mechanism the idea needs in order to
work at all, which for RAG means retrieval, chunking, reranking, vector indexes, embeddings,
BM25, hybrid search.</p>
<p>If the name falls and the machinery holds, <strong>the idea won</strong> so completely that
naming it became unnecessary. If the name falls and the machinery falls with it,
<strong>the idea died</strong>. The machinery is the tell, because an idea that shipped keeps
generating machinery talk — things inside working systems still break, get tuned, and get
argued about.</p>
</div>
"""

CH10_B = """
<p>RAG's name falls a hundred and sevenfold. Its machinery falls <strong>1.9-fold</strong>, and
it is <em>higher</em> in the first half of 2026 (13.37) than it was in the second half of 2024
(12.38). The mechanism never went anywhere. Only the label did.</p>

<p>And the line above both of them is the one that settles it. Memory — long-term memory,
memory layers, what a system keeps and retrieves across turns — goes from 12.91 to a peak of
<strong>20.74</strong>. The job RAG existed to do is discussed <em>more</em> at the end of the
corpus than at the beginning. It simply is not called RAG, because it stopped being an
architecture you choose and became something the software around the model does on every
turn.</p>

<p>You can watch that reclassification happen in the archive's own prose. In 2024, retrieval is
the subject of the sentence. By mid-2025 it has become one item in a list of ingredients — here
is a practitioner definition quoted in the newsletter in June 2025, of the thing that replaced
it: <em>“filling the context window with just the right information for the next step … task
descriptions and explanations, few shot examples, RAG, related (possibly multimodal) data,
tools, state and history, compacting.”</em> RAG appears in that sentence as a comma-separated
component of somebody else's job.</p>

<h2>The control</h2>

<p>A test that returns “absorbed” for everything is worthless, so run it on something that
actually died.</p>

<p>Model merging — averaging the weights of two separately fine-tuned models to get something
better than either — had tooling, named methods and a genre of results in 2024. Its name goes
1.16, 2.40, 0.69, 0.14, <strong>0.00, 0.00</strong>. Its machinery — weight averaging, weight
interpolation, task vectors, task arithmetic — never exceeds <strong>0.37 anywhere in the
corpus</strong>, in any surface, and is 0.00 at the end. There is no residue. Nobody argues
about the tuning of a thing nobody ships.</p>

<p>That is what death looks like, and it does not look like RAG.</p>

<h2>Three more, without commentary</h2>
"""

CH10_C = """
<p>Read the middle two columns as one ratio. <strong>Fine-tuning</strong> is the case most
often cited as a technology that failed: the name falls eighteenfold. Its machinery — LoRA,
QLoRA, PEFT, adapters, SFT, instruction tuning, post-training, synthetic data — falls 1.6-fold
and sits at 9.83 at the end of the corpus. Fine-tuning did not stop. It stopped being a topic
and became a step.</p>

<p><strong>Prompt engineering</strong> is the strongest case in the table: the name falls
eightfold while its machinery — system prompts, few-shot examples, instruction files,
compaction, context management — <em>rises</em> 1.7-fold. An idea whose vocabulary of practice
grows while its name disappears is not in decline by any reading.</p>

<h2>The fifth fate</h2>

<p>The fourth row is doing something the other rows are not, and it needs its own name.</p>

<p><code>MMLU</code>, <code>HumanEval</code> and <code>GSM8K</code> — the benchmarks that
defined 2024 — fall twenty-onefold, from 4.33 to 0.21. But their machinery is not diffuse
mechanism vocabulary. It is <strong>a specific list of successors</strong>: SWE-bench, ARC-AGI,
GPQA, FrontierMath, Terminal-Bench, SciCode, AIME, LiveBench. Those rise from 0.77 to 9.40, a
twelvefold gain, and they occupy the exact role the old ones did.</p>

<p>That is <strong>replacement</strong>, and it is worth separating from absorption because
the two imply opposite actions. When something is absorbed, the mechanism is still there and
your system is already using it; leave it alone. When something is replaced, there is a named
successor doing the same job and you should migrate.</p>

<div class="tw"><table>
<caption>Five fates, and how to tell them apart from the outside</caption>
<thead><tr><th>Fate</th><th>The name</th><th>The machinery</th><th>What to do</th></tr></thead>
<tbody>
<tr><td><b>Absorbed</b></td><td>falls hard</td><td>holds or rises</td><td>nothing; you are
already using it</td></tr>
<tr><td><b>Replaced</b></td><td>falls hard</td><td>a named successor rises</td><td>migrate</td></tr>
<tr><td><b>Dead</b></td><td>falls to zero</td><td>falls to zero</td><td>drop it, and check what
depended on it</td></tr>
<tr><td><b>Deferred</b></td><td>falls in announcement, returns in practice</td><td>reappears
with new hardware or tooling</td><td>watch practice space</td></tr>
<tr><td><b>Artifact</b></td><td>falls in the aggregate only</td><td>holds in every
surface</td><td>fix the instrument</td></tr>
</tbody></table></div>
"""

CH10_D = """
<h2>When the test fails</h2>

<p>It is a cheap test and cheap tests have failure modes. Three of them matter.</p>

<p><strong>Generic machinery vocabulary.</strong> My <code>memory</code> line is the weakest
number in this chapter: the word means at least three things in this corpus — what a system
retains across turns, what a model has memorised, and how many gigabytes a GPU has. The rise
from 12.91 to 20.74 is real but it is not purely about retrieval, and I would not build a
decision on that line alone. The retrieval-machinery line, which uses specific terms, is the
one carrying the argument.</p>

<p><strong>Shared machinery.</strong> Two ideas can need the same mechanism, in which case the
mechanism's persistence tells you one of them survived but not which. Embeddings serve
retrieval, classification, clustering and search alike.</p>

<p><strong>The instrument.</strong> All of this has to be measured inside a fixed source. The
mix of sources in this archive inverts over three years, and a count taken across the whole
document partly measures that inversion rather than the field — so run the name/machinery test
on unsegmented text and you will get a confident answer about your own sampling.</p>

<h2>Running it forwards</h2>

<p>The test also works in the other direction, which is where it earns its keep, because
falling lines are a retrospective problem and rising lines are a decision you have to make now.</p>

<p>Take the biggest rising line in the archive. <code>Agentic</code> language in announcement
space rises eightfold between 2024 and 2026. Its machinery — orchestration, sub-agents,
tool-use, sandboxing, scaffolding — rises <strong>nineteenfold</strong>, faster than the name
itself. Whatever else is true about the agent narrative, real engineering vocabulary is
accumulating underneath it faster than the label is, which is not what a purely marketed term
looks like. Compare model merging in its best year: the name rose and the machinery never
arrived at all.</p>

<p>So the rule is symmetric, and it is the whole chapter in two lines:</p>

<p class="pull">A name that rises faster than its machinery is a term being marketed. A name
that falls while its machinery holds is a technology that won.</p>

<p>Neither is visible in the line everybody quotes, and both take about twenty minutes to
check.</p>
"""


# ---------------------------------------------------------------- chapter 11

CH11 = """
<p class="first">In the last half-year of this archive, <code>MMLU</code> appears zero times in
announcement space. So does <code>HumanEval</code>. So do <code>GSM8K</code>,
<code>MT-Bench</code> and <code>AIME</code>. Every general-knowledge and fixed-problem-set
benchmark that defined how the field ranked models in 2024 reaches literal zero, in 46,815
words of text about model launches.</p>

<p>They were not discredited. There was no scandal and no replacement announcement. They
stopped being mentioned, one at a time, over about two years — and the pattern of how long each
one lasted turns out to be regular enough to plan around.</p>

<h2>How long a scoreboard lasts</h2>

<p>Take each benchmark's density inside the same fixed recap section, quarter by quarter. Find
the quarter it peaks. Then find the first quarter after that where it has fallen below a quarter
of its peak value — the point at which the field has functionally stopped using it.</p>
"""

CH11_B = """
<p>The median is <strong>three quarters from peak to irrelevance</strong>. MT-Bench managed
one. MMLU and HumanEval, the two benchmarks that appear in almost every model card of early
2024, managed two each. The most durable of the fixed-answer benchmarks, GPQA and AIME, managed
four.</p>

<p>Three never fell at all, and they are the interesting ones. But first, why the others
went.</p>

<h2>Saturation, and then contamination</h2>

<p>A benchmark is a fixed set of questions with known answers. That design has a built-in
expiry date, and it expires twice.</p>

<p>The first expiry is <strong>saturation</strong>. Once the leading models score 90% on
something, the remaining 10% is disproportionately made of ambiguous items and mislabelled
answers, and the benchmark can no longer rank anything. A test that everyone passes measures
nothing, and the field's response is not to fix it but to stop citing it.</p>

<p>The second expiry is <strong>contamination</strong>, and it is worse because it is invisible.
The questions are published so people can use them; being published means being on the public
internet; being on the public internet means being in the next model's training data. At that
point a high score may mean the model can reason, or may mean it has seen the answer, and
nothing about the number distinguishes those.</p>

<p>You can watch the anxiety about this build. Contamination language in announcement space runs
at 0.39 in early 2024 and <strong>1.92</strong> in the final half-year — its highest value in
the corpus, at the point where most of the benchmarks it refers to have already gone quiet.</p>

<p>By late 2025 it has stopped being a caveat and become a design requirement. Here is the
newsletter describing a new benchmark in September 2025, and note where contamination sits in
the list of features:</p>

<blockquote><p>SWE-Bench Pro: a harder successor to SWE-Bench Verified with multi-file edits
(avg ~107 LOC across ~4 files), <strong>contamination resistance (GPL/private repos)</strong>,
and tougher deps. Current top scores: GPT-5 = 23.3%, Claude Opus 4.1 = 22.7%, most others
&lt;15%.</p>
<cite>AI News, 2025-09-22</cite></blockquote>

<p>Contamination resistance is listed between the edit size and the dependency difficulty, as an
ordinary engineering property of the artifact. And the top score is 23.3%, which is what a
benchmark looks like before it saturates.</p>
"""

CH11_C = """
<h2>The replacement that also died</h2>

<p>If fixed questions saturate and leak, the obvious fix is to stop asking fixed questions. Show
two anonymous answers to a human, ask which is better, and aggregate a few million of those into
a ranking. That is the Chatbot Arena, and for a while it was the most-cited scoreboard in the
field: 2.63 in early 2024, 8.32, and a peak of <strong>12.04</strong> in the first half of
2025.</p>

<p>Then it goes 6.93, 0.56, <strong>0.43</strong>.</p>

<p>Two entries from April 2025 explain the fall better than the series does. The first is about
what the ranking measures:</p>

<blockquote><p>lm-sys highlighted the importance of style and model response tone on Arena,
demonstrated in style control ranking … They updated their leaderboard policies to reinforce
their commitment to fair, reproducible evaluations. [@vikhyatk] shared that <strong>this is the
clearest evidence that no one should take these rankings seriously</strong>.</p>
<cite>AI News, 2025-04-09</cite></blockquote>

<p>The operators found that response style and tone were driving the votes, and shipped a
correction for it. A prominent practitioner read the existence of the correction as proof the
whole thing was unsound. Both reactions are defensible, which is the problem.</p>

<p>The second is about what the ranking is a ranking <em>of</em>:</p>

<blockquote><p>Llama 4 quietly dropped from <strong>1417 to 1273 ELO</strong>, on par with
DeepSeek v2.5.</p>
<cite>AI News, 2025-04-14</cite></blockquote>

<p>A hundred and forty-four Elo points, because the checkpoint that had been evaluated was not
the checkpoint that shipped. A score you cannot reproduce on the model you are able to call is
not a score about that model.</p>

<p class="pull">Human preference is a real signal and also a measurement of formatting, length
and tone. The moment it becomes the target, it measures the targeting.</p>

<h2>What survived</h2>
"""

CH11_D = """
<p>Three benchmarks in this archive never fall below a quarter of their peak, and two of them
are still climbing when the corpus ends. <strong>SWE-bench</strong> asks a model to fix a real
issue in a real repository, and the test suite decides whether it worked.
<strong>Terminal-Bench</strong> asks it to drive a shell to a goal state.
<strong>ARC-AGI</strong> asks it to solve visual puzzles it has not seen, from a private
holdout set.</p>

<p>What they have in common is not difficulty. It is that <em>none of them has an answer
key</em>.</p>

<div class="aside">
<h4>Why task benchmarks outlive quiz benchmarks</h4>
<p><strong>There is a verifier, not a lookup.</strong> The tests pass or they do not; the shell
reaches the goal state or it does not. Correctness is computed rather than looked up, which
makes this class of benchmark markedly harder to contaminate than one scored against a
published table of answers.<br>
<strong>The task space is effectively unbounded.</strong> There are always more repositories and
more shell tasks. When the current set saturates you add harder instances, which is a data
problem rather than a redesign.<br>
<strong>Partial credit is meaningful.</strong> A 23% pass rate leaves room to rank things.
A 94% multiple-choice score does not.</p>
</div>

<p>The same logic produced a structural fix for the quiz-style benchmarks that survived by
changing what they are. From October 2025:</p>

<blockquote><p>Rolling “Humanity's Last Exam”: CAIS released a <strong>dynamic fork</strong> of
the well-known eval dataset that <strong>swaps easier questions for harder ones as models
improve</strong>; gated to avoid contamination.</p>
<cite>AI News, 2025-10-08</cite></blockquote>

<p>A benchmark that is a service rather than a file. It cannot saturate because it replaces its
own easy items, and it cannot leak because the items are not all public. That is the same two
defences the task benchmarks get for free.</p>

<h2>The other replacement, and its catch</h2>

<p>Running enough real tasks is expensive, so the field did the other obvious thing: it asked a
model to grade the output. LLM-as-judge language rises from 1.08 to <strong>4.27</strong>, and
by the end of the corpus it is denser than any individual benchmark except the task suites.</p>

<p>This solves cost and scale and does not solve validity. You have replaced a fixed set of
questions whose answers might be in the training data with a grader whose own behaviour changes
every time it is updated — and whose preferences, like the Arena's, include style. It is a
reasonable tool for regression testing against yesterday's output. It is a weak instrument for
deciding whether one model is better than another, and the archive does not contain a single
result that resolves that.</p>
"""

CH11_E = """
<div class="aside">
<h4>What to do about scores</h4>
<p><strong>Assume roughly three quarters of useful life from a public benchmark's peak.</strong>
Plan to replace your evaluation set on that cadence rather than standardising on one.<br>
<strong>Prefer a verifier to an answer key.</strong> If correctness is computed — tests pass,
goal state reached, output parses and satisfies constraints — the benchmark resists both
saturation and leakage.<br>
<strong>Distrust any score you cannot reproduce on the checkpoint you can actually call.</strong>
A hundred and forty-four Elo points separated the evaluated Llama 4 from the shipped one.<br>
<strong>Keep a private held-out set drawn from your own traffic.</strong> It cannot leak, it
cannot saturate while your traffic changes, and it measures the only thing you actually care
about.</p>
</div>

<p>The field went through roughly a dozen scoreboards in thirty-two months. The ones it kept are
the ones that ask a model to do something and then check whether it worked; the ones it dropped
are the ones that ask a model a question someone already knows the answer to. That is a smaller
claim than "benchmarks are broken", and a more useful one, because it tells you which kind to
build.</p>
"""


# ---------------------------------------------------------------- chapter 12

CH12 = """
<p class="first">Here is a description of an agent, from September 2024:</p>

<blockquote><p>The big launch of the day is <strong>Replit Agent</strong> … full text to running
app generation with planning and self healing … it is live today to paid users, and can deploy
on a live URL with postgres backend, from <strong>people who cannot code</strong>, including on
your phone. Of course, Replit Agent can even make a Replit clone.</p>
<p>There are unfortunately no benchmarks or even blogposts to write about. Which makes our job
simple. Watch video, try it, or scroll on.</p>
<cite>AI News, 2024-09-05</cite></blockquote>

<p>And here is a description of an agent, from June 2026:</p>

<blockquote><p>M3 was presented as an open-weight multimodal agent/coding model with 1M context,
native multimodality, and competitive agent benchmarks. The headline figures repeated across
launch partners were <strong>59.0% SWE-Bench Pro, 66.0% Terminal Bench 2.1, and 74.2% MCP
Atlas</strong>.</p>
<cite>AI News, 2026-06-01</cite></blockquote>

<p>In 2024 an agent is a <em>product</em>, sold to people who cannot program, and the newsletter
notes with mild regret that there is nothing to measure. In 2026 an agent is a <em>property of a
model</em>, and it is nothing but measurements.</p>

<p>Both passages are about agents. A count of the word across both is not counting one thing,
and this chapter is about how far that problem extends, how to detect it, and what it does to
software that has been running for two years.</p>

<h2>Measuring a word's meaning</h2>

<p>You cannot ask a corpus what a word meant. You can ask what company it kept, which turns out
to be nearly as good.</p>

<div class="aside">
<h4>How the measurement works</h4>
<p>Train a small word-embedding model on the 2024 text alone. It learns a position for every
word such that words appearing in similar contexts land near each other — <code>GPU</code> near
<code>VRAM</code>, <code>latency</code> near <code>throughput</code>. Train a second model on
the 2026 text alone. Each model has its own arbitrary coordinate system, so the two are not
directly comparable; you align them by finding the rotation that best matches the words whose
meaning is least likely to have moved, then apply it. Now the two spaces are in register, and
you can ask, for any word, how far its neighbourhood moved.</p>
<p>The number reported below is the cosine distance between a word's 2024 neighbourhood and its
2026 one. Zero means the same company; one means an entirely different crowd.</p>
</div>

<p>Run that over the corpus and the median technical term moves 0.313. Here are the extremes,
with the actual nearest neighbours in each period.</p>
"""

CH12_B = """
<p>Read the two neighbour columns rather than the numbers. In every high-drift row, the words on
the left and the words on the right belong to different subjects — not to a more advanced
version of the same subject.</p>

<h2>The largest: a word that became a file format</h2>

<p><code>Skills</code> moves 0.590, further than anything else in the corpus, and its trajectory
is unusually easy to follow because it has three distinct phases in the archive.</p>

<p>In April 2024 it is a term in an argument about what intelligence is:</p>

<blockquote><p>Any task that does not involve significant novelty and uncertainty can be solved
via memorization, but <strong>skill is never a sign of intelligence</strong>.</p>
<cite>François Chollet, quoted in AI News, 2024-04-01</cite></blockquote>

<p>Ten days later it is a robotics term:</p>

<blockquote><p>Learning Agile Soccer Skills: DeepMind trained AI agents to demonstrate
<strong>agile soccer skills like turning, kicking, and chasing a ball</strong> using
reinforcement learning.</p>
<cite>AI News, 2024-04-11</cite></blockquote>

<p>And in October 2025 it is neither. It is a directory layout:</p>

<blockquote><p>Anthropic gets two back-to-back headline stories with <strong>Agent Skills</strong>
today, “a new way to build specialized agents <strong>using files and folders</strong>”. It turns
out that Claude's recent new skills for creating and reading PDFs and Docs and PPTs were all
Skills.</p>
<cite>AI News, 2025-10-16</cite></blockquote>

<p>A philosophical claim about the nature of intelligence, then motor control in a physical
robot, then a convention for laying out files on disk. One string, three referents, nineteen
months. Its neighbours move from <code>goals, abilities, experiences</code> to
<code>middleware, reusable, ide, filesystem</code>, which is exactly what you would expect a
word to do on that journey.</p>
"""

CH12_C = """
<h2>The control, and why 0.590 is not noise</h2>

<p>A drift score is only meaningful if some words hold still, and one does.
<code>Context</code> moves <strong>0.170</strong>, the least of anything measured. Its 2024
neighbours are <code>window, length, contexts, yarn</code>; its 2026 neighbours are
<code>window, length, cache, kv, batch</code>.</p>

<p>Look at what stayed and what changed. <code>Window</code> and <code>length</code> are in both
lists — the core of the concept never moved. What arrived is <code>cache</code>,
<code>kv</code> and <code>batch</code>: the implementation. In 2024 the field discussed context
as a specification (how long is the window, how do you extend it). By 2026 it discusses it as a
resource with a memory layout and a scheduling problem. The subject is the same and the
engineering matured underneath it.</p>

<p>That is what a stable term looks like, and it gives the scale meaning. 0.170 is a concept
acquiring an implementation. <strong>0.590 is a different concept wearing the same word.</strong></p>

<h2>Why this is a software problem</h2>

<p>None of this would matter if the words only appeared in prose. They appear in systems.</p>

<ul>
<li><strong>Any metric keyed on a term.</strong> A dashboard counting mentions, tickets, queries
or documents matching <code>agent</code> has been running continuously across a 0.371 drift.
The line is smooth. The subject changed underneath it.</li>
<li><strong>Evaluation suites.</strong> A test set assembled in 2024 to check “agent behaviour”
was assembled against the 2024 referent — planning and self-healing app generation for
non-programmers. Run it in 2026 and it still passes or fails, and the number still goes in the
report, and it is no longer measuring the thing anyone means.</li>
<li><strong>Classifiers and routing rules.</strong> Anything keyword-triggered inherits the
drift silently. A rule that routes “skills” questions to the robotics team was correct for a
year and is now sending filesystem-layout questions there.</li>
<li><strong>Retrieval over a corpus that spans the change.</strong> If your index covers 2024 and
2026 documents, a query for <code>skills</code> retrieves three unrelated subjects and ranks
them by lexical similarity, which is precisely the case where lexical similarity is
uninformative.</li>
<li><strong>Training-data filters.</strong> A keyword filter written once and reused is a
definition frozen at the moment it was written.</li>
</ul>

<p class="pull">There is no exception this class of error throws. The count is correct; the label
is stale; every downstream consumer processes the new thing under the old name.</p>
"""

CH12_D = """
<h2>What to do about it</h2>

<div class="aside">
<h4>Four habits that catch drift</h4>
<p><strong>Store the definition next to the metric.</strong> Not the regular expression — a
sentence saying what you meant, and three example matches from the week you wrote it. Drift is
obvious the moment you compare today's matches with those three; it is invisible otherwise.<br>
<strong>Re-read twenty random matches a quarter.</strong> Not the aggregate, not the top hits —
a random sample, read by a person. This is the only check that reliably catches referent change,
and it takes twenty minutes.<br>
<strong>Watch the neighbours, not the count.</strong> If you can afford it, track which terms
co-occur with yours. The neighbourhood shifts before the count does anything visible, so it is
an early warning rather than a post-mortem.<br>
<strong>Key on mechanisms where you can.</strong> <code>Retrieval</code>, <code>sandbox</code>
and <code>kv-cache</code> name machinery and drift slowly. <code>Agent</code>,
<code>skills</code> and <code>safety</code> name categories, and categories are what marketing
and regulation both act on.</p>
</div>

<p>The last one is the closest thing to a general rule here, though the sample is eight words
and it should be held loosely. Words for things that exist inside a computer tend to hold still:
the most stable term measured, <code>context</code>, is the only one of the eight that names a
data structure. The two largest movers are a category name that a company attached to a product
(<code>skills</code>) and a technique that acquired a legal meaning (<code>distillation</code>) —
neither of which is a change in the engineering, and both of which move the word.</p>

<p>A word is not a measurement. It is a pointer to a measurement, and nothing in your pipeline
checks that the pointer is still valid.</p>
"""


# ---------------------------------------------------------------- chapter 13

CH13 = """
<p class="first">Every Discord channel heading in this archive looks like this:</p>

<blockquote><p><code>### **Unsloth AI (Daniel Han) ▷ #[general](…)** (1123 messages🔥🔥🔥):</code></p>
<cite>AI News, a typical Discord channel heading</cite></blockquote>

<p>That number is not an editorial judgement. Nobody decided the conversation was worth 1,123
units of importance. A bot counted the messages that existed in a room on a day, and printed
the count. Across the whole archive there are <strong>31,607 of those channel-day records,
covering 2,142,082 messages in 56 servers</strong>, from May 2024 to March 2026.</p>

<p>Everything else in this book measures what a publication chose to write about. This measures
what people did, whether or not anyone wrote about it — and what people did turns out to be
duller, more repetitive, and far more constrained by money than any announcement suggests.</p>

<h2>Where the words actually are</h2>

<p>Sort all 2.14 million messages by the kind of channel they were posted in and the result is
lopsided enough to be worth staring at.</p>
"""

CH13_B = """
<p><strong>Five sixths of everything happens in a channel called <code>general</code>.</strong>
A single channel name accounts for 1,397,089 messages — 65% of the entire corpus on its own.
Structured help channels account for 3.2%. Research and paper channels account for 1.9%.
Showcase channels, where people post the things they built, account for 0.6%.</p>

<p>If your mental model of a technical community is a place where people ask well-formed
questions and receive well-formed answers, the census does not support it. The activity is
overwhelmingly undifferentiated conversation, and the second-largest identifiable topic — after
<code>general</code>, <code>ai-discussions</code> and <code>off-topic</code> — is hardware.
<code>hardware-discussion</code> carries 46,273 messages, which puts it fractionally ahead of
every channel named <code>help</code> in the archive combined.</p>

<p>Here is what that channel contains, on three consecutive working days in January 2025:</p>

<blockquote><p>@octaviagoetia expressed a preference for using GPUs over online APIs, citing
concerns over <strong>TOS restrictions</strong> and potential latency issues. @heychazza agreed,
highlighting the benefits of using a beefy laptop for tinkering with LLMs <strong>without
worrying about unexpected costs</strong>.</p>
<p>Users noted that running a 70B model requires more VRAM than available on common GPUs,
leading to reliance on slower CPU inference. Recommendations included <strong>sticking to models
under 16B with Q8 or Q6 quantization</strong> for better performance.</p>
<p>@octaviagoetia is currently using Llama 3.1 for <strong>generating quest lines</strong>, with
plans to upgrade to Llama 3.2 1b, finding it more creative and efficient.</p>
<cite>AI News, Discord recap, LM Studio #hardware-discussion, 2025-01-03 to 2025-01-07</cite></blockquote>

<p>Terms of service, electricity bills, VRAM ceilings, and someone generating quest lines for a
game on a laptop. That is the ground floor of this field by volume, and none of it appears in
any launch post.</p>
"""

CH13_C = """
<h2>The busiest room in the archive</h2>

<p>Rank the 56 servers by total messages and the top of the list is not a frontier lab.</p>
"""

CH13_D = """
<p><strong>Unsloth AI is a fine-tuning toolchain</strong>, and it is the most active community
in this corpus: 302,248 messages across 23 months, more than the OpenAI server and the
HuggingFace server put together. It is busiest in exactly the period when the practice it
supports had largely stopped being written about.</p>

<p>Two other entries are worth pulling out. <strong>LMArena and Cursor Community both appear in
March 2025</strong> and are immediately among the busiest rooms in the archive — evaluation and
coding agents arriving as fully-formed communities rather than growing into them. And
<strong>BASI Jailbreaking</strong>, which starts in November 2025, has the highest activity rate
of any server measured: <strong>19,062 messages per month</strong>, ahead of every established
community including the ones that had been running for two years.</p>

<h2>Two ways this census lies to you</h2>

<p>The counts are mechanical, which makes them tempting to over-read. There are two specific
traps in this data and both took me a while to see.</p>

<p><strong>The identity key is a display name.</strong> Servers appear to die when they have
only been renamed. <em>Cursor IDE</em> runs from November 2024 to April 2025 and stops;
<em>Cursor Community</em> starts in March 2025 and continues. <em>CUDA MODE</em> ends in
September 2024; <em>GPU MODE</em> begins the same month. <em>OpenRouter (Alex Atallah)</em> ends
in August 2025; <em>OpenRouter</em> begins in August 2025. Nothing in the record links them.
Take the birth and death dates literally and you will report a churn of communities that is
partly a churn of strings.</p>

<p><strong>The sample changes underneath the counts.</strong> This is the larger problem.</p>
"""

CH13_E = """
<p>The number of servers sampled runs at about 30 for sixteen months and then drops to
<strong>23 in September 2025</strong> and stays there. That single decision produces a cluster
of servers whose last appearance is August 2025 — Cohere, LlamaIndex, Notebook LM, MCP (Glama)
— and every one of them looks, in the raw data, like a community that died in the same month.
They did not. They were dropped from a list.</p>

<p>The same decision inflates the other line. Messages per sampled server rises from 1,665 in
May 2024 to 6,941 by February 2026, and some of that is real growth and some of it is the
sample being pruned down to the busiest rooms. There is no way to separate the two after the
fact.</p>

<div class="aside">
<h4>What this surface can and cannot support</h4>
<p><strong>It can support:</strong> the trend inside a server that is present throughout.
Nobody wrote those messages for a newsletter and the count is a count, so a server going from
5,000 to 15,000 messages a month is a real change in how busy that room was.<br>
<strong>It cannot support:</strong> comparisons across servers that enter and leave the sample;
any claim about the absolute size of the field, since this is 56 English-language servers on one
editor's list; and anything at all after March 2026, when the section was dropped.</p>
</div>

<h2>What the practice layer looked like</h2>

<p>Put the census together and the practice layer of this field, measured by message volume
rather than by coverage, is remarkably consistent across two years. It is people in an
undifferentiated chat room, talking mostly about what they can afford to run, on hardware they
own, using models they downloaded — and the single largest such room in the archive exists to
help them modify those models.</p>

<p>There is no version of that sentence that would work as a launch announcement, which is
precisely why it is worth measuring separately. Announcements are about what becomes possible.
This is a record of what practitioners were <em>talking about</em> while that was being
announced — not a census of what ran anywhere — and the constraint shaping that talk was never
capability. It was <strong>VRAM, terms of service, and the electricity bill</strong>.</p>

<p class="pull">Practitioner talk about a technology is usually duller than its coverage,
more repetitive, and organised around what things cost.</p>
"""


# ---------------------------------------------------------------- chapter 14

CH14 = """
<p class="first">The model tag <code>gpt-4o-2024-08-06</code> appears in this archive in four
issues, across <strong>two days</strong>. The tag <code>gemini</code> appears across
<strong>973</strong>. In August 2024 both were things you could have written into a config file
and shipped.</p>

<p>That spread is the practical problem this chapter is about. Every integration built on a
model is a dependency with an expiry date, the date is not published, and the difference between
the shortest and longest lives in this corpus is a factor of nearly five hundred. So: given a
model you are about to build on, what is the distribution?</p>

<h2>Why you cannot just average the lifespans</h2>

<p>The obvious approach — take every model, subtract its first mention from its last, average —
is wrong in a way that gets worse the more recent your data is. A model first mentioned last
month and still being discussed today has not had a one-month life. Its life is
<em>unfinished</em>, and counting it as one month drags the average down. Worse, it drags it
down hardest for the newest models, which are exactly the ones you want to compare against the
old ones.</p>

<div class="aside">
<h4>Survival analysis, in one box</h4>
<p>This is the standard problem in medical statistics — patients still alive when the study ends
— and the standard fix is the Kaplan-Meier estimator. Rather than averaging lifespans, it walks
forward in time and asks, at each moment when something died, what fraction of the things still
being observed died then. Multiply those fractions together and you get a curve: the probability
of surviving past any given age. Things still alive at the end contribute to the denominator for
as long as they were watched and then drop out without counting as deaths. That is called
right-censoring, and handling it is the entire reason to use this method.</p>
<p>Here, birth is a model's first mention, and death is its last mention, provided that last
mention is more than 90 days before the archive ends. Models mentioned recently are treated as
alive.</p>
</div>

<p>Run that over every model tag appearing in at least three issues — 255 of them — and the
answer to “how long will it stay relevant” is a curve rather than a number.</p>
"""

CH14_B = """
<p>The median is <strong>137 days</strong>. Four and a half months from a model's first mention
to the halfway point of its time in the conversation.</p>

<p>Stated as a decision table, it is blunter:</p>
"""

CH14_C = """
<p>If you pin an integration to a specific checkpoint today, there is a <strong>one in five
chance anyone is still talking about it in a year</strong>, and a one in twenty chance in two.
Pin to the family instead and those become roughly one in two and one in five.</p>

<h2>The result I published, which was wrong</h2>

<p>Split the same 255 tags by cohort and something jumps out.</p>
"""

CH14_D = """
<p>Read the left half of that table. Models from Chinese labs have a median life of
<strong>85 days</strong> against 175 for US frontier labs — less than half the shelf life. That
is a clean, quotable, decision-relevant finding, and I published it, with a note that it might
be a naming artifact.</p>

<p>It is a naming artifact. Collapse version and size suffixes so that
<code>qwen3.5-235b-a22b</code>, <code>qwen3.6</code> and <code>qwen3.8-max</code> count as one
subject rather than three, and read the right half of the table. The cohort with the shortest
individual lives has <strong>the longest family lives of any group measured</strong>: 398 days
against 315 for US frontier labs.</p>

<p>The ranking inverts completely, on the same data, from one decision about what counts as a
thing.</p>
"""

CH14_E = """
<h2>Why it inverts</h2>

<p>Two measurable causes, and neither is flattering to the original result.</p>

<p><strong>Naming granularity.</strong> Inside this cohort, Chinese labs produce
<strong>5.44 distinct model tags per family</strong> against 4.03 for US frontier labs. More
named checkpoints per underlying thing means each individual name is shorter-lived by
construction, before anything about quality or adoption enters. A lab that ships
<code>kimi-k2</code>, <code>kimi-k2-0905</code>, <code>kimi-k2-thinking</code> and
<code>kimi-k2-turbo-preview</code> will look, at tag level, like four models that each died
young.</p>

<p><strong>Cohort age.</strong> The median Chinese tag first appears on
<strong>2025-07-29</strong>. The median US frontier tag first appears on
<strong>2024-09-13</strong> — eleven months earlier. The estimator handles censoring correctly,
but a cohort concentrated in the final year of the corpus is estimated from far less evidence
than one spread across all three, and its curve is correspondingly jumpy: the Chinese tag curve
below sits flat at 12.9% for five straight months because almost nothing in that group is old
enough to produce another event.</p>

<div class="warn">
<p>The corrected figure rests on <strong>21 Chinese families</strong>. It is the better
estimate — it is measuring subjects rather than strings — and it is not a precise one. Treat
“longest-lived” as “not shortest-lived, and probably above average”, and do not build a
procurement policy on the difference between 398 and 315.</p>
</div>
"""

CH14_F = """
<h2>What this is a clock for</h2>

<p>One thing this number is not: a switch-off date. <code>GPT-4</code> remained callable long
after the conversation moved on, and a model dropping out of this archive says nothing about
whether its endpoint still answers.</p>

<p>What it does measure is how long the field keeps paying attention, and that turns out to be
the clock that governs most of what actually goes wrong with an integration:</p>

<ul>
<li>How long the community answers stay accurate. Stack Overflow-style knowledge about a
checkpoint's quirks stops accumulating when the conversation does.</li>
<li>How long third-party tooling keeps testing against it — quantizations, serving configs,
adapter formats, prompt libraries.</li>
<li>How long the documentation you are relying on stays maintained.</li>
<li>Whether the next engineer to touch your code has heard of the thing it depends on.</li>
</ul>

<div class="aside">
<h4>Four things to do with a 137-day median</h4>
<p><strong>Pin to a family, not a checkpoint</strong>, wherever the API allows it. The whole
difference between the two columns of that decision table is this one choice.<br>
<strong>Expect checkpoint churn on roughly this cadence</strong> for anything keyed to a
specific checkpoint. Note what the 137 days actually measures: how long a checkpoint keeps
being <em>talked about</em>, which is a hypothesis about how long it keeps being supported,
not a measurement of it. Vendors deprecate on their own schedule, and the two clocks are
correlated rather than identical — so use this to decide what to keep loosely coupled, not to
set a maintenance calendar.<br>
<strong>Depreciate checkpoint-specific work on the same clock.</strong> Prompts tuned to one
model's quirks, few-shot examples chosen for its failure modes, and thresholds calibrated to its
scores are all assets with a four-month half-life. Anything you would be unwilling to redo twice
a year should not depend on a specific checkpoint.<br>
<strong>Choose the ecosystem, not the score.</strong> What persists across a family is the
tooling around it — the quantizations, the serving stack, the community's accumulated tricks.
That is what you are really adopting, and it outlives any individual set of weights by a factor
of about two.</p>
</div>

<p class="pull">A model is a dependency whose version you do not control, on a release cadence
nobody publishes, with a median attention span of four and a half months.</p>

<p>That is a worse deal than almost any library you have ever taken, and it is priced into
nothing. The single cheapest mitigation is the one in the table above: depend on the family
name, and let the lab decide which weights are behind it.</p>
"""


# ---------------------------------------------------------------- interlude III

INT3 = """
<p class="first">Six findings in this work were published and then withdrawn or reversed. That
is the honest number, and it is worth setting out in one place — not as a penance, but because
they are not six unrelated mistakes. They are three mistakes made twice each, and each of the
three has a different detection method that costs almost nothing to run.</p>
"""

INT3_B = """
<h2>The first kind: the archive was a copy, and the copy was lossy</h2>

<p>Three of the seven come from treating a database field as though its contents were stable.
The <code>title</code> column of this archive contains a title in 2023 and, increasingly, a
placeholder afterwards, and the human-written opening underneath it goes the same way.</p>
"""

INT3_C = """
<p>Eight percent of 2023 issues open with a non-title — <em>not much happened today</em>,
<em>a quiet weekend</em>, <em>small news items</em>. By the end of the archive it is
<strong>85%</strong>, including days carrying frontier model launches and billion-dollar
funding rounds.</p>

<p>Any series built on titles therefore has a denominator that is quietly filling with blanks.
Every company's headline share falls; I picked the two I expected to fall and wrote a story
about them. The same mechanism produced a second finding — that quiet-day language was rising,
so the field was slowing down — which is a measurement of the template rather than the
field.</p>

<p><strong>Detection:</strong> read the values, not the schema. Twenty rows, spread across the
range, read by a person. It takes an afternoon and nothing else catches this.</p>

<p><strong>What reading the values still missed.</strong> Nothing above is wrong, and it is
only half the story. Reading the archive carefully establishes that its title field went blank;
it cannot establish <em>why</em>, because the answer is not in the archive. Against 397 issues
recovered from the sent emails, the stored and published series track each other through 2024
and 2025 — matching exactly in 2025H1, across 118 issues — the editor really was templating more — and then diverge sharply in 2026, where
64% stored meets 4.6% sent. Four consecutive March 2026 issues the archive files as <em>not much
happened today</em> went out as <em>Context Drought</em> and <em>NVIDIA GTC: Jensen goes hard on
OpenClaw, Vera CPU, and announces $1T sale</em>. So a real trend and a broken pipeline ran in
the same column, in opposite directions, and no amount of careful reading <em>within</em> the
archive separates them. Detection at this level costs more than an afternoon: it requires a
second copy of the data, obtained by a different route.</p>

<h2>The second kind: the document stopped being the document</h2>

<p>Three of the seven come from one cause. The archive's issues are assembled from three kinds of
source — chat logs, forum threads and posts — and the proportions invert completely across the
corpus. The median issue in early 2024 is almost entirely chat; the median issue at the end
contains none at all.</p>

<p>A count taken across a whole issue is therefore a weighted average whose weights are moving,
and the weights move faster than most of the things being measured. That produced three separate
published claims, each with a different flavour of wrong:</p>

<ul>
<li>A term that existed only in chat logs, reported as a field-wide concern.</li>
<li>Two terms that appeared to be neighbours, because their genres were mixed in one embedding
rather than because anyone used them together.</li>
<li>A fivefold rise in the diversity of subjects discussed, which was mostly the newsletter
adding sources — the sampling frame widened from 7 subreddits to 12 and from 384 accounts to
544 over the same window.</li>
</ul>

<p><strong>Detection:</strong> split the corpus by source and re-run. If the finding only exists
in the aggregate, it may be a fact about the mixture rather than about the world. This is the
single most productive check in the whole project, and not only because it catches errors —
splitting by source to remove a confound is what produced the three-surface comparison that most
of this book's surviving results depend on.</p>

<h2>The third kind: the unit of observation was wrong</h2>

<p>One of the seven, and it is the one I would most likely make again, because nothing about it
looks like an error.</p>

<p>Measuring how long models stay in the conversation, I used the model tag as the subject.
<code>qwen3.5-235b-a22b</code> is a row; <code>qwen3.6</code> is a row; <code>qwen3.8-max</code>
is a row. That is a defensible choice — those are genuinely different artifacts with different
weights — and it produced a clean result: models from Chinese labs had a median life of 85 days
against 175 for US frontier labs.</p>

<p>Collapse the version and size suffixes so those three rows become one subject, and the
cohort with the shortest lives becomes the longest-lived of any measured: 398 days against 315.
The ranking inverts, on identical data, because <em>a lab that ships more named checkpoints of
the same underlying thing looks like a lab whose models die young</em>.</p>

<p><strong>Detection:</strong> ask what one row <em>is</em>, and whether the thing you actually
care about is one row or many. If a decision would be made about the family, measure families.
The question is not statistical, and no diagnostic will raise it.</p>
"""

INT3_D = """
<h2>What all six have in common</h2>

<p><strong>Not one of them was a statistical error.</strong> Every count was correct. Every
difference was far outside anything sampling noise could produce. Every significance test would
have passed, every confidence interval would have been narrow, and every one of those numbers
would have been describing the wrong quantity.</p>

<p>All six live in the step before statistics — the one where you decide what to count, over
what population, treating what as a subject. That step has essentially no tooling. There is no
linter for it, no test that fails, and no warning in any output. It is checked by reading, or it
is not checked.</p>

<p class="pull">Every one of these errors produced a clean series with no anomalies in it. That
is what makes them dangerous: the output of a broken definition looks exactly like the output of
a good one.</p>

<h2>Why the wrong versions survived longer</h2>

<p>There is a selection effect worth naming, because it operates on published work generally and
not just on this project.</p>

<p>In every one of the seven cases, <strong>the wrong finding was more quotable than the
correction</strong>. “OpenAI's share of the conversation collapsed” is a headline; “headline
share is uninformative because the title field is increasingly a placeholder” is a footnote.
“Chinese models have half the shelf life” is a slide; “the ranking depends on whether you count
checkpoints or families” is a caveat nobody remembers. “The field fragmented fivefold” travels;
“diversity is roughly flat once you hold the source constant” does not.</p>

<p>Errors that produce a clean story are therefore selected for at every stage — they survive
review longer, they get repeated more, and they are harder to retract because more people have
built on them. Nothing about that is specific to this archive. It is a reason to be most
suspicious of your best-sounding result, which is precisely the one you least want to
re-examine.</p>

<h2>What it cost</h2>

<p>Roughly two months, seven findings, and one genuinely load-bearing claim that had already been
written up before it collapsed. Set against that, two of the three fixes produced things worth
more than what they destroyed: the source split became the comparison this book is organised
around, and the family-level grouping turned a wrong recommendation into a right one.</p>

<div class="aside">
<h4>The whole method, as a checklist</h4>
<p><strong>Read twenty rows, spread across the range, before you count anything.</strong> Not
the schema, not the aggregate — the values.<br>
<strong>Split by source and re-run.</strong> If it only exists in the pooled data, it may be
about the pooling.<br>
<strong>State what a subject is</strong> and ask whether a decision would be made about that
thing or a different one.<br>
<strong>Re-read the same twenty rows on a schedule</strong>, because all three of these failures
can arrive later in a series that started out fine.<br>
<strong>Be most suspicious of the finding you most want to publish.</strong></p>
</div>

<p>None of this is sophisticated, and none of it is new. All of it is cheaper than the two
months.</p>
"""


# ---------------------------------------------------------------- chapter 15

CH15 = """
<p class="first">Here is a question with one obviously correct answer: <em>by how much did this
field's interest in fine-tuning decline between early 2024 and the middle of 2026?</em></p>

<p>Below are six answers. They are computed from the same archive, over the same window, with
no arithmetic errors and no cherry-picking — these are simply the six most natural ways to ask
the question.</p>
"""

CH15_B = """
<p>The range is <strong>265 percentage points</strong>, and it includes a sign change. One of
these units says the subject nearly vanished. Another says it grew by more than half again.
Every one of them is defensible, and I would have trouble telling you that any is wrong.</p>

<p>Nothing statistical happened here. The spread was fixed before a single number was computed,
by decisions nobody writes down.</p>

<h2>The four decisions</h2>

<p>Every measurement over a corpus silently answers four questions. They are not statistical
questions and there is no procedure for them.</p>

<div class="aside">
<h4>What is one?</h4>
<p><strong>What is one subject?</strong> A model checkpoint, a model family, a lab, a
technique.<br>
<strong>What is one document?</strong> An issue, a section of an issue, a paragraph, a
channel-day.<br>
<strong>What counts as one observation?</strong> A string match, a tagged entity, a claim made
about the subject, a person mentioning it.<br>
<strong>What is the denominator?</strong> Words, documents, days, people, messages — or
nothing, if you report raw counts.</p>
</div>

<p>Walk the table with those four in hand and every row differs from its neighbours on exactly
one of them.</p>

<p>Rows one and five share a document (an issue) and differ on the observation: one counts every
mention, the other counts whether there was at least one. That single change moves the answer
from &minus;96% to &minus;35%, because a subject can be mentioned once in almost every issue
while its share of the text collapses.</p>

<p>Rows two, three and four share everything except the document. Narrowing from “an issue” to
“the part of the issue written about announcements” moves it to &minus;94%; narrowing to “the
part written about practitioners” moves it to &minus;64%. The two populations were doing
different things, and the whole-issue number is a blend of them weighted by how much of each the
publication happened to carry that year.</p>

<p>Row six changes the subject entirely. It stops counting words about fine-tuning and starts
counting <em>messages in the busiest community where people fine-tune models</em>. That is a
different population — participants rather than coverage — and it is the only row that measures
activity rather than attention. It is also the only row that goes up.</p>

<h2>Why more statistics cannot help</h2>

<p>This is the part I found genuinely uncomfortable, because my instinct when a result looks
shaky is to reach for a better method, and none of the available methods touch this.</p>
"""

CH15_C = """
<p>Every tool in that list operates on a quantity that has already been defined. Give any of
them a larger sample and they will describe the wrong quantity more precisely. Precision and
validity are orthogonal, and almost all the tooling — and almost all the training — is on the
precision side.</p>

<p>The significance test is the clearest case. Ask of any row in that table whether the change
could be sampling noise, and the answer is no, overwhelmingly, for all six rows
<em>simultaneously</em> — including the one that goes up while the others go down. A test that
confirms every mutually contradictory answer is not adjudicating between them. It was never
asking that question.</p>

<p class="pull">Statistics tells you how much to trust the number you computed. It has nothing
to say about whether you computed the number you meant.</p>

<h2>Write down the estimand</h2>

<p>The quantity you intend to measure has a name — the <strong>estimand</strong> — and the
useful discipline is writing it as a sentence that somebody could disagree with.</p>

<p>“Fine-tuning declined” is not an estimand. It contains no subject definition, no population,
no denominator and no window. Compare:</p>

<blockquote><p>The share of text in this newsletter's Twitter-derived recap devoted to
fine-tuning, measured as regex matches per 10,000 words of that section, fell 94% between the
first half of 2024 and the second half of 2026.</p></blockquote>

<p>That sentence is long, and it is the point. Every clause in it is a decision that could have
gone another way, and stating them makes the disagreement possible. Someone can now tell you
that the Twitter recap is the wrong population for the decision you are making, which is a
useful thing to be told and impossible to say about “fine-tuning declined”.</p>

<p>Most arguments about data are arguments about estimands, conducted as though they were
arguments about method. Two people looking at the same corpus and reaching opposite conclusions
are usually both computing correctly.</p>

<h2>Choosing the unit</h2>

<p>There is no universally right unit, which is why this cannot be automated. There is a rule
that resolves nearly every case in practice: <strong>the unit should match the population your
decision affects</strong>.</p>

<div class="tw"><table>
<caption>The same subject, three decisions, three correct units</caption>
<thead><tr><th>The decision</th><th>The population it affects</th><th>The unit to measure</th></tr></thead>
<tbody>
<tr><td>Should we publish a post about our fine-tuning work?</td><td>People who read
announcements</td><td>Density in announcement coverage</td></tr>
<tr><td>Should we keep the fine-tuning path in the product?</td><td>People who would use
it</td><td>Activity in practitioner communities</td></tr>
<tr><td>Should we hire someone to maintain the tuning pipeline?</td><td>Our own
engineers</td><td>Neither — internal usage of the pipeline</td></tr>
</tbody></table></div>

<p>The third row matters as much as the other two. Sometimes the right answer is that the corpus
in front of you does not contain the population you care about, and the correct move is to stop
measuring it rather than to measure it more carefully.</p>

<h2>The sentence to write before the query</h2>

<p>The whole of this chapter compresses into one fill-in-the-blank, and it takes about thirty
seconds:</p>

<div class="aside">
<h4>Before you compute anything</h4>
<p><strong>One row is ______, drawn from ______, and I am counting ______ per ______, over the
window ______, in order to decide ______.</strong></p>
<p>If any blank is hard to fill, the number does not mean anything yet. If the last blank is
empty, you are measuring for the pleasure of it, which is allowed but should be admitted. And
if two people fill the blanks differently, they will get different answers and neither will be
wrong — that is the moment to argue about the sentence rather than about the result.</p>
</div>

<p>None of this is hard. It is just early, and everything that makes analysis feel rigorous —
the tests, the intervals, the diagnostics, the plots — happens later, which makes it very easy
to do all of it beautifully to a quantity nobody meant to measure.</p>
"""


# ---------------------------------------------------------------- chapter 16

CH16 = """
<p class="first">The last issue in this archive is dated 6 August 2026. In the archive its title
is <em>not much happened today</em> and the human-written line underneath it is three words
long — <em>a quiet day.</em> Neither is what was published. The issue went out under a
headline and a subtitle of its own:</p>

<blockquote><p><strong>AMD buys Taalas</strong><br>
<em>The Inference Inflection is HEATING up.</em></p>
<cite>AI News, 2026-08-06 — the final issue, as sent</cite></blockquote>

<p>Underneath that, the editor was not being quiet at all. He was collecting on a call he had
made twice:</p>

<blockquote><p>In <em>The Custom ASIC Thesis</em> we said Taalas was worth paying attention to,
and in <em>the Inference Inflection</em> we said everything would go vertical. Our Baseten
episode had some skeptical counterpoints against etched LLMs, not just custom ASICs, but
clearly Lisa Su disagrees for now.</p>
<cite>AI News lede, 2026-08-06</cite></blockquote>

<p>And here is part of what the machine summary further down the same issue describes — a third
account of the same day, which agrees with neither of the first two:</p>

<blockquote><p>Meta's Muse Spark 1.2 rapidly rose to frontier-tier with top 5 ranking on Vals
Index at <strong>$0.69/test</strong>, being 3× cheaper than Kimi and 10×+ cheaper than Fable,
Opus, and 5.6 Sol. It achieved <strong>gold-medal-level performance in five STEM
Olympiads</strong> with perfect theory scores in APhO and IPhO.</p>
<cite>AI News, 2026-08-06</cite></blockquote>

<p>So the final day of this corpus has three accounts of itself: an archive that says nothing
happened, an editor who says the inference market just turned, and a summary that says a model
won five Olympiad golds. All three are true, in different senses, and they are ordered by
distance from the day — the further from it you stand, the flatter it looks. The one that got
stored, indexed and handed to me was the flattest. The only way to find out was to read past
it, and that is the whole problem, still present on the archive's last day.</p>

<p>This chapter is what to do about it, stated so it works on any technical field and takes
about an hour a month.</p>

<h2>Find your three surfaces</h2>

<p>Every technical field has at least three layers, kept separate by who is talking and what
they are rewarded for.</p>

<div class="tw"><table>
<caption>The same three layers, in four fields</caption>
<thead><tr><th>Field</th><th>Announcement</th><th>Community</th><th>Practice</th></tr></thead>
<tbody>
<tr><td>AI</td><td>lab accounts, launch posts</td><td>tooling Discords</td><td>local-inference
forums</td></tr>
<tr><td>Databases</td><td>vendor blogs, conference keynotes</td><td>project mailing
lists</td><td>ops postmortems, incident writeups</td></tr>
<tr><td>Frontend</td><td>framework release notes</td><td>maintainer
discussions</td><td>bug trackers, migration threads</td></tr>
<tr><td>Security</td><td>vendor advisories</td><td>research
Slacks</td><td>incident-response writeups</td></tr>
</tbody></table></div>

<p>The announcement layer has a launch schedule and is rewarded for novelty; its volume tracks
how much capital is chasing a category. The practice layer has a constraint — a hardware budget,
an uptime target, a compliance boundary — and is rewarded for things that work under it. Neither
is the truth. They are two populations with different incentives, and the useful information is
in the difference between them.</p>

<p>You do not need three. <strong>Two you can read weekly beats one you read thoroughly</strong>,
and the practice layer is the one people skip.</p>

<h2>Measure the same claim in both</h2>

<p>Pick a specific claim — not a topic. “Everyone is moving to X” is a claim. Then look for it in
both surfaces over the same window, and compare how much it moved in each.</p>
"""

CH16_B = """
<p>That table is the entire method, and its value is in the second and third rows rather than
the first. Spotting hype is easy and mostly useless — you were probably already suspicious.
Spotting the thing practitioners have adopted while the coverage lags is where the decision
changes, and it is invisible if you read only one layer.</p>

<p>In this archive the clearest instance ran for about a year: a category of open-weights models
was rising fastest among people running them on their own hardware, more slowly in the
communities building tooling, and slowest in the announcement layer. Anyone comparing the two
outer surfaces would have seen it a year before the coverage settled.</p>

<h2>Check the machinery, not the name</h2>

<p>Names rise and fall for reasons that have little to do with the technology underneath. A term
can vanish because the idea failed, or because it won so completely that naming it became
unnecessary — and those look identical in any count of the term.</p>

<p>The fix is to count the <em>mechanism</em> alongside the name: the vocabulary the thing needs
in order to work at all. In this corpus, one technique's own name fell a hundredfold while the
words for its machinery — the specific operations it requires — fell less than twofold, which
settles what happened without needing anyone's opinion. A different technique's name fell to
zero and its machinery vocabulary went to zero with it. Same-shaped line, opposite conclusion.</p>

<p>Run it forwards too. A name rising faster than its machinery is a term being marketed. A name
rising more slowly than its machinery is real engineering that has not found its label yet.</p>

<h2>Know what your surfaces cannot see</h2>

<p>The practice layer is an excellent check on anything a person can run and <strong>no check at
all</strong> on anything requiring a data centre, a licence, or a fleet. When it is quiet about
something expensive, that silence carries no information — and reading it as scepticism is the
most likely way to misuse everything above.</p>

<p>The same applies to the other direction. The announcement layer genuinely leads on things
that take enormous capital to build. It is not lying about those; it simply gets there
first.</p>
"""

CH16_C = """
<h2>Five checks on your own measurement</h2>

<p>Every one of these cost me a published finding, and each takes minutes.</p>

<div class="aside">
<h4>Before you trust your own series</h4>
<p><strong>Read twenty rows, spread across the range.</strong> Not the schema, not the
aggregate. Fields stop meaning what they meant, and nothing else catches it.<br>
<strong>Split by source and re-run.</strong> If the finding exists only in the pooled data, it
may be a fact about the pooling.<br>
<strong>State what one row is</strong>, and check that a decision would be made about that thing
rather than a coarser or finer one.<br>
<strong>Check your denominator has not changed shape.</strong> A document whose composition
drifts turns every rate into a weighted average with moving weights.<br>
<strong>Be most suspicious of your best-sounding result.</strong> Clean stories survive review
longer than their corrections do, so the finding you most want to publish is the one that has
been least tested by wanting it to be false.</p>
</div>

<h2>What thirty-two months of this actually contained</h2>

<p>Compressed as far as it will go, and with the caveat that all of it measures attention within
one curated view rather than deployment or revenue:</p>

<ul>
<li><strong>The job kept moving outward from the model.</strong> In early 2024 the central
activity was adapting weights — fine-tuning language ran at 25.6 mentions per ten thousand words
of announcement text. By the end it was 1.9, while the vocabulary for the software
<em>around</em> the model rose eighteen- to twenty-threefold and evaluation language roughly
doubled to become the densest technical term in the corpus.</li>
<li><strong>The frontier of open weights changed continents, and not to a company.</strong> Two
Western labs fell from 42.3 to 1.3 in announcement space; a bloc of five Chinese labs rose, with
no individual member holding the lead for more than two half-years.</li>
<li><strong>Scoreboards last about three quarters.</strong> Every fixed-answer benchmark that
defined 2024 reaches literal zero. The ones still standing ask a model to complete a task and
have a program check the result.</li>
<li><strong>The safety conversation changed species rather than growing.</strong> Alignment
language fell from 7.19 to 1.28; permission, sandboxing and least-privilege language rose
tenfold in announcement space and nineteenfold among practitioners.</li>
</ul>

<h2>Monday</h2>

<p>Concretely, for one technology you care about:</p>

<ol>
<li><strong>Twenty minutes, once.</strong> Name your announcement surface and your practice
surface. Write the estimand sentence: <em>one observation is ___, drawn from ___, counted per
___, in order to decide ___.</em></li>
<li><strong>Fifteen minutes a week.</strong> Read both surfaces. Not exhaustively — the top of
each.</li>
<li><strong>An hour a quarter.</strong> Count your claim in each surface over the quarter.
Compare the two numbers, not either one alone. Read twenty raw matches while you are there.</li>
<li><strong>When they disagree, act on the gap</strong> rather than on either number: shrinking
toward practice means wait, growing toward practice means move, moving together means it is
real.</li>
</ol>

<p>That is roughly an hour a month, and it would have given you the agent narrative, the
open-weights relocation, and the benchmark churn well before any of them were settled.</p>

<h2>Forwards</h2>

<p>Everything written about a fast-moving field afterwards is organised around what turned out
to matter, which makes it excellent history and nearly useless for the decision in front of you.
The value of a daily record is that it is <em>wrong in public</em>, with dates: the enthusiasms
that went nowhere sit next to the ones that changed everything, at the same volume, with nothing
marking which is which.</p>

<p>Reading forwards means accepting that this is also true of today. The correct call and the
expensive mistake are both in your feed this morning, indistinguishable, and no amount of
retrospective clarity will be available in time to help. What is available is the gap between
what is being announced and what is being run — and that gap, unlike the future, you can measure
this afternoon.</p>

<p class="pull">A quiet day, with an inference inflection and five Olympiad golds underneath it.
You only find out by reading.</p>
"""


# ---------------------------------------------------------------- pages

def pages():
    """Return [(slug, kind, num, title, question, body_html)] in reading order."""
    ch1 = (CH1
           + fig(F.cadence(D.CADENCE), 1, "The shape of the archive",
                 "Issues per quarter (bars, left axis) and median issue length in words "
                 "(line, right axis). Cadence is near-constant; length is not. The collapse "
                 "in 2026Q2 is the Discord recap being dropped.")
           + CH1_B)

    tw, rd = D.TWITTER, D.REDDIT
    ch2 = (CH2
           + fig(C.lines(D.P6,
                         [("agentic (announcement)", tw["agentic"], "sig"),
                          ("agentic (practice)", rd["agentic"], "bench")],
                         [0, 40, 80, 120], "mentions / 10⁴ words"),
                 2, "One idea, two surfaces",
                 "Mentions of agents per 10⁴ words, measured inside the Twitter recap and "
                 "the Reddit recap. Same days, same corpus, same regular expression.")
           + CH2_B
           + fig(F.surfaces([("agents", 5.5, 3.0, 1.2, "sig"),
                             ("reasoning", 1.2, 2.1, 1.4, "bench"),
                             ("China bloc", 4.6, 9.9, 9.0, "bench"),
                             ("quantization", 0.8, 0.5, 1.1, "bench"),
                             ("fine-tuning", 0.1, 0.3, 0.3, "bench"),
                             ("RAG", 0.1, 0.2, 0.1, "ink")]),
                 3, "The hype gradient",
                 "Fold change from 2024H1 to 2026H1 within each surface, log scale. Colour "
                 "encodes the verdict: red shrinks toward practitioners (narrative), teal "
                 "grows toward them (under-covered), black is flat (real). Community space "
                 "is the Discord recap, which ends March 2026 — hence 2026H1 rather than "
                 "2026H2 throughout.")
           + CH2_C)

    ch3 = (CH3 + CH3_B
           + fig(C.lines(D.P6,
                         [("fine-tuning", tw["fine-tuning"], "sig"),
                          ("RAG", tw["RAG"], "ink2"),
                          ("agentic", tw["agentic"], "bench")],
                         [0, 40, 80, 120], "mentions / 10⁴ words", gutter=92),
                 4, "The handover, in announcement space",
                 "Mentions per 10⁴ words inside the Twitter recap. Fine-tuning and RAG "
                 "own the beginning of the corpus; agents own the end. All three lines "
                 "are measured the same way in the same section.")
           + CH3_C)

    fate_rows = [[C.esc(n), f"{a:.2f} → {b:.2f}", f"{c:.2f} → {d:.2f}",
                  f"<b>{C.esc(v)}</b>"] for n, a, b, c, d, v in D.FATES]
    ch4 = (CH4
           + fig(C.lines(D.P6,
                         [("state-space", D.FATES_TW["state-space"], "sig"),
                          ("1-bit / ternary", D.FATES_TW["1-bit"], "bench"),
                          ("model merging", D.FATES_TW["model merging"], "ink2"),
                          ("world models", D.FATES_TW["world model"], "ink")],
                         [0, 4, 8, 12], "mentions / 10⁴ words", gutter=112),
                 5, "Four ideas, announcement space",
                 "Mentions per 10⁴ words inside the Twitter recap. Three of these lines end "
                 "at or near zero and one is climbing — but the shape of a line says nothing "
                 "about which fate produced it.")
           + CH4_B + CH4_C
           + fig(C.lines(D.P6,
                         [("1-bit (announcement)", D.FATES_TW["1-bit"], "sig"),
                          ("1-bit (practice)", D.FATES_RD["1-bit"], "bench")],
                         [0, 2, 4, 6], "mentions / 10⁴ words"),
                 6, "An idea returning from below",
                 "The same pattern in the Twitter and Reddit recaps. Announcement space "
                 "peaks in 2024 and effectively stops; practice space reaches its corpus "
                 "high two years later, on hardware that did not exist for it in 2024.")
           + CH4_D
           + table(["Idea", "Announcement", "Practice", "Fate"], fate_rows,
                   "Table 1 · Mentions per 10⁴ words, 2024H1 → 2026H2, in each surface",
                   (1, 2))
           + CH4_E)

    legacy_rows = [[C.esc(n), f"{a:.2f} → {b:.2f}", f"{c:.2f} → {d:.2f}",
                    f"<b>{C.esc(v)}</b>"] for n, a, b, c, d, v in D.LEGACY]
    ch5 = (CH5 + CH5_B
           + fig(C.lines(D.REASON_M_P,
                         [("o1 / o3", D.REASON_M["o1 / o3"], "sig"),
                          ("reasoning", D.REASON_M["reasoning"], "bench"),
                          ("test-time compute", D.REASON_M["test-time compute"], "ink")],
                         [0, 10, 20, 30], "mentions / 10⁴ words", gutter=126),
                 7, "Four months, month by month",
                 "Measured inside the Discord recap, the largest surface in this window at "
                 "roughly half a million words a month. o1 ships on 12 September 2024, o3 "
                 "on 20 December. The vocabulary moves after the products, not with them.")
           + CH5_C
           + fig(C.lines(D.P6,
                         [("reasoning as a knob", D.LEGACY_TW["reasoning as a knob"], "sig"),
                          ("distillation", D.LEGACY_TW["distillation"], "bench"),
                          ("verifiable rewards", D.LEGACY_TW["verifiable rewards"], "ink"),
                          ("RLHF / DPO / PPO", D.LEGACY_TW["RLHF / DPO / PPO"], "ink2")],
                         [0, 4, 8, 12], "mentions / 10⁴ words", gutter=140),
                 8, "What the reasoning turn left behind",
                 "Announcement space. Two vocabularies that did not exist in early 2024, one "
                 "that did and was displaced, and one — distillation — that was old and came "
                 "back bigger. The word “reasoning” is off this chart at 37.7.")
           + CH5_D
           + table(["What", "Announcement", "Practice", "Outcome"], legacy_rows,
                   "Table 2 · Mentions per 10⁴ words, 2024H1 → 2026H2, in each surface",
                   (1, 2))
           + CH5_E)

    bloc_rows = [[C.esc(s), C.esc(w), f"{a}", f"{b}", f"{c}",
                  ("<b>holds</b>" if "bloc" in w else "reverts")]
                 for s, w, a, b, c in D.BLOC_Q]
    ch6 = (CH6
           + fig(F.timeline([d for d, _ in D.R1_DAILY],
                            [("DeepSeek / R1", [v for _, v in D.R1_DAILY], "sig")],
                            [0, 50, 100, 150, 200], "mentions / 10⁴ words",
                            every=3, events=D.R1_EVENTS),
                 9, "One week, by the day",
                 "Mentions of DeepSeek or R1 per 10⁴ words inside the Discord recap, by the "
                 "day each issue covers, 6 January to 19 February 2025. Gaps are weekends.")
           + CH6_B
           + fig(F.timeline(D.BLOC_M_P,
                            [("China bloc", D.BLOC_M["China bloc"], "bench"),
                             ("DeepSeek", D.BLOC_M["DeepSeek"], "sig")],
                            [0, 20, 40, 60], "mentions / 10⁴ words",
                            every=3, gutter=92),
                 10, "The step and the spike",
                 "Community space, monthly. The company reverts below its pre-R1 level; the "
                 "category it belongs to does not. Coverage ends March 2026 with the Discord "
                 "recap.")
           + CH6_C
           + table(["Surface", "What", "Before R1", "Peak", "Latest", "Outcome"], bloc_rows,
                   "Table 3 · Mentions per 10⁴ words, 2024Q4 → 2025Q1 → latest quarter",
                   (2, 3, 4))
           + CH6_D)

    ch7 = (CH7
           + fig(C.paired(D.STACK_GAP),
                 11, "The software around the model",
                 "Fold change from 2024H1 to 2026H2, log scale. Red is announcement space, "
                 "teal is practice. Five terms describing the layer outside the model, and "
                 "one — prompt engineering — describing the craft it replaced. Orchestration "
                 "is measured from 2024H2, its practice baseline being zero.")
           + CH7_B + CH7_C
           + fig(F.timeline(D.MCP_M_P, [("MCP", D.MCP_M, "bench")], [0, 10, 20, 30, 40],
                            "mentions / 10⁴ words", every=3, events=D.MCP_EVENTS),
                 12, "A protocol's adoption curve",
                 "Community space, monthly. The launch barely registers; the peak arrives four "
                 "months later, in the month a competitor implemented the spec.")
           + CH7_D
           + fig(C.lines(D.P6,
                         [("evals (announcement)", D.STACK_TW["evals"], "sig"),
                          ("evals (practice)", D.STACK_RD["evals"], "bench"),
                          ("harness (announcement)", D.STACK_TW["harness"], "ink")],
                         [0, 20, 40, 60], "mentions / 10⁴ words", gutter=160),
                 13, "The largest line in the chapter",
                 "Evaluation language roughly doubles in both durable surfaces and ends the "
                 "corpus at twice the density of anything else measured here.")
           + CH7_E)

    m3 = [[C.esc(q), a, b, c, d] for q, a, b, c, d in D.MISTRAL_THREE]
    ch8 = (CH8
           + fig(C.lines(D.P6,
                         [("Meta / Llama", D.LABS_TW["Meta / Llama"], "sig"),
                          ("Mistral", D.LABS_TW["Mistral"], "ink2"),
                          ("Meta / Llama (practice)", D.LABS_RD["Meta / Llama"], "bench")],
                         [0, 20, 40, 60], "mentions / 10⁴ words", gutter=168),
                 14, "Two shapes of losing",
                 "Meta rises to a peak and breaks; Mistral erodes with no event at all. The "
                 "practice-space line for Meta starts at 55.6, the highest any single lab "
                 "reaches among practitioners anywhere in the corpus.")
           + CH8_B
           + fig(C.lines(D.P6,
                         [("Kimi / Moonshot", D.LABS_TW["Kimi / Moonshot"], "sig"),
                          ("DeepSeek", D.LABS_TW["DeepSeek"], "bench"),
                          ("GLM / Zhipu", D.LABS_TW["GLM / Zhipu"], "ink"),
                          ("Qwen", D.LABS_TW["Qwen"], "ink2")],
                         [0, 10, 20, 30, 40], "mentions / 10⁴ words", gutter=126),
                 15, "The relay",
                 "Announcement space, the Chinese open-weights bloc by lab. MiniMax is omitted "
                 "for legibility; it rises from zero to 6.8 on the same shape as GLM. No lab "
                 "holds the top position for more than two half-years.")
           + CH8_C
           + table(["How you ask", "2023", "2024", "2025", "2026"], m3,
                   "Table 4 · Is Mistral still there? Three measurements, by year. The density row averages the two half-year values.",
                   (1, 2, 3, 4))
           + CH8_D)

    ch9 = (CH9
           + fig(C.lines(D.P6,
                         [("agent permissions", D.SEC_TW["agent permissions"], "bench"),
                          ("regulation", D.SEC_TW["regulation"], "ink2"),
                          ("alignment", D.SEC_TW["alignment"], "sig"),
                          ("CVE / exploit", D.SEC_TW["CVE / exploit"], "ink")],
                         [0, 5, 10, 15], "mentions / 10⁴ words", gutter=126),
                 16, "Two vocabularies crossing",
                 "Announcement space. The philosophical and regulatory language of 2024 falls; "
                 "the operational language of 2026 rises. Regulation's spike is the SB-1047 and "
                 "EU AI Act window, and it reverts completely.")
           + CH9_B
           + fig(C.paired(D.SEC_GAP),
                 17, "Which way each term moved, in both surfaces",
                 "Fold change 2024H1 to 2026H2, log scale. Red is announcement space, teal is "
                 "practice. Permission language rises in both and hardest among practitioners; "
                 "alignment falls in both.")
           + CH9_C + CH9_D)

    mix_rows = [[C.esc(n), a, b, c, d] for n, a, b, c, d in D.MIXTURE]
    int2 = (INT2
            + fig(C.stacked(D.P6,
                            [("Discord recap", D.COMPOSITION["Discord"], "disc"),
                             ("Reddit recap", D.COMPOSITION["Reddit"], "redd"),
                             ("Twitter recap", D.COMPOSITION["Twitter"], "twit")],
                            [0, 25, 50, 75, 100], "% of issue words"),
                  18, "The document turned inside out",
                  "Median share of an issue's words by source section. The Discord recap is "
                  "96% of the median issue in early 2024 and absent from the median issue in "
                  "2026 — 80 of 126 issues in 2026H1 have no Discord section, and none of the "
                  "final 26 do.")
            + INT2_B
            + table(["Pattern", "Whole issue", "Announcement", "Practice", "Community"],
                    mix_rows,
                    "Table 5 · Change from 2024H1 to the end of each surface's coverage",
                    (1, 2, 3, 4))
            + INT2_C)

    nm_rows = [[C.esc(n), f"{a:.2f} → {b:.2f}", f"{c:.2f} → {d:.2f}",
                f"<b>{C.esc(v)}</b>"] for n, a, b, c, d, v in D.NAME_MACH]
    ch10 = (CH10
            + fig(C.lines(D.P6,
                          [("RAG (the name)", D.NAME_MACH_TW["RAG (the name)"], "sig"),
                           ("retrieval machinery", D.NAME_MACH_TW["retrieval machinery"], "bench"),
                           ("memory", D.NAME_MACH_TW["memory"], "ink")],
                          [0, 10, 20], "mentions / 10⁴ words", gutter=134),
                  19, "The name died; the machinery did not",
                  "Announcement space. RAG's own name falls 107-fold. The vocabulary of the "
                  "mechanism it needs — retrieval, chunking, reranking, vector indexes, "
                  "embeddings — falls 1.9-fold, and memory language rises.")
            + CH10_B
            + table(["Idea", "The name", "The machinery", "Verdict"], nm_rows,
                    "Table 6 · Announcement space, 2024H1 → 2026H2, mentions per 10⁴ words",
                    (1, 2))
            + CH10_C + CH10_D)

    life_rows = [[C.esc(n), C.esc(w),
                  (f"{pk} → {fell}" if fell != "—" else f"{pk} → still rising"),
                  (f"<b>{q}</b>" if q != "still rising" else "<b>—</b>")]
                 for n, w, f, pk, fell, q in D.BENCH_LIFE]
    ch11 = (CH11
            + table(["Benchmark", "What it asks", "Peak → below 25% of peak", "Quarters"],
                    life_rows,
                    "Table 7 · Lifespan in announcement space, measured by quarter", (3,))
            + CH11_B
            + fig(C.lines(D.P6,
                          [("LMSYS Arena", D.BENCH_TW["LMSYS Arena"], "sig"),
                           ("SWE-bench", D.BENCH_TW["SWE-bench"], "bench"),
                           ("Terminal-Bench", D.BENCH_TW["Terminal-Bench"], "ink"),
                           ("MMLU", D.BENCH_TW["MMLU"], "ink2")],
                          [0, 4, 8, 12], "mentions / 10⁴ words", gutter=120),
                  20, "Four scoreboards",
                  "Announcement space. One quiz benchmark, one preference ranking, and two "
                  "task suites. The preference ranking rises highest and falls furthest; the "
                  "task suites are the only lines still climbing at the end.")
            + CH11_C
            + fig(C.lines(D.P6,
                          [("contamination", D.BENCH_TW["contamination"], "sig"),
                           ("LLM-as-judge", D.BENCH_TW["LLM-as-judge"], "bench")],
                          [0, 2, 4], "mentions / 10⁴ words", gutter=112),
                  21, "What replaced the certainty",
                  "Announcement space. Worry about contaminated test sets peaks at the end of "
                  "the corpus, alongside the cheapest available substitute for a benchmark: "
                  "asking a model to grade the output.")
            + CH11_D + CH11_E)

    drift_rows = [[f"<code>{C.esc(w)}</code>",
                   f"<b>{d:.3f}</b>" if d > 0.35 else f"{d:.3f}",
                   C.esc(a), C.esc(b)] for w, d, a, b, _ in D.DRIFT]
    ch12 = (CH12
            + table(["Term", "Drift", "Nearest neighbours, 2024",
                     "Nearest neighbours, 2026"], drift_rows,
                    "Table 8 · Cosine distance between a term's 2024 and 2026 neighbourhoods. "
                    "Median across the corpus: 0.313", (1,))
            + CH12_B + CH12_C + CH12_D)

    kind_rows = [[C.esc(k), f"{n:,}", f"{pct}%"] for k, n, pct in D.DISCORD_KIND]
    srv_rows = [[C.esc(s), f"{n:,}", f"{f} → {l}", f"{m}", f"<b>{r:,}</b>"]
                for s, n, f, l, m, r in D.DISCORD_SERVERS]
    ch13 = (CH13
            + table(["Channel kind", "Messages", "Share"], kind_rows,
                    "Table 9 · All 2,142,082 messages, by the kind of channel they were in",
                    (1, 2))
            + CH13_B + CH13_C
            + table(["Server", "Messages", "Active", "Months", "Per month"], srv_rows,
                    "Table 10 · The busiest communities in the sampled window", (1, 3, 4))
            + CH13_D
            + fig(F.timeline(D.DISCORD_SAMPLE_P,
                             [("servers sampled", D.DISCORD_SAMPLE, "sig")],
                             [0, 10, 20, 30], "servers in the sample", every=2, gutter=112),
                  22, "The frame shrinks by a quarter",
                  "Distinct Discord servers appearing in the recap, by month. The drop from "
                  "about 30 to 23 in September 2025 is an editorial decision, and it makes "
                  "several communities look as though they stopped existing in August.")
            + CH13_E)

    hz_rows = [[C.esc(l), f"{a}%", f"<b>{b}%</b>"] for l, a, b in D.KM_HORIZON]
    coh_rows = [[C.esc(c), f"{nt}", f"{mt} d", f"{nf}", f"<b>{mf} d</b>"]
                for c, nt, mt, nf, mf in D.KM_COHORT]
    why_rows = [[C.esc(c), g, age, obs] for c, g, age, obs in D.KM_WHY]
    ch14 = (CH14
            + fig(F.survival(D.KM_DAYS,
                             [("all families", D.KM["fams_all"], "bench"),
                              ("all model tags", D.KM["tags_all"], "sig")],
                             marks=[(137, "137 d"), (254, "254 d")]),
                  23, "How long a model stays in the conversation",
                  "Kaplan-Meier curves over 255 model tags and the 140 families they collapse "
                  "into. Death is 90 days of silence before the archive ends; anything "
                  "mentioned more recently is treated as alive and censored.")
            + CH14_B
            + table(["If you build on it today", "Still discussed — checkpoint",
                     "— family"], hz_rows,
                    "Table 11 · Probability a model is still being discussed after…", (1, 2))
            + CH14_C
            + table(["Cohort", "Tags", "Median", "Families", "Median"], coh_rows,
                    "Table 12 · Median survival at tag level and at family level",
                    (1, 2, 3, 4))
            + CH14_D
            + fig(F.survival(D.KM_DAYS,
                             [("Chinese families", D.KM["fams_cn"], "bench"),
                              ("Chinese model tags", D.KM["tags_cn"], "sig")],
                             marks=[(85, "85 d"), (398, "398 d")]),
                  24, "The same models, counted two ways",
                  "The lower curve counts each named checkpoint as a separate subject; the "
                  "upper one collapses version and size suffixes into families. The long flat "
                  "stretches in the lower curve are periods with too few subjects old enough "
                  "to produce an event.")
            + CH14_E
            + table(["Cohort", "Tags per family", "Median first appearance",
                     "Median observed span"], why_rows,
                    "Table 13 · The two mechanisms behind the reversal", (1,))
            + CH14_F)

    led_rows = [[pub, was, C.esc(D.LEDGER_KIND[kind])] for pub, was, kind in D.LEDGER]
    int3 = (INT3
            + table(["What I published", "What was true", "Root cause"], led_rows,
                    "Table 14 · Every finding withdrawn or reversed, and why")
            + INT3_B
            + fig(F.timeline([y for y, _ in D.TEMPLATED],
                             [("stored titles", [v for _, v in D.TEMPLATED], "sig")],
                             [0, 25, 50, 75], "% of issues", every=1, gutter=126,
                             events=D.TEMPLATED_EVENT),
                  25, "A placeholder that was never published",
                  "Share of issues whose stored title is a template — “not much happened "
                  "today”, “a quiet weekend” — rather than a description of the day. The rise "
                  "is real and the explanation is not: on the 133 issues recoverable from the "
                  f"sent emails, only <b>{D.TEMPLATED_PUBLISHED}%</b> went out under a "
                  "templated subject. The series measures the mirror, not the newsletter.")
            + INT3_C + INT3_D)

    unit_rows = [[C.esc(u), f"<i>{C.esc(row)}</i>", a, b, f"<b>{chg}</b>"]
                 for u, row, a, b, chg in D.UNIT_ANSWERS]
    ch15 = (CH15
            + table(["How you ask", "One row is", "2024H1", "2026H2", "Change"], unit_rows,
                    "Table 15 · Six answers to “how much did fine-tuning decline?”, from one "
                    "corpus", (2, 3, 4))
            + CH15_B
            + table(["Tool", "What it protects you from", "What it says about the unit"],
                    [["Larger sample", "Sampling noise", "Nothing"],
                     ["Confidence interval", "Overstating precision", "Nothing"],
                     ["Significance test", "Reading noise as signal", "Nothing"],
                     ["Multiple-comparison correction", "Fishing across many tests", "Nothing"],
                     ["Censoring-aware estimator", "Unfinished observations", "Nothing"],
                     ["Change-point detection", "Missing a break in a series",
                      "Nothing — it finds breaks <i>within</i> a unit"]],
                    "Table 16 · What the statistical toolkit is for")
            + CH15_C)

    ch16 = (CH16
            + table(["What you see", "What it suggests", "What to do next"],
                    [["The claim moved a lot in announcement space and little in practice",
                      "The launch layer is ahead of the practitioner layer.",
                      "<b>Discount and investigate.</b> Re-check in a quarter."],
                     ["It moved more in practice than in announcement",
                      "Practitioners are discussing something the coverage has not reached.",
                      "<b>Investigate early.</b> This is where the cheap leads are."],
                     ["It moved about the same in both",
                      "Plausibly a field-wide shift.",
                      "<b>Treat as a field-wide signal and triangulate</b> "
                      "against non-discourse evidence."],
                     ["It fell in both",
                      "Either it died or it won so completely that nobody names it.",
                      "<b>Check the machinery</b> before removing anything."],
                     ["Practice space is silent and the thing needs a data centre",
                      "Your check does not apply here.",
                      "<b>Discount the silence.</b> Find another surface."]],
                    "Table 17 · The two-surface test, as a decision table")
            + CH16_B + CH16_C)

    return [
        ("ch1", "ch", "1", "A field talking to itself",
         "What is this thing, and why would anyone read three years of a newsletter?", ch1),
        ("ch2", "ch", "2", "Three surfaces",
         "Why does everything in this field feel like hype?", ch2),
        ("interlude-1", "inter", "I", "The day I measured the newsletter instead of the field",
         "On checking what the field you are counting actually contains.", INT1),
        ("ch3", "ch", "3", "Everyone is fine-tuning",
         "What did the field think the job was?", ch3),
        ("ch4", "ch", "4", "The road not taken",
         "What does it look like when a good idea simply does not arrive?", ch4),
        ("ch5", "ch", "5", "Learning to think",
         "How does a whole field change its mind in four months?", ch5),
        ("ch6", "ch", "6", "Seven days in January",
         "What does it look like when something actually breaks through?", ch6),
        ("ch7", "ch", "7", "The harness",
         "When did the field stop talking about models and start talking about the "
         "software around them?", ch7),
        ("ch8", "ch", "8", "The handover",
         "How does a technological lead change hands?", ch8),
        ("ch9", "ch", "9", "Containment",
         "What happens after the capability race?", ch9),
        ("interlude-2", "inter", "II", "The day the corpus changed shape underneath me",
         "On measuring a document whose composition inverted.", int2),
        ("ch10", "ch", "10", "How ideas die",
         "Retrieval fell 99%. So did things that failed. How do you tell?", ch10),
        ("ch11", "ch", "11", "How the field keeps score",
         "Which benchmarks are worth believing, and for how long?", ch11),
        ("ch12", "ch", "12", "When words change meaning",
         "Is <code>agent</code> in your 2026 dashboard the same <code>agent</code> "
         "you started counting in 2024?", ch12),
        ("ch13", "ch", "13", "Where practitioners spent their attention",
         "If announcements are unreliable, what were the other rooms talking about?", ch13),
        ("ch14", "ch", "14", "The half-life of a dependency",
         "You are about to build on a model. How long will it stay relevant?", ch14),
        ("interlude-3", "inter", "III", "The six things I got wrong",
         "Consolidated, with what each one cost.", int3),
        ("ch15", "ch", "15", "The unit of observation",
         "Why did none of this get caught by better statistics?", ch15),
        ("ch16", "ch", "16", "How to read a field",
         "What do you do on Monday?", ch16),
    ]
