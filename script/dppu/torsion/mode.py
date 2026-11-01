"""
Torsion Mode Enum
=================

Defines the torsion ansatz modes for Einstein-Cartan gravity.

Physical Background:
    The torsion tensor T^λ_μν can be decomposed into three irreducible parts:
    1. Totally antisymmetric (axial/pseudoscalar): S^μ
    2. Vector trace: T_μ
    3. Tensor part (traceless, hook-symmetric)

    For our M³×S¹ ansatz, we consider only the first two:
    - Axial component: S^μ = (η/r)(0,0,0,1) in frame basis
    - Vector-trace component: T_μ = V·δ^3_μ

Modes:
    - AX: Axial-only (S^μ allowed, T_μ = 0)
    - VT: Vector-trace-only (T_μ allowed, S^μ = 0)
    - MX: Mixed (both components allowed, including zero amplitudes)

Author: Muacca
"""

from enum import Enum


class Mode(Enum):
    """
    Torsion ansatz mode enumeration.

    Attributes:
        AX: Axial-only mode.
            Only the totally antisymmetric (axial) component is allowed.
            Parameters: η real, V = 0

        VT: Vector-trace-only mode.
            Only the vector-trace component is allowed.
            Parameters: η = 0, V real

        MX: Mixed mode.
            Both axial and vector-trace components are allowed, including zero amplitudes.
            Parameters: η and V real

    Examples:
        >>> mode = Mode.MX
        >>> mode.value
        'MX'
        >>> Mode['AX']
        <Mode.AX: 'AX'>
    """
    AX = "AX"    # Axial-only (S^μ allowed, T_μ = 0)
    VT = "VT"    # Vector-trace-only (T_μ allowed, S^μ = 0)
    MX = "MX"    # Mixed (both components allowed, including zero amplitudes)

    def __str__(self) -> str:
        return self.value

    @property
    def has_axial(self) -> bool:
        """True if this mode includes axial component."""
        return self in (Mode.AX, Mode.MX)

    @property
    def has_vector_trace(self) -> bool:
        """True if this mode includes vector-trace component."""
        return self in (Mode.VT, Mode.MX)

    @property
    def description(self) -> str:
        """Human-readable description of the mode."""
        descriptions = {
            Mode.AX: "Axial only",
            Mode.VT: "Vector trace only",
            Mode.MX: "Axial and vector trace (zero amplitudes allowed)",
        }
        return descriptions[self]
