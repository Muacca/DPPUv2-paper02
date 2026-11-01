# Frame metric utilities

[日本語](README_ja.md)

`create_frame_metric`, `verify_metric_compatibility`, `raise_index`, and `lower_index` operate on frame tensors. The paper uses the Euclidean identity metric. The metric helper can construct a Lorentzian diagonal matrix, but the paper engine and its curvature norms have not thereby been validated for Lorentzian signature.

[Conventions](../../docs/CONVENTIONS.md) / [Usage](../../README.md)
