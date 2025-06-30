# 作品統計テーブル（work_stats）

---

## 概要
作品系（小説、章、話、設定）の統計情報を一元管理するテーブル。閲覧数、いいね数、コメント数、評価などの統計データを効率的に管理し、パフォーマンスとスケーラビリティを向上させる。

---

## テーブル定義

| 属性名              | 型              | 必須 | 一意 | 説明                           |
|---------------------|-----------------|------|------|--------------------------------|
| id                  | int             | ○    | ○    | 統計ID（主キー）               |
| work_type           | varchar(20)     | ○    |      | 作品種別（novel:小説, chapter:章, story:話, setting:設定） |
| work_id             | int             | ○    |      | 作品ID（各作品テーブルの主キー） |
| user_id             | int             | ○    |      | 作成者ユーザーID（users.id）   |

### 基本統計
| view_count          | int             | ○    |      | 総閲覧数                       |
| unique_view_count   | int             | ○    |      | ユニーク閲覧数                 |
| like_count          | int             | ○    |      | いいね数                       |
| bookmark_count      | int             | ○    |      | ブックマーク数                 |
| comment_count       | int             | ○    |      | コメント数                     |
| share_count         | int             | ○    |      | シェア数                       |

### 評価統計
| rating_average      | decimal(3,2)    | ○    |      | 評価平均値                     |
| rating_count        | int             | ○    |      | 評価数                         |
| rating_1_count      | int             | ○    |      | 1点評価数                      |
| rating_2_count      | int             | ○    |      | 2点評価数                      |
| rating_3_count      | int             | ○    |      | 3点評価数                      |
| rating_4_count      | int             | ○    |      | 4点評価数                      |
| rating_5_count      | int             | ○    |      | 5点評価数                      |

### 時間別統計
| daily_view_count    | int             | ○    |      | 日次閲覧数                     |
| weekly_view_count   | int             | ○    |      | 週次閲覧数                     |
| monthly_view_count  | int             | ○    |      | 月次閲覧数                     |
| daily_like_count    | int             | ○    |      | 日次いいね数                   |
| weekly_like_count   | int             | ○    |      | 週次いいね数                   |
| monthly_like_count  | int             | ○    |      | 月次いいね数                   |

### メタデータ
| last_viewed_at      | datetime        |      |      | 最終閲覧日時                   |
| last_liked_at       | datetime        |      |      | 最終いいね日時                 |
| last_commented_at   | datetime        |      |      | 最終コメント日時               |
| last_rated_at       | datetime        |      |      | 最終評価日時                   |
| last_bookmarked_at  | datetime        |      |      | 最終ブックマーク日時           |
| last_shared_at      | datetime        |      |      | 最終シェア日時                 |

### ランキング・スコア
| popularity_score    | decimal(10,4)   | ○    |      | 人気度スコア                   |
| quality_score       | decimal(10,4)   | ○    |      | 品質スコア                     |
| trending_score      | decimal(10,4)   | ○    |      | トレンドスコア                 |
| weekly_rank         | int             |      |      | 週間ランキング順位             |
| monthly_rank        | int             |      |      | 月間ランキング順位             |
| all_time_rank       | int             |      |      | 総合ランキング順位             |

### 更新管理
| updated_at          | datetime        | ○    |      | 更新日時                       |
| created_at          | datetime        | ○    |      | 作成日時                       |
| deleted_at          | datetime        |      |      | 論理削除日時                   |

---

## インデックス

