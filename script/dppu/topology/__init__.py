"""
DPPU Topology Layer
===================

Topology-specific implementations for M³×S¹ manifolds.

Available:
- S3S1Engine: S³×S¹ (3-sphere × circle)
- T3S1Engine: T³×S¹ (3-torus × circle)
- Nil3S1Engine: Nil³×S¹ (Heisenberg × circle)
"""

from .s3s1 import S3S1Engine
from .t3s1 import T3S1Engine
from .nil3s1 import Nil3S1Engine

__all__ = ['S3S1Engine', 'T3S1Engine', 'Nil3S1Engine']
