#!/usr/bin/env python3
"""Shared loading and tokenization for the method scripts.

Everything under `analysis/methods/` works on the article bodies rather than the
front-matter tags, so they all need the same preprocessing: strip front matter,
strip the boilerplate that repeats in every issue, and tokenize consistently.
"""

from __future__ import annotations

import functools
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


def clean(text: str) -> str:
    return BOILER.sub(" ", FRONT.sub("", text))


@functools.lru_cache(maxsize=1)
def load() -> list[tuple[str, str, str]]:
    """Return [(date, filename, cleaned body)] sorted by date."""
    out = []
    for path in sorted(ARTICLES.glob("*.md")):
        date = f"20{path.name[:8]}"
        out.append((date, path.name, clean(path.read_text(encoding="utf-8", errors="replace"))))
    return out


def tokens(text: str, drop_stop: bool = True) -> list[str]:
    words = TOKEN.findall(text.lower())
    if drop_stop:
        return [w for w in words if w not in STOP and len(w) > 2]
    return words


def half(date: str) -> str:
    return f"{date[:4]}H{1 if int(date[5:7]) <= 6 else 2}"


def quarter(date: str) -> str:
    return f"{date[:4]}Q{(int(date[5:7]) - 1) // 3 + 1}"
