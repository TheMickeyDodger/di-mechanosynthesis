#!/usr/bin/env python3
"""Render the proposed activated donor candidate as a static SVG plate.

The script uses the Python standard library only and is deterministic. It reads the unchanged
coordinates in structures/donor-activated-EAOGe-C2-radical.extxyz and the heavy-atom bond list in
tools/activated-donor-bonds.tsv, which is transcribed from the atom-mapped SMILES and atom-identifier
table in docs/donor-candidates.md. Hydrogen atoms are bonded to the parent named in their identifier.
The script changes no coordinate and computes no chemistry: it checks the bond list against the
structure file, projects the given coordinates orthographically and writes
docs/figures/activated-donor.svg. All 48 atoms are read and every bond is validated, but only the 21
heavy atoms and the bonds between them are drawn; hydrogen atoms are omitted from the plate. Bond
strokes are clipped at the projected atom edges. Labels use chemical symbols mapped to atom IDs
(Ge = D-Ge1, C-alpha = D-Ca, C-beta = D-Cb, O1-O3 = D-O1 to D-O3).

View: the vertical page axis follows the D-Ge1 to D-Cb direction and the reference horizontal axis
follows the D-C7 to D-C3 direction orthogonalised against it. The view is rotated by an azimuth about
the vertical axis and then tilted about the horizontal axis. Both angles are chosen deterministically
from a fixed grid (AZIMUTHS_DEG x TILTS_DEG) by minimising the summed overlap of projected atom discs;
ties go to the smallest azimuth, then the smallest tilt. The choice affects the drawing only. Atoms and
bonds are drawn from back to front.

Usage, from the repository root:
    python3 tools/render_donor_plate.py
"""
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XYZ = os.path.join(ROOT, "structures", "donor-activated-EAOGe-C2-radical.extxyz")
BONDS = os.path.join(ROOT, "tools", "activated-donor-bonds.tsv")
OUT = os.path.join(ROOT, "docs", "figures", "activated-donor.svg")

WIDTH, HEIGHT, MARGIN, FOOT = 760, 620, 56, 44
AZIMUTHS_DEG = [5.0 * k for k in range(72)]
TILTS_DEG = [10.0, 15.0, 20.0, 25.0, 30.0]
RADIUS_A = {"Ge": 0.40, "C": 0.28, "O": 0.27, "H": 0.14}
FILL = {"Ge": "#6e8f8a", "C": "#454545", "O": "#c8322a", "H": "#f6f6f6"}
STROKE = {"Ge": "#24302e", "C": "#151515", "O": "#5e1510", "H": "#8c8c8c"}
LABELS = {"D-Ge1": "Ge", "D-Ca": "Cα", "D-Cb": "Cβ", "D-O1": "O1", "D-O2": "O2", "D-O3": "O3"}
FONT = "Helvetica, Arial, sans-serif"


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def mul(a, k):
    return (a[0] * k, a[1] * k, a[2] * k)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def unit(a):
    n = math.sqrt(dot(a, a))
    return mul(a, 1.0 / n)


