"""Inline-SVG chart primitives for the report. All coordinates computed, no hand-authored paths."""
from __future__ import annotations
import datetime as dt

W, H = 760, 300
PAD = {"t": 18, "r": 20, "b": 40, "l": 52}


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _x(i, n, w=W):
    inner = w - PAD["l"] - PAD["r"]
    return PAD["l"] + (inner * i / max(n - 1, 1))


def _y(v, lo, hi, h=H):
    inner = h - PAD["t"] - PAD["b"]
    if hi == lo:
        return PAD["t"] + inner / 2
    return PAD["t"] + inner * (1 - (v - lo) / (hi - lo))


def _frame(labels, lo, hi, ticks, h=H, w=W, ylab=""):
    out = []
    for t in ticks:
        y = _y(t, lo, hi, h)
        out.append(f'<line class="grid" x1="{PAD["l"]}" y1="{y:.1f}" x2="{w-PAD["r"]}" y2="{y:.1f}"/>')
        out.append(f'<text class="tick" x="{PAD["l"]-8}" y="{y+3.5:.1f}" text-anchor="end">{esc(t)}</text>')
    for i, lb in enumerate(labels):
        out.append(f'<text class="tick" x="{_x(i,len(labels),w):.1f}" y="{h-PAD["b"]+18}" text-anchor="middle">{esc(lb)}</text>')
    if ylab:
        out.append(f'<text class="axlab" x="{PAD["l"]-40}" y="{PAD["t"]-6}" text-anchor="start">{esc(ylab)}</text>')
    return "".join(out)


def lines(labels, series, ticks, ylab="", h=H, note_last=True):
    """series: [(name, values, css_class)]"""
    vals = [v for _, ys, _ in series for v in ys]
    lo, hi = 0, max(vals) * 1.12
    out = [f'<svg viewBox="0 0 {W} {h}" role="img" preserveAspectRatio="xMidYMid meet">']
    out.append(_frame(labels, lo, hi, ticks, h, ylab=ylab))
    for name, ys, cls in series:
        pts = " ".join(f"{_x(i,len(ys)):.1f},{_y(v,lo,hi,h):.1f}" for i, v in enumerate(ys))
        out.append(f'<polyline class="ln {cls}" points="{pts}"/>')
        for i, v in enumerate(ys):
            out.append(f'<circle class="dot {cls}" cx="{_x(i,len(ys)):.1f}" cy="{_y(v,lo,hi,h):.1f}" r="2.6"/>')
    if note_last:
        # place end labels, then push apart any that would overlap
        placed = sorted(((_y(ys[-1], lo, hi, h), name, cls) for name, ys, cls in series))
        laid = []
        for y, name, cls in placed:
            y = max(y, (laid[-1][0] + 15) if laid else y)
            laid.append((y, name, cls))
        lx = _x(len(series[0][1]) - 1, len(series[0][1]))
        for y, name, cls in laid:
            out.append(f'<text class="serlab {cls}" x="{lx-7:.1f}" y="{y-8:.1f}" text-anchor="end">{esc(name)}</text>')
    out.append("</svg>")
    return "".join(out)


def stacked(labels, bands, ticks, ylab=""):
    """bands: [(name, values, css_class)] — values are percentages summing to ~100"""
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" preserveAspectRatio="xMidYMid meet">']
    out.append(_frame(labels, 0, 100, ticks, ylab=ylab))
    base = [0.0] * len(labels)
    for name, ys, cls in bands:
        top = [base[i] + ys[i] for i in range(len(ys))]
        up = " ".join(f"{_x(i,len(ys)):.1f},{_y(v,0,100):.1f}" for i, v in enumerate(top))
        dn = " ".join(f"{_x(i,len(ys)):.1f},{_y(v,0,100):.1f}" for i, v in reversed(list(enumerate(base))))
        out.append(f'<polygon class="band {cls}" points="{up} {dn}"/>')
        # label each band where it is thickest, not at a fixed index
        k = max(range(len(ys)), key=lambda i: ys[i])
        if ys[k] > 8:
            my = _y((base[k] + top[k]) / 2, 0, 100)
            anchor = "middle"
            kx = _x(k, len(ys))
            if k == 0:
                anchor, kx = "start", kx + 8
            elif k == len(ys) - 1:
                anchor, kx = "end", kx - 8
            out.append(f'<text class="bandlab" x="{kx:.1f}" y="{my+4:.1f}" text-anchor="{anchor}">{esc(name)}</text>')
        base = top
    out.append("</svg>")
    return "".join(out)


