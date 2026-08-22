# 設定（Setting）仕様

**目的**: [functional-scope.md](../business/functional-scope.md) D. 設定（Setting）の機能要件を、データモデル・画面仕様のレベルまで詳細化する
**進め方**: Phase分けより先にデータモデル・画面設計を進める方針（2026-07-23〜）。詳細は [todo.md](../../todo.md) 参照

---

## データモデル

### SettingTemplate（設定テンプレート）

| フィールド | 型・制約 |
|---|---|
| world | 所属World（外部キー） |
| name | 文字列、必須。**同一World内で一意** |
| created_at / updated_at | タイムスタンプ |
| deleted_at | 論理削除用（NULLなら有効） |

#### 決定事項

- 管理単位: **Worldごとに個別管理**（2026-07-23決定）。テンプレートはWorld間で共有されない
- 初期セット: **World作成時に5種類（キャラクター／世界・地理／組織・勢力／物品・アイテム／歴史）を自動生成**する。ユーザーは自由に追加・編集・削除でき、初期セットも例外ではない

### SettingTemplateField（テンプレート項目定義）

| フィールド | 型・制約 |
|---|---|
| template | 所属SettingTemplate（外部キー） |
| name | 文字列、必須（例:「性格」「所在地」） |
| field_type | `text` または `setting_reference` |
| order | 表示順（整数） |
| created_at / updated_at | タイムスタンプ |

#### 決定事項

- field_typeは2種類のみ（**テキスト／他Settingへの参照**）。数値・日付等は Phase 1 では扱わない（functional-scope.md D参照）
- 型拡張の見送り（2026-08-22決定）: 数値・日付型は追加しない。現状の検索機能（F区分）が「名前・内容の部分一致検索」のみで、数値ソートや日付検索といった型を活かす機能要件自体が存在しないため。将来そうした検索・ソート機能が必要になったタイミングで、型拡張とセットで検討する

### Setting（設定）

| フィールド | 型・制約 |
|---|---|
| world | 所属World（外部キー、必須） |
| novel | 所属作品（外部キー、**任意**）。NULLならWorld全体で共有、値ありならその作品専用 |
| template | 作成元テンプレート（外部キー、**任意**） |
| parent | 親Setting（自己参照外部キー、任意） |
| name | 文字列、必須 |
| description | 文字列、任意 |
| is_public | 真偽値、デフォルト`false`。詳細は[Publishing.md](Publishing.md)参照 |
| created_at / updated_at | タイムスタンプ |
| deleted_at | 論理削除用（NULLなら有効） |
| deleted_by | 削除実行者（外部キー、User参照、任意）。管理者による強制削除の判定に使う。詳細は[Moderation.md](Moderation.md)参照 |

#### 決定事項

- Setting の範囲: **World単位＋作品単位の両方**（`novel`がNULLかどうかで区別）
- テンプレート: **必須ではない**（2026-08-22決定）。テンプレートを選ばず項目なしで作成し、後から個別に項目を追加することもできる
- 親子階層: **必要**。親子関係は同一Setting同士のツリー構造
  - 親子のスコープ制約（2026-08-22決定）: 子のスコープは親と同じか、それより狭い範囲に限る（Worldスコープの親の下に作品スコープの子をぶら下げることは可。逆――作品スコープの親の下にWorldスコープの子を置くこと――は不可）
- Setting削除時: **連鎖削除**（論理削除。子Setting・関連するSettingFieldも連鎖）
- Setting名の重複: **許容**
- 公開: **作者が個別に選択**（2026-08-22決定、作品の公開状態とは連動しない。判定ロジックの詳細は[Publishing.md](Publishing.md)参照）
- テンプレート削除時の既存参照（2026-08-22決定）: **SET_NULL**。SettingTemplateを削除しても`Setting.template`はNULLになるだけで、Setting自体やコピー済みのSettingFieldには影響しない（SettingField側は作成時にコピーされ独立しているため、影響を受けない）

### SettingField（Settingのカスタム項目）

| フィールド | 型・制約 |
|---|---|
| setting | 所属Setting（外部キー） |
| name | 文字列、必須 |
| field_type | `text` または `setting_reference` |
| text_value | 文字列、任意（field_type=textの場合に使用） |
| reference_value | 参照先Setting（外部キー、任意。field_type=setting_referenceの場合に使用） |
| order | 表示順（整数） |
| created_at / updated_at | タイムスタンプ |

#### 決定事項

