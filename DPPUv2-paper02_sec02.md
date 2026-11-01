# 2. 作用・幾何・固定量

Euclidean正規直交計量と向き0123正を用い、 $\kappa,L$ は正、 $\alpha,\theta$ は実数とする。宇宙項、物質源、境界は加えない。主対象は既約EC-Weylテンソルの二乗ノルム $`I_{\mathrm{W}}=(C_{\mathrm{EC}})_{abcd}(C_{\mathrm{EC}})^{abcd}`$ を含む作用であり、これを既約EC-Weyl作用と呼ぶ。テンソルの射影は第4.2節で定義する。LC-Weyl作用はこの二乗項だけを $`I_{\mathrm{LC}}=(C_{\mathrm{LC}})_{abcd}(C_{\mathrm{LC}})^{abcd}`$ へ置き換えた比較基準であり、ECのRicciスカラーと完全NYは共通である。第4.4節ではRicciトレース除去EC曲率作用を比較する。これらの名称は曲率二乗項の選択を表し、接続全体をLCへ変更する意味ではない。Weyl部分だけを二乗項に含めることは模型上の選択である。以下、比較を明示する箇所以外のUは既約EC-Weyl作用の縮約ポテンシャルを表す。

**式(A)**

$$
S=\int_{M}\left[\left(\frac{R_{\mathrm{EC}}}{2\kappa^{2}}
+\alpha I_{\mathrm{W}}\right)\mathrm{vol}_{4}+\theta N\right],
\qquad U=-S\big|_{\mathrm{ansatz}}.
$$


Uはこの符号で定義した作用の負値であり、Lorentzian Hamiltonianを意味しない。局所規約は次のとおりである。

**式(C)**

$$
\begin{aligned}
de^{a}&=\frac12 C^{a}{}_{bc}e^{b}\wedge e^{c},
&\omega^{a}{}_{b}&=\Gamma^{a}{}_{bc}e^{c},\\
T^{a}&=de^{a}+\omega^{a}{}_{b}\wedge e^{b},
&R^{a}{}_{b}&=d\omega^{a}{}_{b}+\omega^{a}{}_{c}\wedge\omega^{c}{}_{b},\\
T^{a}&=\frac12 T^{a}{}_{bc}e^{b}\wedge e^{c},
&R_{ab}&=\frac12 R_{abcd}e^{c}\wedge e^{d}.
\end{aligned}
$$


NYの曲率項は2形式一個と1形式二個の積なので係数1/2、捩率の積は2形式二個の積なので1/4である。[Chandía–Zanelli](https://arxiv.org/abs/hep-th/9702025)の形式定義と対応する。

**式(NY)**

$$
\begin{aligned}
N&=d(e^{a}\wedge T_{a})=T^{a}\wedge T_{a}-R_{ab}\wedge e^{a}\wedge e^{b},\\
\frac{N}{\mathrm{vol}_{4}}
&=\frac14\epsilon^{abcd}T^{e}{}_{ab}T_{ecd}
-\frac12\epsilon^{abcd}R_{abcd}.
\end{aligned}
$$


二つの4形式の体積係数を次で定義する。

**式(NYD)**

$$
\begin{aligned}
\mathcal T\thinspace\mathrm{vol}_{4}&=T^{a}\wedge T_{a},\\
\mathcal R\thinspace\mathrm{vol}_{4}&=R_{ab}\wedge e^{a}\wedge e^{b},\\
N&=(\mathcal T-\mathcal R)\mathrm{vol}_{4}.
\end{aligned}
$$

ここで $\mathcal R$ は曲率とcoframeの収縮の体積係数であり、Ricciスカラーではない。コードのNY選択との対応は付録Bに示す。

体積保存変形を次で与える。Nil³でもrを共通記号として使い、コードのRに対応させる。等方はS³の $`x=1`$ を指す。

**式(F)**

$$
\begin{aligned}
e^{0}&=r s^{1/3}\sigma^{0},&e^{1}&=r s^{1/3}\sigma^{1},\\
e^{2}&=r s^{-2/3}\sigma^{2},&e^{3}&=L\,du,\\
s&=1+\varepsilon>0,&x&=s^{-2/3}>0.
\end{aligned}
$$


**式(G)**

$$
\begin{aligned}
de^{0}&=n_{0} e^{1}\wedge e^{2},&de^{1}&=n_{1} e^{2}\wedge e^{0},\\
de^{2}&=n_{2} e^{0}\wedge e^{1},&de^{3}&=0,\\
(n_{0},n_{1},n_{2})_{S^{3}}&=\frac1r(4/x,4/x,4x^{2}),\\
(n_{0},n_{1},n_{2})_{T^{3}}&=(0,0,0),
\qquad (n_{0},n_{1},n_{2})_{\mathrm{Nil}^{3}}=\frac1r(0,0,-x^{2}).
\end{aligned}
$$


S³はSU(2)そのものを使い、等方球面の実半径はr/2である。T³の空間角は各2π周期、S¹のuは周期1、したがってLは実円周長である。Nil³は $`\sigma^{0}=dy^{0}`$ 、 $`\sigma^{1}=dy^{1}`$ 、 $`\sigma^{2}=dz-y^{0}dy^{1}`$ を用い、周期を(2π,2π,4π²)、 $`y^{0}`$ 面の貼合せを $`z\mapsto z+2\pi y^{1}`$ とする。この商をr・形状変分で固定する。

**式(VOL)**

$$
\mathrm{Vol}_{4}=c_{M} Lr^{3},
\qquad c_{S^{3}}=\frac{\pi^{2}}{4},\quad
c_{T^{3}}=(2\pi)^{3},\quad c_{\mathrm{Nil}^{3}}=(2\pi)^{4}.
$$


幾何学的捩率を次で定義する。空間epsilon項は添字がすべて0,1,2のときだけ含める。

**式(T)**

$$
T_{abc}=\frac{2\eta}{r}\epsilon_{abc}\big|_{a,b,c<3}
+\frac13(\delta_{ac}V_{b}-\delta_{ab}V_{c}),
\qquad V_{b}=V\delta_{b3}.
$$


固定するのは符号付きη・Vであり、軸性成分2η/rそのものを半径変分で固定するのではない。この軸性成分は空間の3方向で等しく、形状に依存しない。これは族の定義の一部である。先行研究の異方的トーラス経路のように、形状に依存する一つの長さを基準にすると、x＝1でのみ式(T)と一致する別の族になる。主な変分量はrと形状である。公開コード入力の符号対応は式(D)を用い、本文のTと入力配列を同一視しない。

**式(D)**

$$
\begin{aligned}
T_{\mathrm{geom}}&=-\tau_{\mathrm{code}},
& (\eta,V)&=(-\eta_{\tau},-V_{\tau}),\\
K_{abc}[T]&=-\frac12(T_{abc}+T_{bca}-T_{cab}),
&K_{abc}[\tau]&=+\frac12(\tau_{abc}+\tau_{bca}-\tau_{cab}).
\end{aligned}
$$
