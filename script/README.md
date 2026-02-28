# DPPUv2 Computation Engine v4 — Scripts Directory

⇒ [日本語](README_ja.md)

**Paper**: "Structural Robustness of Isotropic S³ Vacua in Einstein-Cartan Minisuperspace via Chiral Equilibrium and Weyl Stability" (paper02)

Python packages and execution scripts for numerical and symbolic computation in Einstein-Cartan + Nieh-Yan + Weyl extended minisuperspace.

---

## Directory Structure

```
script/
├── dppu/                      # Main Python package (DPPUv2 Engine v4)
│   ├── geometry/              # Metric, volume form, structure constants
│   ├── connection/            # Levi-Civita connection, Contortion, EC connection
│   ├── curvature/             # Riemann, Ricci, Hodge dual, self-duality, Pontryagin, Weyl
│   ├── torsion/               # Torsion modes, Ansatz, Nieh-Yan density
│   ├── action/                # Lagrangian, effective potential, stability classification
│   ├── topology/              # S³×S¹, T³×S¹, Nil³×S¹ engines
│   ├── engine/                # Computation pipeline, logging, checkpointing
│   ├── scanning/              # Parameter scan, squashing scan, Phase 1 integration
│   └── utils/                 # Common utilities (Levi-Civita symbol, symbolic computation)
│
└── scripts/                   # Execution scripts
    ├── pipeline/              # Topology runners, parameter scans
    ├── paper02/               # paper02-specific analysis scripts
    ├── proofs/                # Analytic and symbolic proof scripts
    └── visualize/             # Figure-generation Jupyter Notebooks
```

### `docs/` - Documentation

Technical documentation and conventions:
- [DPPUv2 Engine CONVENTIONS](docs/CONVENTIONS.md) - Engine core conventions and specifications
- [DPPUv2 SymPy guideline](docs/SymPy_guideline.md) - SymPy usage guidelines and best practices

---

## Package Overview (dppu/)

| Module | Role | Key Classes / Functions |
|--------|------|------------------------|
| [`geometry`](dppu/geometry/README.md) | Metric and frame field definitions | `build_metric`, `frame_field` |
| [`connection`](dppu/connection/README.md) | EC connection construction | `levi_civita`, `contortion`, `ec_connection` |
| [`curvature`](dppu/curvature/README.md) | Curvature tensors, SD diagnostics | `RiemannTensor`, `SDExtensionMixin`, `compute_pontryagin_inner_product` |
| [`torsion`](dppu/torsion/README.md) | Torsion structure | `Mode`, `NyVariant`, `build_torsion_tensor` |
| [`action`](dppu/action/README.md) | Action and stability analysis | `build_lagrangian`, `classify_stability` |
| [`topology`](dppu/topology/README.md) | Three-topology engines | `S3S1Engine`, `T3S1Engine`, `Nil3S1Engine` |
| [`engine`](dppu/engine/README.md) | 15-step computation pipeline | `BaseFrameEngine`, `ComputationLogger`, `CheckpointManager` |
| [`scanning`](dppu/scanning/README.md) | Parameter space scanning | `run_scan`, `Phase1ResultsLoader`, `SDDiagnosticsWithPhase1` |
| [`utils`](dppu/utils/README.md) | Common utilities | `LeviCivita`, `symbolic_simplify` |

---

## Script Overview (scripts/)

### pipeline/ — Topology Runners

| Script | Description |
|--------|-------------|
| `run_s3s1.py` | Run the S³×S¹ engine for a single parameter set |
| `run_t3s1.py` | Run the T³×S¹ engine |
| `run_nil3s1.py` | Run the Nil³×S¹ engine |
| `run_parameter_scan.py` | Grid scan over (V, η, θ) parameter space |
| `run_mode_ny_scan.py` | Combinatorial scan over torsion modes × NY variants |
| `run_sd_analysis.py` | Self-duality (SD) diagnostics |
| `run_pontryagin_diagnostic.py` | Pontryagin inner product P = ⟨R, *R⟩ diagnostics (auto-detects `run_parameter_scan_*.csv` in `--input-dir`, applies topology filter) |
| `run_alpha_boundary_scan.py` | Verify parameter independence of the α = 0 stability boundary by varying (V, η, θ_NY) (Theorem 3) |

### paper02/ — paper02-Specific Analysis

| Script | Description |
|--------|-------------|
| `potential_landscape_mapping.py` | Generate (r, ε) potential landscape for multiple α values |
| `critical_analysis.py` | High-resolution analysis near the α = 0 phase transition (tracks ε*, r*, V_min) |
| `topology_comparison.py` | Compare potentials for S³, T³, Nil³ under the Weyl extension |
| `optimization_helper.py` | Utility for global minimum search |

