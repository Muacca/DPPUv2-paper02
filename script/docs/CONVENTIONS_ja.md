# CONVENTIONS — DPPUv2 エンジン幾何規約

ECはEinstein–Cartan、LCはLevi-Civita、NYはNieh–Yanの略記です。


E4.3やE4.8aなどは公開計算・checkpointの段階IDであり、研究工程ではない。以下ではIDと処理内容を対応付けて説明する。


本書は、Paper02の `dppu.engine.pipeline.BaseFrameEngine` と各 topology runner が共有する **幾何・添字・符号規約**を固定する。
**全 runner はこの規約に従って `metric_frame` と `structure_constants` を定義すること。**

⇒ [English version](CONVENTIONS.md) | [SymPy ガイドライン](SymPy_guideline_ja.md)

## 1. 作用域と前提

* ここで扱う量はすべて **フレーム（正規直交基底）** 上の成分で表す。
* `metric_frame` はフレーム計量 $`(g_{ab})`$ であり、既定では $`(g_{ab}=\delta_{ab})`$ （`Matrix.eye(dim)`）。
* DPPUv2 engine の曲率成分計算は、（現状）**フレーム方向微分が不要になる状況**を前提にしている。
  具体的には、構造定数 $`(C^{a}{}_{bc})`$ と接続係数 $`(\Gamma^{a}{}_{bc})`$ が「フレームに関して定数扱い」になる（左不変フレームなど）設定を runner が採用すること。
  * **Note:** この設計は $S^3 \times S^1$ （Lie群）や Nil 多様体のような等質空間を扱う上では**合理的かつ効率的**である。ただし、将来的に対称性の低い一般的な曲率時空を扱う場合は、この前提がボトルネックになり得る点に留意すること。

## 2. 添字・配列のインデックス順

配列格納は以下で固定する：

* 構造定数：`C[a,b,c] = C^a_{bc}`
* 接続係数：`Gamma[a,b,c] = Γ^a_{bc}`
* リーマン曲率：`Riemann[a,b,c,d] = R^a_{bcd}`

添字の意味：

* $(a)$ ：出力（上付き）成分
* $(b,c,d)$ ：入力（下付き）成分
  とくに $`(\Gamma^{a}{}_{bc})`$ は $`(\nabla_{E_{c}} E_{b} = \Gamma^{a}{}_{bc} E_{a})`$ に対応する（最後の $(c)$ が “微分方向”）。

## 3. フレーム・コフレームと構造定数の定義（ここが最重要）

フレームの双対を $`(\{E_{a}\})`$ 、コフレーム（1-forms）を $`(\{e^a\})`$ とする。

### 3.1 コフレームの構造方程式（固定）

$$
de^a = \frac12 C^a{}_{bc} e^b\wedge e^c,
\qquad C^a{}_{bc} = - C^a{}_{cb}.
$$

### 3.2 双対フレームの交換関係（同値）

上の定義は次と同値：

$$
[E_{b}, E_{c}] = - C^{a}{}_{bc} E_{a}.
$$

> 注意：多くの教科書では $`([E_{b},E_{c}]=+f^{a}{}_{bc}E_{a})`$ を採用する。
> 本プロジェクトでは **その $`(f^{a}{}_{bc})`$ に対して $`(C^{a}{}_{bc}=-f^{a}{}_{bc})`$** の規約を採用している。

### 3.3 runner 実装ルール（推奨）

* runnerに格納するCは明示したcoframeの $de^a$ と照合する。Paper02の成分式は第9節に示す。
* 最低限、 $`C^{a}_{bc}`$ が **b,c で反対称**になっていることを自動チェックすること。

## 4. 接続（スピン接続）とメトリック整合

接続 1-form を

$$
\omega^{a}{}_{b} = \Gamma^{a}{}_{bc} e^c
$$

で定義する。

メトリック整合（ローレンツ接続／直交接続）を仕様として固定：

$$
\omega_{ab} = -\omega_{ba}
\quad(\Leftrightarrow\quad
\Gamma_{abc} = -\Gamma_{bac})
$$

ただし $`(\Gamma_{abc} = g_{ad}\Gamma^{d}{}_{bc})`$ 。

## 5. Levi-Civita 接続（DPPUv2 engine の一般 Koszul 実装）

フレームが正規直交で、上記の構造定数規約を採用したとき、Levi-Civita 接続は DPPUv2 engine では次の**一般 Koszul 公式**で計算する：

$$
\Gamma^a{}_{bc}
= \frac12\Big(
C^a{}_{bc} + C^c{}_{ba} - C^b{}_{ac}
\Big).
$$

（これは本書 3.2 の交換関係の符号を採用した場合の形である。）

**重要な注記:**

