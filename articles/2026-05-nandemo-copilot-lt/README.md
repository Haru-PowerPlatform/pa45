# 登壇レポート：なんでもCopilot LT大会（オンライン・#80 第3回なんコパLT大会）

automate136.com 向け単発ブログ記事（登壇レポート）。2026-05-13 のオンラインLTで話した「会議コストBot」の内容をまとめたもの。**大阪会（2026-06-07 / Post 2475）とは別々のレポート**（ユーザー指示）。

## ステータス
- 状態: **WordPress 下書き（status=draft）** — 公開はユーザーが手動（自動公開しない）
- WordPress Post ID: **4392**
- 編集 URL: https://www.automate136.com/wp-admin/post.php?post=4392&action=edit
- プレビュー URL: https://www.automate136.com/?p=4392&preview=true
- タイトル: なんでもCopilotのLT大会でオンライン登壇して ──「会議を減らせない」から生まれた“会議コストBot”の話
- カテゴリ: 77（コミュニティ運営）＋76（Power Automate 実践・Tips）
- 本文: 約7,600字（タグ除去後）
- アイキャッチ: **未作成**（todo）

## 生成方法
`python build_article.py`（ローカルの article.html を再生成）。
`python build_article.py --push` で Post 4392 を上書き（status=draft 固定）。
- 認証は `pa45/.env`（WP_URL / WP_USER / WP_PASS）を使用。
- post_state.json に post_id を保持。

## 事実の出典（架空を書かない）
- LT の内容・数字・式はすべて当日スライド `assets/pa45/LT001_Copilot_MeetingCostBot_20260428.pptx` に基づく。
- イベント: なんでもCopilot #80（第3回なんコパLT大会）https://nandemo.connpass.com/event/390633/
- 会議コストBot＝Outlookトリガー＋7アクション（参加者数 split/length → 合計人数 → ticks で会議時間 → コスト=人数×分×(時給÷60) → Teams通知）。
- activity ログ: `pa45/data/activities/2026-05-13-lt-copilot-meeting-cost-bot.json`

## 文体ルール遵守（「AIが書いた記事に見えないように」）
- 本文に「Copilotで書いた」等の但し書きを置かない（題材としてのCopilotはOK）。
- 文末バリエ（です/ます一辺倒にしない・体言止め・言い切りを混ぜる）、章の入り方を毎回変える。
- 禁止語スキャン済み: 正直／素直に／いかがでしたか／近年／となっています／大げさな反応語 = 該当なし。
- 勤務先を特定する表現なし。時給は一般的な例として明記（末尾免責）。
- 架空の参加者の声・盛り上がり描写なし。

## 次にやること
1. はるが内容確認・微修正
2. アイキャッチ作成（未作成）
3. **手動で公開**（自動公開しない）
4. 公開後 IndexNow 送信
