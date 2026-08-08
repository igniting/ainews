#!/usr/bin/env python3
"""Build the book as a multi-page static site.

    python3 book/build_book.py              # -> site/
    python3 book/build_book.py --out docs   # -> docs/

One page per chapter plus a contents page, each a complete self-contained
document: no scripts, no external stylesheets, no remote fonts, no network at
all. Figures are computed SVG emitted inline by report/charts.py and book/figs.py.
"""
from __future__ import annotations

import argparse
import pathlib
import shutil
import sys
import urllib.parse

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))

import content as K  # noqa: E402
import shell as S  # noqa: E402

FAVICON = urllib.parse.quote(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
    '<rect width="32" height="32" rx="3" fill="#1A1A18"/>'
    '<path d="M9 8h14M9 13h14M9 18h9" stroke="#F7F7F5" stroke-width="2.4" '
    'stroke-linecap="round"/>'
    '<circle cx="21.5" cy="23" r="3.4" fill="#8C2F39"/></svg>',
    safe="")

KIND_LABEL = {"ch": "Chapter", "inter": "Interlude"}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def runhead(left: str, right: str) -> str:
    return (f'<div class="rh"><a href="index.html">{esc(K.TITLE)}</a>'
            f'<span>{right}</span></div>')


def nav(prev, nxt) -> str:
    out = ['<nav class="nav">']
    if prev:
        out.append(f'<a class="prev" href="{prev[0]}.html"><span class="dir">Previous</span>'
                   f'<span class="t">{esc(prev[1])}</span></a>')
    if nxt:
        out.append(f'<a class="next" href="{nxt[0]}.html"><span class="dir">Next</span>'
                   f'<span class="t">{esc(nxt[1])}</span></a>')
    else:
        out.append('<a class="next" href="index.html"><span class="dir">Contents</span>'
                   '<span class="t">The rest of the book is in draft</span></a>')
    out.append("</nav>")
    return "".join(out)


def page(title, desc, runhead_html, body) -> str:
    return S.SHELL.format(title=esc(title), desc=esc(desc), ogtitle=esc(title),
                          favicon=FAVICON, css=S.CSS, runhead=runhead_html, body=body)


def contents_page(drafted: set[str]) -> str:
    parts = [
        '<header class="title-page">',
        f'<h1>{esc(K.TITLE)}</h1>',
        f'<p class="sub">{esc(K.SUB)}</p>',
        '<div class="stats"><span><b>690</b> daily issues</span>'
        '<span><b>15.3M</b> words</span>'
        '<span><b>Dec 2023</b> – <b>Aug 2026</b></span>'
        '<span><b>3</b> measurement surfaces</span></div>',
        '</header>',
        '<div class="col">',
        '<p class="lead">This is a book about three years of artificial intelligence, read '
        'forwards — through a daily newsletter that summarised the field every weekday '
        'without knowing how any of it would turn out. It is also a book about how to read '
        'a fast-moving field without being played by it, which is the part that outlives '
        'the subject.</p>',
        '<p>No AI background is assumed. Every technical idea is introduced at the point the '
        'field introduced it, which happens to be the order that makes it easiest to '
        'understand.</p>',
        '</div>',
    ]
    ul_open = False
    for row in K.CONTENTS:
        if row[0] == "part":
            if ul_open:
                parts.append("</ul>")
                ul_open = False
            parts.append(f'<h2 class="part-head">{esc(row[1])}</h2><ul class="toc">')
            ul_open = True
            continue
        kind, num, title, question, slug = row
        live = slug in drafted
        cls = []
        if kind == "inter":
            cls.append("inter")
        if not live:
            cls.append("todo")
        li = f'<li class="{" ".join(cls)}">' if cls else "<li>"
        label = num if kind == "ch" else num
        href = f"{slug}.html" if live else "#"
        parts.append(f'{li}<a href="{href}"><span class="n">{esc(label)}</span>'
                     f'<span class="tx"><span class="t">{esc(title)}</span>'
                     f'<span class="d">{question}</span></span></a></li>')
    if ul_open:
        parts.append("</ul>")
    parts.append(
        '<div class="col"><hr class="sep">'
        '<p style="font-size:.92rem;color:var(--soft)">Chapters marked <em>in draft</em> are '
        'written but not yet typeset here. The measurements behind all of them are already '
        'published in this repository — the analysis scripts under <code>analysis/</code> '
        'regenerate every number in the book from the corpus.</p></div>')
    desc = ("A book about three years of AI read forwards, through 690 daily issues of a "
            "newsletter that never knew how it ended.")
    return page(f"{K.TITLE} — {K.SUB}", desc,
                '<div class="rh"><span>Contents</span><span>690 issues · 15.3M words</span></div>',
                '<div class="front">' + "".join(parts) + "</div>")


