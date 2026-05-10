# 📘 マナビーテスト 解説サイト

家庭学習研究社「マナビーテスト」の小6本人向け解説をまとめたシングルページサイト。

## 公開URL
https://haru-powerplatform.github.io/manabie-kaisetsu/

## 機能
- 📑 タブ切替（理科・算数・MANABIEテキスト）
- 📝 問題文＋ 図 ＋ 解き方ステップ ＋ 答え（クリックで開示）
- ✅ 解答チェック（解けた／解きなおし）
- 🎟 シールガチャ（100種・コレクション機能）
- 📈 進捗バー・問題ジャンプ目次
- 📲 PC ⇄ iPad の履歴コピペ同期

## 構成
- `index.html` ── 本体（シングルページ）
- `figs/` ── 解説用画像（PNG、~65枚）

## 更新方法
1. ローカルで `index.html` を編集
2. `git add . && git commit -m "..."`
3. `git push origin main`
4. GitHub Pages が自動でデプロイ（数十秒）
