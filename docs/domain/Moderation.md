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
| target_type | 選択肢: `novel` / `comment` |
| target_id | 対象オブジェクトのid（整数） |
| reporter | 通報者（外部キー、User参照） |
| reason | 通報理由（外部キー、ReportReason参照） |
| detail | 文字列（TextField）、任意（補足の自由記述） |
| status | 選択肢: `pending`（未対応）/ `resolved`（対応済み）/ `dismissed`（却下） |
| created_at / updated_at | タイムスタンプ |

#### 決定事項

- 対象: **公開コンテンツ全般（作品・コメント両方）**（functional-scope.md L参照）
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

- 管理者は公開コンテンツ（作品・コメント）を削除できる。実装は既存の論理削除（`deleted_at`）の仕組みをそのまま利用する

---

## 未決事項・今後の検討

- ReportReasonの初期セットの具体的な項目
- 一時停止（`suspend`）が`expires_at`を過ぎた際、`User.status`を`active`へ戻す仕組み（アクセス時の都度チェックか、定期バッチか）は実装設計時に検討
