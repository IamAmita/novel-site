# Phase 1 確定メモ

**バージョン**: 2.0
**作成日**: 2026年5月25日（v1.0）
**更新日**: 2026年8月22日（v2.0、全面刷新）
**ステータス**: 確定
**根拠**: [functional-scope.md](../business/functional-scope.md)（A〜L全区分の機能要件）、`docs/domain/`配下の各ドメイン設計、2026-08-22のPhase分け方針決定

> v2.0での変更: 2026-07-21〜2026-08-22にかけて機能要件（A〜L）とデータモデル・画面仕様（`docs/domain/`）を全区分整理した上で、あらためてPhase分けを行った。v1.0時点の大枠（設定管理＋執筆管理から始める、共同制作は後回し）は概ね踏襲しつつ、v1.0にはなかった**「変更履歴を差分（diff）で確認できる」という体験そのものをPhase 1の中核価値に据えた**点が最大の変更点。

---

## 1. Phase 1 のコンセプト

### 1.1 一言で

**Gitを知らなくても、作者が「設定・本文がどう変わったか」を具体的な差分として確認しながら、安心して書き直せる、小説の設定・執筆管理ツール。**

### 1.2 背景

- GitHubのコミット履歴・diff表示は優れた体験だが、多くの執筆者はそれを使ったことがない
- 小説の推敲は「書いては直す」の繰り返しであり、「前はどう書いていたか」「設定をいつ・どう変えたか」を振り返れる価値は大きい
- この体験をGitの知識なしに、小説投稿サイト上で自然に提供する（[Novel.md](../domain/Novel.md)のChangeLog設計思想を参照）

### 1.3 最小成功

自分一人で、Worldの中に設定(Setting)を自由に作り、それを見ながら作品(Novel/Chapter/Episode)を執筆でき、変更履歴を差分で振り返れる。

### 1.4 完了条件（チェックリスト）

- [ ] 設定管理が自由かつ詳細にできる（World / Setting / SettingTemplate / SettingField / 関係性）
- [ ] 設定を執筆画面から参照できる（リンク記法＋サイドパネル）
- [ ] 設定の作成・編集・削除・一覧・検索ができる
- [ ] World 配下で作品（章・話・本文）を執筆できる
- [ ] 設定・作品・本文を検索できる
- [ ] **変更履歴を差分（diff）で確認できる**（Phase 1の中核機能）

---

## 2. Phase 1 に含めるもの／含めないもの

`docs/domain/`配下の各ドメイン設計（A〜L区分）を、Phase 1に含めるかどうかで仕分けた結果。

### 2.1 含めるもの（Phase 1）

| 区分 | ドメイン | 含める理由 |
|---|---|---|
| A | 全体方針・ドメイン構造 | 前提 |
| B | ユーザー・ペンネーム管理 | 自分のアカウント・名義を管理するために必要最小限は必須 |
| C | World（世界観） | 設定・作品の入れ物として必須 |
| D | Setting（設定） | Phase 1のコア機能 → [Setting.md](../domain/Setting.md) |
| E | 作品・執筆（Novel/Chapter/Episode） | 執筆機能そのもの。**ChangeLog（差分表示）が最重要機能** → [Novel.md](../domain/Novel.md) |
| F | 閲覧・検索（自分向け） | 自分のWorld/Setting/作品を見る・探すために必須 |
| G | 非機能・運用 | エクスポート機能・テスト方針 |

### 2.2 含めないもの（Phase 2以降）

| 区分 | ドメイン | 見送る理由 |
|---|---|---|
| H | 共同制作 | Phase 1は**自分一人（単独作者）向け**（2026-08-22決定）。招待・権限管理・掲示板は複雑さの割にPhase 1では使わない → [Collaboration.md](../domain/Collaboration.md) |
| I | コミュニケーション | コメント・評価・フォロー・DMは読者の存在が前提。Phase 1に読者はいない → [Communication.md](../domain/Communication.md) |
| J | 公開・共有 | 「公開する」という概念自体が不要。全て非公開固定で運用する → [Publishing.md](../domain/Publishing.md) |
| K | 読者向け機能 | タグ・カテゴリ・ランキング・お気に入りは読者向け機能そのもの → [Reader.md](../domain/Reader.md) |
| L | 管理機能 | 公開しない以上、通報・モデレーションの出番がない → [Moderation.md](../domain/Moderation.md) |

