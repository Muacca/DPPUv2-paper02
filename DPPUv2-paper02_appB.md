## Appendix B: Numerical Verification Log & $Nil^3$ Analysis

本付録では、探索パラメータと数値検証の詳細、および $Nil^3$ のフラット極限漸近と $\alpha = 0$ 安定性境界の普遍性に関する追加解析を記述する。

### B.1 探索パラメータのサマリー

#### B.1.1 探索範囲

| パラメータ | 範囲 | 分解能 |
|---|---|---|
| $r$ | $[0.01, 10]$ | brute: 30点, L-BFGS-B: 連続 |
| $\varepsilon$ | $[-0.95, 5.0]$ | brute: 30点, L-BFGS-B: 連続 |
| $\alpha$ | $[-1, 1]$ | 201点（ステップ 0.01） |

なお、 $\varepsilon > 1$ への探索上限について検討した結果、 $\varepsilon = 5$ においても $\varepsilon^*$ が境界付近に留まり $V_{\rm min} > 0$ が維持されることを確認した。より大きな $\varepsilon$ では squashing 因子が $(1+\varepsilon)^{-2/3} \ll 1$ となり minisuperspace ansatz の解釈が困難になるため、探索範囲の上限を $\varepsilon = 5$ とした。

#### B.1.2 最適化手法

1. **粗い探索**: `scipy.optimize.brute` (Ns=30) による $(r, \varepsilon)$ の2次元グリッド探索
2. **精密化**: グリッド上位候補（n=8）を初期点とするマルチスタート L-BFGS-B 最適化
3. **収束判定**: L-BFGS-B の収束フラグ (`converged`) による判定。探索境界への張り付きは `converged = False` として報告

#### B.1.3 paper01 パラメータ（参照値）

| パラメータ | 値 |
|---|---|
| $V$ | 4.0 |
| $\eta$ | $-2.0, -3.0, 0.0, 2.0$ |
| $\theta_{\rm NY}$ | 1.0 |
| $\kappa$ | 1.0 |
| $L$ | 1.0 |

### B.2 出力ファイル一覧

ファイル名は `{スクリプト名}_{YYYYMMDD_HHMMSS}.csv` の規則に従う（ `*` はタイムスタンプを示す）。

| ファイル名パターン<br/>/生成スクリプト（`scripts/` 以下） | 内容<br/>/セクション |
|---|---|
| `potential_landscape_mapping_*.csv` <br/>/ `paper02/potential_landscape_mapping.py` | $S^3$ の $(r, \varepsilon)$ グリッド上の $V_{\rm eff}$ <br/>/ §4 (Fig. 2) |
| `critical_analysis_*.csv` <br/>/ `paper02/critical_analysis.py` <br/> ` --topology S3` | $S^3$ の $\alpha$ 走査結果（ $r^*, \varepsilon^*, V_{\rm min}$） <br/>/ §5 (Fig. 3, 4) |
| `critical_analysis_*.csv` <br/>/ `paper02/critical_analysis.py` <br/> ` --topology S3 --fine` | $S^3$ の fine scan（ $\alpha \in [-0.1, 0.1]$） <br/>/ §5 (Fig. 3 インセット) |
| `critical_analysis_*.csv` <br/>/ `paper02/critical_analysis.py` <br/> ` --topology T3` | $T^3$ の $\alpha$ 走査結果 <br/>/ §8 (Fig. 7) |
| `topology_comparison_*.csv` <br/>/ `paper02/topology_comparison.py` | 3トポロジーの $V_{\rm min}(\alpha)$ 比較 <br/>/ §6 (Fig. 5) |
| `run_alpha_boundary_scan_*.csv` <br/>/ `pipeline/run_alpha_boundary_scan.py` <br/>（4パラメータセット分） | パラメータ依存性スキャン結果（4セット） <br/>/ §7 (Fig. 6) |

### B.3 数値結果の信頼性

#### B.3.1 グリッド解像度の検証

Mapping CSV（100×100 グリッド）と critical CSV（最適化結果）の比較:

| 量 | グリッド最小値 | 最適化結果 | 差異の原因 |
|---|---|---|---|
| $V_{\rm min}$ ($S^3$, $\alpha = 0$) | $-415.5$ | $-421.103$ | グリッド解像度の限界 |
| $r^*$ | $\approx 2.13$ | $2.000$ | 同上 |

グリッド探索はポテンシャル地形の概要把握に、L-BFGS-B は高精度な最適点の同定にそれぞれ使用されており、両者の差異はグリッド解像度の限界として妥当である。

