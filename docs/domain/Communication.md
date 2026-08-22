# コミュニケーション仕様

**目的**: [functional-scope.md](../business/functional-scope.md) I. コミュニケーションの機能要件を、データモデル・画面仕様のレベルまで詳細化する
**進め方**: Phase分けより先に、カテゴリごとに詳細仕様を詰める方針（2026-07-21〜）。詳細は [todo.md](../../todo.md) 参照

---

## データモデル

### Comment（コメント）

| フィールド | 型・制約 |
|---|---|
| target_type | 選択肢: `novel` / `episode` |
| target_id | 対象オブジェクトのid（整数） |
| user | 投稿者（外部キー） |
| parent | 親コメント（自己参照外部キー、任意。返信の場合に設定） |
| body | 文字列（TextField）、必須 |
| created_at / updated_at | タイムスタンプ |
| deleted_at | 論理削除用（NULLなら有効） |
| deleted_by | 削除実行者（外部キー、User参照、任意）。管理者による強制削除の判定に使う。詳細は[Moderation.md](Moderation.md)参照 |

#### 決定事項

- 対象: **作品（Novel）＋話（Episode）の両方**（functional-scope.md I参照）
- 返信階層: **1階層のみ**（2026-08-22決定）。`parent`を持つコメント（返信）はさらに`parent`を持てない（アプリ側バリデーションで制約し、同じ親コメントの下にフラットに並ぶ）
- 削除: **論理削除**。投稿者本人、または対象作品の所有者（Worldの`owner_pen_name`）、および[Collaboration.md](Collaboration.md)で`edit`／`full`権限を持つ共同制作者が削除できる
- 除名済み共同制作者の投稿者表示（2026-08-22決定）: 投稿者がその後[Collaborator](Collaboration.md)から`removed`（除名）された場合、投稿自体は残すが、投稿者名は「削除された共同制作者」等に匿名化して表示する

### Rating（評価）

| フィールド | 型・制約 |
|---|---|
| novel | 評価対象Novel（外部キー、必須） |
| user | 評価者（外部キー、必須） |
| score | 整数、1〜5 |
| created_at / updated_at | タイムスタンプ |

#### 決定事項

- 方式: **5段階評価**（functional-scope.md I参照）
- 一意性: **1ユーザー1作品につき1件のみ**（`novel`＋`user`でユニーク制約）
- 変更: **後から変更可能**（2026-08-22決定）。再評価はupsert（既存レコードのscoreを更新）で扱う

### Follow（フォロー）

| フィールド | 型・制約 |
|---|---|
| follower | フォローする人（外部キー、User参照） |
| followee | フォローされるペンネーム（外部キー、**PenName参照**） |
| created_at | タイムスタンプ |

#### 決定事項

- フォロー対象: **PenName単位**（2026-08-22決定）。「作者をフォローする」という要件を、User/PenName完全分離の方針（[User.md](User.md)参照）に合わせてPenName単位で実現する。同一Userの別ペンネームは個別にフォロー・フォロー解除できる
- 一意性: `follower`＋`followee`でユニーク制約
- 目的: **更新通知・フィード表示のため**（functional-scope.md I参照）。フィードはフォロー中の全PenNameの新作・更新をまとめて表示する

### DirectMessage（DM）

| フィールド | 型・制約 |
|---|---|
| sender | 送信者（外部キー、User参照） |
| recipient | 受信者（外部キー、User参照） |
| body | 文字列（TextField）、必須 |
| read_at | 既読タイムスタンプ、任意（NULLなら未読） |
| created_at | タイムスタンプ |

#### 決定事項

- 送受信の単位: **User単位**（PenName単位ではない。DMはアカウント間のやり取りとして扱う）
- 送信可能条件（2026-08-22決定）: **User単位での相互フォローが成立している場合のみ**送信できる。フォローはPenName単位のため、「UserAが所有するいずれかのPenNameを、UserBがフォローしている」かつ「UserBが所有するいずれかのPenNameを、UserAがフォローしている」の両方が成立するときに、UserA・UserB間は相互フォローとみなす

### Notification（通知）

| フィールド | 型・制約 |
|---|---|
| user | 通知の受信者（外部キー、User参照） |
| notification_type | 選択肢: `comment` / `reply` / `follow` / `new_episode` / `collaboration_invite` / `collaboration_accepted` / `collaboration_declined` / `collaboration_removed` / `board_post` / `direct_message` |
| target_type | 通知の元になった対象の種別（`comment` / `episode` / `pen_name` / `collaborator` / `board_post` / `direct_message` 等） |
| target_id | 対象オブジェクトのid（整数） |
| read_at | 既読タイムスタンプ、任意（NULLなら未読） |
| created_at | タイムスタンプ |

#### 決定事項

- 実装方式: **汎用Notificationモデル**（2026-08-22決定）。[Novel.md](Novel.md)のChangeLogと同様、種別ごとに個別テーブルを作らず単一テーブルに集約する
- 通知手段: **アプリ内通知のみ**（functional-scope.md K参照。メール通知はしない）
- notification_typeの範囲（2026-08-22決定）: **基本セット10種**（コメント／返信／フォロー／新着話／共同制作の招待・承諾・辞退・除名／掲示板投稿／DM受信）に絞る。評価（rating）通知やアカウント対応（account_action）通知などは、必要になった時点で追加する
- 既読タイミング（2026-08-22決定）: **個別クリックで既読**にする。通知一覧を開いただけでは既読にせず、各通知をクリック（タップ）した時点でその通知だけが既読になる
- 未読バッジ（2026-08-22決定）: **未読件数を数字で表示**する

---

## 画面仕様

### コメント欄（作品・話ページ）

- 対象ページ（作品詳細・話閲覧画面）にコメント一覧と投稿フォームを表示
- 返信は親コメントの下にフラットにネスト表示（1階層のみのため）
- 削除は本人／作者／編集権限以上の共同制作者にのみ操作を表示

### 評価UI

- 星（またはそれに準ずる）5段階のUIで評価を入力
- 自分が既に付けた評価は選択状態で表示され、選び直すと更新される

### フォロー・フィード画面

- フォロー中のPenName一覧を確認できる
- フィードには、フォロー中の全PenNameの新作・更新（新規話公開等）を時系列で表示する

### DM画面

- User単位の相互フォロー関係にある相手とのみ会話を開始できる
- 会話相手一覧 → 個別スレッド（時系列の送受信一覧）の2階層構成
- 未読件数をNotificationと連動して表示

### 通知一覧画面

- Notificationの一覧を時系列で表示し、既読・未読を区別する
- 種別に応じて対象（コメント元・フォロワーのPenName・新着話等）へのリンクを表示する
- 既読化（2026-08-22決定）: 一覧を開いただけでは既読にならず、個別の通知をクリックした時点でその通知のみ既読になる
- 未読バッジ（2026-08-22決定）: ヘッダー等に未読件数を数字で表示する

---

## 未決事項・今後の検討

（現時点でなし。今後の実装・設計の中で新たに論点が出た場合はここに追記する）