### proofs/ — Analytic and Symbolic Proofs

| Script | Proof Content |
|--------|---------------|
| `analytic_proof_P_equals_zero.py` | **Proposition 1**: Algebraic proof of P = ⟨R, *R⟩ ≡ 0 (outputs .log) |
| `symbolic_block_all_topologies.py` | **Proposition 1** symbolic verification: block-structure check for all topologies (S³, T³, Nil³) (outputs .log) |
| `analytical_proof.py` | **Lemma 1** SymPy proof: symbolic confirmation of C²(ε=0)=0, ∂C²/∂ε|₀=0, ∂²C²/∂ε²|₀>0 (corresponds to paper Appendix C.5, outputs .log) |

### visualize/ — Figure Generation and Interactive Viewer

| File | Contents |
|------|----------|
| `DPPUv2_Paper_Figures.ipynb` | Jupyter Notebook generating all paper02 figures |
| `DPPUv2_visualize_notebook_v4.ipynb` | Interactive phase diagram and effective potential Notebook |
| `DPPUv2_interactive_viewer_v4.py` | Interactive phase diagram and potential viewer for Jupyter (`%matplotlib widget` required) |

---

## Quick Start

### Install Dependencies

```bash
pip install sympy numpy scipy pandas tqdm matplotlib
```

### Run a Single Topology

```bash
# Run from the script/ directory (output: output/run_s3s1_YYYYMMDD_HHMMSS.log)
python scripts/pipeline/run_s3s1.py --mode MX --ny-variant FULL
python scripts/pipeline/run_t3s1.py --mode MX --ny-variant FULL
python scripts/pipeline/run_nil3s1.py --mode MX --ny-variant FULL

# Specify output directory
python scripts/pipeline/run_s3s1.py --mode MX --ny-variant FULL --output-dir results/
```

### Symbolic Proofs for Proposition 1

```bash
# Proposition 1: algebraic proof of P = 0 (generates output/analytic_proof_P_equals_zero_TIMESTAMP.log)
python scripts/proofs/analytic_proof_P_equals_zero.py

# Proposition 1: symbolic block-structure verification for all topologies (S³, T³, Nil³)
python scripts/proofs/symbolic_block_all_topologies.py

# Lemma 1: SymPy symbolic proof of C²(ε=0)=0, ∂C²/∂ε|₀=0, ∂²C²/∂ε²|₀>0 (Appendix C.5)
python scripts/proofs/analytical_proof.py

# Specify output directory (applies to all proofs/ scripts)
python scripts/proofs/analytic_proof_P_equals_zero.py --output-dir proof_logs/
```

### Weyl Extension Analysis (paper02 Main Results)

```bash
# Map (r, ε) potential landscape (all alpha values in one CSV)
python scripts/paper02/potential_landscape_mapping.py --topology S3

# High-resolution analysis near the α = 0 phase transition
python scripts/paper02/critical_analysis.py

# Topology comparison
python scripts/paper02/topology_comparison.py

# Specify output directory (applies to all paper02/ scripts)
python scripts/paper02/critical_analysis.py --output-dir paper02_results/
```

### Parameter Scan and Diagnostics (Phase 1 Integration)

```bash
# Grid scan (output: run_parameter_scan_TIMESTAMP.csv)
python scripts/pipeline/run_parameter_scan.py --output-dir output/

# SD diagnostics (saves to run_sd_analysis_TIMESTAMP.csv)
python scripts/pipeline/run_sd_analysis.py \
    --input-csv output/run_parameter_scan_20260228_120000.csv \
    --theta 0.0 --output-dir output/

# Pontryagin diagnostics (saves to run_pontryagin_diagnostic_TIMESTAMP.csv)
# If run_parameter_scan_*.csv files exist in output/, they are auto-detected with topology filter
python scripts/pipeline/run_pontryagin_diagnostic.py \
    --input-dir output/ --output-dir output/

# Mode/NyVariant scan
python scripts/pipeline/run_mode_ny_scan.py --output-dir output/
```

### α = 0 Boundary Parameter Independence Scan (Theorem 3)

```bash
# Theorem 3 numerical verification: confirm that the α = 0 boundary is invariant under (V, η, θ_NY)
# Output: run_alpha_boundary_scan_TIMESTAMP.csv
python scripts/pipeline/run_alpha_boundary_scan.py --topology S3 --output-dir output/
```

### Using the Python API Directly

