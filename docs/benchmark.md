# The published benchmark

This page records what the benchmark preprint reports, with locators, and how this project relates to it. It
cites and paraphrases; it does not reproduce paper text or figures. All links and their verification basis are in
[SOURCES.md](SOURCES.md).

## Attribution

| Field | Value |
|---|---|
| Authors | Cowie, M. *et al.* |
| Title | "Atomically precise mechanosynthesis of carbon structures on hydrogenated Si(100) by inverted-mode STM" |
| Identifier | arXiv:2605.27250v1 [cond-mat.mtrl-sci], submitted 26 May 2026 |
| DOI | [10.48550/arXiv.2605.27250](https://doi.org/10.48550/arXiv.2605.27250) (arXiv-issued) |
| Status | Preprint. No peer-review status is claimed here. |
| Supplementary Information | "available upon request" per the arXiv listing. **Not obtained by this project.** |

Locators below refer to section headings of the v1 PDF.

## What the authors report

### Setup (section "Mechanosynthetic C2 donation") — `[LIT]` over `[EXP]`

- **Instrument:** inverted-mode STM operated at 4 K. Sparsely deposited tall molecules on the sample act as probes
  that image the apex of a large, flat silicon probe chip (SPC). The molecules can also transfer fragments to and
  from that apex, which serves as the build site.
- **Molecular tool:** EAOGe-C2I, a Ge-substituted adamantane with a C2 functional group, three OH-terminated legs
  and an iodine capping group. The legs anchor the molecules to the Si sample, and a subset stands upright.
- **Build site:** an H-passivated Si(100) probe chip with a flat, crystalline apex, pre-patterned with reactive
  dangling-bond sites (abstract; Fig. 5 discussion).

### Reported per-interaction target formation (section "Positional and chemical control of mechanosynthetic donation") — `[LIT]` over `[EXP]`

| Target | Count | Reported | Reported 95% CI |
|---|---|---|---|
| IR-C2 | 184 / 197 | 93% | 89–96% |
| 2IR-C2 | 71 / 73 | 97% | 91–99% |
| IR-C2/C4 | 45 / 49 | 92% | 81–97% |
| 2IR-C4 | 27 / 32 | 84% | 68–93% |

The authors contrast these targeted outcomes with the broad distribution of C2 donation products they observe
on un-passivated, un-patterned Si(100). They attribute the control as much to build-site preparation
(dangling-bond patterning of H:Si) as to tool choice.

How this project treats these numbers:
- They are **reported experimental counts**, not results of this project.
- They are separate interaction outcomes, not independent full-build events.
- They are **never multiplied** into a build-success probability or a throughput estimate.

### Proposed mechanism (section "C2 donation mechanism", Fig. 3) — `[LIT]` over `[COMP-PRED]`

The authors present a proposed IR-C2 formation mechanism from a QM/MM model, xTB (GFN0) with DFT (ωB97X-D3):
1. A de-iodinated tool (EAOGe-C2•) is positioned with its distal carbon centred under an inter-row dangling-bond
   (IR-DB) pair.
2. As the tool approaches, the first C–Si bond forms at a critical separation.
3. On retraction, the Ge–C bond cleaves and the C2 unit transfers, leaving a pendent intermediate.
4. The intermediate then relaxes into the IR-C2 configuration.

Further points the authors make:
- **Net downhill landscape:** they describe the transfer as proceeding along a net downhill energy landscape, with
  barriers overcome by mechanical work.
- **Representative, not unique:** the arrangement shown is one representative leg-binding configuration among
  several.
- **Alternative pathway:** at larger approach depths, they describe an alternative pathway that forms the second
  Si–C bond before Ge–C cleavage.
- **Supporting calculations:** these are said to be in the Supplementary Materials, which this project has not
  obtained.

This is a **computational proposal**, distinct from the experimental counts. This project has not reproduced the
model, its QM/MM partition or its energy profile, and has no access to its inputs.

## Related preprints consulted (attribution facts from their arXiv listings)

| Work | Relevance here |
|---|---|
| Barrera, E. *et al.*, "Inverted-Mode Scanning Tunneling Microscopy for Atomically Precise Fabrication", arXiv:2512.24431v1 (submitted 30 Dec 2025), [doi:10.48550/arXiv.2512.24431](https://doi.org/10.48550/arXiv.2512.24431) | Introduces inverted-mode STM. Its abstract describes molecules on Si(100) that image and react with the probe apex, positioned with sub-ångström precision. The project's donor-candidate structures carry a locator to this work's supplementary information, as recorded in the original reconstruction notes; that material was not re-read in the current review (see [donor-candidates.md](donor-candidates.md)). |
| Blue, B. *et al.*, "Towards Atom-by-Atom Fabrication: Mechanosynthetic donation and abstraction", arXiv:2606.13876v1 (submitted 11 Jun 2026), [doi:10.48550/arXiv.2606.13876](https://doi.org/10.48550/arXiv.2606.13876) | Its abstract reports donation of carbon and abstraction of silicon on atomically clean Si(100) using IM-STM and functionalized molecular tools. According to the original reconstruction notes, it was used for connectivity and attachment-scheme cross-checks; this was not re-verified in the current review. |

## How this project relates to the benchmark

- **It is the scientific reference point**, not something this project claims to reproduce.
- **The donor-only first experiment** ([e01-method-specification.md](e01-method-specification.md)) checks
  whether an engine setup runs on reconstructed free-donor candidates. It cannot reproduce the benchmark's
  surface chemistry, pathway or counts.
- **Reproduction would need the benchmark authors' inputs:** coordinates, QM/MM partition, drive protocol and
  supplementary material. This project has not obtained any of them.
