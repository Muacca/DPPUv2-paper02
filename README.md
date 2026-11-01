# Curvature Identities and Restricted Potential Bounds in Einstein–Cartan–Nieh–Yan Minisuperspace with Irreducible EC-Weyl Corrections

EC denotes Einstein–Cartan, LC denotes Levi-Civita, and NY denotes Nieh–Yan.


[日本語](README_ja.md)

Manuscripts, code, and figure data for a study of how irreducible EC-Weyl and LC-Weyl terms affect radius and shape dependence in static homogeneous spherical, toroidal, and Nil reductions. An exact spherical shape factorization leads to a classification of minima and their attainment at fixed torsion parameters and circle circumference.

**v2 — revised 2026-11-01.** Changes to the action, conventions, and conclusions are documented in the [CHANGELOG](CHANGELOG.md); the preceding reference expression is discussed in Appendix D of the paper.

Zenodo records: v1 (2026-02-28) is [10.5281/zenodo.18815499](https://doi.org/10.5281/zenodo.18815499); the all-versions DOI [10.5281/zenodo.18815498](https://doi.org/10.5281/zenodo.18815498) resolves to the latest deposited version. Identify the manuscript version and date when citing results.

| Resource | Contents |
|---|---|
| [English PDF](DPPUv2-paper02.pdf) | v2 text, proofs, figures, and appendices |
| [LaTeX](LaTeX/main.tex) | English sources |
| [Code](script/README.md) | Calculation, figure reproduction, and viewer |
| [Conventions](script/docs/CONVENTIONS.md) | Local/global conventions and fixed data |
| [Data](data/revised/README.md) | Revised figures 1–4 and table data |

- [Section 1 (Japanese)](DPPUv2-paper02_sec01.md)
- [Section 2 (Japanese)](DPPUv2-paper02_sec02.md)
- [Section 3 (Japanese)](DPPUv2-paper02_sec03.md)
- [Section 4 (Japanese)](DPPUv2-paper02_sec04.md)
- [Section 5 (Japanese)](DPPUv2-paper02_sec05.md)
- [Section 6 (Japanese)](DPPUv2-paper02_sec06.md)
- [Section 7 (Japanese)](DPPUv2-paper02_sec07.md)
- [Section 8 (Japanese)](DPPUv2-paper02_sec08.md)
- [Section 9 (Japanese)](DPPUv2-paper02_sec09.md)
- [Section 10 (Japanese)](DPPUv2-paper02_sec10.md)

[Appendix A](DPPUv2-paper02_appA.md) / [Appendix B](DPPUv2-paper02_appB.md) / [Appendix C](DPPUv2-paper02_appC.md) / [Appendix D](DPPUv2-paper02_appD.md)

## Action and classification

The main action contains the squared norm of irreducible EC-Weyl curvature. Its tensor equals LC-Weyl on the prescribed static family, so the reduced potentials and radius/shape classifications coincide. Section 4 compares the action built from Ricci-tracefree EC curvature. [Definitions and code selection](script/docs/WEYL_MODELS.md).

The scan and viewer share [joint and fixed-shape classifications](script/docs/CLASSIFICATION.md), including unattained and degenerate minima.

## Reproduce the figures

Run from the repository root. Render uses supplied data; recompute explicitly recalculates them with the current engine. Specify a new output directory.

```powershell
python -m pip install -r script/requirements.txt
python -B script/scripts/paper02/reproduce_figures.py render --output-dir rendered_figures
python -B script/scripts/paper02/reproduce_figures.py recompute --output-dir recomputed_figures
```

The repository contains the current paper, datasets, engine, runners, symbolic supplements, and viewer. Earlier outputs and exploratory code remain in Git history and are excluded from the attached supplement. Code torsion amplitudes have the opposite signs to geometric torsion; restart notebook kernels after changing code versions.

## Build the PDF

```powershell
Push-Location LaTeX
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
Pop-Location
```

The output is LaTeX/main.pdf; these commands do not replace the root PDF.

## Author and license

Muacca. [LICENSE](LICENSE.txt).
