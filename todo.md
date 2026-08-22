# novel-site 決定事項リスト

**作成日**: 2026-07-21
**目的**: 実装前に機能要件を網羅的に整理する。**まず全カテゴリの機能要件を固め、Phase分け（何を先に作るか）はそのあとで検討する**（2026-07-21方針変更）。

---

## 前提（すでに決まっていること）

- **実装言語**: Python（Django + React）に一本化。他言語実装（PHP/TypeScript/Java/Go）は着手しない
- **ドキュメント構成**: `shared/` は廃止し `docs/` に一元化（`docs/project/` に方針・意思決定を記録）
- **ドメイン構造の大枠**: 作者（ペンネーム単位）→ World（世界観）→ Setting（設定）／作品 → 章 → 話
- **既存 python-django 実装**: 現状は Novel 中心モデル（読者・コメント・掲示板等を含む広範な機能）。どこまで再利用するかは機能要件確定後に判断する

> 2026-07-21: 要件・設計ドキュメントを一旦すべて削除し、機能要件から順にしっかり整理し直した。当初は Phase1-確定メモ の Phase 区分に沿って進めていたが、**「まず全機能要件を出し切ってから Phase 分けする」方針に変更**。[docs/business/functional-scope.md](docs/business/functional-scope.md) に **A〜L すべての機能要件を整理済み**（[Phase1-確定メモ](docs/project/Phase1-確定メモ.md) の Phase 区分は暫定の記録として残るのみで、今回の整理を拘束しない）。次のステップは Phase 分け。

---

## 決定事項リスト

### A. 全体方針・ドメイン構造

- [x] ドメイン構造「作者 → ペンネーム → World → Setting／作品 → 章 → 話」で確定 → [functional-scope.md](docs/business/functional-scope.md)
- [ ] 既存 python-django 実装（Novel 中心・バックエンド7アプリ）をどこまで再利用するか。完全に作り直すか、段階的に置き換えるか（全機能要件確定後に判断）
- [ ] `communications` / `administration` アプリ（コメント・通知・掲示板・管理機能等）をどう扱うか（全機能要件確定後に判断）

### B. ユーザー・ペンネーム管理

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] ペンネームは上限なしで複数作成可能
- [x] パスワードリセットはメール送信方式
- [x] アカウント削除時、配下データは論理削除
- [x] ユーザーID（本人が決める一意識別子、変更可）を導入。ログインはメール／ユーザーIDどちらでも可
- [x] ユーザー名（登録時に決める表示名、ユーザーIDとは別概念・重複可）を導入。User情報とPenName情報は完全に分離し、著者名フォールバックとしては使わない（2026-07-28決定）
- [x] ペンネームは登録時には作らず0件からスタート。World作成時に0件ならその場で作成を強制する（2026-07-28決定） → [User.md](docs/domain/User.md)
- [x] ペンネーム名の重複は同一ユーザー内のみ禁止、他ユーザー間は許容
- [x] データモデル・画面仕様を整理済み → [User.md](docs/domain/User.md)
- [x] 「ペンネーム切り替え」はユーザー機能として持たない。名義の指定・変更はWorldごとに行う（2026-07-23決定、C参照）
- [x] プロフィール項目の細部を確定（bioはWorld.descriptionと同じ上限1024文字、ペンネーム一覧画面はシンプル表示、2026-08-22決定） → [User.md](docs/domain/User.md)
- [x] ユーザーIDは変更不可で確定（2026-07-28決定） → [User.md](docs/domain/User.md)

### C. 世界観（World）

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] 表紙画像あり、World削除時は連鎖削除（論理削除）、名前重複は許容
- [x] 名義（ペンネーム）はWorld作成時に選択し、編集画面から変更もできる（2026-07-23決定）
- [x] データモデル・画面仕様を整理済み → [World.md](docs/domain/World.md)

