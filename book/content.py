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
     "How does a whole field change its mind in four months?", None),
    ("ch", "6", "Seven days in January",
     "What does it look like when something actually breaks through?", None),
    ("ch", "7", "The harness",
     "When did the field stop talking about models and start talking about the "
     "software around them?", None),
    ("ch", "8", "The handover",
     "How does a technological lead change hands?", None),
    ("ch", "9", "Containment",
     "What happens after the capability race?", None),
    ("inter", "II", "The day the corpus changed shape underneath me",
     "On measuring a document whose composition inverted.", None),

    ("part", "Part III — What it means"),
    ("ch", "10", "How ideas die",
     "Retrieval fell 99%. So did things that failed. How do you tell?", None),
    ("ch", "11", "How the field keeps score",
     "Which benchmarks are worth believing, and for how long?", None),
    ("ch", "12", "When words change meaning",
     "Is <code>agent</code> in your 2026 dashboard the same <code>agent</code> "
     "you started counting in 2024?", None),
    ("ch", "13", "What people actually ran",
     "If announcements are unreliable, what does the ground truth look like?", None),
    ("ch", "14", "The half-life of a dependency",
     "You are about to build on a model. How long will it stay relevant?", None),
    ("inter", "III", "The four things I got wrong",
     "Consolidated, with what each one cost.", None),

    ("part", "Part IV — Reading forwards"),
    ("ch", "15", "The unit of observation",
     "Why did none of this get caught by better statistics?", None),
    ("ch", "16", "How to read a field",
     "What do you do on Monday?", None),
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
built from a declared list of accounts, a Reddit recap from a declared list of subreddits,
and — until March 2026 — a Discord recap assembled from message logs across dozens of
servers. The sampling frame is stated in the issue itself, which turns out to matter
enormously later. The summaries are model-generated; the framing, the headline, the lede
and the editorial judgement are human. You can watch the seams: the top-of-issue commentary
argues with the summaries underneath it.</p>
"""

CH1_B = """
<p>It is not a steady artifact, and the shape of the unsteadiness is the first thing worth
knowing about it. Issue length nearly quadrupled in the first six months as the Discord
sampling widened, held around 25,000 words for two years, and then <strong>collapsed by a
factor of five in the second quarter of 2026</strong>, when the newsletter dropped the
Discord recap entirely. The cadence barely moved through all of it — roughly 65 issues a
quarter, start to finish.</p>

<p>Hold on to that collapse. Nearly everything that went wrong in the analysis behind this
book traces back to it, and the fix for it produced the book's central idea.</p>

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
its text to fine-tuning — and in chapter 13 you will see that during exactly that window,
the single busiest community in the archive was a fine-tuning toolchain with 302,248
messages. Both facts are true. Neither is “fine-tuning declined.”</p>
</div>

<p>There are three further limits worth stating plainly. The archive is one editor's view,
with one editor's taste; it over-weights the English-language, US-and-China, open-weights-adjacent
conversation and largely misses enterprise procurement, academic publishing outside the
poster-on-Twitter tier, and everything happening in Chinese-language forums. Its sampling
frame widened over time — 7 subreddits to 12, 384 Twitter accounts to 544 — which means any
count of <em>distinct things mentioned</em> is partly counting the newsletter's own appetite.
And it stops. Discord coverage ends in March 2026; the copy of the archive behind this book
ends in August 2026. Anything that looks like a decline after those dates is the instrument.</p>

<p>What is left, after all of that, is still remarkable: a dated, daily, self-describing
record of what one fast-moving technical field paid attention to, across nearly a thousand
consecutive days, written by people who did not know how it ended.</p>

<p>The next chapter is the one that makes it useful.</p>
"""


# ---------------------------------------------------------------- chapter 2

CH2 = """
<p class="first">Here is the problem with reading about AI. Something is announced. It is
described as a step change. Six months later either it is everywhere and you were slow, or
it is gone and you were right to ignore it, and there was no way to tell which at the time.
Every engineer in the field has been played by this at least once, usually while defending a
technology choice in a meeting.</p>

<p>The archive contains an unusually clean solution, and it is structural rather than clever.
Each issue summarises <em>the same day</em> from three different places, and keeps them
separate:</p>

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

<p>Three views of one day, produced by three different populations with three different
incentives. Nobody designed this as an instrument. It is an instrument anyway.</p>

<h2>The measurement</h2>

<p>The method is deliberately dull. Take a pattern — a regular expression for
<code>agentic|agents?</code>, say — and count how often it occurs per ten thousand words
<em>inside a single named recap section</em>, half-year by half-year. Because the section is
fixed, the population writing it is roughly fixed too, and a change in the number is a change
in what that population talked about rather than a change in the document around it.</p>

<p>The obvious version of this measurement — count mentions across the whole issue — is
wrong, and wrong in a way that took me four months of analysis and one very bad afternoon to
find. Interlude II is that afternoon. For now, take it that the section is the unit.</p>