| インデックス名                    | 種類 | 説明               | カラム                |
|----------------------------------|------|-------------------|----------------------|
| PRIMARY KEY                     | 主キー | 統計IDの主キー     | id                   |
| UNIQUE                          | 複合一意 | 作品種別・作品IDの組み合わせ一意 | work_type, work_id |
| INDEX                           | 通常 | 作品種別検索用     | work_type            |
| INDEX                           | 通常 | 作品ID検索用       | work_id              |
| INDEX                           | 通常 | 作成者検索用       | user_id              |
| INDEX                           | 通常 | 閲覧数検索用       | view_count           |
| INDEX                           | 通常 | いいね数検索用     | like_count           |
| INDEX                           | 通常 | 評価平均検索用     | rating_average       |
| INDEX                           | 通常 | 人気度スコア検索用 | popularity_score     |
| INDEX                           | 通常 | 最終閲覧日時検索用 | last_viewed_at       |
| INDEX                           | 複合 | 作品種別・閲覧数検索用 | work_type, view_count |
| INDEX                           | 複合 | 作品種別・いいね数検索用 | work_type, like_count |
| INDEX                           | 複合 | 作品種別・評価平均検索用 | work_type, rating_average |
| INDEX                           | 複合 | 作品種別・人気度スコア検索用 | work_type, popularity_score |
| INDEX                           | 複合 | ユーザー・作品種別検索用 | user_id, work_type |
| INDEX                           | 複合 | 更新日時・作品種別検索用 | updated_at, work_type |

---

## 制約条件

### 主キー制約
- `id`: 自動採番（AUTO_INCREMENT）

### 一意制約
- `work_type`と`work_id`の組み合わせは一意

### 外部キー制約
- `user_id` → `users.id`

### チェック制約
- `work_type` IN ('novel', 'chapter', 'story', 'setting')
- `rating_average` >= 0.00 AND `rating_average` <= 5.00
- `view_count` >= 0
- `like_count` >= 0
- `bookmark_count` >= 0
- `comment_count` >= 0
- `share_count` >= 0
- `rating_count` >= 0
- `rating_1_count` >= 0
- `rating_2_count` >= 0
- `rating_3_count` >= 0
- `rating_4_count` >= 0
- `rating_5_count` >= 0

---

## 設計補足

### 統計管理
- 作品系の全統計を一元管理
- リアルタイム更新とバッチ更新の併用
- キャッシュ戦略との連携

### スコア計算
- **人気度スコア**: 閲覧数、いいね数、ブックマーク数を重み付け
- **品質スコア**: 評価平均、コメント数を重み付け
- **トレンドスコア**: 最近の活動度を重み付け

### ランキング管理
- 週間・月間・総合ランキングの自動更新
- バッチ処理による定期ランキング計算
- ランキング変更の履歴管理

### 時間別統計
- 日次・週次・月次の統計を事前計算
- 古い統計データの自動クリーンアップ
- 統計データの圧縮・アーカイブ

---

## 関連テーブル

- `novels`: 多対1の関係（小説統計）
- `chapters`: 多対1の関係（章統計）
- `stories`: 多対1の関係（話統計）
- `settings`: 多対1の関係（設定統計）
- `users`: 多対1の関係（作成者）
- `work_stat_histories`: 1対多の関係（統計変更履歴）

---

## 運用上の注意点

1. **統計更新**: リアルタイム更新とバッチ更新の併用
2. **パフォーマンス**: インデックスの最適化とキャッシュ戦略
3. **データ整合性**: 統計データの定期的な整合性チェック
4. **ランキング更新**: 定期的なランキング計算と更新
5. **統計クリーンアップ**: 古い統計データの適切な管理
6. **スコア計算**: 人気度・品質・トレンドスコアの定期的な再計算
7. **バックアップ**: 統計データの定期的なバックアップ
8. **監視**: 統計更新処理の監視とアラート設定

---

## 統計更新フロー

### リアルタイム更新
1. ユーザーアクション発生（閲覧、いいね等）
2. Redisでカウント増加
3. キューに更新タスク追加
4. 非同期でDB更新

### バッチ更新
1. 定期的な統計集計（5分間隔）
2. 時間別統計の更新（1時間間隔）
3. ランキング計算（1日間隔）
4. スコア再計算（1週間間隔）

### キャッシュ戦略
1. 統計データのRedisキャッシュ
2. ランキングデータのキャッシュ
3. 人気作品の統計キャッシュ
4. 定期的なキャッシュ更新 