def paired(rows):
    """rows: [(label, a, b, verdict)] — log-scaled fold changes around 1.0"""
    import math
    h = 40 + len(rows) * 46
    left = 132
    gutter = 96  # fixed right column for the verdict label, so it never clips
    out = [f'<svg viewBox="0 0 {W} {h}" role="img" preserveAspectRatio="xMidYMid meet">']
    lo, hi = math.log10(0.02), math.log10(20)

    def px(v):
        return left + (W - left - gutter) * (math.log10(max(v, 0.02)) - lo) / (hi - lo)

    for g in (0.1, 1, 10):
        x = px(g)
        out.append(f'<line class="grid" x1="{x:.1f}" y1="14" x2="{x:.1f}" y2="{h-22}"/>')
        lab = "no change" if g == 1 else (f"{g:g}×")
        out.append(f'<text class="tick" x="{x:.1f}" y="{h-8}" text-anchor="middle">{esc(lab)}</text>')
    for i, (label, a, b, verdict) in enumerate(rows):
        y = 34 + i * 46
        out.append(f'<text class="rowlab" x="{left-12}" y="{y+4}" text-anchor="end">{esc(label)}</text>')
        xa, xb = px(a), px(b)
        out.append(f'<line class="conn" x1="{xa:.1f}" y1="{y}" x2="{xb:.1f}" y2="{y}"/>')
        out.append(f'<circle class="dot sig" cx="{xa:.1f}" cy="{y}" r="6"/>')
        out.append(f'<circle class="dot bench" cx="{xb:.1f}" cy="{y}" r="6"/>')
        out.append(f'<text class="gaplab" x="{W-16}" y="{y+4}" text-anchor="end">{esc(verdict)}</text>')
    out.append("</svg>")
    return "".join(out)


def scatter_bt(rows):
    import math
    h = 320
    out = [f'<svg viewBox="0 0 {W} {h}" role="img" preserveAspectRatio="xMidYMid meet">']
    xs = [math.log10(c) for _, _, c in rows]
    ys = [s for _, s, _ in rows]
    xlo, xhi = math.log10(15), math.log10(230)
    ylo, yhi = 0, max(ys) * 1.12
    for t in (0, 1, 2, 3):
        y = _y(t, ylo, yhi, h)
        out.append(f'<line class="grid" x1="{PAD["l"]}" y1="{y:.1f}" x2="{W-PAD["r"]}" y2="{y:.1f}"/>')
        out.append(f'<text class="tick" x="{PAD["l"]-8}" y="{y+3.5:.1f}" text-anchor="end">{t}</text>')
    for c in (20, 50, 100, 200):
        x = PAD["l"] + (W - PAD["l"] - PAD["r"]) * (math.log10(c) - xlo) / (xhi - xlo)
        out.append(f'<text class="tick" x="{x:.1f}" y="{h-PAD["b"]+18}" text-anchor="middle">{c}</text>')
    y1 = _y(1.0, ylo, yhi, h)
    out.append(f'<line class="ref" x1="{PAD["l"]}" y1="{y1:.1f}" x2="{W-PAD["r"]}" y2="{y1:.1f}"/>')
    labels = []
    for name, s, c in rows:
        x = PAD["l"] + (W - PAD["l"] - PAD["r"]) * (math.log10(c) - xlo) / (xhi - xlo)
        y = _y(s, ylo, yhi, h)
        big = c >= 80
        out.append(f'<circle class="dot {"bench" if big else "sig"}" cx="{x:.1f}" cy="{y:.1f}" r="{5 if big else 3.6}"/>')
        if big or s > 1.6:
            labels.append([x + 8, y + 3.5, name])
    # nudge labels that would sit on top of each other
    labels.sort(key=lambda l: (l[1], l[0]))
    for i, lab in enumerate(labels):
        for prev in labels[:i]:
            if abs(lab[1] - prev[1]) < 11 and abs(lab[0] - prev[0]) < 66:
                lab[1] = prev[1] + 11
    for x, y, name in labels:
        out.append(f'<text class="ptlab" x="{x:.1f}" y="{y:.1f}">{esc(name)}</text>')
    out.append(f'<text class="axlab" x="{PAD["l"]-40}" y="{PAD["t"]-6}">BT strength</text>')
    out.append(f'<text class="axlab" x="{W-PAD["r"]}" y="{h-6}" text-anchor="end">comparisons (log)</text>')
    out.append("</svg>")
    return "".join(out)


