# E-01 postmortem and installed-build survey

This document records how the E-01 attempt was closed. It sets out what the retained run records show and what
they lack, a conditional reading of the engine's version-pinned source text, the results of a bounded static
survey of the installed build, the reasons no exact executable diagnostic could be specified, and the gaps that
remain. The attempt itself is described in [README.md](README.md), and its machine-readable record is
[`outcome.json`](outcome.json). Numbers in square brackets refer to the catalogue in
[docs/SOURCES.md](../../docs/SOURCES.md).

Every statement in this document about the source text, the installed build or the survey is taken from the
project's private, hash-bound records, which are identified in Section 9 by description and SHA256 only. The
source captures, the raw survey captures and the other records bound by those records are not part of this
repository. None of them was inspected, recomputed or re-verified in preparing this document, and each such
statement is attributed to the private records as they report it.

## 1. Outcome

E-01 is closed as technically BLOCKED and scientifically INDETERMINATE. This disposition is terminal for the
attempt as run, and no further step of the attempt is pending. No converged quantum-chemistry result exists for
either donor, and every chemistry-dependent result, including every E-01 criterion that depends on an SCF
solution, a gradient or a population, remains INDETERMINATE. The cause of the engine abort has not been
diagnosed. The activated donor remains blocked and unrun.

The outcome concerns a software run. It is not a finding about the donors, the method, the functional or the
benchmark study [1], and it carries no evidence class about chemistry.

## 2. What the retained run records contain and lack

The retained records of the precursor's first SCF job, P-RKS-core [21], contain the following. The engine
process ended with exit status −6. Its error output was retained complete, 1045 bytes in the original record; the
published copy, [`raw/P-RKS-core.stderr.txt`](raw/P-RKS-core.stderr.txt), is redacted as stated in the export
manifest. The error output reports input/output library error code 17 on unit 92 and an uncaught engine
exception, and the list of recent function calls that follows is empty, so no call stack was retained. The engine
output, [`raw/P-RKS-core.psi4.out`](raw/P-RKS-core.psi4.out), ends during conventional (PK) integral setup, after
reporting 49 atoms, 217 atomic-orbital shells, 484 primitives, 478 basis functions, an integral cutoff of
1.00e-12 and 4 threads. At the single scratch observation, the scratch files of units 92 and 93 held
103 882 500 120 and 207 765 000 120 bytes, and 246 266 699 776 bytes were free. No converged energy or gradient
was produced, and how far the job had progressed internally towards an SCF solution is unknown.

Two identifications come from the `v1.11` source text [23, 24] rather than from the run records. In that text,
unit 92 is the first conventional supermatrix scratch file (`PSIF_SO_PKSUPER1`), unit 93 is the second
(`PSIF_SO_PKSUPER2`), and code 17 is the constant for an incorrect block start address (`PSIO_ERROR_BLKSTART`).
The run records supply the two numbers and the printed description of the error. The mapping of the numbers to
these source-level constants is conditional on the installed build matching the source text.

The scratch observation was made at 06:07:45Z, and two intervals are recorded from it. The first, 84 s, ends at
the termination of the runner. The second, 81 s, ends at the write of the error output and the settlement of the
job. Both are valid; they end at different events, and neither is a correction of the other. Neither ends at the
instant of the abort, which was not observed. Nothing about the growth of the scratch files, the free space or the
state of the job at the abort follows from either interval.

The records give no failing byte offset, no address representation and no mapping from the printed integral batch
index to an address. No inference is drawn from the printed batch table, from its final index exceeding 2³², or
from the fall in sampled memory at about 326 s.

## 3. A conditional source-level pathway

### 3.1 Basis and status

This section reads the Psi4 source text at the `v1.11` tag [23, 24], with the line locators recorded in the
project's private capture records [25]. Source text is conditional evidence. It does not establish the code of the
installed binary, and a type declared in the source is not a measured width in the installed build. Statements
about the order of checks describe the inspected sites only; they exclude neither earlier operations on the table
of contents or the entry nor branches that were not traced.

