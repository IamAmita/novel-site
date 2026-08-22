# novel-site 決定事項リスト

**作成日**: 2026-07-21
**目的**: 実装前に機能要件を網羅的に整理する。**まず全カテゴリの機能要件を固め、Phase分け（何を先に作るか）はそのあとで検討する**（2026-07-21方針変更）。

---

## 前提（すでに決まっていること）

- **実装言語**: Python（Django + React）に一本化。他言語実装（PHP/TypeScript/Java/Go）は着手しない
- **ドキュメント構成**: `shared/` は廃止し `docs/` に一元化（`docs/project/` に方針・意思決定を記録）
- **ドメイン構造の大枠**: 作者（ペンネーム単位）→ World（世界観）→ Setting（設定）／作品 → 章 → 話
- **既存 python-django 実装**: `implementations/python-django/`にNovel中心モデル（読者・コメント・掲示板等を含む広範な機能、バックエンド7アプリ）が実装済みだが、**参考のみに留め、`docs/domain/`の確定済み設計に基づき新規に作り直す**方針で確定（2026-08-22）。PenName（ペンネーム）という中核概念が既存実装に存在しないなど、根幹の前提が異なるため

> 2026-07-21: 要件・設計ドキュメントを一旦すべて削除し、機能要件から順にしっかり整理し直した。当初は Phase1-確定メモ の Phase 区分に沿って進めていたが、**「まず全機能要件を出し切ってから Phase 分けする」方針に変更**。[docs/business/functional-scope.md](docs/business/functional-scope.md) に **A〜L すべての機能要件を整理済み**。その後 `docs/domain/` でデータモデル・画面仕様も全区分整理し、2026-08-22にPhase分け・実装戦略の論点も確定した（詳細は[Phase1-確定メモ](docs/project/Phase1-確定メモ.md)、本ファイルの「進め方」参照）。次のステップは画面設計・実装着手。

---

## 決定事項リスト

### A. 全体方針・ドメイン構造

- [x] ドメイン構造「作者 → ペンネーム → World → Setting／作品 → 章 → 話」で確定 → [functional-scope.md](docs/business/functional-scope.md)
- [x] 既存 python-django 実装の扱いを確定（2026-08-22決定）: **参考のみに留め、新規に作り直す**。既存実装（`implementations/python-django/backend/apps/`の7アプリ）を調査した結果、今回確定した設計の根幹である**PenName（ペンネーム）という概念が既存実装に存在しない**（Userが直接作者）ことが判明。worlds/novelsアプリを活かそうとしても外部キー構造から大規模改修が必要になるため、コードは参考にしつつ`docs/domain/`の確定済み設計に沿ってゼロから実装する
- [x] `communications` / `administration` アプリの扱いを確定（2026-08-22決定）: 既存実装は参考のみ（新規作り直し方針に準じる）。加えてコメント・通知・掲示板・管理機能はいずれもI／L区分であり、[Phase1-確定メモ](docs/project/Phase1-確定メモ.md)でPhase 2以降と決まっているため、**Phase 1では実装自体を行わない**。Phase 2着手時に[Communication.md](docs/domain/Communication.md)・[Moderation.md](docs/domain/Moderation.md)の確定済み設計に基づいて新規実装する

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
- [x] SettingField の型拡張（数値・日付等）は見送りで確定（2026-08-22決定）。数値・日付を活かす検索・ソート機能要件が存在しないため。将来そうした要件が出た時にセットで検討 → [Setting.md](docs/domain/Setting.md)
- [x] データモデル・画面仕様を整理済み → [Setting.md](docs/domain/Setting.md)（2026-07-23）
- [x] SettingTemplateはWorldごとに個別管理、テンプレート項目はSetting作成時にコピー、RelationLabelはサイト全体共通マスタ（2026-07-23決定）
- [x] テンプレート未選択でのSetting作成可否、親子階層のスコープ制約、他ユーザーSettingとの関係性の表示制御を確定（2026-08-22決定） → [Setting.md](docs/domain/Setting.md)

### E. 作品・執筆（Novel / Chapter / Episode）

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] 章は任意、設定参照はリンク記法＋サイドパネルの両方
- [x] 変更履歴はSetting＋作品本文が対象 → [Novel.md](docs/domain/Novel.md)。記録粒度は当初「変更ログのみ」としたが、2026-08-22に**変更前後の値を保存しGitHubのコミット履歴のような差分表示を行う方式**へ変更（下記参照）
- [x] データモデル・画面仕様を整理済み（本文文字数制限なし、章削除時はNovel直下へ付け替え、変更履歴は汎用ChangeLogモデル、2026-08-22決定） → [Novel.md](docs/domain/Novel.md)

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
- [x] データモデル・画面仕様を整理済み（Collaboratorは1テーブルでstatus管理、World権限はNovelへ自動継承、掲示板は返信付きスレッド形式、2026-08-22決定） → [Collaboration.md](docs/domain/Collaboration.md)

