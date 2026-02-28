## 10. Conclusion

本論文では、paper01 で確立された Einstein-Cartan + Nieh-Yan minisuperspace の $S^3 \times S^1$ 等方真空に対し、位相的および力学的に独立な2つの拡張を行い、その頑健性（Robustness）を解析的・数値的に示した。

### 10.1 主要結果の要約

本論文の主要結果は以下の4つの命題・定理に集約される:

#### (1) Proposition 1（カイラル均衡 $P = 0$）

$M^3 \times S^1$ minisuperspace + EC 接続の下で、ポントリャーギン密度 $P = \langle R, *R \rangle = 0$ が恒等的にゼロとなることを示した。2-形式の直交分解 $\Lambda^2(M^4) = \Lambda^2(M^3) \oplus \Lambda^1(M^3) \wedge d\tau$ と Hodge 双対のブロック交換性から、曲率が Spatial block にのみ属するとき $P = 0$ が代数的恒等式として従う。

この結果は、本稿の枠組みでは自己双対インスタントンが許されないことを意味し、インスタントンを経由した量子トンネル効果による真空崩壊の脅威を除去する。

#### (2) Theorem 1（等方真空の Weyl 安定性）

$\alpha \leq 0$ において、 $S^3 \times S^1$ の等方真空は共形的平坦性（ $C^2 = 0$）により Weyl 項の影響を受けず、paper01 の大域的極小が保護されることを示した。数値的には、全201点（ $\alpha \in [-1, 1]$）で $V_{\rm min} = -421.103$（11桁精度で一致）、 $r^* = 2.000$、 $\varepsilon^* = 0$ が $\alpha$ 非依存で維持されることを確認した。

#### (3) Theorem 2（ $\alpha > 0$ の非有界不安定性）

$\alpha > 0$ において、Weyl 項の $r \to 0$ での漸近的支配（ $V_{\rm Weyl} \sim -\alpha/r$ vs $V_{\rm EC} \sim r$）により、有効ポテンシャルが下に非有界（ $\inf V_{\rm eff} = -\infty$）となることを示した。 $\alpha = 0$ が安定性と不安定性を分ける正確な境界であることは、 $C^2 \cdot \mathrm{Vol}$ の非有界性に起因する。

#### (4) Theorem 3（安定性境界のパラメータ独立性）

（本稿の枠内で） $\alpha = 0$ の安定性境界が paper01 パラメータ $(V, \eta, \theta_{\rm NY})$ に依存しないことを示した。これは $C^2$ が純粋に幾何学的な量であり、paper01 パラメータと構造的に分離（Geometric Decoupling）していることに起因する。解析的議論に加え、代表点（Type I 中心、I/II 境界、Type II 中心、II/III 境界の4点）でのパラメータスキャンにて一貫性を確認した。

### 10.2 Weyl 結合定数の符号制約

Theorem 2-3 の結果は、EC+NY+Weyl 理論における Weyl 結合定数の符号制約 $\alpha \leq 0$ を導く。 $\alpha > 0$ はゴースト不安定性（Ostrogradsky の定理の minisuperspace 版）を引き起こし、理論の整合性から排除される。 $\alpha < 0$ は等方性の安定化と $r \to 0$ での斥力芯（正則化）を提供し、物理的に有利である。この制約は paper01 パラメータの調整に依存しない。

### 10.3 トポロジー選択原理の保存

3つのトポロジー（ $S^3$, $T^3$, $Nil^3$）の系統的比較により、paper01 のトポロジー選択原理—— $S^3$ が最低エネルギー真空を形成する——が $\alpha \leq 0$ の Weyl 拡張下で保存されることを確認した。 $S^3$ は $\varepsilon^* = 0$ で厳密に $C^2 = 0$ を達成し安定な等方真空を形成する。 $Nil^3$ は安定な異方真空を持たず、構造定数が消失するフラット極限（ $\varepsilon \to \infty$）に漸近するが、漸近 $V_{\rm min} \approx 5 > 0$ であり $S^3$ に対してエネルギー的に不利である。


