# Curvature Layer

⇒ [日本語](README_ja.md)

Module group for curvature tensor computation and analysis.

## Overview

Provides Riemann tensor, Ricci scalar, Hodge dual, and self-duality diagnostics.

## Modules

### riemann.py

Riemann tensor computation and antisymmetry verification.

**Key classes/functions:**

- `compute_riemann_tensor(connection)`: Compute Riemann tensor
- `verify_antisymmetry(R)`: Verify antisymmetry at 3 levels
- `RiemannAntisymmetryError`: Exception for antisymmetry violations

**Antisymmetry verification (3 levels):**

1. **Level 1**: Symbolic proof via SymPy
2. **Level 2**: High-precision numerical counterexample search
3. **Level 3**: Debug mode (development)

**Riemann curvature definition:**

```
R^a_{bcd} = ∂_c Γ^a_{bd} - ∂_d Γ^a_{bc} + Γ^a_{ec}Γ^e_{bd} - Γ^a_{ed}Γ^e_{bc}
```

### ricci.py

Ricci tensor and scalar computation.

**Key functions:**

- `compute_ricci_tensor(R)`: Ricci contraction
- `compute_ricci_scalar(Ric, metric)`: Ricci scalar

**Definitions:**

```
R_{ab} = R^c_{acb}
R = η^{ab} R_{ab}
```

### hodge.py

Hodge dual operator implementation.

**Key functions:**

- `compute_hodge_dual(R)`: Compute Hodge dual of R^{ab}_{cd}
- `cd_block(a, b)`: 6-component block classification

**Hodge dual definition:**

```
(*R)^{ab}_{cd} = (1/2) ε_{cdef} R^{ab,ef}
```

### self_duality.py

Self-duality (SD/ASD) diagnostics.

**Key classes:**

- `SDExtensionMixin`: Add SD functionality to engine
- `CurvatureSDDiagnostics`: SD residual computation and evaluation

**SD/ASD conditions:**

```
R = *R   (self-dual: SD)
R = -*R  (anti-self-dual: ASD)
```

**Key metrics:**

- `sd_residual`: ||R - *R||
- `asd_residual`: ||R + *R||
- `is_sd`: sd_residual < ε
- `is_asd`: asd_residual < ε

### pontryagin.py

Pontryagin inner product computation and diagnostics.

**Key classes/functions:**

- `compute_pontryagin_inner_product(R)`: Compute P = ⟨R, *R⟩
- `evaluate_sd_status(params)`: Full SD status diagnostics

**Key result:**

```
P = ⟨R, *R⟩ = 0  (holds for all topologies and modes)
```

This implies:
```
SD_residual / ||R|| = √2
ASD_residual / ||R|| = √2
```

## Usage

```python
from dppu.curvature import SDExtensionMixin, CurvatureSDDiagnostics

# Attach SD extension to engine
SDExtensionMixin.attach_to(engine)

# SD diagnostics
diag = CurvatureSDDiagnostics(engine)
result = diag.evaluate_sd_status({
    'r': 1.0, 'L': 1.0, 'eta': -1.0, 'V': 2.0,
    'kappa': 1.0, 'theta_NY': 0.0
})

print(f"P = {result['P_RstarR']:.2e}")
print(f"SD/||R|| = {result['sd_residual']/result['curvature_norm']:.4f}")
```

## Dependencies

- [connection](../connection/README.md): EC connection
- [utils](../utils/README.md): Levi-Civita symbol

