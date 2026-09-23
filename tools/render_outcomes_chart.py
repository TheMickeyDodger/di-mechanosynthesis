#!/usr/bin/env python3
"""Render Figure 2: reported per-interaction target formation as a point-and-interval chart.

The script uses the Python standard library only and is deterministic. It reads
tools/benchmark-reported-outcomes.tsv, which transcribes the percentages, 95% confidence intervals and counts
reported by Cowie et al. (arXiv:2605.27250v1), and writes docs/figures/benchmark-outcomes.svg. It draws the
reported values as given; it does not recompute percentages or intervals from the counts. The horizontal axis
spans 0 to 100 percent.

Usage, from the repository root:
    python3 tools/render_outcomes_chart.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "tools", "benchmark-reported-outcomes.tsv")
OUT = os.path.join(ROOT, "docs", "figures", "benchmark-outcomes.svg")

WIDTH, HEIGHT = 720, 262
X0, X1 = 128.0, 520.0          # plot area for 0 and 100 percent
COLS = (540.0, 584.0, 650.0)   # value columns: reported percentage, reported 95% CI, counts
ROW0, ROW_STEP = 44.0, 42.0    # first row centre and row spacing
TEAL, GRAPHITE, GRID, INK, MUTED = "#127c78", "#3b3b3b", "#e4e4e4", "#1f1f1f", "#5a5a5a"
FONT = "Helvetica, Arial, sans-serif"


def read_rows(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            target, k, n, pct, lo, hi = line.rstrip("\n").split("\t")
            k, n, pct, lo, hi = int(k), int(n), int(pct), int(lo), int(hi)
            assert 0 < k <= n and 0 <= lo <= pct <= hi <= 100, "invalid row for %s" % target
            rows.append((target, k, n, pct, lo, hi))
    assert len(rows) == 4
    return rows


def x(p):
    return X0 + (X1 - X0) * p / 100.0


def main():
    rows = read_rows(DATA)
    axis_y = ROW0 + ROW_STEP * (len(rows) - 1) + 30
    out = []
    out.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" '
               'aria-labelledby="outcomes-title outcomes-desc" font-family="%s">' % (WIDTH, HEIGHT, WIDTH, HEIGHT, FONT))
    out.append('  <title id="outcomes-title">Per-interaction target formation reported by Cowie et al. '
               '(arXiv:2605.27250v1)</title>')
    desc = "; ".join("%s: %d of %d, reported %d percent, 95 percent confidence interval %d to %d" % (t, k, n, p, lo, hi)
                     for t, k, n, p, lo, hi in rows)
    out.append('  <desc id="outcomes-desc">Point-and-interval chart on a 0 to 100 percent axis of the experimental '
               'per-interaction outcomes reported by the benchmark authors, not results of this project. %s.</desc>' % desc)
    out.append('  <rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>' % (WIDTH, HEIGHT))

    for tick in range(0, 101, 20):
        out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>'
                   % (x(tick), ROW0 - 22, x(tick), axis_y, GRID))
        out.append('  <text x="%.1f" y="%.1f" font-size="12" fill="%s" text-anchor="middle">%d</text>'
                   % (x(tick), axis_y + 17, MUTED, tick))
    out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>'
               % (X0, axis_y, X1, axis_y, MUTED))
    out.append('  <text x="%.1f" y="%.1f" font-size="12.5" fill="%s" text-anchor="middle">'
               'Reported target formation (%%), with reported 95%% confidence interval</text>'
               % ((X0 + X1) / 2, axis_y + 38, INK))
    for col, head in zip(COLS, ("Rate", "95% CI", "Count")):
        out.append('  <text x="%.1f" y="%.1f" font-size="11.5" fill="%s">%s</text>' % (col, ROW0 - 26, MUTED, head))

    for i, (target, k, n, pct, lo, hi) in enumerate(rows):
        y = ROW0 + ROW_STEP * i
        out.append('  <text x="%.1f" y="%.1f" font-size="13" fill="%s" text-anchor="end">%s</text>'
                   % (X0 - 16, y + 4.5, INK, target))
        out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6"/>'
                   % (x(lo), y, x(hi), y, GRAPHITE))
        for edge in (lo, hi):
            out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6"/>'
                       % (x(edge), y - 5, x(edge), y + 5, GRAPHITE))
        out.append('  <circle cx="%.1f" cy="%.1f" r="5" fill="%s" stroke="#ffffff" stroke-width="1.5"/>'
                   % (x(pct), y, TEAL))
        out.append('  <text x="%.1f" y="%.1f" font-size="13" fill="%s">%d%%</text>' % (COLS[0], y + 4.5, INK, pct))
        out.append('  <text x="%.1f" y="%.1f" font-size="13" fill="%s">[%d, %d]</text>' % (COLS[1], y + 4.5, MUTED, lo, hi))
        out.append('  <text x="%.1f" y="%.1f" font-size="13" fill="%s">%d/%d</text>' % (COLS[2], y + 4.5, MUTED, k, n))
    out.append("</svg>")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("rows=%d output=%s" % (len(rows), os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    main()