**2026-08-22の方針決定**: 「一般公開・読者向け機能はPhase 1に完全に除外する」「Phase 1利用者は自分一人のみとし、共同制作もPhase 2以降とする」の2点を明確化した。

---

## 3. Phase 1 のデータモデルへの影響

`docs/domain/`の各ファイルはA〜L全区分を詳細設計済みだが、Phase 1の実装では以下のフィールド・モデルは**実装を見送る**（設計ドキュメントとしては残し、Phase 2着手時に実装する）。

### 3.1 実装を見送るフィールド

| モデル | フィールド | 理由 |
|---|---|---|
| Novel | `visibility` | J区分（公開・共有）はPhase 2以降 |
| Novel | `category` | K区分（読者向け機能）はPhase 2以降 |
| Novel | `status`（進捗ステータス） | H区分（共同制作）の文脈で決めた項目。単独作者でも使えなくはないが、Phase 1では見送り、Phase 2着手時に要否を再検討 |
| Episode | `visibility` | 同上（J区分） |
| Episode | `view_count` | K区分（読者向け機能）はPhase 2以降 |
| Setting | `is_public` | J区分（公開・共有）はPhase 2以降 |
| User | `status`（アカウント状態） | L区分（管理機能）はPhase 2以降 |
| 全モデル共通 | `deleted_by` | 管理者による強制削除（L区分）はPhase 2以降。Phase 1では削除実行者は常に本人のため不要 |

### 3.2 実装を見送るモデル

- Collaborator, Board, BoardThread, BoardPost（H区分）
- Comment, Rating, Follow, DirectMessage, Notification（I区分）
- VisibilityGrant（J区分）
- Category, Tag, NovelTag, Favorite（K区分）
- ReportReason, Report, AccountAction（L区分）

### 3.3 認証まわりの簡略化（2026-09-03決定）

Phase 1は自分一人しか使わないため、**メール送信を伴う機能はすべて見送る**。

- パスワードリセット（メール送信方式）: 見送り。商用利用を検討する段階で追加する
- パスワード変更: 見送り（同上）
- 登録時のメール確認（verification）: 行わない

登録時にemail・パスワードの保存は行い、ログイン（メールアドレスまたはユーザーID＋パスワード、Django標準認証）はPhase 1でも実装する。

### 3.4 ChangeLogの扱い（Phase 1に残す）

ChangeLog（変更履歴・差分表示）はPhase 1の中核機能のため、当然実装する。ただし以下はPhase 1の前提（自分一人・非公開固定）により単純化できる。

- 閲覧権限判定（[Novel.md](../domain/Novel.md)決定: 常に作者・共同制作者限定）は、Phase 1では実質「常に本人のみ」となり、Collaborator参照は不要
- 除名済み共同制作者の匿名化ルールは、共同制作が存在しないPhase 1では該当なし

---

## 4. Phase 1 の実装優先順位

| 順位 | 領域 | 備考 |
|:----:|------|------|
| 1 | ユーザー・World（最小限） | ログインしてWorldを作れる状態 |
| 2 | **設定管理（Setting）** | Phase 1のコア。最初に厚く作り込む |
| 3 | 作品・執筆（Novel/Chapter/Episode） | Setting参照機能を含む |
| 4 | **ChangeLog（差分表示）** | Phase 1のコンセプトそのもの。執筆・設定機能が動いてから着手 |
| 5 | 閲覧・検索（自分向け） | 最後でよい |

## 5. Phase 1 完了後の次領域

| 順位 | 領域 | 備考 |
|:----:|------|------|
| 1 | H. 共同制作 | 「作者や編集者が差分を確認できる」というコンセプトを、複数人での利用に拡張する自然な次のステップ |
| 2 | J. 公開・共有 | 共同制作の次に、外部への公開を検討 |
| 3 | I / K / L | 公開後、読者・コミュニケーション・管理機能を順次検討 |

### 実装スタック

**Python / Django + React** でPhase 1を実装する。

---

## 6. 関連ドキュメント

- [functional-scope.md](../business/functional-scope.md)（機能要件、A〜L全区分整理済み）
- [todo.md](../../todo.md)（決定事項リスト）
- `docs/domain/`（User.md / World.md / Setting.md / Novel.md / Collaboration.md / Communication.md / Publishing.md / Reader.md / Moderation.md）
- [プロダクト定義.md](./プロダクト定義.md)
