# CONVENTIONS — DPPUv2 Engine Geometric Conventions

EC denotes Einstein–Cartan, LC denotes Levi-Civita, and NY denotes Nieh–Yan.


Identifiers such as E4.3 and E4.8a are public computation/checkpoint steps. Their functions are described alongside the IDs; they are not research phases.


This document fixes the **geometric, index, and sign conventions** shared between Paper02 `dppu.engine.pipeline.BaseFrameEngine` and its topology runners.
**All runners must define `metric_frame` and `structure_constants` according to these conventions.**

⇒ [日本語版](CONVENTIONS_ja.md) | [SymPy guideline](SymPy_guideline.md)

## 1. Scope and Assumptions

* All quantities treated here are expressed as components on a **Frame (Orthonormal Basis)**.
* `metric_frame` is the frame metric $`(g_{ab})`$, which defaults to $`(g_{ab}=\delta_{ab})`$ (`Matrix.eye(dim)`).
* The curvature component calculation in the DPPUv2 engine currently assumes a situation where **frame directional derivatives are unnecessary**.
  Specifically, the runner must adopt a setting where structure constants $`(C^{a}{}_{bc})`$ and connection coefficients $`(\Gamma^{a}{}_{bc})`$ are treated as "constants with respect to the frame" (e.g., left-invariant frames).
  * **Note:** This design is **rational and efficient** for handling homogeneous spaces like $S^3 \times S^1$ (Lie groups) or Nil manifolds. However, note that this assumption may become a bottleneck if handling general curved spacetimes with low symmetry in the future.

## 2. Indices and Array Index Order

Array storage is fixed as follows:

* Structure constants: `C[a,b,c] = C^a_{bc}`
* Connection coefficients: `Gamma[a,b,c] = Γ^a_{bc}`
* Riemann curvature: `Riemann[a,b,c,d] = R^a_{bcd}`

Meaning of indices:

* $(a)$: Output (superscript) component
* $(b,c,d)$: Input (subscript) components
  In particular, $`(\Gamma^{a}{}_{bc})`$ corresponds to $`(\nabla_{E_{c}} E_{b} = \Gamma^{a}{}_{bc} E_{a})`$ (the last index $(c)$ is the "direction of differentiation").

## 3. Definitions of Frame, Coframe, and Structure Constants (Most Important)

Let the dual of the frame be $`(\{E_{a}\})`$ and the coframe (1-forms) be $`(\{e^a\})`$.

### 3.1 Structure Equations of Coframe (Fixed)

$$
de^a = \frac12 C^a{}_{bc} e^b\wedge e^c,
\qquad C^a{}_{bc} = - C^a{}_{cb}.
$$

### 3.2 Commutation Relations of Dual Frame (Equivalent)

The above definition is equivalent to:

$$
[E_{b}, E_{c}] = - C^{a}{}_{bc} E_{a}.
$$

> Note: Many textbooks adopt $`([E_{b},E_{c}]=+f^{a}{}_{bc}E_{a})`$.
> This project adopts the convention **$`(C^{a}{}_{bc}=-f^{a}{}_{bc})`$ relative to that $`(f^{a}{}_{bc})`$**.

### 3.3 Runner Implementation Rules (Recommended)

* Match each stored C to the exterior derivative of the stated coframe. Section 9 gives the Paper02 components.
* At a minimum, automatically check that $`C^a_{bc}`$ is **antisymmetric in b,c**.

## 4. Connection (Spin Connection) and Metric Compatibility

Define the connection 1-form as:

$$
\omega^{a}{}_{b} = \Gamma^{a}{}_{bc} e^c
$$

Metric compatibility (Lorentz connection / Orthogonal connection) is fixed as a specification:

$$
\omega_{ab} = -\omega_{ba}
\quad(\Leftrightarrow\quad
\Gamma_{abc} = -\Gamma_{bac})
$$

where $`(\Gamma_{abc} = g_{ad}\Gamma^d{}_{bc})`$.

