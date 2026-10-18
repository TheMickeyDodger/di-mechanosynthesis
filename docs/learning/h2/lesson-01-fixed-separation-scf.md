# Lesson 01 — Fixed separation, and what a self-consistent field calculation varies

**Status.** This is an [AGENT] learning document: no calculation was run in writing or checking it, it contains no computed energies, it supports no claim about the mastery of any learner, and it authorizes nothing.

**How to read the labels.** The class of the underlying evidence is assigned first, and a citation alone does not determine it. A statement that takes a source's theory content, with its locator, is [LIT]: conceptual textbook or manual theory, not a measurement and not a calculation by this project. The lesson's own explanations, definitions, prompts and reasoning are [AGENT]. Operational records such as run statuses carry no chemistry class.

## First, a question

Two protons are held a fixed distance R apart with two electrons in their combined field. When a program minimizes the energy, what may it change?

Before reading on: write a short answer and sketch by hand a guess for the energy as a function of R.

## The system

Neutral hydrogen, H2: two protons, two electrons, total spin singlet. The nuclei sit at (0, 0, −R/2) and (0, 0, +R/2), so the bond is centered on the origin and R is the separation. Distances are in bohr, energies in hartree; for scale, one bohr is the Bohr radius, about 5.29 × 10⁻¹¹ m [51].

## How the Hamiltonian splits

The total Hamiltonian separates into three pieces [45, pp. 2–3]: T_N, the kinetic energy of the nuclei; V_NN, the repulsion between the nuclei; and the electronic Hamiltonian, built from the electron kinetic energy, the electron–nucleus attraction, and the electron–electron repulsion. The manual writes the electronic Hamiltonian with the same three electronic terms [48, Theory].

Convention declared in this lesson: E_elec is the electronic energy of the problem with the nuclei fixed; it includes the electron kinetic energy and excludes the nuclear repulsion V_NN.

## Why the nuclei are held fixed

Holding the nuclei at fixed positions is a computational choice, not a claim that the nuclei are classical [45, p. 3]. At fixed R, the electronic problem depends on R only as a parameter [45, pp. 4–5]; [AGENT] "fixed R" means R is an input to this computation, not a variable of it.

**Learner prompt 1.** Holding R fixed is a choice, not a law. If a program is instead allowed to change R, what else must change with it?

## Three energies, one curve

Integrating the electrons out yields an effective nuclear Hamiltonian; its lowest-order form is the nuclear kinetic energy, V_NN, and E_elec(R) [46, pp. 2-4; 46, p. 4]. Dropping the Berry and derivative coupling terms is an approximation to that Hamiltonian and to the nuclear dynamics [46, pp. 3-4], not to the definition of E_BO.

Three quantities appear under the declared convention. E_elec(R) is the fixed-R electronic energy: it includes electron kinetic energy and excludes V_NN. V_NN(R) = 1/R hartree, with R in bohr. E_BO(R) = E_elec(R) + V_NN(R) is the clamped-nuclei potential for nuclear motion; it excludes nuclear kinetic and zero-point energy regardless of the coupling terms. The Hartree-Fock and finite-basis approximations to E_elec are a separate matter, in a later section [AGENT].

Labelling warning: [47, p. 1] writes E_el for the fixed-R electronic energy without stating whether it includes V_NN. [AGENT] When you meet a number, first ask which of these quantities it is; never add V_NN twice.

## What SCF varies — and what it cannot

At fixed R, SCF varies the MO coefficients over the fixed basis functions: constrained variational parameters [48, Theory]. Orthonormality enters through the overlap matrix (generalized eigenproblem) [48, Theory]. RHF keeps alpha and beta spatial orbitals identical [48, Spin/Symmetry Treatment]. The Fock matrix depends on the electron density, so the calculation is iterated until self-consistency [48, Theory].

**What is NOT varied at fixed R [AGENT]:** R and the nuclear positions, the nuclear charges, the number of electrons, the overall charge, the spin state, the definitions of the basis functions.

With STO-3G each hydrogen contributes one contracted s function of three Gaussian primitives [50], giving two basis functions; the singlet's two electrons occupy one spatial orbital, doubly. [50] names [49] as the source of the parameters; [49] is not inspected.

**Learner prompt 2.** Two basis functions span a two-dimensional space, and every normalized combination of them is an admissible occupied orbital. What might the symmetry of two identical nuclei suggest about the converged orbital, and what assumption would that suggestion need? This lesson deliberately does not answer.

## Convergence is not a minimum

