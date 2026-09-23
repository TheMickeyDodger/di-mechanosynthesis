# The benchmark study

This document summarizes what the benchmark preprint reports and how the present work relates to it. The paper is
cited and paraphrased; none of its text or figures is reproduced. Numbered citations refer to the catalogue in
[SOURCES.md](SOURCES.md), where each link is listed with its verification basis. Section headings of the v1 PDF
serve as locators.

## Attribution

The benchmark is Cowie, M. *et al.*, "Atomically precise mechanosynthesis of carbon structures on hydrogenated
Si(100) by inverted-mode STM", arXiv:2605.27250v1 [cond-mat.mtrl-sci], submitted 26 May 2026, with the
arXiv-issued DOI [10.48550/arXiv.2605.27250](https://doi.org/10.48550/arXiv.2605.27250) [1]. It is a preprint, and
no peer-review status is claimed for it here. The arXiv listing states that Supplementary Information is
"available upon request"; this project has not obtained it.

## Experimental setup

The statements in this section are literature-derived descriptions of experimental work (`[LIT]` over `[EXP]`).

The section "Mechanosynthetic C2 donation" describes the setup. Mechanosynthesis is performed by inverted-mode
scanning tunnelling microscopy at 4 K. Sparsely deposited tall molecules on the sample act as probes that image the
apex of a large, flat silicon probe chip. The same molecules can transfer fragments to and from that apex, which
serves as the build site.

The molecular tool, EAOGe-C2I, consists of a germanium-substituted adamantane with a C2 functional group, three
OH-terminated legs and an iodine capping group. The legs anchor the molecules to the silicon sample, and a subset
of the molecules stands upright. The build site is a hydrogen-passivated Si(100) probe chip with a flat,
crystalline apex, pre-patterned with reactive dangling-bond sites, as stated in the abstract and the discussion of
Fig. 5.

## Reported target formation

The section "Positional and chemical control of mechanosynthetic donation" reports per-interaction target
formation for four build targets (`[LIT]` over `[EXP]`).

| Target | Count | Reported | Reported 95% CI |
|---|---|---|---|
| IR-C2 | 184 / 197 | 93% | 89–96% |
| 2IR-C2 | 71 / 73 | 97% | 91–99% |
| IR-C2/C4 | 45 / 49 | 92% | 81–97% |
| 2IR-C4 | 27 / 32 | 84% | 68–93% |

The authors contrast these targeted outcomes with the broad distribution of C2 donation products that they observe
on un-passivated, un-patterned Si(100). They attribute the control as much to the preparation of the build site,
namely dangling-bond patterning of H:Si, as to the choice of tool.

The numbers are experimental counts reported by the authors, not results of this project. Each is a separate count
of interaction outcomes rather than a record of independent full-build events, and none is multiplied here into a
build-success probability or a throughput estimate.

## Proposed mechanism

In the section "C2 donation mechanism" and its Fig. 3, the authors present a proposed mechanism for IR-C2
formation derived from a QM/MM model that combines xTB (GFN0) with DFT (ωB97X-D3). This is literature-derived
provenance over a computational prediction (`[LIT]` over `[COMP-PRED]`). The mechanism proceeds as follows:

1. A de-iodinated tool, EAOGe-C2•, is positioned with its distal carbon centred under an inter-row dangling-bond
   (IR-DB) pair.
2. As the tool approaches, the first C–Si bond forms at a critical separation.
3. On retraction, the Ge–C bond cleaves and the C2 unit is transferred, leaving a pendent intermediate.
4. The intermediate relaxes into the IR-C2 configuration.

The authors describe the transfer as proceeding along a net downhill energy landscape, with barriers overcome by
mechanical work. They present the arrangement shown as one representative leg-binding configuration among several.
They also describe an alternative pathway at larger approach depths, in which the second Si–C bond forms before the
Ge–C bond cleaves. Supporting calculations are said to appear in the Supplementary Materials, which this project
has not obtained.

The mechanism is a computational proposal and is distinct from the experimental counts. The present work has not
reproduced the model, its QM/MM partition or its energy profile, and it has no access to the model's inputs.

## Related preprints

Two related preprints are cited from their arXiv listings.

Barrera, E. *et al.*, "Inverted-Mode Scanning Tunneling Microscopy for Atomically Precise Fabrication",
arXiv:2512.24431v1, was submitted on 30 December 2025
([doi:10.48550/arXiv.2512.24431](https://doi.org/10.48550/arXiv.2512.24431)) [2]. It introduces inverted-mode STM,
and its abstract describes molecules on Si(100) that image the probe apex and react with it at sub-ångström
positioning precision. The donor-candidate structures in this repository carry a locator to its supplementary
information. That locator was recorded in the original reconstruction notes, and the material was not re-read in
the current review ([donor-candidates.md](donor-candidates.md)).

Blue, B. *et al.*, "Towards Atom-by-Atom Fabrication: Mechanosynthetic donation and abstraction",
arXiv:2606.13876v1, was submitted on 11 June 2026
([doi:10.48550/arXiv.2606.13876](https://doi.org/10.48550/arXiv.2606.13876)) [3]. Its abstract reports donation of
carbon and abstraction of silicon on atomically clean Si(100) using IM-STM and functionalized molecular tools.
According to the original reconstruction notes, it was used for cross-checks of connectivity and of the attachment
scheme, and that use has not been re-verified in the current review.

## Relation to the present work

The benchmark is the scientific reference point of the project, not a result that the project claims to
reproduce. The first planned calculation ([e01-method-specification.md](e01-method-specification.md)) asks only
whether an engine setup runs correctly on reconstructed free-donor candidates. It cannot reproduce the surface
chemistry, pathway or counts of the benchmark. A reproduction would require the benchmark authors' coordinates,
QM/MM partition, drive protocol and supplementary material, and this project has obtained none of them.