### I. コミュニケーション

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] コメントは作品＋話の両方、評価は5段階
- [x] フォローは更新通知・フィード表示のため、DMは相互フォローのみ
- [x] データモデル・画面仕様を整理済み（フォローはPenName単位、DMはUser単位の相互フォロー判定、通知は汎用Notificationモデル、2026-08-22決定） → [Communication.md](docs/domain/Communication.md)

### J. 公開・共有

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] 公開範囲は作品単位＋話単位、限定公開は共同制作者自動＋個別指定
- [x] Setting公開は作者が個別に選択
- [x] データモデル・画面仕様を整理済み（VisibilityGrantはNovel/Episode両方で個別指定可、Episode未設定はNovel継承、World共有Settingは公開すると即World全体に反映、2026-08-22決定） → [Publishing.md](docs/domain/Publishing.md)

### K. 読者向け機能

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] 未登録でも閲覧可、タグ・カテゴリあり
- [x] ランキングは閲覧数・評価・お気に入り数の集計、通知はアプリ内のみ
- [x] データモデル・画面仕様を整理済み（カテゴリは単一選択・タグは複数、閲覧数はEpisode単位のシンプルカウンタ、ランキングはリアルタイム計算、2026-08-22決定） → [Reader.md](docs/domain/Reader.md)

### L. 管理機能

- [x] 機能要件を整理済み → [functional-scope.md](docs/business/functional-scope.md)
- [x] 管理者は開発者のみ、対象は公開コンテンツ全般
- [x] アカウント対応は警告・一時停止・永久停止の段階制
- [x] データモデル・画面仕様を整理済み（通報理由は選択肢+自由記述、一時停止は任意日時指定、User.statusフィールドで現在状態を保持、2026-08-22決定） → [Moderation.md](docs/domain/Moderation.md)

---

## 横断レビューで見つかった未決事項（2026-08-22、全10件解消済み）

`docs/domain/` 配下の9ファイル（User/World/Setting/Novel/Collaboration/Communication/Publishing/Reader/Moderation）を横断的にレビューし、ファイル単体では見えにくい矛盾・抜けを洗い出した。以下すべて2026-08-22中に方針を確定し、各ファイルへ反映済み。

### 重大（設計の根幹に関わる）

- [x] 管理者の強制削除と作者の自主削除の区別を確定（2026-08-22決定）: 通報対象6モデル（World/Setting/Novel/Episode/Comment/PenName）に`deleted_by`（任意）を追加し、管理者による削除は作者の復元UI対象外とする → [Moderation.md](docs/domain/Moderation.md)
- [x] 非公開Settingへの参照の表示制御を確定（2026-08-22決定）: `SettingField.reference_value`・Episode本文中の`[[Setting名]]`リンク記法とも、`SettingRelation`と同じルール（項目名／リンクテキストは表示するが参照先の詳細は伏せてリンク無効化）を適用 → [Setting.md](docs/domain/Setting.md)・[Novel.md](docs/domain/Novel.md)
- [x] 閲覧権限判定を明確化（2026-08-22決定）: `Collaborator`は`status=accepted`のレコードのみを閲覧可能者とみなす。Episodeの判定はEpisode自体ではなく所属Novel／Worldに対するCollaboratorを見る → [Publishing.md](docs/domain/Publishing.md)
- [x] `Episode.visibility`が`NULL`（Novelを継承）のときのVisibilityGrant参照先を確定（2026-08-22決定）: effective visibilityと同じ対象を見る（NULLならNovel向け、値ありならEpisode向け） → [Publishing.md](docs/domain/Publishing.md)

### 中程度

