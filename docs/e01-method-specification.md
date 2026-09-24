# First calculation (E-01): prospective specification of donor-only engine validation

**Status (2026-09-24).** This document is the preparation record and is kept as written. Its open clarifications
were settled by review before the run, and the configuration actually used is
[`../results/e01/method-config.json`](../results/e01/method-config.json). E-01 was executed once: the precursor
stopped when the engine aborted during integral setup, no converged result was produced and the activated donor
was not run ([`../results/e01/`](../results/e01/README.md)). Statements below about the calculation not having
been run, and about open clarifications, describe the state before the run.

This document adapts the project's accepted method definition for the first planned calculation, designated E-01.
The calculation had not been run when it was written, and the specification then contained open clarifications
(Section 5). Its
numerical thresholds are prospective engineering choices, not literature values, unless stated otherwise. Several
engine capabilities on which it depends are unverified for the selected program version, as recorded in
[engine-capability-status.md](engine-capability-status.md). The definition originates in an agent-prepared
reconstruction record (`[AGENT]`). It fixes what would be measured and is not evidence of any outcome. Section 3 of
[SOURCES.md](SOURCES.md) identifies the source of each specification element and states whether it is a
primary-source fact or a proposed choice.

## 1. Question and scope

E-01 asks whether the selected engine, functional, basis set with effective core potential and open-shell
treatment run correctly on the two free donor candidates at their given geometries, and which descriptors they
report. Its scope is limited to single-point energies and gradients of the two free donors at fixed geometry, and
to outcomes describing the engine and method setup. It excludes relaxation or repair of coordinates, surface or
combined tool and surface systems, trajectories, barriers and reaction products. It also excludes any claim about
ground states, stability, pathways or agreement with the benchmark.

## 2. Inputs and method

