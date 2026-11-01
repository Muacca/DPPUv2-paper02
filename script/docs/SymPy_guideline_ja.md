# SymPy 実装ガイドライン — Paper02

ECはEinstein–Cartan、LCはLevi-Civita、NYはNieh–Yanの略記です。


E4.3やE4.8aなどは公開計算・checkpointの段階IDであり、研究工程ではない。以下ではIDと処理内容を対応付けて説明する。


対象は公開engineを利用・拡張する読者。共通の幾何規約は[CONVENTIONS](CONVENTIONS_ja.md)、本文では第2〜4節と付録Aに記載する。計算は静的一様な3幾何のEC＋完全NY＋既約EC-Weyl作用を主とし、LCと別のRicciトレースなし作用も比較対象とする。

[English](SymPy_guideline.md) / [規約](CONVENTIONS_ja.md) / [分類仕様](CLASSIFICATION_ja.md)

## 1. 記号計算と簡約

係数はSymPyの整数と`Rational`を使い、記号計算へfloatを混ぜない。成分loop内の簡約を必要箇所へ集約し、式に応じて`factor`・`cancel`・`simplify`を選ぶ。`expand`は式を増大させる場合もあり、計算速度を一律には保証しない。

E4.12は一様密度に大域体積を掛ける。明示的な多重積分を導入する場合は、既知の積分と比較しながら中間式と所要時間を確認する。形状の領域はepsilon > -1である。正のsymbol xと`epsilon = x**Rational(-3, 2) - 1`への置換を使い、許容branchを保つ。無条件の`powdenest(force=True)`などで仮定を飛び越えない。

## 2. テンソル成分の実装指針

### Rule 2.1: フレーム成分を所定の添字順で扱う

エンジンはEuclidean計量 $`g_{ab}=\delta_{ab}`$ （`metric_frame`、既定は `Matrix.eye(dim)`）の正規直交フレームで計算する。このときフレーム添字の上げ下げは恒等操作であり、成分を直接用いてよい。ただし配列の位置は[CONVENTIONS 第2節](CONVENTIONS_ja.md)の順序に従う。

* `C[a,b,c]` $`=C^a{}_{bc}`$
* `Gamma[a,b,c]` $`=\Gamma^a{}_{bc}`$ 。最後の添字が微分方向
* `Riemann[a,b,c,d]` $`=R^a{}_{bcd}`$

非正規直交基底や別の計量では、全ての添字を計量で下げてから入れ替え、必要に応じて上げ直す。配列の転置だけでは添字操作にならない。

### Rule 2.2: 入力配列 $\tau$ と幾何学的捩率 $T$ を区別する

`torsion_tensor` には入力配列 $\tau$ を格納する。Cartan方程式から得られる幾何学的捩率は $T=-\tau$ であり、保存された入力配列と接続から再構成する。contortionのステップ `E4.5` はコードの式を $\tau$ に適用する。

```python
# Step E4.5: 入力配列tauのcontortion
for a in range(dim):
    for b in range(dim):
        for c in range(dim):
            val = (tau[a, b, c] + tau[b, c, a] - tau[c, a, b]) * Rational(1, 2)
```

幾何学的捩率で書くと、同じcontortionは $`K_{abc}[T]=-\frac12(T_{abc}+T_{bca}-T_{cab})`$ である（論文の式(D)）。配列と二つのパラメータを $`\tau=-T`$ 、 $`\eta_{\tau}=-\eta`$ 、 $`V_{\tau}=-V`$ と同時に変換する。 $K$ だけ、または一方の捩率パラメータだけの符号を反転しない。

### Rule 2.3: 構造係数を含む捩率の整合性検証

非座標フレームでは、捩率成分に構造係数が入る。

$$
T^a{}_{bc}=C^a{}_{bc}+\Gamma^a{}_{cb}-\Gamma^a{}_{bc}.
$$

EC接続を構築した後、これが $-\tau$ を再現し、ミスマッチが **0** であることを確認する。

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

`Gamma_EC[a,b,c] - Gamma_EC[a,c,b]` だけでは $C$ が抜ける。 $C\ne0$ の $S^3$ やNilでは有効な検証にならない。

### Rule 2.4: エンジン内蔵の検証

* E4.3は計量適合性検査を呼び、結果をログへ記録する。検査関数の返値は `(passed, violations)` であり、この呼出箇所は自動例外化しない。拡張時は `assert passed` などで判定を確認する。
* E4.3a（LC）とE4.7（EC）は $`R_{abcd}=-R_{bacd}`$ と $`R_{abcd}=-R_{abdc}`$ を `PROVED_ZERO`・`WITNESS_NONZERO`・`UNPROVED` の判定で検証する。証明されていない残差を零として扱わない。
* 捩率を持つ接続では、対交換 $`R_{abcd}=R_{cdab}`$ は要求しない（論文の式(P)）。