- [x] `Report`の対象範囲を拡張（2026-08-22決定）: `novel`／`episode`／`comment`／`world`／`setting`／`pen_name`の6種類を対象とする → [Moderation.md](docs/domain/Moderation.md)。あわせて対象6モデルすべてに`deleted_by`を追加し、管理者削除を判定できるようにした → [World.md](docs/domain/World.md)・[Setting.md](docs/domain/Setting.md)・[Novel.md](docs/domain/Novel.md)・[Communication.md](docs/domain/Communication.md)・[User.md](docs/domain/User.md)
- [x] `edit`／`full`の権限差を権限マトリクスとして確定（2026-08-22決定）: editはコンテンツ編集・運用まで、fullは招待・除名・削除・公開設定変更などの管理操作まで → [Collaboration.md](docs/domain/Collaboration.md)
- [x] `BoardPost`／`BoardThread`の削除権限者を確定（2026-08-22決定）: Commentと同じ基準（投稿者本人／作者／edit・full権限者） → [Collaboration.md](docs/domain/Collaboration.md)
- [x] World詳細画面の共同制作者権限に応じた表示差分を確定（2026-08-22決定）。あわせてWorldの名義（owner_pen_name）変更もfull権限限定の操作として権限マトリクスに追加 → [World.md](docs/domain/World.md)・[Collaboration.md](docs/domain/Collaboration.md)
- [x] マスタデータ削除時の既存参照の扱いを確定（2026-08-22決定）: 基本方針は`SET_NULL`（Category/RelationLabel/SettingTemplate）。多対多の中間テーブル（Tag/NovelTag）は該当行を削除。いずれも使用中でも自由に削除できる → [Reader.md](docs/domain/Reader.md)・[Setting.md](docs/domain/Setting.md)
- [x] アカウント停止後の既存公開コンテンツの扱いを確定（2026-08-22決定）: `suspend`／`ban`実行時、所有する全Novelを自動的に`private`化。停止解除時も自動では戻さず本人が手動再設定 → [Moderation.md](docs/domain/Moderation.md)

---

## 2回目の横断レビューで見つかった問題点（2026-08-22、全7件解消済み）

各ドメインの詳細仕様（ChangeLogの差分保存化を含む）を詰めた後、再度横断レビューを実施。以下すべて2026-08-22中に方針を確定し、各ファイルへ反映済み。

### 重大

- [x] ChangeLogの対象にSettingField・PenNameが漏れている → 解消（2026-08-22）。SettingFieldはSetting本体のChangeLog（`changes`内の`fields.<項目名>`）に統合、PenNameはChangeLog対象外で確定 → [Novel.md](docs/domain/Novel.md)
- [x] ChangeLog（diff）の閲覧権限が未定義で、一般公開作品では誰でも変更履歴が見えてしまう懸念 → 解消（2026-08-22）。**ChangeLogの設計思想**（Gitを知らなくても作者・編集者が差分を直感的に確認できる体験の提供。読者向け機能ではない）を明文化し、閲覧権限は常に作者・共同制作者（`status=accepted`のCollaborator）限定で確定。あわせて過去バージョンへの復元（revert）機能は今回は見送りで確定 → [Novel.md](docs/domain/Novel.md)
- [x] 管理者によるPenName強制削除の矛盾を解消（2026-08-22決定）: 管理者もWorldを保持しているPenNameは削除できない（本人操作と同じルールを適用、例外なし）。その場合はPenName単位ではなくUserを`suspend`／`ban`して対応する（所有者不在World問題は発生しない） → [Moderation.md](docs/domain/Moderation.md)

### 中程度

- [x] 除名済みユーザーの実名表示（ChangeLogは匿名化しない）が読者に晒されないか確認 → 解消（2026-08-22）。Bの決定（ChangeLogは常に作者・共同制作者限定）により、読者には晒されない設計として整合済み
- [x] edit／full権限マトリクスにSetting関連操作を追加（2026-08-22決定）: Setting削除はWorld/Novel削除と同じくfull限定、SettingTemplate管理はeditでも可能 → [Collaboration.md](docs/domain/Collaboration.md)・[Setting.md](docs/domain/Setting.md)
- [x] VisibilityGrant指定時の通知を追加（2026-08-22決定）: `notification_type`に`visibility_grant`を追加し、基本セットを11種に拡張 → [Communication.md](docs/domain/Communication.md)・[Publishing.md](docs/domain/Publishing.md)
- [x] Episode.bodyなど長文フィールドのデータ量増加について方針を明記（2026-08-22決定）: 個人利用規模でパフォーマンス要件を設けない方針、および「全ての変更を振り返れること」がChangeLogの思想そのものであることを踏まえ、圧縮・パージ等の最適化は行わない → [Novel.md](docs/domain/Novel.md)

---

## 進め方

**方針（2026-07-21更新）**: 機能要件をカテゴリ A〜L まで**すべて**整理してから、Phase分け（どの機能を先に作るか）を検討する。データモデル・画面詳細などの設計は、Phase分けが終わってから着手する。

**方針変更（2026-07-23）**: Phase分けより先に、カテゴリごとにデータモデル・画面設計を進める方針に変更。Phase分けは設計がある程度進んでから改めて検討する。

