## 4. Weyl Extension: Squashed Ansatz

本節では、§2 で導入した squashed ansatz の下で Weyl スカラー $C^2(r, \varepsilon)$ の閉じた式を導出し、有効ポテンシャルの構造を明らかにする。

### 4.1 Weyl テンソルの計算方法

Weyl テンソルは Levi-Civita 接続から以下の手順で計算する:

1. **Levi-Civita 接続**: 正規直交フレームでの一般化 Koszul 公式
   $$\Gamma^{a}{}\_{bc} = \frac{1}{2}\left(C^{a}{}\_{bc} + C^{c}{}\_{ba} - C^{b}{}\_{ac}\right)$$

2. **Riemann テンソル**: フレーム基底での曲率
   $$R^{a}{}\_{bcd} = \Gamma^{a}{}\_{ec}\Gamma^{e}{}\_{bd} - \Gamma^{a}{}\_{ed}\Gamma^{e}{}\_{bc} + \Gamma^{a}{}\_{be}C^{e}{}\_{cd}$$

3. **Ricci テンソル・スカラー**: $R_{bd} = R^a{}_{bad}$, $R = R^a{}_a$

4. **Weyl テンソル**: 4次元での定義
   $$C_{abcd} = R_{abcd} - \frac{1}{2}\left(g_{ac}R_{bd} - g_{ad}R_{bc} - g_{bc}R_{ad} + g_{bd}R_{ac}\right) + \frac{R}{6}\left(g_{ac}g_{bd} - g_{ad}g_{bc}\right)$$

5. **Weyl スカラー**: $C^2 = C_{abcd}C^{abcd}$（正規直交フレームなので $g^{ab} = \delta^{ab}$）

### 4.2 Lemma 1: Weyl スカラーの閉じた式

> **Lemma 1.** Squashed $S^3 \times S^1$ の Levi-Civita 接続に基づく4次元 Weyl スカラーは:
>
> $$C^2(r, \varepsilon) = \frac{1024\,\varepsilon^2(\varepsilon+2)^2}{3\,r^4\,(1+\varepsilon)^{16/3}}$$

**証明.** 記号計算ソフトウェアによる代数的導出。§4.1 の手順に従い、squashed 構造定数（§2.3）を入力として Weyl テンソルの全成分を計算し、二乗和を取った。`simplify` および `factor` により上記の閉じた式を得た。 $\square$

記号計算ソフトウェアによる代数的導出の全ステップは Appendix C に記載する。

### 4.3 Lemma 1 の主要な性質

Lemma 1 の式から、以下の性質が直ちに読み取れる:

#### (i) 等方点でのゼロ: $C^2(r, 0) = 0$

分子に $\varepsilon^2$ の因子があるため、 $\varepsilon = 0$ で $C^2 = 0$ となる。

**物理的解釈**: 等方 $S^3$ は3次元定曲率空間であり、共形的に平坦である。 $S^3 \times S^1$ の積計量は4次元で共形的に平坦であり、Weyl テンソルが恒等的に消滅する。

#### (ii) 非負性: $C^2(r, \varepsilon) \geq 0$ $(\varepsilon > -1)$

$C^2 = C_{abcd}C^{abcd}$ は正規直交フレームでの各成分の二乗和であるため、定義から非負。

$C^2 = 0$ となるのは $\varepsilon = 0$ のときのみ（ $\varepsilon = -2$ は $\varepsilon = -1$ の特異点を超えるため物理的に到達不能）。

#### (iii) 等方点での2次振る舞い

$$\frac{\partial C^2}{\partial\varepsilon}\bigg|_{\varepsilon=0} = 0, \qquad \frac{\partial^2 C^2}{\partial\varepsilon^2}\bigg|_{\varepsilon=0} = \frac{8192}{3r^4} > 0$$

$C^2$ は等方点で2次の極小を持ち、小さな異方性に対して $\varepsilon^2$ に比例して増加する:

