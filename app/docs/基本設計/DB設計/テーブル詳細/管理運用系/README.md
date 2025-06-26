# 管理運用系テーブル詳細

---

## 概要
管理運用系テーブルは、小説投稿サイトの管理・運用に関する全てのテーブルを管理します。

---

## 設計方針
- マスターデータは一元管理し、データの整合性を保証
- 運用データは履歴管理と監査ログを適切に実装
- テンプレートや定義データは柔軟な拡張性を確保
- 通報やレポートは適切なステータス管理とワークフローを実装
- 運用履歴は一元管理し、監査・追跡・分析を可能にする

---

## テーブル一覧

### 定義・マスター
- [target_types.md](./target_types.md) - 対象種別定義テーブル
- [templates.md](./templates.md) - テンプレート管理テーブル

### 運用・管理
- [reports.md](./reports.md) - 通報管理テーブル
- [operation_histories.md](./operation_histories.md) - 運用履歴テーブル

---

## テーブル関係図

```
target_types (1) ←→ (N) comments
target_types (1) ←→ (N) reviews
target_types (1) ←→ (N) notifications
target_types (1) ←→ (N) evaluations
target_types (1) ←→ (N) reports
target_types (1) ←→ (N) operation_histories

templates (1) ←→ (N) notifications
templates (1) ←→ (N) operation_histories

users (1) ←→ (N) reports
users (1) ←→ (N) operation_histories
```

---

## 主要な考慮点
- マスターデータの一元管理と整合性確保
- 運用データの適切な履歴管理
- テンプレートによる柔軟な通知管理
- 通報の適切なワークフロー管理
- 監査ログとセキュリティ対策
- 運用履歴の一元管理と監査対応 