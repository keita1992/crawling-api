FROM python:3.9-slim

# poetryのインストールと設定
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

# タイムゾーンの設定
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y gcc python3-dev git

ARG USER_ID
ARG GROUP_ID

# グループが存在しない場合は作成
RUN if ! getent group ${GROUP_ID}; then \
    groupadd -g ${GROUP_ID} appuser; \
fi

# ユーザーが存在しない場合は作成
RUN if ! id -u ${USER_ID} > /dev/null 2>&1; then \
    useradd -m -u ${USER_ID} -g ${GROUP_ID} -s /bin/bash appuser; \
else \
    usermod -s /bin/bash $(id -nu ${USER_ID}); \
fi

WORKDIR /app

# 依存関係のインストール
COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock* /app/poetry.lock*

RUN poetry install --no-root

USER ${USER_ID}:${GROUP_ID}