The status of the pathway governs everything that follows. The pathway is possible in the source text, but it has
not been shown to have occurred. It is not established as the cause of E-01. It is one concrete branch inside the
broader hypothesis of a block or entry inconsistency in the integral input/output path (Section 4), and nothing
establishes that it, rather than another branch, operated. It remains a hypothesis (`[SPEC]`) and is neither
established nor excluded. The retained configuration and engine banner record a configured memory value of
2,000,000,000 bytes. The records do not establish the internal PK memory operand after any engine-side adjustment,
the workload size, the divisor, the row count, the remainder, the extent of each bucket, or the order in which the
buckets' first writes were issued. Those are the quantities needed to decide whether the pathway's conditions were
met in E-01.

### 3.2 The pathway

Before the conventional integral buckets are written, the manager in `PKmanagers.cc` pre-stripes each supermatrix
scratch entry with zeros (lines 950 and 957 to 980). For the J entry it expresses the workload size, `iwlsize`, in
doubles (line 961) and sets the divisor `safemem` to nine tenths of the engine's memory value (line 964). It then
obtains the row count `nrows` by integer division of the workload size by that divisor (line 965) and the
remainder `leftover` (line 966). Only after both have been computed is the divisor clamped to the workload size
(line 967), so the clamp affects neither the row count nor the remainder, and it changes nothing whenever the row
count is positive. The zero-fill routine `zero_disk` is called with the row count only when that count is positive
(lines 968 to 970), and a second call for the remainder follows unconditionally (line 971). The K entry is
pre-striped in the same way with twice the number of rows (lines 977 to 980). The same file maps units 92 and 93
to the two supermatrix files (lines 946 and 947).

In `aio_handler.cc` the zero-fill runs as a queued job of the asynchronous input/output handler. The job sets its
starting position to the entry-relative zero address, `PSIO_ZERO`, once per call and then writes its rows one
after another (lines 410 to 418). As the source reads, a second call on the same key therefore restarts at
entry-relative zero and rewrites inside the extent that the first call wrote, instead of extending it. When both
calls run, the entry ends after `nrows` rows of the divisor's length, short of the full workload by the remainder.

The integral bucket writes are submitted asynchronously through the same handler and share a running position
that each write advances (`PK_workers.cc`, lines 818 to 819 and 951 to 996; `PK_workers.h`, lines 189 to 193;
`aio_handler.cc`, lines 419 to 451). In `write.cc`, a write whose start address lies strictly beyond the entry's
current end fails an in-memory address comparison, and code 17 is raised before the data transfer call at the
inspected sites (lines 57 to 58 and 103 to 106). The corresponding sites on the read path print an explanatory
message first (`read.cc`, lines 71 to 78); the write-path sites print none. A subsequent bucket write that begins
strictly beyond the end of a short pre-striped entry would therefore raise code 17 without an explanatory message.

The handler's worker function contains no exception handler, and its only explicit exception concerns an unknown
job type (`aio_handler.cc`, lines 258 to 466). An error raised inside a queued job therefore ends the process
instead of being passed back to the code that queued the job. That behaviour agrees with the uncaught exception,
the exit status −6 and the missing result file of E-01, but it does not show that the error was raised on this
thread. An error raised on another native thread or in an unguarded parallel region would leave the same retained
evidence, and the retained stack is empty.

### 3.3 Conditions

The pathway requires all four of the following conditions.

1. The pre-clamp divisor is positive. This is nine tenths of the engine's memory value as used before the clamp,
   and its positivity is a precondition of the row-count and remainder computations.
2. The row count is positive. Because the row count is an integer quotient, it is positive exactly when the
   workload size is greater than or equal to the pre-clamp divisor. The condition is inclusive; a strict
   inequality would be wrong.
3. The remainder is positive, that is, the pre-clamp divisor does not divide the workload size. This condition is
   separate from condition 2 and is not implied by it.
4. For at least one bucket, the start is not covered by the pre-striped extent as it stands when that bucket's
   first write is issued.

When conditions 1 to 3 are met, the pre-striped J extent ends at the row count multiplied by the divisor, in
doubles, short of the workload size by the remainder; the K extent is short by twice the remainder. When the row
count is zero, only the unconditional second call runs, the entry receives the full workload size and there is no
shortfall. A positive row count alone is therefore not sufficient.

