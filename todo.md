# novel-site 決定事項リスト

**作成日**: 2026-07-21
**目的**: 詳細な要件・設計ドキュメントを書く前に、決めるべき論点を洗い出す。ここでの決定を経てから `docs/` に文書化し、実装に進む。

---

## 前提（すでに決まっていること）

- **実装言語**: Python（Django + React）に一本化。他言語実装（PHP/TypeScript/Java/Go）は着手しない
- **ドキュメント構成**: `shared/` は廃止し `docs/` に一元化（`docs/project/` に方針・意思決定を記録）
- **Phase 1 のゴール**（[Phase1-確定メモ](docs/project/Phase1-確定メモ.md)より）: 設定管理を自由かつ詳細に行い、それを見ながら執筆できる状態
- **Phase 1 のドメイン構造の大枠**: 作者（ペンネーム単位）→ World（世界観）→ Setting（設定）／作品 → 章 → 話
- **Phase 1 に含めないこと**: 共同創作、一般公開、コメント・評価・通知・掲示板、タグ・カテゴリ、管理者機能（すべて Phase 2 以降）
- **既存 python-django 実装**: 現状は Novel 中心モデル（読者・コメント・掲示板等を含む広範な機能）で、上記 Phase 1 方針と不整合。どこまで再利用し、どこから作り直すかは下記の決定事項に含む

> 2026-07-21: 詳細な要件・エンティティ設計・アーキテクチャ設計ドキュメント（旧 `docs/business` `docs/domain` `docs/design` `docs/quality` `docs/architecture` `docs/specifications`）は一旦すべて削除し、機能要件から順にしっかり整理し直した。[docs/business/functional-scope.md](docs/business/functional-scope.md) に A〜G すべての機能要件を整理済み。次はデータモデル・画面等の設計に進む。

---

## 決定事項リスト

### A. 全体方針の再確認

- [x] Phase 1 の対象ユーザーは作者のみで確定（読者向け機能は Phase 3 以降） → [functional-scope.md](docs/business/functional-scope.md)
- [x] ドメイン構造「作者 → ペンネーム → World → Setting／作品 → 章 → 話」で確定
- [ ] 既存 python-django 実装（Novel 中心・バックエンド7アプリ）をどこまで再利用するか。完全に作り直すか、段階的に置き換えるか（機能要件確定後に判断）
- [ ] `communications` / `administration` アプリ（コメント・通知・掲示板・管理機能等）を Phase 1 の間どう扱うか（触らず残す／削除する。機能要件確定後に判断）

### B. ユーザー・ペンネーム管理

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] ペンネームは上限なしで複数作成可能
- [x] パスワードリセットはメール送信方式
- [x] アカウント削除時、配下データは論理削除
- [ ] プロフィール項目の細部（表示名・アイコン・自己紹介以外に必要な項目はあるか）は設計時に検討

### C. 世界観（World）

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] 表紙画像あり
- [x] World削除時は配下データを連鎖削除（論理削除）
- [x] World名の重複は許容
- [ ] World の項目の文字数制限等は設計時に検討

### D. 設定（Setting）

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] Setting は World単位＋作品単位の両方
- [x] 親子階層構造は必要
- [x] Setting削除時は連鎖削除（論理削除）
- [x] Setting名の重複は許容
- [x] SettingTemplate初期セット5種、編集・削除も自由
- [x] SettingFieldの値はテキスト＋他Settingへの参照
- [x] 関係性は方向性あり、ラベルはマスタ管理（自由追加可）、World横断可
- [x] 関係性の視覚化はPhase 1に含めない
- [ ] SettingField の型拡張（数値・日付等）を将来的に検討するか、Phase1では見送りのままか（設計時に再確認）

### E. 作品・執筆（Novel / Chapter / Episode）

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] 章（Chapter）は任意
- [x] 設定参照はリンク記法＋サイドパネル挿入の両方
- [x] 変更履歴の対象はSetting＋作品本文、粒度は変更ログのみ
- [ ] 本文・あらすじ等の文字数制限、表紙画像のアップロード仕様は設計時に検討

### F. 閲覧・検索

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] 閲覧画面は設定一覧・作品一覧を別メニューに分ける
- [x] 検索方式は部分一致検索
- [x] World検索は必要

### G. 非機能・運用

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] パフォーマンス要件は不要（個人利用前提）
- [x] バックアップはDB定期バックアップ＋作品・設定単位のエクスポート機能
- [x] テスト方針はテスト駆動

---

## 進め方

**方針**: 機能要件（何ができる必要があるか）からしっかり整理する。データモデル・画面詳細などの設計レベルの決定は、機能要件が固まってから詰める。

1. ~~機能要件を A→B→C→D→E→F→G の順でカテゴリごとに整理・合意する~~ — 完了（2026-07-21、[functional-scope.md](docs/business/functional-scope.md)）
2. 残る実装戦略の論点（既存 python-django 実装の再利用方針、`communications`/`administration` アプリの扱い）を決定する
3. 機能要件をもとにデータモデル（`docs/domain/` 新設）・画面（`docs/design/` 新設等）の設計を進める
4. ドキュメントが固まった領域から実装に着手する

---

## 関連ドキュメント

- [Phase1-確定メモ.md](docs/project/Phase1-確定メモ.md)
- [プロダクト定義.md](docs/project/プロダクト定義.md)
- [functional-scope.md](docs/business/functional-scope.md)（機能要件、整理中）
- [docs/archive/python-django-初期実装/](docs/archive/python-django-初期実装/)（旧 Novel 中心モデルの記録、参考程度）