def read_xyz(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    n = int(lines[0])
    atoms = []
    for line in lines[2:2 + n]:
        el, x, y, z, aid, mapnum, _radical = line.split()
        atoms.append((aid, el, (float(x), float(y), float(z)), int(mapnum)))
    assert len(atoms) == n
    return atoms


def read_bonds(path):
    bonds = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            a, b, order, ma, mb = line.rstrip("\n").split("\t")
            bonds.append((a, b, int(order), int(ma), int(mb)))
    return bonds


def main():
    atoms = read_xyz(XYZ)
    pos = {a[0]: a[2] for a in atoms}
    elem = {a[0]: a[1] for a in atoms}
    mapnum = {a[0]: a[3] for a in atoms}

    bonds = []
    for a, b, order, ma, mb in read_bonds(BONDS):
        assert mapnum[a] == ma and mapnum[b] == mb, "map number mismatch for %s-%s" % (a, b)
        bonds.append((a, b, order))
    for aid, el, _, _ in atoms:
        if el == "H":
            parent = aid.rsplit("-", 1)[0]
            assert parent in pos, "hydrogen without parent: %s" % aid
            bonds.append((parent, aid, 1))
    assert {x for a, b, _ in bonds for x in (a, b)} == set(pos), "every atom must be bonded"
    for a, b, _ in bonds:
        d = math.sqrt(dot(sub(pos[a], pos[b]), sub(pos[a], pos[b])))
        limit = 1.25 if "H" in (elem[a], elem[b]) else 2.10
        assert 0.9 <= d <= limit, "implausible listed bond %s-%s at %.3f A" % (a, b, d)

    up = unit(sub(pos["D-Cb"], pos["D-Ge1"]))
    across = sub(pos["D-C3"], pos["D-C7"])
    x0 = unit(sub(across, mul(up, dot(across, up))))
    z0 = cross(x0, up)
    ids = [a[0] for a in atoms if a[1] != "H"]
    heavy_bonds = [(a, b, o) for a, b, o in bonds if elem[a] != "H" and elem[b] != "H"]
    centre = mul(tuple(map(sum, zip(*[pos[k] for k in ids]))), 1.0 / len(ids))

    def frame(az_deg, tilt_deg):
        a, t = math.radians(az_deg), math.radians(tilt_deg)
        xax = add(mul(x0, math.cos(a)), mul(z0, math.sin(a)))
        zax = sub(mul(z0, math.cos(a)), mul(x0, math.sin(a)))
        yax = add(mul(up, math.cos(t)), mul(zax, math.sin(t)))
        zax = sub(mul(zax, math.cos(t)), mul(up, math.sin(t)))
        return {k: (dot(sub(pos[k], centre), xax), dot(sub(pos[k], centre), yax), dot(sub(pos[k], centre), zax))
                for k in ids}

    def overlap(pr):
        total = 0.0
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                a, b = ids[i], ids[j]
                d = math.hypot(pr[a][0] - pr[b][0], pr[a][1] - pr[b][1])
                total += max(0.0, 1.15 * (RADIUS_A[elem[a]] + RADIUS_A[elem[b]]) - d)
        return total

    best = min(((round(overlap(frame(az, tl)), 6), az, tl) for az in AZIMUTHS_DEG for tl in TILTS_DEG))
    _, azimuth, tilt = best
    proj = frame(azimuth, tilt)

    xs = [v[0] for v in proj.values()]
    ys = [v[1] for v in proj.values()]
    pad = 0.6
    scale = min((WIDTH - 2 * MARGIN) / (max(xs) - min(xs) + 2 * pad),
                (HEIGHT - 2 * MARGIN - FOOT) / (max(ys) - min(ys) + 2 * pad))
    ox = WIDTH / 2 - scale * (max(xs) + min(xs)) / 2
    oy = (HEIGHT - FOOT) / 2 + scale * (max(ys) + min(ys)) / 2

    def screen(k):
        x, y, _ = proj[k]
        return ox + scale * x, oy - scale * y

    items = []
    for i, (a, b, order) in enumerate(heavy_bonds):
        items.append(((proj[a][2] + proj[b][2]) / 2, 0, i, "bond", (a, b, order)))
    for i, aid in enumerate(ids):
        items.append((proj[aid][2] + 0.05, 1, i, "atom", aid))
    items.sort(key=lambda it: (it[0], it[1], it[2]))

    out = []
    out.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
               'role="img" aria-labelledby="plate-title plate-desc" font-family="%s">'
               % (WIDTH, HEIGHT, WIDTH, HEIGHT, FONT))
    out.append('  <title id="plate-title">Proposed activated donor candidate EAOGe-C2 radical, unoptimized input, '
               'heavy atoms only</title>')
    out.append('  <desc id="plate-desc">Orthographic ball-and-stick rendering of the 21 heavy atoms of the proposed '
               'activated donor candidate, drawn from the unchanged coordinates of '
               'structures/donor-activated-EAOGe-C2-radical.extxyz, an unoptimized RDKit ETKDGv3 embedding of 48 atoms. '
               'Hydrogen atoms are omitted. The germanium-substituted adamantane cage carries the C2 unit on '
               'germanium and three hydroxyethyl legs ending in oxygen atoms O1, O2 and O3. Labels map to atom IDs: '
               'Ge is D-Ge1, C-alpha is D-Ca, C-beta is D-Cb, O1 to O3 are D-O1 to D-O3. Bonds follow the atom-mapped '
               'SMILES documented in docs/donor-candidates.md. This is a proposed input, not an optimized or validated '
               'structure and not the benchmark authors\' coordinates.</desc>')
    out.append('  <rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>' % (WIDTH, HEIGHT))

    for _, _, _, kind, data in items:
        if kind == "bond":
            a, b, order = data
            (x1, y1), (x2, y2) = screen(a), screen(b)
            length = math.hypot(x2 - x1, y2 - y1)
            r1, r2 = RADIUS_A[elem[a]] * scale, RADIUS_A[elem[b]] * scale
            if length <= r1 + r2:
                continue
            ux, uy = (x2 - x1) / length, (y2 - y1) / length
            x1, y1, x2, y2 = x1 + ux * r1, y1 + uy * r1, x2 - ux * r2, y2 - uy * r2
            nx, ny = -uy, ux
            for k in range(order):
                off = (k - (order - 1) / 2) * 4.2
                out.append('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#6a6a6a" stroke-width="%.1f" '
                           'stroke-linecap="butt"/>'
                           % (x1 + nx * off, y1 + ny * off, x2 + nx * off, y2 + ny * off, 3.0 if order == 1 else 2.0))
        else:
            aid = data
            x, y = screen(aid)
            el = elem[aid]
            out.append('  <circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="0.9"/>'
                       % (x, y, RADIUS_A[el] * scale, FILL[el], STROKE[el]))

    # Label placement: try right, left, above and below each labelled atom and keep the first position
    # whose approximate text box least overlaps atom discs and sampled bond points.
    discs = [(screen(k), RADIUS_A[elem[k]] * scale) for k in ids]
    bond_pts = []
    for a, b, _ in heavy_bonds:
        (x1, y1), (x2, y2) = screen(a), screen(b)
        bond_pts += [(x1 + (x2 - x1) * s / 6.0, y1 + (y2 - y1) * s / 6.0) for s in range(1, 6)]

    def box_penalty(bx0, by0, bx1, by1):
        total = 0.0
        for (cx, cy), r in discs:
            dx = max(bx0 - cx, 0.0, cx - bx1)
            dy = max(by0 - cy, 0.0, cy - by1)
            total += max(0.0, r - math.hypot(dx, dy))
        total += sum(3.0 for px, py in bond_pts if bx0 <= px <= bx1 and by0 <= py <= by1)
        return total

    for aid, text in LABELS.items():
        x, y = screen(aid)
        r = RADIUS_A[elem[aid]] * scale
        w, h = 8.0 * len(text), 13.0
        options = [
            ("start", x + r + 5, y + 4, (x + r + 5, y - 8, x + r + 5 + w, y + 4)),
            ("end", x - r - 5, y + 4, (x - r - 5 - w, y - 8, x - r - 5, y + 4)),
            ("middle", x, y - r - 6, (x - w / 2, y - r - 6 - h, x + w / 2, y - r - 6)),
            ("middle", x, y + r + 16, (x - w / 2, y + r + 4, x + w / 2, y + r + 16)),
        ]
        scores = [round(box_penalty(*opt[3]), 6) for opt in options]
        anchor, tx, ty, _ = options[scores.index(min(scores))]
        out.append('  <text x="%.1f" y="%.1f" font-size="13" fill="#222222" text-anchor="%s">%s</text>'
                   % (tx, ty, anchor, text))

    bar = 2.0 * scale
    base = HEIGHT - 26
    out.append('  <line x1="%d" y1="%d" x2="%.1f" y2="%d" stroke="#222222" stroke-width="1.5"/>'
               % (MARGIN, base, MARGIN + bar, base))
    out.append('  <text x="%.1f" y="%d" font-size="12" fill="#222222" text-anchor="middle">2 Å</text>'
               % (MARGIN + bar / 2, base - 7))
    lx = WIDTH - MARGIN - 3 * 58 - 118
    for i, el in enumerate(["Ge", "C", "O"]):
        cx = lx + i * 58
        out.append('  <circle cx="%.1f" cy="%d" r="6" fill="%s" stroke="%s" stroke-width="0.9"/>'
                   % (cx, base - 4, FILL[el], STROKE[el]))
        out.append('  <text x="%.1f" y="%d" font-size="12" fill="#222222">%s</text>' % (cx + 11, base, el))
    out.append('  <text x="%d" y="%d" font-size="12" fill="#555555" text-anchor="end">H omitted</text>'
               % (WIDTH - MARGIN, base))
    out.append("</svg>")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("atoms_read=%d bonds_validated=%d heavy_drawn=%d heavy_bonds_drawn=%d azimuth=%.0f tilt=%.0f "
          "overlap=%.3f scale=%.2f px/A output=%s"
          % (len(atoms), len(bonds), len(ids), len(heavy_bonds), azimuth, tilt, best[0], scale,
             os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    main()