A shortfall does not imply condition 4. Under the complementary rule in `write.cc` (lines 108 to 124), a write
that begins no later than the current end can lengthen the entry, provided that the end it requests is past the
current end and the routine's last-entry condition allows the extension. Where the requested end is past the
current end but another entry follows, the write instead raises the block-end code 18; in the remaining cases it
lengthens nothing. Coverage alone decides nothing: a shortfall confined to a region whose bucket begins at or
before the covered end leaves the pathway incomplete.

The handler runs its jobs on one worker thread in the order in which they were submitted, and it releases its lock
during the input/output calls (`aio_handler.cc`, lines 89 to 116, 209 to 229, 231 to 256 and 468 to 480). What
matters for condition 4 is therefore the order of submission rather than concurrent completion: writes submitted
earlier for one bucket can already have moved the end beyond the start of a bucket submitted later. This narrows
the ordering question to submission order, but it does not remove ordering as a factor.

### 3.4 Address arithmetic

Relative addresses are computed in `get_address.cc` in unsigned `size_t` arithmetic with no narrower intermediate
(lines 44 to 55). The global address routine in `get_global_address.cc` adds the page and offset components of the
entry start and of the relative address, and then subtracts the page length `PSIO_PAGELEN` (65 536, declared in
`config.h`) at most once, when the offset sum is at least one page length (lines 48 to 53). A normalized result is
therefore guaranteed under a sufficient condition, which is not an equivalence: the offset sum is below twice the
page length, and neither the page sum nor the offset sum overflows. Normalized inputs are one way to meet this
condition but not the only way. Offsets of 0 and 65 536, for example, sum to 65 536, which becomes the next page at
offset 0 although one input is not normalized. The result is not normalized when the offset sum reaches twice the
page length, and both sums are unsigned and wrap on overflow. This arithmetic neither measures the installed ABI
nor fixes the operands of E-01.

## 4. Hypotheses and disk capacity

The postmortem [25] keeps three hypotheses open, ranked as follows.

1. **A block or entry inconsistency in the integral input/output path.** This is retained broadly. It covers the
   caller's formation of operands and their overflow, a bad or stale entry state, submission order, relative
   addresses that are not normalized, and arithmetic. The pathway of Section 3 is one concrete branch inside this
   hypothesis, and nothing establishes that it, rather than another branch, operated.
2. **A filesystem, capacity or operating-system input/output condition.** The captured source paths do not support
   this as a direct raiser of code 17. In the inspected source, failures of the operating system's write, read and
   seek calls raise codes 12, 11 and 10 respectively, and each prints a distinct message (`rw.cc`, lines 94, 105,
   128, 140, 160 and 172; `volseek.cc`, lines 50 to 75). That reading is conditional on the installed build
   matching the source and on the error output having been emitted and captured completely. An indirect
   contribution is neither shown nor excluded.
3. **A workload-dependent trigger.** The conditions of the pathway depend on the workload size, so this hypothesis
   overlaps the caller branch of the first rather than competing with it.

Disk capacity remains a live possible contributor to E-01 and is neither established nor excluded. The observed
scratch allocation exceeded the largest pre-run estimate, and the free space at the instant of the abort was not
observed. No observation made in the postmortem or the survey weakens the capacity hypothesis, and none of the
candidate diagnostic observations considered would weaken it by itself.

## 5. The installed-build survey

### 5.1 Scope and method

After the postmortem, the project carried out a single bounded, read-only static inspection of the installed Psi4
1.11 build [20], to establish whether the entry points a diagnostic would need are available in it [26]. The
survey ran once, as a fixed set of 30 inspection commands with recorded limits on entries, text volume and time,
and its records show that it completed within those limits. It read files and ran standard inspection utilities:
file hashing and type identification, listing of the Mach-O header and load commands, listing of the export trie
and the symbol table, symbol demangling, and queries for the presence and version of the developer toolchain. It
compiled nothing, linked nothing, loaded nothing from the build and executed nothing from it.

### 5.2 Findings covered by the independent review

The survey records report the following findings, which the independent review of the survey result covered.

