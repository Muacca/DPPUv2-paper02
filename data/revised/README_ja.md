# 掲載図表のデータ

[English](README.md)

Paper02 v2の掲載データ（計算日2026-10-30）。入力はコードのτ規約です。L＝κ＝θNY＝1、Vτ＝4を基本とし、各CSVの列と `parameters.json` で形状・α・ηの値を指定します。

| CSV | 図・用途 |
|---|---|
| [shape_penalty.csv](shape_penalty.csv) | 図1：半径を固定した球面の形状差 |
| [small_radius.csv](small_radius.csv) | 図2：形状固定・正結合での小半径の曲線 |
| [round_reference.csv](round_reference.csv) | 図4（付録D）：旧式との比較と現行式の代表断面 |
| [nil_slices.csv](nil_slices.csv) / [torus.csv](torus.csv) | 図3：Nilの形状固定半径極小とトーラスのα非依存性 |
| [stationary_points.csv](stationary_points.csv) | 第7節の代表入力。定常点がない値は空欄 |
| [parameters.json](parameters.json) | 固定量、領域、体積、解釈 |

旧NY比較曲線だけは旧式を現行S³体積へ合わせた値です。その他は完全Nieh–Yan項を選択した `FULL` の出力です。`stationary_points.csv` の値と達成性ラベルは、共通の分類器による半径・形状の二変数分類（α＝0）から得ています。定理3により、非正のαすべてで同じ結果になります。Nilの半径極小は形状固定の断面に対するもので、半径・形状の二変数最小ではありません。`small_radius` と `nil_torus` の図ではUをc_M Lで割っています。CSVは割る前のUです。

再現方法は[計算コードの説明](../../script/README_ja.md)を参照してください。有限標本と解析証明は区別します。

本データはLevi-Civita（LC）Weyl項で計算したものです。本文第4節の恒等式により、指定された静的一様族では既約Einstein–Cartan（EC）Weyl作用にも適用できます。Ricciトレース除去EC曲率作用のデータではありません。
