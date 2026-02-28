## Appendix C: Symbolic Computation Details

本付録では、Weyl スカラー $C^2(r, \varepsilon)$ および等方点での有効ポテンシャル $V_{\rm EC}(r, 0)$ の SymPy による導出ステップを記述する。

### C.1 $C^2(r, \varepsilon)$ の導出

#### C.1.1 入力: Squashed 構造定数

Squashed $S^3$ の構造定数（§2.3）:

$$C^i{}_{jk}(\varepsilon) = \frac{4}{r}\,\varepsilon_{ijk} \times f_i(\varepsilon)$$

$$f_0 = f_1 = (1+\varepsilon)^{1/3} \times (1+\varepsilon)^{1/3} = (1+\varepsilon)^{2/3}$$

$$f_2 = (1+\varepsilon)^{-2/3} \times (1+\varepsilon)^{-2/3} = (1+\varepsilon)^{-4/3}$$

（因子 $f_i$ は正規直交フレーム $e^a = r\, f_a^{1/2}(\varepsilon)\, \sigma^a$ の squashing に由来する。）

#### C.1.2 Step 1: Levi-Civita 接続

Koszul 公式:

$$\Gamma^a{}_{bc} = \frac{1}{2}\left(C^a{}_{bc} + C^c{}_{ba} - C^b{}_{ac}\right)$$

SymPy により非零成分を列挙。 $\varepsilon = 0$ では paper01 の A.2.1 の結果に帰着することを確認。

#### C.1.3 Step 2: Riemann テンソル

フレーム基底での曲率テンソル:

$$R^a{}_{bcd} = \Gamma^a{}_{ec}\,\Gamma^e{}_{bd} - \Gamma^a{}_{ed}\,\Gamma^e{}_{bc} + \Gamma^a{}_{be}\,C^e{}_{cd}$$

第3項はフレーム基底特有の寄与（座標基底の $\partial\Gamma$ 項に対応）。SymPy により全 $4^4 = 256$ 成分を計算し、反対称性 $R_{abcd} = -R_{abdc}$, $R_{abcd} = -R_{bacd}$ を自動検証。

#### C.1.4 Step 3: Ricci テンソル・スカラー

$$R_{bd} = R^a{}_{bad}, \qquad R = R^a{}_a = R_{bb}$$

Levi-Civita 接続の Ricci スカラー:

$$R_{\rm LC}(r, \varepsilon) = \frac{8\left(4(1+\varepsilon)^2 - 1\right)}{r^2\,(1+\varepsilon)^{8/3}}$$

等方点での値: $R_{\rm LC}(r, 0) = 24/r^2$（ $S^3$ の標準値と整合）。

#### C.1.5 Step 4: Weyl テンソル

4次元 Weyl テンソルの定義式:

$$C_{abcd} = R_{abcd} - \frac{1}{2}\left(g_{ac}R_{bd} - g_{ad}R_{bc} - g_{bc}R_{ad} + g_{bd}R_{ac}\right) + \frac{R}{6}\left(g_{ac}g_{bd} - g_{ad}g_{bc}\right)$$

正規直交フレーム（ $g_{ab} = \delta_{ab}$）での計算。SymPy により全 $\binom{4}{2}^2 = 36$ 独立成分を計算。

#### C.1.6 Step 5: Weyl スカラー

$$C^2 = C_{abcd}\,C^{abcd} = \sum_{a,b,c,d} C_{abcd}^2$$

SymPy の `simplify` と `factor` を適用:

$$\boxed{C^2(r, \varepsilon) = \frac{1024\,\varepsilon^2(\varepsilon+2)^2}{3\,r^4\,(1+\varepsilon)^{16/3}}}$$

### C.2 Weyl テンソル非零成分の完全一覧

全24個の非零成分は、共通因子 $\varepsilon(\varepsilon+2) / [r^2(1+\varepsilon)^{8/3}]$ を持つ。

#### 対角型（ $C_{abab}$ 型）

