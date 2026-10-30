#!/usr/bin/env python3
"""Render Figure 5: the signed energy components of the recorded H2-A-01 single point, as a static SVG.

The script uses the Python standard library only and is deterministic. It is postprocess-only: it runs no engine and
computes no chemistry. It reads tools/h2-a01-energy-components.tsv and writes docs/figures/h2-a01-energy-components.svg.
All three signed bars are anchored at zero on one common axis, with these endpoints: nuclear repulsion Vnn, electronic
energy E_elec and total energy E_total, each exactly as the table gives it (as a string, in hartree), with the sign
shown. The convention is the one the independent review established for this engine build: the reported total includes
the nuclear repulsion, so E_total = E_elec + Vnn, that is, E_elec = reported total - reported nuclear repulsion. Vnn and
E_total were reported by the engine. E_elec is that review's derivation, attributed to it; the engine did not print it,
so its bar is drawn with a dashed outline instead of a solid fill. The script checks the identity in exact decimal
arithmetic (a check, not a drawn quantity) and draws the table values only. The axis span (-2.0 to 1.0 hartree) is a
drawing choice.

Usage, from the repository root:
    python3 tools/render_h2_energy_components.py
"""
import os
from decimal import Decimal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "tools", "h2-a01-energy-components.tsv")
OUT = os.path.join(ROOT, "docs", "figures", "h2-a01-energy-components.svg")