## 5. Levi-Civita Connection (General Koszul Implementation in DPPUv2 Engine)

When the frame is orthonormal and the above structure constant conventions are adopted, the Levi-Civita connection is calculated in the DPPUv2 engine using the following **General Koszul Formula**:

$$
\Gamma^a{}_{bc}
= \frac12\Big(
C^a{}_{bc} + C^c{}_{ba} - C^b{}_{ac}
\Big).
$$

(This is the form when the sign of the commutation relation in Section 3.2 is adopted.)

**Important Notes:**

1. This formula **does not assume a bi-invariant metric**.
   It functions correctly as the Levi-Civita connection on left-invariant frames, even for non-bi-invariant cases like Nil³.

2. In special cases where structure constants are totally antisymmetric in lower indices $`C_{abc} = -C_{bac} = -C_{acb}`$ (as on round SU(2)),
   this formula reduces to $`\Gamma^a_{bc} = \frac{1}{2} C^a_{bc}`$.

3. E4.3 calls the metric-compatibility checker. It returns a flag and violation list and logs the result; this call site does not automatically turn a failure into an exception. Check the return value when extending a runner. The strict Riemann checker raises for unproved residuals as well as violations.

## 6. Torsion and Curvature

Torsion 2-form:

$$
T^a = de^a + \omega^{a}{}_{b} \wedge e^b,
\qquad
T^a = \frac12 T^{a}{}_{bc} e^b\wedge e^c.
$$

Curvature 2-form:

$$
R^{a}{}_{b} = d\omega^a{}_{b} + \omega^a{}_{c}\wedge \omega^c{}_{b},
\qquad
R^{a}{}_{b} = \frac12 R^{a}{}_{bcd} e^c\wedge e^d.
$$

### 6.1 Input array and geometric torsion

`torsion_tensor` stores the input parameter array tau. The geometric components are
`T_geom[a,b,c] = C[a,b,c] + Gamma[a,c,b] - Gamma[a,b,c] = -tau[a,b,c]`.
Paper02 stores the input tau; reconstruct geometric torsion with this equation. The contortion formula is
`K[a,b,c]=(tau[a,b,c]+tau[b,c,a]-tau[c,a,b])/2`.

### 6.2 Nieh–Yan density

For Euclidean frame metric and epsilon(0,1,2,3)=+1, the component contractions are
`N_TT=epsilon*T*T/4`, `N_REE=epsilon*R/2`, and `N_FULL=N_TT-N_REE`.
REE denotes the diagnostic action term `+theta*N_REE`.
For the static homogeneous ansatz of the three runners,
`TT=REE=-4*V*eta/r` (using the common positive scale `r`), hence `FULL=0`.

## 7. Curvature Component Formula (Form used by Engine)

The DPPUv2 engine currently uses the following form for $`R^a_{bcd}`$:

$$
R^{a}{}_{bcd} = \Gamma^{a}{}_{ec}\Gamma^{e}{}_{bd}-\Gamma^{a}{}_{ed}\Gamma^{e}{}_{bc}+\Gamma^{a}{}_{be} C^{e}{}_{cd}.
$$

> Important: Generally, a frame directional derivative term
> $`(E_{c}(\Gamma^{a}{}_{bd}) - E_{d}(\Gamma^{a}{}_{bc}))`$
> appears here, but the DPPUv2 engine does not explicitly handle it.
> Therefore, the runner must adopt a setting where **$(\Gamma)$ is treated as constant in the frame direction**, such as with left-invariant frames.

## 8. Mandatory Self-Checks (Consistency the Runner Must Satisfy)

The runner must satisfy the following (failure implies definition inconsistency with the engine):

1. Antisymmetry of Structure Constants:

$$
C^{a}{}_{bc} + C^{a}{}_{cb} = 0.
$$

2. Metric Compatibility (Orthogonal Connection):

$$
\omega_{ab} + \omega_{ba} = 0.
$$

