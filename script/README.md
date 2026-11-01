# Calculation code and reproduction

EC denotes Einstein–Cartan, LC denotes Levi-Civita, and NY denotes Nieh–Yan.


[日本語](README_ja.md)

For Paper02 v2. [Conventions](docs/CONVENTIONS.md) / [LaTeX source](../LaTeX/main.tex)

```powershell
python -m pip install -r script/requirements.txt
python -B script/scripts/paper02/reproduce_figures.py render --output-dir rendered_figures
python -B script/scripts/paper02/reproduce_figures.py recompute --output-dir recomputed_figures
python -B script/scripts/pipeline/run_parameter_scan.py --topologies S3 T3 Nil3 --ny-variants FULL --V-range 0 4 3 --eta-range -3 3 7 --alpha -0.1 0 0.1 --workers 1 --output-dir new_scan
```

Run these commands from the repository root. Render creates figures from saved data; recompute also evaluates the public engine. Existing figure output directories are rejected.

| Entry point | Function and scope |
|---|---|
| `dppu/topology` | S3S1Engine, T3S1Engine, Nil3S1Engine |
| `scripts/pipeline/run_s3s1.py` / `run_t3s1.py` / `run_nil3s1.py` | Symbolic calculation for a mode and NY variant |
| `scripts/pipeline/run_parameter_scan.py` | Joint radius/shape and fixed-shape radial classification |
| `scripts/proofs/analytical_proof.py` | Independent LC-Weyl symbolic calculation |
| `scripts/proofs/symbolic_block_all_topologies.py` | EC curvature block structure in the three specified homogeneous geometries |
| [Figure notebook](scripts/visualize/DPPUv2_Paper_Figures.ipynb) | Separate saved-data rendering and explicit recomputation cells |
| [Viewer notebook](scripts/visualize/DPPUv2_visualize_notebook_v4.ipynb) | Shared analytic classification and engine-direct potential curves |

Code V,eta use the tau convention; the manuscript amplitudes have opposite signs.

```python
import sys
sys.path.insert(0, 'script')
from dppu.topology.s3s1 import S3S1Engine
from dppu.torsion.mode import Mode
from dppu.torsion.nieh_yan import NyVariant
engine = S3S1Engine(Mode.MX, NyVariant.FULL)
engine.run()
U = engine.get_effective_potential_function()
# r, V_code, eta_code, theta_NY, L, kappa, epsilon, alpha
print(U(2, 4, -2, 1, 1, 1, 0, 0))
```

Torsion modes are MX (both components allowed), AX (axial only), and VT (vector trace only); all allow zero amplitudes. NY selectors are FULL (complete difference), TT (positive torsion-product coefficient), and REE (positive curvature–coframe coefficient), multiplied by the real theta coupling. AX ignores the callable V argument; VT ignores eta. Key engine.data outputs are `potential`, `riemann`, `ricci_scalar`, `quadratic_scalar`, and `ny_density_full`; `weyl_scalar` retains its LC meaning.

Current figure and table data are in [data/revised](../data/revised/README.md). Use fresh output directories. Checkpoint loading is explicit; engine.run does not automatically load saved state. Notebook outputs are cleared; restart kernels after source changes.

See [classification and CSV fields](docs/CLASSIFICATION.md). The scan and viewer distinguish finite minima, unattained infima, degenerate minimum sets and unbounded potentials, separately on the joint domain and a fixed-shape radial slice. TT/REE are outside the paper classification. Inputs are not rounded and plot limits do not cut off the classification.

## Symbolic supplements and notebooks

From the repository root, run the supplements into new output directories:

```powershell
python -B script/scripts/pipeline/run_s3s1.py --mode MX --ny-variant FULL --output-dir new_s3
python -B script/scripts/pipeline/run_t3s1.py --mode MX --ny-variant FULL --output-dir new_t3
python -B script/scripts/pipeline/run_nil3s1.py --mode MX --ny-variant FULL --output-dir new_nil
python -B script/scripts/proofs/analytical_proof.py --output-dir new_weyl
python -B script/scripts/proofs/symbolic_block_all_topologies.py --output-dir new_blocks
```

Open the notebooks in a Jupyter environment. The viewer notebook finds the repository from its working directory and uses the ipympl widget backend. Apply controls to redraw both panels; the selected-point table reports both classification domains. The figure notebook can run from the repository root or a subdirectory; rendering supplied data is its default, and recomputation requires `RECOMPUTE=True`.

## Computational guides

[Conventions](docs/CONVENTIONS.md) specifies indices, signs, global geometry and shape; [implementation](docs/SymPy_guideline.md) explains symbolic computation and APIs; [classification](docs/CLASSIFICATION.md) covers joint/radial results, CSV and the viewer. The public library contains the current calculation and reproduction paths. Public computations do not require SciPy.

[Curvature models](docs/WEYL_MODELS.md)

The default engine, runner, scan and viewer model is EC_IRR (irreducible EC-Weyl). Select LC for the reference or EC_TRACEFREE for the Ricci-tracefree EC curvature action. The supplied figure data retain LC provenance and also describe the irreducible EC-Weyl action on the specified family. The action consumes quadratic_scalar; weyl_scalar remains the LC compatibility key.
