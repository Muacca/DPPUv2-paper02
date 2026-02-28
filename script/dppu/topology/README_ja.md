# Topology Layer

⇒ [English](README.md)

トポロジー固有の計算エンジンを提供するモジュール群。

## 概要

3つのトポロジー（S³×S¹, T³×S¹, Nil³×S¹）それぞれに特化した計算エンジン。

## モジュール

### s3s1.py

**S³×S¹ (3-sphere × circle) エンジン**

**数学的構造:**

- Lie群: SU(2)
- 構造定数: C^i_{jk} = (4/r)ε_{ijk}
- 計量: bi-invariant
- 背景曲率: R_LC = 24/r² (正)

**体積:**
```
V = 2π²Lr³
```

**使用例:**
```python
from dppu.topology import S3S1Engine
from dppu.torsion import Mode, NyVariant

engine = S3S1Engine(Mode.MX, NyVariant.FULL)
engine.run()
```

### t3s1.py

**T³×S¹ (3-torus × circle) エンジン**

**数学的構造:**

- Lie群: U(1)³ (Abelian)
- 構造定数: 全てゼロ
- 計量: flat
- 背景曲率: R_LC = 0

**体積:**
```
V = (2π)⁴LR₁R₂R₃
```

等方的スケーリング R₁ = R₂ = R₃ = r を使用。

**使用例:**
```python
from dppu.topology import T3S1Engine

engine = T3S1Engine(Mode.MX, NyVariant.FULL)
engine.run()
```

### nil3s1.py

**Nil³×S¹ (Heisenberg nilmanifold × circle) エンジン**

**数学的構造:**

- Lie群: Heisenberg群
- 構造定数: [E₀, E₁] = (1/R)E₂
- 計量: left-invariant（**NOT bi-invariant**）
- 背景曲率: R_LC = -1/(2R²) (負)

**体積:**
```
V = (2π)⁴LR³
```

**重要な注意:**

Nil³はbi-invariant計量を持たないため、一般Koszul公式を使用:
```
Γ^a_{bc} = (1/2)(C^a_{bc} + η^{ad}η_{be}C^e_{dc} - η^{ad}η_{ce}C^e_{bd})
```

**使用例:**
```python
from dppu.topology import Nil3S1Engine

engine = Nil3S1Engine(Mode.MX, NyVariant.FULL)
engine.run()
```

## エンジン共通インターフェース

全エンジンは`BaseFrameEngine`を継承し、統一されたインターフェースを提供:

```python
class BaseFrameEngine:
    def run(self):
        """15ステップの計算パイプラインを実行"""

    def get_R_ab_cd_numerical(self, params):
        """R^{ab}_{cd}を数値評価"""

    def get_effective_potential(self, params):
        """有効ポテンシャルを取得"""
```

## トポロジー比較

| プロパティ | S³×S¹ | T³×S¹ | Nil³×S¹ |
|-----------|-------|-------|---------|
| 構造定数 | ε_{ijk} | 0 | [E₀,E₁]=E₂ |
| 背景曲率 | +24/r² | 0 | -1/(2R²) |
| bi-invariant | Yes | Yes | **No** |
| Koszul公式 | 簡略 | 自明 | 一般 |

## 依存関係

- [engine](../engine/README_ja.md): BaseFrameEngine
- [geometry](../geometry/README_ja.md): 計量定義
- [connection](../connection/README_ja.md): 接続計算
- [curvature](../curvature/README_ja.md): 曲率計算
- [torsion](../torsion/README_ja.md): トーション構成
- [action](../action/README_ja.md): 作用と安定性
