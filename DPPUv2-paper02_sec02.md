## 2. Framework

本節では、paper01 の EC+NY 理論に Weyl 二乗項を加えた拡張ラグランジアンを定式化し、異方性パラメータ $\varepsilon$ を含む squashed ansatz を導入する。

### 2.1 EC+NY+Weyl ラグランジアン

本論文で扱う拡張ラグランジアンは以下の通りである:

$$\mathcal{L} = \frac{R_{\rm EC}}{2\kappa^2} + \theta_{\rm NY}\, N + \alpha\, C^2$$

各項の意味は以下の通り:

- **$R_{\rm EC}/(2\kappa^2)$**: Einstein-Cartan 接続（トーション含む）による Ricci スカラー。 $\kappa$ は重力結合定数。
- **$\theta_{\rm NY}\, N$**: Nieh-Yan 項。 $N = d(e^a \wedge T_a)$ は Nieh-Yan 密度（4-形式）、 $\theta_{\rm NY}$ はその結合定数。paper01 [1] で導入された記法を踏襲する。
- **$\alpha\, C^2$**: Weyl 二乗項。 $C^2 = C_{abcd}C^{abcd}$ は Weyl テンソルの Kretschner 型スカラー（Levi-Civita 接続から計算）。 $\alpha$ は無次元結合定数。

Weyl テンソルは Levi-Civita 接続から定義する。これは、EC 接続から構成した Weyl テンソルではトーションの寄与が入り混じるため、一般には共形不変性が損なわれうることに基づく。一方、 $R_{\rm EC}$ と $N$ は EC 接続から計算する。

#### 符号規約

paper01 と同一の規約を採用する:

- Frame metric: $\eta_{ab} = \mathrm{diag}(+1, +1, +1, +1)$（ユークリッド署名）
- Riemann テンソル: $R^{a}{}\_{bcd} = \partial_c \Gamma^{a}{}\_{bd} - \partial_d \Gamma^{a}{}\_{bc} + \Gamma^{a}{}\_{ec}\Gamma^{e}{}\_{bd} - \Gamma^{a}{}\_{ed}\Gamma^{e}{}\_{bc}$
- Contortion: $K_{abc} = \frac{1}{2}(T_{abc} + T_{bca} - T_{cab})$（Hehl et al. 1976）[2]
- Levi-Civita 記号: $\varepsilon_{0123} = +1$

### 2.2 $M^3 \times S^1$ Minisuperspace Ansatz の復習

paper01 と同様に、4次元ユークリッド多様体を $\mathcal{M}_4 = \mathcal{M}_3 \times S^1$ に分解する。 $\mathcal{M}_3$ は左不変 coframe $\{\sigma^i\}$（ $i = 0, 1, 2$）を許容する3次元 Lie 群のコンパクト商である。 $S^1$ 方向の周長を $L$ とする。

paper01 では等方的な coframe $e^a = r\, \sigma^a$（ $a = 0, 1, 2$）、 $e^3 = L\, d\tau$ を用いた。ここで $r$ はスケール変数であり、当時の ansatz では有効ポテンシャル $V_{\rm eff}(r)$ の主たる引数であった。

### 2.3 Squashed Ansatz の導入

Weyl 項の効果を診断するためには、等方性からの変形を記述するパラメータが必要である。本論文では、 $S^3$ 上の軸対称な体積保存変形（squashing）を導入する:

$$e^0 = r\,(1+\varepsilon)^{1/3}\,\sigma^0, \quad e^1 = r\,(1+\varepsilon)^{1/3}\,\sigma^1, \quad e^2 = r\,(1+\varepsilon)^{-2/3}\,\sigma^2, \quad e^3 = L\,d\tau$$

ここで:

- **$r > 0$**: スケール変数（paper01 と同一）
- **$\varepsilon$**: 異方性パラメータ。 $\varepsilon = 0$ が等方点であり、 $\varepsilon > -1$ の範囲で物理的に有意
  - $\varepsilon > 0$: oblate 変形（ $e^0, e^1$ 方向に膨張、 $e^2$ 方向に収縮）
  - $\varepsilon < 0$: prolate 変形（ $e^2$ 方向に膨張、 $e^0, e^1$ 方向に収縮）
  - $\varepsilon = -1$: 特異点（1方向の完全縮退）

