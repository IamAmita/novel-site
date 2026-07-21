# novel-site TODO

**作成日**: 2026-07-21（2026-07-21 更新：Python 実装に一本化）
**目的**: 現時点の進捗状況を踏まえた次アクションの整理

---

## 現状サマリー

novel-site は当初「5言語比較学習プロジェクト」として発足したが、**Python（python-django）実装に一本化**する。他言語実装（PHP/Laravel、TypeScript/Next.js、Java/Spring Boot、Go/Gin）は着手しない。

2026-05-25 に要件を見直す大きな方針転換があり、以下が確定した（[Phase1-確定メモ.md](docs/project/Phase1-確定メモ.md)、[functional-scope.md](shared/business/functional-scope.md)）。

- ドメイン構造を `Novel 中心` → **`World（世界観）→ Setting / 作品 → 章 → 話`** に変更
- Phase 1 のスコープを **「設定管理と執筆」のみ** に絞り込み（コメント・評価・通知・掲示板・共同創作・公開・タグ・カテゴリ・管理者機能はすべて Phase 2 以降へ先送り）

python-django の既存実装（バックエンド7アプリ・フロント全ページ実装済み、テストなし）は**旧ドメインモデル（Novel中心）**であり、新方針（World中心・設定管理優先）とは一致しない。この差分を python-django 側で埋めていく。

| 実装 | 状態 |
|------|------|
| python-django | バックエンド7アプリ・フロント全ページ実装済み（テストなし）。旧ドメインモデル（Novel中心）で新方針と不整合 → **今後の実装対象** |

---

## 0. 最優先：方針転換に伴う意思決定（要ユーザー判断）

- [ ] python-django の既存実装（Novel中心・広範な機能）をどう扱うか：**新ドメインモデル（World中心）に作り直す**か、**既存コードを土台に段階移行する**か
- [ ] Phase 1 スコープ外の既存実装（コメント・評価・通知・掲示板・管理機能等、`communications`/`administration` アプリ）を削除するか、後続 Phase 用に残すか

---

## 1. ドキュメント整理（[要件インベントリ.md](docs/project/要件インベントリ.md) 記載の未完了分）

Phase1-確定メモ「11. 次のステップ」より：

- [x] `shared/business/functional-scope.md` の更新（2026-05-25 完了）
- [ ] `shared/domain/core-entities.md` を World 中心モデルに更新（現状 Setting のみで World 概念が反映されていない）
- [ ] `shared/domain/entity-relationships.md` の整合（Comment/Rating/Collaboration など Phase2/3 要素が Phase1 と同列に記載されている）
- [ ] `shared/business/user-stories.md` を創作者・Phase1向けに書き直し
- [ ] `shared/business/business-rules.md` の Phase タグ付け（BR-301〜308 共同創作、BR-406 通知など Phase2/3 相当の整理）
- [ ] `docs/architecture/データベース設計.md` の整合（Novel→Episode直接 の記載が Chapter を挟む構造と不一致）
- [ ] `docs/specifications/機能仕様.md` を索引化（`shared/` との重複解消）
- [ ] 数値要件の統一（同時接続数：`performance-requirements.md`の1000人 vs archive版の100人）
- [ ] 未決定事項の解消（[Phase1-確定メモ.md](docs/project/Phase1-確定メモ.md) §10）：Setting種類の具体一覧、閲覧画面詳細構成、World検索要否など

---

## 2. python-django：Phase 1 実装（設定管理と執筆）

[Phase1-確定メモ.md](docs/project/Phase1-確定メモ.md) §8.1 の優先順位に従う：**設定管理 → ユーザー/World/執筆 → 閲覧**

### 2.1 基盤
- [ ] World / Setting 系モデルへのマイグレーション再設計（既存 `worlds` アプリを新方針に合わせて再構成）
- [ ] ペンネーム機能（1ユーザーが複数ペンネームを持てる構造）
- [ ] プロフィール（表示名・アイコン・自己紹介の最小構成）

### 2.2 世界観・設定管理（最優先領域）
- [ ] World（世界観）CRUD
- [ ] Setting（設定）CRUD
- [ ] 設定テンプレート（種類定義）機能
- [ ] 設定フィールド（カスタム項目）機能
- [ ] 設定間の関係性定義機能
- [ ] 設定の一覧・詳細画面
- [ ] 設定の検索
- [ ] （任意）設定間関係の視覚化

### 2.3 作品・執筆
- [ ] 作品（Novel）CRUD、章・話の構成管理
- [ ] 本文の執筆・編集画面
- [ ] 執筆画面からの設定参照（リンク・挿入・サイドパネル等、方式は未確定）
- [ ] 表紙画像アップロード
- [ ] 変更履歴・編集ログ記録

### 2.4 閲覧・検索
- [ ] 自分向け閲覧画面（World / 作品 / 話 / 設定）
- [ ] 一覧・ソート
- [ ] 作品・本文の検索
- [ ] （任意）World検索

### 2.5 品質
- [ ] テストコード整備（現状ゼロ）
- [ ] Phase 1 スコープ外機能（`communications`/`administration` アプリ等）の扱い整理（0. の意思決定に従う）

---

## 3. Phase 1 完了後（着手順は Phase1確定メモ §8.2 参照）

- [ ] 共同制作機能（Phase1完了後、最優先で着手予定）
- [ ] 限定公開・コミュニケーション機能（コメント/評価/フォロー/DM/掲示板）は Phase 2 スコープとして別途計画

---

## 関連ドキュメント

- [Phase1-確定メモ.md](docs/project/Phase1-確定メモ.md)
- [functional-scope.md](shared/business/functional-scope.md)
- [要件インベントリ.md](docs/project/要件インベントリ.md)
- [プロダクト定義.md](docs/project/プロダクト定義.md)