def monthly_bars(rows, breaks):
    h = 250
    labels = [m for m, _ in rows]
    vals = [v for _, v in rows]
    lo, hi = 0, max(vals) * 1.15
    bw = (W - PAD["l"] - PAD["r"]) / len(rows) * 0.62
    out = [f'<svg viewBox="0 0 {W} {h}" role="img" preserveAspectRatio="xMidYMid meet">']
    for t in (0, 5, 10, 15, 20):
        y = _y(t, lo, hi, h)
        out.append(f'<line class="grid" x1="{PAD["l"]}" y1="{y:.1f}" x2="{W-PAD["r"]}" y2="{y:.1f}"/>')
        out.append(f'<text class="tick" x="{PAD["l"]-8}" y="{y+3.5:.1f}" text-anchor="end">{t}</text>')
    for i, (m, v) in enumerate(rows):
        x = _x(i, len(rows))
        y = _y(v, lo, hi, h)
        isbreak = m in breaks
        cls = "bench" if isbreak else "sig"
        out.append(f'<rect class="bar {cls}" x="{x-bw/2:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{_y(0,lo,hi,h)-y:.1f}"/>')
        if i % 2 == 0:
            out.append(f'<text class="tick tiny" x="{x:.1f}" y="{h-PAD["b"]+16}" text-anchor="middle">{esc(m[2:])}</text>')
    xl4 = _x(6, len(rows))
    out.append(f'<line class="ref dash" x1="{xl4:.1f}" y1="{PAD["t"]}" x2="{xl4:.1f}" y2="{h-PAD["b"]}"/>')
    out.append(f'<text class="ptlab" x="{xl4+7:.1f}" y="{PAD["t"]+12}">Llama 4 ships</text>')
    out.append(f'<text class="axlab" x="{PAD["l"]-40}" y="{PAD["t"]-6}">mentions / 10⁴ words</text>')
    out.append("</svg>")
    return "".join(out)


def km(cohorts):
    """Approximate KM curves from median survival, exponential with matched median."""
    import math
    h = 280
    out = [f'<svg viewBox="0 0 {W} {h}" role="img" preserveAspectRatio="xMidYMid meet">']
    tmax = 700
    for p in (0, 25, 50, 75, 100):
        y = _y(p, 0, 100, h)
        out.append(f'<line class="grid" x1="{PAD["l"]}" y1="{y:.1f}" x2="{W-PAD["r"]}" y2="{y:.1f}"/>')
        out.append(f'<text class="tick" x="{PAD["l"]-8}" y="{y+3.5:.1f}" text-anchor="end">{p}%</text>')
    for d in (0, 137, 300, 500, 700):
        x = PAD["l"] + (W - PAD["l"] - PAD["r"]) * d / tmax
        out.append(f'<text class="tick" x="{x:.1f}" y="{h-PAD["b"]+18}" text-anchor="middle">{d}d</text>')
    classes = {"All models": "ink", "US frontier labs": "bench", "Chinese labs": "sig"}
    for name, n, died, med in cohorts:
        if name not in classes:
            continue
        lam = math.log(2) / med
        pts = []
        for d in range(0, tmax + 1, 14):
            s = 100 * math.exp(-lam * d)
            x = PAD["l"] + (W - PAD["l"] - PAD["r"]) * d / tmax
            pts.append(f"{x:.1f},{_y(s,0,100,h):.1f}")
        out.append(f'<polyline class="ln {classes[name]}" points="{" ".join(pts)}"/>')
        xe = PAD["l"] + (W - PAD["l"] - PAD["r"]) * med / tmax
        out.append(f'<line class="ref dash" x1="{xe:.1f}" y1="{_y(50,0,100,h):.1f}" x2="{xe:.1f}" y2="{h-PAD["b"]:.1f}"/>')
        out.append(f'<text class="serlab {classes[name]}" x="{xe+7:.1f}" y="{_y(50,0,100,h)-8:.1f}">{esc(name)} · {med}d</text>')
    out.append(f'<text class="axlab" x="{PAD["l"]-40}" y="{PAD["t"]-6}">still discussed</text>')
    out.append("</svg>")
    return "".join(out)


