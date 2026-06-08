# 登壇レポート：なんでもCopilot 大阪 ― コミュニティ再確認の記録

automate136.com 向け単発ブログ記事（登壇感想／コミュニティ振り返り）。なんでもCopilot 大阪会（2026-06-07）に登壇した日の所感をまとめたもの。

## ステータス
- 状態: **WordPress 下書き（status=draft）** — 公開はユーザー確認後に手動
- WordPress Post ID: **2475**
- 編集 URL: https://www.automate136.com/wp-admin/post.php?post=2475&action=edit
- プレビュー URL: https://www.automate136.com/?p=2475&preview=true
- タイトル: なんでもCopilot 大阪会に登壇して ── AI時代に、わざわざ会いに行く意味が腑に落ちた日
- 作成日: 2026-06-08
- カテゴリ: ID 77（コミュニティ運営）
- アイキャッチ: 未作成
- 登壇スライドリンク: https://haru-powerplatform.github.io/pa45/talks/2026-osaka-copilot/slides.html（記事内CTA 2箇所）

## 記事の柱（ユーザーの口頭感想を整理）
1. 運営の皆さんへの感謝（見えない段取り・気持ちよく話せる場をつくってもらえた）
2. DX推進は孤独になりやすい（社内で同じ熱量の相手が少ない・一人で調べて直す繰り返し）
3. コミュニティ＝エネルギーの補給場所（人に会うと「またやろう」が戻ってくる）を再確認
4. 同じ"推し"を持つ人に出会えるありがたさ（Copilot/Power Platform/Microsoft製品）
5. 当日のX投稿を本文中に埋め込み（ユーザーが後で差し込む）

## X投稿の差し込み箇所
- `article.html` 内、`<h2>当日のようす（Xより）</h2>` の直下
- `<!-- ▼▼▼ ... ▼▼▼ -->` と `<!-- ▲▲▲ ... ▲▲▲ -->` のコメントで挟んだ `.x-embed-slot` の枠を、X公式の埋め込みコード（`<blockquote class="twitter-tweet">...`）でまるごと置き換える

## ルール遵守
- 内部運用に関する文言なし（CLAUDE.md ルール）
- 架空の参加者の声・チャット実況・盛り上がり描写なし（feedback_pa45_blog_no_fabrication）
- 勤務先を特定する表現なし（開示ライン）
- 上から目線にならないトーン・断定回避（「〜と思っています／気がします」）
- 吹き出し（haru-profile）を要所に2箇所、&nbsp; でセクション間スペース、hl-marker でマーカー演出

## 次にやること
1. ユーザーが内容確認・微修正
2. 当日のX投稿の埋め込みコードを差し込む
3. アイキャッチ作成（任意）
4. WordPress 下書き作成 → 手動公開
5. 公開後 IndexNow 送信
