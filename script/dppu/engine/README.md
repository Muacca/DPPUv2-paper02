# Calculation pipeline

[日本語](README_ja.md)

`BaseFrameEngine(mode, ny_variant, logger=None, checkpoint_mgr=None, *, curvature_model='EC_IRR')` evaluates connection, LC/EC curvature, NY, action, and potential. `run()` executes the registered steps; explicit checkpoint loading is separate. `get_effective_potential_function()` returns f(r,V,eta,theta_NY,L,kappa,epsilon,alpha), including inactive AX/VT arguments. The historical data key torsion_tensor contains tau, not geometric T.

[Conventions](../../docs/CONVENTIONS.md) / [Usage](../../README.md)

[Curvature models and output keys](../../docs/WEYL_MODELS.md). The selected action uses quadratic_scalar. The default is EC_IRR; the legacy weyl_scalar key remains the LC reference.
