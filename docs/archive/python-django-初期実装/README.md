# python-django 初期実装ドキュメント（アーカイブ）

**作成日**: 2025年3月
**アーカイブ日**: 2026-07-21
**状態**: 参照のみ（現行の設計とは不整合）

---

## これは何か

2026-05-25 の方針転換（[Phase1-確定メモ](../../project/Phase1-確定メモ.md)）以前に作成された、python-django 実装の要件定義書・設計書。

- `要件定義書.md` / `機能要件書.md`
- `設計書/01_システム構成.md` 〜 `04_画面設計.md`

## なぜアーカイブしたか

これらのドキュメントは **Novel 中心モデル**（読者・コメント・評価・掲示板・タグ/カテゴリ・管理画面・一般公開を含む広範な機能）を前提としており、2026-05-25 に確定した Phase 1 方針（**World 中心モデル**、作者のみ対象、非公開固定、設定管理と執筆に特化）と矛盾する。

現行の実装（バックエンド7アプリ）はこの旧設計に基づいて構築されたものであり、[todo.md](../../../todo.md) の決定に従って World 中心モデルへ作り直す予定。

## 現行の正本ドキュメント

- ドメイン設計: [docs/domain/core-entities.md](../../domain/core-entities.md)、[docs/domain/entity-relationships.md](../../domain/entity-relationships.md)
- 機能スコープ: [docs/business/functional-scope.md](../../business/functional-scope.md)
- Phase 1 方針: [docs/project/Phase1-確定メモ.md](../../project/Phase1-確定メモ.md)
- システム構成・DB設計: [docs/architecture/](../../architecture/)

## 参考として使える部分

エンティティ・機能に依存しない技術パターン（Docker構成の考え方、JWT認証フローの仕組み、ページネーション・エラーレスポンス形式等の API 規約、React 側のディレクトリ構成パターン）は、World 中心モデルへの再実装時にも参考にできる。
