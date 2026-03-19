-- PostgreSQL 初期化スクリプト
-- Docker コンテナ初回起動時に自動実行されます

-- 拡張機能の有効化
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- タイムゾーン設定
SET timezone = 'Asia/Tokyo';
