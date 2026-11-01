"""
DPPU Curvature Layer
====================

Provides curvature-related components for Einstein-Cartan gravity.

Modules:
- riemann: Riemann tensor computation and antisymmetry verification
- ricci: Ricci tensor and scalar
- weyl: Ricci-trace removal and direct norm
- rc_weyl: irreducible EC-Weyl and Ricci-tracefree model projections
"""

from .riemann import RiemannAntisymmetryError, verify_antisymmetry_strict
from .ricci import compute_ricci_scalar, compute_ricci_tensor

__all__ = [
    'RiemannAntisymmetryError',
    'verify_antisymmetry_strict',
    'compute_ricci_scalar',
    'compute_ricci_tensor',
]
