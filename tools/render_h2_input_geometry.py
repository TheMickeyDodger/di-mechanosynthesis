#!/usr/bin/env python3
"""Render Figure 3: the fixed input geometry of job H2-A-01 as a static SVG.

The script uses the Python standard library only and is deterministic. It is postprocess-only: it runs no engine and
computes no chemistry. It reads tools/h2-a01-input-geometry.tsv, which transcribes the two atom positions that the
engine-side read-back recorded and the recorded separation, and writes docs/figures/h2-a01-input-geometry.svg. The
coordinates are printed exactly as the table gives them (as strings). The script checks, in exact decimal
arithmetic, that both atoms lie on the z axis, that their z coordinates are opposite and that their distance equals
the recorded separation; it draws the table values and does not derive any of them. The drawing shows a fixed INPUT
geometry. It is not an optimized geometry, and the 1.4 bohr internuclear distance is a fixed input, not an optimized or
predicted equilibrium bond length. The horizontal span of the axis (-1.5 to 1.5 bohr)
and the marker size are drawing choices.

Usage, from the repository root:
    python3 tools/render_h2_input_geometry.py
"""
import os
from decimal import Decimal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "tools", "h2-a01-input-geometry.tsv")
OUT = os.path.join(ROOT, "docs", "figures", "h2-a01-input-geometry.svg")

WIDTH, HEIGHT = 720, 292
X0, X1 = 110.0, 610.0            # pixel positions of the display span ends
ZMIN, ZMAX = -1.5, 1.5           # display span, bohr (a drawing choice)
AXIS_Y = 172.0
TEAL, GRAPHITE, GRID, INK, MUTED = "#127c78", "#3b3b3b", "#e4e4e4", "#1f1f1f", "#5a5a5a"
FONT = "Helvetica, Arial, sans-serif"
KEYS = ("H1.x", "H1.y", "H1.z", "H2.x", "H2.y", "H2.z", "separation")


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
    vals = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            key, value, unit, source = line.rstrip("\n").split("\t")
            assert key in KEYS and key not in vals and unit == "bohr", "invalid row for %s" % key
            vals[key] = value
    assert tuple(sorted(vals)) == tuple(sorted(KEYS)), "table rows do not match the expected keys"
    return vals


def px(z):
    return X0 + (X1 - X0) * (z - ZMIN) / (ZMAX - ZMIN)


def signed(s):
    return s if s.startswith("-") else "+" + s


def main():
    assert contrast(INK, "#ffffff") >= 4.5 and contrast(MUTED, "#ffffff") >= 4.5 and contrast(TEAL, "#ffffff") >= 3.0
    v = read_table(DATA)
    d = {k: Decimal(x) for k, x in v.items()}
    assert d["H1.x"] == 0 and d["H1.y"] == 0 and d["H2.x"] == 0 and d["H2.y"] == 0, "atoms must lie on the z axis"
    assert d["H1.z"] == -d["H2.z"] and d["H2.z"] - d["H1.z"] == d["separation"], "geometry and separation disagree"
    z1, z2 = float(d["H1.z"]), float(d["H2.z"])
    out = []
    out.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" '
               'aria-labelledby="geometry-title geometry-desc" font-family="%s">' % (WIDTH, HEIGHT, WIDTH, HEIGHT, FONT))
    out.append('  <title id="geometry-title">Fixed input geometry of job H2-A-01: two hydrogen atoms on the z axis, '
               '%s bohr apart</title>' % esc(v["separation"]))
    out.append('  <desc id="geometry-desc">Drawing, to scale along the z axis in bohr, of the fixed input geometry given to '
               'the engine: H1 at (%s, %s, %s) bohr and H2 at (%s, %s, %s) bohr, separated by %s bohr. It is an input '
               'geometry that was fixed, not an optimized geometry; the separation is the fixed input internuclear distance, not an '
               'optimized or predicted equilibrium bond length. The marker size is a drawing '
               'choice, not an atomic radius.</desc>'
               % (esc(v["H1.x"]), esc(v["H1.y"]), esc(v["H1.z"]), esc(v["H2.x"]), esc(v["H2.y"]), esc(v["H2.z"]),
                  esc(v["separation"])))
    out.append('  <rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>' % (WIDTH, HEIGHT))
    out.append('  <text x="30" y="30" font-size="14" font-weight="bold" fill="%s">Fixed input geometry, not optimized: '
               'H1 and H2 on the z axis</text>' % INK)
    out.append('  <text x="30" y="49" font-size="12" fill="%s">x = y = 0 for both atoms. The marker size is a drawing '
               'choice, not an atomic radius.</text>' % MUTED)
    for t in range(-3, 4):
        zt = t * 0.5
        out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>'
                   % (px(zt), AXIS_Y - 84, px(zt), AXIS_Y + 6, GRID))
        label = "0" if t == 0 else ("%+.1f" % zt)
        out.append('  <text x="%.1f" y="%.1f" font-size="12" fill="%s" text-anchor="middle">%s</text>'
                   % (px(zt), AXIS_Y + 22, MUTED, label))
    out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>'
               % (X0, AXIS_Y, X1, AXIS_Y, MUTED))
    out.append('  <text x="%.1f" y="%.1f" font-size="12.5" fill="%s" text-anchor="middle">z coordinate (bohr)</text>'
               % ((X0 + X1) / 2, AXIS_Y + 42, INK))
    # separation dimension line, above the atoms
    dy = AXIS_Y - 66
    out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6"/>'
               % (px(z1), dy, px(z2), dy, GRAPHITE))
    for z in (z1, z2):
        out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.6"/>'
                   % (px(z), dy - 5, px(z), dy + 5, GRAPHITE))
    out.append('  <text x="%.1f" y="%.1f" font-size="13" fill="%s" text-anchor="middle">fixed separation %s bohr</text>'
               % ((px(z1) + px(z2)) / 2, dy - 9, INK, esc(v["separation"])))
    for name, z, zs in (("H1", z1, v["H1.z"]), ("H2", z2, v["H2.z"])):
        out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1" stroke-dasharray="3 3"/>'
                   % (px(z), dy + 5, px(z), AXIS_Y - 40, MUTED))
        out.append('  <circle cx="%.1f" cy="%.1f" r="14" fill="%s" stroke="#ffffff" stroke-width="1.5"/>'
                   % (px(z), AXIS_Y, TEAL))
        out.append('  <text x="%.1f" y="%.1f" font-size="14" font-weight="bold" fill="%s" text-anchor="middle">%s</text>'
                   % (px(z), AXIS_Y - 23, INK, name))
        out.append('  <text x="%.1f" y="%.1f" font-size="12.5" fill="%s" text-anchor="middle">z = %s bohr</text>'
                   % (px(z), AXIS_Y + 64, INK, esc(signed(zs))))
        out.append('  <text x="%.1f" y="%.1f" font-size="11.5" fill="%s" text-anchor="middle">(%s, %s, %s)</text>'
                   % (px(z), AXIS_Y + 81, MUTED, esc(v[name + ".x"]), esc(v[name + ".y"]), esc(zs)))
    out.append("</svg>")
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print("rows=%d output=%s" % (len(v), os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    main()