### D. 設定（Setting）

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] World単位＋作品単位の両方、親子階層構造あり、削除時は連鎖削除（論理削除）、名前重複は許容
- [x] SettingTemplate初期セット5種（編集・削除自由）、SettingFieldはテキスト＋他Setting参照
- [x] 関係性は方向性あり・ラベルはマスタ管理（自由追加可）・World横断可、視覚化は見送り
- [ ] SettingField の型拡張（数値・日付等）は設計時に再検討
- [x] データモデル・画面仕様を整理済み → [Setting.md](docs/domain/Setting.md)（2026-07-23）
- [x] SettingTemplateはWorldごとに個別管理、テンプレート項目はSetting作成時にコピー、RelationLabelはサイト全体共通マスタ（2026-07-23決定）
- [x] テンプレート未選択でのSetting作成可否、親子階層のスコープ制約、他ユーザーSettingとの関係性の表示制御を確定（2026-08-22決定） → [Setting.md](docs/domain/Setting.md)

### E. 作品・執筆（Novel / Chapter / Episode）

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] 章は任意、設定参照はリンク記法＋サイドパネルの両方
- [x] 変更履歴はSetting＋作品本文が対象、粒度は変更ログのみ
- [ ] 文字数制限・画像仕様は設計時に検討

### F. 閲覧・検索（自分向け）

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] 設定一覧・作品一覧を別メニューに分ける、検索は部分一致、World検索あり

### G. 非機能・運用

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] パフォーマンス要件は不要、バックアップはDB定期バックアップ＋エクスポート機能、テストは駆動方式

### H. 共同制作

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] 招待はWorld単位・作品単位の両方、権限は3段階（閲覧のみ／編集可／全権限）
- [x] 招待権限は所有者＋所有者が許可した共同制作者、掲示板は作品単位
- [x] 進捗管理は作品全体のステータス、公開前評価は自由コメントのみ

### I. コミュニケーション

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] コメントは作品＋話の両方、評価は5段階
- [x] フォローは更新通知・フィード表示のため、DMは相互フォローのみ

### J. 公開・共有

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] 公開範囲は作品単位＋話単位、限定公開は共同制作者自動＋個別指定
- [x] Setting公開は作者が個別に選択

### K. 読者向け機能

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] 未登録でも閲覧可、タグ・カテゴリあり
- [x] ランキングは閲覧数・評価・お気に入り数の集計、通知はアプリ内のみ

### L. 管理機能

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] 管理者は開発者のみ、対象は公開コンテンツ全般
- [x] アカウント対応は警告・一時停止・永久停止の段階制

---

## 進め方

**方針（2026-07-21更新）**: 機能要件をカテゴリ A〜L まで**すべて**整理してから、Phase分け（どの機能を先に作るか）を検討する。データモデル・画面詳細などの設計は、Phase分けが終わってから着手する。

**方針変更（2026-07-23）**: Phase分けより先に、カテゴリごとにデータモデル・画面設計を進める方針に変更。Phase分けは設計がある程度進んでから改めて検討する。

1. ~~機能要件 A〜L を整理する~~ — 完了（2026-07-21、[functional-scope.md](docs/business/functional-scope.md)）
2. **データモデル・画面設計を進める**（`docs/domain/` 新設）: [User.md](docs/domain/User.md)・[World.md](docs/domain/World.md)・[Setting.md](docs/domain/Setting.md) 着手済み。次はE（作品・執筆）以降
3. Phase分け — 設計がある程度進んだ段階で、全機能要件を俯瞰し、どの機能をどのPhaseで作るかを決定する（[Phase1-確定メモ](docs/project/Phase1-確定メモ.md) の区分を土台に見直す）
4. 残る実装戦略の論点（既存実装の再利用方針、communications/administrationアプリの扱い）を決定する
5. 画面設計（`docs/design/` 新設等）
6. ドキュメントが固まった領域から実装に着手する

---

## 関連ドキュメント

- [Phase1-確定メモ.md](docs/project/Phase1-確定メモ.md)（旧Phase区分の記録。今回の整理完了後に見直す）
- [プロダクト定義.md](docs/project/プロダクト定義.md)
- [functional-scope.md](docs/business/functional-scope.md)（機能要件、整理中）
- [docs/archive/python-django-初期実装/](docs/archive/python-django-初期実装/)（旧 Novel 中心モデルの記録、参考程度）