1. この公式は **bi-invariant 計量を仮定しない**。
   左不変フレーム上の Levi-Civita 接続として、Nil³ のような非 bi-invariant な場合でも正しく機能する。

2. 等方 SU(2) のように（低い添字で）構造定数が全反対称 $`C_{abc} = -C_{bac} = -C_{acb}`$ になる特殊な場合は、
   この公式は $`\Gamma^a_{bc} = \frac{1}{2} C^a_{bc}`$ に簡約される。

3. E4.3は計量適合性検査を呼ぶ。検査関数は成否と違反一覧を返してログへ記録するが、この呼出箇所での自動例外化は行わない。runnerを拡張する際は返値を確認する。Riemannの厳密検査は未証明の残差でも例外を送出する。

## 6. ねじれと曲率

ねじれ 2-form：

$$
T^a = de^a + \omega^{a}{}_{b} \wedge e^b,
\qquad
T^a = \frac12 T^{a}{}_{bc} e^b\wedge e^c.
$$

曲率 2-form：

$$
R^a{}_{b} = d\omega^{a}{}_{b} + \omega^{a}{}_{c}\wedge \omega^{c}{}_{b},
\qquad
R^a{}_{b} = \frac12 R^{a}{}_{bcd} e^c\wedge e^d.
$$

### 6.1 入力配列と幾何学的捩率

`torsion_tensor` は入力パラメータ配列τを格納する。幾何学的成分は
`T_geom[a,b,c] = C[a,b,c] + Gamma[a,c,b] - Gamma[a,b,c] = -tau[a,b,c]`。
Paper02は入力τを保存し、幾何学的捩率はこの式で再構成する。contortionは
`K[a,b,c]=(tau[a,b,c]+tau[b,c,a]-tau[c,a,b])/2`で与える。

### 6.2 Nieh–Yan密度

Euclideanフレーム計量とepsilon(0,1,2,3)=+1の下で、成分縮約は
`N_TT=epsilon*T*T/4`、`N_REE=epsilon*R/2`、`N_FULL=N_TT-N_REE`である。
REEは作用に`+theta*N_REE`を加える診断量を表す。
3種のrunnerの静的一様ansatzでは`TT=REE=-4*V*eta/r`（3幾何共通の正のscale `r`）、`FULL=0`。

## 7. 曲率成分の計算式（engine が実際に使う形）

DPPUv2 engine の $`R^{a}_{bcd}`$ は（現状）次の形を用いる：

$$
R^{a}{}_{bcd} = \Gamma^{a}{}_{ec}\Gamma^{e}{}_{bd} -\Gamma^{a}{}_{ed}\Gamma^{e}{}_{bc} +\Gamma^{a}{}_{be} C^{e}{}_{cd}.
$$

> 重要：一般にはここにフレーム方向微分項
> $`(E_{c}(\Gamma^{a}{}_{bd}) - E_{d}(\Gamma^{a}{}_{bc}))`$
> が現れるが、DPPUv2 engine ではそれを明示的に扱っていない。
> したがって runner は、左不変フレーム等により **$(\Gamma)$ がフレーム方向で定数扱い**になる設定を採用すること。

## 8. 必須セルフチェック（runner が満たすべき整合性）

runner は以下を満たすこと（落ちたら定義が engine と不整合）：

1. 構造定数の反対称：

$$
C^{a}{}_{bc} + C^{a}{}_{cb} = 0.
$$

2. メトリック整合（直交接続）：

$$
\omega_{ab} + \omega_{ba} = 0.
$$

3. リーマンの反対称（engine の strict check 対象）：

$$
R_{ab cd} = -R_{ba cd},\qquad
R_{ab cd} = -R_{ab dc}.
$$

## 9. 大域幾何と積分領域

### 9.1 体積保存形状と共通scale

3幾何で半径scale `r`、円周長L、正のκを用いる。形状は次のcoframeで導入する。空間3因子の積は1であり、epsilonを変えても体積は変わらない。

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

### 9.2 球面SU(2)

等方では実半径はr/2である。SU(2)のcoframeを次で固定する。

$$
\begin{aligned}
\lambda^0&=\cos\psi\thinspace d\vartheta+\sin\psi\sin\vartheta\thinspace d\varphi,\\
\lambda^1&=-\sin\psi\thinspace d\vartheta+\cos\psi\sin\vartheta\thinspace d\varphi,\\
\lambda^2&=d\psi+\cos\vartheta\thinspace d\varphi,\qquad \sigma^i=-\lambda^i/4.
\end{aligned}
$$

