# MS-001 Stage 0 source ledger

Every source used by the Stage 0 records of this package is listed below. The retrieval table covers each item
retrieved over the network on 2026-09-26: its URL, version, locator and use, access time, HTTP result, retrieved
byte count and the SHA256 of the retrieved bytes. Two retrievals failed and are listed as not obtained.
Eleven retrievals were added for the corrections after the independent review. They are the Psi4, qcengine and
simple-dftd3 files behind the dispersion-input contract and the Psi4 convergence defaults, and the CP2K SCF-algorithm
pages. The two qcengine files are byte-identical to the files installed with the project's Psi4 build. The
retrieved bytes are kept privately; they are third-party documentation and source, cited here and not copied.
The retrievals and archive reads of the source resolution of 2026-09-27 are listed in their own dated section,
[Source-resolution retrievals, 2026-09-27](#source-resolution-retrievals-2026-09-27), at the end of this ledger.

Version matching:
- **AiiDA pages.** Retrieved from URLs pinned to v2.9.2. Each page names itself "AiiDA 2.9.2 documentation".
- **CP2K manual pages.** Retrieved from the 2026.2-branch manual. CP2K data and source files came from the
  `support/v2026.2` branch.
- **Psi4, simple-dftd3 and libxc files.** Retrieved at the named tags.
- **docs.ase-lib.org pages.** These describe an addition made in ASE 3.30.0, so they are not matched to the
  installed ASE 3.29.0. ASE facts are therefore cited from the installed 3.29.0 source files in the second table.
- **libxc version.** The libxc 7.0.0 files were read for the ωB97X-D3 parameter definition. Which libxc version a
  CP2K 2026.2 build links is build-dependent and is recorded per run; the libxc version identity between engines
  is `[GAP]`.
- **CP2K release identity (added 2026-09-27).** The `support/v2026.2` branch cited above is a mutable ref. The
  release is tag `v2026.2`, which resolves to the release revision
  `67b5da876dd6a76b8b021d5a04d1c81ba79a4c50`. The release archive's own `REVISION` file names that commit's parent,
  `c92cc08`.
  - The six branch-retrieved CP2K files above were re-verified on 2026-09-27 against their SHA256 and are
    byte-identical to the release-revision blobs. Every entry of `S0-cp2k-data-listing` names the same Git object as
    the release revision.
  - This establishes that those retrieved bytes equal the release-revision bytes. It says nothing about the branch
    at any other time, and it does not cover the 2026.2-branch manual pages, which were not compared.
  - The locators in the dated section below are at the release revision.

## Retrieved sources

| ID | URL | Version | Locator and use | Accessed (UTC) | Result | Retrieved bytes | SHA256 of retrieved bytes |
|---|---|---|---|---|---|---:|---|
| `S0-aiida-provenance` | <https://aiida.readthedocs.io/projects/aiida-core/en/v2.9.2/topics/provenance/concepts.html> | AiiDA 2.9.2 (pinned URL) | Topics › Provenance › Concepts; data-model review context | 2026-09-26T18:58:18Z | HTTP 200 | 29572 | `4a3f3c67e71a6100ecfc735029e46f62d4e65054b4732f6a96fabdb58c3d804f` |
| `S0-aiida-data-types` | <https://aiida.readthedocs.io/projects/aiida-core/en/v2.9.2/topics/data_types.html> | AiiDA 2.9.2 | Topics › Data types: core types table; StructureData (Å default unit); BandsData note on stored nodes | 2026-09-26T18:58:18Z | HTTP 200 | 217451 | `fb6c33afd280f25236448481033d82a3e1d3b11f4b6bb702f5cfcb36d46c60b1` |
| `S0-aiida-calc-concepts` | <https://aiida.readthedocs.io/projects/aiida-core/en/v2.9.2/topics/calculations/concepts.html> | AiiDA 2.9.2 | Topics › Calculations › Concepts; review context | 2026-09-26T18:58:18Z | HTTP 200 | 57290 | `6a00942a71b0ce2eba69de793d02f4fbc598d76ba3b7837d041318231bcaadfc` |
| `S0-aiida-calc-usage` | <https://aiida.readthedocs.io/projects/aiida-core/en/v2.9.2/topics/calculations/usage.html> | AiiDA 2.9.2 | Topics › Calculations › Usage: options list (additional_retrieve_list, environment_variables, prepend_text); retrieve lists; parser exit codes | 2026-09-26T18:58:18Z | HTTP 200 | 198008 | `d957ca4048bea8acd39b7393e747f35b6b6c6468dd4d0493a1480f3bfbeae9f7` |
| `S0-aiida-processes-usage` | <https://aiida.readthedocs.io/projects/aiida-core/en/v2.9.2/topics/processes/usage.html> | AiiDA 2.9.2 | Topics › Processes › Usage: exit_status and exit codes | 2026-09-26T18:58:19Z | HTTP 200 | 133272 | `bdf479068c2a9170c1f4e0bd22e92ca0ef285298d7cdb42c5e47bc39e90ef6f9` |
| `S0-aiida-repository` | <https://aiida.readthedocs.io/projects/aiida-core/en/v2.9.2/topics/repository.html> | AiiDA 2.9.2 | Topics › Repository: writing, listing and reading node files | 2026-09-26T18:58:19Z | HTTP 200 | 44763 | `965d8136e7fbb19d42f05428a97537068167ab4cfda35c5ff355e0867dac8a29` |
| `S0-aiida-caching` | <https://aiida.readthedocs.io/projects/aiida-core/en/v2.9.2/topics/provenance/caching.html> | AiiDA 2.9.2 | Topics › Provenance › Caching and hashing: "How are nodes hashed" | 2026-09-26T18:58:19Z | HTTP 200 | 47359 | `d04c56f01e56627789d4b9de795e32d284613b036349c2ec0dbf81e305d7d800` |
| `S0-aiida-quick` | <https://aiida.readthedocs.io/projects/aiida-core/en/v2.9.2/installation/guide_quick.html> | AiiDA 2.9.2 | Installation › Quick installation guide (verdi presto) | 2026-09-26T18:58:19Z | HTTP 200 | 31317 | `3a8da846a80a64fc56548d8f81499c435ca623d9eb36b1a9994d8a6195d1b644` |
| `S0-aiida-run-codes` | <https://aiida.readthedocs.io/projects/aiida-core/en/v2.9.2/howto/run_codes.html> | AiiDA 2.9.2 | How-to › Run external codes (InstalledCode); review context | 2026-09-26T18:58:20Z | HTTP 200 | 121543 | `a6b616a90f802038f897ed32af24923372c45c983e8f631af6a24ca19e45714a` |
| `S0-ase-docs-atoms` | <https://docs.ase-lib.org/ase/atoms.html> | docs.ase-lib.org as served; describes an ASE 3.30.0 addition, so not matched to 3.29.0 | The Atoms object; used only to establish the version mismatch | 2026-09-26T18:58:20Z | HTTP 200 | 246985 | `421abf0cc4b98a0d5dafe2dab9949859621dd9645259cd92b7f63f609fe6b0ed` |
| `S0-ase-docs-io` | <https://docs.ase-lib.org/ase/io/io.html> | docs.ase-lib.org as served; version not stated | File input and output; not used as version-matched evidence | 2026-09-26T18:58:20Z | HTTP 200 | 105807 | `0476cfcec0e02054022b63285f73ca03786741062316e391161ee09be9845ab5` |
| `S0-ase-docs-formatoptions` | <https://docs.ase-lib.org/ase/io/formatoptions.html> | docs.ase-lib.org as served; version not stated | Format-specific options (extxyz); not used as version-matched evidence | 2026-09-26T18:58:21Z | HTTP 200 | 477887 | `9f892c8a94ddec4e6ad9e6597a888efa769d325ff1c3e1006848d5330223663b` |
| `S0-ase-docs-constraints` | <https://docs.ase-lib.org/ase/constraints.html> | docs.ase-lib.org as served; version not stated | Constraints; not used as version-matched evidence | 2026-09-26T18:58:21Z | HTTP 200 | 137892 | `26e841e815e0fbeabd272d6507b7e28427c94dc11077544d9867d22da241439d` |
| `S0-ase-docs-surface` | <https://docs.ase-lib.org/ase/build/surface.html> | docs.ase-lib.org as served; version not stated | Surfaces (diamond100); not used as version-matched evidence | 2026-09-26T18:58:21Z | HTTP 200 | 113944 | `9b441b08832d6ddd25f0c7319fe7e7b0a02152d4df84e64733090919cf500dd1` |
| `S0-ase-docs-data` | <https://docs.ase-lib.org/ase/data.html> | docs.ase-lib.org as served; version not stated | The data module; not used as version-matched evidence | 2026-09-26T18:58:22Z | HTTP 200 | 84051 | `29e770e841fcd78a18651079e89d56663bab8c7d450c973f9b32ee2506a6c0e5` |
| `S0-pypi-aiida-cp2k` | <https://pypi.org/pypi/aiida-cp2k/2.1.1/json> | aiida-cp2k 2.1.1 | PyPI release record: sdist and wheel digests | 2026-09-26T18:58:22Z | HTTP 200 | 7007 | `d7fb64b145a2bc09d56dc9dc176182d30181841506813cdfc64f318c08c87bcb` |
| `S0-aiida-cp2k-sdist` | <https://files.pythonhosted.org/packages/38/3b/9932495c254a47382eaa9ab0778ae9e2c950c044100ca90b34236ed19bcd/aiida_cp2k-2.1.1.tar.gz> | aiida-cp2k 2.1.1 | Source archive; digest equals the PyPI-published SHA256; files read: S0-aiida-cp2k-src, S0-aiida-cp2k-parser | 2026-09-26T19:03:16Z | HTTP 200 | 668750 | `a5f9dfd520628d59be4bc4a193597889b88c84daddf563c5b909fba23afb9876` |
| `S0-cp2k-force-eval` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL.html> | CP2K 2026.2 manual | FORCE_EVAL: METHOD values | 2026-09-26T19:48:11Z | HTTP 200 | 68164 | `13342298309800dffc41de24bad9bdf810d1d931cc072eb3ad556069f65bcd58` |
| `S0-cp2k-mixed` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/MIXED.html> | CP2K 2026.2 manual | FORCE_EVAL/MIXED: MIXING_TYPE (GENMIX), NGROUPS | 2026-09-26T19:48:12Z | HTTP 200 | 67114 | `8578b446b5bde473b0e712aed88e4427357a4abe2a3e4349770243702d8aed52` |
| `S0-cp2k-mixed-generic` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/MIXED/GENERIC.html> | CP2K 2026.2 manual | MIXED/GENERIC: MIXING_FUNCTION, VARIABLES, DX 0.1 bohr (Ridders), ERROR_LIMIT 1e-12 | 2026-09-26T19:48:13Z | HTTP 200 | 70723 | `9f8e2a5bf4dc8e9fcfa56bb415f925b665e402cd0b17b0762e03ef744d1e631b` |
| `S0-cp2k-mapping` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/MIXED/MAPPING.html> | CP2K 2026.2 manual | MIXED/MAPPING: fragment-based atom mapping; default 1-1 | 2026-09-26T19:48:13Z | HTTP 200 | 63013 | `88c6900b6f8a81fdcfec19a2b10fa63131cd5cdece0c459a48ecd5016dc69d96` |
| `S0-cp2k-mapping-fe` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/MIXED/MAPPING/FORCE_EVAL.html> | CP2K 2026.2 manual | MAPPING/FORCE_EVAL: DEFINE_FRAGMENTS | 2026-09-26T19:48:14Z | HTTP 200 | 67191 | `46a1616f89e41d96d77a2cd61c01b5c0a50e80a0a28fb596ac25dddc9f8fc646` |
| `S0-cp2k-mapping-fe-frag` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/MIXED/MAPPING/FORCE_EVAL/FRAGMENT.html> | CP2K 2026.2 manual | MAPPING/FORCE_EVAL/FRAGMENT: start and end atom index; MAP | 2026-09-26T19:48:14Z | HTTP 200 | 69319 | `c78ebb72fe6a2acac816083b64218fdfd6f5603485d083415ded2aed523a7872` |
| `S0-cp2k-mapping-fem` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/MIXED/MAPPING/FORCE_EVAL_MIXED.html> | CP2K 2026.2 manual | MAPPING/FORCE_EVAL_MIXED | 2026-09-26T19:48:15Z | HTTP 200 | 64280 | `555d12ec753a4da8a96e749e80862c75c8c3708da11712404a3c3e1eeccc9674` |
| `S0-cp2k-dft` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT.html> | CP2K 2026.2 manual | DFT: CHARGE (0), MULTIPLICITY (default by parity), UKS, ROKS, BASIS_SET_FILE_NAME | 2026-09-26T19:48:16Z | HTTP 200 | 92337 | `3b882b74509d0ba7dd7984bebbe2ceef3d00bc24d42460727842c25c466824fb` |
| `S0-cp2k-qs` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/QS.html> | CP2K 2026.2 manual | DFT/QS: METHOD (GPW default; GAPW; XTB), EPS_DEFAULT 1e-10 | 2026-09-26T19:48:16Z | HTTP 200 | 132540 | `94d335636fd90dd85be5360505eb6cd126f4435236d05a62381a53682b1da346` |
| `S0-cp2k-xtb` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/QS/XTB.html> | CP2K 2026.2 manual | DFT/QS/XTB: GFN_TYPE (0, 1 or TBLITE; default 1; 0 = internal GFN0-xTB), SCC_MIXER, EPS_PAIRPOTENTIAL and other defaults | 2026-09-26T19:48:17Z | HTTP 200 | 88647 | `82aec8ed3905e4367ab47e23b48f2f74714f09855362c59d49bd26e2aa18436a` |
| `S0-cp2k-xc` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/XC/XC_FUNCTIONAL.html> | CP2K 2026.2 manual | XC/XC_FUNCTIONAL: libxc HYB_GGA_XC_WB97X_D3 with _ALPHA 1.0, _BETA -0.804272, _OMEGA 0.25 | 2026-09-26T19:48:18Z | HTTP 200 | 2596115 | `50a6cab6bb4df8c79cf8781966ccec5a62ef29e2c0702d7c8237bf3f1f1c0d5e` |
| `S0-cp2k-hf` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/XC/HF.html> | CP2K 2026.2 manual | XC/HF: FRACTION (1.0 in mixed-potential calculations) | 2026-09-26T19:48:19Z | HTTP 200 | 72552 | `1c5bbbff7aa7d8305e2c92f7a8be3b02825e754c9c0a22cb371de9b2ac3d878e` |
| `S0-cp2k-hf-ip` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/XC/HF/INTERACTION_POTENTIAL.html> | CP2K 2026.2 manual | HF/INTERACTION_POTENTIAL: POTENTIAL_TYPE MIX_CL, OMEGA, SCALE_COULOMB, SCALE_LONGRANGE | 2026-09-26T19:48:20Z | HTTP 200 | 77879 | `ceda65a7a696ebb8f33de132a2a0f85951d13d330c591764fc03f9002b010dfa` |
| `S0-cp2k-vdw` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/XC/VDW_POTENTIAL.html> | CP2K 2026.2 manual | XC/VDW_POTENTIAL | 2026-09-26T19:48:20Z | HTTP 200 | 66719 | `589c30fe8a9e7ecbc858d26ca95f5979063adca22f4813a9fc88b6748f3fe64d` |
| `S0-cp2k-vdw-pair` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/XC/VDW_POTENTIAL/PAIR_POTENTIAL.html> | CP2K 2026.2 manual | VDW_POTENTIAL/PAIR_POTENTIAL: TYPE (default DFTD3(BJ)), D3_SCALING (s6, sr6, s8), CALCULATE_C9_TERM (F), R_CUTOFF (10.58 A, doubled), EPS_CN, PARAMETER_FILE_NAME | 2026-09-26T19:48:21Z | HTTP 200 | 108668 | `d964b13e00a5e87c100867bf98dedd8712a46da117a2108b3b966aa629403be2` |
| `S0-cp2k-scf` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/SCF.html> | CP2K 2026.2 manual | DFT/SCF: EPS_SCF 1e-5, MAX_SCF 50, SCF_GUESS values | 2026-09-26T19:48:22Z | HTTP 200 | 92560 | `f7bfeb7d25276eb167788547f679bd593f78352b744bd59fe351999367349ad6` |
| `S0-cp2k-poisson` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/POISSON.html> | CP2K 2026.2 manual | DFT/POISSON: PERIODIC, POISSON_SOLVER (MT, MULTIPOLE, WAVELET, ANALYTIC) | 2026-09-26T19:48:22Z | HTTP 200 | 68558 | `859bf837154f3bd382984e7fbc4aa73665b0f59991f1bfc611b3456de67de401` |
| `S0-cp2k-mgrid` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/MGRID.html> | CP2K 2026.2 manual | DFT/MGRID: CUTOFF 280 Ry, REL_CUTOFF 40 Ry, NGRIDS 4 | 2026-09-26T19:48:23Z | HTTP 200 | 77048 | `e4780f367dd1716fd4645893695016e14fe539b826ba7b4168d0941e8ce4b578` |
| `S0-cp2k-kind` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/SUBSYS/KIND.html> | CP2K 2026.2 manual | SUBSYS/KIND: BASIS_SET, POTENTIAL (ALL for all-electron), LEBEDEV_GRID 50, RADIAL_GRID 50 | 2026-09-26T19:48:23Z | HTTP 200 | 106642 | `213be6984fa2ce2cee4701b5c86a80e10f1efba526074e3cfb4d06f5df93e16e` |
| `S0-cp2k-geo-opt` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/MOTION/GEO_OPT.html> | CP2K 2026.2 manual | MOTION/GEO_OPT: OPTIMIZER BFGS, MAX_FORCE 4.5e-4, RMS_FORCE 3.0e-4, MAX_DR 3.0e-3, RMS_DR 1.5e-3, MAX_ITER 200 | 2026-09-26T19:48:24Z | HTTP 200 | 83053 | `70c0ee49a151de7bd6bd03d647cbaf2968a3981adb701f7c10d300d932712434` |
| `S0-cp2k-fixed-atoms` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/MOTION/CONSTRAINT/FIXED_ATOMS.html> | CP2K 2026.2 manual | MOTION/CONSTRAINT/FIXED_ATOMS: LIST, COMPONENTS_TO_FIX (XYZ) | 2026-09-26T19:48:25Z | HTTP 200 | 74912 | `08be63cc54ef056530102025862afafc713c1753ae29360abcd76ef8a42421db` |
| `S0-cp2k-mulliken` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/PRINT/MULLIKEN.html> | CP2K 2026.2 manual | DFT/PRINT/MULLIKEN: Mulliken (spin) population analysis | 2026-09-26T19:48:25Z | HTTP 200 | 76506 | `4ce30f5f82d0e6097dfe56488ec9d469e487d24ca3ccd3b471a873aea913b745` |
| `S0-cp2k-qmmm-link` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/QMMM/LINK.html> | CP2K 2026.2 manual | QMMM/LINK (classical-MM link atoms); comparison context only | 2026-09-26T19:48:26Z | HTTP 200 | 74843 | `759c16900a24fba855d8bd3478af9336319704c3b104de6c895adf2316e19c25` |
| `S0-pychemshell-subtractive` | <https://www.chemshell.org/wp-content/static_files/py-chemshell/manual/build/html/subtractive.html> | Py-ChemShell 25.0 manual | Subtractive QM/MM: NLayerSubtractive, Layer, link_atoms, gradients_eval, embedding | 2026-09-26T19:48:27Z | HTTP 200 | 14261 | `72cd4d1db119581a52ca94030a1686a6e110c6be44d5f56901ae226ef336e864` |
| `S0-pychemshell-qm` | <https://www.chemshell.org/wp-content/static_files/py-chemshell/manual/build/html/qm.html> | Py-ChemShell 25.0 manual | QM interfaces list (no xTB interface) | 2026-09-26T19:48:27Z | HTTP 200 | 21407 | `10bf86e4b9e2536fa424b24c923d557a24ddfc04bf047165d5704d74ca3ab16c` |
| `S0-pychemshell-cp2k` | <https://www.chemshell.org/wp-content/static_files/py-chemshell/manual/build/html/cp2k.html> | Py-ChemShell 25.0 manual | CP2K interface: functional values (no xTB, no wB97X-D3), basis, input | 2026-09-26T19:48:28Z | HTTP 200 | 32187 | `4b26f566ac3971d74cb8de96c5b4bf898ed8e217aee548e4b30415ebd81badce` |
| `S0-pychemshell-psi4` | <https://www.chemshell.org/wp-content/static_files/py-chemshell/manual/build/html/psi4.html> | Py-ChemShell 25.0 manual | Psi4 interface: method, functional, basis, charge, mult | 2026-09-26T19:48:28Z | HTTP 200 | 28886 | `17071114c70d721297ead608fe5b99a5dcd6f8cb7f1786c9cbe0cd2f88a48d9a` |
| `S0-pychemshell-qmmm-fail` | <https://www.chemshell.org/wp-content/static_files/py-chemshell/manual/build/html/qmmm.html> | Py-ChemShell 25.0 manual | NOT obtained (HTTP 404); not needed | 2026-09-26T19:48:28Z | HTTP 404 | 62009 | `f8e9cd27e6da3550f1e2ab60ac7c927188a27cc6b7328231401992790c47af7a` |
| `S0-psi4-hyb-funcs` | <https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/procrouting/dft/hyb_functionals.py> | Psi4 v1.11 tag | psi4/driver/procrouting/dft/hyb_functionals.py: functional dictionary format; no wB97X-D3 entry | 2026-09-26T19:48:30Z | HTTP 200 | 16360 | `9f675874fa289d39f2542c34c7f7ccd659e97f5cbdf63fd53cbde493f0b1d22c` |
| `S0-psi4-read-options` | <https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/src/read_options.cc> | Psi4 v1.11 tag | psi4/src/read_options.cc: REFERENCE (1464), GUESS (1505), E_CONVERGENCE (1544), D_CONVERGENCE (1551), DFT grid (1868-1870), INTS_TOLERANCE (1129), SCF_TYPE (194, 2000), DF_SCF_GUESS (1481), BASIS_GUESS (1566), DF_BASIS_SAD (1825), SAD_SCF_TYPE (1829) | 2026-09-26T19:48:30Z | HTTP 200 | 298807 | `f5e168622419211fb95eb2e9d31d5b0367ea76e84573bc6efb5e3c0511955ae3` |
| `S0-psi4-def2-tzvp` | <https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/share/psi4/basis/def2-tzvp.gbs> | Psi4 v1.11 tag | psi4/share/psi4/basis/def2-tzvp.gbs: spherical; H, C, O, Si, Ge; I with def2 ECP | 2026-09-26T19:48:31Z | HTTP 200 | 126891 | `c7b1fcc367e0cc31a3960a94972ec3b0b2b03f9df7e0627d9c414b9d8d0d1c6a` |
| `S0-psi4-empirical-disp` | <https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/procrouting/empirical_dispersion.py> | Psi4 v1.11 tag | psi4/driver/procrouting/empirical_dispersion.py; consulted, no wB97X entry | 2026-09-26T19:48:31Z | HTTP 200 | 20476 | `aba9852bd7a65069aeb52f0c77fecdfea4a23fef4bd4acc575355605cb73be37` |
| `S0-sdftd3-params` | <https://raw.githubusercontent.com/dftd3/simple-dftd3/v1.6.0/assets/parameters.toml> | simple-dftd3 v1.6.0 tag | assets/parameters.toml: default d3.zero (s6 1.0, s9 1.0, rs8 1.0, alp 14); [parameter.wb97x] d3.zero rs6 1.281, s8 1.0, rs8 1.094, doi 10.1021/ct300715s | 2026-09-26T19:48:31Z | HTTP 200 | 32719 | `b1d9d1b9882dcad5361a99c34745ad44f8a274d80c907d9d0187255e4323d645` |
| `S0-wb97xd3-doi` | <https://doi.org/10.1021/ct300715s> | Lin et al., J. Chem. Theory Comput. (defining reference) | NOT obtained (HTTP 403); [GAP] | 2026-09-26T19:48:31Z | HTTP 403 | 5508 | `8d7eb71a097f4be0d9fe3183fd8d5cdfb27c3453997d5141a90d179377c61f52` |
| `S0-cp2k-data-listing` | <https://api.github.com/repos/cp2k/cp2k/contents/data?ref=support/v2026.2> | CP2K support/v2026.2 branch | GitHub API listing of data/ (68 entries) | 2026-09-26T19:54:08Z | HTTP 200 | 53633 | `9c0ec15741733be8d453f7ed472cb1c6592f85c3c18477afd9ca4db39c826d47` |
| `S0-libxc-wb97` | <https://gitlab.com/libxc/libxc/-/raw/7.0.0/src/hyb_gga_xc_wb97.c> | libxc 7.0.0 tag | src/hyb_gga_xc_wb97.c line 80: wB97X-D3 1.0, -(1.0 - 0.195728), 0.25 | 2026-09-26T19:54:08Z | HTTP 200 | 5706 | `e9a149fb74512ef9ab87d4758bb1ec0dff4855b7ea4be5f4a72a4b801e70f7ce` |
| `S0-libxc-hybrids` | <https://gitlab.com/libxc/libxc/-/raw/7.0.0/src/hybrids.c> | libxc 7.0.0 tag | src/hybrids.c: cam_alpha, cam_beta, cam_omega | 2026-09-26T19:54:09Z | HTTP 200 | 1723 | `ff9dd59d339cff24f72e1c6c85b2b3a70929f892c23d60762f4a363664350ff9` |
| `S0-cp2k-emsl-basis` | <https://raw.githubusercontent.com/cp2k/cp2k/support/v2026.2/data/EMSL_BASIS_SETS> | CP2K support/v2026.2 branch | data/EMSL_BASIS_SETS: Ahlrichs-def2-TZVP for H, C, O, Si, Ge; none for I | 2026-09-26T19:54:19Z | HTTP 200 | 1713484 | `6f1f4b1b707583e0129a149c54221a633a039132f787e5df3d208ff6e8182d84` |
| `S0-cp2k-all-basis` | <https://raw.githubusercontent.com/cp2k/cp2k/support/v2026.2/data/ALL_BASIS_SETS> | CP2K support/v2026.2 branch | data/ALL_BASIS_SETS: no def2 entry | 2026-09-26T19:54:19Z | HTTP 200 | 189331 | `22d8d915c81d8e0a3f471dd8db6477f9498445f0dbb9341c67f8a307f639e883` |
| `S0-cp2k-ecp` | <https://raw.githubusercontent.com/cp2k/cp2k/support/v2026.2/data/ECP_POTENTIALS> | CP2K support/v2026.2 branch | data/ECP_POTENTIALS: no def2 entry | 2026-09-26T19:54:20Z | HTTP 200 | 243766 | `a9dbd382c96344c0cc4bcb96f27ae05ea1ca332ad37042e1b6a5656dd7d4aec4` |
| `S0-cp2k-hf-screening` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/XC/HF/SCREENING.html> | CP2K 2026.2 manual | HF/SCREENING: EPS_SCHWARZ 1e-10, EPS_SCHWARZ_FORCES 1e-6 | 2026-09-26T19:59:12Z | HTTP 200 | 72996 | `40d9c50f2a0f63a43f4b907280f6bc0eaf970c6ad10371d94fecff2dd2140434` |
| `S0-cp2k-print-forces` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/PRINT/FORCES.html> | CP2K 2026.2 manual | FORCE_EVAL/PRINT/FORCES: NDIGITS 8 | 2026-09-26T19:59:13Z | HTTP 200 | 74749 | `2bbe1155bc39878cff78667a9e53072087ab273f8f97ade4c333746de04b6ea9` |
| `S0-cp2k-src-disp-pairpot` | <https://raw.githubusercontent.com/cp2k/cp2k/support/v2026.2/src/qs_dispersion_pairpot.F> | CP2K support/v2026.2 branch | src/qs_dispersion_pairpot.F line 266: alp default 14 | 2026-09-26T19:59:14Z | HTTP 200 | 27663 | `47ec827a9760fa38ba53e055e22884d2bbe7631b61ea2087a747e8c03bda8889` |
| `S0-cp2k-src-disp-utils` | <https://raw.githubusercontent.com/cp2k/cp2k/support/v2026.2/src/qs_dispersion_utils.F> | CP2K support/v2026.2 branch | src/qs_dispersion_utils.F lines 258-326: D3_SCALING read as s6, sr6, s8; no wB97X lookup entry | 2026-09-26T19:59:14Z | HTTP 200 | 55243 | `587b8b35f0fadba226335ec4b45b5290260ea05c67eb8b77b8ec1511ba4bd337` |
| `S0-cp2k-src-disp-d3` | <https://raw.githubusercontent.com/cp2k/cp2k/support/v2026.2/src/qs_dispersion_d3.F> | CP2K support/v2026.2 branch | src/qs_dispersion_d3.F lines 181-187: alp8 = alp6 + 2; rs8 = 1.0 (hard-coded) | 2026-09-26T19:59:53Z | HTTP 200 | 54007 | `447982f6ff48157367fde23cb24af58d21b0728a5b0c75ec77923544c02c2f66` |
| `S0-qcng-disp-resources` | <https://raw.githubusercontent.com/MolSSI/QCEngine/v0.51.0/qcengine/programs/empirical_dispersion_resources.py> | qcengine v0.51.0 tag | qcengine/programs/empirical_dispersion_resources.py: d3zero2b default keys s6, s8, sr6, alpha6, sr8 (line 69); wb97x d3zero2b parameters (line 204). Byte-identical to the file installed with the E-01 Psi4 build (SHA256 recorded in results/e01/method-config.json) | 2026-09-26T20:54:12Z | HTTP 200 | 81052 | `aedefaff49b8aba9c66943fb6d1c5e0cbd87db10df310b67bbc87ca952404ddb` |
| `S0-qcng-dftd-ng` | <https://raw.githubusercontent.com/MolSSI/QCEngine/v0.51.0/qcengine/programs/dftd_ng.py> | qcengine v0.51.0 tag | qcengine/programs/dftd_ng.py lines 299-302: 2b levels routed to s-dftd3 with s9 = 0.0. Byte-identical to the installed file (SHA256 recorded in results/e01/method-config.json) | 2026-09-26T20:54:12Z | HTTP 200 | 16386 | `b90f3534df1b2c699492063432fe771a530c7fe91e6f1f60d493e07b6615fced` |
| `S0-psi4-dft-builder` | <https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/procrouting/dft/dft_builder.py> | Psi4 v1.11 tag | psi4/driver/procrouting/dft/dft_builder.py lines 235-243: dispersion type and exact params key set checked against dashcoeff; lines 370-383: MP2 coefficient set only from a c_mp2 block | 2026-09-26T20:54:12Z | HTTP 200 | 20421 | `b29d52e450f632793103b01249e27e2c6d61a48859b3c65d17f8cf4de45dad5a` |
| `S0-psi4-driver` | <https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/driver.py> | Psi4 v1.11 tag | psi4/driver/driver.py; consulted: no SCF convergence defaults set there | 2026-09-26T20:54:12Z | HTTP 200 | 133069 | `7d2485decb726bf62f18ca5f6c624b6dbc36d540dc9fbe2187a232189be13db6` |
| `S0-cp2k-scf-ot` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/SCF/OT.html> | CP2K 2026.2 manual | SCF/OT: section off by default (SECTION_PARAMETERS F) | 2026-09-26T20:54:12Z | HTTP 200 | 119554 | `7cbb09ce82c7db6537f4c7b4fbdbcd6e057fb675fe99ffb9c221682d6777d869` |
| `S0-cp2k-scf-diag` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/SCF/DIAGONALIZATION.html> | CP2K 2026.2 manual | SCF/DIAGONALIZATION: section off unless requested; ALGORITHM STANDARD default | 2026-09-26T20:54:13Z | HTTP 200 | 74998 | `ce2e520745231e2561e831a52100cad1798e40f0e20de00a40db1cdf7cf204b4` |
| `S0-cp2k-scf-mixing` | <https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/SCF/MIXING.html> | CP2K 2026.2 manual | SCF/MIXING: on by default; METHOD DIRECT_P_MIXING; ALPHA 0.4 | 2026-09-26T20:54:14Z | HTTP 200 | 95141 | `18b2772c8d76564fa4ace05fa597455a3643cfaabd80ed972543012b793ac3f0` |
| `S0-sdftd3-qcschema` | <https://raw.githubusercontent.com/dftd3/simple-dftd3/v1.6.0/python/dftd3/qcschema.py> | simple-dftd3 v1.6.0 tag | python/dftd3/qcschema.py lines 315-319: params_tweaks passed as keyword arguments to the damping-parameter class | 2026-09-26T20:55:25Z | HTTP 200 | 14751 | `52090940392211ba54a96eb79a649d68cb7f0108ec1e35dd0eb6b8ca8e1919b2` |
| `S0-sdftd3-interface` | <https://raw.githubusercontent.com/dftd3/simple-dftd3/v1.6.0/python/dftd3/interface.py> | simple-dftd3 v1.6.0 tag | python/dftd3/interface.py lines 257-286: ZeroDampingParam renames sr6->rs6, sr8->rs8, alpha6->alp; s9 default 1.0 | 2026-09-26T20:56:05Z | HTTP 200 | 23492 | `3db1f7b32330efd89f200381c51a8e46e22aafbfd313d8fa034fb7b4bb21d962` |
| `S0-psi4-proc` | <https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/procrouting/proc.py> | Psi4 v1.11 tag | psi4/driver/procrouting/proc.py; same bytes as SOURCES [9]; sets no SCF energy or density convergence defaults for SCF energies or gradients; DF_BASIS_SCF built only when needed, including DIRECT with DF_SCF_GUESS (1452-1468); SAD bases, with DF_BASIS_SAD only when SAD_SCF_TYPE contains DF (1479-1495); C1-copy JKFIT basis only under use_c1 (1752, 2112-2135); BASIS_GUESS (1825-1860); GUESS AUTO (1883-1888); DF_BASIS_MP2 only for double hybrids (2765-2776); run_scf_gradient to core.scfgrad (2845-2869) | 2026-09-26T20:56:42Z | HTTP 200 | 240508 | `98ac648d84cc4587ec034b9207d3c6fbc3cd74df4c0409a85478e5467c0dd408` |
| `S0-psi4-driver-util` | <https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/driver_util.py> | Psi4 v1.11 tag | psi4/driver/driver_util.py lines 40-86: SCF E/D convergence set to 1e-6 (energy) or 1e-8 (analytic gradient) only if not changed by the user | 2026-09-26T20:57:13Z | HTTP 200 | 21760 | `f7e8118f835d5c669526089abf03321ca33b9e0b220f0d24ed9360e0cdb6219c` |

## Installed source files read locally

These files were read in the project-local environment and were not retrieved over the network. Each is
identified by its own SHA256 and by the SHA256 of the distribution archive that contains it. The archive digests
are those recorded by the hash-locked installation ([C3 §1](C3-PROVENANCE-WIRING.md#1-environment)).

| ID | File | SHA256 of the file | Distribution (archive SHA256) | Locator and use |
|---|---|---|---|---|
| `S0-ase-src-extxyz` | `ase/io/extxyz.py` | `bae127796d6f89f6144733ade5ba8c44920ee182b1b0dae2a7c85de9feef277e` | ASE 3.29.0 wheel (`7b9dd103f007810339c24acfee2f6b677c0c48443b21d3c98e52959246cf4ebf`) | Lines 494–502 and 805–819 (`move_mask` for FixAtoms and FixCartesian); line 796 (periodic flags always saved) |
| `S0-ase-src-data` | `ase/data/__init__.py` | `4bb3b1a8d330c3fcdf2d0321a4d8cc3eae55d1f860034261565661d0203c07e0` | ASE 3.29.0 wheel | Lines 436–442 (citation of Cordero et al. 2008); covalent radii H 447, C 452, O 454, Si 460, Ge 478; `reference_states` Si 593 (diamond, a = 5.43) |
| `S0-ase-src-surface` | `ase/build/surface.py` | `61d203ba9f5b540023c307de5c11051a0355958cd20c4a0393fe66866b036ddc` | ASE 3.29.0 wheel | `diamond100` (line 187) and `_surface` (line 362), used by the geometry generator |
| `S0-ase-src-qmmm` | `ase/calculators/qmmm.py` | `6573b57150bbc88f617f7c0707979c52f841b37d870f5ac185ae2640f4ccc109` | ASE 3.29.0 wheel | `SimpleQMMM`: subset `atoms[selection]` (line 62), vacuum centering (65–66), energy and force composition (69–90) |
| `S0-aiida-src-structure` | `aiida/orm/nodes/data/structure.py` | `6079686947454367ba41591a24f2f371652934edc68fbe5bc5c3285b218940a8` | aiida-core 2.9.2 wheel (`72ec503b427936a00a5b5d81ae7224b40e42065373e95def2795ccecded77bdd`) | `set_ase` (lines 808–818); ASE tag to kind name (2025–2027) |
| `S0-aiida-src-transport` | `aiida/transports/transport.py` | `8fbc221847c7d60d410bbc173ad89a925090047699eda36072bdbaa71d464faf` | aiida-core 2.9.2 wheel | `use_login_shell`, default true (lines 114–121) |
| `S0-aiida-src-dos` | `aiida/repository/backend/disk_object_store.py` | `9b9ff39326cf2af5cb09c95fad28f908f41b421f0d57c0c3b6e7b03c72dfb618` | aiida-core 2.9.2 wheel | SHA256 hash-type check (line 145) |
| `S0-aiida-src-presto` | `aiida/cmdline/commands/cmd_presto.py` | `a25cd5512abf7d482c67e8c7f7c0b9383d2ac7e83fa500954c6bae264a27e1b8` | aiida-core 2.9.2 wheel | Default email (line 119); scratch directory under the configuration directory (279–287) |
| `S0-aiida-src-add` | `aiida/calculations/arithmetic/add.py` and `aiida/parsers/plugins/arithmetic/add.py` | `b5eaf2de557602b638885387f6b5a5fd8eafb4a1a32f574d146a3ec471019a13` and `f8e599564233484896fe35ed7778b9380f031a20ee4832fe2475933ac06d8a3e` | aiida-core 2.9.2 wheel | The trivial job of C3 and its exit codes |
| `S0-aiida-src-container` | `disk_objectstore/container.py` | `e1c185805c5c672a94b971f2208a96d8a6f0241bea0fb7f60f6630b685b06234` | disk-objectstore 1.5.0 wheel (`55dbdaa99340cf127a61d38926ae801a728a7028cc4e487b59a873aa0af9c172`) | `hash_type` default `sha256` (line 310) |
| `S0-aiida-cp2k-src` | `aiida_cp2k/calculations/__init__.py` | `f2fbdf6096ebef8217e60f139498adb6ff69973e9047c68cf00996214f7f9d9b` | aiida-cp2k 2.1.1 source archive (`a5f9dfd520628d59be4bc4a193597889b88c84daddf563c5b909fba23afb9876`), read without installation | Inputs (lines 62–131); structure writing (275–300, 431–436); kind names from tags (452–462); retrieve list (396–404) |
| `S0-aiida-cp2k-parser` | `aiida_cp2k/utils/parser.py` | `3acda03cc5361de51167d2ef843ef4a77f0916fb17ef82057c12d3888259d45d` | same archive | `energy_units` (lines 24, 50); version from the `CP2K\| version string:` line (44–46) |

## Project records cited

| Record | Where |
|---|---|
| SOURCES [11], [20], [22] (Libxc 7.1.2 printed by the installed Psi4 1.11; the Psi4 installation; simple-dftd3 1.6.0, including the sr8 = 1.094 printed at E-01) | [docs/SOURCES.md](../SOURCES.md) |
| The tool bond table used to derive the cut bonds | [tools/activated-donor-bonds.tsv](../../tools/activated-donor-bonds.tsv) |

## Source-resolution retrievals, 2026-09-27

This dated section records the sources of the [source resolution record](SOURCE-RESOLUTION.md) of 2026-09-27.
- **Retrievals.** It adds 16 retrievals; every request returned HTTP 200 and none failed. Access times are the UTC
  start times of the requests.
- **Bytes and URLs.** The retrieved bytes are kept privately and are not copied here. The release archive's download
  redirects to a signed storage address, which is not recorded publicly; the table gives the requested URL.
- **Two kinds of identity.** The ref, tag and commit records are tag-resolution metadata. The archive and file rows
  are content hashes.

| ID | URL | Version | Locator and use | Accessed (UTC) | Result | Retrieved bytes | SHA256 of retrieved bytes |
|---|---|---|---|---|---|---:|---|
| `SR-cp2k-release-v2026.2-api` | <https://api.github.com/repos/cp2k/cp2k/releases/tags/v2026.2> | CP2K v2026.2 release record | Tag name, publication time, and the asset `cp2k-2026.2.tar.bz2` with its published SHA256 | 2026-09-27T14:35:33Z | HTTP 200 | 9861 | `15a969ef78db0465a6c395bb1662a9412dca01e6f338d7db5c512c823fecd4cf` |
| `SR-cp2k-ref-tag-v2026.2-api` | <https://api.github.com/repos/cp2k/cp2k/git/ref/tags/v2026.2> | Tag ref | `refs/tags/v2026.2` resolves to the annotated tag object `09496e05…` | 2026-09-27T14:35:33Z | HTTP 200 | 323 | `98489706021db695966d036f9af66d271cf0b207f44156362e7bffe610d81158` |
| `SR-cp2k-tagobj-v2026.2-api` | <https://api.github.com/repos/cp2k/cp2k/git/tags/09496e055e132aa3dba53a7751ebdf432b4ebb78> | Annotated tag object | Resolves to commit `67b5da87…`; tagger date; verification `unsigned` | 2026-09-27T14:38:04Z | HTTP 200 | 661 | `a886cd0859d3fbab32571f6bf443155cdba222e36a98c68c89eee27e45db1407` |
| `SR-cp2k-ref-branch-support-v2026.2-api` | <https://api.github.com/repos/cp2k/cp2k/git/ref/heads/support/v2026.2> | Branch ref (mutable) | Branch head at the access time: `67b5da87…` | 2026-09-27T14:38:17Z | HTTP 200 | 359 | `621d28946a983618362990eb4f14a9b8d88b21ce5a484239e85c7e561fc51f4e` |
| `SR-cp2k-2026.2-release-tarball` | <https://github.com/cp2k/cp2k/releases/download/v2026.2/cp2k-2026.2.tar.bz2> | CP2K 2026.2 release archive | The source of every CP2K locator of the source resolution. Its SHA256 equals the digest published in the release record. The files read are listed below | 2026-09-27T14:38:37Z | HTTP 200 | 79898041 | `f9bd86f580f57a53a0768c0045d1417f9f9a1d66d851ed7f662f496200043373` |
| `SR-cp2k-commit-67b5da87-api` | <https://api.github.com/repos/cp2k/cp2k/commits/67b5da876dd6a76b8b021d5a04d1c81ba79a4c50> | Commit record of the release revision | Parent `c92cc08b…`; the four files changed, including the added `REVISION` | 2026-09-27T14:39:29Z | HTTP 200 | 7200 | `399ec8189566b6e52aa305eb708ff7813f0cdd9409b7b355d0c4c8812efae9d7` |
| `SR-cp2k-commit-c92cc08-api` | <https://api.github.com/repos/cp2k/cp2k/commits/c92cc08> | Commit record of the parent | Full identity `c92cc08b45378b85150447011b5a4bb552f5b797`, the revision named inside the archive | 2026-09-27T14:39:30Z | HTTP 200 | 85164 | `1fb9dc4afd469ddf2506fac6decfc4c3349a053c6fbfaf43b1280534e98f5f48` |
| `SR-cp2k-tree-67b5da87-api` | <https://api.github.com/repos/cp2k/cp2k/git/trees/67b5da876dd6a76b8b021d5a04d1c81ba79a4c50?recursive=1> | Tree of the release revision | Git blob SHA1 of every path (8 999 blobs, not truncated), compared with the archive and the cached files | 2026-09-27T14:40:45Z | HTTP 200 | 2301084 | `039dbcbf2bd94f70284495a34a03d71ce46e24d07aaaae88f87195cc0d410453` |
| `SR-psi4-release-v1.11-api` | <https://api.github.com/repos/psi4/psi4/releases/tags/v1.11> | Psi4 v1.11 release record | No source asset | 2026-09-27T14:47:15Z | HTTP 200 | 15328 | `62a6179c3a625cc77a903b98d5788f4496459a546bc39a49aca684308fc3929c` |
| `SR-psi4-ref-tag-v1.11-api` | <https://api.github.com/repos/psi4/psi4/git/ref/tags/v1.11> | Tag ref | Resolves to the annotated tag object `75fa0e14…` | 2026-09-27T14:47:15Z | HTTP 200 | 315 | `e45d1eb8ca8efab576c98b974688b770f1fc887e5c6b1a0be1b7ac091e50d9aa` |
| `SR-psi4-tagobj-v1.11-api` | <https://api.github.com/repos/psi4/psi4/git/tags/75fa0e14aa16a868a00eced50eaaa2f8658aa806> | Annotated tag object | Resolves to commit `f16f4ea2…`; verification `unsigned` | 2026-09-27T14:48:59Z | HTTP 200 | 641 | `651f5c8ea235e3a0b317476dff00464c1e84b5ad1883c9b0fa20e20c498a00c3` |
| `SR-psi4-tree-f16f4ea2-api` | <https://api.github.com/repos/psi4/psi4/git/trees/f16f4ea2ff2351cc2ab877d9b3887fcf81c2a670?recursive=1> | Tree of the tag commit | 9 821 blobs, not truncated | 2026-09-27T14:49:25Z | HTTP 200 | 2663531 | `a833c41fb686be0bf79a433b7ca135e5d74003bf49884ac147e29ff08a64f1bd` |
| `SR-psi4-archive-f16f4ea2` | <https://github.com/psi4/psi4/archive/f16f4ea2ff2351cc2ab877d9b3887fcf81c2a670.tar.gz> | GitHub-generated archive of the v1.11 tag commit | The source of every Psi4 locator. It is not a published release asset. All 9 821 files equal the tree's blobs | 2026-09-27T14:49:25Z | HTTP 200 | 51818737 | `040e843efd4e70d286d8705e501bd2be5c7f1f855ec439eb8a27e6565af50266` |
| `SR-libint-ref-tag-v2.8.1-api` | <https://api.github.com/repos/evaleev/libint/git/ref/tags/v2.8.1> | Libint tag ref | A lightweight tag on commit `4482d01abc37732a24b24799d3efe1d1f89a2891` | 2026-09-27T14:52:21Z | HTTP 200 | 337 | `bea1d502b50c7503c39b7fececf8963aaeee8c3c3c729bf4996a076c1173f39c` |
| `SR-libint-v2.8.1-shell-h` | <https://raw.githubusercontent.com/evaleev/libint/v2.8.1/include/libint2/shell.h> | Libint v2.8.1, by tag | `include/libint2/shell.h` | 2026-09-27T14:52:22Z | HTTP 200 | 28504 | `c798162776893960c44fc119a69c00f201c28e164da0885522a5889f7c0e4f00` |
| `SR-libint-4482d01a-shell-h` | <https://raw.githubusercontent.com/evaleev/libint/4482d01abc37732a24b24799d3efe1d1f89a2891/include/libint2/shell.h> | Libint v2.8.1, by commit | The same bytes as by tag: the `Shell` constructor, the unit-normalization flag and `renorm()`. This is the version that Psi4 v1.11 names as its source pin and minimum; it is not the identity of any build | 2026-09-27T14:52:48Z | HTTP 200 | 28504 | `c798162776893960c44fc119a69c00f201c28e164da0885522a5889f7c0e4f00` |

### Archives against their trees

- **The CP2K release archive.**
  - Its 8 985 regular files equal, by Git blob SHA1, the tree of the release revision
    `67b5da876dd6a76b8b021d5a04d1c81ba79a4c50`.
  - Of the tree's 8 999 blob entries, 14 have no regular-file match. Ten are Git metadata files (`.gitignore` files,
    `.gitattributes` and `.git-blame-ignore-revs`), and they, like `CODEOWNERS`, are absent from the archive. Three
    are symbolic links present in the archive as links: `CONTRIBUTING.md`, `data/BASIS_MOLOPT_UZH` and
    `data/POTENTIAL_UZH`. The links were not compared by content.
  - The archive's `REVISION` file names `c92cc08`, the parent of the release revision.
  - The locators below are at the release revision.
- **The Psi4 archive.** All 9 821 of its files equal the blobs of the tree of commit
  `f16f4ea2ff2351cc2ab877d9b3887fcf81c2a670`.

### Files read inside the retrieved archives

Each file is identified by its own SHA256 and by its Git blob SHA1, which equals the blob of the tag-commit tree.
Every cited line range was checked by a measure-then-assert script: 211 assertions over these 72 files pass.

| Archive | File | SHA256 of the file | Git blob SHA1 (equal to the tag-commit tree) | Lines cited |
|---|---|---|---|---|
| `SR-cp2k-2026.2-release-tarball` | `CMakeLists.txt` | `147aaf86596e26e39ce857b62b357f241b59b894b02c5f2dc47476ba58c860b5` | `075f91973c0813684ee791ecba2a95967b4a464d` (yes) | 871–884, 886–889 |
| `SR-cp2k-2026.2-release-tarball` | `cmake/CompilerConfiguration.cmake` | `f371023e738913431e4be9a032a5e991082d2f041f87d673d9e5177d887379c1` | `c6c22850f429588c51543569275a27f0c59aaaa1` (yes) | 146–148 |
| `SR-cp2k-2026.2-release-tarball` | `data/EMSL_BASIS_SETS` | `6f1f4b1b707583e0129a149c54221a633a039132f787e5df3d208ff6e8182d84` | `075418a24b619ab0bfe1555c45efa116a47bbd36` (yes) | 33982–34010 |
| `SR-cp2k-2026.2-release-tarball` | `data/xTB0_parameters` | `278461cabbf89b14379aedc78ef3e141c8cef1f911f3a3c72530aec7a52b6d34` | `4c9f997f3e7e57daa3f600e23d56b9790b44e87d` (yes) | 1–4, 29, 117, 155, 274, 649 |
| `SR-cp2k-2026.2-release-tarball` | `src/CMakeLists.txt` | `6f95a743974942ef15f898480ea46d60954a5e640d6b7206cfc056c664573573` | `21439a11e8123963161ca0ff56927545b77bc594` (yes) | 1825–1836 |
| `SR-cp2k-2026.2-release-tarball` | `src/aobasis/basis_set_types.F` | `a4f386c0f616c76025ed2e456cbb14a24c61f59cc2376921009f51e60ea088b3` | `3b2b3555fa93903dcec07939e982a7963e8f401b` (yes) | 78, 843–859, 1056–1098, 1137–1174, 1182–1202, 1269, 1375–1385, 1410–1420 |
| `SR-cp2k-2026.2-release-tarball` | `src/aobasis/soft_basis_set.F` | `f1e9cdcc5924a78d7a942236f8c1b26908c211db30d92f3a32ddc017b7e73627` | `f4dd7b524bb79d5fbd156bd759bd8ec0b6f91e5f` (yes) | 292 |
| `SR-cp2k-2026.2-release-tarball` | `src/common/cp_data_dir.c` | `a5119a6bec254fafb15e91162d8d286ead315627f9c92c1989e58585316cd33f` | `1d81fbb5142c0dbd34666dde9db9d6309e0d71fc` (yes) | 18–24 |
| `SR-cp2k-2026.2-release-tarball` | `src/common/cp_files.F` | `70c66ab8839d3f9b089114ef3c2a5bcb77c248c9d258854d4f009551675193f8` | `8ce55815ba496ea15f934c8c5d0a6c2738b97a10` (yes) | 447–466, 520–550 |
| `SR-cp2k-2026.2-release-tarball` | `src/common/cp_units.F` | `e853a2e91a4949b81a034de949bb7a03d511da01e2753baac7e7ca8efaca7c3a` | `9677341fd43f1a6a1ce41e1c3221e1bd410ecfbf` (yes) | 720–733 |
| `SR-cp2k-2026.2-release-tarball` | `src/common/physcon.F` | `b7c6a5d2c98ddc90652460059049919fc08512ecfcd32861790c6fd2a928cffb` | `5dfbeaa2ff8706eeb265ef3a06e3fb5a975ec007` (yes) | 147 |
| `SR-cp2k-2026.2-release-tarball` | `src/constraint_fxd.F` | `99e1a032cb2b64cfbc77eda42aba30dbfc38b6b97cd269eae4d5c8cb3745ead1` | `225416d12d4b3b36253f115916d32409d5a43837` (yes) | 220–223, 230–240 |
| `SR-cp2k-2026.2-release-tarball` | `src/cp2k_info.F` | `2b41d36f77967beaada5f797a650926b5b1d19622b83342339e1ce33a50e34ab` | `872951cffda9f289cd890a5fc224c924360ff4cc` (yes) | 226–234 |
| `SR-cp2k-2026.2-release-tarball` | `src/cp_control_utils.F` | `da04a34bb800c6ccc9314a9e434abca7b0f1482a250f1672bb0cd27adff6aa39` | `3a2478e19e0bc67c8fad09fd00736d0b3ef3f960` (yes) | 1482, 1561–1571, 1574–1580, 1579–1594, 1606–1612, 1625–1632, 1651–1662, 1714–1720, 1737–1740, 1777–1784, 1820–1829, 2712–2713, 2736–2738, 2753–2754 |
| `SR-cp2k-2026.2-release-tarball` | `src/force_env_methods.F` | `82b08e7e477c1fe2f1f0ce82b80202dd93863b0b3ab420fa9ba5fe1f35851ada` | `28cbe7e2acafffa9ff01df4dc0c5380bd19a0c1f` (yes) | 314, 361, 366–369, 419–445, 1229–1231, 1356–1385 |
| `SR-cp2k-2026.2-release-tarball` | `src/force_env_utils.F` | `67279322d29605b85e5f7c39210b004d58ccfe8a9144a5ba8690a232d6f2fdc5` | `699045290f6f972f8eb8e7c8ffdf5eca27a20d9e` (yes) | 430–436, 482, 486–490, 503, 577–580, 591 |
| `SR-cp2k-2026.2-release-tarball` | `src/header.F` | `c1ea2aefeca296e9df7ec24ee74a96898b2412c127591c8bd9b2d2452d8d38c7` | `1acadbff542aa4b871e50b2d6e320c25cf1a03c7` (yes) | 216–245 |
| `SR-cp2k-2026.2-release-tarball` | `src/hfx_libint_interface.F` | `476789b2343a023e707f5b196067d7a41354e132d9e8946ad7f195a877a15edc` | `8db58d4b75cdde352bb243d7ce42f6742c741e4a` (yes) | 97–105, 167–179 |
| `SR-cp2k-2026.2-release-tarball` | `src/hfx_pair_list_methods.F` | `f93a70321f1bc0d32bbd4e11181877b23c38e3086eb615d6b9d8b1dd40923b99` | `d0ea682b913be23f05e497ef29e8131186a8517e` (yes) | 332–345 |
| `SR-cp2k-2026.2-release-tarball` | `src/hfx_types.F` | `7299cfa3462bcbb476f78a636c9a40f26cce62d1223d7eba6b564f22275b3b50` | `1c11cc9d779e9144038d2619c77a3f1196b4fb5a` (yes) | 719–720, 1746–1761, 2888–2892 |
| `SR-cp2k-2026.2-release-tarball` | `src/input/input_keyword_types.F` | `6ba30b4d1da1e9cf4a223344743b66b5a8e080efbfaa92b65072ac45dd3d5c79` | `1665d10024189e859b003fed8c757473827f9c74` (yes) | 202, 407–409 |
| `SR-cp2k-2026.2-release-tarball` | `src/input/input_parsing.F` | `7a61a8ad06610de89a0b71dc907343655c29160ee8c30ee6d39e804e69bd0299` | `dab4ca7b6bacced82c1e4ba901a387859e075b26` (yes) | 651–695 |
| `SR-cp2k-2026.2-release-tarball` | `src/input_cp2k_force_eval.F` | `966515458634db9fb5355423781bc69e28ffa4bb65689c10b7ccef7e06413c0f` | `cea88f47605a5c9bc49646e0127bc427f0320b7e` (yes) | 321–343 |
| `SR-cp2k-2026.2-release-tarball` | `src/input_cp2k_hfx.F` | `468ef8c01d0285e2341617d9df269dd3eb227c7006da14937f17acad2db7177f` | `d2b7d2a4b87e75c973201a315a1fe30515ff3f2e` (yes) | 253–266, 272–280, 303–311 |
| `SR-cp2k-2026.2-release-tarball` | `src/input_cp2k_motion_print.F` | `33b63bf95fe3062f1865d3c6cb9ef54b174a8effe7dd196b897fcbe3ccb2b138` | `f37d1b4c39cd7399d187376b15297fc8e86d2bd0` (yes) | 199–203, 361–367 |
| `SR-cp2k-2026.2-release-tarball` | `src/input_cp2k_print_dft.F` | `2cef0bc8e85f0ec6c291a5c5101da55fea0658440c15647d42220f530c0aa2bc` | `304ca5399095e7a80b52df073e2a8ce5b69cc03a` (yes) | 818–820 |
| `SR-cp2k-2026.2-release-tarball` | `src/input_cp2k_tb.F` | `695ae4fc6f92b20c5cfbb10f0619fd35ffd2c9f2d58aee6dd3f8760c19ea5c7a` | `ba3342df1b3903dd8f6a8084e7b9e01f9b17cc06` (yes) | 181–193, 214–224, 239–242, 427–431, 434–438, 472–477, 549–555 |
| `SR-cp2k-2026.2-release-tarball` | `src/libint_2c_3c.F` | `dac61e0cfdb4a8bdf554ba18101ab719c65eb06a84d80a23b9a8bd6c236c47ee` | `e7698ae20d129ff8f13226bfe6a688502361b38b` (yes) | 372–375 |
| `SR-cp2k-2026.2-release-tarball` | `src/motion/bfgs_optimizer.F` | `10f3c8588f863d672ef8757babc949591b65e37c3f8616e15d2b59532d039dea` | `ef6ae345ea076f404cb3df84b09568f690e0c3c8` (yes) | 290, 294–297, 341–344, 386–388, 405, 409–410, 414–417, 427–428, 484–520, 653–694, 765–813, 871–892, 1000–1022 |
| `SR-cp2k-2026.2-release-tarball` | `src/motion/gopt_f77_methods.F` | `aed5caa7ad3d134df229ffd0a2d472de67aa49c12ec3fab8e3e0b0a0d026b972` | `8d5b6727fd4db34b5eaab2fa8a13215cdb017345` (yes) | 132–134, 141–147 |
| `SR-cp2k-2026.2-release-tarball` | `src/motion/gopt_f_methods.F` | `af0a983bd5d43b4843f7394e90ef001e0bbcd0800703ff47798456404cbdc8b2` | `65682a68caa69a6eb002f6ebfa6828b5c5a9d6bd` (yes) | 340–342, 660–666, 669, 700–710, 717–720, 939–941 |
| `SR-cp2k-2026.2-release-tarball` | `src/motion_utils.F` | `478a5431bcb3f6ccc6af02f7d8ec6312ed618d1128317b08117bb81a29731001` | `d83916a8e33606be6ca2b286b667cfaa86a9db84` (yes) | 380–382, 401–405 |
| `SR-cp2k-2026.2-release-tarball` | `src/particle_methods.F` | `eba3978a2a8336b48dbeea33efc3f08e79da51b40ddc6f305ca83fc404b10389` | `e7336c66ad4f47a4c353dd85b989bfbd19450372` (yes) | 303–309 |
| `SR-cp2k-2026.2-release-tarball` | `src/qs_dispersion_d4.F` | `3699c01defd8dd4c13cb57542a04eda0c832a2276af2e5d75e31115de4038097` | `dcf321e4f0bf84151f25431ba353cf3b4fba3d1d` (yes) | 88–112, 259–271, 296–304, 790 |
| `SR-cp2k-2026.2-release-tarball` | `src/qs_environment.F` | `51acf59832239e5610dcb8b3c7117d1311f42d5eb5beb39400591b724ed5e777` | `bf7ae4766d93830f69d35594c8d863224cd55a43` (yes) | 1233–1234, 1941–1946 |
| `SR-cp2k-2026.2-release-tarball` | `src/qs_kind_types.F` | `40ec254a7820bb3976ff7661db1053d11af8a5d33a231f9123a81c5e210736b1` | `8928bc45536fa988d470995b4bc83962ad80fce2` (yes) | 1338–1345 |
| `SR-cp2k-2026.2-release-tarball` | `src/start/input_cp2k_motion.F` | `9371421ff8ace52ba452288647328d34b73cdc30fe421b052474c62734b5963b` | `550678a73f1483cedc587a386948e4eb8fc730ce` (yes) | 875–881 |
| `SR-cp2k-2026.2-release-tarball` | `src/subsys/cp_subsys_types.F` | `d55b2d754d7d1e50fab43a62b0a38d665287eaa0048df4e750eabeed11cbda66` | `822ee61e563cc3ba8526b9878ad3ad583dfe1ee5` (yes) | 518–521 |
| `SR-cp2k-2026.2-release-tarball` | `src/xtb_parameters.F` | `2c270f3fa0157a0dc9ee1a24857847028fd55ad6ce4f7d9855762f78e20b7b4c` | `0c79a46c1979a70ecd92bdc70e27267b7e5a860e` (yes) | 41–150, 185–188, 208–339, 543–597, 763–779 |
| `SR-cp2k-2026.2-release-tarball` | `src/xtb_types.F` | `aa1649a284eb7cca461a31f6fec82a150578f22b9ac96d61cbed6ffb08d29908` | `51240aabdffb7c8d78856378cb38f1ac976452d7` (yes) | 380–391 |
| `SR-cp2k-2026.2-release-tarball` | `tools/toolchain/scripts/stage8/dftd4-4.2.0-gradient-fixes.patch` | `5335cb7d02a8c3141f28967ef61418f425fb1e638d51fe75618b700321d9087a` | `e467cf852e1d1d824bd770f5226d45ab3d38e2a2` (yes) | 18–19 |
| `SR-cp2k-2026.2-release-tarball` | `tools/toolchain/scripts/stage8/install_dftd4.sh` | `d58c9d5b642fe424798c4b2ac0bbc80d7e6d8b3b179f5111e711e99f741950b6` | `1bed51b389f63136b7fc395632a7c0025f68a8c6` (yes) | 9–10, 33–46, 49–58 |
| `SR-cp2k-2026.2-release-tarball` | `tools/toolchain/scripts/stage8/install_tblite.sh` | `b36e31c9c83d679ee45e7b09573575c739291f4ba3e2ecaf579ea939d0396a03` | `9c9654af8fe8e0d785aa9f08109cc223105ca2c6` (yes) | 9–12, 35–43 |
| `SR-psi4-archive-f16f4ea2` | `codedeps.yaml` | `cd36a28c068bc6ec7d4438bf7b7a844e7969bda37a5e22986b24d83ed58da138` | `d1a5689d78354d4737228e7cf4dbad44ee566d3b` (yes) | 435–450, 466–472 |
| `SR-psi4-archive-f16f4ea2` | `psi4/CMakeLists.txt` | `f0736feb8ee74b59b59184ee271f1a8ed56f51db89fcfc832fc0cea05d0e5532` | `1014a6c72e6a13d1b959fb7a221922277f9bc4d7` (yes) | 189 |
| `SR-psi4-archive-f16f4ea2` | `psi4/driver/p4util/python_helpers.py` | `0c39ba0ef11a32fb1a4e921dae64213e5af38ab69d9007170ace44113c49574f` | `1b1c26dd5338e93b522cb441d4def832c5f1f8c5` (yes) | 196, 493–503 |
| `SR-psi4-archive-f16f4ea2` | `psi4/driver/procrouting/dft/dft_builder.py` | `b29d52e450f632793103b01249e27e2c6d61a48859b3c65d17f8cf4de45dad5a` | `d51f6a0eaa56c4ee495c465fcf06f2167157e81d` (yes) | 190–194, 370–383 |
| `SR-psi4-archive-f16f4ea2` | `psi4/driver/procrouting/dft/superfunctionals.py` | `ffa78376bf0b782629923bdde0edb22edf1645a8d6f45a05f123e62eb014d3ce` | `1552090d88d9ebbda92c35b949b247c3dbfb3c3c` (yes) | 66–67, 101–102 |
| `SR-psi4-archive-f16f4ea2` | `psi4/driver/procrouting/proc.py` | `98ac648d84cc4587ec034b9207d3c6fbc3cd74df4c0409a85478e5467c0dd408` | `ab8dfcc8e9c9cfb06eefdc0f7e2a93606eea5e2a` (yes) | 1468, 1479–1484, 2765–2776, 2845–2869 |
| `SR-psi4-archive-f16f4ea2` | `psi4/driver/procrouting/scf_proc/scf_iterator.py` | `4de3bf96fb09d46d2ad7cace03dbad667068e00526edf4adf4ea00df60d7aa8a` | `18767366ebffb71682c843e6033853c4db72fbad` (yes) | 62–80, 103–108 |
| `SR-psi4-archive-f16f4ea2` | `psi4/driver/qcdb/libmintsgshell.py` | `62a805ff605a0787e2dbeff609cbc902fd1db364ac2edf9960395ea60aa6b94c` | `a2974b96818aff5b2db001816d3d087dabd91681` (yes) | 338–346 |
| `SR-psi4-archive-f16f4ea2` | `psi4/share/psi4/basis/def2-tzvp.gbs` | `c7b1fcc367e0cc31a3960a94972ec3b0b2b03f9df7e0627d9c414b9d8d0d1c6a` | `f0ce7145949bede65fb11cae1ddca8a024b26c52` (yes) | 1–5 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/export_functional.cc` | `30c56019a5fae797e8ef9ac30d455fd0f47ef135d20ab66d7efea29818aad038` | `11b904883bbc57ed723d2ad1385757f83c7713a0` (yes) | 178 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/export_mints.cc` | `6eda40690664674ab2e5154036512991c6fefb434c3eedecc6d5b6336116ce2f` | `867ddc560b9c46eca3207b3cda1f05f2fb41b968` (yes) | 118–133 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/psi4/libfock/DirectJK.cc` | `6b2ba577f8e16af315ef7d280cab8ca7d13429f77ff7abf4dc28abd1eaa111dd` | `2fddfd2dad57695bc783fbc76a346af90d2afd31` (yes) | 79 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/psi4/libfock/jk.cc` | `d4c03044aa2b07d2c2706c5aa629b36e015092560795c4cbdad255a3f962cb5b` | `da00c70c8b6fbac2da1a8eebd549fdedab8c314d` (yes) | 172–183, 206–222 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/psi4/libfock/points.cc` | `4c91795cf9070f5387e49c364a0ac6b325995691cdd56c90b381aab51dfd7082` | `1a85be9fda5df5edb0e74bf25f751e2b7bc81d5b` (yes) | 748–754 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/psi4/libfunctional/superfunctional.cc` | `da480f37fe17ff90963e80346c2c29c00281e170d9e1397a1d8892bae615e675` | `32cf5b3738bea31259b3a91d798209443dae3c13` (yes) | 62, 115, 151, 390–392 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/psi4/libfunctional/superfunctional.h` | `a6c1b6217b47c9c5bb0aff86842f0f39a02f40840fec527262b894db7a4e2cda` | `9cc46b7ce3e03639808af6bac78b4e0dcc6b6702` (yes) | 275 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/psi4/libmints/basisset.cc` | `310369f3c0cc1d9eba4d91c8313661873bbe23a756d3e7443969c70537f73794` | `122386b296e7313b040ecb3aced4e0dc37753933` (yes) | 649–651, 801–803, 823–824, 867–884, 1265–1285 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/psi4/libmints/basisset.h` | `de95f710b84cb420d7cf6ec7001b87f35083e35088fd0519c24af78301cee73d` | `ff7fd12e60f5267c1b19210e616ebe918f6bd6cd` (yes) | 171 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/psi4/libmints/eribase.cc` | `637a06c735e5ebbd75057dfef6f569ad425e8df35d5fdda5357ef3efff305cd2` | `64d4929f2c5d12f514230a5fb7a5423d1c881972` (yes) | 225–230 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/psi4/libmints/gshell.cc` | `dd6f25ccb7a257cc42cdad08eab61cab24bafc5b9ea839a1232d3bef27b4f1d6` | `1f80f6026679eafc01bb15b6138962725d191f90` (yes) | 60–76, 78–84, 110–130, 132–140 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/psi4/libmints/gshell.h` | `6e4fae9f3073450a669d54a58e68e02947262060e7996091951a2adc40f50f8b` | `99a3713035a3c84386c5ee4eeffe6772894b6d43` (yes) | 287 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/psi4/libmints/onebody.cc` | `a18ed1adf9ba523ca2001fd4991c254b4af8f7fefd7579c5cedc7fdafa378520` | `1abc05d89273b1d3a96ed61356ccc3dc0167e6ae` (yes) | 351–352 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/psi4/libscf_solver/hf.cc` | `af4539ee67a017dca770e98fa305de911c33f473c7a2ac64b651b179f24994bd` | `9918601d565071d011197292c4673a993208ed9a` (yes) | 961 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/psi4/libscf_solver/sad.cc` | `0c1738ee621a8a020240e3a2281b979947d41055d2f5273e24237247912138f1` | `42f335a6dfdd0c4b57f7885b42830b7ec23e3cc5` (yes) | 234–244, 505–516, 705–719, 969–983 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/psi4/scfgrad/jk_grad.cc` | `d62f45ff9db2e44db5c97c7121cb1e62ae156b4bb81ef6ca7c335b33ed3a808d` | `0947f972e317807506d83f706eabb0fc3b717007` (yes) | 83–84, 99–101, 2318–2321 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/psi4/scfgrad/scf_grad.cc` | `335fc9089c1915a89ba37126883f36e7bc9ef7214d75aa3ce5bb753d0be2f6b4` | `88d3907a2059a5ab77a4c7b60ae1469e1d917495` (yes) | 226 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/psi4/scfgrad/wrapper.cc` | `03ce282da9d75b6200be8218551bbfccfaea8cfdd936e46e9aa7a648f6b55b0f` | `01a0b90c98182e91547aba57a80de94b814f139e` (yes) | 41–50 |
| `SR-psi4-archive-f16f4ea2` | `psi4/src/read_options.cc` | `f5e168622419211fb95eb2e9d31d5b0367ea76e84573bc6efb5e3c0511955ae3` | `d1b5aa9d87f16636b5787fb569c5a8f4b8c9dcf3` (yes) | 167–170, 1836–1843, 1854 |
| `SR-libint-4482d01a-shell-h` | `include/libint2/shell.h` | `c798162776893960c44fc119a69c00f201c28e164da0885522a5889f7c0e4f00` | `948b717ce9017a598c4c11ad7131c5dce5ee19fa` (a single file fetched by commit; no tree compared) | 169–181, 294–303, 359–401 |

### Stage 0 retrievals reused

These 2026-09-26 retrievals were reused and were not retrieved again.
- **Timestamps.** The original access time is the one recorded in Stage 0. The re-verification time is when this
  task recomputed each digest against its row above.
- **Identity.** Identity with the release revision or the v1.11 tag commit is by Git blob SHA1. It establishes that
  the cached bytes equal those revision bytes, and nothing about a mutable branch at any other time.

| ID | Original access (UTC) | Re-verified (UTC) | SHA256 against the row above | Identity with the tag revision |
|---|---|---|---|---|
| `S0-cp2k-emsl-basis` | 2026-09-26T19:54:19Z | 2026-09-27T15:21:36Z | Matches | Equal to `data/EMSL_BASIS_SETS` of `67b5da87…` |
| `S0-cp2k-all-basis` | 2026-09-26T19:54:19Z | 2026-09-27T15:21:36Z | Matches | Equal to `data/ALL_BASIS_SETS` of `67b5da87…` |
| `S0-cp2k-ecp` | 2026-09-26T19:54:20Z | 2026-09-27T15:21:36Z | Matches | Equal to `data/ECP_POTENTIALS` of `67b5da87…` |
| `S0-cp2k-src-disp-pairpot` | 2026-09-26T19:59:14Z | 2026-09-27T15:21:36Z | Matches | Equal to `src/qs_dispersion_pairpot.F` of `67b5da87…` |
| `S0-cp2k-src-disp-utils` | 2026-09-26T19:59:14Z | 2026-09-27T15:21:36Z | Matches | Equal to `src/qs_dispersion_utils.F` of `67b5da87…` |
| `S0-cp2k-src-disp-d3` | 2026-09-26T19:59:53Z | 2026-09-27T15:21:36Z | Matches | Equal to `src/qs_dispersion_d3.F` of `67b5da87…` |
| `S0-cp2k-data-listing` | 2026-09-26T19:54:08Z | 2026-09-27T15:21:36Z | Matches | All 68 entries name the Git object of the same path in `67b5da87…` |
| `S0-psi4-hyb-funcs` | 2026-09-26T19:48:30Z | 2026-09-27T15:21:36Z | Matches | Equal to the blob of `f16f4ea2…` |
| `S0-psi4-read-options` | 2026-09-26T19:48:30Z | 2026-09-27T15:21:36Z | Matches | Equal to the blob of `f16f4ea2…` |
| `S0-psi4-def2-tzvp` | 2026-09-26T19:48:31Z | 2026-09-27T15:21:36Z | Matches | Equal to the blob of `f16f4ea2…` |
| `S0-psi4-empirical-disp` | 2026-09-26T19:48:31Z | 2026-09-27T15:21:36Z | Matches | Equal to the blob of `f16f4ea2…` |
| `S0-psi4-dft-builder` | 2026-09-26T20:54:12Z | 2026-09-27T15:21:36Z | Matches | Equal to the blob of `f16f4ea2…` |
| `S0-psi4-driver` | 2026-09-26T20:54:12Z | 2026-09-27T15:21:36Z | Matches | Equal to the blob of `f16f4ea2…` |
| `S0-psi4-proc` | 2026-09-26T20:56:42Z | 2026-09-27T15:21:36Z | Matches | Equal to the blob of `f16f4ea2…` |
| `S0-psi4-driver-util` | 2026-09-26T20:57:13Z | 2026-09-27T15:21:36Z | Matches | Equal to the blob of `f16f4ea2…` |

### Private records of this section

They are identified by SHA256 only.
- **Retrieval manifest** of the 16 retrievals: `ee2555e0cada3ef4a70418997d9b6c400ac9011124d9db823b5a51cacda7d9f0`.
- **Final locator check**, 211 assertions over 72 files, all passing:
  `6bb90c6e4924f917e24ea0ccccc9db7deb5fe0ccf9c7c1d0bafe37f2e104488f`.
- **First locator check**, with 12 wrong ranges, retained: `f34788d6c7eaddbe988ddb9ba84fec6fc387f978710659de3a78a369341991e7`.
- **Re-verification of the reused Stage 0 retrievals:**
  `e897e9131c9404da3be5615eb5484162301083ecb0c68eb270ffd66be55d5712`.
