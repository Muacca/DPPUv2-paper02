# Curvature-squared actions

[日本語](WEYL_MODELS_ja.md) / [Usage](../README.md)

Einstein–Cartan (EC), Levi-Civita (LC), and Nieh–Yan (NY) have the meanings used in paper Sections 2–4. The actions below share the EC Ricci scalar and the chosen NY term. Only the curvature-squared term changes; selecting LC-Weyl does not replace the entire EC connection.

| Scientific name | Public selector | Tensor in the quadratic term |
|---|---|---|
| Irreducible EC-Weyl action (default) | `EC_IRR` | The ten-component Weyl projection of EC curvature |
| LC-Weyl action | `LC` | The Weyl tensor of the LC connection |
| Ricci-tracefree EC curvature action | `EC_TRACEFREE` | The twenty-component kernel of EC Ricci contraction |

For curvature with four lower indices, `rc_weyl.irreducible_weyl_curvature(R, metric)` first symmetrizes the index pairs, removes the four-form, and then removes the Ricci traces of the resulting algebraic Riemann tensor. This defines the irreducible EC-Weyl tensor. `rc_weyl.ricci_tracefree_curvature(R, metric)` removes Ricci traces directly from the original EC curvature. Its coefficients are fixed by zero Ricci contraction, not fitted to the LC result. A general EC curvature need not satisfy pair exchange or the torsion-free algebraic Bianchi identity.

Write these tensors as $`C_{\mathrm{EC}}`$ and $`\widehat R_{\mathrm{EC}}`$. In the Riemann–Cartan (RC) decomposition, $R^{(2)}$ denotes the nine-component pair-antisymmetric Ricci-tracefree part and $R^{(3)}$ the one-component four-form. Then

$$
\begin{aligned}
\widehat R_{\mathrm{EC}}&=C_{\mathrm{EC}}+R^{(2)}+R^{(3)},\\
I_{\mathrm{W}}&=\lVert C_{\mathrm{EC}}\rVert^2,\qquad
I_{\mathrm{tf}}=\lVert\widehat R_{\mathrm{EC}}\rVert^2.
\end{aligned}
$$

The three sectors are orthogonal in the Euclidean metric. The irreducible EC-Weyl action sets the quadratic couplings of the latter two to zero; the Ricci-tracefree EC curvature action assigns the same coupling to all three. The decomposition does not select a physical action. See paper Section 4 for definitions and the proof, and [McNutt et al.](https://doi.org/10.3842/SIGMA.2024.078) for the RC decomposition.

On the prescribed static homogeneous family, at every positive radius and shape,

$$
C_{\mathrm{EC}}=C_{\mathrm{LC}},\qquad
I_{\mathrm{tf}}-I_{\mathrm{W}}=\frac{16V^2\eta^2}{3r^2},\qquad
U_{\mathrm{tf}}-U_{\mathrm{W}}=-\frac{16}{3}\alpha c_{M}L V^2\eta^2r.
$$

Here $`U_{\mathrm{tf}},U_{\mathrm{W}}`$ are the corresponding reduced potentials. This is not an identity for general fields, unrestricted variations, or kinetic terms. The additional contribution is independent of NY coupling and vanishes when V=0 or eta=0; potentials also agree at alpha=0. It is separate from the NY coefficient correction.

## Engine and command-line selection

```python
engine = S3S1Engine(Mode.MX, NyVariant.FULL, curvature_model='EC_IRR')
engine.run()
I = engine.data['quadratic_scalar']
U = engine.data['potential']
```

All three geometry runners and `run_parameter_scan.py` accept `--curvature-model LC`, `EC_IRR`, or `EC_TRACEFREE`. The viewer displays scientific names with the same stored values and includes the action in its engine cache key. The classifier accepts `curvature_model` and records it in each CSV row.

The independent torsion choices are `AX` (axial only, V=0), `VT` (vector trace only, eta=0), and `MX` (both components allowed). All allow zero amplitudes. The NY choices are `FULL` for the torsion-product coefficient minus the curvature–coframe coefficient, `TT` for the positive torsion-product coefficient alone, and `REE` for the positive curvature–coframe coefficient alone, each multiplied by the real coupling theta. Positive describes the relative sign, not a restriction on theta. TT/REE curves are available, while their classifications are `NOT_APPLICABLE`.

| Data key | Meaning |
|---|---|
| `curvature_model` | Selected quadratic action |
| `quadratic_tensor`, `quadratic_scalar` | Selected tensor and its direct all-index squared norm used in the action |
| `weyl_tensor_LC`, `weyl_scalar_LC` | LC reference |
| `weyl_tensor`, `weyl_scalar` | Compatibility names for the LC reference, for every selected action |

The low-level keyword `compute_lagrangian(..., weyl_scalar=...)` is retained for compatibility; the engine supplies `quadratic_scalar`. Restart notebook kernels after source changes. The curvature-tensor selection step (E4.8a) stores the tensor and its model. The action-construction step (E4.11) rejects a different stored model; rerun E4.8a before constructing that action. `engine.run()` never auto-loads a checkpoint.

## Data and reproduction

The six supplied CSVs, parameters and four figures were computed with LC-Weyl. Recomputation explicitly selects `LC`. The tensor identity makes them equally applicable to the irreducible EC-Weyl action on the stated family. They do not represent the Ricci-tracefree EC curvature action; select `EC_TRACEFREE` in a runner or viewer to calculate that action. The paper provides a short analytic comparison in Section 4.4.
