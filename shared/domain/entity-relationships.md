# エンティティ関係図

**目的**: ドメインオブジェクト間の関係性定義  
**対象**: 全実装で共通のデータ関係

---

## 🔗 主要関係図

```
User
├── 1:N → Novel (作者として)
├── 1:N → Comment (投稿者として)
├── 1:N → Rating (評価者として)
└── N:M → Novel (フォロー関係)

Novel
├── 1:N → Chapter
├── 1:N → Setting
├── 1:N → Comment
├── 1:N → Collaboration
├── N:M → Tag
└── N:1 → Category

Chapter
└── 1:N → Episode

Setting
└── N:M → Setting (相互関係)
```

## 📋 関係性ルール

### 必須関係
- Novel → User (作者): 必須
- Chapter → Novel: 必須  
- Episode → Chapter: 必須

### 任意関係
- Novel → Tag: 0-10個
- Novel → Setting: 0-N個
- User → Comment: 0-N個

---

**実装注意**: 各DBの特性に応じて最適な関係表現を選択
