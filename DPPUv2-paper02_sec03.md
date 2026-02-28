## 3. Chiral Equilibrium: $P = 0$

本節では、 $M^3 \times S^1$ minisuperspace ansatz と EC 接続の下で、ポントリャーギン密度 $P = \langle R, *R \rangle$ が恒等的にゼロとなることを示す。これは paper01 の等方真空に対する位相的脅威——自己双対インスタントンを経由した真空崩壊——を、この ansatz の下で排除する。

### 3.1 ポントリャーギン密度と自己双対性

4次元ユークリッド多様体上で、ポントリャーギン密度は曲率2-形式 $R^{ab}$ の Hodge 双対 $*R^{ab}$ との内積として定義される:

$$P = \langle R, *R \rangle = \frac{1}{4}\varepsilon^{abcd}\, R_{abef}\, R_{cd}{}^{ef}$$

$P$ はトポロジカル不変量（Pontryagin class）の密度であり、自己双対性と以下の関係にある:

- $R = *R$（自己双対） $\Leftrightarrow$ $P = E > 0$
- $R = -*R$（反自己双対） $\Leftrightarrow$ $P = -E < 0$

ここで $E = \langle R, R \rangle = R_{abcd}R^{abcd}$ は Euler 密度（Gauss-Bonnet 密度）に関連するスカラーである。

自己双対（または反自己双対）インスタントン解が存在する場合、それは有限作用の極値を与え、量子力学的トンネル効果を通じた真空崩壊の経路となり得る。 $P \neq 0$ は自己双対性の必要条件であるため、 $P = 0$ は自己双対インスタントンの存在を排除する。

### 3.2 Proposition 1（カイラル均衡）

> **Proposition 1.** $M^3 \times S^1$ minisuperspace ansatz と Einstein-Cartan 接続の下で、ポントリャーギン密度は恒等的にゼロとなる:
>
> $$P = \langle R, *R \rangle = 0$$
>
> これは以下の全てに対して成り立つ代数的恒等式である:
> - $M^3$ の選択（ $S^3$, $T^3$, $Nil^3$）
> - Torsion mode（MX, AX, VT）
> - Nieh-Yan variant（FULL, TT, REE）
> - 全てのパラメータ値（ $r, L, \eta, V, \kappa, \theta_{\rm NY}$）

### 3.3 証明

#### Step 1: 2-形式の直交分解

$M^4 = M^3 \times S^1$ 上の座標を $(x^0, x^1, x^2, \tau)$ とする。2-形式の空間は直交する2つのブロックに分解される:

$$\Lambda^2(M^4) = \underbrace{\Lambda^2(M^3)}_{\text{Spatial block (S)}} \oplus \underbrace{\Lambda^1(M^3) \wedge d\tau}_{\text{Mixed block (M)}}$$

- **Spatial block (S)**: $M^3$ 方向のみの添字を持つ2-形式 $\{(01), (02), (12)\}$
- **Mixed block (M)**: $M^3$ と $S^1$ を混合する2-形式 $\{(03), (13), (23)\}$

#### Step 2: Hodge 双対はブロックを交換する

4次元 Hodge 双対（ $\varepsilon_{0123} = +1$）の作用は:

| Spatial → Mixed | Mixed → Spatial |
|---|---|
| $*(01) = +(23)$ | $*(03) = +(12)$ |
| $*(02) = -(13)$ | $*(13) = -(02)$ |
| $*(12) = +(03)$ | $*(23) = +(01)$ |

すなわち、Hodge 双対は Spatial ブロックと Mixed ブロックを（本稿の基底と分解では）交換する:

$$*: \Lambda^2(M^3) \leftrightarrow \Lambda^1(M^3) \wedge d\tau$$

#### Step 3: 曲率は Spatial ブロックにのみ成分を持つ

Minisuperspace ansatz の下で、EC 接続の曲率テンソル $R^{ab}{}_{cd}$ は、下添字 $(c, d)$ に関して:

- $(c, d) \in$ Spatial block: 非零成分を持つ
- $(c, d) \in$ Mixed block: この ansatz では現れない（ゼロ）

これは minisuperspace ansatz の帰結である。 $S^1$ 方向（ $\tau$）は Killing 方向であり、接続は空間的に一様であるため、曲率2-形式に $dx^i \wedge d\tau$ 成分（Mixed block）が現れない。

