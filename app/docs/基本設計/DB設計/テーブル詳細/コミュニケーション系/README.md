# コミュニケーション系テーブル詳細

---

## 概要
コミュニケーション系テーブルは、小説投稿サイトのユーザー間コミュニケーションに関する全てのテーブルを管理します。

---

## 設計方針
- master_classesは分類定義テーブルで一元管理し、データの整合性を保証
- コメントは共通テーブル方式（target_type, target_id）で管理し、作品・設定・話など多様な対象に柔軟に対応
- レビューや通知も、対象ごとにtarget_type/target_idで管理する設計を推奨
- 論理削除（deleted_at）カラムを持たせ、物理削除は原則行わず、必要に応じてアーカイブ
- 履歴や編集情報は必要に応じて履歴テーブルで管理
- 返信機能は番号指定で簡素化（将来的に階層構造に拡張可能）
- コメントは自動承認、通報による自動削除で運用

---

## テーブル一覧

### コメント・評価
- [comments.md](./comments.md) - コメントテーブル
- [reviews.md](./reviews.md) - レビューテーブル
- [evaluations.md](./evaluations.md) - 評価テーブル（コメント・レビュー共通）

### 通知
- [notifications.md](./notifications.md) - 通知テーブル

---

## テーブル関係図

```
master_classes (1) ←→ (N) comments
master_classes (1) ←→ (N) reviews
master_classes (1) ←→ (N) notifications
master_classes (1) ←→ (N) evaluations
master_classes (1) ←→ (N) reports

users (1) ←→ (N) comments
users (1) ←→ (N) reviews
users (1) ←→ (N) notifications
users (1) ←→ (N) evaluations

comments (1) ←→ (N) comments (reply_to_number)
comments (1) ←→ (N) evaluations (target_type=0)
reviews (1) ←→ (N) evaluations (target_type=4)
```

---

## 主要な考慮点
- コメントの返信機能の簡素化（番号指定）
- 自動承認による運用負荷の軽減
- 通報による自動削除機能
- Good/Bad評価によるユーザーエンゲージメント向上
- 通知の効率的な管理
- スパム対策とモデレーション機能 