| Item | Definition |
|---|---|
| Species | Precursor `donor-precursor-EAOGe-C2I.extxyz` (49 atoms, charge 0, multiplicity 1, restricted Kohn–Sham). Activated `donor-activated-EAOGe-C2-radical.extxyz` (48 atoms, charge 0, multiplicity 2, unrestricted Kohn–Sham). Both are unoptimized ETKDG embeddings. |
| Engine | Psi4 1.11 |
| Functional | ωB97X-D3 |
| Basis | 6-31G(d,p) on all atoms except iodine; LANL2DZ with its effective core potential on iodine |
| Integration grid | Engine default |
| SCF convergence | 10⁻⁸ Eh in energy and 10⁻⁸ RMS in density for any quantity entering a criterion; at most 100 iterations. Non-convergence is a stop, and no damping or level shift is introduced silently. |
| Initial guesses | Several per species: core Hamiltonian, SAD and a broken-symmetry guess (the precursor's guess set is an open question, Section 5) |
| Diagnostic | Hartree–Fock RHF→UHF stability check for the precursor, as a separate and non-equivalent diagnostic |
| Resource envelope | At most 8 cores and 16 GB, one species at a time, and 2 h aggregate wall time per species across all sub-calculations. A breach is a reported stop, not a retry. |

## 3. Engine-validation criteria

The outcomes in this section concern the software and method setup only.

| Observable | PASS | INDETERMINATE | FAIL |
|---|---|---|---|
| SCF convergence (both species, every guess) | All converged within 100 iterations | Some converged (report which) | None converged |
| Consistency across initial guesses | All converged solutions agree within 10⁻⁶ Eh and ⟨S²⟩ within 0.01 | Solutions differ (report the lowest and the spread) | Not used; a spread is a finding, not an engine failure |
| RHF→UHF stability (precursor, Hartree–Fock) | Stable | Unstable (report) | Not used |
| ⟨S²⟩ of the activated donor (lowest-energy solution) | Deviation from 0.75 below 0.10 | Deviation of at least 0.10 and below 0.30 | Deviation of 0.30 or more; a limitation of the method only, never a claim about the ground state |
| Analytic versus finite-difference gradient | Section 3.1 | Section 3.1 | Section 3.1 |
| Reproducibility (repeat run) | ΔE ≤ 10⁻⁸ Eh and Δg ≤ 10⁻⁶ au | Not used | Otherwise (reproducibility only, not gradient correctness) |
| Resource envelope | Within the envelope | Not used | Breach: stop, reported |

No Kohn–Sham stability criterion is used. Whether Psi4 1.11 can perform Kohn–Sham stability analysis for this
functional is unverified, and the specification does not claim that it is impossible. The archived development
documentation limits Kohn–Sham support in the Davidson algorithm to LDA functionals (as of version 1.7). It is
silent, in the lines inspected, on the Kohn–Sham coverage of the direct-inversion algorithm, which therefore
remains unresolved. The version-tagged source restricts only stability root-following to UHF references.
Stability is always reported as indeterminate, and the use of several initial guesses does not establish
stability or a ground state.

### 3.1 Analytic versus finite-difference gradient rule

The finite-difference gradient is obtained by central differences g<sub>fd</sub>(h) with step h = 0.005 bohr and
half step h/2 = 0.0025 bohr. Every displaced-point SCF is converged to 10⁻¹⁰ Eh and 10⁻¹⁰; a component whose
displaced points do not meet this is designated SCF-unmet. The sampled components are the x, y and z components of
`D-Cb` and the x, y and z components of one leg hydrogen.

For each component, three quantities are computed, with g<sub>a</sub> the analytic gradient:
- the absolute error e<sub>abs</sub> = |g<sub>a</sub> − g<sub>fd</sub>(h)|
- the relative error e<sub>rel</sub> = e<sub>abs</sub> / max(|g<sub>fd</sub>|, 10⁻⁴ au)
- the step consistency s = |g<sub>fd</sub>(h) − g<sub>fd</sub>(h/2)|

The maximum over the sampled components is used. Components with |g<sub>fd</sub>| < 10⁻⁴ au are judged by
absolute error only; the relative-error conditions apply only where |g<sub>fd</sub>| ≥ 10⁻⁴ au. The outcome is the
first of the following that applies:

1. **FAIL**, if any e<sub>abs</sub> > 10⁻⁴ au, or (|g<sub>fd</sub>| ≥ 10⁻⁴ au and e<sub>rel</sub> > 10⁻²).
2. **INDETERMINATE**, if any of the following holds:
   - any component is SCF-unmet
   - any s > 10⁻⁵ au
   - any 10⁻⁵ < e<sub>abs</sub> ≤ 10⁻⁴ au
   - any (|g<sub>fd</sub>| ≥ 10⁻⁴ au and 10⁻³ < e<sub>rel</sub> ≤ 10⁻²)
3. **PASS**, otherwise.

If analytic gradients are unavailable for this setup, the finite-difference gradient serves as the gradient. This
criterion is then reported as "analytic unavailable", which is INDETERMINATE.

## 4. Localization hypothesis for the activated donor

The localization hypothesis concerns the activated donor only. It is reported separately from the
engine-validation outcomes and is never an engine FAIL.

The guess set G consists of exactly three unrestricted runs, started from the core Hamiltonian, SAD and
broken-symmetry guesses. For each guess g the record contains its convergence and, if converged, the energy
E<sub>g</sub>, the value ⟨S²⟩<sub>g</sub> and the Löwdin spin population *p*<sub>g</sub> on `D-Cb`. Two solutions
are degenerate if |ΔE| ≤ 10⁻⁶ Eh and energetically distinct otherwise.

The reference solution L is the converged solution with the lowest energy. Energies within 10⁻⁶ Eh count as tied,
and ties are resolved by the lowest ⟨S²⟩, then by guess order (core Hamiltonian, SAD, broken symmetry). The
population used by the rules below is *p* = *p*<sub>L</sub>, the population of solution L. The spread Δ*p* is the
maximum minus the minimum of *p*<sub>g</sub> over the converged guesses.

Exactly one outcome applies, namely the first of the following rules that matches:

1. **Not evaluable**, if any of the following holds:
   - a stop condition fired
   - any guess failed to converge
   - Löwdin spins or ⟨S²⟩ are unavailable or unverified in the installed version
   - any required value is missing or non-finite
2. **Indeterminate (unstable description)**, if 0.10 ≤ ⟨S²⟩<sub>L</sub> − 0.75, or if any pair of converged
   solutions is energetically distinct.
3. **Indeterminate (guess-dependent)**, if all solutions are degenerate and Δ*p* > 0.10 e.
4. **Indeterminate (intermediate)**, if 0.50 e ≤ *p* < 0.80 e.
5. **Supported**, if *p* ≥ 0.80 e.
6. **Not supported**, if *p* < 0.50 e.

"Supported" never means "ground state". Spin populations are model-dependent descriptors, not evidence about
reactions or about parity with the benchmark.

## 5. Stop conditions and open clarifications

A calculation stops on SCF non-convergence, on ⟨S²⟩ ≥ 1.05, or on a breach of the resource envelope. Each stop is
reported as a result and is never retuned silently.

One apparent ambiguity has been clarified. The ⟨S²⟩ tolerance of 0.01 belongs to the engine-validation row on
consistency across initial guesses (Section 3). The statement that no 0.01 tolerance is used applies only to the
localization hypothesis (Section 4). The two sections have separate scopes.

Four technical clarifications were open when this specification was written and had to be settled before any
run:
- whether the precursor also runs unrestricted, and with which guess set
- which leg hydrogen, and which species, the finite-difference check samples
- whether the full set of sub-calculations fits the per-species budget
- how a run proceeds if ⟨S²⟩ is unavailable, since the stop at ⟨S²⟩ ≥ 1.05 could not then be evaluated

They were settled by review before the run, as recorded in
[`../results/e01/method-config.json`](../results/e01/method-config.json):
- the precursor schedule prescribes restricted core and SAD guesses, with unrestricted core, SAD and
  broken-symmetry guesses for comparison; in the run only the restricted core guess was attempted, and every later
  guess was not run after the stop
- the finite-difference check samples `D-Cb` and the leg hydrogen `D-L1a-H1` in both species
- the per-species budget is an aggregate ceiling; exhausting it is a reported stop, and the budget was not shown in
  advance to suffice
- an unavailable ⟨S²⟩ downgrades the dependent criteria and makes the localization hypothesis not evaluable,
  without substituting a value

The run also applied one rule more strictly than the text above: any SCF non-convergence, and ⟨S²⟩ ≥ 1.05 for any
converged unrestricted guess, stops that species at once, before any further job.

## 6. What E-01 can and cannot establish

E-01 can establish whether the engine, functional, basis set with effective core potential and open-shell setup
run on the reconstructed donor candidates, and which descriptors they report. It cannot establish anything about
the surface reaction, the pathway or stability. Nor can it establish parity with the benchmark's calculations.
