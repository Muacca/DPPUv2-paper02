# SymPy Implementation Guidelines — Paper02

EC denotes Einstein–Cartan, LC denotes Levi-Civita, and NY denotes Nieh–Yan.


Identifiers such as E4.3 and E4.8a are public computation/checkpoint steps. Their functions are described alongside the IDs; they are not research phases.


For readers using or extending the public engine. Shared geometric conventions are in [CONVENTIONS](CONVENTIONS.md), and in paper Sections 2–4 and Appendix A. Computation concerns the static homogeneous EC + complete NY + irreducible EC-Weyl action, with LC and the separate Ricci-tracefree action as comparisons on the three geometries.

[日本語](SymPy_guideline_ja.md) / [Conventions](CONVENTIONS.md) / [Classification](CLASSIFICATION.md)

## 1. Symbolic Arithmetic and Simplification

Use SymPy integers and `Rational` for symbolic coefficients; do not introduce floats into symbolic contractions. Concentrate simplification outside expensive component loops where possible and choose `factor`, `cancel` or `simplify` for the expression. `expand` may increase expression size; no uniform speed guarantee is implied.

E4.12 multiplies a homogeneous density by the global volume. If explicit multiple integration is introduced, check intermediate size and time against known integrals. The shape domain is epsilon > -1. A positive symbol x with `epsilon = x**Rational(-3, 2) - 1` preserves the allowed branch. Do not bypass assumptions with unconditional operations such as `powdenest(force=True)`.

## 2. Implementation Rules for Tensor Components

### Rule 2.1: Use Frame Components in the Stored Index Order

