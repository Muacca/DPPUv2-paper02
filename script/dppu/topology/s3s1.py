"""
S³×S¹ Topology Implementation
=============================

3-sphere (SU(2)) × circle.
Structure constants: C^i_jk = (4/r)ε_ijk
Volume: V = 2π²Lr³
"""

from sympy import symbols, Matrix, S, pi, Rational
from sympy.tensor.array import MutableDenseNDimArray

from ..engine.pipeline import BaseFrameEngine
from ..torsion.mode import Mode
from ..utils.levi_civita import epsilon_symbol


class S3S1Engine(BaseFrameEngine):
    """S³×S¹ Topology Engine."""

    def step_E4_1_setup(self):
        """Setup parameters for S³×S¹."""
        self.logger.info("Topology: S³×S¹")

        r = symbols('r', positive=True, real=True)
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
            'r': r, 'L': L, 'kappa': kappa, 'theta_NY': theta_NY,
            'eta': eta, 'V': V, 'epsilon': epsilon, 'alpha': alpha, 'q': 2 * eta
        }
        self.data['dim'] = 4
        self.logger.success("Setup complete")

    def step_E4_2_metric_and_frame(self):
        """Define metric, volume, structure constants for S³×S¹ (Squashed)."""
        dim = self.data['dim']
        r = self.data['params']['r']
        L = self.data['params']['L']
        epsilon = self.data['params']['epsilon']

        # Frame metric (identity)
        self.data['metric_frame'] = Matrix.eye(dim)

        # Volume: 2π²Lr³ (Preserved by ansatz)
        self.data['total_volume'] = 2 * pi**2 * L * r**3

        # Structure constants: 
        # Base: C^i_jk = (4/r)ε_ijk
        # Squashed:
        # C^0_12 -> (1+eps)^(2/3) * C_base
        # C^1_20 -> (1+eps)^(2/3) * C_base
        # C^2_01 -> (1+eps)^(-4/3) * C_base
        
        C = MutableDenseNDimArray.zeros(dim, dim, dim)
        
        # Factors for C^a_{bc} where a,b,c are permutation of 0,1,2
        # If a=0 (bc=12 or 21): factor (1+eps)^(2/3)
        # If a=1 (bc=20 or 02): factor (1+eps)^(2/3)
        # If a=2 (bc=01 or 10): factor (1+eps)^(-4/3)
        
        factor_0 = (1 + epsilon)**Rational(2, 3)
        factor_1 = (1 + epsilon)**Rational(2, 3)
        factor_2 = (1 + epsilon)**Rational(-4, 3)
        
        factors = [factor_0, factor_1, factor_2]

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    eps_val = epsilon_symbol(i, j, k)
                    if eps_val != 0:
                        # Base value
                        val = 4 * eps_val / r
                        # Apply factor based on upper index i
                        val *= factors[i]
                        C[i, j, k] = val

        self.data['structure_constants'] = C
        self.logger.success("Metric and structure constants defined")
