#!/usr/bin/env python3
"""Shared loading and tokenization for the method scripts.

Everything under `analysis/methods/` works on the article bodies rather than the
front-matter tags, so they all need the same preprocessing: strip front matter,
strip the boilerplate that repeats in every issue, and tokenize consistently.
"""

from __future__ import annotations

import functools
import json
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
ARTICLES = REPO / "articles"

FRONT = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
# Per-issue boilerplate that would otherwise dominate any frequency method.
BOILER = re.compile(
    r"^>\s*(?:all recaps done by|AI News for).*$|"
    r"buttondown-editor-mode.*$|"
    r"https?://\S+|"
    r"^#{1,4}\s*(?:AI (?:Twitter|Reddit|Discord) Recap|PART \d).*$",
    re.M | re.I,
)
TOKEN = re.compile(r"[a-z][a-z0-9\-\.]{1,28}")

# Frequent, uninformative, and (for the domain words) so ubiquitous they drown
# out anything discriminative.
STOP = set(
    """the a an and or but if then than that this these those with without within from into onto
    for to of in on at by as is are was were be been being do does did have has had not no yes so
    such it its it's they them their there here what which who whom whose when where why how all
    any both each few more most other some only own same too very can will just should now also
    about after again against because before below between during further once over under up down
    out off while about you your yours we our ours i me my mine he she his her hers him
    new use used using get gets got make makes made like via etc vs vs. per one two three
    model models ai llm llms user users com www http https href img src png jpg
    discord twitter reddit message messages channel channels thread post posts comment comments
    said says say discussed discussing mentioned noted highlighted shared reported
    """.split()
)

# Markup and per-era template wording. These change when the publishing pipeline
# changes, so without them any frequency method ranks *format drift* as loudly as
# content drift — `div`, `linksmentioned` and `commenters` all outscored real
# content on a first pass.
FORMAT_NOISE = set(
    """div class span href img alt src table tbody thead style width height px
    linksmentioned linkmentioned description descriptions summary summaries recap recaps
    activity commenter commenters upvotes upvoted karma subreddit subreddits
    found strong links link mentions mention title titles image images video videos
    detail details section sections part parts general announcements
    """.split()
)
STOP |= FORMAT_NOISE


# "PART 2: Detailed by-Channel summaries" is a per-message transcript digest and is
# dominated by Discord handles. Left in, topic models cluster on *who was talking*
# rather than what about — a first pass returned topics made of usernames
# (solbus, noobmaster29, poltronsuperstar) instead of subjects.
PART2 = re.compile(r"^#\s*PART 2\b.*", re.M | re.I | re.S)
# The whole Discord recap is person-centric: even the Part 1 per-server summaries
# are built from "<handle> said X" lines. For topic modelling we want the news
# prose (lede + Twitter + Reddit), so this drops Discord entirely.
DISCORD = re.compile(r"^#\s*AI Discord Recap\b.*", re.M | re.I | re.S)


@functools.lru_cache(maxsize=1)
def handles() -> frozenset[str]:
    """Known person handles, taken from the front-matter `people` tags."""
    index = REPO / "analysis" / "index.json"
    if not index.exists():
        return frozenset()
    names = set()
    for record in json.loads(index.read_text(encoding="utf-8")):
        for person in record.get("people", []):
            person = person.strip().lower().lstrip("_")
            if person:
                names.add(person)
                names.add(person.replace("-", ""))
                names.update(person.split("-"))
    return frozenset(n for n in names if len(n) > 2)


def clean(text: str, drop_transcripts: bool = False, drop_discord: bool = False) -> str:
    text = FRONT.sub("", text)
    if drop_discord:
        text = DISCORD.sub(" ", text)
    elif drop_transcripts:
        text = PART2.sub(" ", text)
    return BOILER.sub(" ", text)


@functools.lru_cache(maxsize=4)
def load(drop_transcripts: bool = False, drop_discord: bool = False) -> list[tuple[str, str, str]]:
    """Return [(date, filename, cleaned body)] sorted by date."""
    out = []
    for path in sorted(ARTICLES.glob("*.md")):
        date = f"20{path.name[:8]}"
        raw = path.read_text(encoding="utf-8", errors="replace")
        out.append((date, path.name, clean(raw, drop_transcripts, drop_discord)))
    return out


def tokens(text: str, drop_stop: bool = True, drop_handles: bool = False) -> list[str]:
    words = TOKEN.findall(text.lower())
    if drop_stop:
        words = [w for w in words if w not in STOP and len(w) > 2]
    if drop_handles:
        bad = handles()
        words = [w for w in words if w not in bad]
    return words


def half(date: str) -> str:
    return f"{date[:4]}H{1 if int(date[5:7]) <= 6 else 2}"


def quarter(date: str) -> str:
    return f"{date[:4]}Q{(int(date[5:7]) - 1) // 3 + 1}"
