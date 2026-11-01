# Revised figure and table data

[日本語](README_ja.md)

Datasets for Paper02 v2, computed on 2026-10-30. Inputs use the code tau convention. Defaults are L=kappa=theta_NY=1 and V_tau=4; CSV columns and parameters.json specify shape, alpha, and eta variations.

| CSV | Figure or purpose |
|---|---|
| [shape_penalty.csv](shape_penalty.csv) | Figure 1: fixed-radius spherical shape differences |
| [small_radius.csv](small_radius.csv) | Figure 2: fixed-shape positive-alpha small-radius curves |
| [round_reference.csv](round_reference.csv) | Figure 4 (Appendix D): historical comparison and current representative slices |
| [nil_slices.csv](nil_slices.csv) / [torus.csv](torus.csv) | Figure 3: Nil radial slice minima and torus alpha independence |
| [stationary_points.csv](stationary_points.csv) | Representative inputs in Section 7; absent stationary values are empty |
| [parameters.json](parameters.json) | Fixed data, domains, volumes, and interpretation |

Only the old-NY comparison curve uses the historical expression rescaled to the current spherical volume. Other values use the current FULL engine. stationary_points.csv takes its values and attainment labels from the shared classifier, over radius and shape at alpha=0; by Theorem 3 they hold for every nonpositive alpha. Nil radial minima hold shape fixed and are not joint minima. The small_radius and nil_torus plots divide U by c_M L; CSVs contain unscaled U.

For reproduction see the [script guide](../../script/README.md). Distinguish finite samples from analytic proofs.

These datasets retain their LC calculation provenance. Paper Section 4 proves that they also describe irreducible EC-Weyl on the prescribed static family. They do not represent the Ricci-tracefree EC curvature action.
