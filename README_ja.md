# 既約EC-Weyl補正を持つEinstein–Cartan–Nieh–Yan minisuperspaceの曲率恒等式と縮約ポテンシャルの有界性

ECはEinstein–Cartan、LCはLevi-Civita、NYはNieh–Yanの略記です。


[English](README.md)

S³・T³・Nil³の静的一様な幾何で、既約EC-WeylとLC-Weylの項が縮約ポテンシャルの半径・形状依存へ与える効果を解析する論文の本文・コード・図表データです。S³の形状差の厳密な因数分解を中心に、固定捩率パラメータと円周長の下で最小値の存在と達成性を分類します。

**v2 — 2026-11-01改訂。** 作用・規約・結論の版間の変更は[CHANGELOG](CHANGELOG.md)、旧代表式との比較は[付録D](DPPUv2-paper02_appD.md)を参照してください。

Zenodoの記録：v1（2026-02-28）は[10.5281/zenodo.18815499](https://doi.org/10.5281/zenodo.18815499)です。全版共通の[10.5281/zenodo.18815498](https://doi.org/10.5281/zenodo.18815498)は、最新の登録版を指します。引用時は本文の版と日付を併記してください。

| 資料 | 内容 |
|---|---|
| [English PDF](DPPUv2-paper02.pdf) | v2本文・証明・図表・付録 |
| [LaTeX](LaTeX/main.tex) | 英語原稿 |
| [Code](script/README_ja.md) | 計算・図の再現・viewer |
| [Conventions](script/docs/CONVENTIONS_ja.md) | 局所・大域規約と固定量 |
| [Data](data/revised/README_ja.md) | 訂正後の図1〜4・表のデータ |

- [第1節](DPPUv2-paper02_sec01.md)
- [第2節](DPPUv2-paper02_sec02.md)
- [第3節](DPPUv2-paper02_sec03.md)
- [第4節](DPPUv2-paper02_sec04.md)
- [第5節](DPPUv2-paper02_sec05.md)
- [第6節](DPPUv2-paper02_sec06.md)
- [第7節](DPPUv2-paper02_sec07.md)
- [第8節](DPPUv2-paper02_sec08.md)
- [第9節](DPPUv2-paper02_sec09.md)
- [第10節](DPPUv2-paper02_sec10.md)

[Appendix A](DPPUv2-paper02_appA.md) / [Appendix B](DPPUv2-paper02_appB.md) / [Appendix C](DPPUv2-paper02_appC.md) / [Appendix D](DPPUv2-paper02_appD.md)

## 作用と分類

主対象は既約EC-Weyl作用です。指定した静的族ではLC-Weylとテンソルとして一致し、縮約ポテンシャルと半径・形状の分類も共通です。Ricciトレース除去EC曲率作用は第4節で短く比較します。[定義とコードの選択](script/docs/WEYL_MODELS_ja.md)。

scanとviewerは[二変数領域と固定形状の分類](script/docs/CLASSIFICATION_ja.md)を共有し、未達成下限・退化最小も区別します。

## 図の再現

リポジトリ直下から実行します。renderは同梱データを使い、recomputeは現行engineでデータも計算します。出力先は新しいフォルダを指定します。

```powershell
python -m pip install -r script/requirements.txt
python -B script/scripts/paper02/reproduce_figures.py render --output-dir rendered_figures
python -B script/scripts/paper02/reproduce_figures.py recompute --output-dir recomputed_figures
```

現行論文、データ、engine、runner、記号計算補足、viewerを収録しています。以前の出力と探索コードはGit履歴に保持し、添付資料には含めません。コード入力は幾何学的捩率の符号反転です。版変更後はnotebookのkernelを再起動してください。

## PDFの作成

```powershell
Push-Location LaTeX
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
Pop-Location
```

生成先はLaTeX/main.pdfです。ルートのPDFはこのコマンドでは置換しません。

## 著者・ライセンス

Muacca. [LICENSE](LICENSE.txt).
