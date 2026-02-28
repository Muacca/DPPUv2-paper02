"""
Shared Optimization Helpers for paper02
=========================================

Global minimum search with coarse grid (brute) + multi-start local refinement.
Used by 02_critical_analysis.py and 03_comparison.py.

Pattern adapted from scripts/run_critical_analysis.py (brute + L-BFGS-B).
"""

import numpy as np
from scipy.optimize import minimize, brute
from typing import Dict, Tuple


def find_global_minimum(
    V_func,
    params: Dict[str, float],
    r_bounds: Tuple[float, float] = (0.01, 2.0),
    eps_bounds: Tuple[float, float] = (-0.95, 1.0),
    coarse_Ns: int = 20,
    n_candidates: int = 5,
    tol: float = 1e-8
) -> Tuple[float, float, float, bool]:
    """
    Find global minimum of V_eff(r, epsilon) for given parameters.

    Strategy:
      1. scipy.optimize.brute on (r, eps) grid with Ns points per axis
      2. Collect top-N grid candidates by function value
      3. Local refinement from each candidate using Nelder-Mead
      4. Return the best result across all starts

    Args:
        V_func: lambdified V(r, V, eta, theta_NY, L, kappa, epsilon, alpha)
        params: Dict with keys 'V', 'eta', 'theta_NY', 'L', 'kappa', 'alpha'
        r_bounds: (r_min, r_max) search bounds
        eps_bounds: (eps_min, eps_max) search bounds
        coarse_Ns: Number of grid points per axis for brute search
        n_candidates: Number of top candidates for multi-start refinement
        tol: Optimization tolerance

    Returns:
        (r_star, eps_star, V_min, success)
    """
    V_val = params.get('V', 4.0)
    eta_val = params.get('eta', -2.0)
    theta_val = params.get('theta_NY', 1.0)
    L_val = params.get('L', 1.0)
    kappa_val = params.get('kappa', 1.0)
    alpha_val = params.get('alpha', 0.0)

    def objective(x):
        r, eps = x
        # Enforce bounds: penalty for out-of-range (Nelder-Mead is unconstrained)
        if r < r_bounds[0] or r > r_bounds[1]:
            return 1e50
        if eps < eps_bounds[0] or eps > eps_bounds[1]:
            return 1e50
        try:
            val = V_func(r, V_val, eta_val, theta_val, L_val, kappa_val, eps, alpha_val)
            if np.isnan(val) or np.isinf(val):
                return 1e50
            return float(val)
        except Exception:
            return 1e50

    # Step 1: Coarse brute-force grid search
    rranges = (r_bounds, eps_bounds)
    x0_brute, fval_brute, grid, Jout = brute(
        objective, rranges, Ns=coarse_Ns, full_output=True, finish=None
    )

    # Step 2: Collect top-N candidates from the grid
    # Jout is a 2D array of function values on the grid
    flat_indices = np.argsort(Jout.flatten())[:n_candidates]
    r_grid = np.linspace(r_bounds[0], r_bounds[1], coarse_Ns)
    eps_grid = np.linspace(eps_bounds[0], eps_bounds[1], coarse_Ns)
    candidates = []
    for idx in flat_indices:
        i, j = np.unravel_index(idx, Jout.shape)
        candidates.append((r_grid[i], eps_grid[j], Jout[i, j]))

    # Step 3: Multi-start local optimization (L-BFGS-B respects bounds)
    bounds_opt = [r_bounds, eps_bounds]
    best_result = None
    best_val = float('inf')

    for r0, eps0, _ in candidates:
        try:
            res = minimize(
                objective,
                [r0, eps0],
                method='L-BFGS-B',
                bounds=bounds_opt,
                options={'ftol': tol, 'maxiter': 2000}
            )
            if res.fun < best_val:
                best_val = res.fun
                best_result = res
        except Exception:
            continue

    if best_result is not None and best_result.fun < fval_brute:
        return best_result.x[0], best_result.x[1], best_result.fun, True

    # Fallback to brute result
    return float(x0_brute[0]), float(x0_brute[1]), float(fval_brute), False