1. ~~機能要件 A〜L を整理する~~ — 完了（2026-07-21、[functional-scope.md](docs/business/functional-scope.md)）
2. ~~データモデル・画面設計を進める~~ — 完了（2026-08-22、`docs/domain/` に[User.md](docs/domain/User.md)・[World.md](docs/domain/World.md)・[Setting.md](docs/domain/Setting.md)・[Novel.md](docs/domain/Novel.md)・[Collaboration.md](docs/domain/Collaboration.md)・[Communication.md](docs/domain/Communication.md)・[Publishing.md](docs/domain/Publishing.md)・[Reader.md](docs/domain/Reader.md)・[Moderation.md](docs/domain/Moderation.md) を整理。F・Gは各ファイルの一覧画面・非機能決定事項で実質カバー済みのため個別ファイルなし）
3. ~~各ドメインの詳細仕様を詰める~~ — 完了（2026-08-22。各domainファイルに残っていた未決事項・細部仕様を全て確定。ChangeLogは「GitHubのコミット履歴のような差分表示」の要望を受け、変更ログのみの記録から変更前後の値を保存する方式に方針変更）。対象一覧:
   - ~~[Setting.md](docs/domain/Setting.md): SettingFieldの型拡張（数値・日付等）~~ — 完了（2026-08-22、見送りで確定）
   - ~~[World.md](docs/domain/World.md): 削除済みWorldの復元UI（画面遷移・アクセス経路）~~ — 完了（2026-08-22、一覧画面の「削除済みを表示」トグルに統一）
   - ~~[Novel.md](docs/domain/Novel.md): 削除済みNovel/Chapter/Episodeの復元UI、ChangeLogの一覧・詳細画面UI~~ — 完了（2026-08-22、階層ごとに同じフィルタ方式／ChangeLogは対象ごとの絞り込みのみ）
   - ~~[Collaboration.md](docs/domain/Collaboration.md): 除名（`removed`）されたユーザーの投稿・変更履歴の扱い~~ — 完了（2026-08-22。Comment/BoardPostは投稿者名を匿名化、ChangeLogは追跡目的のため実名のまま残す）
   - ~~ChangeLog（[Novel.md](docs/domain/Novel.md)）の記録方式~~ — 完了（2026-08-22、GitHubのコミット履歴のような差分表示が欲しいとの要望を受け、変更ログのみの記録から「フィールド単位で変更前後の値を保存しdiff表示する」方式に変更）
   - ~~[Communication.md](docs/domain/Communication.md): Notificationの`notification_type`列挙、DM・通知の既読UI詳細~~ — 完了（2026-08-22、基本セット10種／個別クリックで既読／未読件数バッジ）
   - ~~[Publishing.md](docs/domain/Publishing.md): 限定公開の個別ユーザー指定の検索・追加UI、一般公開作品の検索・ランキング反映タイミング~~ — 完了（2026-08-22、user_id検索／リアルタイム計算のため即時反映）
   - ~~[Reader.md](docs/domain/Reader.md): ランキングの合成スコアかタブ切り替えか、お気に入り数の公開可否~~ — 完了（2026-08-22、タブ切り替えのみ／お気に入り数は公開）
   - ~~[Moderation.md](docs/domain/Moderation.md): ReportReasonの初期セット、一時停止解除（`expires_at`到達）時の自動復帰の仕組み~~ — 完了（2026-08-22、5項目の初期セット／アクセス時に都度チェック）
4. ~~Phase分け~~ — 完了（2026-08-22）。Phase 1は**「Gitを知らなくても差分を確認しながら書ける、単独作者向けの設定・執筆管理ツール」**に決定。含めるのはA〜G区分（ユーザー最小限／World／Setting／Novel・Chapter・Episode・ChangeLog／自分向け閲覧・検索／非機能）。H（共同制作）・I（コミュニケーション）・J（公開・共有）・K（読者向け機能）・L（管理機能）は全てPhase 2以降に見送り → [Phase1-確定メモ.md](docs/project/Phase1-確定メモ.md)（v2.0に全面刷新）
5. ~~残る実装戦略の論点~~ — 完了（2026-08-22）。既存python-django実装（`implementations/python-django/`）はPenName概念の欠如など根幹の前提が異なるため**参考のみに留め、新規に作り直す**方針で確定。communications/administrationアプリもPhase 1では実装自体を行わない
6. 画面設計（`docs/design/` 新設等）
7. ドキュメントが固まった領域から実装に着手する

---

## 関連ドキュメント

- [Phase1-確定メモ.md](docs/project/Phase1-確定メモ.md)（旧Phase区分の記録。今回の整理完了後に見直す）
- [プロダクト定義.md](docs/project/プロダクト定義.md)
- [functional-scope.md](docs/business/functional-scope.md)（機能要件、整理中）
- [docs/archive/python-django-初期実装/](docs/archive/python-django-初期実装/)（旧 Novel 中心モデルの記録、参考程度）
