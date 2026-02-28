# DPPUv2 計算エンジン v4 — スクリプトディレクトリ

⇒ [English](README.md)

**論文**: "Structural Robustness of Isotropic S³ Vacua in Einstein-Cartan Minisuperspace via Chiral Equilibrium and Weyl Stability"（paper02）

Einstein-Cartan + Nieh-Yan + Weyl 拡張 minisuperspace における数値・記号計算のための Python パッケージ群と実行スクリプト。

---

## ディレクトリ構成

```
script/
├── dppu/                      # メインPythonパッケージ（DPPUv2 Engine v4）
│   ├── geometry/              # 計量・体積形式・構造定数
│   ├── connection/            # Levi-Civita接続・Contortion・EC接続
│   ├── curvature/             # Riemann・Ricci・Hodge双対・自己双対性・Pontryagin・Weyl
│   ├── torsion/               # トーションモード・Ansatz・Nieh-Yan密度
│   ├── action/                # ラグランジアン・有効ポテンシャル・安定性分類
│   ├── topology/              # S³×S¹・T³×S¹・Nil³×S¹ エンジン
│   ├── engine/                # 計算パイプライン・ロギング・チェックポイント
│   ├── scanning/              # パラメータスキャン・Squashing走査・Phase1統合
│   └── utils/                 # 共通ユーティリティ（Levi-Civita記号・記号計算）
│
└── scripts/                   # 実行スクリプト
    ├── pipeline/              # トポロジー別ランナー・パラメータスキャン
    ├── paper02/               # paper02 固有の解析スクリプト
    ├── proofs/                # 解析的・記号的証明スクリプト
    └── visualize/             # 図生成 Jupyter Notebook
```

### `docs/` - ドキュメント

技術ドキュメントと規約：
- [DPPUv2 Engine CONVENTIONS](docs/CONVENTIONS_ja.md) - エンジンコアの規約と仕様
- [DPPUv2 SymPy guideline](docs/SymPy_guideline_ja.md) - SymPy使用ガイドラインとベストプラクティス

---

## パッケージ概要（dppu/）

| モジュール | 役割 | 主要クラス・関数 |
|-----------|------|----------------|
| [`geometry`](dppu/geometry/README_ja.md) | 計量・フレーム場定義 | `build_metric`, `frame_field` |
| [`connection`](dppu/connection/README_ja.md) | EC接続の構築 | `levi_civita`, `contortion`, `ec_connection` |
| [`curvature`](dppu/curvature/README_ja.md) | 曲率テンソル群・SD診断 | `RiemannTensor`, `SDExtensionMixin`, `compute_pontryagin_inner_product` |
| [`torsion`](dppu/torsion/README_ja.md) | トーション構造 | `Mode`, `NyVariant`, `build_torsion_tensor` |
| [`action`](dppu/action/README_ja.md) | 作用・安定性解析 | `build_lagrangian`, `classify_stability` |
| [`topology`](dppu/topology/README_ja.md) | 3トポロジーエンジン | `S3S1Engine`, `T3S1Engine`, `Nil3S1Engine` |
| [`engine`](dppu/engine/README_ja.md) | 15ステップ計算パイプライン | `BaseFrameEngine`, `ComputationLogger`, `CheckpointManager` |
| [`scanning`](dppu/scanning/README_ja.md) | パラメータ空間走査 | `run_scan`, `Phase1ResultsLoader`, `SDDiagnosticsWithPhase1` |
| [`utils`](dppu/utils/README_ja.md) | 共通ユーティリティ | `LeviCivita`, `symbolic_simplify` |

---

## 実行スクリプト概要（scripts/）

### pipeline/ — トポロジー別ランナー

| スクリプト | 説明 |
|-----------|------|
| `run_s3s1.py` | S³×S¹ エンジンを単一パラメータで実行 |
| `run_t3s1.py` | T³×S¹ エンジンを実行 |
| `run_nil3s1.py` | Nil³×S¹ エンジンを実行 |
| `run_parameter_scan.py` | (V, η, θ) パラメータ空間のグリッドスキャン |
| `run_mode_ny_scan.py` | トーションモード × NYバリアントの組み合わせスキャン |
| `run_sd_analysis.py` | 自己双対性（SD）診断の実行 |
| `run_pontryagin_diagnostic.py` | Pontryagin内積 P = ⟨R, *R⟩ の診断（`--input-dir` に `run_parameter_scan_*.csv` があれば自動検出・トポロジー別フィルタ適用） |
| `run_alpha_boundary_scan.py` | (V, η, θ_NY) を変化させて α = 0 安定性境界のパラメータ独立性を検証（Theorem 3） |

### paper02/ — paper02 固有解析

