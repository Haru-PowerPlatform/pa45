#!/bin/bash
# PA45 アイキャッチ自動生成 + WordPress投稿スクリプト
# 使い方: bash scripts/post-with-ogp.sh <PostId> <Title> [Sub] [Label]
# 例: bash scripts/post-with-ogp.sh 1224 "記事タイトル" "PA45" "業務効率化 × Teams 活用"

set -e

POST_ID="${1}"
TITLE="${2}"
SUB="${3:-Power Automate 45}"
LABEL="${4:-社外コミュニティ活動}"

if [ -z "$POST_ID" ] || [ -z "$TITLE" ]; then
  echo "使い方: bash scripts/post-with-ogp.sh <PostId> <Title> [Sub] [Label]"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# .env 読み込み（スペース入りパスワード対応）
while IFS='=' read -r key val; do
  [[ "$key" =~ ^#|^$ ]] && continue
  export "$key"="$val"
done < "$ROOT_DIR/.env"

TEMPLATE="$SCRIPT_DIR/ogp-template.html"
TEMP_HTML="$SCRIPT_DIR/ogp-temp.html"
PNG_PATH="$SCRIPT_DIR/ogp-output.png"
EDGE="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"

# ── Step 1: HTMLにタイトルを埋め込む ──────────────────────
echo "▶ Step 1: HTML生成..."
TITLE_HTML=$(echo "$TITLE" | sed 's/\\n/<br>/g')

sed \
  "s|<div class=\"title\" id=\"title\">[^<]*\(<br>[^<]*\)*</div>|<div class=\"title\" id=\"title\">${TITLE_HTML}</div>|g" \
  "$TEMPLATE" | \
sed "s|<span class=\"sub\" id=\"sub\">[^<]*</span>|<span class=\"sub\" id=\"sub\">${SUB}</span>|g" | \
sed "s|社外コミュニティ活動|${LABEL}|g" \
  > "$TEMP_HTML"

echo "  HTML OK"

# ── Step 2: Edge ヘッドレスでスクリーンショット ─────────────
echo "▶ Step 2: PNG生成..."
[ -f "$PNG_PATH" ] && rm "$PNG_PATH"

# bash の /c/... パスを Windows の C:/... に変換
WIN_TEMP_HTML=$(echo "$TEMP_HTML" | sed 's|^/c/|C:/|')
WIN_PNG_PATH=$(echo "$PNG_PATH" | sed 's|^/c/|C:/|')
FILE_URI="file:///${WIN_TEMP_HTML}"

"$EDGE" \
  --headless \
  --disable-gpu \
  --window-size=1280,720 \
  "--screenshot=${WIN_PNG_PATH}" \
  --hide-scrollbars \
  "$FILE_URI" 2>/dev/null

sleep 5

if [ ! -f "$PNG_PATH" ]; then
  echo "❌ PNG生成失敗"
  exit 1
fi
echo "  PNG OK: $PNG_PATH"

# ── Step 3: WordPress メディアアップロード ───────────────────
echo "▶ Step 3: WordPressにアップロード..."
FNAME="ogp-$(date +%Y%m%d-%H%M%S).png"

MEDIA_JSON=$(curl -s -X POST "${WP_URL}/wp-json/wp/v2/media" \
  --user "${WP_USER}:${WP_PASS}" \
  -H "Content-Disposition: attachment; filename=${FNAME}" \
  -H "Content-Type: image/png" \
  --data-binary "@${PNG_PATH}")

MEDIA_ID=$(echo "$MEDIA_JSON" | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')

if [ -z "$MEDIA_ID" ]; then
  echo "❌ アップロード失敗"
  echo "$MEDIA_JSON"
  exit 1
fi
echo "  Media ID: $MEDIA_ID"

# ── Step 4: アイキャッチ設定 ────────────────────────────────
echo "▶ Step 4: 投稿 #${POST_ID} にアイキャッチ設定..."
curl -s -X POST "${WP_URL}/wp-json/wp/v2/posts/${POST_ID}" \
  --user "${WP_USER}:${WP_PASS}" \
  -H "Content-Type: application/json" \
  --data-binary "{\"featured_media\":${MEDIA_ID}}" > /dev/null

echo ""
echo "✅ 完了！"
echo "   投稿ID    : $POST_ID"
echo "   メディアID: $MEDIA_ID"
echo "   管理画面  : ${WP_URL}/wp-admin/post.php?post=${POST_ID}&action=edit"

# 一時ファイル削除
rm -f "$TEMP_HTML"
