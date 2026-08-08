#!/usr/bin/env python3
"""Verify every generated page is a complete, self-contained, balanced document.

    python3 book/check.py [site]

Run by CI before deploying. The book must work with no network at all, so any
external reference is a failure, not a warning.
"""
from __future__ import annotations

import pathlib
import re
import sys

VOID = {"br", "hr", "img", "input", "meta", "link", "circle", "line", "rect",
        "polyline", "polygon", "path", "use"}
EXTERNAL = (r"<script\b", r'<link[^>]+href="https?://', r'src="https?://', r"@import")


def check(path: pathlib.Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    fail = []
    if not html.startswith("<!doctype html>"):
        fail.append("missing doctype")
    if "<title>" not in html:
        fail.append("missing title")
    for tag in ("html", "head", "body"):
        if f"</{tag}>" not in html:
            fail.append(f"missing </{tag}>")
    for pat in EXTERNAL:
        if re.search(pat, html, re.I):
            fail.append(f"external reference: {pat}")
    stack: list[str] = []
    for m in re.finditer(r"<(/?)([a-zA-Z][\w-]*)([^>]*?)(/?)>", html):
        close, tag, selfc = m.group(1), m.group(2).lower(), m.group(4)
        if tag == "!doctype" or selfc == "/" or (tag in VOID and not close):
            continue
        if close:
            if not stack or stack[-1] != tag:
                fail.append(f"unbalanced </{tag}>")
            elif stack:
                stack.pop()
        else:
            stack.append(tag)
    if stack:
        fail.append(f"unclosed: {stack[:5]}")
    # every internal link must resolve to a page that exists
    for href in re.findall(r'href="([^"#][^"]*)"', html):
        if href.startswith("data:") or href.startswith("http"):
            continue
        if not (path.parent / href).exists():
            fail.append(f"dead link: {href}")
    return fail


def main(argv: list[str]) -> int:
    root = pathlib.Path(argv[1] if len(argv) > 1 else "site")
    pages = sorted(root.glob("*.html"))
    if not pages:
        print(f"no pages in {root}")
        return 1
    bad = 0
    for p in pages:
        fail = check(p)
        size = p.stat().st_size
        if fail:
            bad += 1
            print(f"FAILED {p.name}", *(f"    {f}" for f in fail), sep="\n")
        else:
            print(f"ok {p.name:<20} {size:>8,} bytes")
    if bad:
        print(f"\n{bad} of {len(pages)} pages failed")
        return 1
    print(f"\nall {len(pages)} pages self-contained and balanced")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
