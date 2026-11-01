# 計算コードと再現手順

ECはEinstein–Cartan、LCはLevi-Civita、NYはNieh–Yanの略記です。


[English](README.md)

Paper02 v2に対応します。 [Conventions](docs/CONVENTIONS_ja.md) / [LaTeX原稿](../LaTeX/main.tex)

```powershell
python -m pip install -r script/requirements.txt
python -B script/scripts/paper02/reproduce_figures.py render --output-dir rendered_figures
python -B script/scripts/paper02/reproduce_figures.py recompute --output-dir recomputed_figures
python -B script/scripts/pipeline/run_parameter_scan.py --topologies S3 T3 Nil3 --ny-variants FULL --V-range 0 4 3 --eta-range -3 3 7 --alpha -0.1 0 0.1 --workers 1 --output-dir new_scan
```

上記はリポジトリ直下から実行します。renderは保存データから図だけを作り、recomputeは公開engineからデータも計算します。既存の図出力フォルダは上書きしません。

| 入口 | 機能・範囲 |
|---|---|
| `dppu/topology` | S3S1Engine, T3S1Engine, Nil3S1Engine |
| `scripts/pipeline/run_s3s1.py` / `run_t3s1.py` / `run_nil3s1.py` | 指定modeとNY variantのsymbolic計算 |
| `scripts/pipeline/run_parameter_scan.py` | 半径・形状全体の分類と固定形状の半径分類 |
| `scripts/proofs/analytical_proof.py` | LC-Weyl式の独立したsymbolic計算 |
| `scripts/proofs/symbolic_block_all_topologies.py` | 指定した3幾何・静的一様ansatzのEC曲率block構造 |
| [Figure notebook](scripts/visualize/DPPUv2_Paper_Figures.ipynb) | 保存データ描画と明示的再計算を別セルで実行 |
| [Viewer notebook](scripts/visualize/DPPUv2_visualize_notebook_v4.ipynb) | 共通の解析分類と現行engineのポテンシャル曲線 |

コードのV,etaはτ規約、本文のη,Vはその符号反転です。

```python
import sys
sys.path.insert(0, 'script')
from dppu.topology.s3s1 import S3S1Engine
from dppu.torsion.mode import Mode
from dppu.torsion.nieh_yan import NyVariant
engine = S3S1Engine(Mode.MX, NyVariant.FULL)
engine.run()
U = engine.get_effective_potential_function()
# r, V_code, eta_code, theta_NY, L, kappa, epsilon, alpha
print(U(2, 4, -2, 1, 1, 1, 0, 0))
```

捩率modeはMX（両成分を許す）、AX（軸性のみ）、VT（ベクトルトレースのみ）で、全て零振幅を許す。NY選択はFULL（完全な差）、TT（正符号の捩率積の体積係数）、REE（正符号の曲率・coframe収縮の体積係数）に実結合θを掛ける。AXではV、VTではetaのcallable引数が無視されます。engine.dataの主要キーは `potential`、`riemann`、`ricci_scalar`、`quadratic_scalar`、`ny_density_full` です。`weyl_scalar` はLC基準の意味を保持します。

現行の図・表データは[data/revised](../data/revised/README_ja.md)にあります。出力先は新しいフォルダを指定します。checkpointのloadは明示操作であり、engine.runは保存状態を自動読込しません。notebookの保存出力は空で、source更新後はkernelを再起動します。

[分類とCSV仕様](docs/CLASSIFICATION_ja.md)を参照してください。scanとviewerは有限最小・未達成下限・退化最小・非有界を、二変数領域と固定形状の半径断面で別々に分類します。TT/REEは本文の分類の適用外です。入力を丸めず、描画範囲で分類を切り捨てません。

## 記号計算補足とnotebook

リポジトリ直下から、新しい出力先を指定して実行します。

```powershell
python -B script/scripts/pipeline/run_s3s1.py --mode MX --ny-variant FULL --output-dir new_s3
python -B script/scripts/pipeline/run_t3s1.py --mode MX --ny-variant FULL --output-dir new_t3
python -B script/scripts/pipeline/run_nil3s1.py --mode MX --ny-variant FULL --output-dir new_nil
python -B script/scripts/proofs/analytical_proof.py --output-dir new_weyl
python -B script/scripts/proofs/symbolic_block_all_topologies.py --output-dir new_blocks
```

notebookはJupyter環境で開きます。viewer notebookは作業ディレクトリからリポジトリを探し、ipymplのwidget backendを使います。Applyで両panelを更新し、選択点表には二つの領域の分類を表示します。図notebookはリポジトリ直下または配下から実行できます。既定は同梱データの描画であり、再計算は`RECOMPUTE=True`で明示します。

## 計算資料

[計算規約](docs/CONVENTIONS_ja.md)は添字・符号・大域幾何と形状、[実装ガイド](docs/SymPy_guideline_ja.md)は記号計算・API、[分類仕様](docs/CLASSIFICATION_ja.md)は二変数/半径方向・CSV・viewerを説明します。公開ライブラリは現行の計算・再現経路を収録しています。公開計算はSciPyを必要としません。

[曲率二乗モデル](docs/WEYL_MODELS_ja.md)

engine・runner・scan・viewerの既定はEC_IRR（既約EC-Weyl）。比較基準はLC、Ricciトレース除去EC曲率作用はEC_TRACEFREEで明示選択する。掲載図データはLCの来歴を維持し、指定族では既約EC-Weyl作用も表す。作用はquadratic_scalarを使い、weyl_scalarはLCの互換キーを保持する。