WIDTH, HEIGHT = 720, 386
X0, X1 = 224.0, 536.0                 # pixel positions of VMIN and VMAX
VMIN, VMAX = -2.0, 1.0                # display span, hartree (a drawing choice)
VALUE_X = 554.0
ROWS_Y = (112.0, 168.0, 224.0)        # nuclear repulsion, electronic, total
BAR_H = 28.0
AXIS_Y = 254.0
TEAL, GRAPHITE, GRID, INK, MUTED = "#127c78", "#3b3b3b", "#e4e4e4", "#1f1f1f", "#5a5a5a"
FONT = "Helvetica, Arial, sans-serif"
COMPONENTS = ("nuclear_repulsion", "electronic", "total")


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
    vals, basis = {}, {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            comp, value, kind, source = line.rstrip("\n").split("\t")
            assert comp in COMPONENTS and comp not in vals, "invalid row for %s" % comp
            assert kind in ("engine_reported", "review_derivation")
            vals[comp], basis[comp] = value, kind
    assert tuple(sorted(vals)) == tuple(sorted(COMPONENTS)), "table rows do not match the expected components"
    assert basis == {"nuclear_repulsion": "engine_reported", "electronic": "review_derivation",
                     "total": "engine_reported"}
    return vals


def vx(v):
    return X0 + (X1 - X0) * (v - VMIN) / (VMAX - VMIN)


def signed(s):
    return s if s.startswith("-") else "+" + s


def main():
    assert contrast(INK, "#ffffff") >= 4.5 and contrast(MUTED, "#ffffff") >= 4.5 and contrast(TEAL, "#ffffff") >= 3.0
    v = read_table(DATA)
    d = {k: Decimal(x) for k, x in v.items()}
    assert d["nuclear_repulsion"] + d["electronic"] == d["total"], "E_total = E_elec + Vnn does not hold for the table"
    ends = {k: float(d[k]) for k in COMPONENTS}
    out = []
    out.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" '
               'aria-labelledby="components-title components-desc" font-family="%s">' % (WIDTH, HEIGHT, WIDTH, HEIGHT, FONT))
    out.append('  <title id="components-title">Signed energy components of the recorded H2-A-01 single point, in hartree</title>')
    out.append('  <desc id="components-desc">Three signed bars anchored at zero on one axis in hartree (Eh): nuclear repulsion Vnn %s, '
               'electronic energy E_elec %s and total energy E_total %s, as recorded for one RHF/STO-3G calculation at a fixed '
               'separation of 1.4 bohr, with E_total = E_elec + Vnn. Vnn and E_total were reported by the engine. E_elec is the '
               'independent review\'s derivation, reported total minus reported nuclear repulsion, under the convention that the '
               'reported total includes the nuclear repulsion; the engine did not print it, and its bar has a dashed outline. '
               'This is a single point and not a curve.</desc>'
               % (esc(signed(v["nuclear_repulsion"])), esc(v["electronic"]), esc(v["total"])))
    out.append('  <rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>' % (WIDTH, HEIGHT))
    out.append('  <text x="30" y="30" font-size="14" font-weight="bold" fill="%s">Signed energy components of the recorded '
               'single point (hartree, Eh)</text>' % INK)
    out.append('  <text x="30" y="49" font-size="12" fill="%s">One RHF/STO-3G calculation at a fixed separation of 1.4 bohr. '
               'All three bars start at zero on one axis. Signs are shown.</text>' % MUTED)
    for t in range(-4, 3):
        vt = t * 0.5
        out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>'
                   % (vx(vt), 70.0, vx(vt), AXIS_Y, GRID))
        label = "0" if t == 0 else ("%+.1f" % vt)
        out.append('  <text x="%.1f" y="%.1f" font-size="12" fill="%s" text-anchor="middle">%s</text>'
                   % (vx(vt), AXIS_Y + 17, MUTED, label))
    out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6"/>'
               % (vx(0.0), 70.0, vx(0.0), AXIS_Y, GRAPHITE))
    out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>'
               % (X0, AXIS_Y, X1, AXIS_Y, MUTED))
    out.append('  <text x="%.1f" y="%.1f" font-size="12.5" fill="%s" text-anchor="middle">Energy (hartree, Eh)</text>'
               % ((X0 + X1) / 2, AXIS_Y + 37, INK))
    labels = (("Nuclear repulsion, Vnn", "engine-reported"),
              ("Electronic energy, E_elec", "independent review's derivation"),
              ("Total energy, E_total", "engine-reported"))
    texts = (signed(v["nuclear_repulsion"]), v["electronic"], v["total"])
    for i, (comp, y, (lab, sub), txt) in enumerate(zip(COMPONENTS, ROWS_Y, labels, texts)):
        end = ends[comp]
        left, right = min(vx(0.0), vx(end)), max(vx(0.0), vx(end))      # every bar is anchored at zero
        if i == 1:
            out.append('  <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#ffffff" stroke="%s" stroke-width="2" '
                       'stroke-dasharray="6 3"/>' % (left, y - BAR_H / 2, right - left, BAR_H, GRAPHITE))
        else:
            out.append('  <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>'
                       % (left, y - BAR_H / 2, right - left, BAR_H, TEAL))
        out.append('  <text x="%.1f" y="%.1f" font-size="13" fill="%s" text-anchor="end">%s</text>' % (X0 - 20, y - 1, INK, esc(lab)))
        out.append('  <text x="%.1f" y="%.1f" font-size="11" fill="%s" text-anchor="end">%s</text>' % (X0 - 20, y + 13, MUTED, esc(sub)))
        out.append('  <text x="%.1f" y="%.1f" font-size="13" fill="%s">%s Eh</text>' % (VALUE_X, y + 4.5, INK, esc(txt)))
    out.append('  <text x="30" y="318" font-size="12.5" font-weight="bold" fill="%s">E_total = E_elec + Vnn:   %s = %s + %s Eh</text>'
               % (INK, esc(v["total"]), esc(v["electronic"]), esc(v["nuclear_repulsion"])))
    out.append('  <text x="30" y="338" font-size="11.5" fill="%s">Convention (independent review, this build): the reported total includes the '
               'nuclear repulsion.</text>' % INK)
    out.append('  <text x="30" y="354" font-size="11.5" fill="%s">The dashed bar is the review\'s derivation, E_elec = reported total - reported '
               'nuclear repulsion;</text>' % INK)
    out.append('  <text x="30" y="370" font-size="11.5" fill="%s">the engine did not print it. Solid bars are values the engine '
               'reported.</text>' % INK)
    out.append("</svg>")
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print("rows=%d output=%s" % (len(v), os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    main()
