# 開発支援ツール（tools）

Python/Django実装のパフォーマンス測定・開発支援を行うツール群。

## 📁 ディレクトリ構成

```
tools/
├── benchmark/              # パフォーマンス測定
│   ├── load-test/         # 負荷テスト
│   ├── memory-test/       # メモリ使用量測定
│   ├── response-time/     # レスポンス時間測定
│   └── results/           # 測定結果
└── scripts/               # 自動化スクリプト
    ├── setup/            # 環境構築自動化
    ├── migration/        # データ移行
    └── deployment/       # デプロイ自動化
```

## 🔬 benchmark/ - パフォーマンス測定

### 負荷テスト（load-test/）
```bash
# Apache Bench での負荷テスト
ab -n 1000 -c 10 http://localhost:8000/api/novels/

# wrk での負荷テスト
wrk -t4 -c100 -d30s http://localhost:8000/api/novels/
```

### メモリ使用量測定（memory-test/）
```bash
# Docker stats による測定
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### レスポンス時間測定（response-time/）
```bash
# 各エンドポイントのレスポンス時間測定
./benchmark/response-time/measure.js --endpoints ./config/endpoints.json
```

## 🤖 scripts/ - 自動化スクリプト

### 環境構築自動化（setup/）
```bash
./scripts/setup/setup-python.sh
```

### データ移行（migration/）
```bash
# データベースの初期化
./scripts/migration/init-db.sh

# サンプルデータの投入
./scripts/migration/seed-data.sh
```

### デプロイ自動化（deployment/）
```bash
./scripts/deployment/build.sh
./scripts/deployment/deploy-demo.sh
```

## 📊 測定項目・指標

### パフォーマンス指標
- **レスポンス時間**: 平均・最大・最小・パーセンタイル
- **スループット**: RPS（Request Per Second）
- **メモリ使用量**: 平均・最大・アイドル時
- **CPU使用率**: 平均・最大・負荷時
- **同時接続数**: 最大同時接続処理能力

### コード品質指標
- **複雑度**: サイクロマティック複雑度
- **テストカバレッジ**: 単体・統合テストのカバレッジ
- **依存関係**: 外部ライブラリ依存度

## 🔧 ツール要件

### 必要なツール
- **Python**: 分析スクリプト実行
- **Docker**: コンテナ環境での測定
- **Apache Bench** / **wrk**: 負荷テスト

### インストール
```bash
./scripts/setup/install-tools.sh
pip install -r requirements.txt
```

---

**目的**: Python/Django実装のパフォーマンス測定・品質分析
**更新頻度**: 実装の主要マイルストーン完了時、定期測定時