3. Antisymmetry of Riemann (Target of engine's strict check):

$$
R_{ab cd} = -R_{ba cd},\qquad
R_{ab cd} = -R_{ab dc}.
$$

## 9. Global Geometry and Integration Domains

### 9.1 Volume-preserving shape and common scale

All three geometries use radius scale r, circle circumference L and positive kappa. Introduce shape by this coframe. The three spatial factors multiply to one, so epsilon does not change the volume.

$$
\begin{aligned}
s&=1+\epsilon>0,\qquad x=s^{-2/3}>0,\\
e^0&=r s^{1/3}\sigma^0,\qquad e^1=r s^{1/3}\sigma^1,\\
e^2&=r s^{-2/3}\sigma^2,\qquad e^3=L\thinspace du,\qquad u\in[0,1).
\end{aligned}
$$

$$
\begin{aligned}
de^0&=n_{0} e^1\wedge e^2,\quad de^1=n_{1} e^2\wedge e^0,\quad de^2=n_{2} e^0\wedge e^1,\quad de^3=0,\\
(n_{0},n_{1},n_{2})_{S^3}&=r^{-1}(4/x,4/x,4x^2),\\
(n_{0},n_{1},n_{2})_{T^3}&=(0,0,0),\qquad (n_{0},n_{1},n_{2})_{\mathrm{Nil}^3}=r^{-1}(0,0,-x^2).
\end{aligned}
$$

### 9.2 Spherical SU(2)

The round physical radius is r/2. Fix the SU(2) coframe by

$$
\begin{aligned}
\lambda^0&=\cos\psi\thinspace d\vartheta+\sin\psi\sin\vartheta\thinspace d\varphi,\\
\lambda^1&=-\sin\psi\thinspace d\vartheta+\cos\psi\sin\vartheta\thinspace d\varphi,\\
\lambda^2&=d\psi+\cos\vartheta\thinspace d\varphi,\qquad \sigma^i=-\lambda^i/4.
\end{aligned}
$$

The domain is $0\le\vartheta\le\pi$, $0\le\varphi<2\pi$, $0\le\psi<4\pi$, with polar degeneracies and boundary identification $(\varphi+2\pi,\psi)\sim(\varphi,\psi+2\pi)$. The positive volume density is $r^3\sin\vartheta/64$. The coframe orientation is opposite to $d\vartheta\wedge d\varphi\wedge d\psi$; the orientation convention is $`e^0\wedge e^1\wedge e^2\wedge e^3>0`$.

### 9.3 Torus

Take $`\sigma^i=dy^i`$ with each angle of period $2\pi$. The circumferences are $`2\pi r s^{1/3},2\pi r s^{1/3},2\pi r s^{-2/3}`$. Paper02 uses a common r and volume-preserving shape. The radius and shape specify this volume-preserving path; independent directional radii are not required.

### 9.4 Fixed compact Nil quotient

Specify the left quotient of the Heisenberg group by

$$
\begin{aligned}
\sigma^0&=dy^0,\qquad \sigma^1=dy^1,\qquad \sigma^2=dz-y^0\thinspace dy^1,\\
(y^0,y^1,z)&\sim(y^0+2\pi,y^1,z+2\pi y^1),\\
(y^0,y^1,z)&\sim(y^0,y^1+2\pi,z),\\
(y^0,y^1,z)&\sim(y^0,y^1,z+4\pi^2).
\end{aligned}
$$

The fundamental domain is [0,2pi)×[0,2pi)×[0,4pi²). The horizontal commutator equals the central period 4pi². Hold the lattice and quotient fixed when varying r and shape; do not replace the central period by 2pi.

### 9.5 Volume, input dictionary and variation

$$
\mathrm{Vol}_{4}=c_{M} Lr^3,\qquad
c_{S^3}=\frac{\pi^2}{4},\quad c_{T^3}=(2\pi)^3,\quad c_{\mathrm{Nil}^3}=(2\pi)^4.
$$

The signed manuscript amplitudes satisfy $`(\eta,V)=(-\eta_{\tau},-V_{\tau})`$. The positive-symbol assumption for code V maps to negative manuscript V; interval endpoints change signs and order. Numerical APIs accept signed real inputs. The spherical physical-radius conversion does not silently redefine torsion amplitudes.

The Nil engine's `params['R']` and `params['r']` denote the same symbol. The public callable's first argument is the common radius scale. Torsion amplitudes, L and kappa are held fixed: fixed eta differs from fixed 2eta/r. See [classification](CLASSIFICATION.md) for the joint and fixed-shape domains.

## 10. Curvature-Squared Terms and Reduced Action

The main term is irreducible EC-Weyl; LC is a reference and EC_TRACEFREE (Ricci-tracefree EC curvature) a different action. See [curvature models](WEYL_MODELS.md). The formulas below are shared by the irreducible EC-Weyl and LC-Weyl actions on the stated static family. Alpha is separate from shape.

$$
\begin{aligned}
f(x)&=4x-x^4,\\
R_{\mathrm{LC},S^3}&=\frac{8f(x)}{r^2},& C^2_{\mathrm{LC},S^3}&=\frac{1024x^2(1-x^3)^2}{3r^4},\\
R_{\mathrm{LC},T^3}&=0,&C^2_{\mathrm{LC},T^3}&=0,\\
R_{\mathrm{LC},\mathrm{Nil}^3}&=-\frac{x^4}{2r^2},&C^2_{\mathrm{LC},\mathrm{Nil}^3}&=\frac{4x^8}{3r^4},\\
R_{\mathrm{EC}}&=R_{\mathrm{LC}}-\frac{6\eta^2}{r^2}-\frac23 V^2.
\end{aligned}
$$

$$
S=\int\left[\left(\frac{R_{\mathrm{EC}}}{2\kappa^2}+\alpha I_{\mathrm{W}}\right)\mathrm{vol}_{4}+\theta N\right],
\qquad U=-S\big|_{\mathrm{family}}.
$$

Here $N$ is the NY four-form; its scalar coefficient is `N_FULL` from Section 6. $`I_{\mathrm{W}}`$ is the squared norm of irreducible EC-Weyl curvature.

LC-Weyl vanishes on the round sphere and throughout the torus, and is nonzero at finite Nil shape. Sections 5–8 prove the nonpositive-alpha spherical shape bound, positive-alpha small-radius unboundedness, and the distinction between Nil radial and joint minima. Minima of U do not classify full-field vacua or Lorentzian ghosts.

## 11. Form-Index Hodge Duality and Curvature Norms

With orientation epsilon0123=+1 and Euclidean metric, dualize the last, form-index pair:

$$
\begin{aligned}
(*R)_{abcd}&=\frac12\varepsilon_{cdef}R_{abef},\\
\mathcal P\thinspace\mathrm{vol}_{4}&=\sum_{a,b}R_{ab}\wedge R_{ab},\qquad
\mathcal P=\frac14\varepsilon^{cdef}R_{abcd}R_{abef},\\
E_{\mathrm{all}}&=\sum_{a,b,c,d}R_{abcd}^2,\qquad
P_{\mathrm{all}}=\sum_{a,b,c,d}R_{abcd}(*R)_{abcd}=2\mathcal P.
\end{aligned}
$$

Distinguish this from internal-index duality. E_all is a curvature norm, not Euler density. Earlier numerical names E_RR and P_RstarR correspond to E_all and P_all. These normalizations are defined in Section 3 and Appendix C independently of any numerical diagnostic API. The public symbolic supplement independently verifies the spatial block structure and zero Pontryagin for the three geometries.

[LaTeX source](../../LaTeX/main.tex) / [Implementation guide](SymPy_guideline.md) / [Classification, CSV and viewer](CLASSIFICATION.md)