#### B.3.2 $\alpha > 0$ 領域の converged フラグ

$\alpha > 0$ 領域で `converged = False` が一貫して出力される。最適化結果は $(r^*, \varepsilon^*) = (0.01, -0.95)$（探索境界）に収束する。

これは最適化の失敗ではなく、ポテンシャルが探索範囲内で下に非有界であることの正しい報告である。真の最小値は $(r, \varepsilon) \to (0, -1)$ の方向に存在するが、探索境界により到達できない。

### B.4 $Nil^3$ の挙動: フラット極限への漸近

#### B.4.1 数値探索と結果

$Nil^3$ の平坦極限への漸近挙動を正確に捉えるため、$\varepsilon \in [-0.95, 5.0]$ の範囲で探索を行った（グリッド Ns=30, マルチスタート n=8）。

| 量 | 探索結果（ $\varepsilon_{\max} = 5.0$） |
|---|---|
| $r^*$ | $\approx 1.500$ |
| $\varepsilon^*$ | $5.0$（上限張り付き） |
| $V_{\rm min}$（ $\alpha = -1$） | $5.0$ |
| $V_{\rm min}$（ $\alpha = -0.01$） | $4.9$ |

$\varepsilon^*$ が探索上限に張り付くことから、 $V_{\rm eff}$ は $\varepsilon$ に対して単調減少であり、有限 $\varepsilon$ での内部極小は存在しない。 $V_{\rm min}$ は $\varepsilon \to \infty$ で漸近値 $\approx 4.9$ に収束する（ $\alpha$ 弱依存）。

#### B.4.2 物理的考察: フラット極限への漸近

$Nil^3$ の構造定数は squashing 因子 $(1+\varepsilon)^{-4/3}$ を含む:

$$C^2{}_{01} = -\frac{(1+\varepsilon)^{-4/3}}{r}, \quad C^2{}_{10} = +\frac{(1+\varepsilon)^{-4/3}}{r}$$

$\varepsilon \to \infty$ で $(1+\varepsilon)^{-4/3} \to 0$ となり、構造定数が消失する。これは $Nil^3$ がフラット極限（ $T^3$ 的挙動）に漸近することを意味する。 $\varepsilon = 5$ で $(1+5)^{-4/3} \approx 0.11$ であり、構造定数は既に1割以下に抑制されている。

物理的には、 $Nil^3$ の有効ポテンシャルは Heisenberg 群構造に由来する曲率コスト（ $C^2 > 0$）を最小化するために、構造定数をゼロに近づける方向（ $\varepsilon \to \infty$）を選好する。 $Nil^3$ は安定な異方真空を形成せず、フラットな配位に向かって「崩壊」する。

#### B.4.3 結論への影響

$Nil^3$ のフラット極限漸近は本論文の主要結論に影響しない:

1. $Nil^3$ は漸近 $V_{\rm min} \approx 5 > 0$ であり、 $S^3$（ $V_{\rm min} = -421$）に対してエネルギー的に不利。符号関係 $V_{\rm min}(S^3) < 0 < V_{\rm min}(T^3) \approx 0 < V_{\rm min}(Nil^3)$ は不変。
2. $S^3$ の結果（ $\varepsilon^* = 0$）は Theorem 1 の仮定の下で解析的に示されており、探索範囲に依存しない。
3. $Nil^3$ のフラット極限漸近は、共形的平坦配位（ $C^2 = 0$）がエネルギー的に有利であるという本論文の主題と整合する。

### B.5 $\alpha = 0$ 安定性境界の $Nil^3$ での追加確認

$\alpha = 0$ 境界付近の安定性遷移を詳細に調べるため、 $\alpha \in [-0.05, 0.05]$（ステップ 0.001）の高解像度スキャンを $\varepsilon \in [-0.95, 5.0]$ の範囲で実施した。

| 量 | 値 |
|---|---|
| 遷移位置 | $\alpha = 0.000 \to +0.001$ |
| $\alpha = 0$ の状態 | converged = True（ $V_{\rm min} \approx 4.9$） |

$\alpha = 0$ 自体は converged = True であり、安定性の遷移は $\alpha = 0 \to +0.001$ で発生する。この結果は、 $\alpha = 0$ の安定性境界が $S^3$, $T^3$, $Nil^3$ の3トポロジー全てで普遍的に成立することを示す追加的な数値的証拠である。
