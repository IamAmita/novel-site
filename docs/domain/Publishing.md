# 公開・共有仕様

**目的**: [functional-scope.md](../business/functional-scope.md) J. 公開・共有の機能要件を、データモデル・画面仕様のレベルまで詳細化する
**進め方**: Phase分けより先に、カテゴリごとに詳細仕様を詰める方針（2026-07-21〜）。詳細は [todo.md](../../todo.md) 参照

---

## データモデル

### Novel.visibility（作品の公開範囲）

既存の[Novel.md](Novel.md)のNovelモデルに以下を追加する。

| フィールド | 型・制約 |
|---|---|
| visibility | 選択肢: `private`（非公開）/ `limited`（限定公開）/ `public`（一般公開） |

#### 決定事項

- デフォルト値: **`private`**（作成直後は非公開）
- 単位: **作品単位＋話単位**（functional-scope.md J参照。話ごとに上書き可能）

### Episode.visibility（話の公開範囲・上書き）

既存の[Novel.md](Novel.md)のEpisodeモデルに以下を追加する。

| フィールド | 型・制約 |
|---|---|
| visibility | 選択肢: `NULL`（Novelを継承）/ `private` / `limited` / `public` |

#### 決定事項

- 未設定時（NULL）の扱い（2026-08-22決定）: **所属Novelの`visibility`をそのまま継承する**。値が入っていればNovelの設定を上書きする（例: 作品は一般公開だが、最新話だけ非公開にする、といった運用ができる）

### VisibilityGrant（限定公開の個別ユーザー指定）

| フィールド | 型・制約 |
|---|---|
| target_type | 選択肢: `novel` / `episode` |
| target_id | 対象オブジェクトのid（整数） |
| user | 閲覧を許可されたユーザー（外部キー） |
| created_at | タイムスタンプ |

#### 決定事項

- 指定単位（2026-08-22決定）: **作品単位・話単位の両方で個別に持てる**（`target_type`で区別）。話ごとに閲覧を許可する相手を変えられる
- 共同制作者（[Collaboration.md](Collaboration.md)の`Collaborator`）は、このテーブルに登録しなくても**自動的に閲覧可能**（functional-scope.md J参照）
- `limited`（限定公開）時の実質的な閲覧可能者 = 共同制作者（自動）＋ このテーブルに登録された個別ユーザー
- Episodeでの参照対象（2026-08-22決定）: **effective visibilityと同じ対象を見る**。`Episode.visibility`がNULL（Novelを継承）の場合、`VisibilityGrant`も`target_type=novel`のレコードを参照する。`Episode.visibility`に値が入っている（Novelの設定を上書きしている）場合は、`target_type=episode`のレコードを参照する

### Setting.is_public（設定の公開）

既存の[Setting.md](Setting.md)のSettingモデルに以下を追加する。

| フィールド | 型・制約 |
|---|---|
| is_public | 真偽値、デフォルト`false` |

#### 決定事項

- 公開単位: **Setting単位**（作品の公開状態とは連動しない。作者が個別に選ぶ。functional-scope.md J参照）
- World単位のSetting（複数作品で共有）を公開した場合（2026-08-22決定）: **説明文なしにWorld全体の設定として誠実に公開される**。「所属作品が1つも公開されていなければ表示しない」といった連動ルールは設けない

---

## 閲覧権限の判定ロジック

あるユーザーが特定のEpisode／Novelを閲覧できるかは、以下の優先順で判定する。

1. **effective visibility** を決定する: Episodeの場合は`Episode.visibility`（NULLなら所属`Novel.visibility`）、Novelの場合は`Novel.visibility`
2. `public`: 誰でも閲覧可能
3. `private`: Worldの`owner_pen_name`が属するUser、および対象（World／Novel）に対する**`status=accepted`の**[Collaborator](Collaboration.md)のみ閲覧可能（2026-08-22明確化）。`pending`（招待中で未回答）・`declined`（辞退）・`removed`（除名済み）のレコードは閲覧可能者に含めない
4. `limited`: 上記`private`の閲覧可能者に加え、対象の`VisibilityGrant`に登録されたユーザーも閲覧可能
5. Episodeの閲覧可否を判定する際の`Collaborator`は、Episode自体ではなく**所属Novel（またはそのWorld）に対するレコード**を見る（Collaboratorの`target_type`は`world`／`novel`のみのため）
6. Episodeの`VisibilityGrant`は、**手順1で決定したeffective visibilityと同じ対象**を見る。`Episode.visibility`がNULL（Novel継承）ならNovel向けの`VisibilityGrant`を、値が入っていればEpisode向けの`VisibilityGrant`を参照する（2026-08-22決定）

Settingの閲覧可否は上記と独立し、`is_public`が`true`なら誰でも、`false`なら所有者・共同制作者のみが閲覧できる。

---

## 画面仕様

### 公開範囲設定UI（作品編集画面）

- 非公開／限定公開／一般公開のセレクトを表示
- 限定公開を選んだ場合、個別ユーザー指定（VisibilityGrant）の追加・削除UIを表示
- 個別ユーザー指定の検索方法（2026-08-22決定）: **user_id（`/u/{user_id}`の識別子）によるオートコンプリート検索**。フォロー関係の有無に関わらず、任意のユーザーを指定して公開できる

### 公開範囲設定UI（話編集画面）

- 「作品の設定を継承（未設定）」／非公開／限定公開／一般公開のセレクトを表示。継承時は所属作品の実効設定をバッジ等で表示する
- 限定公開を選んだ場合、話単位の個別ユーザー指定を編集できる（検索方法は作品編集画面と同じuser_id検索）

### Setting公開設定UI

- Setting編集画面に公開／非公開のトグルを表示

---

## 未決事項・今後の検討

（現時点でなし。今後の実装・設計の中で新たに論点が出た場合はここに追記する）

## 検索・ランキングへの反映タイミング

- **即時反映**（2026-08-22決定）。[Reader.md](Reader.md)の検索・ランキングはいずれもDBを都度参照するリアルタイム計算方式のため、`visibility`を`public`に変更すれば直後の検索・ランキング表示から対象になり、`public`以外に変更すれば直後から対象外になる。反映のためのバッチ処理・キャッシュ更新は不要
