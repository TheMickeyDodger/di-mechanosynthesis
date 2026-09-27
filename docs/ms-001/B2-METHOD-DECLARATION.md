# B2 two-level method declaration

Status: MS-001 Stage 0, scope option B. Every setting below is an `[AGENT]` declared deviation, chosen by this
project because the benchmark states no partition, embedding, link treatment, charge, spin, basis, core treatment
or numerical settings (spike §2.9, P2 and P3).

- **Not a reproduction.** Parity with the benchmark is unknown for every item (B4), and nothing here is a
  reproduction of the benchmark setup.
- **Electronic states are declared, not claimed.** Charge and multiplicity are declared electronic states to be
  computed. They are not claims about any ground state.
- **Sources.** Every value is cited to version-matched documentation or source `[S0-…]`, listed in
  [SOURCE-LEDGER.md](SOURCE-LEDGER.md). A value that cannot be established from those sources is marked
  `UNVERIFIED` or `[GAP]`.

The two levels are composed by the route declared in [C2](C2-COUPLING-ROUTE.md): CP2K 2026.2 `MIXED` with
E = E1 − E2 + E3.

## 1. Configurations covered

The declaration applies to the frozen files of [structures/ms-001](../../structures/ms-001/README.md):
- the start configuration and V1 to V3, which have 409 atoms each;
- P2, the 10-atom test molecule (Section 6).

M1 alone is an input to the combined files and is not computed by itself.

## 2. Partition, embedding and cut bonds

| Item | Declaration |
|---|---|
| High-level region S (18 atoms) | Tool: `D-Ge1`, `D-Ca`, `D-Cb`, `D-C2`, `D-C8`, `D-C9`, `D-C2-H1`, `D-C2-H2`, `D-C8-H1`, `D-C8-H2`, `D-C9-H1`, `D-C9-H2`. Build site: `S-L1-07-05` and `S-L1-09-05` (the two three-coordinate sites), their dimer partners `S-L1-05-05` and `S-L1-11-05`, and the partners' caps `S-L1-05-05-H1` and `S-L1-11-05-H1`. Composition: Ge 1, C 5, Si 4, H 8 |
| Low-level region | The full system, all 409 atoms, as sub-force_eval E3 |
| Region membership | By `atom_id`, which is identical in every combined file. It does not change along a scan |
| Embedding | Mechanical subtractive only (C2 §4) |
| Cut bonds (11) | `D-C2`–`D-C3`, `D-C8`–`D-C7`, `D-C9`–`D-C5` (C–C); `S-L1-05-05`–`S-L2-05-04`, `S-L1-05-05`–`S-L2-05-06`, `S-L1-07-05`–`S-L2-07-04`, `S-L1-07-05`–`S-L2-07-06`, `S-L1-09-05`–`S-L2-09-04`, `S-L1-09-05`–`S-L2-09-06`, `S-L1-11-05`–`S-L2-11-04`, `S-L1-11-05`–`S-L2-11-06` (Si–Si). The host is named first |
| Link atoms | One H per cut bond in E1 and E2, 11 in all, placed and force-mapped as in C2 §4 (g = 0.7039 for C–C and 0.6396 for Si–Si) |
| Charge | 0 for the full system, for S+L and for P2. This is also the CP2K default `DFT/CHARGE 0` [S0-cp2k-dft]; it is declared explicitly |
| Multiplicity and spin treatment | Full system (2977 electrons, odd) and S+L (137 electrons, odd): multiplicity 2, unrestricted (`DFT/UKS`, `DFT/MULTIPLICITY 2`) [S0-cp2k-dft]. P2 (64 electrons): multiplicity 1, restricted. CP2K's own default (1 for an even electron count and 2 for an odd one [S0-cp2k-dft]) is not relied on; every value is declared explicitly |
| Spin alternative for diagnostics | Multiplicity 4 for the full system and S+L. It is used only by the failed-reproduction diagnostic that the spike's §8.8 lists first. It is not a production state |

The electron counts are bookkeeping on file contents. Whether CP2K's GFN0-xTB accepts `UKS` and `MULTIPLICITY` is
`UNVERIFIED` (C2 §5, item 4).