def ribbon(regimes):
    """The recurring motif: publishing regimes on a true date axis."""
    h = 84
    d0 = dt.date(2023, 12, 6)
    d1 = dt.date(2026, 8, 6)
    span = (d1 - d0).days
    out = [f'<svg viewBox="0 0 {W} {h}" role="img" preserveAspectRatio="xMidYMid meet">']
    cls = ["r1", "r2", "r3", "r4"]
    for i, (a, b, n, name) in enumerate(regimes):
        xa = 8 + (W - 16) * (dt.date.fromisoformat(a) - d0).days / span
        xb = 8 + (W - 16) * (dt.date.fromisoformat(b) - d0).days / span
        out.append(f'<rect class="reg {cls[i]}" x="{xa:.1f}" y="20" width="{max(xb-xa,2):.1f}" height="26" rx="2"/>')
        cx = (xa + xb) / 2
        if xb - xa > 90:
            out.append(f'<text class="regname" x="{cx:.1f}" y="37">{esc(name)}</text>')
            out.append(f'<text class="tick tiny" x="{cx:.1f}" y="60" text-anchor="middle">{esc(a[:7])} → {esc(b[:7])}</text>')
            out.append(f'<text class="tick tiny" x="{cx:.1f}" y="73" text-anchor="middle">{n} issues</text>')
        else:
            out.append(f'<text class="tick tiny" x="{cx:.1f}" y="14" text-anchor="middle">{esc(name)}</text>')
    out.append("</svg>")
    return "".join(out)


def price(rows):
    import math
    h = 280
    labels = [p for p, _, _, _ in rows]
    out = [f'<svg viewBox="0 0 {W} {h}" role="img" preserveAspectRatio="xMidYMid meet">']
    lo, hi = math.log10(0.06), math.log10(12)

    def ly(v):
        inner = h - PAD["t"] - PAD["b"]
        return PAD["t"] + inner * (1 - (math.log10(v) - lo) / (hi - lo))

    for t in (0.1, 0.5, 1, 5, 10):
        y = ly(t)
        out.append(f'<line class="grid" x1="{PAD["l"]}" y1="{y:.1f}" x2="{W-PAD["r"]}" y2="{y:.1f}"/>')
        out.append(f'<text class="tick" x="{PAD["l"]-8}" y="{y+3.5:.1f}" text-anchor="end">${t:g}</text>')
    for i, lb in enumerate(labels):
        out.append(f'<text class="tick" x="{_x(i,len(labels)):.1f}" y="{h-PAD["b"]+18}" text-anchor="middle">{esc(lb)}</text>')
    med = " ".join(f"{_x(i,len(rows)):.1f},{ly(m):.1f}" for i, (_, m, _, _) in enumerate(rows))
    p10 = " ".join(f"{_x(i,len(rows)):.1f},{ly(p):.1f}" for i, (_, _, p, _) in enumerate(rows))
    poly = med + " " + " ".join(f"{_x(i,len(rows)):.1f},{ly(p):.1f}" for i, (_, _, p, _) in reversed(list(enumerate(rows))))
    out.append(f'<polygon class="band gap" points="{poly}"/>')
    out.append(f'<polyline class="ln sig" points="{med}"/>')
    out.append(f'<polyline class="ln bench" points="{p10}"/>')
    for i, (_, m, p, _) in enumerate(rows):
        out.append(f'<circle class="dot sig" cx="{_x(i,len(rows)):.1f}" cy="{ly(m):.1f}" r="3"/>')
        out.append(f'<circle class="dot bench" cx="{_x(i,len(rows)):.1f}" cy="{ly(p):.1f}" r="3"/>')
    out.append(f'<text class="serlab sig" x="{_x(2,len(rows)):.1f}" y="{ly(8)-11:.1f}" text-anchor="middle">median claimed price</text>')
    out.append(f'<text class="serlab bench" x="{_x(3,len(rows)):.1f}" y="{ly(0.45)+18:.1f}" text-anchor="middle">10th percentile — the cheap frontier</text>')
    out.append(f'<text class="axlab" x="{PAD["l"]-40}" y="{PAD["t"]-6}">$ / 1M tokens (log)</text>')
    out.append("</svg>")
    return "".join(out)


