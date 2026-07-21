# エンティティ関係図

**目的**: ドメインオブジェクト間の関係性定義
**対象**: python-django実装のデータ関係
**参照**: [core-entities.md](./core-entities.md)

---

## 🔗 Phase 1 関係図

```
User
└── 1:N → Pseudonym

Pseudonym
└── 1:N → World

World
├── 1:N → Novel
├── 1:N → Setting          （World単位のSetting）
├── 1:N → SettingTemplate  （World単位のテンプレート）
└── 1:N → RelationLabel    （World固有の関係ラベル）

Novel
├── 1:N → Chapter
├── 1:N → Setting          （Novel単位のSetting。World単位とは排他）
└── 1:N → SettingTemplate  （Novel単位のテンプレート。World単位とは排他）

SettingTemplate
└── 1:N → Setting（同じスコープ内）

Setting
├── 1:N → SettingField
└── N:M → Setting（SettingRelation 経由。関係元→関係先の方向性あり、RelationLabel 付き）

RelationLabel
└── N:1 → World（World固有ラベルの場合）／システム共通マスタ（World非依存）

Chapter
└── 1:N → Episode

Episode
└── N:M → Setting（EpisodeSettingReference 経由。自動生成／手動追加）

EditHistory
└── N:1 → 各対象エンティティ（Setting / Novel / Chapter / Episode）
```

## 📋 関係性ルール

### 必須関係
- Pseudonym → User: 必須
- World → Pseudonym: 必須
- Novel → World: 必須
- Chapter → Novel: 必須
- Episode → Chapter: 必須
- Setting → World または Novel: どちらか一方が必須（排他）
- SettingTemplate → World または Novel: どちらか一方が必須（排他、Setting と同じスコープ規則）
- SettingRelation → 関係元 Setting・関係先 Setting: 両方必須
- SettingRelation → RelationLabel: 必須

### 任意関係
- Setting → SettingField: 0-N個（テンプレート由来＋個別追加）
- Setting → SettingRelation: 0-N個
- Episode → Setting（EpisodeSettingReference）: 0-N個
- RelationLabel → World: World固有ラベルの場合のみ（システム共通マスタは World を持たない）

### スコープ制約
- Setting・SettingTemplate は同一スコープ（同じ World、または同じ Novel）内でのみ相互参照する
- World単位の Setting は、その World 内のどの Novel からも参照できる
- Novel単位の Setting は、その Novel の Episode からのみ参照できる
- SettingRelation は同一 World に属する Setting 同士に限定する（World単位の Setting と、その World 配下の Novel単位の Setting との関係は可。World をまたぐ関係は不可、Phase 1 では扱わない。2026-07-21 確定）

---

## 🔗 Phase 2 以降の関係（参考、未実装）

Phase 2 で追加される Collaboration・Comment・Rating・Follow 等は、World・Novel・User との関係を持つ想定。詳細は Phase 2 計画時に定義する（[functional-scope.md](../business/functional-scope.md) 参照）。

---

**実装注意**: 実装（Django ORM）の特性に応じて最適な関係表現を選択する
