"""Weyl and Ricci-tracefree projections of metric-compatible curvature.

All inputs have four lower indices. EC_IRR selects the Weyl part of the
Riemann--Cartan decomposition. EC_TRACEFREE retains its pair-antisymmetric
tracefree and four-form parts as well, defining a different quadratic action.
The projection does not assume a particular homogeneous torsion ansatz.
"""
from itertools import product
from sympy import Matrix, Rational, simplify, trace
from sympy.tensor.array import MutableDenseNDimArray
from .weyl import compute_weyl_tensor

CURVATURE_MODELS = ('LC', 'EC_IRR', 'EC_TRACEFREE')


def ricci_from_lower(curvature, metric):
    """Contract slots one and three with the inverse metric."""
    n = metric.rows
    inv = metric.inv()
    return Matrix(n, n, lambda b, d: simplify(sum(
        inv[a, c]*curvature[a, b, c, d] for a, c in product(range(n), repeat=2))))


def ricci_tracefree_curvature(curvature, metric):
    """Project to the kernel of the Ricci contraction (twenty components in 4D)."""
    n = metric.rows
    if n < 3:
        raise ValueError('Ricci-tracefree projection requires dimension >= 3')
    ricci = ricci_from_lower(curvature, metric)
    scalar = trace(metric.inv()*ricci)
    return compute_weyl_tensor(curvature, ricci, scalar, metric, n)


def irreducible_weyl_curvature(curvature, metric):
    """Project to algebraic Riemann symmetries, then remove Ricci traces.

    In 4D Euclidean signature the Weyl space has dimension ten (5+5 under
    self/anti-self duality). No torsion or field equations are imposed.
    """
    n = metric.rows
    if n != 4 or metric.cols != n or curvature.shape != (n,)*4:
        raise ValueError('The RC Weyl interface requires a 4D metric and curvature')
    indices = list(product(range(n), repeat=4))
    symmetric = MutableDenseNDimArray([
        (curvature[a,b,c,d]+curvature[c,d,a,b])/2 for a,b,c,d in indices], (n,)*4)
    algebraic = MutableDenseNDimArray([
        simplify(symmetric[a,b,c,d]-Rational(1,3)*(
            symmetric[a,b,c,d]+symmetric[a,c,d,b]+symmetric[a,d,b,c]))
        for a,b,c,d in indices], (n,)*4)
    return ricci_tracefree_curvature(algebraic, metric)
