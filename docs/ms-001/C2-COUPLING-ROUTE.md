# C2 coupling route: comparison, selection and specification

Status: MS-001 Stage 0, scope option B. The selection and every specified setting are `[AGENT]`, a declared
deviation. The comparison rests on version-matched documentation and source, cited as `[S0-…]` and listed in
[SOURCE-LEDGER.md](SOURCE-LEDGER.md). Parity with the benchmark's scheme is unknown, and it is undeterminable
because the benchmark does not state its scheme (spike §4, P3).

**P3b stays open.** No composition of a GFN0-xTB level with a ωB97X-D3 level has been demonstrated for this system
through any route, including the selected one. Demonstrating the route and validating the composite coupled energy
and gradient are Stage 1 work (C6, spike §8.5), and nothing here claims either.

## 1. What the declared partition requires

The partition is declared in [B2-METHOD-DECLARATION.md §2](B2-METHOD-DECLARATION.md#2-partition-embedding-and-cut-bonds).
It places 18 atoms in the high-level region and cuts 11 covalent bonds (3 C–C and 8 Si–Si). A route must provide:

| # | Requirement |
|---|---|
| Q1 | Two-level subtractive composition, E = E_high(S+L) − E_low(S+L) + E_low(full system), where S is the high-level region and L its link atoms |
| Q2 | A GFN0-xTB level selected explicitly, since no documented route defaults to GFN0 (spike §4, P1), and a ωB97X-D3 level |
| Q3 | Link atoms on cut covalent bonds, with positions defined from the host and partner atoms and link forces mapped back to them (chain rule) |
| Q4 | An analytic composite gradient, for the per-step relaxations of the drive (B3) and for the composite finite-difference check (N5) |
| Q5 | A non-periodic cluster treatment for both levels |
| Q6 | Provenance capture through AiiDA (C3) |

## 2. Comparison of the three candidates

| Requirement | R-A: ASE `SimpleQMMM` (ASE 3.29.0) | R-B: CP2K `MIXED` / `GENMIX` / `MAPPING` (CP2K 2026.2) | R-C: Py-ChemShell `NLayerSubtractive` (25.0) |
|---|---|---|---|
| Q1 composition | Documented in the installed source: E = QM(subset) + MM2(all) − MM1(subset), with forces combined the same way on the selected indices [S0-ase-src-qmmm, lines 69–90] | `MIXING_TYPE GENMIX` provides a user-driven generic coupling of an unlimited number of force_evals [S0-cp2k-mixed]. `GENERIC` evaluates a `MIXING_FUNCTION` of the sub-force_eval energies [S0-cp2k-mixed-generic] | `NLayerSubtractive` provides N-layer subtractive (ONIOM-like) composition with mechanical embedding [S0-pychemshell-subtractive] |
| Q2 levels | Any ASE calculator for each term. GFN0 would need a calculator that can select it; the tblite ASE calculator cannot, because tblite has no GFN0 (spike §4) | GFN0: `XTB/GFN_TYPE 0` selects "the CP2K-internal GFN0-xTB implementation" (default 1) [S0-cp2k-xtb]. ωB97X-D3: libxc `HYB_GGA_XC_WB97X_D3` [S0-cp2k-xc], with exact exchange supplied by the `HF` section [S0-cp2k-hf; S0-cp2k-hf-ip] | ωB97X-D3 possibly through the Psi4 interface (`method`, `functional`, `basis`, `charge`, `mult`) [S0-pychemshell-psi4]; the accepted functional strings are not listed. **Undocumented capability (GFN0)**: the QM interface list has no xTB interface [S0-pychemshell-qm], and the documented CP2K-interface options list functionals `B3LYP` to `TPSS`, with no xTB setting and no ωB97X-D3 [S0-pychemshell-cp2k]. This is an absence of documentation, not an established impossibility |
| Q3 link atoms | **Native-interface limitation, documented in the installed source.** The subset calculators receive only `atoms[selection]` [S0-ase-src-qmmm, lines 62, 75, 80–81, 89–90], so the partner atom of a cut bond never reaches them, and a link atom cannot be placed inside the calculators the class accepts. This is not a demonstrated negative for a subtractive route in ASE: a wrapper or subclass that passes partner atoms would be new code outside the reuse candidates | **Undocumented capability.** The `MAPPING` pages define fragments by starting and ending atom index and map them one-to-one between sub-force_evals and the mixed force_eval [S0-cp2k-mapping-fe; S0-cp2k-mapping-fe-frag; S0-cp2k-mapping-fem]. No link-atom facility is described, and whether a sub-force_eval may hold atoms outside the mixed system is not stated | Documented: `link_atoms` defaults to hydrogen for QM layers [S0-pychemshell-subtractive]. Placement and force mapping are not described on that page |
| Q4 gradient | Forces combined analytically [S0-ase-src-qmmm] | The mixing function's derivative is computed numerically [S0-cp2k-mixed-generic]; its effect on the composite gradient is unmeasured | `gradients_eval` is `'analytic'` (default) or `'finitediff'` [S0-pychemshell-subtractive] |
| Q5 non-periodic | The selected subset is made non-periodic [S0-ase-src-qmmm, lines 62–66] | `POISSON/PERIODIC NONE` with a 0D solver (`MT`, `MULTIPOLE`, `WAVELET`, `ANALYTIC`) [S0-cp2k-poisson] | Per interface; not examined |
| Q6 provenance | Through ASE calculators; AiiDA wrapping not provided | One engine, one AiiDA plugin (`aiida-cp2k` 2.1.1, which generates the input from a `parameters` Dict; C3 §2) | A second driver beside ASE, with its own provenance capture |
| Native-interface limitations (documented) | Q3: the class passes only the selection to the subset calculators | None found | None found |
| Undocumented capabilities (neither shown nor excluded) | Selecting GFN0 through an ASE calculator, for example ASE's CP2K calculator with an input template | Q3 link atoms; different methods per sub-force_eval; GFN0 with `UKS`; exact exchange in GAPW (Section 5) | Q2: a GFN0 level; the accepted ωB97X-D3 functional strings; macOS support and licence name (MS-000 landscape §4.3) |
| Demonstrated negatives | None; nothing has been run | None; nothing has been run | None; nothing has been run |

## 3. Selection

**Selected: R-B, CP2K `FORCE_EVAL/MIXED` with `MIXING_TYPE GENMIX`, `GENERIC` and `MAPPING`, in CP2K 2026.2.**
This is an `[AGENT]` selection.

The reasoning is as follows. No candidate has a demonstrated negative, because nothing has been run, and absence of
documentation does not establish impossibility.
- **R-A has a native-interface limitation on a critical requirement (Q3).** It is documented in the installed
  source. Using R-A for this partition would require new code, a wrapper or subclass that places link atoms, which
  lies outside the reuse candidates.
- **R-C has an undocumented capability on a critical requirement (Q2, a GFN0 level).** It is neither shown nor
  excluded. It could be settled only through undocumented interface options or new interface work.
- **R-B also has an undocumented capability on a critical requirement (Q3, link atoms), plus the further
  undocumented items of Section 5.** Unlike R-C, R-B documents both method levels, the composition and the
  non-periodic treatment in one engine version. That keeps the GFN0 identity provenance (P1) and the functional
  settings (P2) in a single engine record.

Choosing R-B over R-C is therefore an `[AGENT]` judgement between two routes, each with one undocumented critical
capability. It prefers the route whose method levels and composition are documented. It does not exclude R-A or
R-C.

If Stage 1 shows that R-B cannot meet Q3 or Q4, the route returns to Stage 0 through the revision sequence (spike
§8.6). The failure is retained and a new route is selected and reviewed. Nothing here selects the fallback in
advance.

## 4. Specification of the selected route

All CP2K keywords below are documented for CP2K 2026.2. Values are declared in B2 and C4.

| Item | Declaration |
|---|---|
| Top level | `FORCE_EVAL` with `METHOD MIXED`. `MIXED/MIXING_TYPE GENMIX`, with `GENERIC/MIXING_FUNCTION E1-E2+E3` and `GENERIC/VARIABLES E1 E2 E3` [S0-cp2k-mixed; S0-cp2k-mixed-generic]. `GENERIC/DX` stays at its documented default of 0.1 bohr (the step of the Ridders' derivative) and `GENERIC/ERROR_LIMIT` at 1.0e-12. The variables follow the force_eval order [S0-cp2k-mixed-generic] |
| Sub-force_eval 1 (E1) | ωB97X-D3 on S+L: `METHOD QS`, `DFT/QS/METHOD GAPW`, with the settings in B2 §4 |
| Sub-force_eval 2 (E2) | GFN0-xTB on S+L: `METHOD QS`, `DFT/QS/METHOD XTB`, `XTB/GFN_TYPE 0`, with the settings in B2 §3 |
| Sub-force_eval 3 (E3) | GFN0-xTB on the full system, with the same settings as E2 |
| Composition formula | E = E1 − E2 + E3. Forces are computed by CP2K from the mixing function |
| Fragment mapping | Mixed system: every atom of the frozen configuration file, in file order. Sub-force_evals 1 and 2: the 18 atoms of S in a declared order, mapped by `MAPPING/FORCE_EVAL/FRAGMENT` onto the corresponding mixed-system atoms; because fragments are index ranges, the frozen order yields several fragments. Sub-force_eval 3: the default one-to-one mapping |
| Cut-bond treatment | One hydrogen link atom L per cut bond, in E1 and E2 only. L lies on the line from host h to partner p, at r_L = r_h + g (r_p − r_h), where g is the ratio of the covalent-radius sums: g = (r_H + r_h)/(r_h + r_p), with radii from `ase.data.covalent_radii` (ASE 3.29.0). That gives g = 0.7039 for the three C–C cuts and 0.6396 for the eight Si–Si cuts. The force on L is mapped by the chain rule: F_h += (1 − g) F_L and F_p += g F_L. Link atoms carry no charge (mechanical embedding) |
| Embedding | Mechanical (subtractive) only. There is no electrostatic embedding |
| Non-periodic treatment | `SUBSYS/CELL` with `PERIODIC NONE` and `DFT/POISSON/PERIODIC NONE`, using the 0D solver declared in B2 §5 |

## 5. What the official documentation does not establish

Each item is an undocumented capability: `UNVERIFIED`, neither shown nor excluded. Items 1 to 5 are dependencies
within Stage 1. They are settled by a demonstration run after installation, or earlier by version-matched source.
Item 6 is the Stage 2 gate C6.

1. **Link atoms (Q3).** No CP2K 2026.2 manual page retrieved documents link atoms in `MIXED`. None states that a
   sub-force_eval may contain atoms (L) that are absent from the mixed system, how their positions would follow
   the hosts, or how their forces would be mapped. The link-atom treatment in Section 4 is therefore a
   requirement on the route. It is not a documented capability.
2. **Different methods per sub-force_eval.** No retrieved page states that sub-force_evals under one `MIXED` may
   use different `DFT/QS/METHOD` values (GAPW and XTB).
3. **Numerical mixing derivative.** The mixing function's derivative is taken numerically [S0-cp2k-mixed-generic].
   Its contribution to the composite gradient error is measured only by the composite finite-difference check
   (N5).
4. **GFN0 under CP2K with open-shell settings.** Whether CP2K's internal GFN0-xTB accepts `UKS` and `MULTIPLICITY`
   as declared in B2 is not stated on the XTB page [S0-cp2k-xtb], which says only that GFN0 has no SCC variables to
   mix.
5. **ωB97X-D3 with exact exchange in GAPW.** The HF pages retrieved state no restriction and no support for
   all-electron GAPW [S0-cp2k-hf; S0-cp2k-hf-ip; S0-cp2k-hf-screening].
6. **The composite as a whole.** Correctness of the coupled energy and gradient, including link-atom chain-rule
   terms and constraint projection, is validated only by C6 in Stage 1.

## 6. Relation to other items

- **Validation.** Validating this route is Stage 1, under C6 and N5/N8 in [C4](C4-TOLERANCES-AND-CONVERGENCE.md),
  on the validation set in [C7](C7-VALIDATION-SET.md).
- **Driving.** The drive protocol (B3) runs the composite as one CP2K `FORCE_EVAL` per accepted step.
- **Provenance.** The frozen field set of C3 applies to every sub-force_eval output.