<p>Run it on the two most promoted ideas of the period and the result is not subtle.</p>
"""

CH2_B = """
<p>Agents rise 10.9× in announcement space between the first half of 2024 and the first half
of 2026. In community space, 3.5×. Among people running models on their own machines,
<strong>1.2×</strong> — which is to say, essentially not at all. Reasoning does the same thing
more gently: 2.5×, 1.9×, 1.4×.</p>

<p>That descending staircase is what hype looks like when you can measure it. It is not that
agents are fake; it is that the further you get from the people with something to announce,
the smaller the change becomes. If you only ever read announcement space — and announcement
space is what shows up in your feed, your inbox and your board deck — you are reading the
largest of three numbers and believing it is the only one.</p>

<h2>The part that makes it a tool</h2>

<p>If every pattern behaved that way, this would be a complaint about marketing rather than a
method. The useful discovery is that <strong>some patterns run the other way</strong>.</p>
"""

CH2_C = """
<p>The Chinese open-weights bloc — Qwen, DeepSeek, Kimi, GLM, MiniMax — rises 5.6× in
announcement space and <strong>8.9× in practice space</strong>, with community space higher
still at 12.2×. Practitioners were running those models, in volume, before the announcement
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
<p><strong>If a shift shrinks as you approach the people doing the work, it is a
narrative.</strong> Discount it, and wait.<br>
<strong>If it grows as you approach them, it is an adoption the coverage has not caught up
with.</strong> That is the one to act on early.<br>
<strong>If it moves the same amount everywhere, it is a real field-wide change.</strong>
Believe it.</p>
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

<p>With that in hand, the rest of Part II is a history: what this field actually paid
attention to, in order, from a December when everyone was fine-tuning to an August when
almost nobody talked about it.</p>

<p>But first, a confession, because I got the very first thing I measured completely wrong.</p>
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

<p>Here are four consecutive titles from the summer of 2026, exactly as published:</p>

<blockquote><p>not much happened today<br>
not much happened today<br>
not much happened today<br>
not much happened today</p></blockquote>

<p>Underneath those four issues, among other things, were a frontier model launch, a major
open-weights release, and a funding round in the billions. The phrase is not a description.
At some point in 2025 it had quietly become the newsletter's default title — the thing that
goes in the field when the editor has not written something better yet. In 2023, zero percent
of titles began that way. In 2026, <strong>68%</strong> did.</p>

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

<h2>What survived</h2>

<p>The fix was to restrict every headline measurement to titles that actually describe
something, which drops roughly half the corpus in the later years and makes the remaining
series much noisier and much less quotable. Under that restriction, the OpenAI collapse
disappears. So does most of the fragmentation story — and the rest of it died later, for an
unrelated reason, in a way I will get to in Interlude III.</p>

<p>What survived was the thing I had not built a story around: measurements taken inside the
body of the issues, in fixed sections, where the population writing the text was held
constant. That is the instrument the previous chapter described, and the reason it is the
instrument is that the obvious alternative failed first.</p>

<p>I would like to report that this was the last time. It was the second of four.</p>
"""


# ---------------------------------------------------------------- chapter 3

CH3 = """
<p class="first">To understand how strange the end of this story is, you have to start with a
field that believed its central activity was making models — and by “making,” it did not mean
training them from scratch. It meant taking someone else's weights and doing something to
them.</p>

<p>In the first half of 2024, <code>fine-tuning</code> appears 34.9 times per ten thousand
words of the newsletter's Twitter recap. That is the densest any theme in this archive reaches
until agents in 2025, and it means roughly one mention every three hundred words, every day,
for six months. Retrieval-augmented generation runs at 22.5. Between them they are the
architecture: take an open model, tune it on your data, put a vector database in front of it,
ship.</p>

<p>Two and a half years later, in announcement space, fine-tuning is at 1.9 and RAG is at 0.2.
The default architecture of 2024 essentially stopped being discussed.</p>

<p>The obvious reading — the field tried fine-tuning and RAG, and they did not work — is
wrong for both, in two different ways, and untangling that is most of Part III. This chapter
is about the world before it happened.</p>

<h2>December 2023: the Mixtral rush</h2>

<div class="scene">
<span class="when">2023-12-08 to 2023-12-15</span>
<p>Mistral releases the weights for an eight-expert mixture-of-experts model by posting a
magnet link. No paper, no code, no inference implementation. The issue on the 9th is titled
<em>The Mixtral Rush</em>, and describes independent groups racing to write the inference code
from scratch overnight so anyone can actually run the thing. By the 11th the headline is
<em>Mixtral beats GPT3.5 and Llama2-70B</em>. By the 15th, <em>Mixtral-Instruct beats Gemini
Pro</em>.</p>
</div>

