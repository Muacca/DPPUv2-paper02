## Appendix A: DPPUv2 Engine v4 Specification

本付録では、計算に用いた DPPUv2 計算エンジン v4 の仕様と、信頼性の検証結果を記述する。

### A.1 エンジンの概要

DPPUv2 計算エンジン v4 は、EC+NY+Weyl 理論の minisuperspace 還元を実行する記号・数値計算エンジンである。paper01 の EC+NY 実装を基盤とし、本稿のために以下の拡張を実装した:

1. **Squashed ansatz の導入**: 異方性パラメータ $\varepsilon$ を含む squashed coframe を導入し、2変数 $(r, \varepsilon)$ の有効ポテンシャル計算を実装。
2. **Levi-Civita 接続に基づく Weyl テンソルの計算**: Levi-Civita 接続から Weyl テンソルの全成分と $C^2$ スカラーを記号的に計算する機能を追加。
3. **物理層別モジュール構成と整合性検証の自動実行**: Levi-Civita 接続層、EC 接続層、Weyl テンソル層、有効ポテンシャル層を分離し、各層の独立検証を可能にした。3段階の整合性検証（§A.3）を自動実行する構成とした。

### A.2 計算フロー

#### 理論構築（記号計算）

1. **幾何学的セットアップ**: トポロジーに応じた構造定数 $C^i{}_{jk}$ の設定
2. **Levi-Civita 接続**: Koszul 公式 $\Gamma^{a}{}\_{bc} = \frac{1}{2}(C^{a}{}\_{bc} + C^{c}{}\_{ba} - C^{b}{}\_{ac})$
3. **Contortion の導出**: Torsion ansatz から $K_{abc} = \frac{1}{2}(T_{abc} + T_{bca} - T_{cab})$
4. **EC 接続の構成**: $\Gamma^a_{\rm EC,bc} = \Gamma^a_{\rm LC,bc} + K^a{}_{bc}$
5. **スカラー量の計算**: $R_{\rm EC}$, $T_{abc}T^{abc}$, $N_{\rm TT}$, $N_{\rm REE}$, $N_{\rm FULL}$
6. **Weyl テンソルの計算**: Levi-Civita 接続から $R^{a}{}\_{bcd} \to R\_{bd} \to R \to C\_{abcd} \to C^2$
7. **有効ポテンシャルの組み立て**: $V_{\rm eff} = -\mathcal{L} \times \mathrm{Vol}$

#### 数値探索

1. **パラメータ走査**: $\alpha \in [-1, 1]$（201点）, $(r, \varepsilon)$ の2次元グリッド
2. **最適化**: `scipy.optimize.brute`（Ns=20）によるグリッド探索 + マルチスタート L-BFGS-B
3. **分類**: 最適化結果に基づく安定性判定（converged フラグ、境界張り付き判定）

### A.3 整合性検証（自動実行）

エンジンは各計算ステップで以下の検証を自動実行する:

#### Level 1: Metric Compatibility

$$\nabla_c\, g_{ab} = 0$$

EC 接続が frame metric $\eta_{ab} = \delta_{ab}$ と整合することを検証。

#### Level 2: Riemann テンソルの反対称性

$$R_{abcd} = -R_{abdc} = -R_{bacd} = R_{cdab}$$

全成分について3つの対称性条件を検証。

#### Level 3: スカラー量の解析的既知値との比較

- $S^3$: $R_{\rm LC}(r, 0) = 24/r^2$ との一致
- $T^3$: $R_{\rm LC} = 0$, $C^2 = 0$ の確認
- $S^3$: $C^2(r, 0) = 0$（等方点での共形的平坦性）の確認

### A.4 $T^3$ Null Test: エンジンの健全性検証

$T^3$ は $C^2 = 0$ であるため、有効ポテンシャルに $\alpha$ 依存性は現れないはずである。数値計算で全201点（ $\alpha \in [-1, 1]$）における結果の一致（機械精度）を確認した（§8.3 参照）。

この null test は以下の整合性チェックとして機能する:

1. $\alpha$ の実装が正しい（ $\alpha C^2$ 項が正確に加算されている）
2. $C^2 = 0$ のトポロジーで Weyl 項が残留しない
3. 数値精度が機械精度レベルで維持されている

