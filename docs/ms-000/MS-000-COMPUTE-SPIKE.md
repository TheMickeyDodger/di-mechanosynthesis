# MS-000 Compute Spike: Cowie IR-C2 as a reproduction target

Status: public adaptation of the MS-000 feasibility study. MS-000 scientific gate: **PENDING**
([Section 8](#8-ms-000-scientific-gate-and-ms-001-prospective-protocol)). Faithful-reproduction readiness:
**BLOCKED** on missing inputs and missing parity evidence ([Section 5](#5-reproduction-readiness-and-scope-options)).
This document does not authorize MS-001 work.

Companion documents: [ARCHITECTURE.md](ARCHITECTURE.md), [EVIDENCE-POLICY.md](EVIDENCE-POLICY.md),
[OPEN-SOURCE-LANDSCAPE.md](OPEN-SOURCE-LANDSCAPE.md), [SOURCE-LEDGER.md](SOURCE-LEDGER.md),
[SMOKE-AND-ENVIRONMENT-RECORD.md](SMOKE-AND-ENVIRONMENT-RECORD.md).

Evidence-class tags (defined in EVIDENCE-POLICY.md): `[EXP]` experimentally demonstrated, `[COMP-REPRO]`
computationally reproduced, `[COMP-PRED]` computationally predicted, `[LIT]` literature-derived, `[AGENT]`
agent-proposed, `[SPEC]` speculative, `[GAP]` unavailable input recorded as a gap. Tags name the underlying evidence
type. Every Cowie-derived statement here has literature provenance, so `[EXP]` means the paper reports an
experimental observation, never that this project observed it. This document paraphrases the source material and
does not reproduce paper text, figures, or supplementary files.

---

## 1. Primary source and what was actually retrieved

| Item | Finding | Locator |
|---|---|---|
| Paper | Cowie et al., arXiv:2605.27250, cond-mat.mtrl-sci | [S1] abs page |
| Version / date | v1, submitted 2026-05-26; no later version listed | [S1] abs page, submission line |
| Retrieved forms | abs page, HTML v1, PDF v1 (11 pages by the PDF page-tree count), all retrieved 2026-09-16; digests in SOURCE-LEDGER.md | [S1], [S2], [S3] |
| Supplementary Information | The abs page Comments field states that the SI is provided on request. **It was not obtained for MS-000.** This is the source status for this study, not a statement about availability to others. | [S1] Comments field |
| Methods section | **Verified absent.** The body of [S2]/[S3] has six science sections, referred to below by number: §1 single-site C2 donation; §2 stepwise patterning; §3 the donation mechanism; §4 extension to IR-C4; §5 reproducibility and outcome statistics; §6 placement/bonding control claims and off-target analysis. These are followed by acknowledgements, funding, author contributions and references. No Methods, Materials and Methods, or Computational Methods heading exists. | [S2] body; [S3] heading scan |
| Trajectory-simulation method label | `QM/MM xTB(GFN0)/DFT (ωB97X-D3)` is the **only methodological specification the main text gives for the IR-C2 and IR-C4 trajectory simulations**. | [S2] Fig. 3 caption, first sentence; Fig. 4 caption, panels D–J |
| Other stated levels | A separate molecular-proxy bond-energy comparison is stated at the ωB97X-D functional with the Def2-TZVPP basis (Section 2.6). The STM image simulations and the DFT formation predictions carry no level in the main text. | [S2] §6, para 4 |
| Internal dates (observed metadata) | The PDF's first page carries the date 2026-05-27; the HTML header carries 2026-08-24; the abs page gives a submission date of 2026-05-26 and lists only v1. Reported as observed; the cause of the differing internal dates was not established. | [S3] p.1; [S2] header; [S1] |

**Consequence carried through every document:** coordinates, atom mapping, layer/partition definition, link atoms,
embedding scheme, cluster/slab choice, charge and spin, basis set, ECPs, dispersion damping variant, constraint
definitions, convergence criteria, step sizes, and software identities/versions for the trajectory simulations
are **not available to this study**. Each is a `[GAP]`. No number that is not in [S2]/[S3] or [S4]/[S5] (Barrera,
kept separate) appears in this document.

### 1.1 Reference-list entries with no citing paragraph in the retrieved text

The HTML reference list [S2] shows, for each entry, the paragraph(s) citing it. Entries 1–37 are cited from
paragraphs present in the rendered main text. Entries 38–57 are cited only from a locator (`p52.2.3`, some also
`p52.2`) that does not correspond to any paragraph in [S2] or the 11-page [S3]; the names Gaussian 16 and TeraChem
occur only in the reference list of [S3]. The citing paragraph is therefore outside the retrieved text, which is
consistent with it belonging to the unobtained SI. What this does and does not establish:

- The bibliography includes, among entries 38–57: Tersoff–Hamann STM theory (39); three TeraChem GPU
  quantum-chemistry papers (40–42); B3LYP (43); ωB97X-D (44); a Pople-family basis paper (45); Wadt–Hay ECPs
  (46); the ωB97X-D3 functional paper (47); Weigend Coulomb-fitting sets (48); Gaussian 16 (49); ASE (50); WKB
  theory (51–53); climbing-image NEB (54); three Si(100)/H papers (55–57). `[LIT]`
- It does **not** establish which code computed the trajectories, which basis/ECP applied to which layer, or
  whether NEB was used for any main-text result. **The main text does not say what performed the QM/MM.**

### 1.2 Gaussian 16 (ref 49) and ASE (ref 50): verified, with consequence

- Ref 49 is Gaussian 16 (Frisch et al., 2013; Gaussian, Inc., Wallingford, Connecticut). Ref 50 is the ASE paper (Hjorth
  Larsen et al., J. Phys.: Condens. Matter 29, 273002, 2017). `[LIT]` [S2] refs [49], [50]; [S3] reference list.
- Consequence: Gaussian 16 is commercial. Its presence in the bibliography means the original pipeline **possibly**
  involved a commercial code. An open-source stack is therefore a **methodological deviation from a
  possibly-commercial original pipeline**, not a re-run. This document does **not** assert that Gaussian performed
  the QM/MM; the paper does not say what did.

### 1.3 Refs 29, 36, 37: what was read, and what they do not specify

| Ref | Identity (verified) | What was actually read | What it specifies | What it does not do |
|---|---|---|---|---|
| 29 | Barrera et al. 2025, arXiv:2512.24431, submitted 2025-12-30; the IM-STM method paper the Cowie experiment follows ([S2] §1, para 1) | Full PDF retrieved (47 pages by page-tree count, [S5]); read: Methods → *Computational Modeling* (p. 11 range) and SI §2 *Computational Modeling* with Fig. S1 (p. 19 range). Abstract page [S4]. | See Section 1.4 | Its model is a different reaction (H abstraction), a single-level DFT cluster scan, and a different functional/basis. **None of its settings transfer to Cowie IR-C2.** |
| 36 | Senn & Thiel 2009, Angew. Chem. Int. Ed. 48(7), 1198–1229, doi 10.1002/anie.200802019 | Publisher page returned HTTP 403 (not read). Crossref metadata and abstract retrieved [S6]: a Review of the general methodological aspects of QM/MM, its use in optimization and simulation, and application areas, with a biomolecular focus. | General QM/MM methodology (review) | Cited once by Cowie, in the sentence introducing the QM/MM model ([S2] §3, para 1). It does not define the Cowie partition, embedding, link atoms or coupling. Full text not obtained. |
| 37 | Svensson et al. 1996, J. Phys. Chem. 100(50), 19357–19363, doi 10.1021/jp962071j (ONIOM) | Publisher page returned HTTP 403 (not read). Crossref metadata retrieved [S7]; no abstract available via Crossref. | The original multilayer ONIOM method paper | Same single citation site as ref 36. Citing ONIOM does not state that a subtractive ONIOM scheme was used, nor any layer definition. Full text not obtained. |

**Plain statement:** refs 36 and 37 are general methodology citations. They do **not** specify the Cowie setup.

### 1.4 Barrera (ref 29) computational model, kept separate from Cowie

`[LIT]` from [S5], Methods → *Computational Modeling*, and SI §2 / Fig. S1. Barrera's calculations: single-level
DFT with the B3LYP hybrid functional, the 6-311G(d,p) basis set, Grimme D3 dispersion with Becke–Johnson damping,
run in TeraChem 1.96H, with a wavefunction convergence threshold of 1.0e-8 a.u. and a two-electron integral
threshold of 1.0e-12. The potential-energy surface is a mesh of constrained H-atom positions over a reduced
molecular model (germa-adamantane cage with a pendent ethynyl radical) and a small Si(100) proxy with anchored
atoms (Fig. S1); SI Fig. S12 presents that H-transfer surface.

Methodological distinctions from the Cowie trajectory label, and why nothing transfers:

| Aspect | Barrera ref 29 (H abstraction) | Cowie IR-C2 trajectory label |
|---|---|---|
| Reaction | Removal of one surface hydrogen off the Si proxy by the ethynyl radical | Donation of C2 onto an IR-DB pair, Ge–C cleavage, relaxation |
| Levels | One level: B3LYP/6-311G(d,p)-D3(BJ) | Two levels: GFN0-xTB and ωB97X-D3 in a QM/MM scheme (partition unstated) |
| Model | Reduced molecule + small Si(100) proxy, anchored atoms | Unstated (cluster/slab, size, legs) |
| Coordinate | Constrained mesh over H positions | Externally driven separation z with approach and retraction |
| Code | TeraChem 1.96H | Unstated |

These Barrera values are recorded only to characterise the cited method context. They are **not** Cowie IR-C2
settings and are not used anywhere in the MS-001 plan.

---

## 2. Extraction from the primary source (paraphrased, with locators)

Section numbers (§1–§6) refer to the six body sections in the order given in the Section 1 table.

### 2.1 Substrate, surface reconstruction, dangling-bond pair

| Element | Content | Class | Locator |
|---|---|---|---|
| Inverted-mode geometry | Tool molecules sit on a flat Si(100) sample; an H-passivated Si(100) probe chip (SPC), whose apex is flat and crystalline, is brought above them. The SPC apex is the build site; fragments transfer to and from it. | `[EXP]` | [S2] Fig. 1 caption (A); §1, para 1 |
| Build-site surface | Hydrogen-terminated Si(100) with the 2×1 reconstruction, on the SPC. | `[EXP]` | [S2] §1, para 3 |
| DB pair geometry | Two dangling bonds are created by voltage pulses and arranged inter-row, i.e. spanning a trough between dimer rows; the tool molecule plays the role of the STM tip in the electron-induced desorption. The intra-row alternative is not the IR-C2 precursor. | `[EXP]` | [S2] §1, para 3; Fig. 1 caption (C) |
| Reference feature | A single unchanged DB close to the target region acts as a stationary visual reference. | `[EXP]` | [S2] §1, para 2 |
| Build-site coordinates, slab/cluster size, model termination | Not given in the main text. | `[GAP]` | SI not obtained ([S1]) |

### 2.2 Tool composition, preparation, de-iodination, characterization

| Element | Content | Class | Locator |
|---|---|---|---|
| Tool molecule | EAOGe-C2I: Ge-substituted adamantane bearing a C2 group, three legs ending in OH, and an iodine cap (synthesis in ref 31). | `[EXP]`/`[LIT]` | [S2] §1, para 1 |
| Anchoring | The OH legs bind the molecule to the sample surface; a subset stands vertically, with its Ge–C2–I axis normal to the surface, and appears tallest in IM-STM. | `[EXP]` | [S2] §1, para 1 |
| Leg configuration in the model | The Fig. 3 arrangement is just one among several low-energy leg-binding configurations, shown as representative. | `[COMP-PRED]` (model choice) | [S2] Fig. 3 caption, penultimate sentence |
| De-iodination | Performed with the tool positioned elsewhere on the sample, by raising the bias, which exposes the C2 radical; the imaging modality changes (iodinated tool resolves dimers; de-iodinated tool resolves rows only). | `[EXP]` | [S2] §1, para 3; Fig. 1 caption (D) |
| Tool-state characterization | Modality changes track the tool termination and are reported as reproducible across sequences, with examples in the SI. | `[EXP]` (examples not obtained) | [S2] §1, para 2 |
| Tool coordinates, leg attachment sites, iodine handling in the model | Not given. | `[GAP]` | SI not obtained |

### 2.3 Starting geometry, build-site definition, species present

| Element | Content | Class | Locator |
|---|---|---|---|
| Alignment | Experiment: the de-iodinated tool is centred under the IR-DB pair. Model: the tool's distal C atom is centred under the pair (Fig. 3A). | `[EXP]` / `[COMP-PRED]` | [S2] §1, para 4; §3, para 1 |
| Species | Build side: H:Si(100)-2×1 with an IR-DB pair and a nearby reference DB. Tool side: EAOGe-C2• (Ge, C2, cage, three OH legs) bound to the sample surface. Elements: Si, H, C, Ge, O (I before de-iodination). | `[EXP]` | [S2] Fig. 1 caption; §1, paras 1, 3 |
| Product | IR-C2: a C2 unit bridging the IR-DB pair across the trough. The assignment rests on five stated lines: modality evolution, agreement with a simulated filled-state STM image (hexagonal feature, twofold mirror symmetry, trough-centred, little height contrast), exclusion of known defects and alternative binding geometries, prior independent formation of IR-C2 on bare Si(100) (ref 35), and predicted formation. | `[EXP]` assignment supported by `[COMP-PRED]` | [S2] §1, para 5; Fig. 1 caption (F–H) |
| Lateral targeting tolerance | Deferred to the SI by the paper. | `[GAP]` | [S2] §6, para 3 |

### 2.4 Operating conditions

| Element | Content | Class | Locator |
|---|---|---|---|
| Temperature | IM-STM at 4 K. | `[EXP]` | [S2] §1, para 1 |
| Bias/current during mechanosynthesis | Bias 0 V (no tunneling current); z-controller disengaged. | `[EXP]` | [S2] §1, para 4 |
| Imaging conditions | Sample bias +3.2 V; current 10 pA; imaging tool: an intact EAOGe-C2I. | `[EXP]` | [S2] Fig. 2 caption |
| Depth-sampling increment | Maximum approach depth raised by 50 pm per cycle, stated to be less than half the C2 dimer length of about 120 pm; a constant-current image after each increment. | `[EXP]` | [S2] §1, para 4 |
| Product stability | IR-C2 persists over days and weeks at 4 K; tolerates sample biases of about −3 to +4 V and currents of 10–100 pA, with various tool terminations. | `[EXP]` | [S2] §2, para 2 |
| Model temperature, thermostat, dynamics vs static relaxation | Not stated. | `[GAP]` | SI not obtained |

### 2.5 The approach/retraction coordinate and how it is driven

| Element | Content | Class | Locator |
|---|---|---|---|
| Experimental drive | Cycles of approach and retraction starting from a large separation, deepening by 50 pm per cycle, imaging after each, until modality and apparent height change. Open loop (z-controller off). | `[EXP]` | [S2] §1, para 4 |
| Model coordinate | z is the distance between the two silicon surfaces; z0 is the value at which the initial C–Si bond is formed; the energy profile is plotted against z−z0. | `[COMP-PRED]` | [S2] §3, para 1; Fig. 3 caption (E) |
| Experiment-to-model relation | Because of the 50 pm stepping, the smallest separation sampled satisfies z−z0 > −50 pm; at that depth the Ge–C2–Si link is only transiently compressed relative to the bond-formation point, leaving the proposed mechanism unchanged. | `[COMP-PRED]` reasoning about an `[EXP]` protocol | [S2] §3, para 2 |
| How z is imposed in the model (fixed atoms, step size, per-step relaxation, explicit sample-side Si, leg constraints) | Not stated. | `[GAP]` | SI not obtained |

### 2.6 Intermediate sequence: bonds formed/cleaved, relaxation steps (the paper's model)

All rows are `[COMP-PRED]`: the paper labels this a proposed mechanism from the QM/MM model ([S2] §3, paras 1–2;
Fig. 3 caption).

| Step | Content | Locator |
|---|---|---|
| A | Tool positioned with its distal C under the IR-DB pair. | Fig. 3 caption (A) |
| B | On approach, at z = z0, the initial C–Si bond is formed with a sharp potential-energy drop. | §3, para 1; Fig. 3 (B) |
| C | On retraction, the strained junction breaks at Ge–C, leaving an upright pendent C2• on the surface, transiently stabilised through a radical-coordinative contact with the residual EAOGe• fragment. | §3, para 1; Fig. 3 (C) |
| D | With further retraction that contact weakens until the pendent C2• settling into IR geometry is described as barrierless (supporting calculations in the SI), giving IR-C2. | §3, para 1; Fig. 3 (D) |
| Summary claim | The transfer is described as net downhill overall, with every barrier surmounted by mechanical work done through z. | §3, para 1, last sentence |
| Alternative at larger depth | Beyond the sampled depth, IR-C2 can still form, with a second Si–C bond forming while Ge–C is still intact (SI calculations). | §3, para 2 |
| Relaxation-orientation factors | The pendent's tilt is attributed to the anchoring Si's sp3 preference and to where the post-donation EAOGe• sits laterally, steering it toward the other DB of the pair rather than adjacent dimers (SI calculation). | §6, para 5 |
| Bond-competition proxy | Molecular-proxy calculations at ωB97X-D/Def2-TZVPP give Ge–C 5.200 eV versus Si–C 5.139 eV; the paper notes the near-degeneracy and that Ge–C cleavage is nonetheless the empirically preferred outcome. This proxy level is **not** the trajectory label. | §6, para 4 |

**Mandatory framing preserved:** the words barrierless and net downhill are statements about the model's energy
profile. The experiment observes outcomes (modality changes, product features, yields), not barrier heights. No
barrierlessness has been experimentally observed. The relaxation-step supporting calculations are in the
unobtained SI. Fig. 3E's energies were **not digitized for MS-000, and no numeric tables were retrieved**.

### 2.7 Experimental observations vs computational proposals, separated

| Experimentally observed (`[EXP]`, per [S2]) | Locator |
|---|---|
| IR-DB pair patterning on the H:Si(100)-2×1 SPC apex; de-iodination modality change; a dark feature where the IR-DB pair had been, after donation; unchanged reference DB | §1, paras 2–4; Fig. 1 B–E |
| Close-up image with a second, intact tool of a trough-centred feature assigned to IR-C2 | §1, para 5; Fig. 1F |
| Patterning of two and three IR-C2 in a row, and nine C2 units (18 C atoms) arranged as an X | Fig. 2 caption |
| Stability windows (Section 2.4) | §2, para 2 |
| Yields with Wilson-score 95% intervals, exactly as reported: IR-C2 93% (184/197, 89–96%); 2IR-C2 97% (71/73, 91–99%); IR-C2/C4 92% (45/49, 81–97%); 2IR-C4 84% (27/32, 68–93%) | §6, para 1; Fig. 5 caption (I–L) |
| Off-target counts, exactly as reported: H abstraction 9 of 351 interactions (3%, 95% CI 1–5%); Si-atom abstraction believed 1 of 351 (0.3%, 95% CI 0.05–2%); other isolated outcomes 11 of 351 (3%, 95% CI 2–6%); one reproducible off-target C2 product during 2IR-C4 attempts | §6, paras 3, 4, 6 |
| Pendent C2H/C4H products not observed | §6, para 5 |

| Computationally proposed (`[COMP-PRED]`, per [S2]) | Locator |
|---|---|
| The A→D mechanism and the E(z−z0) profile | Fig. 3; §3 |
| Simulated filled-state STM image and calculated geometry of IR-C2; IR-C2 predicted to be under less strain than alternative configurations | Fig. 1 caption (G, H); §2, para 2 |
| Predicted IR-C2 formation under the experiment's conditions | §1, para 5 |
| IR-C4 mechanism (Fig. 4 D–J); IR-C4 predicted lowest among alternatives by over 2 eV (SI); trajectory calculations predicting its formation | Fig. 4 caption; §4, paras 2–3 |
| The only predicted competing bond at approach: C–H with a neighbouring passivated Si | §6, para 3 |
| Proxy bond energies (Section 2.6) | §6, para 4 |

| Proposed without stated computational support (`[LIT]` provenance over `[SPEC]` underlying evidence, per [S2]) | Locator |
|---|---|
| A pair of candidate failure routes for the reproducible 2IR-C4 off-target product (bonding to the IR-C4 instead of the IR-C2, or the pendent C4• coupling to the neighbouring IR-C4); the paper offers them as possibilities and states that further work is needed to distinguish them; no calculation supporting either is stated | §6, para 6 |
| Possible contributors to off-target H abstraction (tool lateral flexibility, hydrogen tunneling, limited positional control); offered as factors that could contribute | §6, para 3 |

Statistical note: counts are per interaction as reported; **no independence between events is assumed here**, and
no throughput, latency or per-step time is stated in the paper, so none is used.

### 2.8 Methods actually stated vs methods merely cited

| Stated in the main text | Merely cited (bibliography only; usage not stated) |
|---|---|
| Trajectory label `QM/MM xTB(GFN0)/DFT (ωB97X-D3)` (Fig. 3, Fig. 4 captions) | Gaussian 16 (49), ASE (50), TeraChem (40–42), CI-NEB (54), Tersoff–Hamann (39), B3LYP (43), ωB97X-D (44), Pople basis (45), Wadt–Hay ECP (46), ωB97X-D3 paper (47), Weigend fitting sets (48), WKB (51–53) |
| A QM/MM model, with refs 36 and 37 (§3, para 1) | refs 36, 37 define no setup (Section 1.3) |
| Molecular-proxy level ωB97X-D/Def2-TZVPP (§6, para 4); code not stated | Not applicable |
| Simulated filled-state STM image (§1, para 5); method not stated | (39) is the only STM-theory entry and is cited from the unretrieved paragraph |
| Trajectory calculations for IR-C4 (§4, para 2); method not stated | Not applicable |

### 2.9 Uncertainties (all `[GAP]` unless noted)

1. **QM/MM layer assignment is not stated anywhere in the paper.** The label gives two levels of theory, not which
   atoms are treated at which level. Reading DFT as the high layer and GFN0 as the low layer is an inference, and
   the written order is the reverse of that reading. This document asserts **no partition**. Also unstated: link
   atoms/boundary treatment; embedding (mechanical vs electrostatic; subtractive vs additive); cluster vs slab;
   total charge; spin state (tool radical, DB pair, pendent radical: the multiplicity used is unknown).
2. Basis set(s) and ECPs for Ge and I in the DFT layer: unstated.
3. Dispersion variant: the label names ωB97X-D3 (ref 47); the damping form and parameters used are unstated.
4. Which code performed which calculation: unstated (Sections 1.1–1.2).
5. Optimizer, constraints, model z step, per-step and SCF convergence criteria: unstated.
6. Whether Fig. 3E is a relaxed static scan or a dynamical trajectory, and what the IR-C4 trajectory calculations
   are: unstated.
7. Leg binding configuration: acknowledged by the paper as one of several (Fig. 3 caption). `[COMP-PRED]` with
   stated non-uniqueness.
8. Lateral targeting tolerance: SI only.
9. Hydrogen tunneling as a contributor to off-target H abstraction: offered by the paper as one of three possible
   factors; `[SPEC]` in its own framing.
10. Independence of successive interactions in the yield statistics: not claimed by the paper; not assumed here.

---

## 3. Core mapping table

One row per requirement. Column 3 names candidates evaluated in OPEN-SOURCE-LANDSCAPE.md. Column 5 is a plan
**conditional** on the parity gaps in Section 4, on the scope decision in Section 5, and on human authorization.

| # | Cowie method element (locator) | Required capability | Candidate open-source implementation | Known gap | MS-001 plan (conditional) |
|---|---|---|---|---|---|
| M1 | H:Si(100)-2×1 SPC apex carrying the IR-DB pair; Fig. 1B–C | Atomistic model with atom identities; cluster/slab, size, termination | ASE (`ase.build`, `Atoms`, tags) | Cowie geometry unknown `[GAP]`; any model is `[AGENT]` | Construct a candidate model; label `[AGENT]`; Reviewer signs off on the model definition before Stage 2 |
| M2 | EAOGe-C2• with three OH legs on the Si sample; representative leg configuration (Fig. 1A; Fig. 3 caption) | Molecular builder; treatment of legs and sample-side surface | ASE; engines for relaxation | No coordinates; leg attachment non-unique; explicit-vs-implicit legs and their level unknown `[GAP]` | Model one leg configuration; record it as a choice and a deviation |
| M3 | Two-level energetics per the trajectory label (Fig. 3, Fig. 4 captions) | GFN0-xTB energies/forces; ωB97X-D3 energies/forces (range-separated hybrid + D3); a coupling scheme | GFN0: xtb `--gfn 0` or CP2K `GFN_TYPE 0`. DFT: CP2K via libxc `WB97X_D3` with HF and VDW sections, or Psi4 for cluster-only checks. Coupling: three existing subtractive-composition candidates (ASE `SimpleQMMM`; CP2K `MIXED`/`GENMIX` with `MAPPING`; Py-ChemShell `NLayerSubtractive`), none yet shown to compose GFN0 with ωB97X-D3 for this system (P3b) | Partition, embedding, link atoms, HFX/range-separation/D3 damping/basis/ECP all unstated; **no implementation can be shown equivalent** (P1–P3); coupling route not yet demonstrated (P3b) | No parity claim. Any scheme is a declared deviation, frozen in provenance, run only under an authorized scope option and only once a P3b route is demonstrated and its coupled gradient validated |
| M4 | Driven coordinate z with approach then retraction (Fig. 3E; §3) | Externally driven constrained relaxation at a sequence of fixed z, keeping both branches and atom identity | ASE constraints (`FixAtoms` on remote layers of each body; rigid displacement of one body per step) with ASE or Sella minimization; engines from M3 | Drive definition unstated (P4) | Driven-scan protocol with explicit fixed sets, step, per-step criteria and branch bookkeeping; **no NEB substitute** |
| M5 | Event sequence A→D (Fig. 3A–D) | Connectivity tracking along the driven path with atom identity | ASE neighbor lists / OVITO bond analysis on computed coordinates | Bond cutoffs are an analysis choice `[AGENT]` | Report qualitative event order and connectivity (Section 8.4) with cutoffs recorded and their selection procedure (8.6) |
| M6 | Energy profile E(z−z0) (Fig. 3E) | Per-step total energies | Same as M3 | Cowie profile not digitized; no numeric tables retrieved `[GAP]` | Report the sign of energy changes at events; **no numerical agreement claim** |
| M7 | Relaxation described as barrierless at large z (model; SI calculations) | Supporting saddle/barrier analysis at fixed z | ASE NEB (`climb=True`) or Sella | Supporting analysis only; a zero-force MEP is not the driven trajectory | Optional, after M4, labeled supporting analysis |
| M8 | Alternative pathway at larger depth (§3, para 2) | Deeper driven scan | Same as M4 | Mechanical-variable perturbation | Defer to MS-003 |
| M9 | Filled-state STM simulation (Fig. 1G) | Tersoff–Hamann-type image | Not in the required list; CP2K can write cube files | Method unstated `[GAP]` | Defer; not required for M5 |
| M10 | Molecular-proxy bond energies at ωB97X-D/Def2-TZVPP (§6, para 4) | Molecular hybrid DFT with a def2 basis | Psi4 (`WB97X-D` listed) or CP2K | Code/ECP details unstated; not the trajectory level | Optional engine sanity check; not an MS-001 gate item |
| M11 | Yield statistics with Wilson intervals (Fig. 5 I–L) | Evidence bookkeeping only | DI evidence layer | Not applicable | Cite exactly; never combine with computed results |
| M12 | Provenance of any computed result | Job execution and provenance graph | AiiDA (`aiida-core`, `aiida-cp2k`) | Plugin compatibility untested `[GAP]` | AiiDA owns scientific job execution and provenance; DI records evidence class and review |
| M13 | Visualizing configurations | Render computed coordinates | ASE and OVITO Python module / Basic | Not applicable | Render computed coordinates only |

---

## 4. Parity gaps that keep the stack CONDITIONAL

Each gap lists what evidence would close it. None is closed. **CP2K availability is not proof of parity.** Any
alternative engine or model is a **documented methodological deviation** until equivalent implementation is
verified against a stated Cowie setup, and the Cowie setup is not stated. Tool locators `[S-…]` are in
SOURCE-LEDGER.md.

| Gap | Statement | Evidence that would close it |
|---|---|---|
| **P1 GFN0 through the chosen adapter** | tblite's built-in methods are GFN1-xTB, GFN2-xTB and IPEA1-xTB only [S-tblite-methods]. The xtb CLI selects the parametrisation with `--gfn INT`, default 2 [S-xtb-cli], and locates `param_gfn0-xtb.txt` through `XTBPATH` [S-xtb-setup]. xtb-python exposes `GFN0xTB = 3` and requires that parameter file via `XTBPATH` [S-xtbpy-api]; its ASE calculator defaults to GFN2-xTB [S-xtbpy-ase]. CP2K's `GFN_TYPE` accepts `0`, `1` or `TBLITE` and defaults to `1` [S-cp2k-xtb]. **No route defaults to GFN0.** A silent fallback to GFN2 (or to GFN1 in CP2K) is a **correctness failure**, not a nuance. | **GFN0 identity provenance** captured in the run record: the selector as passed, the program's own printed method banner, the program version, and the parameter provenance (file path and sha256; for xtb the `param_gfn0-xtb.txt` header declares level 0 and the GFN0-xTB name; the main-branch file digest is in SOURCE-LEDGER.md and must be re-recorded for the installed release). A numerical difference from a GFN2 run is **neither sufficient proof nor guaranteed** and is not the identity test. |
| **P2 Hybrid exchange / dispersion / basis / ECP** | libxc evaluates only the semilocal part of a hybrid; the exact-exchange admixture is supplied by the calling code [S-libxc-manual]. libxc defines `HYB_GGA_XC_WB97X_D3` (id 399) [S-libxc-funcs]; CP2K lists `WB97X_D3` among its libxc hybrid GGA entries and requires hybrid scaling and potential types to be set in its HF section [S-cp2k-xc], [S-cp2k-hf]; D3 is a separate pair potential with `TYPE` in {DFTD2, DFTD3, DFTD3(BJ), DFTD4}, default DFTD3(BJ), with a reference-functional parameter lookup [S-cp2k-vdw]. Whether the range-separation parameters, exact-exchange fractions, D3 damping variant/parameters, basis and Ge/I ECPs match the Cowie run **cannot be established**: none are stated. | (a) A frozen input with explicit HF fraction/interaction potential and D3 parameters, cross-checked against the ωB97X-D3 definition in ref 47; (b) a molecular cross-engine check (Psi4 `WB97X-D3` vs the CP2K input on one small molecule) to a tolerance selected by the procedure in 8.6; (c) explicit basis/ECP declarations for Ge and I. Even then, parity to Cowie stays **unknown**; only internal consistency is established. |
| **P3 QM/MM coupling scheme and partition** | Partition, embedding, link atoms, charge and spin are unstated (2.9 item 1). CP2K's QMMM `E_COUPL` choices (mechanical/point-charge, `COULOMB`, `GAUSS`, `S-WAVE`, `POINT_CHARGE`) couple a QM region to a **classical MM** region [S-cp2k-qmmm]; whether Cowie's low level is a force field, GFN0-xTB in a subtractive scheme, or something else is not stated. | Only the SI or the authors can close this. Until then, the only acceptable content is a gap statement plus, if the human selects scope option B (Section 5), a **declared deviation**: a fully specified scheme. |
| **P3b Coupling implementation route** | Separate from P3. CP2K's xTB module, libxc hybrid DFT and QMMM section are documented as separate features ([S-cp2k-xtb], [S-cp2k-xc], [S-cp2k-qmmm]); the QMMM section couples to a classical MM region. **Three existing, maintained subtractive-composition candidates were identified from official sources** (OPEN-SOURCE-LANDSCAPE.md §4): ASE `SimpleQMMM` (subtractive, ONIOM-like, any two ASE calculators; QM subset made nonperiodic; no link-atom handling in the class) [S-ase-qmmm-docs], [S-ase-qmmm-installed]; CP2K `MIXED` with `MIXING_TYPE GENMIX`, a user-defined `MIXING_FUNCTION` of sub-force_eval energies and fragment `MAPPING` [S-cp2k-mixed], [S-cp2k-mixed-generic], [S-cp2k-mixed-mapping]; Py-ChemShell 25.0 `NLayerSubtractive` (mechanical embedding, analytic or finite-difference gradients, link-atom options; CP2K among its QM interfaces; no xTB interface listed) [S-pychemshell-subtractive], [S-pychemshell-qm]. **None of them is shown to compose a GFN0-xTB level with a ωB97X-D3 level for this system, and none proves Cowie parity, boundary placement or link-atom suitability.** | A demonstrated composition through one of the three candidate routes (or another evidenced route) on the declared partition, followed by the composite coupled energy/gradient validation in 8.5 (boundary/link chain-rule terms and constraint projection). Until then the coupling route is an explicit open gap; it is a reuse-first question, not a build-first one. |
| **P4 Driven constrained motion vs zero-force NEB** | The Cowie profile follows an externally driven coordinate with distinct approach and retraction branches; hysteresis is expected (bond formation on approach, cleavage on retraction). NEB (ASE `ase.mep.neb.NEB`; CI-NEB per ref 54) finds a zero-force minimum-energy path between fixed endpoints, with no drive, no branches and no history. A constrained NEB is supporting analysis, never a substitute. | A driven-scan protocol with explicit fixed atom sets, step definition, per-step relaxation criteria and branch bookkeeping, approved by the Reviewer; NEB only as optional supporting analysis at fixed z. |

---

## 5. Reproduction readiness and scope options

**Faithful-reproduction readiness: BLOCKED.** A faithful reproduction requires the Cowie model geometry,
partition, embedding, numerical setup and drive protocol. None is available to this study (Section 1), and no
parity evidence exists for any candidate implementation (Section 4). Readiness is evidence-based: it changes only
when those inputs are obtained through an authorized channel **and** equivalence evidence exists (8.3-A). A human
decision cannot change it; a human can only authorize a different scope (option B), which has its own, separate
prerequisites (8.3-B).

Two scope options exist for MS-001. **Neither is selected here; selection is a human-reviewed scope decision.**

| Option | Definition | Current status |
|---|---|---|
| A. Faithful reproduction | Re-run the Cowie setup with open-source implementations shown equivalent on each of P1–P4 | BLOCKED on missing inputs and missing parity evidence (prerequisites in 8.3-A) |
| B. Declared-deviation prospective study | Test whether the qualitative event sequence of Fig. 3 (Section 8.4) appears under a fully documented, independently chosen setup, with every deviation from Cowie recorded (code, partition/embedding/links, DFT numerics, drive protocol, model geometry) | A **possible** scope option for human review; **not selected**; if explicitly authorized it would still require 8.2, 8.3-B and Reviewer approval |

Whichever option a human selects, any result is a **methodological deviation from a possibly-commercial original
pipeline** (Section 1.2) unless equivalence is demonstrated.

---

## 6. Source-review findings

| Item examined | Outcome |
|---|---|
| 11-page PDF, main text and references only, no SI | **Validated** ([S3] page-tree count 11; no SI content) |
| SI provided on request | **Validated** ([S1] Comments field); not obtained for MS-000 |
| Fig. 3 label; H:Si(100)-2×1; IR DB pair; Ge-adamantane with OH legs; de-iodinated radical; 4 K; 0 V; 50 pm | **Validated** (Section 2 locators) |
| Refs 29/36/37 identities | **Validated** (Section 1.3) |
| Barrera ref 29 model details: B3LYP/6-311G(d,p), D3(BJ), TeraChem 1.96H, wavefunction convergence 1e-8 a.u., two-electron threshold 1e-12; constrained H mesh over a reduced tool model and a Si proxy; Methods p.11 and SI Fig. S1 p.19 | **Validated by reading** [S5] (Section 1.4); kept separate from Cowie settings |
| Ref 36 review, ref 37 ONIOM: general methodology | **Validated at metadata/abstract depth** ([S6], [S7]); full texts not obtained (HTTP 403) |
| tblite has no GFN0 | **Validated** ([S-tblite-methods]) |
| xtb-python GFN0 needs the parameter file via `XTBPATH`; ASE adapter defaults to GFN2 | **Validated** ([S-xtbpy-api], [S-xtbpy-ase]) |
| CP2K 2026.2 native GFN0 via `GFN_TYPE 0`, default 1 | **Validated** ([S-cp2k-xtb]) |
| AiiDA 2.9.2 built-in ZeroMQ broker; RabbitMQ not mandatory | **Validated** ([S-aiida-install], [S-aiida-quick]) |
| ASE docs Python ≥ 3.11 | **Validated with a discrepancy**: docs state 3.11 or newer [S-ase-install]; PyPI 3.29.0 metadata states `>=3.10` [S-pypi-ase] |
| xtb-python 22.1 dated 2022, Linux-only PyPI wheels | **Validated** ([S-pypi-xtb]); conda-forge lists osx-arm64 builds of 22.1 [S-conda-xtb-python]; upstream README marks the project no longer actively developed [S-xtbpy-readme] |
| OVITO Basic binary MIT, source GPL | **Validated with refinement** against the vendor's License information page (OVITO User Manual 3.16.1): Basic binaries MIT; source GPL v3 and MIT; Pro proprietary EULA; vendor Python packages MIT; conda-forge metadata differs and is kept separate. See OPEN-SOURCE-LANDSCAPE.md §OVITO |
| Pynta identity and Fireworks dependency | **Validated** ([S-pynta-readme]) |

---

## 7. Smoke tests performed

Two attempts of one bounded ASE import/IO smoke test were made; both are preserved in
[SMOKE-AND-ENVIRONMENT-RECORD.md](SMOKE-AND-ENVIRONMENT-RECORD.md), which also carries the exact tested program,
the resolved dependency list, and the digests of the private scripts, logs, replay record, and output. The public
record omits the path-specific runner and raw log renderings.

- **Attempt 1 (FAILED before any install or test).** The script relied on a `timeout` utility that does not
  exist on this macOS host. Captured exit codes: `install_exit=127`, `smoke_exit=127` (command not found). No
  package was installed and nothing was tested. The end-of-script marker in that log is not a result.
- **Attempt 2 (completed).** Perl `alarm` cap verified first (`cap_test_exit=142`); throwaway venv under
  an isolated workspace with local cache and temporary paths; `ase==3.29.0` installed (`install_exit=0`); import
  and extxyz round-trip of a placeholder 8-atom structure with tags, a `FixAtoms` constraint and an `info` key:
  nine checks `PASS`, `RESULT: ALL_PASS`, `smoke_exit=0`, 35 s wall time for install plus test.

- **Independent replay** of the unchanged program after attempt 2: exit 0, nine checks `PASS`, and an identical
  round-trip file digest. The public smoke record gives the evidence digest and the limits of this check. No
  further rerun is needed unless the test program or environment changes.

**Label: toy import/IO smoke test. It is not benchmark reproduction and it is not chemistry evidence.** No xtb,
CP2K, tblite, Psi4 or AiiDA was installed or executed; `which xtb cp2k cp2k.psmp cp2k.ssmp` found nothing.

---

## 8. MS-000 scientific gate and MS-001 prospective protocol

Three things are kept separate: **document acceptance** (an independent reviewer approves these documents as a research
deliverable), the **scientific gate** (MS-000 criteria met with evidence), and **human authorization** (a person
authorizes MS-001 and its scope option). None implies another.

### 8.1 MS-000 gate criteria and current status

| Criterion (operator handoff) | Status | Evidence / blocker |
|---|---|---|
| Credible stack identified | **MET, CONDITIONAL** | OPEN-SOURCE-LANDSCAPE.md §3 |
| All major Cowie requirements mapped to implementations or explicit gaps | **MET** | Sections 3 and 4 |
| Justified minimum dependency set | **MET** | OPEN-SOURCE-LANDSCAPE.md, adopt/defer/reject per tool |
| Prospective MS-001 acceptance criteria | **MET qualitatively; numerical tolerances PENDING the 8.6 procedure** | Sections 8.4–8.6 |
| No LLM physics | **MET** | Every physical statement is `[EXP]`/`[COMP-PRED]` with a Cowie locator, `[LIT]` with a source, or a `[GAP]`; none originates from an LLM |
| Independent scientific review approves the plan | **PENDING in this public record** | This adaptation publishes no private review receipt and claims no approval |
| **Overall MS-000 scientific gate** | **PENDING** | Reasons, in order: (1) the trajectory setup (geometry, partition, embedding, numerics, drive) is unavailable; (2) no parity evidence exists for P1–P4, and no two-level coupling route has been demonstrated for this system through any of the identified reuse candidates (P3b); (3) independent scientific approval is not established in this public record; (4) tolerance selection under 8.6 awaits review. **Not marked passed.** |

### 8.2 Sequencing: preliminary method-validation calculations precede scientific trajectory calculations

P1 and P2 checks are themselves calculations. They are **Stage 1** work, permitted only under a human-authorized
MS-001 scope option, and they precede **Stage 2** (the scientific trajectory).

| Stage | Content | Precondition |
|---|---|---|
| 0 | No calculations. Under option A: the source-provided model, partition, embedding, links, charge/spin, numerics and drive frozen and hashed. Under option B: model definitions (M1, M2), declared scheme (P3), drive protocol (P4). Under either: a coupling route selected from the reuse candidates (P3b), tolerance-selection record (8.6), provenance wiring test on a trivial AiiDA job | 8.3 "before Stage 0" group only: human authorization of a scope option (C1) and, for option A, the source inputs (A1) |
| 1 | Preliminary method-validation calculations: P1 GFN0 identity run with full provenance; P2 cross-engine molecular check; **composite coupled energy/gradient validation** (8.5); constraint-projection check | 8.3 "before Stage 1" group: Stage 0 definitions frozen (C2–C4 and A3, or B1–B3); Reviewer approval of the definitions |
| 2 | Scientific trajectory calculations (M4–M6), then optional supporting analyses (M7) | 8.3 "before Stage 2" group: Stage 1 results reviewed (C5, C6, and A2/A4 or B4); no parameter changed after Stage 1 without a recorded reason unrelated to agreement with the paper |

### 8.3 MS-001 prerequisites, per stage and per scope option

Prerequisites are grouped by the **earliest stage that can satisfy them**, so that no stage depends on a later
stage. Every check below is required; the grouping only fixes where each one sits.

**Before Stage 0 may begin (authorization and inputs only):**

- C1. Human authorization of a scope option (Section 5), recorded by DI separately from document acceptance.
- Option A only, evidence-based, none currently met:
  - A1. Source inputs obtained through an authorized channel: the Cowie model geometry with atom identities,
    partition, embedding and link treatment, charge and spin, basis/ECP and dispersion parameters, drive
    protocol and per-step criteria, and software identities (Section 1, Section 2.9).
- Option B only, applies only if option B is explicitly authorized: no additional input prerequisite beyond C1;
  the model and scheme are *defined* during Stage 0 (B1–B3 below).

**Before Stage 1 may begin (definitions frozen during Stage 0, no calculations yet):**

- C2. A coupling route **selected** from the reuse candidates (P3b) and fully specified; its validation is a
  Stage 1 activity (see C6).
- C3. Provenance capture (EVIDENCE-POLICY.md §4) tested on a trivial AiiDA job.
- C4. Tolerances selected and approved under 8.6 and recorded.
- Option A only:
  - A3. Model inputs frozen and hashed as **source-provided**, not `[AGENT]`.
- Option B only:
  - B1. Model geometries (M1, M2) frozen, hashed, labeled `[AGENT]`.
  - B2. P3 declared as a fully specified scheme (partition, embedding, links, charge, spin), labeled `[AGENT]`
    deviation, Reviewer-approved.
  - B3. P4 drive protocol Reviewer-approved.

**Before Stage 2 may begin (results of Stage 1 method-validation calculations):**

- C5. Stage 1 complete with P1 identity provenance captured and P2 internal consistency established.
- C6. The selected coupling route's composite coupled energy/gradient validated (8.5), including boundary/link
  chain-rule terms and constraint projection.
- Option A only:
  - A2. Equivalence evidence for each of P1–P4 against the stated Cowie setup (Section 4), recorded per item.
  - A4. Parity status recorded per item as **established** or **not established**; any item not established
    makes the run a deviation, to be reported as such.
- Option B only:
  - B4. Parity to Cowie recorded as **unknown** for every item, in every result (carried into Stage 2 reporting).

Dependency check: Stage 0 needs only C1 and (option A) A1; Stage 1 needs Stage 0 outputs (C2–C4, A3 or B1–B3);
Stage 2 needs Stage 1 outputs (C5, C6, A2/A4 or B4). No group references a later stage.

### 8.4 Qualitative event-order and connectivity observations a reproduction must show

Targets derived from Fig. 3 A–D and §3 (`[COMP-PRED]` targets: a reproduction reproduces the **model's** sequence,
not an experimental observation). Each is reported as observed / not observed / indeterminate with its criterion
recorded in advance.

- E1. Approach branch: a Si–C bond forms between the tool's distal C and one Si of the IR-DB pair, with a
  concurrent decrease in total energy at that step (sign only).
- E2. Retraction branch: the Ge–C bond breaks while the Si–C bond persists; Si–Si bonds at the anchoring Si stay
  intact (the paper reports Si abstraction as almost never observed).
- E3. After Ge–C cleavage, a pendent C2 bound to one Si exists over a finite z range near the EAOGe• fragment.
  **Three distinct claims, each with its own evidence and its own prospective criterion (8.6):**
  (i) *geometric proximity/connectivity*: a declared distance criterion supports only the claim that the
  fragments remain close; (ii) *radical character*: a declared spin-density or spin-population localization
  criterion from the engine's own output supports only the claim that unpaired-electron density resides on the
  pendent C2 and/or the EAOGe• Ge site; (iii) *interaction/stabilization*: a declared interaction-energy
  criterion (energy of the pendent-plus-tool configuration relative to the same fragments at a declared
  non-interacting separation, computed within the same scheme, or an equivalent decomposition the scheme
  supports) is required before any claim that the contact stabilizes the pendent. Proximity never supports (ii)
  or (iii); radical localization never supports (iii). Each claim is reported **indeterminate** whenever its
  required evidence is unavailable in the chosen scheme.
- E4. At larger z, the pendent C2 bridges the IR-DB pair across the trough: both Si of the pair bonded to the C2;
  no bond to a neighbouring dimer's Si; no H abstracted from the surface.
- E5. Net energy change from A to D is negative (sign only).
- E6. Atom identity preserved: the two C atoms in the final IR-C2 are the tool's C2 (tagged indices).

### 8.5 Convergence, energy-force validation and provenance coverage plan

- Per-step reporting: SCF convergence status, maximum residual force at each accepted step, and a step-size
  sensitivity check (one coarser and one finer z step on a short segment) showing whether the event order
  E1–E4 changes. Report; never tune.
- **Constituent-level consistency:** finite-difference force checks against energies for each level on one
  configuration per branch.
- **Composite coupled energy/gradient validation (required, Stage 1):** finite-difference validation of the
  *coupled* total energy and gradient of the declared scheme, including (a) boundary/link-atom chain-rule
  contributions (displace a boundary atom and a link-atom host and compare the analytic coupled gradient with the
  finite difference), and (b) constraint projection (verify that the projected gradient used by the driven scan is
  the analytic gradient with the fixed-atom and rigid-displacement constraints applied, and that constrained atoms
  do not move). Validating each level separately is insufficient.
- P1 identity provenance and P2 cross-engine check as Stage 1 items.
- Provenance coverage: every accepted step and check is an AiiDA node carrying the fields in EVIDENCE-POLICY.md §4;
  a coverage report lists any step lacking a field; missing fields block the `[COMP-REPRO]`/`[COMP-PRED]` label.

### 8.6 Prospective tolerance selection and approval procedure (before any run)

No numerical tolerance is derived from Cowie, because none is available. The procedure fixes **how** each
tolerance is chosen, **by whom**, and **how pass/fail is decided**, all before Stage 1:

| Quantity needing a tolerance | Selection basis (proposal) | Proposed by | Checked by | Approved by | Pass/fail rule |
|---|---|---|---|---|---|
| Force convergence per accepted step | The engine's documented default for the optimizer used, tightened only if the step-size sensitivity check shows event-order dependence; the source of the value is cited in the record | Method author | Independent reviewer | Human | A step is accepted only if the reported maximum residual force is at or below the recorded value |
| SCF energy convergence | The engine's documented default for the method, cited | Method author | Independent reviewer | Human | Step rejected if SCF did not converge to the recorded value |
| Bond/no-bond cutoff per element pair (E1, E2, E4, E6) | A stated multiple of the sum of covalent radii from a cited tabulation, with the multiple recorded; sensitivity reported by re-evaluating E1–E4 at one smaller and one larger multiple | Method author | Independent reviewer | Human | Observation counts as observed only if it holds at all three multiples; otherwise indeterminate |
| E3(i) proximity criterion | A distance cutoff chosen by the same covalent-radius rule | Method author | Independent reviewer | Human | Proximity claim only |
| E3(ii) radical-character criterion | A spin-population localization threshold from the engine's population analysis, with the analysis scheme named and the sites (pendent C2; EAOGe• Ge) declared; if the scheme cannot produce spin populations, E3(ii) is reported indeterminate | Method author | Independent reviewer | Human | Radical-character claim only, and only if the threshold is met on every accepted step in the range; it never supports E3(iii) |
| E3(iii) interaction/stabilization criterion | A declared interaction-energy threshold: energy of the pendent-plus-tool configuration minus the energy of the same fragments at a declared non-interacting separation, both within the same scheme at the same z, with the reference separation recorded; if the scheme cannot produce a consistent fragment reference (e.g., the partition forbids it), E3(iii) is reported indeterminate | Method author | Independent reviewer | Human | Stabilization claim only if the threshold is met on every accepted step in the range and E3(i) also holds; independent of E3(ii) |
| P2 cross-engine agreement | A tolerance on total-energy differences and on per-atom force differences for one molecule, justified from the documented numerical precision of both engines | Method author | Independent reviewer | Human | Internal consistency established only if both tolerances are met |
| Composite coupled gradient (8.5) | A finite-difference agreement tolerance justified from the displacement size and engine precision | Method author | Independent reviewer | Human | Scheme accepted for Stage 2 only if met at every tested atom |
| Step-size sensitivity | No numeric tolerance; the rule is that the E1–E4 event order is unchanged between the three step sizes | Method author | Independent reviewer | Human | Unchanged: pass; changed: the run is reported as sensitive and Stage 2 does not proceed without human review |

All selected values, their cited basis and the approval record are frozen before Stage 1. Changing any value after
Stage 1 requires a recorded reason unrelated to agreement with the paper and a fresh approval.

### 8.7 Reviewer approval requirement

MS-001 results are not evidence of anything until an independent Reviewer has (a) checked provenance completeness,
(b) checked that no parameter changed after Stage 1 without a recorded, agreement-independent reason, (c) assessed
the technical claims (coupled-gradient validation, E3 electronic evidence, GFN0 identity provenance) independently,
and (d) issued a canonical decision recorded by DI. No forced pass.

### 8.8 Failed-reproduction protocol

A failed reproduction (any of E1–E6 not observed) is a **valid scientific result** and is reported as such.
**Parameters are never tuned merely to obtain agreement with the paper.**

The list below is a **proposed diagnostic priority order** (`[AGENT]`), not a probability ranking; no likelihood is
inferred from missing information. The order is revisited with the Reviewer after the first failure.

1. **P3 deviation** (partition/embedding/links/charge/spin). Discriminating test: re-run the failing segment with
   the alternative spin multiplicity, or with the region boundary moved by one shell, all else fixed; report
   whether the event order changes.
2. **P4 protocol** (drive definition, step, per-step relaxation). Test: the step-size sensitivity segment, and a
   check that the fixed set excludes atoms the mechanism requires to move.
3. **Model geometry** (M1/M2). Test: change one geometry choice (e.g., leg configuration, which the paper itself
   marks as non-unique) and re-run the segment.
4. **P2 numerical setup** (HFX/dispersion/basis/ECP). Test: the cross-engine check and a basis/ECP variation on the
   Ge–C vs Si–C molecular proxy (Section 2.6) to see whether the ordering is sensitive.
5. **P1 method selection** (wrong GFN variant). Test: re-verify the identity provenance (selector, banner,
   version, parameter digest).
6. **Engine defect or platform numerics** (e.g., BLAS-dependent deviations noted in the xtb README on macOS).
   Test: a second platform or build.
7. **The model's mechanism is not reproduced under any reasonable deviation**: a substantive result reported to
   the human, not resolved by the project team.

The next discriminating test is always the single cheapest test that separates the top two entries in the current
order, recorded before it is run.

---

## 9. Scope boundary

MS-000 performed source analysis, package evaluation, and a bounded ASE import and file-round-trip test. It did
not run quantum chemistry, propose novel chemistry, implement a reaction compiler or primitive library, or model
manufacturing. The Cowie Supplementary Information and source coordinate set were not obtained. The private
working records used to prepare this public adaptation are identified by SHA256 in the export manifest; local
paths, internal identifiers, and orchestration records are excluded.