$$C^2(r, \varepsilon) \approx \frac{8192}{3r^4}\,\varepsilon^2 \quad (|\varepsilon| \ll 1)$$

#### (iv) $r \to 0$ での発散

固定された $\varepsilon \neq 0$ に対して、 $C^2 \sim 1/r^4$ で発散する。体積 $\mathrm{Vol} = 2\pi^2 L r^3$ との積は:

$$C^2 \cdot \mathrm{Vol} = \frac{2048\pi^2 L\,\varepsilon^2(\varepsilon+2)^2}{3\,r\,(1+\varepsilon)^{16/3}} \sim \frac{1}{r} \quad (r \to 0)$$

この非有界性が §6 での不安定性の証明の鍵となる。

### 4.4 Weyl テンソルの非零成分の構造

一般の $\varepsilon$ において、24個の非零 Weyl テンソル成分が存在する。全てが共通の因子を持つ:

$$C_{abcd} \propto \frac{\varepsilon(\varepsilon+2)}{r^2\,(1+\varepsilon)^{8/3}}$$

代表的な非零成分:

| 成分 | 値 |
|---|---|
| $C_{0101}$ | $+\dfrac{16\,\varepsilon(\varepsilon+2)}{3r^2(1+\varepsilon)^{8/3}}$ |
| $C_{0202}$, $C_{0303}$ | $-\dfrac{8\,\varepsilon(\varepsilon+2)}{3r^2(1+\varepsilon)^{8/3}}$ |
| $C_{2323}$ | $+\dfrac{16\,\varepsilon(\varepsilon+2)}{3r^2(1+\varepsilon)^{8/3}}$ |
| $C_{1212}$, $C_{1313}$ | $-\dfrac{8\,\varepsilon(\varepsilon+2)}{3r^2(1+\varepsilon)^{8/3}}$ |

列挙した成分はいずれも $\varepsilon(\varepsilon+2)$ を因子として含むため、 $\varepsilon = 0$ で消滅する。全成分の一覧は Appendix C に記載する。

### 4.5 有効ポテンシャルの分離（再掲）

§2.5 で導入した有効ポテンシャルの分離を、Lemma 1 の結果を用いて具体化する:

$$V_{\rm eff}(r, \varepsilon; \alpha) = V_{\rm EC}(r, \varepsilon) - \alpha \cdot \frac{2048\pi^2 L\,\varepsilon^2(\varepsilon+2)^2}{3\,r\,(1+\varepsilon)^{16/3}}$$

$\alpha$ の符号に応じた Weyl 項の効果:

| $\alpha$ の符号 | Weyl 項 $-\alpha C^2 \cdot \mathrm{Vol}$ | $\varepsilon \neq 0$ への効果 |
|---|---|---|
| $\alpha = 0$ | $0$ | 影響なし（paper01 と同等） |
| $\alpha < 0$ | $+\|\alpha\| C^2 \cdot \mathrm{Vol} > 0$ | 正のペナルティ（等方性を安定化） |
| $\alpha > 0$ | $-\alpha C^2 \cdot \mathrm{Vol} < 0$ | 負の報酬（異方性を促進） |

### 4.6 $(r, \varepsilon)$ 平面の有効ポテンシャル等高線図

![$(r, \varepsilon)$ 平面における $V_{\rm eff}$ の等高線図](LaTeX/figures/fig02_landscape.png)

> **[Fig. 2]** $(r, \varepsilon)$ 平面における $V_{\rm eff}$ の等高線図（ $S^3$:  $\alpha = -10, 0, +10$）


Fig. 2 は、 $\alpha$ の符号による安定性の劇的な変化を視覚的に示す。 $\alpha \leq 0$ では等方真空（ $\varepsilon = 0$）が安定な谷底を形成する一方、 $\alpha > 0$ では谷が消失し、ポテンシャル地形が崩壊する。この定性的な変化の解析的基盤を §5 と §6 で示す。
