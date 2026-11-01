# 計算pipeline

[English](README.md)

`BaseFrameEngine(mode, ny_variant, logger=None, checkpoint_mgr=None, *, curvature_model='EC_IRR')`は接続、LC/EC曲率、NY、作用、Uを計算する。`run()`は登録された各stepを実行し、checkpoint読込は別の明示操作。`get_effective_potential_function()`はAX/VTの不活性引数も含むf(r,V,eta,theta_NY,L,kappa,epsilon,α)を返す。旧来のdataキーtorsion_tensorの内容は幾何学的Tではなくτ。

[Conventions](../../docs/CONVENTIONS_ja.md) / [Usage](../../README_ja.md)

[曲率モデルと保存キー](../../docs/WEYL_MODELS_ja.md)。選択作用はquadratic_scalarを使い、既定はEC_IRR。従来のweyl_scalarキーはLC基準を保持する。