<p>Seven days from an unexplained file to a model beating the previous generation's frontier.
That week set the emotional tone for the next eighteen months: <strong>open weights arriving
faster than anyone could evaluate them</strong>, and a community whose reflex was to
reimplement rather than wait.</p>

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
— they got worse — is not what the archive says. Mistral raised $1.7 billion and beat DeepSeek
in human evaluations in roughly the same month its coverage reached zero. Chapter 8 takes that
apart properly, because <em>ceasing to be news</em> and <em>ceasing to be good</em> turn out to
be different events with different causes, and telling them apart is worth real money to
anyone choosing a dependency.</p>
"""

CH3_C = """
<p>The figure above is the whole of Part II in outline, measured in announcement space. Two
themes that own the beginning and are near zero by the end; one that starts at nothing and
takes over. What it does not show — because a chart of what people talked about cannot show it
— is that the two falling lines fell for opposite reasons. Retrieval fell because it won so
completely that it stopped being worth mentioning; it is now a feature of every serious
product and a paragraph in every system design. Fine-tuning fell out of announcement space
while remaining, on the evidence of chapter 13, one of the largest sustained practical
activities in the entire archive.</p>

<p>Both fell 90%. One is absorption and one is a coverage artifact, and no amount of looking at
the falling line will tell you which is which.</p>

<p class="pull">A line going down is not a verdict. It is a question about where the thing
went.</p>

<p>The next chapter is about the third possibility — a good idea, loudly covered by
serious people, that simply never arrived at all.</p>
"""


# ---------------------------------------------------------------- chapter 4

CH4 = """
<p class="first">The third issue this book quotes ran on 8 December 2023 under the headline
<em>Mamba v Mistral v Hyena</em>. Three architectures, presented as live competitors on equal
footing. One of them is now inside nearly every model you use. Of the other two, one is a
footnote and one you have probably never heard of.</p>

<p>The interesting part is not that two of them lost. It is that the archive contains
<strong>four different ways to lose</strong>, they look almost identical in a chart, and only
one of them means the idea was wrong. Getting this distinction right is the difference
between correctly dropping a dead technique and abandoning something that was merely early.</p>

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
0.39) and in community space (2.38 to 0.43). Whatever happened, it happened everywhere, so by
the chapter-2 test it is not a coverage artifact. Something real ended.</p>
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
and datasets. The pure-SSM bet lost. The mechanism is in production.</p>

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
death looks like in this data, and the reason is legible from chapter 3: merging was a
technique for a world in which everyone had a pile of their own fine-tunes to combine. When
that world ended, the technique had nothing to operate on.</p>
"""

CH4_C = """
<h2>Fate three: refuted, then revived from below</h2>

<p>On 1 March 2024 the headline was <em>The Era of 1-bit LLMs</em>. The paper behind it —
BitNet b1.58 — proposed training models whose weights are restricted to three values,
&minus;1, 0 and 1, which removes multiplication from the forward pass almost entirely.
Announcement-space density hits 6.96. It is, briefly, the most exciting idea in the corpus.</p>

<p>Then, on 13 November 2024, a headline that is itself a verdict:</p>

<blockquote><p>BitNet was a lie?</p>
<cite>AI News, 2024-11-13</cite></blockquote>

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

<p>Nobody there is excited about the era of anything. They are asking which 4GB model is
better than which other 4GB model, on a laptop they own. That is the signature of an idea
that was not wrong, only early — it was waiting on kernels and hardware rather than on
insight, and it reappeared the moment someone shipped the kernels.</p>
"""

CH4_D = """
<h2>Fate four: still open</h2>

<p>On 10 March 2026 the headline was <em>Yann LeCun's AMI Labs launches with a $1.03B seed to
build world models</em>. World-model language in announcement space goes from 0.31 in early
2024 to 4.59 by early 2026 and 5.34 by the last half-year — a fifteenfold rise, on counts
large enough to trust (4 mentions, then 91).</p>

<p>Run the chapter-2 test on it. Because the practice-space baseline is a single mention, a
fold change is meaningless, so compare levels instead. In the first half of 2026: <strong>4.59
in announcement space, 1.22 in community space, 0.29 in practice space.</strong> That is the
descending staircase — the narrative signature, the same shape agents made.</p>

<p>Except this time I do not think the test applies, and it is worth being precise about why.</p>

<div class="aside">
<h4>Where the practice surface is blind</h4>
<p>Practice space is people running models on hardware they own. It is therefore an excellent
check on anything downloadable and <strong>no check at all</strong> on anything that requires
a data centre. You could not run a world model in 2026 if you wanted to. Reasoning models had
the same problem in late 2024 — invisible in practice space for months — and they were real.
When the practice surface is silent because the thing is unrunnable rather than uninteresting,
its silence carries no information.</p>
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

<p>None of these four is visible from the falling line alone, which is the recurring lesson of
this book stated in a new place. A chart of attention tells you where the conversation went.
It never tells you why, and the why is the entire decision.</p>

<p>The next chapter is about the one case where the conversation changed faster than anyone
could have kept up with — a whole field revising what it thought a model was, in about four
months.</p>
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
           + fig(F.surfaces([("agents", 10.9, 3.5, 1.2, "sig"),
                             ("reasoning", 2.5, 1.9, 1.4, "sig"),
                             ("China bloc", 5.6, 12.2, 8.9, "bench"),
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
                         [0, 40, 80, 120], "mentions / 10⁴ words"),
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
                         [0, 4, 8, 12], "mentions / 10⁴ words"),
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
    ]
