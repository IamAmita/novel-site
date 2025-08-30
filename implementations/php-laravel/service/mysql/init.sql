-- 小説投稿サイト用MySQL初期設定

-- 文字セット設定
SET NAMES utf8mb4;
SET character_set_client = utf8mb4;
SET character_set_connection = utf8mb4;
SET character_set_database = utf8mb4;
SET character_set_results = utf8mb4;
SET character_set_server = utf8mb4;

-- データベース作成（存在しない場合）
CREATE DATABASE IF NOT EXISTS novel_site 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- ユーザー作成・権限付与
CREATE USER IF NOT EXISTS 'novel_user'@'%' IDENTIFIED BY 'novel_pass';
GRANT ALL PRIVILEGES ON novel_site.* TO 'novel_user'@'%';

-- テスト用データベース
CREATE DATABASE IF NOT EXISTS novel_site_test 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON novel_site_test.* TO 'novel_user'@'%';

-- 権限反映
FLUSH PRIVILEGES;

-- 小説サイト用設定
USE novel_site;

-- 全文検索用設定（日本語対応）
SET GLOBAL innodb_ft_min_token_size = 1;
SET GLOBAL ft_min_word_len = 1;

-- その他最適化設定
SET GLOBAL innodb_buffer_pool_size = 134217728; -- 128MB
SET GLOBAL max_connections = 200;
SET GLOBAL wait_timeout = 28800;
SET GLOBAL interactive_timeout = 28800;
