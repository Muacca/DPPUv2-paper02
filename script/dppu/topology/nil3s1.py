"""
Nil³×S¹ Topology Implementation
===============================

Heisenberg nilmanifold (Bianchi II) × circle.
Structure constants: C²₀₁ = -1/R, C²₁₀ = +1/R
Volume: V = (2π)⁴LR³
"""

from sympy import symbols, Matrix, S, pi, simplify, Rational
from sympy.tensor.array import MutableDenseNDimArray

from ..engine.pipeline import BaseFrameEngine
from ..torsion.mode import Mode


class Nil3S1Engine(BaseFrameEngine):
    """Nil³×S¹ (Heisenberg) Topology Engine."""

    def step_E4_1_setup(self):
        """Setup parameters for Nil³×S¹."""
        self.logger.info("Topology: Nil³×S¹ (Heisenberg)")

        R = symbols('R', positive=True, real=True)
        L = symbols('L', positive=True, real=True)
        kappa = symbols('kappa', positive=True, real=True)
        theta_NY = symbols('theta_NY', real=True)
        epsilon = symbols('epsilon', real=True)
        alpha = symbols('alpha', real=True)


        if self.mode == Mode.AX:
            eta = symbols('eta', real=True)
            V = S.Zero
        elif self.mode == Mode.VT:
            eta = S.Zero
            V = symbols('V', real=True, positive=True)
        else:  # MX
            eta = symbols('eta', real=True)
            V = symbols('V', real=True, positive=True)

        self.data['params'] = {
            'R': R, 'r': R,  # Alias for compatibility
            'L': L, 'kappa': kappa, 'theta_NY': theta_NY,
            'eta': eta, 'V': V, 'epsilon': epsilon, 'alpha': alpha, 'q': 2 * eta
        }
        self.data['dim'] = 4
        self.logger.success("Setup complete")

    def step_E4_2_metric_and_frame(self):
        """Define metric, volume, structure constants for Nil³×S¹ (Squashed)."""
        dim = self.data['dim']
        R = self.data['params']['R']
        L = self.data['params']['L']
        epsilon = self.data['params']['epsilon']

        # Frame metric (identity)
        self.data['metric_frame'] = Matrix.eye(dim)

        # Volume: (2π)⁴LR³
        self.data['total_volume'] = (2 * pi)**4 * L * R**3

        # Structure constants (Squashed)
        # Base: C²₀₁ = -1/R, C²₁₀ = +1/R
        # Squashed: C^2_{01} -> (1+eps)^(-4/3) * C_base
        
        factor = (1 + epsilon)**Rational(-4, 3)
        lam = (1 / R) * factor

        C = MutableDenseNDimArray.zeros(dim, dim, dim)
        C[2, 0, 1] = -lam
        C[2, 1, 0] = +lam

        self.data['structure_constants'] = C

        # Verify antisymmetry
        self._verify_structure_antisymmetry(C, dim)
        self.logger.success("Heisenberg structure constants defined")

    def _verify_structure_antisymmetry(self, C, dim):
        """Verify C^a_bc = -C^a_cb."""
        for a in range(dim):
            for b in range(dim):
                for c in range(b + 1, dim):
                    check = simplify(C[a, b, c] + C[a, c, b])
                    if check != 0:
                        raise ValueError(f"Antisymmetry violated: C^{a}_{b}{c}")