-----

## 3. エンジンが用いる規約

### 3.1 Torsionと曲率

捩率と曲率は2-formで定義し、 $`\omega^a{}_{b}=\Gamma^a{}_{bc}e^c`$ とする（[CONVENTIONS 第6節](CONVENTIONS_ja.md)）。

$$
\begin{aligned}
T^a&=de^a+\omega^a{}_{b}\wedge e^b=\frac12T^a{}_{bc}\thinspace e^b\wedge e^c,\\
R^a{}_{b}&=d\omega^a{}_{b}+\omega^a{}_{c}\wedge\omega^c{}_{b}=\frac12R^a{}_{bcd}\thinspace e^c\wedge e^d.
\end{aligned}
$$

### 3.2 接続

$$
\begin{aligned}
\Gamma^{\mathrm{EC}}_{abc}&=\Gamma^{\mathrm{LC}}_{abc}+K_{abc},\qquad
\Gamma^{\mathrm{LC}}_{abc}=\frac12\left(C_{abc}+C_{cba}-C_{bac}\right),\\
K_{abc}[T]&=-\frac12\left(T_{abc}+T_{bca}-T_{cab}\right)
=\frac12\left(\tau_{abc}+\tau_{bca}-\tau_{cab}\right).
\end{aligned}
$$

Levi–Civita部分は[CONVENTIONS 第5節](CONVENTIONS_ja.md)の一般Koszul公式であり、両側不変計量を仮定しない。

### 3.3 曲率成分

各runnerではフレーム成分が一定なので、ステップ `E4.7` は次の式を用いる。

$$
R^a{}_{bcd}=\Gamma^a{}_{ec}\Gamma^e{}_{bd}-\Gamma^a{}_{ed}\Gamma^e{}_{bc}+\Gamma^a{}_{be}C^e{}_{cd}.
$$

最後の項は非座標フレームの $de^c$ に由来し、省略してはならない（論文付録A）。

-----

## 4. Torsion Ansatz と Mode 分解規約

### 4.1 モード定義

| Mode | 入力成分 |
|---|---|
| `Mode.AX` | axial成分のみ（ $`V_{\tau}=0`$ ） |
| `Mode.VT` | vector-trace成分のみ（ $`\eta_{\tau}=0`$ ） |
| `Mode.MX` | 両成分 |

### 4.2 成分

ステップ `E4.4` は、runnerのパラメータ `eta` $`=\eta_{\tau}`$ 、`V` $`=V_{\tau}`$ とスケール `r` から入力配列を構成する。3幾何とも`params['r']`を用いる。Nilの内部symbol名Rも同じscaleを表す。

$$
\begin{aligned}
\tau^{\mathrm{ax}}_{ijk}&=\frac{2\eta_{\tau}}{r}\varepsilon_{ijk}\quad(i,j,k\in\lbrace 0,1,2\rbrace ),\\
\tau^{\mathrm{vec}}_{abc}&=\frac13\left(\delta_{ac}(V_{\tau})_{b}-\delta_{ab}(V_{\tau})_{c}\right),\qquad
(V_{\tau})_{a}=(0,0,0,V_{\tau}).
\end{aligned}
$$

幾何学的捩率 $T=-\tau$ は、 $`\eta=-\eta_{\tau}`$ 、 $`V=-V_{\tau}`$ として同じ形を持つ（論文の式(T)）。runnerはステップ `E4.1`〜`E4.2` で計量・構造定数・体積・パラメータを与え、捩率配列を自前で構成しない。

-----

## 5. Nieh–Yan 密度と作用のバリアント

### 5.1 密度

Euclideanフレームで $`\varepsilon_{0123}=+1`$ とし、ステップ `E4.10` は次を計算する。

$$
N_{\mathrm{TT}}=\frac14\varepsilon^{abcd}T^e{}_{ab}T_{ecd},\qquad
N_{\mathrm{REE}}=\frac12\varepsilon^{abcd}R_{abcd},\qquad
N_{\mathrm{FULL}}=N_{\mathrm{TT}}-N_{\mathrm{REE}}.
$$

TTの係数 $1/4$ は二つの捩率 2-formから、REEの係数 $1/2$ は一つの曲率2-formから生じる。 $`N_{\mathrm{TT}}`$ は捩率の二次式なので、 $\tau$ で評価しても同じ値になる。三つのrunnerのansatzでは

$$
N_{\mathrm{TT}}=N_{\mathrm{REE}}=-\frac{4V\eta}{r}=-\frac{4V_{\tau}\eta_{\tau}}{r},\qquad N_{\mathrm{FULL}}=0
$$

