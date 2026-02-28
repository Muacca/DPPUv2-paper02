"""
T³×S¹ Topology Implementation
=============================

Flat 3-torus × circle.
Structure constants: All zero (Abelian)
Volume: V = (2π)⁴LR₁R₂R₃
"""

from sympy import symbols, Matrix, S, pi
from sympy.tensor.array import MutableDenseNDimArray

from ..engine.pipeline import BaseFrameEngine
from ..torsion.mode import Mode


class T3S1Engine(BaseFrameEngine):
    """T³×S¹ (Flat Torus) Topology Engine."""

    def step_E4_1_setup(self):
        """Setup parameters for T³×S¹."""
        self.logger.info("Topology: T³×S¹ (Flat)")

        # Isotropic: R1 = R2 = R3 = r
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
            'r': r, 'R1': r, 'R2': r, 'R3': r,
            'L': L, 'kappa': kappa, 'theta_NY': theta_NY,
            'eta': eta, 'V': V, 'epsilon': epsilon, 'alpha': alpha, 'q': 2 * eta
        }
        self.data['dim'] = 4
        self.logger.success("Setup complete")

    def step_E4_2_metric_and_frame(self):
        """Define metric, volume, structure constants for T³×S¹."""
        dim = self.data['dim']
        r = self.data['params']['r']
        L = self.data['params']['L']

        # Frame metric (identity)
        self.data['metric_frame'] = Matrix.eye(dim)

        # Volume (isotropic): (2π)⁴L r³
        self.data['total_volume'] = (2 * pi)**4 * L * r**3

        # Structure constants: All zero (Abelian/flat)
        self.data['structure_constants'] = MutableDenseNDimArray.zeros(dim, dim, dim)

        self.logger.success("Flat torus metric defined")
