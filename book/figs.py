"""Book-specific figures. The report's chart primitives are reused where they fit;
these are the ones the book needs and the report never did."""
from __future__ import annotations

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "report"))

import charts as C  # noqa: E402

W = C.W


def cadence(rows):
    """rows: [(quarter, issues, median_kilowords)] — bars for cadence, line for length."""
    h = 270
    pad = {"t": 26, "r": 56, "b": 42, "l": 46}
    n = len(rows)
    inner_w = W - pad["l"] - pad["r"]
    imax = max(r[1] for r in rows) * 1.22
    wmax = max(r[2] for r in rows) * 1.22
    bw = inner_w / n * 0.56

    def x(i):
        return pad["l"] + inner_w * (i + 0.5) / n

    def yi(v):
        return pad["t"] + (h - pad["t"] - pad["b"]) * (1 - v / imax)

    def yw(v):
        return pad["t"] + (h - pad["t"] - pad["b"]) * (1 - v / wmax)

    out = [f'<svg viewBox="0 0 {W} {h}" role="img" preserveAspectRatio="xMidYMid meet">']
    for t in (0, 20, 40, 60):
        y = yi(t)
        out.append(f'<line class="grid" x1="{pad["l"]}" y1="{y:.1f}" x2="{W-pad["r"]}" y2="{y:.1f}"/>')
        out.append(f'<text class="tick" x="{pad["l"]-8}" y="{y+3.5:.1f}" text-anchor="end">{t}</text>')
    for t in (0, 10, 20, 30):
        y = yw(t)
        out.append(f'<text class="tick" x="{W-pad["r"]+8}" y="{y+3.5:.1f}" text-anchor="start">{t}k</text>')
    for i, (q, iss, kw) in enumerate(rows):
        out.append(f'<rect class="bar sig" x="{x(i)-bw/2:.1f}" y="{yi(iss):.1f}" '
                   f'width="{bw:.1f}" height="{yi(0)-yi(iss):.1f}"/>')
        if i % 2 == 0 or i == n - 1:
            out.append(f'<text class="tick tiny" x="{x(i):.1f}" y="{h-pad["b"]+16}" '
                       f'text-anchor="middle">{C.esc(q)}</text>')
    pts = " ".join(f"{x(i):.1f},{yw(kw):.1f}" for i, (_, _, kw) in enumerate(rows))
    out.append(f'<polyline class="ln bench" points="{pts}"/>')
    for i, (_, _, kw) in enumerate(rows):
        out.append(f'<circle class="dot bench" cx="{x(i):.1f}" cy="{yw(kw):.1f}" r="2.6"/>')
    out.append(f'<text class="axlab" x="{pad["l"]-38}" y="{pad["t"]-9}">issues per quarter</text>')
    out.append(f'<text class="serlab bench" x="{W-pad["r"]+18:.1f}" y="{pad["t"]-9}" '
               f'text-anchor="end">median issue length</text>')
    out.append("</svg>")
    return "".join(out)


