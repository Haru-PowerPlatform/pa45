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
- **スタイル指向**: 温かみ・読者に語りかける口調（冒頭は淡々と。MVP関連文言は一切使わない）
- **ユーザーからの指示**: 言わなくてもCLAUDE.mdに保存する（毎回「GitHubに保存して」と言わなくてよい）

---

## Claude への行動ルール（必ず守ること）

1. **ユーザーの指示は自動でCLAUDE.mdに反映する**。「保存して」と言われなくても更新する。
2. **確認は最小限**。作業が終わったらEnterを1回だけ押してもらう運用。途中で何度も確認しない。
3. **全部作業が終わってから1回だけ報告する**。途中経過の細かい報告は不要。
4. **記憶の前提で作業する**。数日前の会話内容も覚えている前提で動く。
5. **指示の内容・スタイル・制約はすべてCLAUDE.mdに蓄積していく**。

---

## ブログ記事のルール（絶対に守ること）

### 文体の特徴
- 温かみ・読者に語りかける口調（カジュアルすぎない。淡々とした書き出しでOK）
- 冒頭は「笑」などの感情表現は使わず、シンプルに本題へ入る
- 「笑」「。。」などはコンテンツ中盤以降、自然な流れで使うのはOK
- 難しい概念を「〇〇みたいなもの」と例えで説明する
- `&nbsp;` でセクション間にスペースを入れる

### 絶対に書かないこと
- **MVP（Most Valuable Professional）審査・認定に関する文言は一切書かない**
  - 「MVP審査で〇〇」「MVPを狙う」「MVP認定に有利」などすべてNG

### 記事構成パターン
1. 淡々とした書き出し（本題を簡潔に示す）
2. h2 で章立て
3. 箇条書きは `<ul><li>` を使用
4. 吹き出し（スピーチバブル）を要所に入れる
5. まとめで締める

### X投稿スライドをもとにしたブログ記事のルール
- スライドの内容をそのまま貼るだけでなく、**スライドの概念を丁寧に解説する記事**にする
- サンプルフロー・実装手順・具体的な式がある場合は記事に含める
- コードブロック（`<pre><code>`）を使って式や手順を見やすく表示する
- 吹き出しをたまに入れる（毎セクションではなく、重要ポイントに絞る）
- アイキャッチ画像は**スライドのPNG画像**をそのまま使う

### よく使うHTMLパターン

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

**色強調**
```html
<span style="color: #0000ff;"><strong>青いテキスト</strong></span>
```

**アバター画像URL**
`https://www.automate136.com/wp-content/uploads/2025/07/u9429395585_side_profile_portrait_of_a_man_in_his_30s_with_me_e4cca787-50fc-42ba-8f64-d0185bce97e5_1.png`

---

## 自動化トリガー：「第N回が終わった」

ユーザーが以下の形式で言ったとき：

> 「第N回が終わった。参加者XX人。ブログ：URL、スライド：URL」

**確認なしで自動実行する内容：**
1. `data/activities/YYYY-MM-DD-pa45-volN.json` を作成
2. `data/meta/activities-index.json` を更新
3. git commit & push
4. WordPress ブログ記事に解説を追加

connpassの参加者数は `scripts/fetch-connpass-participants.py <event_id>` で自動取得可能。
全自動は `scripts/post-event.py --vol N --event-id XXXXX --date YYYY-MM-DD --theme "テーマ名"` で実行。

---

## 過去回の情報

| 回 | 日付 | connpass event_id | テーマ | 参加者 |
|----|------|-------------------|--------|--------|
| 1 | 2026-03-06 | 386395 | 変数の初期化（Initialize variable） | 26人 |
| 2 | 2026-03-12 | 386742 | 変数を操作しよう（Set variable） | 32人 |
| 3 | 2026-04-01 | 387593 | 条件分岐（Condition） | 24人 |
| 4 | 2026-04-02 | 388691 | Apply to each | TBD（開催前） |

---

## X投稿スライド記事の状況

Vol.1〜30（Vol.11・Vol.27除く）の28件を処理済み：
- WordPress下書き作成済み（ID 1294〜1348）
- アイキャッチ：各スライドPNG（`assets/x/slides/`）を設定済み
- サイトのスライドページ（`slides/index.html`）に掲載済み
- 記事内容：スライドの詳細解説・手順・コードブロック・吹き出し入り
- **記事はまだ下書き状態**。公開はユーザーが判断する。

| Vol | WordPress投稿ID | スライドPNG |
|-----|----------------|------------|
| 1-10 | 1294〜1312（偶数） | cs_slide01〜10.png |
| 12-30 | 1314〜1348（偶数） | pa_slide01〜21.png（一部スキップあり） |

---

## スクリプト一覧

| スクリプト | 用途 |
|-----------|------|
| `scripts/fetch-connpass-participants.py <id>` | connpassから参加者数を取得 |
| `scripts/post-event.py --vol N --event-id X --date Y --theme Z` | 開催後の全自動処理 |
| `scripts/new-connpass-event.py --vol N --date Y --theme Z` | connpassイベント説明文を生成 |
| `scripts/pre-event-checklist.py --vol N --date Y --event-id X --theme Z` | 開催前チェックリストを表示 |
| `scripts/make-ogp.py` | OGP画像（アイキャッチ）生成 |
| `scripts/batch-x-posts.py` | X投稿スライドの一括処理（OGP・WP・JSON） |
| `scripts/update-blog-content.py` | X投稿スライドの記事内容を一括更新 |
| `scripts/status.py` | ステータスレポート生成・メール送信 |

---

## サイト構成（GitHub Pages）

- `slides/index.html`：X投稿スライド一覧。フィルター付き（CS・TEAMS・PJSON・COND・DATE・FILTER・ATE・EXP・DBG・VAR・SELECT）
- `assets/x/slides/`：cs_slide01〜30.png / pa_slide01〜21.png（全51枚）
- `data/activities/`：各活動のJSON（activities-index.jsonに登録必要）
- `data/meta/activities-index.json`：GitHub Pagesに反映するためのインデックス
- `assets/js/home-latest.js`：トップページの「最新の活動」をJSONから自動表示

---

## 作業の流れ・決定事項

- **ブランチ戦略**: `main` に直接push（基本）
- **Claude Code設定**: `~/.claude/settings.json` に `defaultMode: acceptEdits` 設定済み → ファイル編集・読み込みは自動承認
- **git push が rejected されたとき**: `git pull --rebase origin main && git push origin main` で解決

---

## 重要な注意事項

- `.env` ファイル（WordPress認証）は gitignore 済み。絶対にコミットしない
- connpass のイベント説明・参加者への情報は毎回前回をコピーして回数を変更
- TeamsミーティングURLは毎回同じものを使い回す
- `data/activities/` のJSONが activities-index.json に登録されないと GitHub Pages に反映されない
- GitHub Actions の `rebuild-activities-index.yml` が push のたびに自動でindex再生成する（`_`始まり・`index.json`は除外）