def context(rows):
    import math
    h = 250
    labels = [p for p, _ in rows]
    vals = [v for _, v in rows]
    lo, hi = math.log10(18), math.log10(1400)
    out = [f'<svg viewBox="0 0 {W} {h}" role="img" preserveAspectRatio="xMidYMid meet">']

    def ly(v):
        inner = h - PAD["t"] - PAD["b"]
        return PAD["t"] + inner * (1 - (math.log10(v) - lo) / (hi - lo))

    for t, lab in ((32, "32K"), (128, "128K"), (512, "512K"), (1000, "1M")):
        y = ly(t)
        out.append(f'<line class="grid" x1="{PAD["l"]}" y1="{y:.1f}" x2="{W-PAD["r"]}" y2="{y:.1f}"/>')
        out.append(f'<text class="tick" x="{PAD["l"]-8}" y="{y+3.5:.1f}" text-anchor="end">{lab}</text>')
    pts = " ".join(f"{_x(i,len(vals)):.1f},{ly(v):.1f}" for i, v in enumerate(vals))
    out.append(f'<polyline class="ln bench" points="{pts}"/>')
    for i, (p, v) in enumerate(rows):
        out.append(f'<circle class="dot bench" cx="{_x(i,len(vals)):.1f}" cy="{ly(v):.1f}" r="3.4"/>')
        out.append(f'<text class="tick" x="{_x(i,len(vals)):.1f}" y="{h-PAD["b"]+18}" text-anchor="middle">{esc(p)}</text>')
    out.append(f'<text class="ptlab" x="{_x(6,len(vals))-8:.1f}" y="{ly(1000)-10:.1f}" text-anchor="end">1M median</text>')
    out.append(f'<text class="axlab" x="{PAD["l"]-40}" y="{PAD["t"]-6}">claimed context (log)</text>')
    out.append("</svg>")
    return "".join(out)


def heat(periods, rows):
    """Domain heatmap: rows = [(name, [pct,...])]"""
    lh, left = 21, 168
    h = 34 + len(rows) * lh
    cw = (W - left - 24) / len(periods)
    out = [f'<svg viewBox="0 0 {W} {h}" role="img" preserveAspectRatio="xMidYMid meet">']
    for j, p in enumerate(periods):
        out.append(f'<text class="tick tiny" x="{left+cw*(j+.5):.1f}" y="16" text-anchor="middle">{esc(p)}</text>')
    for i, (name, vals) in enumerate(rows):
        y = 26 + i * lh
        out.append(f'<text class="rowlab" x="{left-10}" y="{y+14}" text-anchor="end">{esc(name)}</text>')
        for j, v in enumerate(vals):
            o = min(v / 90, 1.0)
            out.append(f'<rect class="cell" x="{left+cw*j:.1f}" y="{y:.1f}" width="{cw-2:.1f}" '
                       f'height="{lh-3}" rx="1.5" style="fill-opacity:{o:.3f}"/>')
            if v >= 40:
                out.append(f'<text class="cellv" x="{left+cw*(j+.5):.1f}" y="{y+14:.1f}" '
                           f'text-anchor="middle">{v}</text>')
    out.append("</svg>")
    return "".join(out)


def lifecycle(rows):
    """Benchmark lifespans as dated bars. rows = (name, claims, first, last, median, note)"""
    import datetime as dt
    lh, left, right = 24, 132, 210
    h = 34 + len(rows) * lh
    d0, d1 = dt.date(2024, 1, 1), dt.date(2026, 9, 1)
    span = (d1 - d0).days

    def px(s):
        y, m = int(s[:4]), int(s[5:7])
        return left + (W - left - right) * (dt.date(y, m, 1) - d0).days / span

    out = [f'<svg viewBox="0 0 {W} {h}" role="img" preserveAspectRatio="xMidYMid meet">']
    for yr in (2024, 2025, 2026):
        x = px(f"{yr}-01")
        out.append(f'<line class="grid" x1="{x:.1f}" y1="20" x2="{x:.1f}" y2="{h-16}"/>')
        out.append(f'<text class="tick tiny" x="{x+4:.1f}" y="14">{yr}</text>')
    for i, (name, n, a, b, med, note) in enumerate(rows):
        y = 26 + i * lh
        xa, xb = px(a), px(b)
        alive = b >= "2026-05"
        out.append(f'<text class="rowlab" x="{left-10}" y="{y+13}" text-anchor="end">{esc(name)}</text>')
        out.append(f'<rect class="bar {"bench" if alive else "sig"}" x="{xa:.1f}" y="{y+2:.1f}" '
                   f'width="{max(xb-xa,4):.1f}" height="13" rx="2"/>')
        out.append(f'<text class="tick tiny" x="{xb+8:.1f}" y="{y+13:.1f}">{med}% · {esc(note)}</text>')
    out.append("</svg>")
    return "".join(out)