である。

### 5.2 バリアント選択

| `NyVariant` | ラグランジアンのNY項 | 役割 |
|---|---|---|
| `NyVariant.FULL` | $`\theta N_{\mathrm{FULL}}`$ | 完全NY作用 |
| `NyVariant.TT` | $`\theta N_{\mathrm{TT}}`$ | 診断用作用 |
| `NyVariant.REE` | $`+\theta N_{\mathrm{REE}}`$ | 正符号で加える診断用作用。FULLの負の成分ではない |

このansatzではTTとREEが同じポテンシャルを与える。それらの障壁や $\theta$ 依存性は、完全NY作用の結果ではない。

### 5.3 実装

`step_E4_10_nieh_yan_frame` は `ny_density_TT`・`ny_density_Ree`・`ny_density_full` を格納し、`BaseFrameEngine` の引数 `ny_variant` で採用する密度を選ぶ。

-----

## 6. 作用と縮約ポテンシャル

### 6.1 曲率二乗と作用

E4.3aはLC曲率・Ricci、E4.3bはLC-Weylテンソルとその二乗を構成する。E4.7でEC曲率を構成し、E4.8aで選択テンソルを射影してノルムIをquadratic_scalarへ保存する。E4.11〜E4.13は次の作用を評価する。

$$
\mathcal L=\frac{R_{\mathrm{EC}}}{2\kappa^2}+\theta N+\alpha I,
\qquad S=\mathcal L\thinspace\mathrm{Vol}_{4},\qquad U=-S.
$$

`total_volume`は各幾何の固定商と体積保存形状に対応する。保存キーは`riemann_LC`、`ricci_scalar_LC`、`weyl_tensor`、`weyl_scalar`、`riemann`、`ricci_scalar`、`lagrangian`、`action`、`potential`である。

### 6.2 ポテンシャルの取得

リポジトリ直下からの例：

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

3幾何で8引数を共有する。AXはV引数、VTはeta引数を無視する。FULLではthetaに依存しない。本文の幾何学的振幅を渡すときはV・etaをともに符号反転する。T3ではepsilonにより体積保存経路が指定され、方向別の独立半径の代入は不要である。

`get_potential_decomposition()`は`r^3`、`r^2`、`r^1`、`r^0`、`total`を返す。逆半径項の独立したキーはなく、その項は`total`に保持される。係数は、たとえば`expand(engine.data['potential']).coeff(engine.data['params']['r'], -1)`で取得する。LC-Weylが非零ならこの項を保ち、4個の多項式係数だけから一般のポテンシャルを再構成しない。

## 7. 半径と形状の分類

E4.14は半径微分をログに記録する段階であり、`equilibria`は空のままである。分類にはscanとviewerで共有する公開APIを使う。

```python
from dppu.scanning import classify_configuration

result = classify_configuration('Nil3', V=4, eta=-2, alpha=-1, epsilon=0)
print(result['global_class'])  # UNATTAINED_INFIMUM
print(result['radial_class'])  # FINITE_MINIMUM
```

`global_*`は固定捩率・L・κで全r>0・x>0、`radial_*`は指定epsilonを固定した全r>0の結果である。有限最小、未達成下限、退化最小、非有界を区別する。TT/REEは曲線比較に使えるが、完全NY分類は適用外となる。引数、CSV、数値範囲の詳細は[CLASSIFICATION](CLASSIFICATION_ja.md)を参照する。

入力の小数丸め、非零値の零への吸着、描画窓による根の除外は行わない。固定形状の解析式は80桁Decimalで評価する。数値的不確定やfloat範囲外は明示され、任意入力に対する区間保証は主張しない。分類の証明は本文第5〜8節、半径の判定式は付録Bにある。

## 8. 実行環境と再現

公開の依存は[requirements](../requirements.txt)。現行engine・分類器はSciPyを必要としない。notebookはipywidgets・ipymplを使う。式や規約の変更後は新しい出力／checkpoint先と再起動したkernelを使う。runnerのcheckpoint保存は明示的なオプションで、`engine.run()`は旧checkpointを自動読込しない。

[図のrenderとrecompute](../README_ja.md)を分け、旧出力を現行結果として使わない。本文の主張は本文・付録で完結し、外部作業用コードは公開計算の依存先ではない。

## 曲率モデルの選択

E4.8aはEC曲率の計算後に二乗作用のテンソルを選択し、E4.11はquadratic_scalarを使う。以前からのweyl_scalar、weyl_tensorはLC基準の互換名であり、選択された作用を意味しない。[モデル定義とAPI](WEYL_MODELS_ja.md)を参照する。