- **Core extension library.** The engine's core Python extension module, `core.cpython-314-darwin.so`, is a
  64-bit Mach-O dynamic library for arm64 with 18 declared dependencies, none of them a Psi4- or
  input/output-library-named library. The survey recorded its SHA256, which matched the project's earlier record
  of the file; that recorded value is the one listed for the file in [`method-config.json`](method-config.json).
  Its symbol table records 3 662 symbols, of which one is local, and the library has no `__DWARF` segment.
  Because the table records a single local symbol, it effectively omits local and hidden definitions, so the
  absence of a name from it cannot show that the image lacks a hidden definition of that name.
- **Headers.** The four installed input/output library headers, `aiohandler.h`, `config.h`, `psio.h` and
  `psio.hpp`, were captured in full. The installed `config.h` has the same SHA256 as the `v1.11` source capture of
  that file; no other header was compared with the source. The installed `aiohandler.h` declares the handler class
  `AIOHandler` without the `PSI_API` export macro, and `psio.h` declares the free functions `psio_init` and
  `psio_error` without it, whereas the classes `PSIO` and `PSIOManager` and the function `psio_get_address` carry
  it. `PSIO::set_pid` and `PSIO::set_default_namespace` are defined inline in `psio.hpp`. The definition of
  `PSI_API` itself is not in the four headers.
- **Checklist of 22 required names.** Twelve are present in the export trie and defined as external symbols in
  the symbol table: the `PSIO` constructor and destructor, `PSIO::shared_object`, `open`, `open_check`, `write` and
  `close`; `PSIOManager::shared_object`, `set_default_path`, `set_specific_path` and `psiclean`; and
  `psio_get_address`. The other ten were not found by the applied pattern: all seven items of the handler class
  (its constructor and destructor, `zero_disk`, `write_iwl`, `write`, `synchronize` and `wait_for_job`), the two
  header-inline functions `PSIO::set_pid` and `PSIO::set_default_namespace`, and the error function `psio_error`.
  The misses are consistent with hidden-visibility definitions of the handler class and the error function, which
  lack the export macro, and with inline functions, which need not be emitted at all. Failing to match a pattern
  does not prove that a definition is absent.
- **Type widths.** The installed widths of `double` and `int` remain unresolved. The survey found no static size
  assertion for either, and the target architecture is not substituted for them. They are written here as the
  unresolved installed quantities D = sizeof(double) and I = sizeof(int); the conventional values 8 and 4 are not
  assumed.
- **Link-time artifacts and toolchain.** Among the enumerated package file names there is no Psi4- or
  input/output-library-named shared library, and there are no CMake, pkg-config, static-archive (`.a`) or text-stub
  (`.tbd`) files. Apple clang 17.0.0 and the command-line developer tools are present, and `pkg-config` is not.
  The presence of a compiler is not evidence that a harness would compile, link or be ABI-compatible.
- **Enumeration coverage.** The survey enumerated 1 791 of the 6 260 file names listed in the package metadata
  before reaching a fixed entry limit. Every absence statement above is scoped to the enumerated names, and no
  absence across the whole installation follows.

### 5.3 Supplemental observations not covered by the independent review

The following observations were recorded in the acceptance record of the survey result after the independent
review of the survey, and they are not covered by that review; the survey status record states as much. They are
supplemental. They rest on searches of the retained export-trie and symbol-table captures, and on a count of the
retained package metadata, all of which are private.

- **No literal occurrence of `AIOHandler` or `psio_error`** in the retained export-trie or symbol-table captures.
  This is stricter than the pattern miss that the survey itself reported. It describes those listings only, and
  it cannot show that the image lacks a hidden definition.
- **Five names outside the checklist.** `PSIO::read`, `PSIO::filecfg_kwd`, `_default_psio_lib_` and
  `_default_psio_manager_` are present in the export trie and also in the symbol table. `PSIO::zero_disk` does
  not match the applied pattern, and that miss does not prove its absence. `PSIO_ZERO` also appears in both
  listings, as an external symbol, and is declared in the captured `config.h`. None of these presences
  establishes callability.
- **Coverage figure.** The enumeration coverage of Section 5.2 is quantified as 28.6 percent of the file names in
  the package metadata.
- **Byte reconciliation.** The two text totals recorded by the survey differ by 208 bytes, and the difference
  equals the length of the survey's final ledger event line, so the two totals are consistent.

