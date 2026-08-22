# 管理機能仕様

**目的**: [functional-scope.md](../business/functional-scope.md) L. 管理機能の機能要件を、データモデル・画面仕様のレベルまで詳細化する
**進め方**: Phase分けより先に、カテゴリごとに詳細仕様を詰める方針（2026-07-21〜）。詳細は [todo.md](../../todo.md) 参照

---

## データモデル

### ReportReason（通報理由マスタ）

| フィールド | 型・制約 |
|---|---|
| name | 文字列、必須、一意（例: スパム／著作権侵害／不適切な内容／嫌がらせ／その他） |
| created_at / updated_at | タイムスタンプ |

### Report（通報）

| フィールド | 型・制約 |
|---|---|
| target_type | 選択肢: `novel` / `episode` / `comment` / `world` / `setting` / `pen_name` |
| target_id | 対象オブジェクトのid（整数） |
| reporter | 通報者（外部キー、User参照） |
| reason | 通報理由（外部キー、ReportReason参照） |
| detail | 文字列（TextField）、任意（補足の自由記述） |
| status | 選択肢: `pending`（未対応）/ `resolved`（対応済み）/ `dismissed`（却下） |
| created_at / updated_at | タイムスタンプ |

#### 決定事項

- 対象: **公開されうる全モデル**（2026-08-22決定、functional-scope.md L「公開コンテンツ全般」を拡張）。Novel／Episode／Commentに加え、World（名前・説明・表紙画像）、Setting（`is_public=true`のもの）、PenName（表示名・アイコン・自己紹介）も対象とする
- 理由の入力方式: **選択肢＋自由記述**（2026-08-22決定）。ReportReasonマスタから選び、`detail`で補足できる

### AccountAction（アカウント対応履歴）

| フィールド | 型・制約 |
|---|---|
| user | 対応対象のユーザー（外部キー） |
| action_type | 選択肢: `warning`（警告）/ `suspend`（一時停止）/ `ban`（永久停止） |
| reason | 文字列（TextField）、必須（対応理由） |
| expires_at | タイムスタンプ、任意（`suspend`の場合、一時停止の解除日時を管理者が指定。`warning`・`ban`ではNULL） |
| created_at | タイムスタンプ |

#### 決定事項

- 対応の粒度: **警告／一時停止／永久停止**の段階制（functional-scope.md L参照）
- 一時停止期間: **管理者が任意の日時を指定**（2026-08-22決定）。固定の期間選択肢は用意しない
- 既存公開コンテンツの扱い（2026-08-22決定）: `suspend`／`ban`を実行すると、対象ユーザーが所有する全World配下のNovelを**自動的に`private`へ変更する**（[Publishing.md](Publishing.md)参照）。警告（`warning`）では変更しない
- 停止解除時の扱い（2026-08-22決定）: 一時停止が解除（`expires_at`到達等で`User.status`が`active`に戻る）されても、自動非公開化したNovelの公開範囲は**自動的には戻さない**。作者本人が確認のうえ手動で再設定する（停止理由が解消していないのに意図せず再公開される事態を避ける）

### User.status（ユーザーの現在状態）

既存の[User.md](User.md)のUserモデルに以下を追加する。

| フィールド | 型・制約 |
|---|---|
| status | 選択肢: `active`（通常）/ `suspended`（一時停止中）/ `banned`（永久停止） |

#### 決定事項

- 保持方式: **User.statusフィールドを追加**（2026-08-22決定）。AccountActionは対応履歴として別途保持しつつ、現在の状態はUser.statusを直接参照することで即座に判定できるようにする（AccountActionの最新レコードから毎回算出する必要をなくす）
- 管理者権限（functional-scope.md L参照）: **管理者体制は開発者（自分）のみ**を想定。複数管理者向けのロール管理は設計に含めない（Userに`is_staff`等の単純なフラグを1つ持たせれば足りる）

---

## 画面仕様

### 通報フォーム

- 作品詳細画面・コメント表示箇所から通報ボタンを設置
- 通報理由（ReportReasonから選択）＋補足の自由記述を入力するフォーム

### 管理画面（通報対応）

- 未対応（`pending`）の通報を一覧表示
- 通報内容を確認し、対象コンテンツの削除・対象ユーザーへの警告／一時停止／永久停止・却下のいずれかを実行できる
- 対応後、Reportの`status`を`resolved`または`dismissed`に更新する

### 管理画面（ユーザー管理）

- ユーザー一覧から、個別ユーザーの現在状態（`status`）・AccountAction履歴を確認できる
- 警告・一時停止（解除日時指定）・永久停止の対応を実行できる

### コンテンツ削除

- 管理者は公開コンテンツを削除できる。実装は既存の論理削除（`deleted_at`）の仕組みを利用する
- 削除実行者の区別（2026-08-22決定）: 通報対象の6モデル（**World／Setting／Novel／Episode／Comment／PenName**）に**`deleted_by`（外部キー、User参照、任意）を追加**する。作者自身や共同制作者が削除した場合は`deleted_by`にその人が入り、管理者が通報対応として削除した場合は管理者のUserが入る
- 作者向けの「削除済み一覧からの復元」UI（[World.md](World.md)・[Novel.md](Novel.md)・[Setting.md](Setting.md)等）は、**`deleted_by`が管理者（`is_staff=true`）のレコードを対象外とする**（一覧に表示しない・復元操作を無効化する）。管理者による削除を作者が誤って（あるいは意図的に）復元できてしまう事態を防ぐ
- 管理者削除の取り消しは、管理画面から別途行える（管理者の判断ミスがあった場合の救済手段）

---

## 未決事項・今後の検討

- ReportReasonの初期セットの具体的な項目
- 一時停止（`suspend`）が`expires_at`を過ぎた際、`User.status`を`active`へ戻す仕組み（アクセス時の都度チェックか、定期バッチか）は実装設計時に検討