A convergence report means the reported criteria fell below their thresholds within an iteration limit [48, Initial Guess]; the source's prose and its example iteration output differ on the second quantity [48, Initial Guess], so the exact test is version-specific and must be checked for the build used [AGENT]. A stationary point may be a saddle or maximum, and a stability analysis checks for a lower solution under the same constraints (internal) or after relaxing one, for RHF only toward UHF (external) [48, Stability Analysis]. [AGENT] None of this proves a global minimum.

**Learner prompt 3.** A converged SCF may be a saddle point. What does "converged" in a log file actually tell you, and what would a separate check need to show?

## What RHF and a finite basis leave out

RHF is a single Slater determinant. [47, p. 7] gives E_corr = E_exact - E_HF without saying which basis E_HF is computed in. [AGENT] The lesson's convention is that E_HF there means the Hartree-Fock energy in the complete-basis-set limit [47, p. 4], so the formula isolates the single-determinant approximation. [AGENT] The difference between the exact energy and a finite-basis, for example STO-3G, RHF energy mixes the single-determinant approximation and the finite-basis restriction, so it is not purely correlation; neither part is estimated.

STO-3G gives one contracted s function per H [50]; the complete-basis-set limit is defined as the hypothetical result with an infinite number of atomic orbitals [47, p. 4]. [AGENT] A finite basis restricts which orbitals the calculation can represent; no error size is claimed. Method and basis are separate choices [47, pp. 2, 9].

One bound [46, p. 1]: the energy expectation in ANY normalized admissible trial state of the same clamped-nuclei electronic Hamiltonian is at least its exact ground-state energy; convergence is NOT a condition. It bounds E_elec and E_BO (V_NN is the same added constant), while a reported number carries approximations and thresholds, so applying the bound to it needs separate care [AGENT].

## Single point, scan, and optimization

[AGENT] Definitions for this lesson:

- A **single point** is one SCF calculation at one fixed R: one input, one answer.
- A **scan** is a set of separate fixed-R calculations, with a person or a driver choosing a new R between them; each point is an independent single point.
- A **geometry optimization** is an algorithm that moves the nuclei.

The lowest point of a discrete scan is a grid minimum — the best of the points that happened to be computed. It is not an optimized equilibrium, and it is not a global minimum over R.

**Learner prompt 4.** If the middle point of a ten-point scan of E_BO comes out lowest, what can you honestly claim about the true minimum?

## Spin, multiplicity, and reference

The two electrons of the singlet are paired: total spin S = 0, and the multiplicity 2S + 1 is 1. RHF is one modeling choice for a closed-shell singlet, with identical alpha and beta densities [48, Spin/Symmetry Treatment]. UHF lets the two densities differ, and it need not be an S² eigenfunction [48, Spin/Symmetry Treatment]. A triplet is a different spin state, and hence a different problem.

## Self-check

Without looking back, try to explain each of these in your own words:

- What the program may change at fixed R, and what it may not.
- The difference between E_elec(R), V_NN(R), and E_BO(R), and why the label matters.
- Why "converged" does not mean "the best possible answer."
- What RHF leaves out, in two separate ways.
- The difference between a grid minimum from a scan and an optimized equilibrium.
- Why holding the nuclei fixed is a computational choice, not a claim that nuclei are classical.

This self-check does not establish mastery. Mastery requires your own explanations of these points, reviewed by a person. No model answers are given here, and none should be fabricated.

## What comes next

The next document in this folder, [h2-method-specification.md](h2-method-specification.md), is a prospective specification only. Any actual run needs separate review and a separate, bounded authorization by a person.

## References

This lesson draws only on the sources below, cited with the locators actually used; the full catalogue entries are in [../../SOURCES.md](../../SOURCES.md).

- **[45]** MIT OpenCourseWare 8.06 (Spring 2018), "L18.1 Born–Oppenheimer approximation": pp. 2–3, p. 3, pp. 4–5.
- **[46]** MIT OpenCourseWare 8.06 (Spring 2018), "L18.2 Effective nuclear Hamiltonian": p. 1, pp. 2–4, pp. 3–4.
- **[47]** MIT OpenCourseWare 5.61 (Fall 2017), "Lecture 28 and 29 Notes": p. 1, pp. 2, 9, p. 4, p. 7.
- **[48]** Psi4 manual, development version, "HF: Hartree–Fock Theory": Theory, Spin/Symmetry Treatment, Initial Guess, Stability Analysis. A development manual, not any installed build.
- **[49]** Hehre, Stewart, Pople, J. Chem. Phys. 51, 2657–2664 (1969): named by [50]; not inspected in this lesson.
- **[50]** Basis Set Exchange, STO-3G, element H, version 1. Says nothing about any installed basis file.
- **[51]** NIST CODATA 2022, Bohr radius. Used only for unit display.
