#!/bin/bash
# WordPress下書き投稿スクリプト
# 使い方: bash scripts/wp-draft.sh "タイトル" "本文（HTML可）" "カテゴリ名"

set -e

# .env 読み込み
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
source "$SCRIPT_DIR/.env"

TITLE="${1}"
CONTENT="${2}"
CATEGORY_NAME="${3:-未分類}"

if [ -z "$TITLE" ] || [ -z "$CONTENT" ]; then
  echo "使い方: bash scripts/wp-draft.sh \"タイトル\" \"本文\" \"カテゴリ\""
  exit 1
fi

# カテゴリID取得
CATEGORY_ID=$(curl -s "${WP_URL}/wp-json/wp/v2/categories?search=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$CATEGORY_NAME'))")" \
  | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')

CATEGORY_ID="${CATEGORY_ID:-1}"

# 下書き投稿
RESPONSE=$(curl -s -X POST "${WP_URL}/wp-json/wp/v2/posts" \
  --user "${WP_USER}:${WP_PASS}" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": $(echo "$TITLE" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read().strip()))"),
    \"content\": $(echo "$CONTENT" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read().strip()))"),
    \"status\": \"draft\",
    \"categories\": [$CATEGORY_ID]
  }")

DRAFT_ID=$(echo "$RESPONSE" | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')
DRAFT_LINK=$(echo "$RESPONSE" | grep -o '"link":"[^"]*"' | head -1 | sed 's/"link":"//;s/"//')

if [ -n "$DRAFT_ID" ]; then
  echo "✅ 下書き作成完了！"
  echo "   ID: $DRAFT_ID"
  echo "   管理画面: ${WP_URL}/wp-admin/post.php?post=${DRAFT_ID}&action=edit"
else
  echo "❌ エラーが発生しました"
  echo "$RESPONSE"
fi
