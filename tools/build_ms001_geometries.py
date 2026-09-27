"""Build the MS-001 Stage 0 model geometries (B1) and validation configurations (C7) geometrically.

Evidence label: [AGENT]. Every coordinate written here comes from a declared geometric rule: lattice points, a
dimer and cap construction, rigid rotations and rigid translations. Nothing is relaxed or optimized, no
calculator is attached, and no energy, force or gradient is evaluated. No bond order, bond cleavage, electronic
state, spin state or stability is computed. Topology words (dimer, cap, three-coordinate site, contact) name the
construction recipe and the constructed distances only. "dangling-bond pair" is only a nominal name for two
three-coordinate, unterminated Si sites. "intact" and "broken" in two file names are nominal C7 names and denote
the geometry recipe only. The files are proposals, not measurements or results. They are not a model of the
benchmark's geometry and have not been compared with the benchmark authors' coordinates, which this project has
not obtained [GAP].

Outputs (default directory structures/ms-001/):
    M1-build-site.extxyz                 M1: H:Si(100)-2x1 cluster with two three-coordinate, unterminated
                                         top-layer Si sites facing each other across one inter-row trough
    start-combined.extxyz                M1 with the tool file (M2) placed above the two sites, D-Cb toward M1
    V1-separated-bodies.extxyz           C7 V1, nominal "separated bodies": same coordinates as the start
    V2-contact-GeC-intact.extxyz         C7 V2, nominal "contact, Ge-C intact": tool rigidly translated so that
                                         D-Cb lies at the declared contact distance from one site; D-Ge1 to D-Ca
                                         at its constructed M2 distance
    V3-pendent-C2-GeC-broken.extxyz      C7 V3, nominal "pendent C2, Ge-C broken": V2 with D-Ca and D-Cb kept in
                                         place and the other 46 tool atoms rigidly translated by a declared vector
    P2-test-molecule-H3GeCCSiH3.extxyz   C7: the P2 cross-engine test molecule geometry
    geometry-record.json                 every declared parameter, every reported distance and angle as measured
                                         on the written file, and each file's SHA256

M2 is the published file structures/donor-activated-EAOGe-C2-radical.extxyz, read by digest and not
regenerated. Run from the repository root:  python tools/build_ms001_geometries.py [--outdir DIR]
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

import ase
from ase import Atoms
from ase.build import diamond100
from ase.data import atomic_numbers, covalent_radii, reference_states
from ase.io import read, write

REPO = Path(__file__).resolve().parents[1]
GENERATOR = 'tools/build_ms001_geometries.py'
M2_FILE = 'structures/donor-activated-EAOGe-C2-radical.extxyz'
M2_SHA256 = 'bb7ab3443a99fcdfe47df6a928a07cc45cdd531299051727a5b160493c9186e3'
PROTECTED = {'donor-activated-EAOGe-C2-radical.extxyz', 'donor-precursor-EAOGe-C2I.extxyz'}

# Declared [AGENT] parameters. Radii and the lattice constant are read from the ASE 3.29.0 tables and checked here.
LATTICE_A = 5.43              # angstrom; ase.data.reference_states[Si]['a']
DIMERS_PER_ROW = 5            # dimers along each dimer row
DIMER_ROWS = 4                # dimer rows; the pair spans the trough between rows 1 and 2 (0-based)
SI_LAYERS = 4                 # silicon layers, the dimer layer included
PAIR_ROWS = (1, 2)            # the two rows whose facing top-layer atoms are left without an H cap
PAIR_COLUMN = 2               # dimer position along the rows (0-based; the middle of five)
START_HEIGHT = 6.00           # angstrom; tool Cb above the plane of the two pair Si atoms in the start
V3_LIFT = 1.50                # angstrom; rigid +z displacement of the tool without its C2 unit in V3
COVALENT = {el: float(covalent_radii[atomic_numbers[el]]) for el in ('H', 'C', 'Si', 'Ge')}
R_SIH = COVALENT['Si'] + COVALENT['H']
R_SIC = COVALENT['Si'] + COVALENT['C']
R_GEH = COVALENT['Ge'] + COVALENT['H']

BENCHMARK_RELATION = ('not a model of the benchmark geometry; not compared with the benchmark authors '
                      'coordinates, which have not been obtained [GAP]')
CONSTRUCTION = 'geometric construction only; no relaxation, optimization, energy, force or gradient evaluation'
NOT_COMPUTED = ('bond order, bond formation or cleavage, electronic state, spin state and stability were not '
                'computed; no energy, force or gradient was evaluated; no geometry is relaxed; not compared with the '
                "benchmark authors' coordinates [GAP]; not a model of the benchmark geometry; topology words name the "
                'construction recipe and constructed distances only')
FILENAME_NOTE = 'intact/broken in the V2 and V3 file names are C7 recipe labels and denote the geometry recipe only'

# Every reported distance and angle is measured on the coordinates read back from the written file, and every declared
# value is asserted against that measurement within these declared tolerances. The files carry 8 decimals.
DIST_TOL = 1e-6                                           # angstrom
ANGLE_TOL = 1e-4                                          # degrees
TETRAHEDRAL_DEG = float(np.degrees(np.arccos(-1.0 / 3.0)))  # ideal tetrahedral angle, 109.4712206...
MEASUREMENT_BASIS = ('every derived distance and angle is measured on the coordinates read back from the written '
                     'file (norms and dot products); each declared value is asserted within '
                     f'{DIST_TOL:g} A for distances and {ANGLE_TOL:g} deg for angles')


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def measure(atoms, specs):
    """Measure on the given coordinates and assert each declared value; returns {label: measurement}.

    Spec kinds (atom ids, declared value or None):
      ('distance', (a, b), d)                      |b - a|
      ('angle', (a, centre, b), deg)               angle at centre between centre->a and centre->b, by dot product
      ('z_difference', (a, b), d)                  z(a) - z(b)
      ('xy_offset_from_midpoint', (a, b, c), d)    lateral distance of a from the midpoint of b and c
      ('projected_angle', (a, pa, b, pb), deg)     angle between the xy projections of pa->a and pb->b
      ('angle_to_outward', (a, site, n1, n2, n3), deg)  angle between site->a and the negative normalized sum of
                                                   the unit vectors site->n1, site->n2, site->n3
    """
    P = atoms.get_positions()
    ix = {k: n for n, k in enumerate(atoms.arrays['atom_id'])}
    at = lambda k: P[ix[k]]  # noqa: E731

    def angle(u, w):
        c = float(np.dot(u, w) / (np.linalg.norm(u) * np.linalg.norm(w)))
        return float(np.degrees(np.arccos(np.clip(c, -1.0, 1.0))))

    out = {}
    for kind, ids, declared in specs:
        if kind == 'distance':
            value, is_angle = float(np.linalg.norm(at(ids[1]) - at(ids[0]))), False
        elif kind == 'angle':
            value, is_angle = angle(at(ids[0]) - at(ids[1]), at(ids[2]) - at(ids[1])), True
        elif kind == 'z_difference':
            value, is_angle = float(at(ids[0])[2] - at(ids[1])[2]), False
        elif kind == 'xy_offset_from_midpoint':
            mid = (at(ids[1]) + at(ids[2])) / 2.0
            value, is_angle = float(np.linalg.norm((at(ids[0]) - mid)[:2])), False
        elif kind == 'projected_angle':
            value, is_angle = angle((at(ids[0]) - at(ids[1]))[:2], (at(ids[2]) - at(ids[3]))[:2]), True
        elif kind == 'angle_to_outward':
            site = at(ids[1])
            outward = -unit(sum(unit(at(n) - site) for n in ids[2:]))
            value, is_angle = angle(at(ids[0]) - site, outward), True
        else:
            raise ValueError(kind)
        tol = ANGLE_TOL if is_angle else DIST_TOL
        if declared is not None:
            assert abs(value - declared) <= tol, (kind, ids, value, declared)
        out[f"{kind} {' / '.join(ids)}"] = {
            'measured': round(value, 6), 'unit': 'deg' if is_angle else 'A',
            'declared': None if declared is None else round(float(declared), 6),
            'tolerance': tol if declared is not None else None}
    return out


def unit(v):
    return v / np.linalg.norm(v)


def rotation_between(a, b):
    """Proper rotation matrix taking unit vector a onto unit vector b (Rodrigues)."""
    a, b = unit(a), unit(b)
    v, c = np.cross(a, b), float(np.dot(a, b))
    if np.isclose(c, -1.0):
        axis = unit(np.cross(a, [1.0, 0.0, 0.0] if abs(a[0]) < 0.9 else [0.0, 1.0, 0.0]))
        return 2.0 * np.outer(axis, axis) - np.eye(3)
    k = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + k + k @ k / (1.0 + c)


def rotation_z(angle):
    ca, sa = np.cos(angle), np.sin(angle)
    return np.array([[ca, -sa, 0.0], [sa, ca, 0.0], [0.0, 0.0, 1.0]])


def build_m1():
    """H-capped H:Si(100)-2x1 cluster; returns atoms, the uncapped pair ids, their open cap directions and a log."""
    a = LATTICE_A
    d0 = a * np.sqrt(3.0) / 4.0          # bulk nearest-neighbour distance for this lattice constant
    s = a / np.sqrt(2.0)                  # (100) surface lattice spacing
    # Lattice patch: one virtual layer above and one below the cluster layers, generous lateral margins.
    patch = diamond100('Si', size=(DIMERS_PER_ROW + 8, 2 * DIMER_ROWS + 8, SI_LAYERS + 2), a=a, orthogonal=True)
    lat = patch.get_positions()
    zs = np.unique(np.round(lat[:, 2], 6))[::-1]           # descending; zs[0] is the virtual upper layer
    layer = np.array([int(np.argmin(abs(zs - z))) for z in lat[:, 2]])
    grid = np.rint(2.0 * lat[:, :2] / s).astype(int)      # half-spacing integer lattice coordinates
    dist = np.linalg.norm(lat[:, None, :] - lat[None, :, :], axis=2)
    nbr = [set(np.nonzero(np.isclose(row, d0, atol=1e-6))[0]) for row in dist]

    top = np.nonzero(layer == 1)[0]
    # Dimer axis: the in-plane direction from a top atom to its two missing upper neighbours.
    t0 = top[int(np.argmin(np.linalg.norm(lat[top, :2] - lat[top, :2].mean(axis=0), axis=1)))]  # interior atom
    ups = [j for j in nbr[t0] if layer[j] == 0]
    assert len(ups) == 2
    dimer_axis = int(np.argmax(abs(lat[ups[0], :2] - lat[ups[1], :2])))   # 0 = x, 1 = y
    row_axis = 1 - dimer_axis
    ge, gr = grid[top, dimer_axis], grid[top, row_axis]
    e0 = int(np.sort(np.unique(ge))[4])                   # start 4 spacings (2 surface cells) in from the edge
    r0 = int(np.sort(np.unique(gr))[4])
    sel_top = [i for i in top
               if 0 <= (grid[i, dimer_axis] - e0) // 2 < 2 * DIMER_ROWS and (grid[i, dimer_axis] - e0) % 2 == 0
               and 0 <= (grid[i, row_axis] - r0) // 2 < DIMERS_PER_ROW and (grid[i, row_axis] - r0) % 2 == 0]
    assert len(sel_top) == 2 * DIMER_ROWS * DIMERS_PER_ROW
    ke = {i: (grid[i, dimer_axis] - e0) // 2 for i in sel_top}   # 0 .. 2*rows-1 across the rows
    kr = {i: (grid[i, row_axis] - r0) // 2 for i in sel_top}     # 0 .. dimers-1 along a row
    # Lower layers: lattice sites inside the top box widened by half a surface spacing, then pruned so that every
    # silicon keeps at least two silicon neighbours.
    lo = lat[sel_top, :2].min(axis=0) - s / 2 - 1e-6
    hi = lat[sel_top, :2].max(axis=0) + s / 2 + 1e-6
    cluster = set(sel_top) | {i for i in range(len(lat)) if 2 <= layer[i] <= SI_LAYERS
                              and np.all(lat[i, :2] >= lo) and np.all(lat[i, :2] <= hi)}
    while True:
        drop = {i for i in cluster if layer[i] >= 2 and len(nbr[i] & cluster) < 2}
        if not drop:
            break
        cluster -= drop
    for i in sel_top:
        assert len([j for j in nbr[i] & cluster if layer[j] == 2]) == 2, 'top atom lost a second-layer neighbour'

    # Dimer construction: partners (2m, 2m+1) across each row move toward each other so that the dimer Si-Si distance
    # and both distances to second-layer neighbours equal d0; the lower layers stay on bulk lattice positions.
    delta = (s - d0) / 2.0
    dz = a / 4.0 - np.sqrt((a / 4.0) ** 2 - delta ** 2)
    pos = {i: lat[i].copy() for i in cluster}
    partner = {}
    for i in sel_top:
        sign = 1.0 if ke[i] % 2 == 0 else -1.0                # lower-index atom moves up the dimer axis
        pos[i][dimer_axis] += sign * delta
        pos[i][2] -= dz
        partner[i] = next(j for j in sel_top if kr[j] == kr[i] and ke[j] == ke[i] + int(sign))
    pair = [next(i for i in sel_top if kr[i] == PAIR_COLUMN and ke[i] == 2 * PAIR_ROWS[0] + 1),
            next(i for i in sel_top if kr[i] == PAIR_COLUMN and ke[i] == 2 * PAIR_ROWS[1])]

    # Stable identifiers from layer and half-spacing lattice coordinates, relative to the cluster's minima.
    gmin = grid[sorted(cluster)].min(axis=0)
    def sid(i):
        gx, gy = grid[i] - gmin
        return f'S-L{layer[i]}-{gx:02d}-{gy:02d}'

    si_order = sorted(cluster, key=lambda i: (layer[i], grid[i][1], grid[i][0]))
    symbols, positions, ids, roles = [], [], [], []
    edges = set()                         # constructed neighbour edges (lattice, dimer, cap); not computed bonds
    for i in si_order:
        symbols.append('Si'); positions.append(pos[i]); ids.append(sid(i))
        roles.append('M1-Si-3c-site' if i in pair else 'M1-Si-dimer' if layer[i] == 1 else 'M1-Si-sub')
    index = {i: n for n, i in enumerate(si_order)}
    for i in si_order:
        for j in nbr[i] & cluster:
            edges.add(tuple(sorted((index[i], index[j]))))
        if layer[i] == 1:
            edges.add(tuple(sorted((index[i], index[partner[i]]))))
    outward, site_nbrs = {}, {}
    for i in si_order:
        if layer[i] == 1:
            si_nbrs = [partner[i]] + [j for j in nbr[i] & cluster if layer[j] == 2]
            direction = -unit(sum(unit(pos[j] - pos[i]) for j in si_nbrs))    # tetrahedral completion
            if i in pair:
                outward[sid(i)] = direction    # nominal outward direction from the coordination geometry
                site_nbrs[sid(i)] = [sid(j) for j in si_nbrs]
                continue
            caps = [direction]
        else:
            caps = sorted((unit(lat[j] - lat[i]) for j in nbr[i] - cluster),
                          key=lambda v: tuple(np.round(v, 6)))
        for k, v in enumerate(caps, start=1):
            symbols.append('H'); positions.append(pos[i] + R_SIH * v); ids.append(f'{sid(i)}-H{k}')
            roles.append('M1-H-dimer' if layer[i] == 1 else 'M1-H-cap')
            edges.add((index[i], len(symbols) - 1))
    atoms = Atoms(symbols=symbols, positions=np.array(positions), pbc=False)
    atoms.new_array('atom_id', np.array(ids, dtype='U32'))
    atoms.new_array('role', np.array(roles, dtype='U16'))

    # Construction checks (bookkeeping on coordinates and constructed edges; no physics).
    P = atoms.get_positions()
    D = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)
    for p, q in edges:
        ref = d0 if symbols[p] == symbols[q] == 'Si' else R_SIH
        assert abs(D[p, q] - ref) < 1e-9, (ids[p], ids[q], D[p, q])
    coord = np.zeros(len(atoms), int)
    for p, q in edges:
        coord[p] += 1; coord[q] += 1
    for n, (el, r) in enumerate(zip(symbols, roles)):
        assert coord[n] == (1 if el == 'H' else 3 if r == 'M1-Si-3c-site' else 4), (ids[n], coord[n])
    info = {
        'declared_construction_parameters': {
            'lattice_constant_A': LATTICE_A, 'si_si_constructed_distance_A': d0, 'surface_spacing_A': s,
            'dimer_lateral_shift_A': delta, 'dimer_vertical_drop_A': dz,
            'si_si_constructed_distance_rule': 'a*sqrt(3)/4',
            'dimer_rule': 'dimer Si-Si distance and both second-layer distances set to the Si-Si constructed distance',
        },
        'dimer_axis': 'xy'[dimer_axis], 'row_axis': 'xy'[row_axis],
        'three_coordinate_site_ids': [sid(pair[0]), sid(pair[1])],
        'three_coordinate_site_neighbour_ids': site_nbrs,
        'three_coordinate_site_note': ('two Si sites left unterminated by construction (three constructed '
                                       'neighbours each); "dangling-bond pair" is only a nominal name for these '
                                       'sites, not an electronic-state, unpaired-electron or radical claim'),
        'nominal_outward_direction_rule': 'negative normalized sum of unit vectors to the three constructed neighbours',
        'counts': {'Si': symbols.count('Si'), 'H': symbols.count('H'), 'total': len(symbols),
                   'Si_by_layer': [int(sum(1 for i in cluster if layer[i] == L)) for L in range(1, SI_LAYERS + 1)],
                   'H_dimer': roles.count('M1-H-dimer'), 'H_cap': roles.count('M1-H-cap')},
        'constructed_coordination_checked': '3 at the two unterminated Si sites, 4 at every other Si, 1 at every H',
    }
    edge_list = sorted((ids[p], ids[q], d0 if symbols[p] == symbols[q] == 'Si' else R_SIH) for p, q in edges)
    declared_separation = s + 2.0 * delta
    declared_layer_spacing = a / 4.0 - dz
    return (atoms, [sid(pair[0]), sid(pair[1])], outward, info, edge_list,
            declared_separation, declared_layer_spacing)


def edges_on_output(atoms, edge_list):
    """Re-measure every constructed edge on read-back coordinates; assert each declared length within DIST_TOL."""
    P = atoms.get_positions()
    ix = {k: n for n, k in enumerate(atoms.arrays['atom_id'])}
    dev = max(abs(float(np.linalg.norm(P[ix[a]] - P[ix[b]])) - ref) for a, b, ref in edge_list)
    assert dev <= DIST_TOL, dev
    return {'constructed_edges_remeasured': len(edge_list), 'max_abs_deviation_from_declared_A': float(f'{dev:.3e}'),
            'tolerance_A': DIST_TOL}


def min_unjoined(atoms, edge_list, group_a=None, group_b=None, exclude=()):
    """Shortest measured distance between atoms not joined by a constructed edge; optional groups and exclusions."""
    P = atoms.get_positions()
    ids = list(atoms.arrays['atom_id'])
    sym = atoms.get_chemical_symbols()
    joined = {frozenset((a, b)) for a, b, _ in edge_list} | {frozenset(x) for x in exclude}
    ga = range(len(atoms)) if group_a is None else group_a
    gb = None if group_b is None else set(group_b)
    best = {}
    for p in ga:
        for q in (range(p + 1, len(atoms)) if gb is None else gb):
            if p == q or frozenset((ids[p], ids[q])) in joined:
                continue
            key = 'H-H' if sym[p] == sym[q] == 'H' else 'other'
            d = float(np.linalg.norm(P[p] - P[q]))
            if key not in best or d < best[key][0]:
                best[key] = (d, ids[p], ids[q])
    return {k: [round(v[0], 6), v[1], v[2]] for k, v in sorted(best.items())}


def load_m2():
    path = REPO / M2_FILE
    if sha256_file(path) != M2_SHA256:
        sys.exit(f'{M2_FILE}: SHA256 differs from the frozen digest')
    tool = read(str(path), format='extxyz')
    ids = list(tool.arrays['atom_id'])
    return tool, {k: n for n, k in enumerate(ids)}


def oriented_tool(tool, ix):
    """Rigidly rotate the tool: Ge1->Cb along -z, then the projection of Ge1->O1 onto the xy plane along +x."""
    P = tool.get_positions()
    ge = P[ix['D-Ge1']]
    R1 = rotation_between(P[ix['D-Cb']] - ge, np.array([0.0, 0.0, -1.0]))
    Q = (P - ge) @ R1.T
    o1 = Q[ix['D-O1']]
    R2 = rotation_z(-np.arctan2(o1[1], o1[0]))
    Q = Q @ R2.T
    before = np.linalg.norm(P[:, None] - P[None], axis=2)
    after = np.linalg.norm(Q[:, None] - Q[None], axis=2)
    assert np.max(abs(before - after)) < 1e-10, 'rotation changed an interatomic distance'
    return Q


def combined(m1, tool, tool_pos, role_info):
    atoms = m1.copy()
    t = Atoms(symbols=tool.get_chemical_symbols(), positions=tool_pos, pbc=False)
    t.new_array('atom_id', np.array(tool.arrays['atom_id'], dtype='U32'))
    t.new_array('role', np.array(['M2-tool'] * len(t), dtype='U16'))
    atoms += t
    atoms.info.update(role_info)
    return atoms


def build_p2(tool, ix):
    """H3Ge-C-C-SiH3 geometry: Ge, two C and Si collinear on z, H placed tetrahedrally, SiH3 staggered against GeH3.

    The Ge-C and C-C distances are copied from D-Ge1/D-Ca/D-Cb of the frozen tool file; no bond order is implied.
    Returns the atoms and the measurement specs whose declared values are asserted on the written file."""
    P = tool.get_positions()
    r_gec = float(np.linalg.norm(P[ix['D-Ca']] - P[ix['D-Ge1']]))
    r_cc = float(np.linalg.norm(P[ix['D-Cb']] - P[ix['D-Ca']]))
    z_ca, z_cb = r_gec, r_gec + r_cc
    z_si = z_cb + R_SIC
    theta = np.arccos(-1.0 / 3.0)                            # polar angle of each H direction from the +z axis
    symbols = ['Ge', 'C', 'C', 'Si']
    positions = [[0.0, 0.0, 0.0], [0.0, 0.0, z_ca], [0.0, 0.0, z_cb], [0.0, 0.0, z_si]]
    ids = ['P2-Ge1', 'P2-Ca', 'P2-Cb', 'P2-Si1']
    for k in range(3):                                       # H on Ge, on the side away from the C2 unit
        phi = 2.0 * np.pi * k / 3.0
        v = [np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)]
        symbols.append('H'); positions.append(list(R_GEH * np.array(v))); ids.append(f'P2-Ge1-H{k + 1}')
    for k in range(3):                                       # H on Si, azimuth offset by 60 degrees (staggered)
        phi = 2.0 * np.pi * k / 3.0 + np.pi / 3.0
        v = [np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), -np.cos(theta)]
        symbols.append('H'); positions.append(list(np.array([0.0, 0.0, z_si]) + R_SIH * np.array(v)))
        ids.append(f'P2-Si1-H{k + 1}')
    atoms = Atoms(symbols=symbols, positions=np.array(positions), pbc=False)
    atoms.new_array('atom_id', np.array(ids, dtype='U32'))
    atoms.new_array('role', np.array(['P2-molecule'] * len(atoms), dtype='U16'))
    specs = [('distance', ('P2-Ge1', 'P2-Ca'), r_gec), ('distance', ('P2-Ca', 'P2-Cb'), r_cc),
             ('distance', ('P2-Cb', 'P2-Si1'), R_SIC),
             ('angle', ('P2-Ge1', 'P2-Ca', 'P2-Cb'), 180.0), ('angle', ('P2-Ca', 'P2-Cb', 'P2-Si1'), 180.0)]
    for k in (1, 2, 3):
        specs += [('distance', ('P2-Ge1', f'P2-Ge1-H{k}'), R_GEH),
                  ('angle', (f'P2-Ge1-H{k}', 'P2-Ge1', 'P2-Ca'), TETRAHEDRAL_DEG),
                  ('distance', ('P2-Si1', f'P2-Si1-H{k}'), R_SIH),
                  ('angle', (f'P2-Si1-H{k}', 'P2-Si1', 'P2-Cb'), TETRAHEDRAL_DEG),
                  ('projected_angle', (f'P2-Ge1-H{k}', 'P2-Ge1', f'P2-Si1-H{k}', 'P2-Si1'), 60.0)]
    return atoms, specs


def header(role, extra):
    info = {
        'model_role': role, 'origin': 'agent-proposed/geometric-construction', 'evidence_class': 'AGENT',
        'optimization': CONSTRUCTION, 'not_computed': NOT_COMPUTED, 'stability_claim': 'none', 'units': 'Angstrom',
        'benchmark_relation': BENCHMARK_RELATION,
        'charge_multiplicity': 'not assigned here; no electronic-state claim; assignment deferred to B2',
        'generator': GENERATOR, 'generator_sha256': sha256_file(REPO / GENERATOR),
        'ase_version': ase.__version__, 'numpy_version': np.__version__,
    }
    info.update(extra)
    return info


def electron_bookkeeping(atoms):
    """Composition and neutral-atom electron count; bookkeeping on file contents only."""
    symbols = atoms.get_chemical_symbols()
    count = int(sum(atomic_numbers[el] for el in symbols))
    return {'composition': {el: symbols.count(el) for el in sorted(set(symbols))},
            'all_electron_count_neutral_atoms': count, 'all_electron_count_parity': 'even' if count % 2 == 0 else 'odd',
            'note': 'bookkeeping only; charge and spin not assigned here; no electronic-state claim; deferred to B2'}


def emit(atoms, path):
    """Write one extxyz file and return it as read back; checks identity, periodicity and header labels."""
    if path.name in PROTECTED:
        sys.exit(f'refusing to overwrite protected file {path.name}')
    write(str(path), atoms, format='extxyz', columns=['symbols', 'positions', 'atom_id', 'role'])
    back = read(str(path), format='extxyz')
    assert list(back.arrays['atom_id']) == list(atoms.arrays['atom_id'])
    assert list(back.arrays['role']) == list(atoms.arrays['role'])
    assert np.allclose(back.get_positions(), atoms.get_positions(), atol=5e-8, rtol=0)
    assert not any(back.pbc)
    assert back.info['evidence_class'] == 'AGENT' and back.info['not_computed'] == NOT_COMPUTED
    assert back.info['generator_sha256'] == sha256_file(REPO / GENERATOR)
    return back


def tool_rigidity(back, tool, n1):
    """Largest change of any tool-internal distance between the written file and the frozen M2 file."""
    T = back.get_positions()[n1:]
    R = tool.get_positions()
    dev = float(np.max(abs(np.linalg.norm(T[:, None] - T[None], axis=2) - np.linalg.norm(R[:, None] - R[None], axis=2))))
    assert dev <= DIST_TOL, dev
    return {'tool_internal_distances_max_abs_change_from_M2_A': float(f'{dev:.3e}'), 'tolerance_A': DIST_TOL}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--outdir', default=str(REPO / 'structures' / 'ms-001'))
    args = ap.parse_args()
    out = Path(args.outdir).resolve()
    if out == (REPO / 'structures').resolve():
        sys.exit('refusing to write into structures/ itself; the existing files there are protected')
    out.mkdir(parents=True, exist_ok=True)

    assert reference_states[atomic_numbers['Si']]['a'] == LATTICE_A
    assert (COVALENT['H'], COVALENT['C'], COVALENT['Si'], COVALENT['Ge']) == (0.31, 0.76, 1.11, 1.20)

    m1, pair_ids, outward, m1_info, edge_list, decl_sep, decl_layer = build_m1()
    s1, s2 = pair_ids
    nbrs1 = m1_info['three_coordinate_site_neighbour_ids'][s1]
    nbrs2 = m1_info['three_coordinate_site_neighbour_ids'][s2]
    tool, ix = load_m2()
    n1 = len(m1)
    m1_ids = list(m1.arrays['atom_id'])
    pair_idx = [m1_ids.index(k) for k in pair_ids]
    P1 = m1.get_positions()
    z_pair = float(P1[pair_idx[0], 2])
    assert abs(P1[pair_idx[1], 2] - z_pair) < 1e-12
    mid = (P1[pair_idx[0]] + P1[pair_idx[1]]) / 2.0

    Q = oriented_tool(tool, ix)
    cb = ix['D-Cb']
    start_pos = Q + (np.array([mid[0], mid[1], z_pair + START_HEIGHT]) - Q[cb])
    v2_target = P1[pair_idx[0]] + R_SIC * outward[s1]
    v2_pos = start_pos + (v2_target - start_pos[cb])
    v3_pos = v2_pos.copy()
    c2 = [ix['D-Ca'], ix['D-Cb']]
    rest = [n for n in range(len(tool)) if n not in c2]
    v3_pos[rest] += np.array([0.0, 0.0, V3_LIFT])

    m1_idx = list(range(n1))
    tool_idx = list(range(n1, n1 + len(tool)))
    rest_idx = [n1 + n for n in rest]
    c2_idx = [n1 + n for n in c2]
    placement = {
        'tool_orientation': 'D-Ge1->D-Cb along -z; projection of D-Ge1->D-O1 on xy along +x',
        'start_Cb_lateral': 'midpoint of the two three-coordinate Si sites',
        'start_Cb_height_A': START_HEIGHT,
    }
    site_ids = ','.join(pair_ids)
    tool_keys = {'m2_source': M2_FILE, 'm2_source_sha256': M2_SHA256,
                 'm2_reuse': 'read by digest, not regenerated', 'three_coordinate_site_ids': site_ids}
    records = {}

    def record(name, back, derived):
        records[name] = {
            'role': back.info['model_role'], 'c7_role': back.info.get('c7_role', 'not a C7 configuration'),
            'atoms': len(back), 'electron_bookkeeping': electron_bookkeeping(back),
            'derived_measured_on_written_file': derived, 'sha256': sha256_file(out / name),
            'evidence_class': 'AGENT', 'not_computed': NOT_COMPUTED,
        }

    # M1
    m1.info.update(header('M1 build site (B1)', {
        'model': ('H:Si(100)-2x1 finite cluster, H-terminated except two Si sites left three-coordinate and '
                  'unterminated by construction'),
        'three_coordinate_site_ids': site_ids,
        'site_name_note': ('"inter-row dangling-bond pair" is only a nominal name for these two sites; no '
                           'electronic-state, unpaired-electron or radical claim')}))
    m1b = emit(m1, out / 'M1-build-site.extxyz')
    sym, roles = m1b.get_chemical_symbols(), list(m1b.arrays['role'])
    counts = {'Si': sym.count('Si'), 'H': sym.count('H'), 'total': len(sym),
              'H_dimer': roles.count('M1-H-dimer'), 'H_cap': roles.count('M1-H-cap')}
    assert all(counts[k] == m1_info['counts'][k] for k in counts)
    Pb, ixb = m1b.get_positions(), {k: n for n, k in enumerate(m1b.arrays['atom_id'])}
    outward_out = {s: [round(float(x), 6) for x in -unit(sum(unit(Pb[ixb[n]] - Pb[ixb[s]]) for n in nb))]
                   for s, nb in ((s1, nbrs1), (s2, nbrs2))}
    for s in (s1, s2):
        assert np.allclose(outward_out[s], outward[s], atol=1e-6)
    record('M1-build-site.extxyz', m1b, {
        'measurements': measure(m1b, [('distance', (s1, s2), decl_sep),
                                      ('z_difference', (s1, nbrs1[1]), decl_layer),
                                      ('z_difference', (s2, nbrs2[1]), decl_layer)]),
        'constructed_edges': edges_on_output(m1b, edge_list),
        'counts_on_output': counts,
        'nominal_outward_directions_on_output': outward_out,
        'min_distance_not_joined_by_constructed_edge_A': min_unjoined(m1b, edge_list),
    })

    # start and V1
    decl_cb_site = float(np.hypot(START_HEIGHT, decl_sep / 2.0))
    start_specs = [('distance', ('D-Cb', s1), decl_cb_site), ('distance', ('D-Cb', s2), decl_cb_site),
                   ('z_difference', ('D-Cb', s1), START_HEIGHT), ('xy_offset_from_midpoint', ('D-Cb', s1, s2), 0.0)]
    start = combined(m1, tool, start_pos, header('start of the approach branch (combined M1 + M2)', {
        **tool_keys, 'tool_file_note': 'M2 tool file as published; contains no iodine atom', **placement}))
    startb = emit(start, out / 'start-combined.extxyz')
    start_derived = {
        'measurements': measure(startb, start_specs),
        'min_distance_M1_to_tool_A': min_unjoined(startb, [], m1_idx, tool_idx),
        'tool_rigidity': tool_rigidity(startb, tool, n1),
    }
    record('start-combined.extxyz', startb, start_derived)

    v1 = combined(m1, tool, start_pos, header('C7 validation configuration V1', {
        **tool_keys, 'c7_role': 'V1, nominal name "separated bodies"', 'filename_note': FILENAME_NOTE,
        'construction_rule': 'identical coordinates to the start of the approach branch', **placement}))
    v1b = emit(v1, out / 'V1-separated-bodies.extxyz')
    assert np.array_equal(v1b.get_positions(), startb.get_positions())
    record('V1-separated-bodies.extxyz', v1b, {
        'measurements': measure(v1b, start_specs),
        'coordinates_identical_to_start_file': True,
        'min_distance_M1_to_tool_A': min_unjoined(v1b, [], m1_idx, tool_idx),
        'tool_rigidity': tool_rigidity(v1b, tool, n1),
    })

    # V2
    r_gec_m2 = float(np.linalg.norm(tool.get_positions()[ix['D-Ca']] - tool.get_positions()[ix['D-Ge1']]))
    v2 = combined(m1, tool, v2_pos, header('C7 validation configuration V2', {
        **tool_keys, 'c7_role': 'V2, nominal name "contact, Ge-C intact"', 'filename_note': FILENAME_NOTE,
        'construction_rule': ('geometric construction: the start tool rigidly translated so that D-Cb lies at the '
                              f'declared contact distance from {s1} along its nominal outward direction; '
                              'D-Ge1 to D-Ca stays at its constructed M2 distance; no claim that any bond is '
                              'intact or formed'),
        'declared_contact_distance_A': round(R_SIC, 6),
        'declared_contact_distance_basis': 'Si + C covalent radii, ase.data.covalent_radii (ASE 3.29.0)'}))
    v2b = emit(v2, out / 'V2-contact-GeC-intact.extxyz')
    assert np.array_equal(v2b.get_positions()[:n1], m1b.get_positions())
    cb_n = n1 + cb
    record('V2-contact-GeC-intact.extxyz', v2b, {
        'measurements': measure(v2b, [('distance', ('D-Cb', s1), R_SIC),
                                      ('angle_to_outward', ('D-Cb', s1, *nbrs1), 0.0),
                                      ('distance', ('D-Ge1', 'D-Ca'), r_gec_m2),
                                      ('distance', ('D-Cb', s2), None)]),
        'lateral_shift_of_D-Cb_from_start_file_A': round(float(np.linalg.norm(
            (v2b.get_positions()[cb_n] - startb.get_positions()[cb_n])[:2])), 6),
        'M1_block_identical_to_M1_file': True,
        'min_distance_M1_to_tool_excluding_declared_contact_A':
            min_unjoined(v2b, [], m1_idx, tool_idx, exclude={(s1, 'D-Cb')}),
        'tool_rigidity': tool_rigidity(v2b, tool, n1),
    })

    # V3
    v3 = combined(m1, tool, v3_pos, header('C7 validation configuration V3', {
        **tool_keys, 'c7_role': 'V3, nominal name "pendent C2 with Ge-C broken"', 'filename_note': FILENAME_NOTE,
        'construction_rule': ('geometric construction: V2 with D-Ca and D-Cb kept in place and the other 46 tool '
                              f'atoms rigidly translated by the declared vector (0, 0, +{V3_LIFT:.2f}) A; no claim '
                              'that any bond is broken or cleaved'),
        'kept_in_place_atom_ids': 'D-Ca,D-Cb',
        'declared_translation_A': f'0 0 {V3_LIFT:.2f}'}))
    v3b = emit(v3, out / 'V3-pendent-C2-GeC-broken.extxyz')
    P2b, P3b = v2b.get_positions(), v3b.get_positions()
    assert np.array_equal(P3b[:n1], m1b.get_positions()) and np.array_equal(P3b[c2_idx], P2b[c2_idx])
    shift_dev = float(np.max(abs(P3b[rest_idx] - P2b[rest_idx] - np.array([0.0, 0.0, V3_LIFT]))))
    assert len(rest_idx) == 46 and shift_dev <= DIST_TOL, shift_dev
    ge_n, ca_n = n1 + ix['D-Ge1'], n1 + ix['D-Ca']
    decl_v3_gec = float(np.linalg.norm(P2b[ca_n] - (P2b[ge_n] + np.array([0.0, 0.0, V3_LIFT]))))
    v3_meas = measure(v3b, [('distance', ('D-Cb', s1), R_SIC), ('distance', ('D-Ge1', 'D-Ca'), decl_v3_gec)])
    record('V3-pendent-C2-GeC-broken.extxyz', v3b, {
        'measurements': v3_meas,
        'D-Ge1_D-Ca_over_Ge_plus_C_covalent_radii': round(
            v3_meas['distance D-Ge1 / D-Ca']['measured'] / (COVALENT['Ge'] + COVALENT['C']), 6),
        'translated_atoms': {'count': len(rest_idx), 'max_abs_deviation_from_declared_vector_A':
                             float(f'{shift_dev:.3e}'), 'tolerance_A': DIST_TOL},
        'kept_atoms_identical_to_V2_file': True, 'M1_block_identical_to_M1_file': True,
        'min_distance_translated_atoms_to_M1_or_kept_atoms_A':
            min_unjoined(v3b, [], rest_idx, m1_idx + c2_idx, exclude={('D-Ge1', 'D-Ca')}),
    })

    # P2
    p2, p2_specs = build_p2(tool, ix)
    p2_book = electron_bookkeeping(p2)
    p2.info.update(header('C7 P2 cross-engine test molecule', {
        'c7_role': 'P2 test molecule',
        'molecule': 'H3Ge-C-C-SiH3 geometry (Ge, two C and Si collinear)',
        'electron_bookkeeping': (f"composition C2 H6 Ge Si; all-electron count of the neutral atoms "
                                 f"{p2_book['all_electron_count_neutral_atoms']}, parity "
                                 f"{p2_book['all_electron_count_parity']}; bookkeeping only"),
        'construction_rule': ('Ge, C, C, Si collinear on z; each H at the ideal tetrahedral angle to the bonded C '
                              'direction; SiH3 staggered against GeH3')}))
    p2b = emit(p2, out / 'P2-test-molecule-H3GeCCSiH3.extxyz')
    record('P2-test-molecule-H3GeCCSiH3.extxyz', p2b, {'measurements': measure(p2b, p2_specs)})

    rec = {
        'evidence_class': 'AGENT',
        'statement': ('Geometric constructions only. No relaxation, optimization, energy, force or gradient '
                      'evaluation of any kind. ' + BENCHMARK_RELATION + '. Electron counts are bookkeeping on '
                      'file contents, not electronic-structure results; charge and spin are not assigned here.'),
        'not_computed': NOT_COMPUTED,
        'measurement_basis': MEASUREMENT_BASIS,
        'tolerances': {'distance_A': DIST_TOL, 'angle_deg': ANGLE_TOL, 'ideal_tetrahedral_angle_deg': TETRAHEDRAL_DEG},
        'filename_note': FILENAME_NOTE,
        'c7_role_mapping': {'V1': 'V1-separated-bodies.extxyz', 'V2': 'V2-contact-GeC-intact.extxyz',
                            'V3': 'V3-pendent-C2-GeC-broken.extxyz', 'P2': 'P2-test-molecule-H3GeCCSiH3.extxyz'},
        'generator': GENERATOR, 'generator_sha256': sha256_file(REPO / GENERATOR),
        'software': {'ase': ase.__version__, 'numpy': np.__version__, 'python': sys.version.split()[0]},
        'm2': {'file': M2_FILE, 'sha256': M2_SHA256, 'reused': 'read by digest, not regenerated'},
        'parameters': {
            'lattice_constant_A': LATTICE_A, 'lattice_constant_basis': 'ase.data.reference_states[Si] in ASE 3.29.0',
            'covalent_radii_A': COVALENT, 'covalent_radii_basis': 'ase.data.covalent_radii in ASE 3.29.0 (Cordero et al. 2008)',
            'Si_H_cap_distance_A': R_SIH, 'declared_contact_distance_Si_C_A': R_SIC, 'Ge_H_distance_A': R_GEH,
            'dimers_per_row': DIMERS_PER_ROW, 'dimer_rows': DIMER_ROWS, 'si_layers': SI_LAYERS,
            'pair_rows': list(PAIR_ROWS), 'pair_column': PAIR_COLUMN,
            'start_Cb_height_A': START_HEIGHT, 'v3_lift_A': V3_LIFT, **placement,
        },
        'm1_construction': m1_info,
        'files': records,
    }
    (out / 'geometry-record.json').write_text(json.dumps(rec, indent=2, sort_keys=True) + '\n')
    for name, r in records.items():
        print(f"{r['sha256']}  {name}  atoms={r['atoms']}")
    print(f"{sha256_file(out / 'geometry-record.json')}  geometry-record.json")
    return 0


if __name__ == '__main__':
    sys.exit(main())
