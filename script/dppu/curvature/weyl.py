"""Ricci-trace removal and direct tensor norm.

For algebraic Riemann curvature this gives the Weyl tensor. For general RC
curvature the same removal gives the broader Ricci-tracefree tensor. Use
rc_weyl.irreducible_weyl_curvature for the RC Weyl part.
"""

from typing import Any, Optional, Tuple

from sympy import S, simplify, Matrix, Rational
from sympy.tensor.array import MutableDenseNDimArray

def compute_weyl_tensor(
    R_abcd: MutableDenseNDimArray,
    Ricci: Matrix,
    R_scalar: Any,
    metric: Matrix,
    dim: int,
    logger: Optional[Any] = None
) -> MutableDenseNDimArray:
    """
    Remove Ricci traces; Weyl only for algebraic Riemann curvature.

    Args:
        R_abcd: Curvature tensor with all lower indices
        Ricci: Ricci tensor R_{ab}
        R_scalar: Ricci scalar R
        metric: Metric tensor g_{ab} (or eta_{ab})
        dim: Dimension (must be >= 3, usually 4)
        logger: Optional logger

    Returns:
        Ricci-tracefree tensor as MutableDenseNDimArray; Weyl for algebraic Riemann input
    """
    if logger:
        logger.info("Removing curvature Ricci traces...")

    if dim < 3:
        return MutableDenseNDimArray.zeros(dim, dim, dim, dim)

    C_abcd = MutableDenseNDimArray.zeros(dim, dim, dim, dim)

    n = dim
    if n == 4:
        coeff_Ricci = Rational(1, 2)
        coeff_Scalar = Rational(1, 6)
    else:
        coeff_Ricci = Rational(1, n - 2)
        coeff_Scalar = Rational(1, (n - 1) * (n - 2))

    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                for d in range(dim):
                    term = R_abcd[a, b, c, d]

                    term_Ricci = (
                        metric[a, c] * Ricci[b, d] -
                        metric[a, d] * Ricci[b, c] -
                        metric[b, c] * Ricci[a, d] +
                        metric[b, d] * Ricci[a, c]
                    )
                    
                    term -= coeff_Ricci * term_Ricci
                    
                    term_Scalar = (
                        metric[a, c] * metric[b, d] -
                        metric[a, d] * metric[b, c]
                    )
                    
                    term += coeff_Scalar * R_scalar * term_Scalar
                    
                    if term != 0:
                        C_abcd[a, b, c, d] = simplify(term)

    if logger:
        logger.success("Ricci-tracefree tensor computed")

    return C_abcd

def compute_weyl_scalar(
    C_abcd: MutableDenseNDimArray,
    metric_inv: Matrix,
    dim: int,
    logger: Optional[Any] = None
) -> Any:
    """
    Compute the direct squared norm of a tensor with four lower indices.

    The function and argument names are retained for compatibility.
    The input may be LC-Weyl, irreducible EC-Weyl, or Ricci-tracefree EC curvature.

    Args:
        C_abcd: Selected tensor with all lower indices (compatibility name)
        metric_inv: Inverse metric g^{ab} (or eta^{ab})
        dim: Dimension
        logger: Optional logger

    Returns:
        Tensor squared norm as SymPy expression
    """
    if logger:
        logger.info("Computing tensor squared norm I...")

    C_sq = S.Zero

    C_upper = MutableDenseNDimArray.zeros(dim, dim, dim, dim)
    
    has_nonzero = False
    
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                for d in range(dim):
                    val = S.Zero

                    is_diagonal = True
                    for i in range(dim):
                        for j in range(dim):
                            if i != j and metric_inv[i, j] != 0:
                                is_diagonal = False
                                break
                    
                    if is_diagonal:
                         val = (metric_inv[a, a] * metric_inv[b, b] * 
                                metric_inv[c, c] * metric_inv[d, d] * 
                                C_abcd[a, b, c, d])
                    else:
                        for e in range(dim):
                            for f in range(dim):
                                for g in range(dim):
                                    for h in range(dim):
                                        term = (metric_inv[a, e] * metric_inv[b, f] * 
                                                metric_inv[c, g] * metric_inv[d, h] * 
                                                C_abcd[e, f, g, h])
                                        val += term
                    
                    if val != 0:
                        C_upper[a, b, c, d] = simplify(val)
                        has_nonzero = True

    if not has_nonzero:
        return S.Zero

    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                for d in range(dim):
                    term = C_abcd[a, b, c, d] * C_upper[a, b, c, d]
                    C_sq += term

    C_sq = simplify(C_sq)

    if logger:
        logger.info(f"  Tensor squared norm I = {C_sq}")

    return C_sq