## 3. GFN0-xTB level (sub-force_evals E2 and E3)

| Item | Declaration and source |
|---|---|
| Engine | CP2K 2026.2 |
| Selector as passed | `FORCE_EVAL/DFT/QS/METHOD XTB` [S0-cp2k-qs] and `FORCE_EVAL/DFT/QS/XTB/GFN_TYPE 0`. The documented values are `0`, `1` and `TBLITE`, with default `1`; `0` is "the CP2K-internal GFN0-xTB implementation" [S0-cp2k-xtb]. The input file that carries this line is hashed into every run record (C3 F2) |
| SCC mixing | The manual states that GFN0 has no SCC variables to mix, so `SCC_MIXER AUTO` is treated as `NONE` [S0-cp2k-xtb]. The default is kept |
| Other XTB keywords | Documented defaults: `CHECK_ATOMIC_CHARGES T`, `COULOMB_INTERACTION T`, `DO_EWALD F`, `DO_NONBONDED F`, `EPS_PAIRPOTENTIAL 1.0e-10` [S0-cp2k-xtb]. The run record enumerates every other default as printed by the engine (C3 F2) |
| Non-periodic treatment | As Section 5 |
| Parameter provenance (P1) | Each GFN0 run record must carry: the selector line as passed; CP2K's printed banner and version; the output line that names the method actually used; and the parameter provenance. The XTB manual page documents no GFN0 parameter file or parameter identifier for the internal implementation [S0-cp2k-xtb], so parameter provenance through CP2K is **`[GAP]` (closure gap G4)**. It must be closed from version-matched CP2K source (the file and revision that hold the GFN0 parameters, with its digest) before Stage 1b records P1. Until then P1 records the field as missing, and C5 is unmet |
| Silent-fallback rule | A run whose output does not identify GFN0 as the method is a correctness failure (spike §4, P1). It is never a result |

## 4. ωB97X-D3 level (sub-force_eval E1)

