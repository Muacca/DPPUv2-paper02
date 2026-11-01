# Revision history

## v2 — 2026-11-01

This revision corrects the Nieh–Yan (NY) density and global volume normalization, and develops the radius-and-shape classification of the reduced potential with an irreducible EC-Weyl term and an explicit LC reference. The date is the manuscript revision date.

### Action and torsion conventions

- Corrected the curvature-side NY density from $`\frac14\varepsilon^{abcd}R_{abcd}`$ to $`\frac12\varepsilon^{abcd}R_{abcd}`$. The torsion-side coefficient remains $1/4$. On the stated static homogeneous family, the two contributions coincide, so complete NY vanishes and the FULL potential is independent of $\theta$.
- Adopted geometric torsion $T$ in the manuscript and specified the code-input dictionary $\tau=-T$, $`V_{\tau}=-V`$, $`\eta_{\tau}=-\eta`$, including signed input domains. The connection formulas and input API retain the code convention.
- Distinguished complete NY from the TT and positive-REE diagnostic actions. Their equal densities on this family do not imply that their potential dependence belongs to the complete action.
- Distinguished form-index Hodge duality from internal-index duality. Defined the all-component curvature norm separately from the Euler density, and the all-component Pontryagin contraction as twice the four-form coefficient. Corrected the torsion-free checker index order and distinguished the Weyl Taylor coefficient from the shape Hessian.

### Global geometry and normalization

The circle coordinate has period 1, and $L$ denotes its physical circumference. The three spatial coframe factors have product one, so varying shape preserves volume at fixed radius scale $r$.

| Background | Adopted geometry | Four-volume |
|---|---|---|
| $S^3\times S^1$ | SU(2), with round physical radius $r/2$ | $\pi^2 Lr^3/4$ |
| $T^3\times S^1$ | Spatial angles of period $2\pi$; common scale and volume-preserving shape | $(2\pi)^3 Lr^3$ |
| $\mathrm{Nil}^3\times S^1$ | Heisenberg lattice $(2\pi,2\pi,4\pi^2)$ with twisted face identifications | $(2\pi)^4 Lr^3$ |

At the same inputs, the volume correction multiplies spherical action values by $1/8$ and toroidal values by $1/(2\pi)$. The Nil volume is retained with its compact quotient specified. These positive volume factors do not move extrema within a fixed geometry; the NY coefficient correction changes the potential itself. All three engine callables use the common radius argument, including Nil.

### Curvature models

- Defined the irreducible EC-Weyl projection and proved its tensor equality to LC-Weyl throughout the prescribed static homogeneous shape families. The LC potential classification, datasets and figures therefore also apply to the irreducible EC-Weyl action. This equality is not extended to general fields or dynamical perturbations.
- Distinguished the Ricci-tracefree quadratic action built from Ricci-tracefree EC curvature, which includes two additional curvature sectors with the same coupling. Gave its exact potential shift and a short classification comparison; its contribution is a model difference, separate from the NY coefficient correction.
- Added explicit LC, EC_IRR (default), and EC_TRACEFREE (Ricci-tracefree EC curvature) model selection to the public engine, runners, scan and viewer. Preserved LC compatibility keys and recorded the selected quadratic tensor separately. Figure recomputation explicitly retains LC provenance.

### Conclusions and interpretation

- Retitled the paper; v1 was titled “Structural Robustness of Isotropic $S^3$ Vacua in Einstein–Cartan Minisuperspace via Chiral Equilibrium and Weyl Stability”. Withdrew the claim that the isotropic $S^3$ vacuum of the preceding paper is robust under the Weyl extension, and the claim that $S^3$ is energetically selected among the three topologies.
- Retained the vanishing form-index Pontryagin density as an algebraic property of the prescribed connection. Withdrew its interpretation as a “chiral equilibrium” that closes self-dual instanton decay channels; transition paths are a separate question (Section 9).
- Limited the role of the sign of the Weyl coupling. On the sphere, positive coupling is unbounded below for every fixed parameter choice, whereas at nonpositive coupling the existence and boundedness of minima depend on $V$ and $\eta$ (Theorem 3). This replaces the earlier parameter-independent stability boundary at $\alpha=0$.
- Established the exact spherical shape bound for nonpositive Weyl coupling. Joint minimization over radius and shape reduces to the round slice. At fixed torsion parameters and circle circumference, $V\ne0$ and $\eta^2<4$ give a unique negative finite-radius minimum whose radius and value are independent of the Weyl coupling. Increasing the magnitude of a nonpositive coupling increases the shape entry of the restricted Hessian.
- Classified the remaining spherical cases by attained or unattained infima, degenerate minimum sets, and unboundedness. Retained positive-coupling small-radius unboundedness on nonround spheres and Nil, with the round slice and torus treated separately.
- Distinguished a fixed-shape Nil radial minimum from joint radius-and-shape minimization, where the zero infimum is unattained for nonpositive coupling. Specified the shape-independent toroidal cases and the fixed quotients used in comparisons.
- Removed the complete-action minimum at the reference radius $r=2$. Appendix D separates the NY coefficient correction from the volume normalization and compares the reference expression with the complete-NY potential at the same volume.
- Reframed the results as extrema of a restricted static action. They do not establish full-field Einstein–Cartan vacua, dynamical or quantum stability, Lorentzian ghost avoidance, or a universal topology-selection law. Section 9 states the additional field, constraint, and observable requirements.

### Manuscripts, computation and figures

- Defined scientific action names, curvature invariants, NY component densities, torsion modes, and first-use abbreviations consistently across the text, guides and user interfaces, retaining API selector values and data fields.
- Revised the Japanese Markdown and English LaTeX/PDF consistently around the curvature identities, spherical shape bound, fixed-parameter classification, and geometric comparison. Kept the scientific arguments and interpretation limits within the paper and appendices. Displayed the version, first-release date, and revision date on separate title-page lines.
- Updated the engine and its consumers for the corrected coefficients and volumes. Replaced handwritten round-only scan formulas with engine callables, handled inactive AX/VT inputs, and retained Weyl dependence on undeformed Nil.
- Shared the [joint and fixed-shape classifier](script/docs/CLASSIFICATION.md) between the scan and viewer. Replaced Type I/II/III labels with explicit attainment and boundedness outcomes, removed input rounding and radius-window exclusions, and flagged unresolved or unrepresentable numerical cases. TT/REE remain available for curve exploration outside the complete-NY classification.
- Aligned the [conventions](script/docs/CONVENTIONS.md) and [SymPy guideline](script/docs/SymPy_guideline.md) with the attached implementation, specifying volume-preserving shape, curvature-squared actions, and minimization over radius and shape or at fixed shape.
- Supplied four figures, six figure/table CSV datasets, and their parameters in [data/revised](data/revised/README.md). Separated rendering of supplied data from explicit engine recomputation. Figures 1–3 illustrate the research results; Figure 4 accompanies Appendix D.
- Limited the public library to the engine, three geometry runners, classification scan, two symbolic supplements, viewer, and figure-reproduction paths. Removed the legacy interval classifier, round-only formula registry, optional numerical self-duality/Pontryagin APIs, their re-exports, and the SciPy requirement. Superseded outputs and exploratory workflows are excluded from the supplement; notebooks are distributed without evaluated outputs.
- Preserved the original acknowledgments and DPPU attribution in the English manuscript, with an addition describing revision assistance and deterministic numerical plotting. The Japanese Markdown ends with the conclusions and has no acknowledgments section.
