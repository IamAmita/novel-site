# API一覧サマリー

本ドキュメントは、小説投稿サイトの主要リソースごとに必要なAPIエンドポイントとHTTPメソッド、簡単な説明、優先度をまとめたサマリーです。

---

| 優先度 | リソース         | メソッド | エンドポイント                           | 説明                     |
|--------|------------------|----------|------------------------------------------|--------------------------|
| 高     | users            | POST     | /api/v1/users/regist                     | ユーザー新規登録         |
| 高     | auth             | POST     | /api/v1/auth/login                       | ログイン                 |
| 高     | auth             | POST     | /api/v1/auth/logout                      | ログアウト               |
| 高     | users            | GET      | /api/v1/users/{id}                       | ユーザー詳細取得         |
| 高     | novels           | GET      | /api/v1/novels                           | 小説一覧取得             |
| 高     | novels           | POST     | /api/v1/novels/new                       | 小説新規投稿             |
| 高     | novels           | GET      | /api/v1/novels/{id}                      | 小説詳細取得             |
| 高     | episodes         | GET      | /api/v1/novels/{novel_id}/episodes       | エピソード一覧取得       |
| 高     | episodes         | POST     | /api/v1/novels/{novel_id}/episodes/new   | エピソード新規作成       |
| 高     | comments         | GET      | /api/v1/novels/{novel_id}/comments       | コメント一覧取得         |
| 高     | comments         | POST     | /api/v1/novels/{novel_id}/comments       | コメント投稿             |
| 高     | follows          | POST     | /api/v1/users/{id}/follow                | フォローする             |
| 高     | follows          | DELETE   | /api/v1/users/{id}/follow                | フォロー解除             |
| 高     | follows          | GET      | /api/v1/users/{id}/followings            | フォロー一覧取得         |
| 高     | follows          | GET      | /api/v1/users/{id}/followers             | フォロワー一覧取得       |
| 中     | users            | PUT      | /api/v1/users/{id}                       | ユーザー情報更新         |
| 中     | users            | DELETE   | /api/v1/users/{id}                       | ユーザー削除             |
| 中     | novels           | PUT      | /api/v1/novels/{id}                      | 小説情報更新             |
| 中     | novels           | DELETE   | /api/v1/novels/{id}                      | 小説削除                 |
| 中     | episodes         | GET      | /api/v1/episodes/{id}                    | エピソード詳細取得       |
| 中     | episodes         | PUT      | /api/v1/episodes/{id}                    | エピソード更新           |
| 中     | episodes         | DELETE   | /api/v1/episodes/{id}                    | エピソード削除           |
| 中     | comments         | DELETE   | /api/v1/comments/{id}                    | コメント削除             |
| 中     | likes            | POST     | /api/v1/novels/{id}/like                 | いいねする               |
| 中     | likes            | DELETE   | /api/v1/novels/{id}/like                 | いいね解除               |
| 中     | bookmarks        | POST     | /api/v1/novels/{id}/bookmark             | ブックマークする         |
| 中     | bookmarks        | DELETE   | /api/v1/novels/{id}/bookmark             | ブックマーク解除         |
| 中     | notifications    | GET      | /api/v1/notifications                    | 通知一覧取得             |
| 中     | notifications    | PUT      | /api/v1/notifications/{id}/read          | 通知を既読にする         |
| 低     | settings         | GET      | /api/v1/settings                         | 設定一覧取得             |
| 低     | settings         | POST     | /api/v1/settings                         | 設定新規作成             |
| 低     | settings         | GET      | /api/v1/settings/{id}                    | 設定詳細取得             |
| 低     | settings         | PUT      | /api/v1/settings/{id}                    | 設定更新                 |
| 低     | settings         | DELETE   | /api/v1/settings/{id}                    | 設定削除                 |

---

※優先度は開発順やMVP（最小限プロダクト）を意識して暫定的に設定しています。今後の要件や運用に応じて見直す場合があります。

※今後の設計・実装に応じて追加・修正する場合があります。 