| Item | Declaration and source |
|---|---|
| Engine and method | CP2K 2026.2, `DFT/QS/METHOD GAPW` (all-electron capable) [S0-cp2k-qs]. Each kind uses `POTENTIAL ALL`, "for all-electron calculations" [S0-cp2k-kind] |
| Semilocal part | Libxc `HYB_GGA_XC_WB97X_D3` [S0-cp2k-xc]. Its documented parameter defaults are `_ALPHA` 1.0 ("fraction of HF exchange"), `_BETA` −0.804272 ("fraction of short-range exchange") and `_OMEGA` 0.25 ("range-separation constant") [S0-cp2k-xc]. They agree with the libxc 7.0.0 source definition, 1.0, −(1.0 − 0.195728), 0.25 [S0-libxc-wb97, line 80]. The libxc version linked into a given CP2K 2026.2 build is build-dependent and is recorded in the run record; which version will be used is `[GAP]` until then |
| Exact exchange | `XC/HF/FRACTION 1.0`. The manual states that in a mixed-potential calculation this should be 1.0 [S0-cp2k-hf]. `HF/INTERACTION_POTENTIAL`: `POTENTIAL_TYPE MIX_CL` (1/r + erf(ωr)/r, each part scalable), `OMEGA 0.25`, `SCALE_COULOMB 0.195728` and `SCALE_LONGRANGE 0.804272` [S0-cp2k-hf-ip]. The two scale factors are derived by this project `[AGENT]`, reading the libxc parameters as exact exchange = α·(1/r) + β·erfc(ωr)/r. Because erfc = 1 − erf, that equals (α + β)/r − β·erf(ωr)/r. Whether this reading reproduces the published functional is `UNVERIFIED`: the defining reference (Lin et al., doi:10.1021/ct300715s) was not obtained (HTTP 403) `[GAP]`, and CP2K's unit for `OMEGA` is not stated on the page (libxc's ω is in bohr⁻¹) |
| Exchange screening | `HF/SCREENING/EPS_SCHWARZ 1.0e-10` and `EPS_SCHWARZ_FORCES 1.0e-6`, the documented defaults [S0-cp2k-hf-screening] |
| Dispersion form | `XC/VDW_POTENTIAL/PAIR_POTENTIAL`, `TYPE DFTD3` (zero damping, two-body): `D3_SCALING 1.0 1.281 1.0` (s6, sr6, s8) [S0-cp2k-vdw-pair]; `CALCULATE_C9_TERM F` (the documented default, declared explicitly); `R_CUTOFF 25.0` Å (default 10.58 Å; the manual states that the cutoff is twice this value); `EPS_CN 1.0e-6` (default); `PARAMETER_FILE_NAME dftd3.dat` (CP2K data, 2026.2 branch) |
| Fixed D3 parameters | CP2K 2026.2 sets α6 = 14 [S0-cp2k-src-disp-pairpot, line 266], sets α8 = α6 + 2 [S0-cp2k-src-disp-d3, line 182], and **hard-codes sr8 = 1.0** [S0-cp2k-src-disp-d3, line 187] |
| Declared dispersion deviation | simple-dftd3 v1.6.0 tabulates the ωB97X-D3 zero-damping parameters as rs6 = 1.281, s8 = 1.0 and rs8 = 1.094, on defaults s6 = 1.0 and α = 14, citing doi:10.1021/ct300715s [S0-sdftd3-params]. The project's Psi4 1.11 run of E-01 printed sr8 = 1.094 (SOURCES [22]). CP2K cannot set sr8, so this level uses **sr8 = 1.0: a declared `[AGENT]` deviation from the tabulated ωB97X-D3 parametrization**. The P2 check uses the same sr8 = 1.0 in both engines (Section 6) |
| Basis and core, per element | See Section 7 |
| Numerical settings (production rung) | `MGRID/CUTOFF 600` Ry and `REL_CUTOFF 60` Ry (declared; defaults are 280 and 40 Ry [S0-cp2k-mgrid]); `NGRIDS 4` (default); `QS/EPS_DEFAULT 1.0e-10` (default [S0-cp2k-qs]); `KIND/LEBEDEV_GRID 50` and `RADIAL_GRID 50` (defaults [S0-cp2k-kind]); `SCF/EPS_SCF 1.0e-5` (default [S0-cp2k-scf]; a stopping criterion, not an accuracy bound); `SCF/MAX_SCF 200` (declared; default 50 [S0-cp2k-scf]; an iteration limit only); `SCF/SCF_GUESS ATOMIC` (default) for the first configuration of a branch, then restart from the previous accepted step (B3). The tighter rungs are in C4 N1 |
| SCF algorithm (E1) | Diagonalization: `SCF/DIAGONALIZATION` switched on explicitly with `ALGORITHM STANDARD`, which is the documented default; the section itself is off unless requested [S0-cp2k-scf-diag]. `SCF/MIXING` on with `METHOD DIRECT_P_MIXING` and `ALPHA 0.4`, the documented defaults, set explicitly [S0-cp2k-scf-mixing]. The `SCF/OT` section is not used; it is off by default [S0-cp2k-scf-ot]. `ADDED_MOS 0` (default) and no `SMEAR` section [S0-cp2k-scf]. These are frozen and not discovered from the run |
| Effective energy and gradient controls (E1) | Energies and forces come from the same converged SCF. The controls that govern both are set explicitly at the production rung: `EPS_SCF 1.0e-5`, `EPS_DEFAULT 1.0e-10`, `EPS_SCHWARZ 1.0e-10` and `EPS_SCHWARZ_FORCES 1.0e-6` (the screening threshold applied to exchange forces). The CP2K 2026.2 pages retrieved document no automatic tightening of these for force evaluations, so the declared values are the effective ones. Whether an undocumented override exists is `UNVERIFIED` and is checked against the printed input echo of the first Stage 1 run |
| Auxiliary basis (E1) | No auxiliary or fitting basis is declared for the converged E1 energy and forces. Exact four-centre exchange is used: the optional `HF/RI` subsection [S0-cp2k-hf] and the optional `DFT/AUXILIARY_DENSITY_MATRIX_METHOD` and `DFT/DENSITY_FITTING` subsections [S0-cp2k-dft] are not included. The initial-guess generators used by the repeats of C4 N3 affect only the starting wavefunction. `EHT` is documented as using "the EHT (gfn0-xTB) code" [S0-cp2k-scf]. Whether `ATOMIC` or `EHT` build any internal basis of their own is not established |

