#!/usr/bin/env python3
"""Render Figure 4: the SCF convergence of job H2-A-01, from the two rows the engine printed, as a static SVG.

The script uses the Python standard library only and is deterministic. It is postprocess-only: it runs no engine and
computes no chemistry. It reads tools/h2-a01-scf-rows.tsv, which copies the engine's own printed column labels and the
two printed rows, and writes docs/figures/h2-a01-scf-rows.svg with two panels.

Panel A is a two-point plot: SCF iteration (1 and 2 only) against the ABSOLUTE VALUE of the printed Delta E, in
hartree, on a logarithmic axis. Taking the absolute value is a postprocessing transformation, stated on the figure:
the engine printed signed values. The only operation applied to a printed Delta E is the removal of its leading minus
sign; the labels of the two points are those printed strings without the sign, and the vertical position of a point is
the base-10 logarithm of that printed number. No iteration 0, no extra sample and no curve other than the straight
segment joining the two actual points is drawn. A dashed reference line marks the recorded E_CONVERGENCE setting and is
labelled as that; it is not a statement that the engine's convergence decision is made on Delta E alone.

Panel B is the engine's own table, verbatim: its labels Total Energy, Delta E and RMS |[F,P]| and the two printed rows,
with the signed Delta E values. Nothing is rounded, relabelled or derived, Delta E is not recomputed from the totals,
and the third column is RMS |[F,P]|, not a density change. An equals sign is drawn between the two rows of a column
only when the two printed strings of that column are identical.

Usage, from the repository root:
    python3 tools/render_h2_scf_rows.py
"""
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "tools", "h2-a01-scf-rows.tsv")
OUT = os.path.join(ROOT, "docs", "figures", "h2-a01-scf-rows.svg")

