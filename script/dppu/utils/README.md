# Symbolic and epsilon helpers

[日本語](README_ja.md)

`epsilon_symbol`, `levi_civita_4d`, and `levi_civita_nd` implement antisymmetric symbols. `prove_zero` attempts exact symbolic simplification and returns a Boolean and method string; its timeout_seconds argument is currently unused. `find_nonzero_witness` and `generate_test_points` provide finite numerical probes; absence of a witness is not an identity proof. In examples using the engine amplitudes, the axial input array is tau; geometric torsion is -tau.

[Conventions](../../docs/CONVENTIONS.md) / [Usage](../../README.md)
