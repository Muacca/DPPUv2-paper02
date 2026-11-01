# 4. Weyl射影・曲率恒等式と縮約ポテンシャル

## 4.1 比較基準としてのLC曲率

Cartanの捩率なし条件と計量適合性を解いてLC接続を得ると、式(G)の一般のnに対して次を得る。軸性項の符号を入力配列から幾何学的Tへ変えても、スカラーの二乗項は同じである。

**式(R)**

$$
\begin{aligned}
R_{\mathrm{LC}}&=n_{0}n_{1}+n_{1}n_{2}+n_{2}n_{0}
-\frac12(n_{0}^{2}+n_{1}^{2}+n_{2}^{2}),\\
R_{\mathrm{EC}}&=R_{\mathrm{LC}}-\frac{6\eta^{2}}{r^{2}}-\frac23V^{2}.
\end{aligned}
$$


4次元LC曲率の関係 $`C^{2}=R_{abcd}R^{abcd}-2R_{ab}R^{ab}+R^{2}/3`$ を用いると、各幾何の式は次のようになる。この関係をEC曲率へ無条件に転用しない。

**式(W)**

$$
\begin{aligned}
f(x)&=4x-x^{4},\\
R_{\mathrm{LC},S^{3}}&=\frac{8f(x)}{r^{2}},
&C_{\mathrm{LC},S^{3}}^{2}&=\frac{1024x^{2}(1-x^{3})^{2}}{3r^{4}},\\
R_{\mathrm{LC},T^{3}}&=0,&C_{\mathrm{LC},T^{3}}^{2}&=0,\\
R_{\mathrm{LC},\mathrm{Nil}^{3}}&=-\frac{x^{4}}{2r^{2}},
&C_{\mathrm{LC},\mathrm{Nil}^{3}}^{2}&=\frac{4x^{8}}{3r^{4}}.
\end{aligned}
$$



## 4.2 既約EC-WeylとLCの恒等式