| 成分 | 値 |
|---|---|
| $C_{0101}$ | $+\dfrac{16\,\varepsilon(\varepsilon+2)}{3r^2(1+\varepsilon)^{8/3}}$ |
| $C_{0202}$ | $-\dfrac{8\,\varepsilon(\varepsilon+2)}{3r^2(1+\varepsilon)^{8/3}}$ |
| $C_{0303}$ | $-\dfrac{8\,\varepsilon(\varepsilon+2)}{3r^2(1+\varepsilon)^{8/3}}$ |
| $C_{1212}$ | $-\dfrac{8\,\varepsilon(\varepsilon+2)}{3r^2(1+\varepsilon)^{8/3}}$ |
| $C_{1313}$ | $-\dfrac{8\,\varepsilon(\varepsilon+2)}{3r^2(1+\varepsilon)^{8/3}}$ |
| $C_{2323}$ | $+\dfrac{16\,\varepsilon(\varepsilon+2)}{3r^2(1+\varepsilon)^{8/3}}$ |

#### 交差型

Weyl テンソルの対称性 $C_{abcd} = C_{cdab}$, $C_{abcd} = -C_{abdc} = -C_{bacd}$ により、対角型成分から全ての非零成分が生成される。独立成分は上記6個であり、添字の対称性により残りの18個が定まる。

#### トレースレス条件の検証

$$C^a{}_{bac} = 0 \qquad (\forall\, b, c)$$

SymPy により全てのトレースがゼロであることを確認。

### C.3 $V_{\rm EC}(r, 0)$ の完全な記号式

EC エンジン（`S3S1Engine`, MX mode, FULL variant）による等方点 $\varepsilon = 0$ での有効ポテンシャル:

$$V_{\rm EC}(r, 0) = \frac{2\pi^2 L r}{3\kappa^2}\left(V^2 r^2 + 6V\eta\kappa^2 r\,\theta_{\rm NY} + 9\eta^2 - 36\right)$$

参照パラメータ $(V=4, \eta=-2, \theta_{\rm NY}=1, \kappa=1, L=1)$ の代入:

$$V_{\rm EC}(r, 0) = \frac{2\pi^2}{3} \cdot r \cdot \left(16r^2 - 48r + 0\right) = \frac{32\pi^2}{3}\,r^2(r - 3)$$

この3次多項式（ $r$ について）の極小:

$$\frac{dV_{\rm EC}}{dr} = \frac{32\pi^2}{3}\left(3r^2 - 6r\right) = \frac{32\pi^2}{3} \cdot 3r(r - 2) = 0$$

$r^* = 2$（ $r = 0$ は自明解）。

$$V_{\rm EC}(2, 0) = \frac{32\pi^2}{3} \cdot 4 \cdot (2 - 3) = -\frac{128\pi^2}{3} \approx -421.1$$

### C.4 $C^2 \cdot \mathrm{Vol}$ の閉じた式

Weyl スカラーと体積の積:

$$C^2(r, \varepsilon) \cdot \mathrm{Vol}(r) = \frac{1024\,\varepsilon^2(\varepsilon+2)^2}{3\,r^4\,(1+\varepsilon)^{16/3}} \times 2\pi^2 L r^3 = \frac{2048\pi^2 L\,\varepsilon^2(\varepsilon+2)^2}{3\,r\,(1+\varepsilon)^{16/3}}$$

$r \to 0$ でのスケーリング: $C^2 \cdot \mathrm{Vol} \sim 1/r$（発散）。

$\varepsilon \to -1$（ $\delta = 1 + \varepsilon \to 0^+$）でのスケーリング: $C^2 \cdot \mathrm{Vol} \sim 1/\delta^{16/3}$（発散）。

この二方向への非有界性が、Theorem 2 Part (a) の証明の数学的基盤である。

### C.5 検証スクリプト

上記の全計算は `scripts/proofs/analytical_proof.py` により再現可能である。スクリプトは以下を自動実行する:

1. Squashed 構造定数の設定
2. Levi-Civita 接続の計算
3. Riemann テンソルの計算と反対称性検証
4. Ricci テンソル・スカラーの計算
5. Weyl テンソルの計算とトレースレス条件の検証
6. $C^2$ の `simplify` + `factor`
7. $\varepsilon = 0$ での値の確認（ $C^2 = 0$）
8. $\varepsilon$ 方向の1次・2次微分の計算
9. $R_{\rm LC}$ の計算と既知値との比較