def timeline(labels, series, ticks, ylab="", every=1, events=(), gutter=0, h=300):
    """Like charts.lines but for long dated series: labels every `every` points, and
    optional vertical event markers at given indices.

    series: [(name, values, css_class)]; events: [(index, text)]"""
    # one row per event annotation, so long labels never collide with each other
    pad = {"t": 26 + 14 * len(events), "r": 20 + gutter, "b": 40, "l": 52}
    n = len(labels)
    inner_w = W - pad["l"] - pad["r"]
    hi = max(v for _, ys, _ in series for v in ys) * 1.14

    def x(i):
        return pad["l"] + inner_w * i / max(n - 1, 1)

    def y(v):
        return pad["t"] + (h - pad["t"] - pad["b"]) * (1 - v / hi)

    out = [f'<svg viewBox="0 0 {W} {h}" role="img" preserveAspectRatio="xMidYMid meet">']
    for t in ticks:
        out.append(f'<line class="grid" x1="{pad["l"]}" y1="{y(t):.1f}" '
                   f'x2="{W-pad["r"]}" y2="{y(t):.1f}"/>')
        out.append(f'<text class="tick" x="{pad["l"]-8}" y="{y(t)+3.5:.1f}" '
                   f'text-anchor="end">{t}</text>')
    drawn = [i for i in range(n) if i % every == 0]
    if n - 1 - drawn[-1] > every * 0.6:
        drawn.append(n - 1)
    for i in drawn:
        out.append(f'<text class="tick tiny" x="{x(i):.1f}" y="{h-pad["b"]+16}" '
                   f'text-anchor="middle">{C.esc(labels[i])}</text>')
    # event markers first, so the data draws over them
    for k, (idx, text) in enumerate(events):
        ex = x(idx)
        out.append(f'<line class="ref dash" x1="{ex:.1f}" y1="{18+14*k:.0f}" '
                   f'x2="{ex:.1f}" y2="{h-pad["b"]:.1f}"/>')
        # anchor away from the nearer edge so the label always has room
        anchor = "end" if ex > pad["l"] + (W - pad["l"] - pad["r"]) * 0.62 else "start"
        dx = -6 if anchor == "end" else 6
        out.append(f'<text class="ptlab" x="{ex+dx:.1f}" y="{22+14*k:.0f}" '
                   f'text-anchor="{anchor}">{C.esc(text)}</text>')
    for name, ys, cls in series:
        pts = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(ys))
        out.append(f'<polyline class="ln {cls}" points="{pts}"/>')
        for i, v in enumerate(ys):
            out.append(f'<circle class="dot {cls}" cx="{x(i):.1f}" cy="{y(v):.1f}" r="2.2"/>')
        if gutter:
            out.append(f'<text class="serlab {cls}" x="{x(n-1)+9:.1f}" '
                       f'y="{y(ys[-1])+4:.1f}">{C.esc(name)}</text>')
    if ylab:
        out.append(f'<text class="axlab" x="{pad["l"]-44}" y="{pad["t"]-24}">{C.esc(ylab)}</text>')
    out.append("</svg>")
    return "".join(out)


def surfaces(rows):
    """rows: [(pattern, announcement, community, practice)] — three-point slope chart,
    log-scaled fold change, one line per pattern."""
    import math
    h = 330
    pad = {"t": 30, "r": 116, "b": 44, "l": 80}
    cols = ["Announcement", "Community", "Practice"]
    inner_w = W - pad["l"] - pad["r"]
    lo, hi = math.log10(0.06), math.log10(14)

    def x(i):
        return pad["l"] + inner_w * i / (len(cols) - 1)

    def y(v):
        f = (math.log10(max(v, 0.06)) - lo) / (hi - lo)
        return pad["t"] + (h - pad["t"] - pad["b"]) * (1 - f)

    out = [f'<svg viewBox="0 0 {W} {h}" role="img" preserveAspectRatio="xMidYMid meet">']
    for g, lab in ((0.1, "0.1×"), (1, "no change"), (10, "10×")):
        gy = y(g)
        cls = "ref" if g == 1 else "grid"
        out.append(f'<line class="{cls}" x1="{pad["l"]}" y1="{gy:.1f}" x2="{W-pad["r"]}" y2="{gy:.1f}"/>')
        out.append(f'<text class="tick" x="{pad["l"]-8}" y="{gy+3.5:.1f}" text-anchor="end">{lab}</text>')
    for i, c in enumerate(cols):
        out.append(f'<text class="axlab" x="{x(i):.1f}" y="{h-pad["b"]+18}" text-anchor="middle">{c}</text>')
    placed = []
    for name, a, b, c, cls in rows:
        pts = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate((a, b, c)))
        out.append(f'<polyline class="ln {cls}" points="{pts}"/>')
        for i, v in enumerate((a, b, c)):
            out.append(f'<circle class="dot {cls}" cx="{x(i):.1f}" cy="{y(v):.1f}" r="3.2"/>')
        placed.append((y(c), name, cls))
    laid = []
    for yy, name, cls in sorted(placed):
        yy = max(yy, (laid[-1][0] + 15) if laid else yy)
        laid.append((yy, name, cls))
    for yy, name, cls in laid:
        out.append(f'<text class="serlab {cls}" x="{x(2)+10:.1f}" y="{yy+4:.1f}">{C.esc(name)}</text>')
    out.append(f'<text class="axlab" x="{pad["l"]-70}" y="{pad["t"]-11}">fold change, 2024H1 → 2026H1</text>')
    out.append("</svg>")
    return "".join(out)