積分域は $0\le\vartheta\le\pi$ 、 $0\le\varphi<2\pi$ 、 $0\le\psi<4\pi$ で、極の退化と境界の同定 $(\varphi+2\pi,\psi)\sim(\varphi,\psi+2\pi)$ を伴う。正の体積密度は $r^3\sin\vartheta/64$ 。coframeの向きは $d\vartheta\wedge d\varphi\wedge d\psi$ と逆である。向きの規約は $`e^0\wedge e^1\wedge e^2\wedge e^3>0`$ とする。

### 9.3 トーラス

$`\sigma^i=dy^i`$ とし、各角を $2\pi$ 周期にする。各周長は $`2\pi r s^{1/3},2\pi r s^{1/3},2\pi r s^{-2/3}`$ 。Paper02は共通rと体積保存形状を使う。Paper01の独立なR1/R2/R3を同じAPIとみなさない。

### 9.4 固定コンパクトNil商

Heisenberg群の左商を次のcoframeと同定で指定する。

$$
\begin{aligned}
\sigma^0&=dy^0,\qquad \sigma^1=dy^1,\qquad \sigma^2=dz-y^0\thinspace dy^1,\\
(y^0,y^1,z)&\sim(y^0+2\pi,y^1,z+2\pi y^1),\\
(y^0,y^1,z)&\sim(y^0,y^1+2\pi,z),\\
(y^0,y^1,z)&\sim(y^0,y^1,z+4\pi^2).
\end{aligned}
$$

基本領域は [0,2π)×[0,2π)×[0,4π²)。水平生成元の交換子は中央周期4π²に対応する。rと形状を変えても格子・商は固定し、中央座標を2π周期に置き換えない。

### 9.5 体積・入力辞書・変分

$$
\mathrm{Vol}_{4}=c_{M} Lr^3,\qquad
c_{S^3}=\frac{\pi^2}{4},\quad c_{T^3}=(2\pi)^3,\quad c_{\mathrm{Nil}^3}=(2\pi)^4.
$$

本文の符号付き振幅とコード入力は $`(\eta,V)=(-\eta_{\tau},-V_{\tau})`$ 。コードVの正値symbol仮定は本文のV<0へ写り、入力区間の端点も符号と順序を変換する。数値APIは符号付き実入力を扱う。rの倍率は球面の実半径だけに関わり、捩率振幅を無断で再定義しない。

Nil engineの`params['R']`と`params['r']`は同じsymbolであり、公開callableの第1引数は共通の半径scaleである。捩率振幅・L・κを固定した変分であり、η固定と2η/r固定は異なる。二変数と固定形状の領域は[分類仕様](CLASSIFICATION_ja.md)を参照する。

## 10. 曲率二乗項と縮約作用

主対象は既約EC-Weyl作用、LCは比較基準、EC_TRACEFREE（Ricciトレース除去EC曲率）は別作用である。[曲率二乗モデル](WEYL_MODELS_ja.md)を参照する。以下の式は指定静的族の既約EC-Weyl作用とLC-Weyl作用に共通であり、αは形状とは別の結合である。

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

ここでNはNYの4形式であり、その体積係数が第6節の `N_FULL` である。 $`I_{\mathrm{W}}`$ は既約EC-Weylテンソルの二乗ノルムを表す。

LC-Weylは等方球面と全トーラスで零、有限形状のNilでは非零である。非正αの球面形状下限、正αの小半径非有界性、Nilの半径断面と二変数の違いは本文第5〜8節で証明する。Uの最小を全場真空やLorentzian ghostの判定として扱わない。

## 11. 形式Hodge双対と曲率ノルム

向きε0123=+1、Euclidean計量の下で、最後の形式添字対を双対化する。

$$
\begin{aligned}
(*R)_{abcd}&=\frac12\varepsilon_{cdef}R_{abef},\\
\mathcal P\thinspace\mathrm{vol}_{4}&=\sum_{a,b}R_{ab}\wedge R_{ab},\qquad
\mathcal P=\frac14\varepsilon^{cdef}R_{abcd}R_{abef},\\
E_{\mathrm{all}}&=\sum_{a,b,c,d}R_{abcd}^2,\qquad
P_{\mathrm{all}}=\sum_{a,b,c,d}R_{abcd}(*R)_{abcd}=2\mathcal P.
\end{aligned}
$$

内部添字対の双対と区別する。E_allは曲率ノルムでありEuler密度ではない。以前の数値出力名E_RR・P_RstarRは、それぞれE_all・P_allに対応する。これらの規格化は数値診断APIの有無によらず本文第3節と付録Cの定義である。公開の記号計算補足は3幾何の空間block構造と零のPontryaginを独立に確認する。

[LaTeX原稿](../../LaTeX/main.tex) / [実装ガイド](SymPy_guideline_ja.md) / [分類・CSV・viewer](CLASSIFICATION_ja.md)
