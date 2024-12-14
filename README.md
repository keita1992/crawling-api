# 環境要件

- Docker
- Docker Compose
- AWS CLI(本番環境にデプロイを行う管理者のみ)
- AWS SAM CLI(本番環境にデプロイを行う管理者のみ)

# 主要な利用ライブラリ

- FastAPI - Web フレームワーク API
- Mangum - AWS Lambda 用アダプター
- Python-dotenv - 環境変数管理

# 環境構成

- AWS Lambda
- API Gateway

# 環境構築

## 1. リポジトリをクローン

```
git clone https://github.com/keita1992/crawling-api.git
cd crawling-api
```

## 2. .env.sample から.env ファイルを作成

```
cp .env.sample .env
```

## 3. 以下のコマンドを実行

```
docker compose build
docker compose up -d
docker compose exec fastapi bash -c "poetry install"
```

# 開発手順

```
docker compose exec fastapi bash -c "poetry run task dev"
```

# テスト実行

```
sam local invoke -e events/event.json LambdaFunction --env-vars ./events/.env.json
```

# コマンド一覧

- `poetry run task dev` - 開発サーバー起動(Hot Reload 有効)
- `poetry run task lint` - コードスタイルチェック
- `poetry run task fix` - コードスタイル自動修正

# デプロイ手順

1. `samconfig.sample.yaml`から`samconfig.yaml`を作成

```
cp samconfig.sample.yaml samconfig.yaml
```

2. S3 バケットを作成
3. `samconfig.yaml` に必要なパラメータを設定
4. 以下のコマンドでデプロイ

```
// 検証環境
sam build --config-env staging && sam deploy --config-env staging

// 本番環境
sam build --config-env prod && sam deploy --config-env prod
```

4. (オプション) カスタムドメインを設定する場合

- ACM でカスタムドメインの証明書を取得
- API Gateway でカスタムドメインの設定
- Route53 で A レコードを登録し、API のドメインを API Gateway に紐づける

# API 呼び出しテスト

```
curl -X POST {YOUR_API_URL}/v1/crawl \
-H "Content-Type: application/json" \
-H "x-api-key: {API_GATEWAY_API_KEY}" \
-d '{"url": "https://google.com"}'
```

# アプリケーション構成

- `src/` - アプリケーションコード
- `tests/` - テストコード

# 環境変数

- `STAGE` - 実行環境(dev/prod)
