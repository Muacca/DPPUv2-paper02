# Action and potential

[日本語](README_ja.md)

`compute_lagrangian` combines EC scalar, NY and the selected curvature quadratic term; `compute_action` multiplies by the stated volume and `compute_effective_potential` gives U=-S. Use `dppu.scanning.classify_configuration` for radius/shape classification.

[Conventions](../../docs/CONVENTIONS.md) / [Usage](../../README.md) / [Classification](../../docs/CLASSIFICATION.md)

[Curvature models and output keys](../../docs/WEYL_MODELS.md). The selected action uses quadratic_scalar. The default is EC_IRR; the legacy weyl_scalar key remains the LC reference.