この性質は、 $S^3$, $T^3$, $Nil^3$ の全てのトポロジーに対して 記号計算ソフトウェア（symbolic computation）による代数的検証で確認されている（§3.5 参照）。

#### Step 4: 直交性により $P = 0$

$R$ の下添字が Spatial block にのみ属するため、 $*R$ の下添字は Mixed block にのみ属する（Step 2）。Spatial block と Mixed block は直交するため:

$$\langle R, *R \rangle = 0 \qquad \square$$

### 3.4 One-line proof

上記の証明を1行で要約すれば:

$$R \in \Lambda^2(M^3) \quad \Rightarrow \quad *R \in \Lambda^1(M^3) \wedge d\tau \quad \Rightarrow \quad \langle R, *R \rangle = 0$$

### 3.5 記号計算ソフトウェア による検証

記号計算ソフトウェアによる代数的検証により、3つのトポロジー全てで $P = 0$ が確認された。（代数的検証の詳細は Appendix C に記載）

| トポロジー | Spatial 成分 | Mixed 成分 | $P = \langle R, *R \rangle$ | 検証状況 |
|---|---|---|---|---|
| $S^3 \times S^1$ | 6 | 0 | $\mathbf{0}$ | $\checkmark$ |
| $T^3 \times S^1$ | 6 | 0 | $\mathbf{0}$ | $\checkmark$ |
| $Nil^3 \times S^1$ | 6 | 0 | $\mathbf{0}$ | $\checkmark$ |

$S^3 \times S^1$ の非零曲率成分（代表例）:

$$R^{01}{}_{01} = \frac{-V^2 r^2/9 - \eta^2 - 8\eta - 12}{r^2}, \qquad R^{03}{}_{12} = \frac{-2V(\eta + 4)}{3r}$$

本稿の成分計算では、非零成分の下添字 $(c, d)$ は $\{01, 02, 12\}$（Spatial block）に属しており、Mixed block には成分が現れない。

### 3.6 物理的解釈

#### 3.6.1 カイラル均衡

$P = 0$ は、曲率の自己双対成分と反自己双対成分が（本稿の分解の下で）規範的に釣り合っていることを意味する。曲率2-形式を自己双対/反自己双対分解すると:

$$R = R^+ + R^-, \qquad R^{\pm} = \frac{1}{2}(R \pm *R)$$

$P = \langle R, *R \rangle = \|R^+\|^2 - \|R^-\|^2$ であるから、本稿の枠組みにおいて $P = 0$ は:

$$\|R^+\| = \|R^-\|$$

を意味する。両方の「カイラリティ」が正確に等量存在する——これを本 minisuperspace の枠組みでは「カイラル均衡（chiral equilibrium）」と呼ぶ。

#### 3.6.2 自己双対インスタントンの構造的禁止

自己双対性 $R = *R$ は $R^- = 0$、すなわち $\|R^-\| = 0$ を要求する。 $P = 0$ により $\|R^+\| = \|R^-\|$ が成り立つため、 $\|R^-\| = 0$ であれば同時に $\|R^+\| = 0$、つまり $R = 0$ となる。

したがって、**曲率がゼロでない限り**、 $M^3 \times S^1$ minisuperspace では自己双対解は存在し得ない。反自己双対解についても同様である。

$S^3 \times S^1$ 等方真空は、本稿の ansatz の下で、自己双対インスタントンを経由したトンネル効果による崩壊の脅威から保護されている。この保護は特定のパラメータ値や torsion の配位に依存せず、 $M^3 \times S^1$ 積構造と minisuperspace ansatz から従う**幾何学的帰結**である。

### 3.7 $P = 0$ が成り立たなくなる条件

$P \neq 0$ を実現し、自己双対解を許容するためには、本研究の幾何学的設定を以下のいずれかの方向に拡張する必要がある:

| 拡張の方向 | 変更内容 | $P = 0$ が破れる理由 |
|---|---|---|
| 非等方 torsion | 位置依存の $T^a(x)$ | 均質性の破壊により Mixed block に曲率成分が出現 |
| 非積多様体 | $M^3 \times S^1$ 以外 | 積構造がブロック制限の原因 |
| Lorentz 署名 | $(-,+,+,+)$ | Hodge $*$ の固有空間構造が変化 |
| 非コンパクト $M^3$ | 非均質な幾何 | 曲率構造が異なり得る |

これらの拡張は将来的な課題として §9 で議論する。