def chapter_page(entry, prev, nxt) -> str:
    slug, kind, num, title, question, body = entry
    label = f"{KIND_LABEL[kind]} {num}"
    # Interludes are asides about method, not steps in the argument. Mark them so a
    # reader landing on one knows immediately that the narrative has not moved on.
    cls = "opener inter-open" if kind == "inter" else "opener"
    tag = ('<span class="kind">an aside on method</span>' if kind == "inter" else "")
    opener = (f'<header class="{cls}"><p class="chno">{esc(label)}{tag}</p>'
              f'<h1>{esc(title)}</h1><p class="q">{question}</p></header>')
    html = ('<div class="col">' + opener + '</div>'
            + wrap_columns(body)
            + '<div class="col">' + nav(prev, nxt) + '</div>')
    return page(f"{title} — {K.TITLE}", strip_tags(question), runhead(K.TITLE, esc(label)), html)


def strip_tags(s: str) -> str:
    import re
    return re.sub(r"<[^>]+>", "", s)


def wrap_columns(body: str) -> str:
    """Figures and tables run full width; prose runs at the measure. The chapter text is
    written as one stream, so split it around block-level elements here."""
    import re
    out = []
    pos = 0
    for m in re.finditer(r"<(figure|div class=\"tw\")\b", body):
        start = m.start()
        tag = "figure" if m.group(1) == "figure" else "div"
        end = closing(body, start, tag)
        prose = body[pos:start]
        if prose.strip():
            out.append('<div class="col">' + prose + "</div>")
        out.append(body[start:end])
        pos = end
    tail = body[pos:]
    if tail.strip():
        out.append('<div class="col">' + tail + "</div>")
    return "".join(out)


def closing(s: str, start: int, tag: str) -> int:
    """Index just past the element opened at `start`, honouring nesting."""
    import re
    depth = 0
    for m in re.finditer(rf"</?{tag}\b[^>]*>", s[start:]):
        depth += -1 if m.group(0).startswith("</") else 1
        if depth == 0:
            return start + m.end()
    return len(s)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="site")
    args = ap.parse_args(argv)

    out = REPO / args.out
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    entries = K.pages()
    drafted = {e[0] for e in entries}
    titles = [(e[0], f"{KIND_LABEL[e[1]]} {e[2]} · {e[3]}") for e in entries]

    (out / "index.html").write_text(contents_page(drafted), encoding="utf-8")
    written = ["index.html"]
    for i, entry in enumerate(entries):
        prev = titles[i - 1] if i > 0 else ("index", "Contents")
        nxt = titles[i + 1] if i + 1 < len(entries) else None
        (out / f"{entry[0]}.html").write_text(chapter_page(entry, prev, nxt), encoding="utf-8")
        written.append(f"{entry[0]}.html")

    (out / ".nojekyll").write_text("", encoding="utf-8")
    total = sum((out / f).stat().st_size for f in written)
    print(f"wrote {len(written)} pages to {out.relative_to(REPO)}/ ({total:,} bytes)")
    for f in written:
        print(f"  {(out/f).stat().st_size:>8,}  {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