## 5. Non-periodic treatment (all three sub-force_evals)

| Item | Declaration and source |
|---|---|
| Periodicity | `SUBSYS/CELL/PERIODIC NONE` and `DFT/POISSON/PERIODIC NONE` [S0-cp2k-poisson] |
| Poisson solver | `POISSON_SOLVER WAVELET`. It "allows for 0D … systems" and "does not require very large unit cells, only that the density goes to zero on the faces of the cell". It requires `PREFERRED_FFT_LIBRARY FFTSG` [S0-cp2k-poisson] |
| Cell | Orthorhombic, the bounding box of the configuration plus 8.0 Å on every side (declared). The same cell is used by all three sub-force_evals of a given configuration |

## 6. Second implementation for the P2 check

P2 requires a second implementation of ωB97X-D3 (spike §8.3 C5). The declared second engine is **Psi4 1.11**, the
build installed for E-01 (SOURCES [20]). The model chemistry is held identical to Section 4, as N2 requires.

| Item | Declaration and source |
|---|---|
| Functional | A custom functional dictionary, `{"name": …, "xc_functionals": {"HYB_GGA_XC_WB97X_D3": {}}, "dispersion": {"type": "d3zero2b", "params": {"s6": 1.0, "s8": 1.0, "sr6": 1.281, "sr8": 1.0, "alpha6": 14.0}}}`, following the dictionary format of Psi4 v1.11 `hyb_functionals.py` [S0-psi4-hyb-funcs]. Psi4 v1.11 defines no `wB97X-D3` entry in that file; the name-based route through Psi4's built-in functional table is not used, because its parameters carry sr8 = 1.094 (SOURCES [22]). |
| Dispersion-input contract | Established from version-matched source. (1) Psi4 v1.11 `dft_builder.py` accepts a custom functional's `dispersion` only if its `type` is a known alias and the sorted keys of `params` equal the keys of qcengine's `dashcoeff[type]["default"]` [S0-psi4-dft-builder, lines 235–243]. (2) In qcengine 0.51.0, whose file is byte-identical to the one installed with the project's Psi4 build (SHA256 `aedefaff…`, recorded in `results/e01/method-config.json`), those keys for `d3zero2b` are `s6`, `s8`, `sr6`, `alpha6` and `sr8` [S0-qcng-disp-resources, line 69]. The declared `params` match them exactly. (3) qcengine routes every `…2b` level to s-dftd3 with `s9 = 0.0`, so the three-body term is off [S0-qcng-dftd-ng, lines 299–302; installed file byte-identical, `b90f3534…`]. (4) s-dftd3 v1.6.0 passes the tweaks to `ZeroDampingParam`, which renames `sr6`→`rs6`, `sr8`→`rs8` and `alpha6`→`alp` [S0-sdftd3-qcschema, lines 315–318; S0-sdftd3-interface, lines 257–286]. The dictionary therefore reaches the dispersion library as s6 1.0, s8 1.0, rs6 1.281, rs8 1.0, alp 14 and s9 0. The s-dftd3 files were read at the v1.6.0 tag and were not byte-compared with the installed package. How s-dftd3 forms the r⁻⁸ damping exponent from `alp` was not read (`UNVERIFIED`); CP2K uses α8 = α6 + 2 [S0-cp2k-src-disp-d3, line 182]. That item and the engines' D3 cutoff treatments are N2 representation checks |
| Reference | `REFERENCE RKS` for P2 (option list [S0-psi4-read-options, line 1464]) |
| Basis | def2-TZVP from the Psi4 v1.11 library (`def2-tzvp.gbs`, marked `spherical`) [S0-psi4-def2-tzvp] |
| SCF stopping criteria (effective) | `SCF E_CONVERGENCE 1.0e-8` and `SCF D_CONVERGENCE 1.0e-8`, set explicitly for energies and gradients alike. The module defaults are 1e-6 [S0-psi4-read-options, lines 1544 and 1551]. The v1.11 driver would set 1e-6 for SCF energies and 1e-8 for analytic gradients, but only when these options have not been changed by the user [S0-psi4-driver-util, lines 40–86]. The explicit values are therefore the effective ones, and no driver override is relied on |
| SCF algorithm, guess and auxiliary bases (Psi4) | `SCF_TYPE DIRECT`: exact integrals, recomputed as needed [S0-psi4-read-options, lines 194 and 2000]. **Declared `GUESS SAD`** for the production run, which is also the first N3 repeat; the other two repeats use `CORE` and `GWH` (C4 §2). The default `AUTO` would resolve to `SAD` for any molecule with more than one atom [S0-psi4-proc, lines 1883–1888], so the explicit value removes the dependence on that rule. Psi4 v1.11 has two fitting paths that are on by default, and both are switched off with documented options. (1) `DF_SCF_GUESS` defaults to true: "Do a density fitting SCF calculation to converge the orbitals before switching to the use of exact integrals in a … `DIRECT` calculation" [S0-psi4-read-options, line 1481]. With it true, a `DIRECT` run builds a `DF_BASIS_SCF` JKFIT auxiliary basis [S0-psi4-proc, lines 1452–1466]. **Declared `DF_SCF_GUESS false`**, so the wavefunction is given a zero auxiliary basis [S0-psi4-proc, line 1468]. (2) When the guess is `SAD`, `SADNO`, `HUCKEL` or `MODHUCKEL`, the per-atom SAD bases are built from the orbital basis [S0-psi4-proc, lines 1479–1484], and a `DF_BASIS_SAD` fitting basis is built as well whenever `SAD_SCF_TYPE` contains "DF" [lines 1486–1495]. The defaults are `SAD_SCF_TYPE DF` and `DF_BASIS_SAD SAD-FIT` [S0-psi4-read-options, lines 1829 and 1825]. **Declared `SAD_SCF_TYPE DIRECT`**, a documented value (line 1829), so the driver builds no SAD fitting basis. `BASIS_GUESS` stays at its default `FALSE` [line 1566], so no guess basis or guess fitting basis is cast [S0-psi4-proc, lines 1825–1860]. The `CORE` and `GWH` guesses do not enter the SAD path. Two further builds in the same file are not reached under these settings: the JKFIT basis of a C1 copy is made only when a caller passes `use_c1` [lines 1752 and 2112–2135], and `run_scf_gradient` hands its keyword arguments to `run_scf` unchanged [lines 2845–2860], with no such argument declared; and `run_scf` builds a `DF_BASIS_MP2` fitting basis only for a double-hybrid functional [lines 2765–2776], while the declared dictionary has no `c_mp2` block, the only place `dft_builder` sets an MP2 coefficient [S0-psi4-dft-builder, lines 370–383]. Within the Python driver source cited here, these settings therefore request no auxiliary or fitting basis. Three steps run in compiled code that was not read (`UNVERIFIED`): the SAD atomic solver under `SAD_SCF_TYPE DIRECT`, the double-hybrid test `is_c_hybrid()`, and the analytic gradient `core.scfgrad` under `DIRECT` [line 2869]. Whether any of them uses a fitting basis must be settled from version-matched source before Stage 1 starts (Section 8). The disk-based `PK` algorithm is not used; E-01 aborted during its setup (SOURCES [21]) |
| Grid and integrals | `DFT_RADIAL_POINTS 75` and `DFT_SPHERICAL_POINTS 302` [lines 1868–1870]; `INTS_TOLERANCE 1.0e-12` [line 1129], all defaults |
| Libxc version | Psi4 1.11 printed Libxc 7.1.2 at E-01 (SOURCES [11]). Whether CP2K's build uses the same libxc version is `[GAP]` |
| Isolated-molecule treatment in CP2K | Section 5: `PERIODIC NONE`, `WAVELET` and the box-plus-8-Å cell |

