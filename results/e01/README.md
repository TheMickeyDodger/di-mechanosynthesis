# E-01 result: a stopped engine-validation attempt

E-01 was designed to test whether the selected engine setup runs correctly on the two free donor candidates at
fixed geometry. It was executed once on 2026-09-24. The precursor stopped at its first self-consistent-field (SCF)
job when the engine aborted during integral setup. No converged electronic energy or gradient of either donor was
produced, and every dependent criterion is therefore INDETERMINATE. The activated donor was not run. The cause of the abort has not
been diagnosed. This outcome concerns the software run only; it is not a finding about the donors, the method or
the functional, and it does not bear on the benchmark study [1].

The machine-readable record is [`outcome.json`](outcome.json), and the configuration actually used is
[`method-config.json`](method-config.json). Engine output and error text are in [`raw/`](raw/). Numbers in square
brackets refer to the catalogue in [docs/SOURCES.md](../../docs/SOURCES.md).

## 1. What was run

The engine was Psi4 1.11 [6] from conda-forge, installed in a project-local environment of 94 packages [20]. The
method was ωB97X-D3 with D3 zero-damping dispersion, 6-31G(d,p) on all atoms except iodine and LANL2DZ with its
effective core potential on iodine, using the conventional (PK) SCF algorithm, 4 threads and 2 GB of engine memory
[21]. The run followed a reviewed configuration that settled the open clarifications of the prospective protocol
in [docs/e01-method-specification.md](../../docs/e01-method-specification.md); that document is kept as the
preparation record, while [`method-config.json`](method-config.json) records the method as run.

The runner treated the two donors one at a time, precursor first. For each donor the planned sequence was a set of
SCF solutions from prescribed initial guesses, an analytic gradient, 24 displaced-point energies for the
finite-difference check, an independent repeat and, for the precursor, a Hartree–Fock stability diagnostic. Any
SCF non-convergence or engine failure stopped that donor at once, and nothing was retried or retuned.

## 2. What happened

Before the first SCF job the runner checked host memory (31 % free of 17 179 869 184 bytes, above the
3 073 741 824 bytes required), the recorded identity of all 94 installed packages and the hashes of selected
installed files. It also ran a construction-only job, which built the precursor basis with 478 Cartesian basis
functions and 46 core electrons on iodine and computed no integrals
([`raw/FEASIBILITY.result.json`](raw/FEASIBILITY.result.json), [`raw/FEASIBILITY.psi4.out`](raw/FEASIBILITY.psi4.out)).

The first SCF job, P-RKS-core (restricted Kohn–Sham, core-Hamiltonian guess), printed its setup: 192 explicit
electrons, 478 basis functions, 46 core electrons in the iodine potential, the ωB97X-D3 functional through Libxc
7.1.2, the Yoshimine PK integral algorithm and a table of 44 planned integral batches
([`raw/P-RKS-core.psi4.out`](raw/P-RKS-core.psi4.out)). The printed table is the planned batch layout, not
evidence that the batches were completed. The engine also printed its standard warning that its
effective-core-potential capability is in beta. The output ends after the integral batch table, and no SCF
iteration was printed. After 852 s the process terminated with exit status −6 and the error
`PSIO_ERROR: 17 (Incorrect block start address)` on unit 92, from the engine's input/output library
([`raw/P-RKS-core.stderr.txt`](raw/P-RKS-core.stderr.txt)). No result file was written. The job's standard output
was empty.

The runner recorded the failure, stopped the precursor and launched nothing further for it. The classification is
in [`raw/precursor-classification.json`](raw/precursor-classification.json).

| Criterion | Precursor | Activated |
|---|---|---|
| SCF convergence | INDETERMINATE: 0 of 5 prescribed solutions produced | Not run |
| Consistency across initial guesses | INDETERMINATE; Kohn–Sham stability never PASS | Not run |
| Hartree–Fock stability diagnostic | INDETERMINATE: not run (not produced after the stop) | Not applicable |
| Analytic versus finite-difference gradient | INDETERMINATE: not produced | Not run |
| Reproducibility | INDETERMINATE: not produced | Not run |
| Resource envelope | PASS: runner classification from sampled memory observations and cooperative thread limits, not hard containment | Not run |
| Localization hypothesis | Not applicable | Not evaluable |

The activated donor was blocked rather than run. It uses the same configuration, the failure is unresolved and
potentially shared, and nothing isolates it to the precursor or shows that the activated donor would avoid it. No
prediction of the activated outcome is made.

## 3. Runtime observations

| Quantity | Value |
|---|---|
| Wall time charged to the precursor | 853.6 s of 7200 s; 3414.4 core-seconds; activated 0 s |
| P-RKS-core numerical wall time | 852.442 s |
| Peak sampled memory of the P-RKS-core process family | 1 131 232 kB, from 1581 samples; about 1.1 GB until roughly 326 s, then 11 to 17 MB until the abort |
| Integral scratch files at 06:07:45Z, 84 s before the runner recorded the stop | unit 92: 103 882 500 120 bytes; unit 93: 207 765 000 120 bytes |
| Free scratch space at that time | 246 266 699 776 bytes |
| Largest pre-run scratch estimate | 209 696 221 472 bytes (arithmetic, not engine-reported) |
| Free space after cleanup | 557 900 038 144 bytes; job scratch removed |

The observed scratch allocation exceeded the pre-run estimate. Disk exhaustion at the moment of the abort is
neither established nor excluded: the last observation was taken 84 s before the runner recorded the stop, and the
instant of the abort was not observed. The free space recorded after cleanup shows only that space was reclaimed.

## 4. Interpretation

No cause is asserted. The following hypotheses are ranked and untested:
1. a large-file or block-address handling failure in the conventional PK integral path and its input/output layer,
   which the explicit error and the large integral files suggest;
2. scratch capacity or another filesystem or input/output condition;
3. a trigger specific to the precursor, such as its size or its iodine-containing integral workload.

The result establishes that the installed engine, basis construction and method setup reached integral setup for
the precursor. It establishes nothing about SCF convergence, converged electronic energies, gradients, spin
properties or the localization hypothesis, and nothing about the activated donor.

## 5. Proposed next work

The following is a proposal. It has not been executed or authorized.

- **A.** Tabulate what the existing records contain. They give no failing byte offset, no address representation
  and no mapping from the integral batch index to an address, so no inference is drawn from the batch index.
- **B.** Optionally, a single filesystem-only probe on the same storage, with stated limits on size, free space
  and time. It would not run the engine's integral or input/output code, so its success could not weaken the first
  hypothesis.
- **Outstanding.** The engine-specific question needs a separately authorized diagnostic of the engine's own code
  path. Completing A and B, even with a successful probe, would not resolve it.
- **C.** Only afterwards, a revised configuration proposal, for example a different SCF algorithm with a named
  auxiliary basis, or the same algorithm on storage verified for the required file sizes, each subject to review.

Any future attempt should sample scratch free space and file sizes through to termination and record the sampling
interval. A value between samples remains unobserved.

## 6. Provenance

The private run records, the reviewed as-run evidence manifest of 45 files and the preparation manifest of 33
files are identified by SHA256 in [`outcome.json`](outcome.json) and
[provenance/EXPORT-MANIFEST.md](../../provenance/EXPORT-MANIFEST.md). The files in [`raw/`](raw/) are copies of
engine output and records; four of them were redacted to remove local paths and a host name, as stated in the
export manifest. The records were also stored, with verified digests, in the project's provenance system [12].
That storage succeeded, and it is evidence of record-keeping, not of any scientific result.
