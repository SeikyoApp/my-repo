# ベースイメージ: 軽量な Python 環境
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係をインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリコードをコンテナにコピー
COPY . .

# アプリケーションを実行するエントリポイントを指定
CMD ["python", "ClinicalTrials_gov_API.py"]