Basis identity was checked as bookkeeping, with no calculation, by comparing the text of the def2-TZVP definitions
in CP2K 2026.2 `EMSL_BASIS_SETS` [S0-cp2k-emsl-basis] and Psi4 v1.11 `def2-tzvp.gbs` for H, C, O, Si and Ge:
- The shell structure, all exponents and all multi-primitive contraction coefficients are identical.
- For C, O, Si and Ge, one or two single-primitive shells carry a non-unit coefficient in the CP2K file and 1.0 in
  the Psi4 file. Such a coefficient only scales one primitive, so the two definitions coincide after normalization
  if each engine normalizes contracted functions.
- That normalization behaviour is not established from the retrieved documentation (`UNVERIFIED`). N2 requires it
  to be confirmed before a P2 comparison is used.

## 7. Basis and core treatment per element

| Element | In the frozen configurations | ωB97X-D3 in CP2K 2026.2 | ωB97X-D3 in Psi4 1.11 (P2) | GFN0-xTB |
|---|---|---|---|---|
| H | Yes (M1 caps, tool; link atoms) | `Ahlrichs-def2-TZVP` from `EMSL_BASIS_SETS` [S0-cp2k-emsl-basis]; all-electron, `POTENTIAL ALL` | def2-TZVP [S0-psi4-def2-tzvp]; all-electron | The method's internal basis (CP2K-internal GFN0) |
| C | Yes | As H | As H | As H |
| O | Yes, tool legs only. Under the declared partition O is in the low-level region only; the basis is declared for completeness | As H | As H | As H |
| Si | Yes | As H | As H | As H |
| Ge | Yes | As H. def2-TZVP is all-electron for Ge in both files | As H | As H |
| I | **No.** The tool in every frozen configuration is de-iodinated | **`[GAP]`.** The 2026.2-branch data files hold no def2-TZVP entry for I in `EMSL_BASIS_SETS` and no def2 ECP in `ECP_POTENTIALS` [S0-cp2k-data-listing; S0-cp2k-ecp] | def2-TZVP with the def2 ECP (28 core electrons for Te–Xe, per the file header) [S0-psi4-def2-tzvp] | Not applicable |