| スクリプト | 説明 |
|-----------|------|
| `potential_landscape_mapping.py` | (r, ε) ポテンシャル地形の生成（複数のα値） |
| `critical_analysis.py` | α = 0 相転移点付近の高解像度解析（ε*・r*・Vmin の追跡） |
| `topology_comparison.py` | S³・T³・Nil³ のポテンシャル比較（Weyl拡張下） |
| `optimization_helper.py` | 大域的最小値探索のユーティリティ |

### proofs/ — 解析的・記号的証明

| スクリプト | 証明内容 |
|-----------|---------|
| `analytic_proof_P_equals_zero.py` | **Proposition 1**: P = ⟨R, *R⟩ ≡ 0 の代数的証明（.log 出力あり） |
| `symbolic_block_all_topologies.py` | **Proposition 1** 記号的検証: 全トポロジー（S³・T³・Nil³）のブロック構造一括検証（.log 出力あり） |
| `analytical_proof.py` | **Lemma 1** SymPy 証明: C²(ε=0)=0・∂C²/∂ε|₀=0・∂²C²/∂ε²|₀>0 の記号的確認（論文 Appendix C.5 対応、.log 出力あり） |

### visualize/ — 図生成・インタラクティブビューア

| ファイル | 内容 |
|---------|------|
| `DPPUv2_Paper_Figures.ipynb` | paper02 の論文図を生成する Jupyter Notebook |
| `DPPUv2_visualize_notebook_v4.ipynb` | インタラクティブな相図と有効ポテンシャルの Jupyter Notebook |
| `DPPUv2_interactive_viewer_v4.py` | Jupyter 上で動作するインタラクティブ相図・ポテンシャルビューア（`%matplotlib widget` が必要） |

---

## クイックスタート

### 依存関係のインストール

```bash
pip install sympy numpy scipy pandas tqdm matplotlib
```

### 単一トポロジーの実行

```bash
# script/ ディレクトリで実行（出力先: output/run_s3s1_YYYYMMDD_HHMMSS.log）
python scripts/pipeline/run_s3s1.py --mode MX --ny-variant FULL
python scripts/pipeline/run_t3s1.py --mode MX --ny-variant FULL
python scripts/pipeline/run_nil3s1.py --mode MX --ny-variant FULL

# 出力先を指定する場合
python scripts/pipeline/run_s3s1.py --mode MX --ny-variant FULL --output-dir results/
```

### Proposition 1 の記号的証明

```bash
# Proposition 1: P = 0 の代数的証明（output/analytic_proof_P_equals_zero_TIMESTAMP.log を生成）
python scripts/proofs/analytic_proof_P_equals_zero.py

# Proposition 1: 全トポロジー（S³・T³・Nil³）記号的ブロック構造検証
python scripts/proofs/symbolic_block_all_topologies.py

# Lemma 1: C²(ε=0)=0・∂C²/∂ε|₀=0・∂²C²/∂ε²|₀>0 の SymPy 記号的証明（AppC.5 対応）
python scripts/proofs/analytical_proof.py

# 出力先を指定する場合（全 proofs/ スクリプト共通）
python scripts/proofs/analytic_proof_P_equals_zero.py --output-dir proof_logs/
```

### Weyl 拡張解析（paper02 主要結果）

```bash
# (r, ε) ポテンシャル地形のマッピング（全 alpha 値を 1 CSV に統合）
python scripts/paper02/potential_landscape_mapping.py --topology S3

# α = 0 臨界解析
python scripts/paper02/critical_analysis.py

# トポロジー比較
python scripts/paper02/topology_comparison.py

# 出力先を指定する場合（全 paper02 スクリプト共通）
python scripts/paper02/critical_analysis.py --output-dir paper02_results/
```

### パラメータスキャン・診断（Phase1 統合）

```bash
# グリッドスキャン（出力: run_parameter_scan_TIMESTAMP.csv）
python scripts/pipeline/run_parameter_scan.py --output-dir output/

# SD診断（結果を run_sd_analysis_TIMESTAMP.csv に保存）
python scripts/pipeline/run_sd_analysis.py \
    --input-csv output/run_parameter_scan_20260228_120000.csv \
    --theta 0.0 --output-dir output/

# Pontryagin 診断（結果を run_pontryagin_diagnostic_TIMESTAMP.csv に保存）
# ※ output/ に run_parameter_scan_*.csv があれば自動検出・トポロジー別フィルタが適用される
python scripts/pipeline/run_pontryagin_diagnostic.py \
    --input-dir output/ --output-dir output/

# Mode/NyVariant スキャン
python scripts/pipeline/run_mode_ny_scan.py --output-dir output/
```

### α = 0 境界パラメータ独立性スキャン（Theorem 3）

```bash
# Theorem 3 数値検証: V, η, θ_NY を変化させても α = 0 境界が不変であることを確認
# 出力: run_alpha_boundary_scan_TIMESTAMP.csv
python scripts/pipeline/run_alpha_boundary_scan.py --topology S3 --output-dir output/
```

### Python API から直接使用

