# ユーザー系テーブル詳細

---

## 概要
ユーザー系テーブルは、小説投稿サイトのユーザー管理に関する全てのテーブルを管理します。

---

## 設計方針
- ユーザー情報とプロフィール情報は1対1で分離
- ユーザー登録時に必ずプロフィールも同時作成、削除もセットで行う運用
- is_admin等のフラグは初期のみ、将来的な権限拡張は権限管理テーブル・権限定義テーブルで柔軟に対応
- 履歴・ログ系は「履歴種別」「操作ユーザーID」を持ち、定期アーカイブ・自動削除運用を推奨
- ダイレクトメッセージは送信者・受信者ごとに論理削除フラグを持ち、両者削除時のみ物理削除
- ブロック・通報は理由・解除日時・対応状況等を管理

---

## テーブル一覧

### 基本情報
- [users.md](./users.md) - ユーザー基本情報
- [user_profiles.md](./user_profiles.md) - ユーザープロフィール情報

### 認証・セキュリティ
- [two_factor_auth.md](./two_factor_auth.md) - 2段階認証設定
- [login_history.md](./login_history.md) - ログイン履歴

### 権限管理
- [permissions.md](./permissions.md) - 権限定義
- [user_permissions.md](./user_permissions.md) - ユーザー権限管理

### コミュニケーション
- [follows.md](./follows.md) - フォロー関係
- [likes.md](./likes.md) - いいね
- [direct_messages.md](./direct_messages.md) - ダイレクトメッセージ

### モデレーション
- [blocks.md](./blocks.md) - ブロック
- [reports.md](./reports.md) - 通報

### 履歴・ログ
- [user_history.md](./user_history.md) - ユーザー情報変更履歴

---

## テーブル関係図

```
users (1) ←→ (1) user_profiles
users (1) ←→ (N) two_factor_auth
users (1) ←→ (N) login_history
users (1) ←→ (N) user_permissions
users (1) ←→ (N) follows (as follower)
users (1) ←→ (N) follows (as followed)
users (1) ←→ (N) likes
users (1) ←→ (N) direct_messages (as sender)
users (1) ←→ (N) direct_messages (as receiver)
users (1) ←→ (N) blocks (as blocker)
users (1) ←→ (N) blocks (as blocked)
users (1) ←→ (N) reports (as reporter)
users (1) ←→ (N) user_history

permissions (1) ←→ (N) user_permissions
```

---

## 主要な考慮点
- プロフィール情報の拡張性（将来的な複数プロフィールや公開/非公開対応など）
- 権限管理の粒度（どの対象にどの権限を付与できるかのルール整理）
- 退会・論理削除時のデータ保持方針（プロフィールや履歴の残し方、完全削除の有無）
- 2FAやセキュリティ設計（方式追加やbackup_codes運用は拡張時に見直し）
- 履歴・ログ系テーブルの肥大化対策（アーカイブ・自動削除運用ルールの設計）
- 外部サービス連携（SNSログイン等）を見据えた拡張性
- ユーザー状態管理（BAN、凍結、一時停止などの多様な状態管理） 