#### 体積の保存

Squashing 因子 $(1+\varepsilon)^{1/3} \times (1+\varepsilon)^{1/3} \times (1+\varepsilon)^{-2/3} = 1$ のため、体積は $\varepsilon$ に依存しない:

$$\mathrm{Vol}(\mathcal{M}_4) = 2\pi^2 L r^3 \quad (\varepsilon \text{非依存})$$

これは、 $\varepsilon$ が「形」のみを変え、「サイズ」（ $r$）を変えない変形パラメータであることを保証する。

#### Squashed 構造定数

Squashing により、 $S^3$ の構造定数は $\varepsilon$ 依存の因子を持つ:

$$C^i{}_{jk}(\varepsilon) = \frac{4}{r}\,\varepsilon_{ijk} \times f_i(\varepsilon)$$

ただし:

$$f_0(\varepsilon) = f_1(\varepsilon) = (1+\varepsilon)^{2/3}, \qquad f_2(\varepsilon) = (1+\varepsilon)^{-4/3}$$

等方点 $\varepsilon = 0$ では $f_0 = f_1 = f_2 = 1$ となり、paper01 の構造定数に帰着する。

### 2.4 記号の定義

本論文で用いる主要な記号を以下にまとめる:

| 記号 | 意味 | 走査範囲（数値計算） |
|---|---|---|
| $r$ | スケール変数 | $[0.01, 10]$ |
| $\varepsilon$ | 異方性パラメータ | $[-0.95, 5.0]$ |
| $\alpha$ | Weyl 結合定数 | $[-1, 1]$ |
| $V$ | ベクトル torsion 振幅 | 固定（ $V = 4$） |
| $\eta$ | 軸性 torsion 振幅 | 固定（ $\eta = -2$, ほか） |
| $\theta_{\rm NY}$ | Nieh-Yan 結合定数 | 固定（ $\theta_{\rm NY} = 1$） |
| $\kappa$ | 重力結合定数 | 固定（ $\kappa = 1$） |
| $L$ | $S^1$ 周長 | 固定（ $L = 1$） |

paper01 パラメータ $(V, \eta, \theta_{\rm NY})$ は §7 において走査するが、§4-6 では上記の参照値を用いる。

### 2.5 有効ポテンシャルの分離

Squashed ansatz の下で、有効ポテンシャルは以下のように $\alpha$ に関して**厳密に線形**に分離する:

$$V_{\rm eff}(r, \varepsilon; \alpha) = V_{\rm EC}(r, \varepsilon) - \alpha\, C^2(r, \varepsilon) \cdot \mathrm{Vol}(r)$$

ここで、Weyl 項の符号に注意されたい。ユークリッド署名における有効ポテンシャルは $V_{\rm eff} = -\mathcal{L} \times \mathrm{Vol}$ と定義されるため（Appendix A §A.2 参照）、ラグランジアン（§2.1）に $+\alpha C^2$ として現れる Weyl 項は、有効ポテンシャルでは $-\alpha C^2 \cdot \mathrm{Vol}$ と符号が反転して現れる。

各項の定義:

- **$V_{\rm EC}(r, \varepsilon)$**: EC+NY 部分の有効ポテンシャル。 $\alpha$ に依存しない。
  $$V_{\rm EC} = -\left(\frac{R_{\rm EC}}{2\kappa^2} + \theta_{\rm NY}\, N\right) \times \mathrm{Vol}$$

- **$C^2(r, \varepsilon) \cdot \mathrm{Vol}(r)$**: Weyl スカラーと体積の積。純粋に幾何学的な量であり、paper01 パラメータ $(V, \eta, \theta_{\rm NY})$ に依存しない。

この分離構造は、本論文の中心的な解析の基盤となる。特に:

1. $V_{\rm EC}$ は paper01 の結果をそのまま含む
2. $C^2 \cdot \mathrm{Vol}$ は幾何的量であり、torsion パラメータと独立
3. 本稿の範囲では、 $\alpha$ の符号により安定性が分類される

計算エンジン（DPPUv2 Engine v4）の詳細——Levi-Civita 接続の導出、EC 接続の構成、Weyl テンソルの計算手順——は Appendix A に記載する。
