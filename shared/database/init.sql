-- PostgreSQL初期化スクリプト
-- app用データベース設定

-- データベース作成（既にdocker-composeで作成済み）
-- CREATE DATABASE app;

-- 拡張機能の有効化
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- 全文検索用の設定
CREATE TEXT SEARCH CONFIGURATION IF NOT EXISTS japanese (COPY = pg_catalog.simple);

-- 初期設定完了
SELECT 'Database initialization completed' as status; 