The engine works in an orthonormal frame with the Euclidean metric $`g_{ab}=\delta_{ab}`$ (`metric_frame`, default `Matrix.eye(dim)`). Raising and lowering frame indices is then the identity, and components may be used directly. Array positions must follow [CONVENTIONS Section 2](CONVENTIONS.md#2-indices-and-array-index-order):

* `C[a,b,c]` $`=C^a{}_{bc}`$
* `Gamma[a,b,c]` $`=\Gamma^a{}_{bc}`$, where the last index is the direction of differentiation
* `Riemann[a,b,c,d]` $`=R^a{}_{bcd}`$

For a non-orthonormal basis or another metric, lower all indices with the metric, permute them, and raise them again. A bare array transposition is not an index operation.

### Rule 2.2: Distinguish the Input Array $\tau$ from Geometric Torsion $T$

`torsion_tensor` stores the input array $\tau$. The torsion obtained from the Cartan equation is the geometric torsion $T=-\tau$, reconstructed from the stored input and connection. The contortion step `E4.5` applies the code formula to $\tau$:

```python
# Step E4.5: contortion of the input array tau
for a in range(dim):
    for b in range(dim):
        for c in range(dim):
            val = (tau[a, b, c] + tau[b, c, a] - tau[c, a, b]) * Rational(1, 2)
```

In geometric torsion the same contortion is $`K_{abc}[T]=-\frac12(T_{abc}+T_{bca}-T_{cab})`$ (paper Eq. D). Convert the array and both parameters together, $`\tau=-T`$, $`\eta_{\tau}=-\eta`$, $`V_{\tau}=-V`$. Do not reverse $K$ alone or only one torsion parameter.

### Rule 2.3: Torsion Consistency Check Including Structure Coefficients

In a noncoordinate frame, the torsion components contain the structure coefficients:

$$
T^a{}_{bc}=C^a{}_{bc}+\Gamma^a{}_{cb}-\Gamma^a{}_{bc}.
$$

After constructing the EC connection, confirm that this reproduces $-\tau$ with a mismatch count of **0**:

```python
dim = engine.data['dim']
C = engine.data['structure_constants']
Gamma_EC = engine.data['connection_EC']
tau = engine.data['torsion_tensor']
mismatch = sum(
    1
    for a in range(dim) for b in range(dim) for c in range(dim)
    if simplify(C[a, b, c] + Gamma_EC[a, c, b] - Gamma_EC[a, b, c] + tau[a, b, c]) != 0
)
assert mismatch == 0
```

The difference `Gamma_EC[a,b,c] - Gamma_EC[a,c,b]` alone omits $C$. It is not a valid check on $S^3$ or Nil, where $C\ne0$.

### Rule 2.4: Built-in Checks

* E4.3 calls the metric-compatibility checker and logs its result. The function returns `(passed, violations)`; this call site does not automatically raise. Check the verdict, for example with `assert passed`, when extending a runner.
* E4.3a (LC) and E4.7 (EC) verify $`R_{abcd}=-R_{bacd}`$ and $`R_{abcd}=-R_{abdc}`$ with the verdicts `PROVED_ZERO`, `WITNESS_NONZERO` and `UNPROVED`. An unproved residual is not treated as zero.
* Pair exchange $`R_{abcd}=R_{cdab}`$ is not required for a connection with torsion (paper Eq. P).

-----

## 3. Conventions Used by the Engine

### 3.1 Torsion and Curvature

Torsion and curvature are defined by two-forms, with $`\omega^a{}_{b}=\Gamma^a{}_{bc}e^c`$ ([CONVENTIONS Section 6](CONVENTIONS.md#6-torsion-and-curvature)):

$$
\begin{aligned}
T^a&=de^a+\omega^a{}_{b}\wedge e^b=\frac12T^a{}_{bc}\thinspace e^b\wedge e^c,\\
R^a{}_{b}&=d\omega^a{}_{b}+\omega^a{}_{c}\wedge\omega^c{}_{b}=\frac12R^a{}_{bcd}\thinspace e^c\wedge e^d.
\end{aligned}
$$

### 3.2 Connection

$$
\begin{aligned}
\Gamma^{\mathrm{EC}}_{abc}&=\Gamma^{\mathrm{LC}}_{abc}+K_{abc},\qquad
\Gamma^{\mathrm{LC}}_{abc}=\frac12\left(C_{abc}+C_{cba}-C_{bac}\right),\\
K_{abc}[T]&=-\frac12\left(T_{abc}+T_{bca}-T_{cab}\right)
=\frac12\left(\tau_{abc}+\tau_{bca}-\tau_{cab}\right).
\end{aligned}
$$

The Levi–Civita part is the general Koszul formula of [CONVENTIONS Section 5](CONVENTIONS.md#5-levi-civita-connection-general-koszul-implementation-in-dppuv2-engine). It does not assume a bi-invariant metric.

### 3.3 Curvature Components

With frame components constant in each runner, step `E4.7` uses

$$
R^a{}_{bcd}=\Gamma^a{}_{ec}\Gamma^e{}_{bd}-\Gamma^a{}_{ed}\Gamma^e{}_{bc}+\Gamma^a{}_{be}C^e{}_{cd}.
$$

The last term comes from $de^c$ in a noncoordinate frame and must not be dropped (paper Appendix A).

-----

## 4. Torsion Ansatz and Mode Decomposition Rules

### 4.1 Mode Definitions

| Mode | Input components |
|---|---|
| `Mode.AX` | Axial part only ( $`V_{\tau}=0`$ ) |
| `Mode.VT` | Vector-trace part only ( $`\eta_{\tau}=0`$ ) |
| `Mode.MX` | Both parts |

### 4.2 Components

Step `E4.4` builds the input array from the runner parameters `eta` $`=\eta_{\tau}`$, `V` $`=V_{\tau}`$ and the scale `r`. All three geometries use `params['r']`; Nil's internal symbol R denotes the same scale.

$$
\begin{aligned}
\tau^{\mathrm{ax}}_{ijk}&=\frac{2\eta_{\tau}}{r}\varepsilon_{ijk}\quad(i,j,k\in\lbrace 0,1,2\rbrace ),\\
\tau^{\mathrm{vec}}_{abc}&=\frac13\left(\delta_{ac}(V_{\tau})_{b}-\delta_{ab}(V_{\tau})_{c}\right),\qquad
(V_{\tau})_{a}=(0,0,0,V_{\tau}).
\end{aligned}
$$

The geometric torsion $T=-\tau$ has the same form with $`\eta=-\eta_{\tau}`$ and $`V=-V_{\tau}`$ (paper Eq. T). Runners supply the metric, structure constants, volume and parameters in steps `E4.1`–`E4.2`; they do not construct the torsion array themselves.

-----

## 5. Nieh–Yan Densities and Action Variants

### 5.1 Densities

With $`\varepsilon_{0123}=+1`$ in the Euclidean frame, step `E4.10` computes

$$
N_{\mathrm{TT}}=\frac14\varepsilon^{abcd}T^e{}_{ab}T_{ecd},\qquad
N_{\mathrm{REE}}=\frac12\varepsilon^{abcd}R_{abcd},\qquad
N_{\mathrm{FULL}}=N_{\mathrm{TT}}-N_{\mathrm{REE}}.
$$

The TT factor $1/4$ comes from the two torsion two-forms and the REE factor $1/2$ from the single curvature two-form. $`N_{\mathrm{TT}}`$ is quadratic in torsion, so evaluating it with $\tau$ gives the same value. On the ansatz of the three runners,

$$
N_{\mathrm{TT}}=N_{\mathrm{REE}}=-\frac{4V\eta}{r}=-\frac{4V_{\tau}\eta_{\tau}}{r},\qquad N_{\mathrm{FULL}}=0.
$$

### 5.2 Variant Selection

| `NyVariant` | NY term in the Lagrangian | Role |
|---|---|---|
| `NyVariant.FULL` | $`\theta N_{\mathrm{FULL}}`$ | Complete NY action |
| `NyVariant.TT` | $`\theta N_{\mathrm{TT}}`$ | Diagnostic action |
| `NyVariant.REE` | $`+\theta N_{\mathrm{REE}}`$ | Diagnostic action with a positive sign; not the negative component of FULL |

On this ansatz TT and REE give the same potential. Their barriers and $\theta$ dependence are not results of the complete NY action.

### 5.3 Implementation

`step_E4_10_nieh_yan_frame` stores `ny_density_TT`, `ny_density_Ree` and `ny_density_full`, and selects the adopted density by the `ny_variant` argument of `BaseFrameEngine`.

-----

## 6. Action and Reduced Potential

### 6.1 Quadratic curvature and action

E4.3a constructs LC curvature and Ricci; E4.3b constructs the LC-Weyl tensor and its squared norm. E4.7 constructs EC curvature; E4.8a projects the selected tensor and stores its norm I in quadratic_scalar. E4.11–E4.13 evaluate

$$
\mathcal L=\frac{R_{\mathrm{EC}}}{2\kappa^2}+\theta N+\alpha I,
\qquad S=\mathcal L\thinspace\mathrm{Vol}_{4},\qquad U=-S.
$$

`total_volume` belongs to the fixed quotient and volume-preserving shape family. Output keys are `riemann_LC`, `ricci_scalar_LC`, `weyl_tensor`, `weyl_scalar`, `riemann`, `ricci_scalar`, `lagrangian`, `action` and `potential`.

### 6.2 Obtaining the Potential

From the repository root:

```python
import sys
sys.path.insert(0, 'script')  # from the repository root
from dppu.torsion import Mode, NyVariant
from dppu.topology import S3S1Engine

engine = S3S1Engine(Mode.MX, NyVariant.FULL)
engine.run()
U = engine.get_effective_potential_function()
# (r, V_tau, eta_tau, theta_NY, L, kappa, epsilon, alpha)
print(U(1.0, 4.0, 0.0, 1.0, 1.0, 1.0, 0.3, -0.1))
```

All three geometries share these eight arguments. AX ignores V and VT ignores eta. FULL is independent of theta. Reverse both V and eta when translating manuscript geometric amplitudes into code inputs. Unlike Paper01's independent torus radii, epsilon specifies the volume-preserving path and no R2/R3 substitution is needed.

`get_potential_decomposition()` returns `r^3`, `r^2`, `r^1`, `r^0` and `total`. It has no separate inverse-radius entry: that term remains in `total`. For example, obtain its coefficient with `expand(engine.data['potential']).coeff(engine.data['params']['r'], -1)`. Retain this term when LC-Weyl is nonzero; do not reconstruct the general potential from the four polynomial entries alone.

## 7. Radius and Shape Classification

E4.14 logs the radial derivative; `equilibria` remains empty. Classification uses the public API shared by the scan and viewer:

```python
from dppu.scanning import classify_configuration

result = classify_configuration('Nil3', V=4, eta=-2, alpha=-1, epsilon=0)
print(result['global_class'])  # UNATTAINED_INFIMUM
print(result['radial_class'])  # FINITE_MINIMUM
```

`global_*` covers all r>0 and x>0 at fixed torsion, L and kappa; `radial_*` covers all r>0 at the specified epsilon. Finite minima, unattained infima, degenerate minima and unboundedness are separate outcomes. TT/REE permit curve exploration, but complete-NY classification does not apply. See [CLASSIFICATION](CLASSIFICATION.md) for arguments, CSV fields and numerical ranges.

Do not round inputs, snap nonzero values to zero or discard roots outside a plot window. Fixed-shape analytic formulas use 80-digit Decimal arithmetic. Numerical uncertainty and values outside the float range are flagged; no interval guarantee for arbitrary inputs is asserted. Proofs are in Sections 5–8 and the radial criterion is in Appendix B.

## 8. Runtime and Reproduction

Public dependencies are in [requirements](../requirements.txt). The current engine and classifier do not require SciPy. Notebooks use ipywidgets and ipympl. After changing formulas or conventions, use new output/checkpoint locations and restart kernels. Runner checkpoint saving is explicit; `engine.run()` does not automatically load old checkpoints.

Separate [figure rendering and recomputation](../README.md), and do not treat earlier outputs as current results. The paper and appendices contain the scientific arguments. External work tools are not dependencies of public computations.

## Curvature selection

E4.8a selects the quadratic tensor after the EC curvature calculation. E4.11 consumes quadratic_scalar. The earlier weyl_scalar and weyl_tensor keys remain LC reference aliases; they do not identify the selected action. See [model definitions and API](WEYL_MODELS.md).