計量適合なEC曲率は各添字対で反対称だが、対交換対称性と捩率なしの代数Bianchi恒等式は一般には満たさない。既約EC-Weylテンソルは標準的なRiemann–Cartan曲率分解のWeyl部分を取る（[McNuttほか、§2](https://doi.org/10.3842/SIGMA.2024.078)）。4次元Euclideanでは10成分を持ち、Hodgeの自己双対・反自己双対の各5成分に分かれる。全EC曲率から、次の線形操作で定義する。

**式(WP)**

$$
\begin{aligned}
S_{abcd}&=\tfrac12(R^{\mathrm{EC}}_{abcd}+R^{\mathrm{EC}}_{cdab}),\\
F_{abcd}&=\tfrac13(S_{abcd}+S_{acdb}+S_{adbc}),\qquad Q=S-F,\\
q_{bd}&=\delta^{ac}Q_{abcd},\qquad s=\delta^{bd}q_{bd},\\
(C_{\mathrm{EC}})_{abcd}&=Q_{abcd}-\tfrac12(\delta_{ac}q_{bd}-\delta_{ad}q_{bc}
-\delta_{bc}q_{ad}+\delta_{bd}q_{ac})
+\tfrac{s}{6}(\delta_{ac}\delta_{bd}-\delta_{ad}\delta_{bc}).
\end{aligned}
$$

Fは完全反対称な4形式であり、Qは代数的Riemann曲率の対称性を持つ。最後の行は、そのRicciから計量を使って再構成される部分を直交的に除く一意の操作である。縮約すると $`q_{bd}-(2q_{bd}+s\delta_{bd})/2+s\delta_{bd}/2=0`$ となる。これは曲率の一部分を定義する操作であり、接続に捩率なしの場の方程式を課す操作ではない。

**命題2（指定族における同値性）**　式(T)の任意の符号付き振幅と、全ての正の半径・形状で、次が成り立つ。

**式(ID)**

$$
C_{\mathrm{EC}}=C_{\mathrm{LC}},\qquad I_{\mathrm{W}}=I_{\mathrm{LC}}.
$$

**証明。** $h=\eta/r$ 、 $`q_{0}=h^2+V^2/9`$ と置く。付録AのCartan接続とcontortionから、式(G)の構造定数を一般のまま残すと、曲率差の独立成分は次になる。

**式(CD)**

$$
\begin{aligned}
\Delta R_{ijkl}&=-q_{0}(\delta_{ik}\delta_{jl}-\delta_{il}\delta_{jk}),\\
\Delta R_{i3jk}&=-\tfrac{2hV}{3}\epsilon_{ijk},\\
\Delta R_{ijk3}&=0,\qquad\Delta R_{i3j3}=0,
\qquad i,j,k,l\in\lbrace 0,1,2\rbrace.
\end{aligned}
$$

残りは各添字対の反対称性で決まる。第1行の空間Ricciは $`-2q_{0}\delta_{ij}`$ 、33成分は零、スカラーは $`-6q_{0}`$ であり、式(WP)の最終行へ代入すると零となる。第2行の対交換対称部分は4形式 $`-hV\epsilon_{abcd}/3`$ となってFで除かれ、対交換反対称部分はSで除かれる。従って曲率差のWeyl射影は零である。LC曲率は式(WP)の最初の二操作で変わらないので、テンソルとしての同値性を得る。h、V、x−1で割っていないため零振幅と等方も含み、式(CD)が構造定数に依存しないため3幾何の全形状を覆う。□

この恒等式は指定された静的一様族についての結果である。一般の場でのLC-Weyl作用と既約EC-Weyl作用、制限のない変分、時間依存の摂動作用素の同値性を意味しない。

## 4.3 既約EC-Weyl作用とLC-Weyl作用に共通の縮約ポテンシャル

体積と完全NY零を代入して得るUは次のとおりである。

**式(S3)**

$$
U_{S^{3}}=\frac{c_{S^{3}}L}{3\kappa^{2}}
\left[V^{2}r^{3}+(9\eta^{2}-12f(x))r
-\frac{1024\kappa^{2}\alpha x^{2}(1-x^{3})^{2}}{r}\right].
$$


**式(TN)**

$$
\begin{aligned}
U_{T^{3}}&=\frac{c_{T^{3}}L}{3\kappa^{2}}(V^{2}r^{3}+9\eta^{2}r),\\
U_{\mathrm{Nil}^{3}}&=\frac{c_{\mathrm{Nil}^{3}}L}{3\kappa^{2}}
\left[V^{2}r^{3}+\left(9\eta^{2}+\frac34x^{4}\right)r
-\frac{4\kappa^{2}\alpha x^{8}}{r}\right].
\end{aligned}
$$


等方球面の近傍のWeyl項は形状変形の二次から始まる。二次係数と二階微分を区別すると、次の局所展開を得る。

**式(DERIV)**

$$
\begin{aligned}
C_{\mathrm{LC},S^{3}}^{2}
&=\frac{1024\varepsilon^{2}(\varepsilon+2)^{2}}{3r^{4}(1+\varepsilon)^{16/3}}
=\frac{4096}{3r^{4}}\varepsilon^{2}+O(\varepsilon^{3}),\\
\left.\frac{\partial^{2} C^{2}}{\partial\varepsilon^{2}}\right|_{0}
&=\frac{8192}{3r^{4}}.
\end{aligned}
$$

式(W)から、Weyl項はS³の等方断面とT³で消え、有限の正の形状を持つNil³では正の曲率二乗を与える。この違いが、次節以降の形状最小化と小半径での振る舞いを決める。

## 4.4 Ricciトレース除去EC曲率作用との比較

比較するテンソル $`\widehat R_{\mathrm{EC}}`$ は、式(WP)の最後のRicci除去操作だけを元のEC曲率へ適用して定義する。その際はEC曲率自身のRicciとスカラーを使う。これは20次元のRicci縮約の核への正当な射影であり、既約Weyl部分の10成分とは範囲が異なる。帽子はRicciトレースの除去を表し、Weyl射影とは区別する。その二乗ノルムを $`I_{\mathrm{tf}}=(\widehat R_{\mathrm{EC}})_{abcd}(\widehat R_{\mathrm{EC}})^{abcd}`$ と定義する。tfはRicci縮約が零であることを表す。標準分解では

**式(TF)**

$$
\widehat R_{\mathrm{EC}}=C_{\mathrm{EC}}+R^{(2)}+R^{(3)},\qquad
I_{\mathrm{tf}}=I_{\mathrm{W}}+\lVert R^{(2)}\rVert^2+\lVert R^{(3)}\rVert^2.
$$

$R^{(2)}$ は対交換反対称でRicciトレースなしの9成分、 $R^{(3)}$ は4形式の1成分である。各部分の直交性がノルム和を与える。Ricciトレース除去EC曲率作用は式(A)の $`I_{\mathrm{W}}`$ を $`I_{\mathrm{tf}}`$ へ置き換え、三つの部分に同じ二乗結合を与える。既約EC-Weyl作用は後二者の結合を零とする。どちらを作用に含めるかは分解だけからは決まらない。

既約EC-Weyl作用と比較作用の縮約ポテンシャルをそれぞれ $`U_{\mathrm{W}},U_{\mathrm{tf}}`$ とする。指定族では式(CD)から次を得る。

**式(SHIFT)**

$$
\begin{aligned}
\lVert R^{(2)}\rVert^2=\lVert R^{(3)}\rVert^2&=\frac{8V^2\eta^2}{3r^2},\\
I_{\mathrm{tf}}-I_{\mathrm{W}}&=\frac{16V^2\eta^2}{3r^2},\\
U_{\mathrm{tf}}-U_{\mathrm{W}}&=-\frac{16}{3}\alpha c_{M} L V^2\eta^2 r.
\end{aligned}
$$

追加項は形状とNY結合に依存せず、V=0またはη=0では消える。ポテンシャルはα=0でも一致する。この寄与は作用に含めた曲率成分の選択で決まり、付録DのNY係数訂正とは独立である。

Ricciトレース除去EC曲率作用の3幾何のポテンシャルは、式(S3),(TN)で $9\eta^2$ を $\gamma=\eta^2(9-16\kappa^2\alpha V^2)$ に置き換えて得る。球面の形状差は変わらず、非正αでの有限等方最小条件は $V\ne0,\gamma<36$ 、半径は $r^2=(36-\gamma)/(3V^2)$ となる。他の場合は $`U_{\mathrm{tf},\mathrm{round}}=c_{S^3}L[V^2r^3+(\gamma-36)r]/(3\kappa^2)`$ から判定する。正αでは球面の二変数領域で非有界である。Nilも式(SHIFT)が形状非依存なので同じ二変数分類が成り立ち、非正αではγも非負となって未達成下限零、正αでは逆半径項による非有界性を持つ。T³では $\gamma<0$ なら $r^2=-\gamma/(3V^2)$ に半径最小が生じ、全形状で達成される退化した二変数最小集合となる。それ以外のT³では両振幅零なら全半径・形状が最小であり、そうでなければ下限零は未達成である。これらはRicciトレース除去EC曲率作用の比較結果であり、以下の定理1〜3は既約EC-Weyl作用とLC-Weyl作用を対象とする。
