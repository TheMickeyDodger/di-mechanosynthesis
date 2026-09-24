# Engine capability status for Psi4 1.11

The first calculation selects Psi4 1.11. A capability of the program is treated as available only if it is shown
for that exact version. This document records what the inspected primary sources establish about each capability
the calculation requires, and what remains unverified. Numbered citations refer to [SOURCES.md](SOURCES.md), which
also contains the full catalogue of tools and documentation.

## Sources and their standing

Two kinds of source were inspected.

The first kind is a set of archived pages of the Psi4 manual [7], whose headers carry the development-manual
version string `1.12a1.dev35`. They are the chapters on the self-consistent field
([scf](https://psicode.org/psi4manual/master/scf.html)), one-electron properties
([oeprop](https://psicode.org/psi4manual/master/oeprop.html)) and basis sets
([basissets](https://psicode.org/psi4manual/master/basissets.html)), together with the functional table
([dft_byfunctional](https://psicode.org/psi4manual/master/dft_byfunctional.html)).

The second kind is two source files attributed to the `v1.11` tag by their retrieval URLs:
- [`proc.py`](https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/procrouting/proc.py) [9], inspected
  for its stability-analysis check.
- [`libxc_functionals.py`](https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/procrouting/dft/libxc_functionals.py)
  [10], inspected only for its `wB97X-D3` entry. It was retrieved on 2026-09-23 as 13 425 bytes, with Git blob
  `d1ed5e1a27b61b780e42449ab8f093718c9286e5`, an exact match to the expected blob, and SHA256
  `e289d7d713e2ae9cecf8e37a22d80ed7fd9beed0c9febd0aa9282afd81c448fe`.

According to the project's retrieval record, the version-pinned `1.11.0` manual pages returned HTTP 404 when
requested, so no 1.11 release manual was available. Development documentation cannot establish what an installed
1.11 release does, and a source file does not prove runtime behaviour. Vendor text and code are cited by URL and
paraphrased rather than copied.

## Capabilities

### Analytic ωB97X-D3 gradients

Both species require analytic gradients, and the precursor requires them with an effective core potential on
iodine. No archived statement establishing this capability was inspected in the current review, so it is
`UNVERIFIED`. If analytic gradients are unavailable, the gradient criterion reports "analytic unavailable", which
is INDETERMINATE.

### ⟨S²⟩ reporting for unrestricted Kohn–Sham references

The activated donor requires this, and so would the precursor if it were also run unrestricted. The development
manual states that the deviation of ⟨S²⟩ from its expected value is printed for UHF. The passage read does not
address unrestricted Kohn–Sham references, so the capability is `UNVERIFIED`.

### Per-atom and per-label basis assignment with effective core potentials

Only the precursor requires this. The development manual documents an `assign` syntax that sets a basis globally,
per element or per atom label. It states that an effective core potential given in the same section as the
orbital basis is parsed automatically, with its core-electron count detected. The capability is `UNVERIFIED` for
1.11.

### Löwdin spin populations (`LOWDIN_SPINS`)

Only the localization hypothesis for the activated donor requires these. The development manual lists Löwdin
atomic spins among the one-electron properties, described as the "fractional number of unpaired electrons". The
capability is `UNVERIFIED` for 1.11. Until it is verified the hypothesis is not evaluable, although engine
validation is unaffected.

### SCF convergence controls

Both species require these. The development manual defines convergence by the change in energy, the
root-mean-square change in density and a maximum iteration count, in a passage that covers both Fock and Kohn–Sham
potentials. The capability is `UNVERIFIED` for 1.11.

### Kohn–Sham stability analysis

No criterion of the specification uses this capability.
- The development manual limits Davidson instability analysis for Kohn–Sham references to LDA functionals (as of
  1.7).
- It is silent, in the lines read, on the Kohn–Sham coverage of the direct-inversion algorithm.
- It states that the only external instability that can be checked is RHF→UHF.
- The v1.11 source restricts stability root-following to UHF references.

None of this shows that all Kohn–Sham stability analysis is unsupported. The capability is `UNVERIFIED` for the
exact version, with direct-inversion coverage unresolved, and stability is always reported as indeterminate.

### Functional identity of `wB97X-D3`

Both species depend on the identity of the functional. The v1.11 source [10] declares an entry named `wB97X-D3`
with the lookup key `wb97x-d3` and no alias or citation field. The entry delegates exchange and correlation to the
Libxc identifier `HYB_GGA_XC_WB97X_D3`, with no parameter overrides. It declares a dispersion term of type
`d3zero2b` with s6 = 1.0, s8 = 1.0, sr6 = 1.281, sr8 = 1.094 and alpha6 = 14.0. A separate `wB97X-D` entry uses a
different Libxc identifier and a different dispersion type.

The development-manual functional table lists `WB97X-D3` as a hybrid GGA; its numeric columns were not
interpreted. This is evidence at the level of a declaration only. Equivalence to the functional used by the
benchmark has not been established and remains an open question.

### Basis coverage and the iodine core-electron count

Both species depend on basis coverage, through 6-31G(d,p) for germanium and LANL2DZ for iodine. Coverage and the
iodine core-electron count were not inspected in the current review and are `UNVERIFIED`.

## Remaining dependencies for the functional

Settling the identity of the functional requires five further sources:
1. The Libxc definition of `HYB_GGA_XC_WB97X_D3` (functional form, exact-exchange fraction and range separation),
   in the Libxc version linked into the installed build [11].
2. The Psi4 driver code that converts the functional list into a functional.
3. The implementation that computes the `d3zero2b` dispersion, and whether it is present in an installed
   environment.
4. The primary literature for ωB97X-D3 and its D3 parameters, compared with the declared values and with the
   setup of the benchmark.
5. Confirmation that an installed 1.11 build contains this exact file and resolves `wb97x-d3` to it.

A mismatch found in any of these would constitute a change of method, to be decided explicitly and never
substituted silently.

## Evidence from the installed build (2026-09-24)

Psi4 1.11 was later installed from conda-forge in a project-local environment [20] and used for the E-01 attempt
[21]. The sections above describe the archived sources and are kept as written; this section records what the
installed build showed, and what it did not. Evidence from the installed build concerns this build only.

| Capability | Status for the installed build | Evidence |
|---|---|---|
| Installation of Psi4 1.11 and its dependencies | Established: 94 conda-forge packages; package identities checked before the run | [20] |
| Per-element basis assignment with the iodine core potential | Established for construction: `assign 6-31G**` with `assign I lanl2dz` built 478 Cartesian basis functions for the precursor, with 46 core electrons in the iodine potential and 192 explicit electrons. The comma-free spelling `6-31G**` was used; it resolves to the same installed basis file as `6-31G(d,p)`. | [21]; [`../results/e01/raw/FEASIBILITY.result.json`](../results/e01/raw/FEASIBILITY.result.json), [`../results/e01/raw/P-RKS-core.psi4.out`](../results/e01/raw/P-RKS-core.psi4.out) |
| Basis coverage for germanium and iodine | Established for construction: the installed basis files supplied entries for Ge, C, O, H and I, including the iodine core potential | [21] |
| Composition of `wB97X-D3` as run | Printed by the engine: Libxc 7.1.2, `XC_HYB_GGA_XC_WB97X_D3`, and the exact-exchange lines `0.8043 HF,LR [omega = 0.2500]` and `0.1957 HF`, as printed | [21]; [`../results/e01/raw/P-RKS-core.psi4.out`](../results/e01/raw/P-RKS-core.psi4.out) |
| `d3zero2b` dispersion | Configured route through simple-dftd3 [22]; the declared parameters were printed at E-01 setup, and the route was exercised in a dispersion-only check without SCF. E-01 completed no dispersion-corrected energy. | [21], [22] |
| Installed `libxc_functionals.py` | Differs from the `v1.11` tag [10] at the TH-FL entry only; the `wB97X-D3` entry is unchanged | [20]; [`../results/e01/method-config.json`](../results/e01/method-config.json) |
| Conventional (PK) SCF for the precursor at 478 basis functions | Not established: the first SCF job aborted during integral setup with `PSIO_ERROR: 17 (Incorrect block start address)`, and no SCF iteration was printed; cause undiagnosed | [21]; [`../results/e01/`](../results/e01/README.md) |
| SCF convergence controls, analytic gradients with the core potential, ⟨S²⟩ for unrestricted Kohn–Sham references, Löwdin spins | Still `UNVERIFIED`: not validated by the stopped attempt. The gradient and property jobs were never launched. Whether any SCF activity occurred inside the aborted job is unknown; the absence of printed iterations does not show that none occurred | [21] |
| RHF→UHF stability diagnostic | Not run: it was not produced after the precursor stopped. The reviewed plan would have recorded its result as unavailable (INDETERMINATE), because the inspected driver code of the installed build returns no machine-readable result for the check mode; no engine behaviour was observed | [21] |
| Functional equivalence with the benchmark | Open | Not applicable |

The engine printed its standard warning that its effective-core-potential capability is in beta. Nothing here
shows how the build behaves in an SCF, a gradient or a property calculation for these systems.
