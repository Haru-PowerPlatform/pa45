#!/usr/bin/env bash
# なんでもCopilot大阪スライドの自動コミット&プッシュ（安全版）
# - 公開してよいファイルだけをステージ（スライド本体＋参照画像＋connpassアイキャッチPNG）
# - agent-prompt.md / source原本 / 無関係な変更は絶対に含めない
# - 変更が無ければ何もしない
set -e
REPO="/c/Users/isamu/Documents/pa45"
SLIDE="talks/2026-osaka-copilot/slides.html"
cd "$REPO" || exit 0

# スライドに差分が無ければ終了（毎ターン無駄に走らせない）
git diff --quiet -- "$SLIDE" && git diff --cached --quiet -- "$SLIDE" && [ -z "$(git status --porcelain -- "$SLIDE")" ] && exit 0

# スライド＋参照画像だけをステージ
git add "$SLIDE" talks/2026-osaka-copilot/assets/haru-icon.png assets/connpass-eyecatch/*.png 2>/dev/null || true
grep -oE 'assets/photos/[^"]+\.(jpg|jpeg|png)|cutout/[^"]+\.png' "$SLIDE" \
  | sed 's#^cutout/#assets/photos/cutout/#' | sort -u \
  | while IFS= read -r f; do git add "talks/2026-osaka-copilot/$f" 2>/dev/null || true; done

# 念のため要配慮ファイルを除外
git reset -q -- talks/2026-osaka-copilot/assets/agent-prompt.md talks/2026-osaka-copilot/assets/photos/source 2>/dev/null || true

# ステージが空なら終了
git diff --cached --quiet && exit 0

git commit -q -m "auto: なんでもCopilot大阪スライド更新" || exit 0
git pull --rebase --autostash -q origin main 2>/dev/null || true
git push -q origin main 2>/dev/null && echo "[auto-push] slides published" || echo "[auto-push] push failed (手動で確認)"