### 5.4 Two verification scopes

Two verifications must be kept apart. The first is historical. The survey evidence manifest lists 76 local
bindings by SHA256, among them the 69 retained run-evidence files, and it excludes itself. The private survey
records report that all 76 bindings were verified. That verification was performed within the project's private
records, against files that are not present in this repository, and it was not repeated for this export.

The second is the verification performed for this export, and it is narrower. The SHA256 of each of the ten
records listed in Section 9 was recomputed from the copies used to prepare this document, and all ten matched the
values listed there. That check covers those ten records only. It re-examines none of the files they bind.

## 6. Six levels of evidence for an installed interface

The survey distinguishes six levels of evidence about an interface in the installed build. Each is distinct, and
none implies the next.

| Level | What it would establish | What the survey shows |
|---|---|---|
| Header declaration | A name and signature appear in an installed header | Four headers captured in full, with the declarations of Section 5.2 |
| Symbol-table definition | The image defines the name as an external symbol | Twelve of 22 checklist names; one local symbol recorded, so hidden definitions are not visible |
| Dynamic export | The name is in the export trie and available to the dynamic linker | The same twelve names; none of the handler-class names |
| ABI compatibility | A separately built caller agrees with the image on layouts, widths and calling conventions | Not established; D and I unresolved |
| Initialization and setup order | The state that a call requires can be brought up in a working order outside the engine | Not established; the declarations name the pieces but not a working order |
| Callability | A call made from outside the engine completes with the intended behaviour | Not established; nothing was called |

An exported name establishes name availability only. Neither a pattern miss nor a presence establishes callable
behaviour: a miss does not show that a definition is absent, and a presence does not show that the definition can
be reached, set up or called correctly from outside the engine.

## 7. Why no exact executable diagnostic could be specified

### 7.1 The conditional design and what it lacks

The postmortem drew up a conditional design for a fixed-position test that would discriminate restart from append
behaviour of the installed zero-fill [25]. Two zero-fill calls on one key, of C and then L rows with 0 < L < C,
would be followed by a write at a position P fixed in advance so that C·D < P ≤ (C + L)·D. Under restart
behaviour, as the source reads, the entry would end at C·D and the write would raise code 17; under append
behaviour it would end at (C + L)·D and the write would succeed. Two controls would follow a single zero-fill call
of C rows: a positive control writing at exactly C·D, and a negative control writing beyond C·D, which is past the
end on either reading. The three cases would each need a separate scratch unit and a separate process, because an
error raised inside the handler ends the process. The design was never completed, built or run.

The design cannot be completed from the evidence obtained, in four named respects.

1. **The installed widths.** D and I are unresolved, so the numeric constants C, L and P cannot be fixed.
2. **Write call and payload.** A variant faithful to the integral path would write through the handler's
   `write_iwl`, with label and value buffers and a shared address. The records do not capture whether label or
   value writes of zero size are permitted, so non-empty buffers of unfixed size would be required. A simpler
   variant with an explicit address would exercise less of the integral-write path.
3. **The standalone setup sequence.** What a process outside Python must do to bring the input/output library up,
   including its scratch path, namespace, process identifier and unit open status, is not established.
4. **Callability.** The handler-class entry points were not found among the exported names (Section 5.2), and
   whether any of the sequence can be called from outside the engine is not established.

The inspected Python binding (`export_psio.cc`, lines 41 to 70) exposes none of `read`, `write`, `zero_disk` or
`write_iwl`, so no test written only in Python can express the sequence. That binding is only one of fifteen such
export files, and whether some other binding route exists is left open. A harness built from copies of the source
would test the source text rather than the installed build. This determination is a statement about the current
evidence and its gaps. It does not assert that a diagnostic is impossible.

### 7.2 The declined guard-only replay

A narrower option was identified: a replay of the relevant write sequence through the exported low-level
`PSIO::write`, starting at `PSIO_ZERO` [26]. It was declined [27]. Such a replay would exercise only the exported
block-start guard. It would not test the installed `AIOHandler` restart-versus-append behaviour, which is the
mechanism at issue, so it could not discriminate that mechanism.

