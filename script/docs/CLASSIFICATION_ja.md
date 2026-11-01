# 分類とscan出力

ECはEinstein–Cartan、LCはLevi-Civita、NYはNieh–Yanの略記です。


[English](CLASSIFICATION.md) / [利用方法](../README_ja.md)

`dppu.scanning.classify_configuration`をscanとviewerで共有する。入力は幾何、符号付きコードV・eta、α、epsilon、mode、NY作用、theta、L、kappa。epsilon > -1、L,kappa > 0を要求する。CLI/viewerではL=kappa=1。AXは有効V=0、VTは有効eta=0とする。コード入力の符号は本文の幾何学的捩率と逆である。

## 二つの領域

- `global_*`：両Weyl作用は第7・8節、Ricciトレース除去EC曲率作用は第4.4節の完全NY分類。捩率振幅・L・kappaを固定し、全r>0・全x>0で考える。epsilonによる断面制限はしない。非正αの球面の有限最小は等方にあり、Nilは半径断面に極小があっても二変数領域の下限0は未達成である。
- `radial_*`：指定epsilon、x=(1+epsilon)**(-2/3)を固定した全r>0の分類。付録Bの半径二乗に関する二次方程式と端点極限を使う。描画範囲や有限格子を判定範囲にしない。

| ラベル | 指定領域における意味 |
|---|---|
| `FINITE_MINIMUM` | 一意な有限最小が存在する |
| `UNATTAINED_INFIMUM` | 有限の下限へ境界で近づくが達成しない |
| `DEGENERATE_MINIMUM` | 非孤立な集合で最小を達成する |
| `UNBOUNDED_BELOW` | 下に非有界 |
| `NOT_APPLICABLE` | TT/REEは別作用なので本文の分類を適用しない |
| `NUMERIC_UNRESOLVED` | 固定形状の境界を作業精度で識別できない |

両Weyl作用の非正αのS3では、V非零・eta二乗が4未満の有限最小、未達成下限0、V=0・閾値未満のrunaway、V=0・eta二乗=4の退化等方 rayを区別する。正αでは、等方の半径断面に最小があっても二変数領域では非有界である。T3は両振幅零なら全域で零、それ以外は下限0を達成しない。Nilは非正αで下限0が未達成、正αで下に非有界である。

## CSVと数値境界

各行には`V_input`・`eta_input`と有効`V`・`eta`、幾何・mode・作用・α・epsilon・theta・L・kappaを保存する。旧`stability_type`に代えて`global_class`と`radial_class`を使う。`global_infimum`・`radial_infimum`は下限で、非有界なら`-inf`、適用外・数値が得られない場合は空欄となる。`global_r`・`global_x`・`radial_r`は得られる最小点の座標を示す。Ricciトレース除去EC曲率作用のT3では退化二変数集合の共通半径も記録する。`*_limit`は極限経路または退化集合を示す。`radial_local_min_r`は下限が負の無限大でも存在し得る局所半径極小であり、大域最小を意味しない。

旧`r0`・`delta_V`列は使わない。旧CSVを新分類へ読み替えない。既定はFULLで、thetaに依存しないため既定では1点だけ採る。明示的にTT/REEを指定した行はNOT_APPLICABLEとする。それらのポテンシャルはengineとviewerで引き続き扱う。

有限の二進浮動小数点入力を小数第2位へ丸めない。V=0、abs(eta)=2、α=0は保存された入力値で判定し、近傍を境界へ吸着させる許容幅を設けない。例えばV=4・eta=1.999には有限等方最小があり、eta=2では下限0が未達成となる。表現可能な最小の非零値も零へ置き換えない。

固定形状の係数と根は、桁落ちを抑えた式と80桁のDecimal演算を使う。`numeric_status`は係数境界・合流根の数値的不確定、またはfloatで表せない数値を示す。後者では該当数値を空欄にし、別途確定した分類は保持する。任意入力に対する区間保証付きsolverではなく、記載した式の数値実装である。

## Viewer

mapの選択欄で二変数／固定形状の半径分類を切り替える。曲線は常に指定epsilonの現行engineを使う。選択点表は両領域の分類・下限・半径を並べ、描画範囲外の最小点も明示する。TT/REEは曲線比較が可能だが、本文の分類mapは適用外とする。FULLでは不活性なtheta欄を無効にする。

点の数値欄には1.999などを入力できる。Applyで両panelを一緒に更新し、control変更後は以前の図が更新待ちであることを表示する。色付きcellは格子上の分類の可視化であり、球面の閾値線や退化点の表示は厳密な境界に有限の幅を与えるものではない。コード振幅と変分領域を明記し、全場真空・Lorentzian ghost・普遍的なトポロジー選択を判定しない。

曲線が縦軸範囲外なら図内に案内を表示する。`Fit U to curves`は現在の半径窓の曲線標本に縦軸を合わせ、分類を変更しない。Nilなど値の幅が大きい場合は`U scale`の`Symlog`と組み合わせる。最小点が半径窓または縦軸範囲外の場合も選択点表で確認できる。

## 曲率二乗作用

`curvature_model` は既約EC-Weyl（`EC_IRR`、既定）、LC-Weyl（`LC`）、Ricciトレース除去EC曲率（`EC_TRACEFREE`）を選ぶ。上記の分類は両Weyl作用に共通である。Ricciトレース除去EC曲率作用は半径一次係数の $9\eta^2$ を $\gamma=\eta^2(9-16\kappa^2\alpha V^2)$ へ置き換え、付録Bの停留点方程式を使う。

S³の非正αではγ<36かつV非零が一意な等方球面での最小、V=0かつγ<36が非有界、V=0かつγ=36が等方半直線の退化最小、それ以外が未達成下限零となる。正αでは半径・形状の二変数領域で非有界であり、Nilも両Weyl作用と同じ二変数分類を持つ。T³のγ<0では半径最小が生じ、全形状で達成するため二変数では `DEGENERATE_MINIMUM` となる。`global_r` に共通半径を保存し、`global_x` は空、`global_limit` は `fixed_r_all_shape` となる。γ非負のT³では両振幅零なら全半径・形状が最小であり、そうでなければ下限零は未達成である。

Ricciトレース除去EC曲率作用のγと36−γの符号は、入力floatから正確な有理数演算で決めてから値を80桁Decimalへ変換する。丸めた積で閾値を判定しない。両Weyl作用は上記の境界規則を使う。図は選択作用を表示し、eta=±2の破線は両Weyl作用の境界としてのみ描く。[作用の定義](WEYL_MODELS_ja.md)を参照する。
