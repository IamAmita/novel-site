-- Novel Site データベース初期化スクリプト
-- MySQL 8.0用

-- 文字セットをUTF-8に設定
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 小説サイト用データベースの作成確認
CREATE DATABASE IF NOT EXISTS `novel_site` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- テスト用データベースの作成
CREATE DATABASE IF NOT EXISTS `novel_site_test` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- ユーザー権限の設定
GRANT ALL PRIVILEGES ON `novel_site`.* TO 'sail'@'%';
GRANT ALL PRIVILEGES ON `novel_site_test`.* TO 'sail'@'%';
FLUSH PRIVILEGES;

-- 初期化完了ログ
SELECT 'Novel Site Database Initialization Completed' AS Status;
