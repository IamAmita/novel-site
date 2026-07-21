# novel-site TODO

**作成日**: 2026-07-21（2026-07-21 更新：Python 実装に一本化）
**目的**: 現時点の進捗状況を踏まえた次アクションの整理

---

## 現状サマリー

novel-site は当初「5言語比較学習プロジェクト」として発足したが、**Python（python-django）実装に一本化**する。他言語実装（PHP/Laravel、TypeScript/Next.js、Java/Spring Boot、Go/Gin）は着手しない。

2026-05-25 に要件を見直す大きな方針転換があり、以下が確定した（[Phase1-確定メモ.md](docs/project/Phase1-確定メモ.md)、[functional-scope.md](docs/business/functional-scope.md)）。

- ドメイン構造を `Novel 中心` → **`World（世界観）→ Setting / 作品 → 章 → 話`** に変更
- Phase 1 のスコープを **「設定管理と執筆」のみ** に絞り込み（コメント・評価・通知・掲示板・共同創作・公開・タグ・カテゴリ・管理者機能はすべて Phase 2 以降へ先送り）

python-django の既存実装（バックエンド7アプリ・フロント全ページ実装済み、テストなし）は**旧ドメインモデル（Novel中心）**であり、新方針（World中心・設定管理優先）とは一致しない。この差分を python-django 側で埋めていく。

| 実装 | 状態 |
|------|------|
| python-django | バックエンド7アプリ・フロント全ページ実装済み（テストなし）。旧ドメインモデル（Novel中心）で新方針と不整合 → **今後の実装対象** |

---

## 0. 方針転換に伴う意思決定（2026-07-21 決定済み）

- [x] python-django の既存実装（Novel中心・広範な機能）の扱い → **新ドメインモデル（World中心）に作り直す**
- [x] Phase 1 スコープ外の既存実装（`communications`/`administration` アプリ）の扱い → **残す**（Phase 2以降で再利用。今は手を付けない）

---

## 1. ドキュメント整理（[要件インベントリ.md](docs/project/要件インベントリ.md) 記載の未完了分）

Phase1-確定メモ「11. 次のステップ」より：

- [x] `docs/business/functional-scope.md` の更新（2026-05-25 完了）
- [x] `docs/domain/core-entities.md` を World 中心モデルに更新（2026-07-21 完了。Setting/SettingTemplateのWorld・Novel両対応スコープ、SettingField ハイブリッド方式、SettingRelation の方向性・ラベル管理、Episode-Setting参照の自動＋手動方式まで確定）
- [x] `docs/domain/entity-relationships.md` の整合（2026-07-21 完了）
- [x] `docs/project/Phase1-確定メモ.md` §4.1 を確定エンティティ設計に合わせて更新（2026-07-21）
- [x] `docs/business/user-stories.md` を創作者・Phase1向けに書き直し（2026-07-21完了。読者/共同創作/公開等のPhase2以降ストーリーを分離）
- [ ] `docs/business/business-rules.md` の Phase タグ付け（BR-301〜308 共同創作、BR-406 通知など Phase2/3 相当の整理）
- [x] `docs/architecture/データベース設計.md` の整合（2026-07-21完了。World→Novel→Chapter→Episode に統一済み）
- [x] `docs/specifications/機能仕様.md` を索引化（2026-07-21完了。各正本ドキュメントへのリンク集に置き換え）
- [ ] 数値要件の統一（同時接続数：`performance-requirements.md`の1000人 vs archive版の100人）
- [x] 未決定事項の一部解消（2026-07-21）：Setting種類の初期セット、閲覧画面の基本構成、World検索要否、SettingRelationのWorld横断可否 → [Phase1-確定メモ.md §10.1](docs/project/Phase1-確定メモ.md)
- [ ] 残る未決定事項（[Phase1-確定メモ.md](docs/project/Phase1-確定メモ.md) §10）：閲覧画面の詳細ワイヤーフレーム、関係性の視覚化、Phase1内第2優先の内訳

---

## 1.5 ドキュメント構造の一元化（2026-07-21 完了）

技術がPython単独に統合されたことに伴い、複数実装を前提とした `shared/` と `docs/` の分離を廃止し、`docs/` 配下に一元化した。

