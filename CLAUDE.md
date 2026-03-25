# CLAUDE.md — PA45 プロジェクト 永続コンテキスト

このファイルはClaude Codeが毎回自動読み込みするコンテキストです。
セッションをまたいで記憶すべき情報をここに書いています。

---

## プロジェクト概要

**PA45（Power Automate 45分）**は、はる（ism136）が主催するPower Automateハンズオン勉強会。
- connpassグループ: `powerautomate-create`
- 開催周期: 毎週木曜（不定期）
- サイト: GitHub Pages（このリポジトリ） + ブログ: https://www.automate136.com

---

## オーナー情報

- **名前**: はる（ism136）
- **WordPress**: https://www.automate136.com
- **WordPress認証**: `.env` ファイル（リポジトリルート、gitignore済み）を参照
- **スタイル指向**: カジュアル・温かみ・読者に語りかける口調

---

## 自動化トリガー：「第N回が終わった」

ユーザーが以下の形式で言ったとき：

> 「第N回が終わった。参加者XX人。ブログ：URL、スライド：URL」

**確認なしで自動実行する内容：**
1. `data/activities/YYYY-MM-DD-pa45-volN.json` を作成（日付・connpass_event_id・participants・evidence URLs 含む）
2. `data/meta/activities-index.json` を更新
3. git commit & push → PR作成
4. WordPress ブログ記事に `<h3>Slide N：タイトル</h3>` + 解説を追加

**一時停止するのは PR マージの確認のみ。**

connpassの参加者数は `scripts/fetch-connpass-participants.py <event_id>` で自動取得可能。
全自動は `scripts/post-event.py --vol N --event-id XXXXX --date YYYY-MM-DD --theme "テーマ名"` で実行。

---

## 過去回の情報

| 回 | 日付 | connpass event_id | テーマ | 参加者 |
|----|------|-------------------|--------|--------|
| 1 | 2026-03-06 | （要確認） | （要確認） | 26人 |
| 2 | 2026-03-12 | （要確認） | （要確認） | 32人 |
| 3 | 2026-03-19 | 387593 | （要確認） | 25人 |
| 4 | 2026-04-02 | 388691 | Apply to each | TBD（開催前） |

---

## スクリプト一覧

| スクリプト | 用途 |
|-----------|------|
| `scripts/fetch-connpass-participants.py <id>` | connpassから参加者数を取得 |
| `scripts/post-event.py --vol N --event-id X --date Y --theme Z` | 開催後の全自動処理 |
| `scripts/new-post.py` | WordPress記事作成＋OGP生成＋サイト更新 |
| `scripts/make-ogp.py` | OGP画像（アイキャッチ）生成 |

---

## ブログ文体・HTMLパターン

はるさんのブログ（automate136.com）の文体・スタイル：

### 文体の特徴
- カジュアル・温かみ・読者に語りかける口調
- 自分ツッコミ・ユーモアを冒頭に入れる（例：「ホッとしております 笑」）
- 「笑」「。。」など感情表現をそのまま書く
- 難しい概念を「〇〇みたいなもの」と例えで説明する
- セクション末尾に「↓」で次へ誘導
- `&nbsp;` でセクション間にスペースを入れる

### 記事構成パターン
1. カジュアルな書き出し（自分ツッコミ or 感謝）
2. h2 で章立て
3. 箇条書きは `<ul><li>` を使用
4. 吹き出しで自分の言葉として一言まとめ
5. 次回予告やCTAで締め

### よく使うHTMLパターン

**強調（大きい文字）**
```html
<span style="font-size: 24px;"><strong>テキスト</strong></span>
```

**色強調**
```html
<span style="color: #ff0000;">赤いテキスト</span>
<span style="color: #0000ff;">青いテキスト</span>
```

**吹き出し（スピーチバブル）**
```html
<div class="speech-wrap sb-id-14 sbs-stn sbp-l sbis-cb cf">
<div class="speech-person">
<figure class="speech-icon"><img class="speech-icon-image" src="https://www.automate136.com/wp-content/uploads/2025/07/u9429395585_side_profile_portrait_of_a_man_in_his_30s_with_me_e4cca787-50fc-42ba-8f64-d0185bce97e5_1.png" alt="" width="1024" height="1024" /></figure>
</div>
<div class="speech-balloon">
吹き出しの中のテキスト
</div>
</div>
```

**引用（アンケート・声など）**
```html
<blockquote><strong>「〇〇」</strong></blockquote>
```

**アバター画像URL**
`https://www.automate136.com/wp-content/uploads/2025/07/u9429395585_side_profile_portrait_of_a_man_in_his_30s_with_me_e4cca787-50fc-42ba-8f64-d0185bce97e5_1.png`

---

## 作業の流れ・決定事項

- **ブランチ戦略**: `main` に直接push（小さい変更）or PRを作成
- **PR作成後**: ユーザーがGitHubでマージ、その後ブランチ削除
- **Claude Code設定**: `~/.claude/settings.json` に `defaultMode: acceptEdits` 設定済み → ファイル編集・読み込みは自動承認
- **worktree**: `.claude/worktrees/` 以下に作業用worktreeが作られることがある

---

## WordPress 既存記事

| 投稿ID | タイトル | ステータス |
|--------|----------|------------|
| 1288 | Power Automateとの設計判断ポイント ― 実行型AIエージェント時代の役割分担を整理する ― | 下書き |
| 1287 | （OGP画像メディア） | — |

---

## connpass Vol.4 残タスク

- [ ] アイキャッチ画像を手動アップロード（`C:\Users\isamu\pa45_vol4_eyecatch.png`）
- [ ] イベントを公開（event_id: 388691）
- [ ] 開催後に参加者数を確定してJSONを更新

---

## 重要な注意事項

- `.env` ファイル（WordPress認証）は gitignore 済み。絶対にコミットしない
- connpass のイベント説明・参加者への情報は毎回前回をコピーして回数を変更
- TeamsミーティングURLは毎回同じものを使い回す
- `data/activities/` のJSONが activities-index.json に登録されないと GitHub Pages に反映されない
