import os
from contextlib import asynccontextmanager

import yaml
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from router.v1.router import router as v1_router

load_dotenv()


# yamlファイルを生成する
def generate_swagger_yaml():
    """OpenAPI仕様をYAMLファイルとして出力する"""
    # OpenAPI仕様を取得
    openapi_json = app.openapi()

    # JSONをYAMLに変換
    openapi_yaml = yaml.dump(openapi_json, sort_keys=False, allow_unicode=True)

    # ファイルに保存
    with open("swagger.yml", "w", encoding="utf-8") as f:
        f.write(openapi_yaml)


# アプリケーション起動時にSwagger仕様を生成
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 起動時の処理
    if os.getenv("STAGE") == "dev":
        generate_swagger_yaml()
    yield
    # シャットダウン時の処理
    pass

app = FastAPI(lifespan=lifespan)
app.include_router(v1_router, prefix="/v1")

# CORSミドルウェアの設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["authorization", "content-type", "x-api-key"],
)

handler = Mangum(app)
