# 曲率二乗作用

[English](WEYL_MODELS.md) / [利用方法](../README_ja.md)

Einstein–Cartan（EC）、Levi-Civita（LC）、Nieh–Yan（NY）は本文第2〜4節の定義を用いる。以下の作用はECのRicciスカラーと選択したNY項を共通に持ち、曲率二乗項だけを変更する。LC-Weylの選択は接続全体をLCへ置き換える意味ではない。

| 科学的名称 | 公開の選択値 | 二乗項に使うテンソル |
|---|---|---|
| 既約EC-Weyl作用（既定） | `EC_IRR` | EC曲率の既約Weyl射影、10成分 |
| LC-Weyl作用 | `LC` | LC接続のWeylテンソル |
| Ricciトレース除去EC曲率作用 | `EC_TRACEFREE` | EC曲率のRicci縮約の核、20成分 |

全添字を下げた曲率に対し、 `rc_weyl.irreducible_weyl_curvature(R, metric)` は対交換対称化、4形式の除去、得られた代数的Riemann曲率のRicciトレース除去を行う。 `rc_weyl.ricci_tracefree_curvature(R, metric)` は元のEC曲率から直接Ricciトレースを除く。係数はRicci縮約が零となる条件で決まり、LCとの一致に合わせて調整していない。一般のEC曲率は対交換対称性や捩率なしの代数Bianchi恒等式を満たすとは限らない。

二つのテンソルを $`C_{\mathrm{EC}}`$ 、 $`\widehat R_{\mathrm{EC}}`$ と書く。Riemann–Cartan（RC）分解において、 $R^{(2)}$ は対交換反対称でRicciトレースなしの9成分、 $R^{(3)}$ は4形式の1成分である。

$$
\begin{aligned}
\widehat R_{\mathrm{EC}}&=C_{\mathrm{EC}}+R^{(2)}+R^{(3)},\\
I_{\mathrm{W}}&=\lVert C_{\mathrm{EC}}\rVert^2,\qquad
I_{\mathrm{tf}}=\lVert\widehat R_{\mathrm{EC}}\rVert^2.
\end{aligned}
$$

三つの部分はEuclidean計量で直交する。既約EC-Weyl作用は後二者の二乗結合を零とし、Ricciトレース除去EC曲率作用は三部分に同じ結合を与える。分解だけから物理的な作用は決まらない。定義と証明は本文第4節、RC分解は [McNuttほか](https://doi.org/10.3842/SIGMA.2024.078) を参照する。

指定された静的一様族の全ての正の半径・形状に対して、

$$
C_{\mathrm{EC}}=C_{\mathrm{LC}},\qquad
I_{\mathrm{tf}}-I_{\mathrm{W}}=\frac{16V^2\eta^2}{3r^2},\qquad
U_{\mathrm{tf}}-U_{\mathrm{W}}=-\frac{16}{3}\alpha c_{M}L V^2\eta^2r.
$$

$`U_{\mathrm{tf}},U_{\mathrm{W}}`$ は対応する縮約ポテンシャルである。一般の場、制限のない変分、運動項の同値性を意味しない。追加項はNY結合に依存せず、V=0またはη=0で消え、ポテンシャルはα=0でも一致する。NY係数の訂正とは別の寄与である。

## engineとコマンドラインの選択

```python
engine = S3S1Engine(Mode.MX, NyVariant.FULL, curvature_model='EC_IRR')
engine.run()
I = engine.data['quadratic_scalar']
U = engine.data['potential']
```

3幾何のrunnerと `run_parameter_scan.py` は `--curvature-model LC`、 `EC_IRR`、 `EC_TRACEFREE` に対応する。viewerは同じ保存値に科学的名称を表示し、作用を計算cacheの識別にも使う。分類関数は `curvature_model` を受け、CSVの各行に記録する。

捩率の選択は `AX`（軸性のみ、V=0）、 `VT`（ベクトルトレースのみ、η=0）、 `MX`（両成分を許す）であり、全て零振幅を許す。独立したNY選択の `FULL` は捩率の積の体積係数から曲率・coframe収縮の体積係数を引く。 `TT` と `REE` はそれぞれ正符号の単独成分に実結合θを掛ける。正符号はθの値の制限を意味せず、REE単独には完全NY内の負号を含めない。TT/REEの曲線は計算できるが、分類は `NOT_APPLICABLE` となる。

| 保存キー | 意味 |
|---|---|
| `curvature_model` | 選択された曲率二乗作用 |
| `quadratic_tensor`, `quadratic_scalar` | 作用に使うテンソルと全添字縮約による二乗ノルム |
| `weyl_tensor_LC`, `weyl_scalar_LC` | LC比較基準 |
| `weyl_tensor`, `weyl_scalar` | 全ての作用選択でLC基準を意味する互換キー |

低水準の `compute_lagrangian(..., weyl_scalar=...)` はキーワードを保持し、engineは `quadratic_scalar` を渡す。ソース変更後はnotebook kernelを再起動する。曲率二乗テンソルの選択段階（E4.8a）がテンソルとモデルを保存する。作用構築段階（E4.11）は保存モデルの不一致を拒否するため、作用変更時はE4.8aで再射影する。 `engine.run()` はcheckpointを自動ロードしない。

## 掲載データと再現

掲載6 CSV・設定・4図はLC-Weylで計算したもので、再計算も `LC` を明示選択する。テンソル恒等式により指定族の既約EC-Weyl作用にも適用できる。Ricciトレース除去EC曲率作用のデータではない。その作用の計算にはrunner/viewerで `EC_TRACEFREE` を選ぶ。本文第4.4節には短い解析比較を掲載している。
