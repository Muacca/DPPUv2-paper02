# 作用とポテンシャル

[English](README.md)

`compute_lagrangian`はEC スカラー・NY・選択された曲率二乗項を合成し、`compute_action`が指定体積を掛け、`compute_effective_potential`がU=-Sを作ります。半径・形状の分類は`dppu.scanning.classify_configuration`を使います。

[規約](../../docs/CONVENTIONS_ja.md) / [利用方法](../../README_ja.md) / [分類仕様](../../docs/CLASSIFICATION_ja.md)

[曲率モデルと保存キー](../../docs/WEYL_MODELS_ja.md)。選択作用はquadratic_scalarを使い、既定はEC_IRR。従来のweyl_scalarキーはLC基準を保持する。
