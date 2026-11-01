# Classification and scan outputs

EC denotes Einstein–Cartan, LC denotes Levi-Civita, and NY denotes Nieh–Yan.


[日本語](CLASSIFICATION_ja.md) / [Usage](../README.md)

`dppu.scanning.classify_configuration` is shared by the scan and viewer. It takes topology, signed code V and eta, alpha, epsilon, mode, NY action, theta, L and kappa. Inputs satisfy epsilon > -1 and L,kappa > 0. The CLI/viewer fix L=kappa=1. AX sets effective V=0; VT sets effective eta=0. Input signs are opposite to the manuscript's geometric torsion signs.

## Two domains

- `global_*`: the complete-NY classification of Sections 7–8 for the two Weyl actions (Section 4.4 for the Ricci-tracefree EC curvature action) on all r>0 and x>0, at fixed torsion parameters, L and kappa. Epsilon specifies no restriction on this domain. For nonpositive alpha the spherical finite minimum is round; Nil has an unattained zero infimum even when a radial slice has a minimum.
- `radial_*`: all r>0 at the specified epsilon, with x=(1+epsilon)**(-2/3). The classifier solves the quadratic stationary equation in r squared from Appendix B and checks the endpoint limits. Plot bounds and a finite sampling grid do not determine these labels.

| Label | Meaning in the stated domain |
|---|---|
| `FINITE_MINIMUM` | A unique finite minimum exists |
| `UNATTAINED_INFIMUM` | The finite infimum is approached at a boundary and not attained |
| `DEGENERATE_MINIMUM` | A nonisolated set attains the minimum |
| `UNBOUNDED_BELOW` | The potential is unbounded below |
| `NOT_APPLICABLE` | TT/REE is a different action; this paper classification is not applied |
| `NUMERIC_UNRESOLVED` | A fixed-shape boundary cannot be resolved at the working precision |

For the two Weyl actions, the classification over radius and shape for S3 at alpha<=0 distinguishes V nonzero with eta squared below four, the unattained-zero cases, the V=0 runaway below the threshold, and the degenerate round ray at V=0 and eta squared equal to four. Positive alpha is unbounded in the joint spherical domain even when its round radial slice has a minimum. T3 is flat when both amplitudes vanish, otherwise its zero infimum is unattained. Nil has an unattained zero infimum for nonpositive alpha and is unbounded below for positive alpha.

## CSV and numerical boundaries

Each row retains `V_input`, `eta_input`, effective `V`, `eta`, topology, mode, action, alpha, epsilon, theta, L and kappa. `global_class` and `radial_class` replace the former `stability_type` field. `global_infimum`/`radial_infimum` contain the infimum, including `-inf`; empty values are unavailable or outside scope. `global_r`, `global_x` and `radial_r` give available minimizing coordinates; the Ricci-tracefree EC curvature action on T3 also records the common radius of its degenerate joint set. `*_limit` describes a limiting path or a degenerate set. `radial_local_min_r` may be present even when the global radial infimum is minus infinity; it does not imply a global minimum.

The former `r0` and `delta_V` columns are not used. Readers should not reinterpret old CSV labels as the new categories. FULL is the default; theta has no effect and only one theta value is sampled by default. Explicit TT/REE rows report NOT_APPLICABLE; their potentials remain available in the engines and viewer.

Inputs are finite binary floats and are not rounded to two decimals. The V=0, abs(eta)=2 and alpha=0 tests use the actual stored values, without a tolerance band that converts nearby inputs to the boundary. For example, V=4 and eta=1.999 has a finite round minimum, whereas eta=2 has an unattained zero infimum. The smallest nonzero representable inputs are not treated as zero.

Fixed-shape coefficients and roots use 80-digit Decimal arithmetic with cancellation-resistant expressions. `numeric_status` flags coefficient/merging-root uncertainty or values outside the float range. In the latter case the affected value is empty; an independently established categorical result is retained. This is a numerical implementation of the stated formulas, not an interval-certified solver for arbitrary inputs.

## Viewer

The map selector chooses joint or fixed-shape radial classification. The curves always use the current engine at the specified epsilon. The selected-point table shows both domains, infima and radii; a minimizer outside the plot window is explicitly identified. TT/REE permit curve exploration but have no theorem map. FULL disables the inactive theta control.

Numeric point fields accept values such as 1.999. Apply controls to redraw both panels together; changed controls mark existing plots as pending. Grid cells visualize sampled classifications; dashed spherical threshold lines and marked degenerate samples do not give a nonzero width to exact boundaries. Code amplitudes and variation domains are shown explicitly. The viewer does not classify full-field vacua, Lorentzian ghosts, or universal topology selection.

Curves outside the vertical window are identified in the plot. `Fit U to curves` fits the sampled curves within the current radius window without changing classification. Use it with `U scale: Symlog` for wide ranges such as the Nil examples. The point table also identifies minima outside either the radius or vertical window.

## Curvature-squared actions

`curvature_model` selects irreducible EC-Weyl (`EC_IRR`, default), LC-Weyl (`LC`), or Ricci-tracefree EC curvature (`EC_TRACEFREE`). The two Weyl actions share the classifications above. For the Ricci-tracefree EC curvature action, replace $9\eta^2$ in the radial coefficient by $\gamma=\eta^2(9-16\kappa^2\alpha V^2)$; Appendix B's stationary equation is otherwise unchanged.

On S3 at alpha<=0, gamma<36 and V!=0 give the unique round minimum; V=0,gamma<36 is unbounded, V=0,gamma=36 is a degenerate round ray, and all other cases have unattained infimum zero. Positive alpha is unbounded over radius and shape. Nil has the same classification over radius and shape as the Weyl actions. T3 with gamma<0 has a finite radial minimum and a `DEGENERATE_MINIMUM` set at fixed radius for all shapes; `global_r` is set, `global_x` is empty, and `global_limit` is `fixed_r_all_shape`. At gamma>=0 its zero infimum is unattained unless both amplitudes vanish, when all radii and shapes minimize.

The signs of gamma and 36-gamma for the Ricci-tracefree EC curvature action use exact rational arithmetic on the input floats before conversion to 80-digit Decimal for values. No rounded products are used to classify the threshold. The two Weyl actions use the boundary rules above. The map identifies the selected action; fixed eta=±2 dashed lines apply to the two Weyl actions, not to the shifted Ricci-tracefree EC curvature boundary. See [model definitions](WEYL_MODELS.md).
