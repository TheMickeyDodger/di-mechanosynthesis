#!/usr/bin/env python3
"""Export the three H2-A-01 figure SVGs to PNG with the macOS image tool sips.

The script uses the Python standard library only. It is postprocess-only: it reads the three SVG files that the
renderers wrote (docs/figures/h2-a01-input-geometry.svg, h2-a01-scf-rows.svg and h2-a01-energy-components.svg) and
writes a PNG of each beside it, 1440 pixels wide (twice the 720 pixel SVG width), by calling /usr/bin/sips once per
figure. It draws nothing itself and reads no data. The PNG bytes depend on the operating system's SVG rasterizer, so
the repository records the tool and OS version that produced the committed PNG files (sips-316, macOS 27.0.1 build
26A434) in provenance/EXPORT-MANIFEST.md; the SVG files are the authoritative figures.

Usage, from the repository root:
    python3 tools/export_h2_figure_png.py
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURES = ("h2-a01-input-geometry", "h2-a01-scf-rows", "h2-a01-energy-components")
SIPS = "/usr/bin/sips"
WIDTH = 1440


def main():
    if not os.path.exists(SIPS):
        sys.exit("sips not found at %s; no PNG was written" % SIPS)
    for name in FIGURES:
        svg = os.path.join(ROOT, "docs", "figures", name + ".svg")
        png = os.path.join(ROOT, "docs", "figures", name + ".png")
        subprocess.run([SIPS, "-s", "format", "png", "--resampleWidth", str(WIDTH), svg, "--out", png],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("figure=%s width=%d output=%s" % (name, WIDTH, os.path.relpath(png, ROOT)))


if __name__ == "__main__":
    main()
