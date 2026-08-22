# 共同制作仕様

**目的**: [functional-scope.md](../business/functional-scope.md) H. 共同制作の機能要件を、データモデル・画面仕様のレベルまで詳細化する
**進め方**: Phase分けより先に、カテゴリごとに詳細仕様を詰める方針（2026-07-21〜）。詳細は [todo.md](../../todo.md) 参照

---

## データモデル

### Collaborator（共同制作者・招待）

| フィールド | 型・制約 |
|---|---|
| target_type | 選択肢: `world` / `novel` |
| target_id | 対象オブジェクトのid（整数） |
| user | 招待された（共同制作する）ユーザー（外部キー） |
| invited_by | 招待した人（外部キー、User参照） |
| permission_level | 選択肢: `view`（閲覧のみ）/ `edit`（編集可）/ `full`（全権限） |
| status | 選択肢: `pending`（招待中）/ `accepted`（承諾済み）/ `declined`（辞退）/ `removed`（除名・解除済み） |
| created_at / updated_at | タイムスタンプ |

#### 決定事項

- 実装方式: **1テーブルでstatus管理**（2026-08-22決定）。招待中／承諾済みを分けた別テーブルは持たず、単一の`Collaborator`テーブルの`status`で状態遷移を表現する
- 招待単位: **World単位・作品（Novel）単位の両方**（`target_type`で区別）
- 権限の粒度: **閲覧のみ／編集可／全権限**の3段階（functional-scope.md H参照）
- 権限の継承（2026-08-22決定）: **World単位の権限はNovelに自動継承する**。あるNovelへのアクセス権限を判定する際は、まずそのNovelに対する直接のCollaboratorレコード（`target_type=novel`）を確認し、なければ所属Worldに対するCollaboratorレコード（`target_type=world`）を見る。**Novel単位の権限があればWorld単位の権限より優先される**（Worldでは編集可でも、特定Novelだけ閲覧のみに制限する、といった上書きができる）
- 招待権限: **所有者（Worldのowner_pen_name／NovelのownerにあたるWorldのowner_pen_name）、および所有者が許可した共同制作者も招待できる**（functional-scope.md H参照。「許可した」の具体的な操作は未決事項参照）

### Board（掲示板）

| フィールド | 型・制約 |
|---|---|
| novel | 所属Novel（外部キー、必須） |
| created_at | タイムスタンプ |

#### 決定事項

- 単位: **作品（Novel）単位**（functional-scope.md H参照）。Novel作成時に自動で1件生成される

### BoardThread（掲示板スレッド）

| フィールド | 型・制約 |
|---|---|
| board | 所属Board（外部キー、必須） |
| title | 文字列、必須 |
| created_by | 作成者（外部キー、User参照） |
| created_at / updated_at | タイムスタンプ |
| deleted_at | 論理削除用（NULLなら有効） |

### BoardPost（掲示板投稿・返信）

| フィールド | 型・制約 |
|---|---|
| thread | 所属BoardThread（外部キー、必須） |
| user | 投稿者（外部キー） |
| body | 文字列（TextField）、必須 |
| created_at / updated_at | タイムスタンプ |
| deleted_at | 論理削除用（NULLなら有効） |

#### 決定事項

- 実装形式: **返信付きスレッド形式**（2026-08-22決定）。1つのBoardThreadに複数のBoardPostがぶら下がる構成（フラットな一覧ではなくスレッド単位で議論をまとめる）

### Novel.status（進捗ステータス）

既存の[Novel.md](Novel.md)のNovelモデルに以下を追加する。

| フィールド | 型・制約 |
|---|---|
| status | 選択肢: `writing`（執筆中）/ `reviewing`（レビュー中）/ `completed`（完成） |

#### 決定事項

- 進捗管理の粒度: **作品全体のステータス**（functional-scope.md H参照。話単位の細かい進捗管理はしない）
- ステータス値: **執筆中／レビュー中／完成**の3段階（2026-08-22決定）

### 公開前評価

- 独自モデルは新設しない。[I. コミュニケーション](../business/functional-scope.md)で定義するコメント機能を、**共同制作者限定で利用する**形で実現する（functional-scope.md H参照）

---

## 画面仕様

### 共同制作者管理画面

- World詳細画面・作品詳細画面それぞれから、共同制作者の一覧・招待・権限変更・除名ができる
- 一覧には対象ユーザー・権限レベル・ステータス（招待中／承諾済み）を表示する
- Novel側の一覧では、Worldから継承された権限（直接のNovel向けCollaboratorレコードがない場合）とNovel固有の上書き権限を区別して表示する

### 招待・承諾画面

- 招待されたユーザーは、アプリ内通知（[K. 読者向け機能](../business/functional-scope.md)の通知機構を利用）経由で招待を確認し、承諾・辞退できる

### 掲示板画面（作品単位）

- 作品詳細画面から掲示板へ遷移
- スレッド一覧 → スレッド詳細（投稿＋返信）の2階層構成
- スレッド作成・投稿は共同制作者（閲覧のみ権限を含む）が行える

### 進捗ステータス表示

- 作品詳細画面にステータスバッジを表示
- 編集可／全権限を持つ共同制作者がステータスを変更できる（閲覧のみ権限は変更不可）

---

## 未決事項・今後の検討

- 「所有者が許可した共同制作者も招待できる」の具体的な操作（招待権限自体を個別に付与するフラグを持つか、`full`権限者は常に招待できるとするか）
- `edit`（編集可）と`full`（全権限）の権限差の具体（例: 共同制作者の招待・除名、作品削除、公開設定変更などをどちらが行えるか）
- 除名（`removed`）されたユーザーの、それまでの投稿・変更履歴の扱い（残す前提だが、表示上の扱いは実装時に検討）
