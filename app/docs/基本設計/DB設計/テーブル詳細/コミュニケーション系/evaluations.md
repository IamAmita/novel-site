# evaluations テーブル詳細

---

## 概要
ユーザーの評価（Good/Bad）を管理するテーブルです。コメント、レビューなど多様な対象への評価履歴を保持し、重複評価を防ぎます。評価対象はclass_id（master_classes.id, 2桁:10〜99）とtable_id（master_tables.id, 4桁:1000〜9999）で管理します。

---

## テーブル定義

| 属性名             | 型         | 必須 | 一意 | 説明                                 |
|--------------------|------------|------|------|--------------------------------------|
| id                 | int        | ○    | ○    | 評価ID（主キー）                     |
| class_id           | int        | ○    |      | 評価対象クラスID（master_classes.id, 2桁:10〜99） |
| table_id           | int        | ○    |      | 評価対象テーブルID（master_tables.id, 4桁:1000〜9999） |
| target_id          | int        | ○    |      | 評価対象ID                           |
| user_id            | int        | ○    |      | 評価者ID（外部キー）                 |
| evaluation_type    | tinyint    | ○    |      | 評価種別                             |
| created_at         | datetime   | ○    |      | 評価日時                             |
| updated_at         | datetime   |      |      | 更新日時                             |

---

## インデックス

| インデックス名 | 種類 | 説明 | カラム |
|----------------|------|------|--------|
| PRIMARY KEY | 主キー | 評価IDの主キー | id |
| UNIQUE | 複合一意 | 重複評価防止 | class_id, table_id, target_id, user_id |
| INDEX | 複合 | ユーザーの評価履歴検索用 | user_id, evaluation_type |
| INDEX | 複合 | 対象の評価集計用 | class_id, table_id, target_id |
| INDEX | 複合 | 評価種別別集計用 | class_id, table_id, target_id, evaluation_type |

---

## 制約条件

### 主キー制約
- `id`: 自動採番（AUTO_INCREMENT）

### 外部キー制約
- `user_id` → `users.id`: 評価者ユーザーテーブルを参照
- `class_id` → `master_classes.id`: クラス種別マスタを参照
- `table_id` → `master_tables.id`: テーブル種別マスタを参照

### ユニーク制約
- `class_id, table_id, target_id, user_id`: 1ユーザーにつき1対象に1つの評価のみ許可

### チェック制約
- `class_id`: 10〜99のいずれかである必要があります
- `table_id`: 1000〜9999のいずれかである必要があります
- `evaluation_type`: 0、1、2のいずれかである必要があります

---

## 設計補足

### 評価対象（class_id, table_id, target_id）
- master_classesテーブルで定義されたクラスID（例：10=コメント、20=レビューなど）
- master_tablesテーブルで定義されたテーブルID（例：1001=comments, 2001=reviewsなど）
- target_idは対象テーブルの主キーID

### 評価種別（evaluation_type）
- `0`: なし（評価未実施）
- `1`: good（良い評価）
- `2`: bad（悪い評価）

### 評価の仕組み
1. **初回評価**: ユーザーが対象を評価する際にレコードを作成
2. **評価変更**: 既存の評価を更新（1 → 2、2 → 1）
3. **評価取消**: evaluation_typeを0に更新（評価を取り消す場合）

### 集計との連携
- 評価テーブルからリアルタイムで集計を取得
- 表示時は集計カラムを使用し、パフォーマンスを確保
- キャッシュ機能で評価数の表示を最適化

---

## 関連テーブル

- `comments`: 多対1の関係（評価対象コメント）
- `reviews`: 多対1の関係（評価対象レビュー）
- `users`: 多対1の関係（評価者）
- `master_classes`: 多対1の関係（クラス種別）
- `master_tables`: 多対1の関係（テーブル種別）

---

## 運用上の注意点

1. **論理削除**: is_deleted=1で削除済み、0で有効。全テーブルで統一。
2. **重複評価防止**: 1ユーザーにつき1対象に1つの評価のみ許可
3. **評価種別制限**: 0:なし、1:good、2:bad のみ許可
4. **パフォーマンス**: 対象別の評価集計が高速
5. **データ整合性**: 重複評価の防止と評価種別の範囲制限