```python
from dppu.topology import S3S1Engine
from dppu.torsion import Mode, NyVariant
from dppu.engine import ComputationLogger

logger = ComputationLogger('run.log')
engine = S3S1Engine(Mode.MX, NyVariant.FULL, logger)
engine.run()
```

---

## paper02 の主要結果と対応スクリプト

| 結果 | 論文箇所 | 内容（証明種別） | 対応スクリプト |
|-----|---------|----------------|--------------|
| **Proposition 1** | §3 | P = ⟨R, *R⟩ ≡ 0（カイラル均衡）**解析的証明**（幾何学的直交分解） | `proofs/analytic_proof_P_equals_zero.py` |
| **Proposition 1** 記号的検証 | §3.5 | 全トポロジー・全Mode・全NyVariantで P = 0 を**記号的に確認** | `proofs/symbolic_block_all_topologies.py`、`pipeline/run_mode_ny_scan.py`、`pipeline/run_pontryagin_diagnostic.py` |
| **Lemma 1** | §4・AppC | C²(r, ε) 閉形式を**記号的に導出**（SymPy、厳密計算） | `proofs/analytical_proof.py` |
| **Theorem 1** | §5 | α ≤ 0 での等方真空 Weyl 安定性 — **解析的証明** + **数値検証**（201点・11桁一致） | `paper02/potential_landscape_mapping.py`、`paper02/critical_analysis.py` |
| **Theorem 2** | §6 | α > 0 での下に非有界な不安定性 — **解析的証明**（漸近スケーリング）+ **数値検証**（境界収束確認） | `paper02/critical_analysis.py` |
| **Theorem 3** | §7 | 安定性境界 α = 0 のパラメータ（V, η, θ_NY）独立性 — **解析的証明**（幾何的分離・漸近支配）+ **数値検証**（4パラメータセット） | `pipeline/run_alpha_boundary_scan.py` |
| **Topology Comparison** | §8 | Weyl 拡張下での S³ 優位性・T³ null test・Nil³ 漸近挙動（**数値解析**） | `paper02/topology_comparison.py` |

---

## トポロジー一覧

| トポロジー | Lie群 | 背景曲率 | Koszul公式 |
|-----------|-------|---------|-----------|
| S³×S¹ | SU(2) | +24/r² | 簡略 |
| T³×S¹ | U(1)³ | 0 (平坦) | 自明 |
| Nil³×S¹ | Heisenberg群 | −1/(2R²) | 一般（bi-invariant 非成立） |

---

## 出力ファイル規則

全実行スクリプトは以下の規則に従って出力を統一しています。

| 規則 | 内容 |
|------|------|
| オプション | `--output-dir OUTPUT_DIR`（デフォルト: `output`） |
| ファイル名 | `{モジュール名}_{YYYYMMDD_HHMMSS}.{拡張子}` |
| 出力先 | `OUTPUT_DIR` 直下（サブディレクトリなし） |
| ディレクトリ | 実行時に自動作成（`exist_ok=True`） |

| スクリプト種別 | 出力ファイル例 |
|--------------|------------|
| run_s3s1/t3s1/nil3s1.py | `run_s3s1_20260228_153045.log` |
| run_alpha_boundary_scan.py | `run_alpha_boundary_scan_20260228_153045.csv` |
| run_mode_ny_scan.py | `run_mode_ny_scan_20260228_153045.csv` |
| run_sd_analysis.py | `run_sd_analysis_20260228_153045.csv` |
| run_pontryagin_diagnostic.py | `run_pontryagin_diagnostic_20260228_153045.csv` |
| potential_landscape_mapping.py | `potential_landscape_mapping_20260228_153045.csv` |
| critical_analysis.py (paper02) | `critical_analysis_20260228_153045.csv` |
| topology_comparison.py | `topology_comparison_20260228_153045.csv` |
| analytic_proof_P_equals_zero.py | `analytic_proof_P_equals_zero_20260228_153045.log` |
| analytical_proof.py | `analytical_proof_20260228_153045.log` |
| run_parameter_scan.py | `run_parameter_scan_20260228_153045.csv` |
| symbolic_block_all_topologies.py | `symbolic_block_all_topologies_20260228_153045.log` |

---

## チェックポイント機能

長時間計算の中断・再開が可能:

```bash
# チェックポイント付きで実行（--output-dir と独立して指定）
python scripts/pipeline/run_s3s1.py --mode MX --ny-variant FULL \
    --output-dir output/ --checkpoint-dir ./checkpoints

# 中断後の再開（チェックポイントディレクトリを再指定するだけで自動再開）
python scripts/pipeline/run_s3s1.py --mode MX --ny-variant FULL \
    --output-dir output/ --checkpoint-dir ./checkpoints
```
---
## ライセンス

リポジトリルートのLICENSEファイルを参照してください。

---

**Author**: Muacca
**Version**: DPPUv2 Engine v4
**Date**: 2026-02

