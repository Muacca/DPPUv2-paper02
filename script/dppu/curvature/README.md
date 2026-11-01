# Curvature and Weyl projections

[日本語](README_ja.md)

`compute_riemann_tensor` includes the noncoordinate-frame structure term; `verify_antisymmetry_strict` checks both index pairs. Ricci contractions and LC-Weyl have separate functions. Conventions Section 11 defines form-Hodge/Pontryagin normalization; the public symbolic supplement verifies the spatial blocks and zero Pontryagin on all three geometries.

[Conventions](../../docs/CONVENTIONS.md) / [Usage](../../README.md) / [Classification](../../docs/CLASSIFICATION.md)

[Curvature models and output keys](../../docs/WEYL_MODELS.md). The selected action uses quadratic_scalar. The default is EC_IRR; the legacy weyl_scalar key remains the LC reference.