- [x] `shared/business` `shared/domain` `shared/design` `shared/quality` `shared/assets` を `docs/` 配下（`docs/business` 等）へ移動し `shared/` を廃止
- [x] `implementations/python-django/docs/要件定義/`・`設計書/`（Novel中心・現行のPhase1方針と矛盾する内容）を `docs/archive/python-django-初期実装/` へアーカイブし、経緯を README.md に明記
- [x] リポジトリ全体の相対リンクを新構造に合わせて修正
- [x] `docs/README.md`・ルートREADME.md・`implementations/README.md`を新構造の索引に更新
- [x] `docs/project/要件インベントリ.md` の該当箇所を整理済みとして更新
- [ ] 検討記録系ガイド（`*-ガイド.md`）・`docs/archive/` 内の既存コンテンツ自体は履歴として意図的に未変更（方針: [Phase1-確定メモ-ガイド.md](docs/project/Phase1-確定メモ-ガイド.md) 等）

---

## 2. python-django：Phase 1 実装（設定管理と執筆）

[Phase1-確定メモ.md](docs/project/Phase1-確定メモ.md) §8.1 の優先順位に従う：**設定管理 → ユーザー/World/執筆 → 閲覧**

> エンティティ定義は [docs/domain/core-entities.md](docs/domain/core-entities.md) / [entity-relationships.md](docs/domain/entity-relationships.md) を正とする（2026-07-21 確定）。

### 2.1 基盤
- [ ] World / Setting 系モデルへのマイグレーション再設計（既存 `worlds` アプリを新方針に合わせて再構成）
- [ ] Pseudonym（ペンネーム）モデル（1ユーザーが複数ペンネームを持てる構造）
- [ ] プロフィール（表示名・アイコン・自己紹介の最小構成）

### 2.2 世界観・設定管理（最優先領域）
- [ ] World（世界観）CRUD
- [ ] Setting（設定）CRUD。World単位／Novel単位のスコープ切り替え（排他）に対応
- [ ] SettingTemplate（設定テンプレート）機能。World単位／Novel単位のスコープ対応
- [ ] SettingField（カスタム項目）機能。テンプレート由来の雛形項目＋Setting個別追加のハイブリッド実装
- [ ] SettingRelation（設定間の関係性）機能。方向性あり、RelationLabel参照
- [ ] RelationLabel（関係ラベル）機能。システム共通マスタ＋World固有ラベルの管理
- [ ] 設定の一覧・詳細画面
- [ ] 設定の検索
- [ ] （任意）設定間関係の視覚化

### 2.3 作品・執筆
- [ ] 作品（Novel）CRUD、章・話の構成管理
- [ ] 本文の執筆・編集画面
- [ ] 執筆画面からの設定参照：本文リンク記法（`[[設定名]]`等）のパースによるEpisodeSettingReference自動生成
- [ ] Setting参照の手動追加・削除UI（サイドパネル等）
- [ ] 表紙画像アップロード
- [ ] EditHistory（変更履歴・編集ログ）記録機能

### 2.4 閲覧・検索
- [ ] 自分向け閲覧画面：「設定一覧」「作品一覧」を別メニューとする構成（World横断表示、2026-07-21確定。詳細ワイヤーフレームは未確定）
- [ ] 一覧・ソート
- [ ] 作品・本文の検索
- [ ] World検索（2026-07-21 実装する方針に確定）

### 2.5 品質
- [ ] テストコード整備（現状ゼロ）

> `communications`/`administration` アプリは Phase 1 では変更しない（Phase 2 以降で再利用予定、0. 参照）

---

## 3. Phase 1 完了後（着手順は Phase1確定メモ §8.2 参照）

- [ ] 共同制作機能（Phase1完了後、最優先で着手予定）
- [ ] 限定公開・コミュニケーション機能（コメント/評価/フォロー/DM/掲示板）は Phase 2 スコープとして別途計画

---

## 関連ドキュメント

- [Phase1-確定メモ.md](docs/project/Phase1-確定メモ.md)
- [functional-scope.md](docs/business/functional-scope.md)
- [要件インベントリ.md](docs/project/要件インベントリ.md)
- [プロダクト定義.md](docs/project/プロダクト定義.md)