```python
from dppu.topology import S3S1Engine
from dppu.torsion import Mode, NyVariant
from dppu.engine import ComputationLogger

logger = ComputationLogger('run.log')
engine = S3S1Engine(Mode.MX, NyVariant.FULL, logger)
engine.run()
```

---

## paper02 Main Results and Corresponding Scripts

| Result | Paper Section | Content (Proof Type) | Script |
|--------|--------------|----------------------|--------|
| **Proposition 1** | §3 | P = ⟨R, *R⟩ ≡ 0 (chiral equilibrium) — **analytic proof** (geometric orthogonal decomposition) | `proofs/analytic_proof_P_equals_zero.py` |
| **Proposition 1** symbolic check | §3.5 | P = 0 **symbolically confirmed** for all topologies, modes, and NY variants | `proofs/symbolic_block_all_topologies.py`, `pipeline/run_mode_ny_scan.py`, `pipeline/run_pontryagin_diagnostic.py` |
| **Lemma 1** | §4 · AppC | Closed-form C²(r, ε) **symbolically derived** via SymPy (exact computation) | `proofs/analytical_proof.py` |
| **Theorem 1** | §5 | Isotropic vacuum Weyl stability for α ≤ 0 — **analytic proof** + **numerical verification** (201 points, 11-digit agreement) | `paper02/potential_landscape_mapping.py`, `paper02/critical_analysis.py` |
| **Theorem 2** | §6 | Unbounded-below instability for α > 0 — **analytic proof** (asymptotic scaling) + **numerical verification** (boundary convergence) | `paper02/critical_analysis.py` |
| **Theorem 3** | §7 | Parameter independence of the α = 0 stability boundary — **analytic proof** (geometric decoupling, asymptotic dominance) + **numerical verification** (4 parameter sets) | `pipeline/run_alpha_boundary_scan.py` |
| **Topology Comparison** | §8 | S³ preference, T³ null test, Nil³ flat-limit asymptotics under Weyl extension (**numerical analysis**) | `paper02/topology_comparison.py` |

---

## Topology Reference

| Topology | Lie Group | Background Curvature | Koszul Formula |
|----------|-----------|----------------------|----------------|
| S³×S¹ | SU(2) | +24/r² | Simplified |
| T³×S¹ | U(1)³ | 0 (flat) | Trivial |
| Nil³×S¹ | Heisenberg group | −1/(2R²) | General (bi-invariant does not hold) |

---

## Output File Convention

All execution scripts follow a unified output convention.

| Rule | Detail |
|------|--------|
| Option | `--output-dir OUTPUT_DIR` (default: `output`) |
| Filename | `{module_name}_{YYYYMMDD_HHMMSS}.{ext}` |
| Location | Directly under `OUTPUT_DIR` (no subdirectories) |
| Directory | Created automatically at runtime (`exist_ok=True`) |

| Script | Example Output File |
|--------|---------------------|
| run_s3s1/t3s1/nil3s1.py | `run_s3s1_20260228_153045.log` |
| run_alpha_boundary_scan.py | `run_alpha_boundary_scan_20260228_153045.csv` |
| run_mode_ny_scan.py | `run_mode_ny_scan_20260228_153045.csv` |
| run_sd_analysis.py | `run_sd_analysis_20260228_153045.csv` |
| run_pontryagin_diagnostic.py | `run_pontryagin_diagnostic_20260228_153045.csv` |
| potential_landscape_mapping.py | `potential_landscape_mapping_20260228_153045.csv` |
| critical_analysis.py (paper02) | `critical_analysis_20260228_153045.csv` |
| topology_comparison.py | `topology_comparison_20260228_153045.csv` |
| analytic_proof_P_equals_zero.py | `analytic_proof_P_equals_zero_20260228_153045.log` |
| analytical_proof.py | `analytical_proof_20260228_153045.log` |
| run_parameter_scan.py | `run_parameter_scan_20260228_153045.csv` |
| symbolic_block_all_topologies.py | `symbolic_block_all_topologies_20260228_153045.log` |

---

## Checkpoint Feature

Long-running computations can be interrupted and resumed:

```bash
# Run with checkpointing (--checkpoint-dir is independent of --output-dir)
python scripts/pipeline/run_s3s1.py --mode MX --ny-variant FULL \
    --output-dir output/ --checkpoint-dir ./checkpoints

# Resume after interruption (simply re-specify the checkpoint directory)
python scripts/pipeline/run_s3s1.py --mode MX --ny-variant FULL \
    --output-dir output/ --checkpoint-dir ./checkpoints
```
---
## License

See LICENSE file in the repository root.

---

**Author**: Muacca
**Version**: DPPUv2 Engine v4
**Date**: 2026-02