Two further limits apply to any fixed-position test. Such a test could not identify the cause of E-01, and a
synthetic demonstration of underallocation would not by itself weaken the capacity hypothesis. A result that did
not reproduce the error would not clear the pathway either, unless condition 4 of Section 3.3, the uncovered
bucket start, were independently demonstrated to have been met in E-01.

## 8. Ranked unresolved gaps

The private records rank the unresolved gaps as follows.

1. **Installed-link feasibility:** the exported symbols, headers, toolchain and ABI, including the installed
   widths D and I.
2. **Standalone setup:** the setup order of the input/output library and the exact call signatures as installed.
3. **Binary identity:** whether the installed binary corresponds to the `v1.11` source text. Apart from the one
   header whose hash matches, the source text is not shown to be the installed code, and finding a string in the
   binary would not demonstrate a live control path.
4. **Engine sizes:** the internal PK memory operand after any adjustment from the known configured value of
   2,000,000,000 bytes, the integral buffer length (`IWL_INTS_PER_BUF`) and the sizes of the `Label` and `Value`
   types. These would be needed to evaluate the divisor, the row count and the remainder for E-01 or for any
   configuration meant to meet the conditions of Section 3.3.
5. **Operating branch:** which branch of the first hypothesis operated, whether entry state, submission order or
   operands.
6. **Indirect contribution:** an indirect operating-system or capacity contribution, which is neither shown nor
   excluded.
7. **E-01's operands:** the actual operands, write order and failing write of E-01, which cannot be recovered from
   the retained records.

## 9. Provenance and limits

The activity behind this record was limited as follows. The postmortem was a source-level assessment of
version-pinned source text and the retained run records; nothing was executed, compiled, linked, installed or
delivered for it. The installed-build survey was the single bounded, read-only static inspection described in
Section 5.1. It read files and ran standard inspection utilities, and it compiled nothing, linked nothing, loaded
nothing from the build and executed nothing from it. No diagnostic harness was built, linked, loaded or executed
at any point. No chemistry, engine run or calculation was performed at any point in the postmortem, the survey or
the closeout.

Every chemistry-dependent result of E-01 remains INDETERMINATE. Output from language models, including any text
produced in preparing this record, is never physical evidence
([docs/evidence-policy.md](../../docs/evidence-policy.md)). The source-level pathway is a hypothesis without
supporting calculation or observation, and the survey findings concern software artifacts, not chemistry.

This document and the related revisions of the repository are derived from ten private, hash-bound project
records, listed below by description and SHA256 only. The project's orchestration records, the raw captures of the
survey, the source captures and the other records that these ten bind remain private and are not published. The
SHA256 values below were recomputed for this export (Section 5.4).

| Private record | SHA256 |
|---|---|
| Postmortem source assessment (controlling record) | `629601e688b5f22379ca408f2eb43bfa112ff67ee106c1bb8a7a077095bf0d37` |
| Independent review of the postmortem source assessment | `4ce5f8469639733d4b6c90b3e8e9e94326eec9bf130c119c316cba62f49e2532` |
| Installed-build survey observations | `f3a0d09fdac5fa15c9c88e0f2870b18e67c7c6cde77afe329770149883153045` |
| Installed-build survey diagnostic-feasibility determination | `adb4a6eee85de8b450d04db55b1809e482500dccdd1ce4c532a37624e0ecc3d3` |
| Installed-build survey evidence manifest (76 bindings, self-excluded) | `e99807c15ba01b76b9d43181a10d6512f5297ecac385bef7cfd7c30d5fb954d7` |
| Independent review of the survey result | `37c77fe100f9df814d57b912e0b8f7b861c2aafcf432e379d0dc3842ba68a546` |
| Acceptance record of the survey result, with supplemental findings | `6b28b3a9e2157cc60ac13d2c3cdf84b22c346cc5f17c87cb19faddb200165dc8` |
| Survey result status record | `2230695b2dcef3f49cef380b4707447cd467b989547829b2b43ac13c618485c6` |
| Terminal disposition of the diagnostic route | `fb958eefbe078bc7a2bc8cedbe7b0bc7a3ff7495ad5fd0a60259f149f29e49cc` |
| Closure record of the attempt | `9261fa1903901f7b4eb660be56e0e612ba4f93b9062bc9c5782bc6114df15a87` |
