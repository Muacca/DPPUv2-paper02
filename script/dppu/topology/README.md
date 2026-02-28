# Topology Layer

⇒ [日本語](README_ja.md)

Module group providing topology-specific computation engines.

## Overview

Dedicated computation engines for three topologies: S³×S¹, T³×S¹, Nil³×S¹.

## Modules

### s3s1.py

**S³×S¹ (3-sphere × circle) Engine**

**Mathematical structure:**

- Lie group: SU(2)
- Structure constants: C^i_{jk} = (4/r)ε_{ijk}
- Metric: bi-invariant
- Background curvature: R_LC = 24/r² (positive)

**Volume:**
```
V = 2π²Lr³
```

**Usage:**
```python
from dppu.topology import S3S1Engine
from dppu.torsion import Mode, NyVariant

engine = S3S1Engine(Mode.MX, NyVariant.FULL)
engine.run()
```

### t3s1.py

**T³×S¹ (3-torus × circle) Engine**

**Mathematical structure:**

- Lie group: U(1)³ (Abelian)
- Structure constants: All zero
- Metric: flat
- Background curvature: R_LC = 0

**Volume:**
```
V = (2π)⁴LR₁R₂R₃
```

Uses isotropic scaling R₁ = R₂ = R₃ = r.

**Usage:**
```python
from dppu.topology import T3S1Engine

engine = T3S1Engine(Mode.MX, NyVariant.FULL)
engine.run()
```

### nil3s1.py

**Nil³×S¹ (Heisenberg nilmanifold × circle) Engine**

**Mathematical structure:**

- Lie group: Heisenberg group
- Structure constants: [E₀, E₁] = (1/R)E₂
- Metric: left-invariant (**NOT bi-invariant**)
- Background curvature: R_LC = -1/(2R²) (negative)

**Volume:**
```
V = (2π)⁴LR³
```

**Important note:**

Since Nil³ does not admit a bi-invariant metric, the general Koszul formula is used:
```
Γ^a_{bc} = (1/2)(C^a_{bc} + η^{ad}η_{be}C^e_{dc} - η^{ad}η_{ce}C^e_{bd})
```

**Usage:**
```python
from dppu.topology import Nil3S1Engine

engine = Nil3S1Engine(Mode.MX, NyVariant.FULL)
engine.run()
```

## Common Engine Interface

All engines inherit from `BaseFrameEngine` and provide a unified interface:

```python
class BaseFrameEngine:
    def run(self):
        """Execute the 15-step computation pipeline"""

    def get_R_ab_cd_numerical(self, params):
        """Numerically evaluate R^{ab}_{cd}"""

    def get_effective_potential(self, params):
        """Get effective potential"""
```

## Topology Comparison

| Property | S³×S¹ | T³×S¹ | Nil³×S¹ |
|----------|-------|-------|---------|
| Structure constants | ε_{ijk} | 0 | [E₀,E₁]=E₂ |
| Background curvature | +24/r² | 0 | -1/(2R²) |
| bi-invariant | Yes | Yes | **No** |
| Koszul formula | Simplified | Trivial | General |

## Dependencies

- [engine](../engine/README.md): BaseFrameEngine
- [geometry](../geometry/README.md): Metric definitions
- [connection](../connection/README.md): Connection computation
- [curvature](../curvature/README.md): Curvature computation
- [torsion](../torsion/README.md): Torsion construction
- [action](../action/README.md): Action and stability