A configuration that contains iodine would need a new declaration through the revision sequence. None exists in
Stage 0.

## 8. What stays open

None of the items below is claimed. They are sorted by when they must be settled; the three categories match the
[freeze record](STAGE0-FREEZE-RECORD.md#1-disposition).

**Prerequisites to starting Stage 1.** These are definitions that must be settled from version-matched source before
any Stage 1 calculation, or recorded as reviewed-blocked, so that no Stage 1 input depends on a Stage 1 result:
- GFN0 parameter provenance through CP2K `[GAP]` (G4; the closure assigns it to Stage 0 source reading).
- CP2K's unit for `OMEGA`.
- The normalization of single-primitive basis coefficients in both engines (needed by N2).
- The printed representations that N8 compares (C4, row 10).
- Whether the compiled Psi4 v1.11 steps named in Section 6 (the SAD atomic solver, `is_c_hybrid()` and
  `core.scfgrad`) use any fitting basis under the declared settings (`UNVERIFIED`).

**Dependencies within Stage 1.** These can be settled only by Stage 1 work after installation, and they gate
specific Stage 1b checks:
- CP2K 2026.2 installation, with the build identity and the libxc version it links (libxc identity between the
  engines is `[GAP]` until then).
- Link atoms, mixed methods and the numerical mixing derivative in CP2K `MIXED` (C2 §5).
- GFN0 under `UKS` and `MULTIPLICITY`.
- GAPW with exact exchange.
- Mulliken spin populations for E1 inside `MIXED` (the N2 diagnostic).
- Absence of any undocumented override of the E1 convergence controls.
- The s-dftd3 r⁻⁸ damping exponent and the D3 cutoff treatments (N2).

**Stage 2 gates.**
- **C5.** A convergence regime in Stage 1a, P1 identity provenance including parameter provenance, and P2 established.
  P2 needs the defining ωB97X-D3 reference for its check against the primary definition (spike §4, P2(a)), which is
  `[GAP]` because the paper was not obtained.
- **C6.** Composite validation, including N5 and N8.
- **B4.** Parity unknown, carried into every result.