WIDTH, HEIGHT = 720, 644
# panel A: plot area and axis ranges (display choices)
PL, PR, PT, PB = 118.0, 458.0, 116.0, 336.0
XMIN, XMAX = 0.5, 2.5                          # iteration axis; only 1 and 2 are marked
DEC_TOP, DEC_BOT = 1, -17                      # log10 of the top and bottom of the vertical axis
NOTE_X = 480.0
# panel B: table
LABEL_X = 34.0
RIGHT = (318.0, 462.0, 598.0)
TRAIL_X = 612.0
HEAD_Y, RULE_Y, ROW_Y, EQ_Y = 452.0, 462.0, (490.0, 536.0), 518.0
TEAL, GRAPHITE, GRID, INK, MUTED = "#127c78", "#3b3b3b", "#e4e4e4", "#1f1f1f", "#5a5a5a"
FONT = "Helvetica, Arial, sans-serif"
MONO = "Menlo, Monaco, 'Courier New', monospace"


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def _lum(h):
    r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a, b):
    hi, lo = sorted((_lum(a), _lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def read_table(path):
    header, rows, guide = None, [], None
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            row, label, total, delta, rms, trailer, source = line.rstrip("\n").split("\t")
            if row == "header":
                assert header is None
                header = (total, delta, rms)
            elif row == "guide":
                assert guide is None and label == "E_CONVERGENCE"
                guide = delta
            else:
                rows.append((row, label, total, delta, rms, trailer))
    assert header == ("Total Energy", "Delta E", "RMS |[F,P]|"), "unexpected printed column labels"
    assert [r[0] for r in rows] == ["1", "2"], "the table must hold exactly the two printed rows"
    assert guide is not None
    return header, rows, guide


def px(it):
    return PL + (PR - PL) * (it - XMIN) / (XMAX - XMIN)


def py(value):                                   # value: positive number; logarithmic position only
    return PT + (PB - PT) * (DEC_TOP - math.log10(value)) / (DEC_TOP - DEC_BOT)


def main():
    assert contrast(INK, "#ffffff") >= 4.5 and contrast(MUTED, "#ffffff") >= 4.5 and contrast(TEAL, "#ffffff") >= 3.0
    header, rows, guide = read_table(DATA)
    signed = [r[3] for r in rows]
    assert all(s.startswith("-") for s in signed), "the printed Delta E values are signed (negative)"
    absval = [s[1:] for s in signed]             # removal of the printed minus sign, the postprocessing transformation
    pts = [(float(it), float(a)) for it, a in zip((1, 2), absval)]
    out = []
    out.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" '
               'aria-labelledby="scf-title scf-desc" font-family="%s">' % (WIDTH, HEIGHT, WIDTH, HEIGHT, FONT))
    out.append('  <title id="scf-title">SCF convergence of job H2-A-01: the two printed iterations</title>')
    desc = "; ".join("iteration %s: Delta E printed as %s, plotted as the absolute value %s, Total Energy %s, RMS |[F,P]| %s"
                     % (r[0], r[3], a, r[2], r[4]) for r, a in zip(rows, absval))
    out.append('  <desc id="scf-desc">Panel A is a two-point plot of SCF iteration, 1 and 2 only, against the absolute value of the '
               'printed Delta E in hartree on a logarithmic axis, with the points joined by one straight segment and a dashed '
               'reference line at the recorded E_CONVERGENCE setting %s. The absolute value is a postprocessing transformation; '
               'the engine printed signed values. Panel B reproduces the engine\'s own two printed rows with its own labels '
               'Total Energy, Delta E and RMS |[F,P]|: %s. There is no iteration 0 and there are no other points.</desc>'
               % (esc(guide), esc(desc)))
    out.append('  <rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>' % (WIDTH, HEIGHT))
    out.append('  <text x="30" y="30" font-size="14" font-weight="bold" fill="%s">SCF convergence of job H2-A-01: the two '
               'printed iterations</text>' % INK)
    out.append('  <text x="30" y="49" font-size="12" fill="%s">Source: the engine\'s printed iteration table (psi4-output.dat lines '
               '151, 153 and 154). Nothing else was sampled.</text>' % MUTED)
    out.append('  <text x="30" y="80" font-size="13" font-weight="bold" fill="%s">A. Absolute value of the printed Delta E, '
               'logarithmic axis</text>' % INK)
    # panel A: grid, axes
    for dec in (0, -4, -8, -12, -16):
        y = py(10.0 ** dec)
        out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>' % (PL, y, PR, y, GRID))
        out.append('  <text x="%.1f" y="%.1f" font-size="12" fill="%s" text-anchor="end">1e%+03d</text>'
                   % (PL - 8, y + 4, MUTED, dec))
    for it in (1, 2):
        out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>' % (px(it), PT, px(it), PB, GRID))
        out.append('  <text x="%.1f" y="%.1f" font-size="12.5" fill="%s" text-anchor="middle">%d</text>' % (px(it), PB + 18, INK, it))
    out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>' % (PL, PT, PL, PB, MUTED))
    out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>' % (PL, PB, PR, PB, MUTED))
    out.append('  <text x="%.1f" y="%.1f" font-size="12.5" fill="%s" text-anchor="middle">SCF iteration (rows 1 and 2 as printed)</text>'
               % ((PL + PR) / 2, PB + 40, INK))
    out.append('  <text x="%.1f" y="%.1f" font-size="12" fill="%s">absolute value of Delta E (hartree), log scale</text>'
               % (PL, PT - 10, INK))
    # reference line at the recorded E_CONVERGENCE
    gy = py(float(guide))
    out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.4" stroke-dasharray="6 4"/>'
               % (PL, gy, PR, gy, GRAPHITE))
    out.append('  <text x="%.1f" y="%.1f" font-size="11.5" fill="%s" text-anchor="end">E_CONVERGENCE %s</text>'
               % (PR - 4, gy - 6, INK, esc(guide)))
    # the two actual points and the one segment between them
    (x1, v1), (x2, v2) = pts
    out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6"/>'
               % (px(x1), py(v1), px(x2), py(v2), GRAPHITE))
    for (xv, vv), a in zip(pts, absval):
        out.append('  <circle cx="%.1f" cy="%.1f" r="6" fill="%s" stroke="#ffffff" stroke-width="1.5"/>' % (px(xv), py(vv), TEAL))
        out.append('  <text x="%.1f" y="%.1f" font-size="13" fill="%s">%s</text>' % (px(xv) + 11, py(vv) + 4.5, INK, esc(a)))
    # plain statement of the transformation, beside the plot, in a tinted box so that it stands out
    boxed = ("Postprocessing transformation:", "the plotted quantity is the", "absolute value of Delta E. The",
             "engine printed signed values,", "%s and %s;" % (signed[0], signed[1]), "only the minus sign was removed.")
    rest = ("", "Dashed line: the recorded", "E_CONVERGENCE setting, shown as", "a reference only.", "",
            "Two points, joined by one segment.", "No iteration 0 and no other sample.")
    out.append('  <rect x="%.1f" y="%.1f" width="236" height="%.1f" fill="#f2f2f2"/>' % (NOTE_X - 10, PT - 8, 17 * len(boxed) + 10))
    out.append('  <rect x="%.1f" y="%.1f" width="3" height="%.1f" fill="%s"/>' % (NOTE_X - 10, PT - 8, 17 * len(boxed) + 10, TEAL))
    ny = PT + 6
    for text in boxed:
        out.append('  <text x="%.1f" y="%.1f" font-size="12" fill="%s">%s</text>' % (NOTE_X, ny, INK, esc(text)))
        ny += 17
    ny += 10
    for text in rest:
        if text:
            out.append('  <text x="%.1f" y="%.1f" font-size="12" fill="%s">%s</text>' % (NOTE_X, ny, MUTED, esc(text)))
        ny += 17
    # panel B: the engine's own printed rows, verbatim
    out.append('  <text x="30" y="424" font-size="13" font-weight="bold" fill="%s">B. The two printed rows, verbatim (signed Delta E)</text>' % INK)
    for edge, head in zip(RIGHT, header):
        out.append('  <text x="%.1f" y="%.1f" font-size="13" font-family="%s" fill="%s" text-anchor="end" '
                   'xml:space="preserve">%s</text>' % (edge, HEAD_Y, MONO, MUTED, esc(head)))
    out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>' % (LABEL_X, RULE_Y, 676.0, RULE_Y, GRID))
    for (row, label, total, delta, rms, trailer), y in zip(rows, ROW_Y):
        out.append('  <text x="%.1f" y="%.1f" font-size="13" font-family="%s" fill="%s" xml:space="preserve">%s</text>'
                   % (LABEL_X, y, MONO, INK, esc(label)))
        for edge, val in zip(RIGHT, (total, delta, rms)):
            out.append('  <text x="%.1f" y="%.1f" font-size="13" font-family="%s" fill="%s" text-anchor="end" '
                       'xml:space="preserve">%s</text>' % (edge, y, MONO, INK, esc(val)))
        out.append('  <text x="%.1f" y="%.1f" font-size="13" font-family="%s" fill="%s" xml:space="preserve">%s</text>'
                   % (TRAIL_X, y, MONO, MUTED, esc(trailer)))
    for col, edge in enumerate(RIGHT):          # an equals sign only where the two printed strings are identical
        if rows[0][2 + col] == rows[1][2 + col]:
            out.append('  <text x="%.1f" y="%.1f" font-size="18" font-weight="bold" fill="%s" text-anchor="end">=</text>'
                       % (edge - 52.0, EQ_Y, TEAL))
    out.append('  <text x="30" y="572" font-size="12" fill="%s">An = between the rows marks a column whose two printed strings '
               'are identical.</text>' % INK)
    out.append('  <text x="30" y="590" font-size="12" fill="%s">Delta E is quoted as printed; it is not recomputed from the '
               'rounded totals. The engine printed no iteration 0 row.</text>' % INK)
    out.append('  <text x="30" y="608" font-size="12" fill="%s">Units: Total Energy and Delta E are energies in hartree (Eh).</text>' % MUTED)
    out.append('  <text x="30" y="624" font-size="12" font-family="%s" fill="%s" xml:space="preserve">RMS |[F,P]| (third column): '
               'the engine prints no unit.</text>' % (MONO, MUTED))
    out.append("</svg>")
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print("rows=%d output=%s" % (len(rows), os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    main()
