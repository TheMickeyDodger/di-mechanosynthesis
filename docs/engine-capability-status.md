# Engine capability status (Psi4 1.11)

The first experiment selects **Psi4 1.11**. A capability counts only if it is shown for that exact version. This
page records what archived primary sources support, and what remains unverified.

- **Two kinds of source:**
  - archived **development-manual** pages, which carry the version string `1.12a1.dev35` in their headers
  - two **version-tagged** source files from the `v1.11` tag
- **What they can and cannot show:** development documentation cannot establish what an installed 1.11 release
  does, and a source file does not prove runtime behaviour.
- **What is copied:** nothing. Vendor text and code are cited by URL and paraphrased. The complete tool and
  documentation index is in [SOURCES.md](SOURCES.md).

## Sources inspected

| Source (public URL) | Version basis | What was read |
|---|---|---|
| <https://psicode.org/psi4manual/master/scf.html> | development manual `1.12a1.dev35` | ⟨S²⟩ reporting, convergence keywords, stability analysis |
| <https://psicode.org/psi4manual/master/oeprop.html> | development manual `1.12a1.dev35` | Löwdin atomic spins |
| <https://psicode.org/psi4manual/master/basissets.html> | development manual `1.12a1.dev35` | per-atom and per-label basis assignment; effective core potentials |
| <https://psicode.org/psi4manual/master/dft_byfunctional.html> | development manual `1.12a1.dev35` | the `WB97X-D3` functional row |
| <https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/procrouting/proc.py> | `v1.11` tag URL (attribution by retrieval URL) | stability-analysis root-following check |
| <https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/procrouting/dft/libxc_functionals.py> | `v1.11` tag URL; retrieved 2026-09-23, 13 425 bytes, Git blob `d1ed5e1a27b61b780e42449ab8f093718c9286e5`, SHA256 `e289d7d713e2ae9cecf8e37a22d80ed7fd9beed0c9febd0aa9282afd81c448fe` (exact match to the expected blob) | the `wB97X-D3` functional entry only |

According to the project's retrieval record, version-pinned `1.11.0` manual pages were requested and returned
HTTP 404, so no 1.11 release manual was available.

## Capability table

| Capability | Needed for | What the inspected source supports | Status for installed 1.11 |
|---|---|---|---|
| Analytic ωB97X-D3 gradients (with an effective core potential for the precursor) | both species (effective core potential: precursor only) | No archived statement establishing it was inspected in the current review | **UNVERIFIED** — if unavailable, the gradient criterion reports "analytic unavailable" (INDETERMINATE) |
| ⟨S²⟩ reporting for unrestricted Kohn–Sham | activated donor; also the precursor if it runs unrestricted | The development manual states the ⟨S²⟩ deviation is printed for **UHF**. Unrestricted Kohn–Sham is not addressed in the passage read. | **UNVERIFIED** |
| Per-atom / per-label basis assignment with effective core potentials in the same block | precursor only | The development manual documents an `assign` syntax (global, per element, per label). It also says an ECP given with the orbital basis is parsed automatically and its core-electron count detected. | **UNVERIFIED** |
| Löwdin spin populations (`LOWDIN_SPINS`) | activated donor, localization hypothesis only | The development manual lists Löwdin atomic spins as a property ("fractional number of unpaired electrons") | **UNVERIFIED** — the hypothesis is not evaluable until verified; engine validation is unaffected |
| SCF convergence controls | both | The development manual defines convergence by energy change, RMS density change and a maximum iteration count, in a passage covering Fock and Kohn–Sham potentials | **UNVERIFIED** |
| Kohn–Sham stability analysis | — (no criterion uses it) | The manual limits **Davidson** instability analysis for Kohn–Sham references to LDA functionals (as of 1.7). It is silent in the lines read on **direct-inversion** Kohn–Sham coverage. It says the only *external* instability checkable is RHF→UHF. The v1.11 source restricts stability *root-following* to UHF references. None of this shows that all Kohn–Sham stability analysis is unsupported. | **UNVERIFIED** for the exact version (direct-inversion coverage unresolved). There is no stability criterion; stability is always reported indeterminate. |
| Functional identity: `wB97X-D3` | both | The v1.11 source declares `wB97X-D3` (lookup key `wb97x-d3`, no alias or citation field). Its exchange–correlation part is delegated to the Libxc identifier `HYB_GGA_XC_WB97X_D3` with no parameter overrides, and it declares dispersion type `d3zero2b` with s6 = 1.0, s8 = 1.0, sr6 = 1.281, sr8 = 1.094, alpha6 = 14.0. A separate `wB97X-D` entry uses a different Libxc identifier and dispersion type. The development-manual row lists `WB97X-D3` as a hybrid GGA; its numeric columns were not interpreted. | **Open.** Declaration-level evidence only; equivalence to the benchmark's functional is not established |
| Basis coverage (6-31G(d,p) for Ge; LANL2DZ for I) and the iodine core-electron count | both | Not inspected in the current review | **UNVERIFIED** |

## Remaining dependency gaps for the functional

1. The Libxc definition of `HYB_GGA_XC_WB97X_D3` (functional form, exact-exchange fraction, range separation) in
   the Libxc version linked into the installed build.
2. The Psi4 driver code that turns the functional list into a functional.
3. The implementation that computes dispersion type `d3zero2b`, and whether it is present in an installed
   environment.
4. Primary literature for ωB97X-D3 and its D3 parameters, compared with the declared values and with the
   benchmark's setup.
5. Confirmation that an installed 1.11 build contains this exact file and resolves `wb97x-d3` to it.

Any mismatch found in these would be a **method change**, to be decided explicitly and never substituted
silently.