- テンプレート由来の項目は**Setting作成時にコピー**する（2026-07-23決定）。以後テンプレートを変更しても、既存Settingの項目には影響しない
- テンプレート由来の項目に加えて、Setting個別に項目を自由追加できる
- 1項目につき値は1つ（複数のSetting参照を持たせたい場合は項目を複数作る）
- 閲覧権限がない参照先の表示制御（2026-08-22決定）: `reference_value`が閲覧権限のないSettingを指している場合、**SettingRelationと同じルール**を適用する。項目名は表示するが、参照先Settingの名前・詳細は伏せて「(非公開の設定)」のように表示し、リンクもさせない

### RelationLabel（関係ラベル・マスタ）

| フィールド | 型・制約 |
|---|---|
| name | 文字列、必須、**一意（サイト全体）** |
| created_at / updated_at | タイムスタンプ |

#### 決定事項

- 管理単位: **サイト全体で共通のマスタ**（2026-07-23決定）。ユーザーは自由に追加できる（既存ラベルがあればそれを選ぶ）
- 初期セット（2026-08-22決定）: SettingTemplateと同様、よく使う関係を自動生成する。初期ラベル案: 師匠／弟子／友人／恋人／ライバル／家族／上司／部下／所属。自由に追加・編集・削除でき、初期セットも例外ではない

### SettingRelation（Setting間の関係性）

| フィールド | 型・制約 |
|---|---|
| from_setting | 関係元Setting（外部キー） |
| to_setting | 関係先Setting（外部キー） |
| label | RelationLabel（外部キー、**任意**。ラベル削除時はNULLになる） |
| created_at / updated_at | タイムスタンプ |
| deleted_at | 論理削除用（NULLなら有効） |

#### 決定事項

- 方向性: **あり**（例:「Aの師匠はB」→ from=A, label=師匠, to=B）
- World横断: **可**。さらに**自分が所有・編集権限を持つ範囲を越えて、他ユーザーが所有するSettingとの関係も設定できる**（2026-07-23決定。ラベルがサイト全体共通のマスタであることに対応）
- 閲覧権限がない相手Settingの表示制御（2026-08-22決定）: **関係の存在・ラベルは表示するが、相手Settingは非公開扱いで表示する**（名前・詳細は伏せ、リンクもさせない）。例:「(非公開の設定)との関係: 師匠」
- 視覚化（グラフ表示等）: **Phase 1に含めない**（functional-scope.md D参照）
- ラベル削除時の既存参照（2026-08-22決定）: **SET_NULL**。RelationLabelを削除すると、それを参照していたSettingRelation.labelはNULLになる（関係自体は残り、「(ラベルなし)」等と表示する）。使用中でも自由に削除できる

---

## 画面仕様

### Setting一覧画面

- F（閲覧・検索）で定義した「設定一覧」メニューに対応。World横断で自分のSettingを一覧できる
- 検索: 名前・内容の部分一致検索
- 親子階層はツリー表示（初期は折りたたみ、必要に応じて展開）

### Setting詳細画面

- 表示内容: 名前・説明・カスタム項目一覧（テンプレート由来＋個別追加分）・関係性一覧（from/to両方向）・子Setting一覧
- カスタム項目のうち`setting_reference`型は、参照先Settingへのリンクとして表示

### Setting作成・編集フォーム

- 入力項目: 所属World（必須）、所属作品（任意。作品単位で作る場合のみ選択）、親Setting（任意）、テンプレート（任意）、名前（必須）、説明（任意）
- テンプレートを選択すると、そのテンプレートのSettingTemplateFieldがSettingFieldとしてコピーされる
- 作成後もカスタム項目の追加・編集・削除、親子関係の変更が可能

### テンプレート管理画面

- World単位でSettingTemplate・SettingTemplateFieldの一覧・作成・編集・削除ができる
- 初期セット5種もこの画面から編集・削除できる

### 関係性の設定UI

- Setting詳細画面から、関係先Setting・ラベル・方向を指定して関係性を追加できる
- ラベルは既存のRelationLabelから選択、またはその場で新規追加できる

### Setting削除

- 論理削除。子Setting・SettingFieldは連鎖削除
- 削除確認: 単純な確認ダイアログ（World.mdの方針にならう）
- 削除後の復元: **World.mdと同じ方針**（2026-08-22決定）。期限なく手動復元可能。一覧画面から削除済みSettingをフィルタして表示し、そこから復元する
- 削除権限（2026-08-22決定）: World／作品削除と同じく**`full`権限限定**（詳細は[Collaboration.md](Collaboration.md)の権限マトリクス参照）
- 復元対象の制限（2026-08-22決定）: `deleted_by`が管理者による削除の場合は、この復元UIの対象外とする（詳細は[Moderation.md](Moderation.md)参照）

---

## 未決事項・今後の検討

（現時点でなし。今後の実装・設計の中で新たに論点が出た場合はここに追記する）
