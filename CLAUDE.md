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
  - WP_USER / WP_PASS / WP_URL が設定済み
  - **ClaudeはWordPress REST API（`/wp-json/wp/v2/`）に直接アクセスできる**
  - カテゴリー確認: `GET /wp-json/wp/v2/categories?per_page=100`
  - 投稿操作: `GET/POST /wp-json/wp/v2/posts`
  - 「WordPressの管理画面を確認して」と言われたらREST APIで直接取得する（毎回同じ質問をしない）

### WordPressカテゴリー構成（2026-03-27更新）

| ID | カテゴリー名 | 用途 |
|----|------------|------|
| 76 | Power Automate 実践・Tips | 技術解説・Tips・ハウツー記事 |
| 77 | コミュニティ運営（PA45） | PA45セッションレポート・外部コミュニティ記事 |
| 78 | 社内DX推進・人材育成 | 社内研修・講座設計・育成事例 |

- デフォルトカテゴリー: ID76
- 新規投稿時のカテゴリーは上記3つのみ使用する
- **スタイル指向**: 温かみ・読者に語りかける口調（冒頭は淡々と。MVP関連文言は一切使わない）
- **ユーザーからの指示**: 言わなくてもCLAUDE.mdに保存する（毎回「GitHubに保存して」と言わなくてよい）

---

## Claude への行動ルール（必ず守ること）

1. **ユーザーの指示は自動でCLAUDE.mdに反映する**。「保存して」と言われなくても更新する。
2. **確認は最小限**。作業が終わったらEnterを1回だけ押してもらう運用。途中で何度も確認しない。
3. **全部作業が終わってから1回だけ報告する**。途中経過の細かい報告は不要。
4. **記憶の前提で作業する**。数日前の会話内容も覚えている前提で動く。
5. **指示の内容・スタイル・制約はすべてCLAUDE.mdに蓄積していく**。
6. **Cドライブのファイル・フォルダパスはコードブロックで表示する**。エクスプローラーのアドレスバーに貼り付けて開ける形式：` ```C:\Temp\file.png``` `。file:///リンクはClaudeチャットでは開けないので使わない。
7. **X予約投稿の時刻はすべて日本時間（JST）で指定する**。X.comのスケジューラーはアカウントのタイムゾーン設定に依存するため、ユーザーが「12時15分」と言ったら JST 12:15 として設定する。

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
<figure class="speech-icon"><img class="speech-icon-image" src="https://www.automate136.com/wp-content/uploads/2026/04/haru-profile.png" alt="" width="1024" height="1024" /></figure>
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
`https://www.automate136.com/wp-content/uploads/2026/04/haru-profile.png`

---

## 自動化トリガー：「第N回が終わった」

ユーザーが以下の形式で言ったとき：

> 「第N回が終わった。参加者XX人。ブログ：URL、スライド：URL」

**確認なしで自動実行する内容：**
1. `data/activities/YYYY-MM-DD-pa45-volN.json` を作成
2. `data/meta/activities-index.json` を更新
3. git commit & push
4. WordPress PA45ランディングページ（ID:2228）の開催実績リストに今回の回を追加（post-event.py が自動実行）
5. **WordPressホームページ（ID:2069）の「参加する」ボタンを次回に更新**
   - テキスト：「第N回に参加する」→「第N+1回に参加する」
   - URL：`event/旧ID/` → `event/新ID/`
   - REST API経由で直接更新（pages/2069をPATCH）

connpassの参加者数は `scripts/fetch-connpass-participants.py <event_id>` で自動取得可能。
全自動は `scripts/post-event.py --vol N --event-id XXXXX --date YYYY-MM-DD --theme "テーマ名"` で実行。

---

## 過去回の情報

| 回 | 日付 | connpass event_id | テーマ | 参加者 |
|----|------|-------------------|--------|--------|
| 1 | 2026-03-06 | 386395 | 変数の初期化（Initialize variable） | 26人 |
| 2 | 2026-03-12 | 386742 | 変数を操作しよう（Set variable） | 32人 |
| 3 | 2026-03-26 | 387593 | 条件分岐（Condition） | 30人 |
| 4 | 2026-04-02 | 388691 | Apply to each | 29人 |
| 5 | 2026-04-09 | 389833 | 基礎固めWeek（第1〜4回を5回で完全定着） | 38人 |
| 6 | 2026-04-17 | 390451 | Formsの回答が来たら自動でお礼メールを送ろう | 37人 |
| 7 | 2026-04-23 | 391508 | Formsの申請をSharePointに自動登録して担当者に通知しよう | 26人 |
| 8 | 2026-04-30 | 391996 | 申請承認フロー（Approvals） | - |

---

## X投稿 自動化ワークフロー（2026-04-27設計）

### 基本方針
- **X APIは使わない。Chrome MCPでX.comを直接操作して予約投稿する。**
- GitHub Actionsでcronを組み、ClaudeがChrome経由でX.comの予約投稿UIを操作する。

### 毎回3本セットの投稿スケジュール
connpassにPA45イベントがある週は以下3本を自動予約：

| タイミング | 時刻（JST） | 内容 |
|-----------|------------|------|
| 開催週の月曜 | 12:15 | 今週開催のお知らせ |
| 開催当日（木曜） | 12:15 | 当日案内（本日開催！） |
| 開催当日（木曜） | 19:30 | 開催直前（あと45分！） |

### 投稿テンプレート

**① 月曜 12:15「今週開催のお知らせ」**
```
📢 今週木曜（M/D）PA45 第N回を開催します！

テーマ：{テーマ名}

Power Automateの{テーマ概要}を45分で作ります💡

🔰 初心者歓迎・無料・参加登録はこちら↓
https://powerautomate-create.connpass.com/event/{event_id}/

#PowerAutomate #PA45 #PowerPlatform
```

**② 木曜 12:15「当日案内」**
```
📢 本日開催！PA45 第N回

テーマ：{テーマ名}

今夜20:15〜 Power Automateの{テーマ概要}を45分で作ります💡

参加登録はこちら↓
https://powerautomate-create.connpass.com/event/{event_id}/

#PowerAutomate #PA45 #PowerPlatform
```

**③ 木曜 19:30「開催直前」**
```
⏰ あと45分で始まります！

PA45 第N回：{テーマ名}
本日 20:15〜 オンライン開催

よかったらぜひ↓
https://powerautomate-create.connpass.com/event/{event_id}/

#PowerAutomate #PA45 #PowerPlatform
```

### X投稿のルール（絶対に守ること）
- ハッシュタグは `#PowerAutomate #PA45 #PowerPlatform` の3つのみ
- `#自動化` `#ハンズオン` は使わない（上から目線に見える表現も禁止）
- 「まだ間に合います」は使わない → 「参加登録はこちら↓」「よかったらぜひ↓」に統一
- `document.execCommand('createLink')` はX.comでは使わない（@マーク化バグ）
  → `insertText` execCommandでplaintext URLを書けば自動リンクになる
- 予約投稿時刻はすべて日本時間（JST）

### Vol.8（2026-04-30）の予約投稿状況
| 投稿 | 状況 |
|------|------|
| 月曜 4/27 12:15「今週開催のお知らせ」 | ✅ 完了（2026-04-27設定済み） |
| 木曜 4/30 12:15「当日案内」 | ❌ 未設定 |
| 木曜 4/30 19:30「開催直前」 | ❌ 未設定 |

### 開催後のサイト自動更新（木曜 21:15 自動）
イベント終了後に以下を自動実行する仕組みを実装予定：

| 処理 | 方法 |
|------|------|
| connpassから参加者数を自動取得 | connpass API |
| `data/activities/` にJSONを自動生成 | post-event.py流用 |
| `activities-index.json` 更新 | 自動 |
| `index.html` の回数・参加者数を更新 | 自動 |
| `sessions/index.html` に新しい回を追加 | 自動 |
| git commit & push → GitHub Pages反映 | 自動 |

**手動のまま（自動化不可）：** YouTube動画アップロード、ブログ記事公開、アンケート結果（翌週以降に自動取得済み）

### 実装状況
- ❌ GitHub Actions（4本）未作成
- ❌ 開催後自動更新スクリプト未作成
- → **次の会話で実装を依頼する**

---

## X投稿スライド記事の状況（2026-04-07更新）

Vol.1〜30（Vol.11・Vol.27除く）の28件：**すべて公開済み**（ID 1294〜1348）

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
| `scripts/parse-survey.py` | SharePointからアンケートExcelを取得・集計・JSON出力 |
| `scripts/cross-post-qiita.py` | WordPressからQiitaへのクロスポスト |

---

## サイト構成（GitHub Pages）

- `slides/index.html`：X投稿スライド一覧。フィルター付き（CS・TEAMS・PJSON・COND・DATE・FILTER・ATE・EXP・DBG・VAR・SELECT）
- `assets/x/slides/`：cs_slide01〜30.png / pa_slide01〜21.png（全51枚）
- `data/activities/`：各活動のJSON（activities-index.jsonに登録必要）
- `data/meta/activities-index.json`：GitHub Pagesに反映するためのインデックス
- `assets/js/home-latest.js`：トップページの「最新の活動」をJSONから自動表示

---

## WordPress SEO 施策状況（2026-04-07実施済み）

### AIOSEO設定
- **meta description**: 全公開記事63件に一括設定済み（REST API経由）
- **著者スキーマ**: siteRepresents=person、personName=「はる（Haru）」に変更済み
- **SNSリンク**: X=`@isamu_Automate`、YouTube=`@Haru_PowerAutomate136` を設定済み
- **AIOSEO REST APIの使い方**:
  - GET: `/wp-json/aioseo/v1/post?postId={id}` → `response.post.description` で取得
  - POST: `/wp-json/aioseo/v1/post` with `{id: postId, description: '...'}` で更新
  - OPTIONS更新: GET current → modify `options` key → POST back full object
  - **注意**: CSRF cookie名は `connpass-csrftoken`（通常のcsrftokenではない）

### PA45 ランディングページ
- WordPress固定ページ ID:2228、URL: `https://www.automate136.com/pa45/`
- 狙いキーワード: Power Automate 勉強会 無料 / ハンズオン 初心者 / 45分
- FAQ5問・参加者の声・CTAボタン2箇所を含む

### PA45 内部リンクCTA
- cat:76（Power Automate Tips）・cat:77（コミュニティ）・cat:78（社内DX）の全記事末尾にCTA追加済み
- リンク先: `https://www.automate136.com/pa45/`

### 下書きスケジュール公開（2026-04-07設定）
- 46件を1日2本（10:00 / 18:00 JST）で自動公開設定済み
- 公開期間: 2026-04-08 〜 2026-04-30
- 各記事にmeta description・PA45 CTAも同時設定済み
- 除外: ID:2110（草案タイトル）・ID:2161（空タイトル）

### 未実施（手動が必要）
- Google Search Consoleにsitemap.xml送信
- AIOSEOとGSCのOAuth接続（接続後はClaude経由で順位確認可能）
- PA45ページのFAQ Schema設定（AIOSEO管理画面）

---

## 作業の流れ・決定事項

- **ブランチ戦略**: `main` に直接push（基本）
- **Claude Code設定**: `.claude/settings.json` に `allow: ["Bash","Read","Write","Edit","Glob","Grep"]` + `ask: ["Bash(git push:*)","Bash(git commit:*)"]` 設定済み → git push/commit のみ確認、それ以外は全自動承認。
- **git push が rejected されたとき**: `git pull --rebase origin main && git push origin main` で解決

---

## PA45スライド構成ルール（第4回以降）

P003で確立した標準構成。毎回この順番で作成する：

| # | 内容 | 備考 |
|---|------|------|
| 1 | PA45とは？（INTRODUCTION） | 固定 |
| 2 | ご参加にあたってのお願い | 固定 |
| 3 | 講師自己紹介（Haru） | 固定 |
| 4 | タイトルスライド（第N回：テーマ名） | 毎回更新。Theme/Target/Time |
| 5 | 今日やること（3つだけ） | 毎回更新 |
| 6 | テーマ解説（概念・演算子など） | 毎回更新。フォント16pt以上 |
| 7 | 10分ハンズオン4つのステップ | 毎回フロー内容に合わせて更新 |
| 8 | 今日のポイント3つ | 初心者が「受講して良かった」と思える内容 |
| 9 | 活用事例（実務での自動化） | 毎回テーマに合わせて更新 |
| 10 | うまくいかない時のチェックポイント | 毎回テーマに合わせて更新 |
| 11 | アンケートへの誘導（Special Gift） | フッターに第N回を入れる |

**削除済みスライド（P003から廃止）：**
- 「Power Automateって何？」（第4回以降不要）
- 「ネクストセッション」（不要）
- 「今日の学び」（8番と重複）

**スタイルルール：**
- フォント最小16pt（例外なし）
- Flow Imageプレースホルダーは使わない → テキストで条件を記述
- スライド9の活用事例カードは「条件ラベル（≥ 5件？など）」＋「フロー説明文」で構成

---

## 視覚確認ツール（スライドQA）

インストール済み：
- LibreOffice: `C:\Program Files\LibreOffice\program\soffice.exe`
- Poppler (pdftoppm): `C:\Temp\poppler\poppler-24.08.0\Library\bin\pdftoppm.exe`

**スライドを画像変換する手順：**
```bash
cp "assets/pa45/PXXX.pptx" "C:\Temp\test.pptx"
"C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to pdf "C:\Temp\test.pptx" --outdir "C:\Temp"
rm -f /c/Temp/slides/slide-*.jpg
"/c/Temp/poppler/poppler-24.08.0/Library/bin/pdftoppm.exe" -jpeg -r 120 "C:\Temp\test.pdf" "C:\Temp\slides\slide"
```
※ファイルパスに日本語があるとLibreOfficeがエラーになるため、C:\Tempにコピーしてから変換する

---

## MVP戦略

目標：Microsoft MVP（Power Platform カテゴリ）取得

**作戦①：YouTube仕組み化（最優先）**
- PA45の各回終了後にYouTube動画を公開する仕組みを構築中
- `scripts/youtube-release.py <vol> <YouTube URL>` を作成予定
  - YouTube用タイトル・説明文を自動生成
  - `data/activities/vol-N.json` に youtube フィールドを追記
  - `sessions/index.html` に YouTubeボタンを追加
  - git commit & push まで完了

**作戦②：ブログ週2-3本公開**
- 28記事が下書き済み。ユーザーが確認・編集してから手動公開

**作戦③：数字で実績を可視化**
- PA45参加者数・理解度スコアをサイトに自動表示（実装済み）

**重要：自動化はスケジュール・配信のみOK。コンテンツは必ずユーザーが確認してから公開。**

---

## バッジ自動送信ワークフロー

### 仕組み
Formsのアンケート回答者に参加バッジ＋お礼メール＋次回connpass URLを自動送信する。

### 使い方（Claudeへの指示）
「第4回のバッジ送って」と言われたら、Claudeは以下の3ステップで進める。**ユーザー確認なしに本番送信しない。**

```
STEP 1: 日付一覧を確認（送信しない）
  python scripts/send-badges.py --session 4 --scan
  → 出力を見てユーザーに「どの日付の回答に送りますか？」と聞く

STEP 2: 送信予定リストを確認（送信しない）
  python scripts/send-badges.py --session 4 --date 2026-04-02 --dry-run
  → 宛先一覧を見てユーザーに「この宛先でよいですか？」と聞く

STEP 3: ユーザーのOKが出た後のみ本番送信
  python scripts/send-badges.py --session 4 --date 2026-04-02
```

### 安全装置（必ず通過）
**以下の条件を満たさない限り、メールは1件も送信しない：**
- `assets/badges/session-XXX/badge.png` が存在すること（バッジ未配置なら即終了）
- `--date` が明示されていること（未指定なら即終了・誤送信防止）
- `data/badge-sent/session-XXX.json` で重複送信チェック（送信済みアドレスには送らない）
- **Claudeはユーザーのチャット確認なしに --dry-run なしのコマンドを実行しない**

### バッジ画像配置ルール
- ユーザーがClaudeにバッジ画像を渡す
- Claudeが `assets/badges/session-XXX/badge.png` に保存してコミット
- **画像が配置・コミットされるまでスクリプトは実行しない**

### 毎回の更新箇所（.env）
- `NEXT_CONNPASS_URL` → 次回のconnpass URL（開催前に更新）
- `BADGE_FORMS_FILE_ID` → FormsのExcel（OneDrive）のファイルID（初回設定後は変更不要）

### アンケートExcelの構造（確認済み）
- ファイルID: `47E8E22E-7B13-4D0C-9181-31D6B9BF9150`（parse-survey.pyと同じ）
- オーナー: `ixa_mct@plug136.onmicrosoft.com`
- 全回のアンケートが1ファイルに蓄積される（同じFormsリンクを毎回使用）
- 列1「開始時刻」= タイムスタンプ（例: `2026-03-26 21:00:51`）← 日付フィルターに使用
- 列3「メール」= 常に「匿名」（Formsの自動フィールド、メアドは取れない）
- 列23 = Xアカウント名（現在のバッジ配布列）
- **バッジ用メールアドレス列はまだない** → 下記セットアップが必要

### 残りのセットアップ（1回だけ）
1. **Formsにメールアドレス質問を追加する**
   - 質問文例: 「メールアドレスを入力してください（バッジ配布用・任意）」
   - 種類: テキスト入力
   - 追加後、Excelに新しい列が自動で増える
2. **Outlookアプリパスワードを発行** → `.env` の `SMTP_USER` / `SMTP_PASSWORD` に設定する
3. **`NEXT_CONNPASS_URL`** を `.env` に設定する（開催前に毎回更新）

---

## アンケート自動化ワークフロー

### 完全自動（GitHub Actions）
毎週金曜にGitHub Actionsが自動実行：
- Microsoft Graph APIでSharePointのExcelをダウンロード
- 日付でVol別に分割して `data/surveys/vol-XX.json` を自動生成・更新
- git commit & push まで自動

**SharePoint設定（変更不要）：**
- ファイルオーナー: `ixa_mct@plug136.onmicrosoft.com`
- ファイルID: `47E8E22E-7B13-4D0C-9181-31D6B9BF9150`
- Azure App: `PA45-survey-reader`（GitHub SecretsにMS_CLIENT_ID・MS_TENANT_ID・MS_CLIENT_SECRET登録済み）

### survey JSONの必須フィールド
```json
{
  "vol": 1,
  "date": "2026-03-05",
  "total_responses": 17,
  "understanding_pct": 82.4,
  "usefulness_pct": 88.2,
  "understanding": {...},
  "usefulness": {...},
  "time_preference": {...},
  "can_do": {...},
  "comments": [...]
}
```

- `sessions/index.html` はJSで `data/surveys/vol-{N}.json` を自動読み込み（HTMLの変更不要）
- カードに「理解度・役立ち度・コメント1件」が自動表示される
- テスト回答（5件未満の日付）は自動除外

---

## YouTube動画ワークフロー（PA45開催後）

PA45の各回が終わったら以下の手順でYouTube動画を公開する：

### 動画編集（ffmpegで実施）
- Teamsの録画はPowerShellのffmpegで編集する
- **クロップコマンド（白いスライドエリアのみ切り抜き）**
  - 解像度1920×1080の場合：`crop=1133:719:125:49`
  - 最初N分削除・終了時刻指定の場合：`-ss 00:11:00 -to 01:11:00`
- 出力ファイル名：`P00N-PA45.mp4`（例：P001-PA45.mp4）

```powershell
ffmpeg -ss 00:11:00 -to 01:11:00 -i "元ファイル.mp4" -vf "crop=1133:719:125:49" "P001-PA45.mp4"
```

### YouTubeアップロード（手動）
- YouTube Studioのファイル選択は手動操作（Claudeはiframeの制約でアップロードできない）
- ユーザーが「アップロードした」「続きをお願い」と言ったら、ClaudeはChrome MCP（mcp__Claude_in_Chrome）を使ってYouTube Studioを自動操作する

### YouTube Studio 自動操作手順（Chrome MCP使用）
1. YouTube Studio動画一覧（https://studio.youtube.com/channel/UCjRBVwQ33_mqT6II1BvHriA/videos）を開く
2. 最新のドラフト動画を探し、「ドラフトを編集」ボタンをクリックしてvideo IDを取得（URLの `udvid=XXXXXXXXXXX` から取得）
3. `/video/{ID}/edit` に移動
4. JavaScriptでタイトル・説明文を設定して保存
   - タイトル形式：`Power Automate 45 第N回 – {テーマ}を45分で体験しよう！`
   - 説明文：PA45概要・公式サイトURL・connpass URL・ブログURL・ハッシュタグ
5. **公開操作のみユーザーに依頼**（誤公開防止）
6. ユーザーが公開完了を伝えたら後続処理を実行

### YouTube SEO設定（公開後にClaude MCP自動実施）

**タグ設定（12個固定）**
```
PowerAutomate, PA45, PowerPlatform, Microsoft365, 自動化, ハンズオン, 初心者向け, 変数, 条件分岐, 繰り返し処理, ローコード, RPA
```
- JS注入パターン：
  1. `inputs.find(el => el.getAttribute('aria-label') === 'タグ')` で input 取得
  2. `input.value = tag; input.dispatchEvent(new KeyboardEvent('keydown', {key:'Enter', keyCode:13, bubbles:true}))` で追加

**言語設定**
- 動画の言語：日本語（「すべて表示」→「動画の言語」ドロップダウン → `find("日本語 option")` → click）
- タイトルと説明の言語：日本語（同様の手順）

**サムネイル（カスタムサムネイル）**
- CSPにより Claude から直接ファイルアップロード不可（"Not allowed"）
- 手順：
  1. `python scripts/make-ogp.py --title "第N回\nテーマ名" --label "PA45 第N回" --sub "Power Automate ハンズオン" --theme orange --out assets/ogp/pa45-volN-thumb.png`
  2. `cp assets/ogp/pa45-volN-thumb.png C:/Temp/pa45-volN-thumb.png`
  3. ユーザーに手動アップロードを依頼：「カスタムサムネイル」→ C:/Temp/pa45-volN-thumb.png を選択 → 保存

### アップロード後の自動処理（Claudeが実施）
1. `data/activities/YYYY-MM-DD-pa45-volN.json` の `evidence.youtube` にURLを追記
2. `sessions/index.html` の該当回カードに「▶ YouTube動画を見る →」ボタンを追加
3. WordPress に該当回の session report 下書き投稿を作成（カテゴリID:77）
4. CLAUDE.md のYouTube動画URL記録テーブルを更新
5. git commit & push

### YouTube動画URL記録
| 回 | YouTube URL |
|----|-------------|
| 1 | https://youtu.be/GEB2zGcmF88 |
| 4 | https://youtu.be/RzHylaoTRrs |
| 5 | https://youtu.be/cltHw91fYm4 |
| 6 | https://youtu.be/rvSX575fdbo |
| 7 | https://youtu.be/JOOlaiBvYgQ |

※ Vol.2・3 は録画データなし（公開不可）。対応不要。

---

## Qiitaクロスポスト

- **APIトークン**: `.env` に `QIITA_TOKEN` として保存済み（GitHub Secretsにも登録済み）
- **スクリプト**: `scripts/cross-post-qiita.py`
- **投稿ペース**: 火・木・土（GitHub Actions `daily-qiita-post.yml`）
- **canonical URLの代わり**: 記事冒頭に「元記事：https://www.automate136.com/...」を自動挿入
- **現状**: Vol.1投稿済み（https://qiita.com/Haru_PowerAutomate136）。Vol.2以降は火・木・土に自動投稿。
- **Zenn**: 未連携（後回し）
- **WordPress記事・Qiita記事**: ユーザーが内容を確認・編集してから手動で公開する（自動公開は絶対にしない）。「公開しなくていい」と明示的に指示済み。
- **Qiitaスコープ**: `write_qiita`（read_qiitaは任意）

---

## 重要な注意事項

- `.env` ファイル（WordPress認証）は gitignore 済み。絶対にコミットしない
- connpass のイベント説明・参加者への情報は毎回前回をコピーして回数を変更
- TeamsミーティングURLは毎回同じものを使い回す
- `data/activities/` のJSONが activities-index.json に登録されないと GitHub Pages に反映されない
- GitHub Actions の `rebuild-activities-index.yml` が push のたびに自動でindex再生成する（`_`始まり・`index.json`は除外）

## 📋 PA45プロジェクト 引き継ぎコンテキスト（2026-03-30時点）

---

### 🙋 プロジェクト概要

- **オーナー**: はる（ism136）
- **サイト**: https://www.automate136.com（WordPress / Cocoonテーマ）
- **GitHubリポジトリ**: https://github.com/Haru-PowerPlatform/pa45
  - ローカルパス: `C:\Users\isamu\OneDrive\ドキュメント\GitHub\pa45`
- **GitHub Pages**: https://haru-powerplatform.github.io/pa45/
- **目標**: Microsoft MVP（Power Platform枠）取得

---

### ✅ 直前の会話で完了した作業

**モバイル表示修正（WPCode Lite スニペット）**
- CSS スニペット ID: 2087
- JS スニペット ID: 2086（カテゴリページ専用 hero/CTA）

解決済みの問題：
- ✅ モバイルでナビ2重表示 → @media (min-width:835px) 内にPC navスタイルを移動
- ✅ モバイル上部の白い空白 → .home #header { display:none !important } + min-height:0
- ✅ モバイルナビ消滅 → .menu-top.menu-mobile を flex で直接表示
- ✅ PCナビ色分け・hover正常維持

最終CSSの核心部分（@media (max-width:834px) 内）:

.home #header { display: none !important; }
body #navi ul.menu-top.menu-pc,
body #navi ul.menu-top.menu-header.menu-pc {
  display: none !important; height: 0 !important;
  position: absolute !important; pointer-events: none !important;
}
body #navi ul.menu-top.menu-mobile {
  display: flex !important; flex-wrap: wrap;
}
.home #content { margin-top: 0 !important; }
.home #navi { min-height: 0 !important; }

---

### 🎯 次にやること（最優先）

#### 1. 活動実績グラフ可視化ページの作成

**決定事項：**
- 実装方式: 静的HTML（案B）— GitHub Pages上に置き、JSONを直接fetch
- データ: https://raw.githubusercontent.com/Haru-PowerPlatform/pa45/main/data/ から取得
- 公開対象: 一般公開 + MVP審査官向け
- 内容（全部乗せ）:
  1. KPIカード — 累計活動数・PA45参加者累計・投稿数・活動期間
  2. 月別活動数 折れ線グラフ（継続性の証明）
  3. PA45参加者数 + 満足度推移（棒グラフ+折れ線の複合）
  4. 活動タイプ別ドーナツチャート（PA45/X/Blog/Event の多様性）
  5. タイムライン（全活動ログ一覧）
- ライブラリ: Chart.js（CDN）
- 配置先: achievements/index.html（既存ディレクトリ）

**現在あるデータ（data/ 配下）:**

data/activities/
  2026-03-06-pa45-vol1.json       // PA45, 参加者26人
  2026-03-12-pa45-vol2.json       // PA45, 参加者32人
  2026-03-19-ippo-fumidasete-tv-ep25.json  // Event（登壇）
  2026-03-21-x-compose-debug.json // X投稿
  2026-03-22-x-last-bizday.json   // X投稿
  2026-03-26-pa45-vol3.json       // PA45, 参加者30人

data/meta/activities-index.json   // 全JSONへのパス配列

data/surveys/
  vol-01.json〜vol-03.json        // 理解度・満足度スコア

活動JSONの形式例:
{
  "id": "2026-03-06-pa45-vol1",
  "type": "PA45",
  "title": "PA45 第1回：変数の初期化",
  "date": "2026-03-06",
  "participants": 26,
  "evidence": { "blog": "...", "slide": "...", "connpass": "..." }
}

---

### 📊 PA45 開催実績

| 回 | 日付       | テーマ             | 参加者 | connpass event_id |
|----|------------|--------------------|--------|-------------------|
| 1  | 2026-03-06 | 変数の初期化       | 26人   | 386395            |
| 2  | 2026-03-12 | Set variable       | 32人   | 386742            |
| 3  | 2026-03-26 | 条件分岐           | 30人   | 387593            |
| 4  | 2026-04-02 | Apply to each      | 29人   | 388691            |
| 5  | 2026-04-09 | 基礎固めWeek（第1〜4回を5回で完全定着） | 38人 | 389833 |

---

### 📝 WordPress状況

- カテゴリ: ID76（Power Automate Tips）/ ID77（コミュニティ運営）/ ID78（社内DX）
- X投稿スライド記事: Vol.1〜30（Vol.11・27除く）28件が下書き状態（投稿ID 1294〜1348）
- 自動公開は絶対しない。ユーザーが確認してから手動公開。
- ClaudeはWordPress REST API（/wp-json/wp/v2/）に直接アクセスできる
- WP_USER: ism136 / WP_URL: https://www.automate136.com（認証は .env 参照）

---

### 🔧 Claude への行動ルール

1. 指示はCLAUDE.mdに自動保存（「保存して」と言わなくてよい）
2. 確認は最小限。作業後に1回だけ報告
3. git push/commit のみ確認、それ以外は全自動
4. rejected時: git pull --rebase origin main && git push origin main
5. ブログ記事に「MVP」関連の文言は絶対に書かない
6. 文体: 温かみ・読者に語りかける口調。冒頭は淡々と本題へ

---

### 📁 重要ファイルパス

| 用途 | パス |
|------|------|
| プロジェクト永続コンテキスト | C:\Users\isamu\OneDrive\ドキュメント\GitHub\pa45\CLAUDE.md |
| 活動記録インデックス | data/meta/activities-index.json |
| アンケートデータ | data/surveys/vol-XX.json |
| CSSスニペット管理 | WPCode Lite > ID 2087 |
| JSスニペット管理 | WPCode Lite > ID 2086 |
これが会話の初めに指示した前提

---

## biz-english-ai.com アフィリエイトブログ

**完全別プロジェクト。PA45とは独立して運用。**

### WordPress認証
- URL: https://biz-english-ai.com
- USER: phi93399
- APP PASSWORD: lWvX knO4 IGL5 7gW1 nms1 G7fg
- REST API: `POST /wp-json/wp/v2/posts/{id}` で記事更新

### 記事スタイルの絶対ルール
1. **インラインスタイルのみ**（CSSクラス禁止。WordPressのwpautopがフレックス等を破壊するため）
2. **吹き出し（バルーン）なし**（アイコン品質が低いため廃止）
3. **ユーザー口コミOK**（ネットから収集した実際の口コミ・レビューを引用形式で入れる。架空の体験談は書かない）
4. **段落前に必ず空行**（`\n\n<p>...</p>` 形式）
5. 各HTML要素は1行で完結させる（改行でwpautopに干渉させない）

### 記事生成用ヘルパー関数（毎回再利用）
```python
P  = lambda t: f"\n\n<p>{t}</p>"
H2 = lambda t: f"\n\n<h2>{t}</h2>"
H3 = lambda t: f"\n\n<h3>{t}</h3>"
UL = lambda items: "\n\n<ul>" + "".join(f"\n<li>{i}</li>" for i in items) + "\n</ul>"
def box_yellow(html): return f'\n\n<div style="background:#fffbeb;border-left:5px solid #f59e0b;padding:16px 20px;margin:24px 0;border-radius:8px;font-size:15px;line-height:1.8;">{html}</div>'
def box_blue(html): return f'\n\n<div style="background:#eff6ff;border-left:5px solid #3b82f6;padding:16px 20px;margin:24px 0;border-radius:8px;font-size:15px;line-height:1.8;">{html}</div>'
def box_green(title, items):
    li = "".join(f"<li style='margin:8px 0;font-size:14px;'>{i}</li>" for i in items)
    return f'\n\n<div style="background:#f0fdf4;border:2px solid #86efac;border-radius:12px;padding:20px 24px;margin:16px 0;"><p style="font-weight:700;font-size:15px;margin:0 0 12px;">✅ {title}</p><ul style="margin:0;padding-left:20px;">{li}</ul></div>'
def box_red(title, items):
    li = "".join(f"<li style='margin:8px 0;font-size:14px;'>{i}</li>" for i in items)
    return f'\n\n<div style="background:#fff1f2;border:2px solid #fda4af;border-radius:12px;padding:20px 24px;margin:16px 0;"><p style="font-weight:700;font-size:15px;margin:0 0 12px;">❌ {title}</p><ul style="margin:0;padding-left:20px;">{li}</ul></div>'
def cta(label, url, sub=""):
    s = f'<p style="margin:10px 0 0;font-size:13px;color:#64748b;">{sub}</p>' if sub else ""
    return f'\n\n<div style="text-align:center;margin:36px 0;"><a href="{url}" style="display:inline-block;background:linear-gradient(135deg,#3b82f6,#8b5cf6);color:#fff;text-decoration:none;padding:16px 36px;border-radius:50px;font-size:16px;font-weight:700;box-shadow:0 4px 14px rgba(59,130,246,.4);" target="_blank">{label}</a>{s}</div>'
def compare_table(headers, rows):
    ths = "".join(f'<th style="background:linear-gradient(135deg,#3b82f6,#6366f1);color:#fff;padding:12px 14px;text-align:left;font-size:14px;">{h}</th>' for h in headers)
    trs = ""
    for i, row in enumerate(rows):
        bg = "background:#f8faff;" if i%2==1 else ""
        tds = "".join(f'<td style="padding:10px 14px;font-size:14px;border-bottom:1px solid #e2e8f0;{bg}">{c}</td>' for c in row)
        trs += f"<tr>{tds}</tr>"
    return f'\n\n<table style="width:100%;border-collapse:collapse;margin:24px 0;font-size:14px;"><thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table>'
```

### 現在の記事一覧（10記事・全記事 publish 済み）

| Post ID | ラベル | タイトル | スラッグ | 投稿日 |
|---------|--------|---------|---------|--------|
| 7  | COMPARE | AIビジネス英会話アプリ おすすめ5選 | ai-business-english-apps-recommended | 2026-04-16 |
| 10 | REVIEW  | ELSA Speak 評判・料金・効果 | elsa-speak-review | 2026-04-12 |
| 11 | REVIEW  | スタサプENGLISH ビジネス版 | studysapuri-english-business-review | 2026-04-11 |
| 12 | GUIDE   | AIアプリで英語は話せるようになる？ | ai-english-app-effectiveness | 2026-04-08 |
| 13 | REVIEW  | Speak 評判・料金レビュー | speak-app-review | 2026-04-05 |
| 14 | TIPS    | ビジネス英語メールをAIで書く方法 | business-english-email-ai-template | 2026-03-27 |
| 59 | GUIDE   | 無料AI英会話アプリまとめ | free-ai-english-conversation-app | 2026-03-26 |
| 60 | GUIDE   | 英語の発音矯正 完全ガイド | english-pronunciation-correction-guide | 2026-03-23 |
| 61 | TIPS    | ビジネス英語フレーズ集 会議・プレゼン | business-english-phrases-meeting-presentation | 2026-03-22 |
| 62 | TIPS    | 英語学習が続かない理由と対策 | english-study-continue-tips-ai-app | 2026-03-19 |

記事一覧ページ: https://biz-english-ai.com/articles/ （Page ID=87）

### 実装済み機能（2026-04-18）
- **全記事モバイルリライト済み**：p/h2/h3/ul/hl/box/cta/compare_tableヘルパー使用。段落margin:2em、line-height:2.0
- **蛍光ペンアニメーション**：`.hl`クラス + IntersectionObserver でスクロール時に左→右アニメーション
- **SNS非表示CSS**：全記事の`<style>`ブロックに `.sns-share,.author-box`等を`display:none`で組み込み
- **関連記事カルーセル**：各記事末尾に `<!-- related-posts -->` マーカー付きの横スクロールカード
- **記事一覧ページ**：/articles/ にカテゴリ別リスト（Page ID=87）

### アイキャッチ画像のデザインルール
- テンプレート：白背景・グレー枠・バインダークリップ（左上）・ラベル「[ REVIEW ]」＋横線・大見出し・太線区切り・サブテキスト
- サイズ：1280×670px
- **カテゴリ別グラデーション枠（14px）**：
  - COMPARE → インディゴ(99,102,241)→パープル(139,92,246)
  - REVIEW  → ブルー(59,130,246)→シアン(6,182,212)
  - GUIDE   → グリーン(16,185,129)→ティール(5,150,105)
  - TIPS    → アンバー(245,158,11)→オレンジ(249,115,22)
- 生成スクリプト：`C:\Temp\eyecatch_border_preview.py` / `C:\Temp\apply_all_borders_and_dates.py`

### サイドバー（2026-04-18構成）
- WordPress widget: `text-2`（sidebar）のみ使用
- 構成：①自己紹介（Hana / AI英語学習アドバイザー） → ②アフィリエイトランキングTOP3 → ③カテゴリー
- プロフィール画像URL: `https://biz-english-ai.com/wp-content/uploads/2026/04/sidebar_profile.png`
- アフィリエイトリンク（現在は直リンク・ASP登録後に差し替え予定）：
  - ELSA Speak: https://elsaspeak.com/ja/
  - Speak: https://www.speak.com/ja
  - スタサプENGLISH: https://eigosapuri.jp/

### アフィリエイト登録状況（2026-04-18）
- もしもアフィリエイト: 仮登録完了（本登録はブログ5記事後）
- **A8.net: 未登録 → 今すぐ申請可能（記事10本公開済み）**
- **afb: 未登録 → スタサプENGLISH案件あり**
- リンク差し替えはスクリプトで一括対応予定

### Python作業スクリプト（C:\Temp\）
| ファイル | 用途 |
|---------|------|
| rewrite_post7_mobile.py | 記事7モバイルリライトテンプレート |
| rewrite_post13_mobile.py | 記事13（蛍光ペン+口コミ削除） |
| rewrite_all_mobile.py | 残り8記事一括リライト+publish |
| add_related_posts.py | 関連記事カルーセル全記事追加 |
| hide_sns_all_posts.py | SNS非表示CSS全記事追加 |
| create_index_page.py | 記事一覧ページ生成 |
| rebuild_sidebar.py | サイドバーウィジェット再構築 |
| apply_all_borders_and_dates.py | アイキャッチ枠追加+投稿日ランダム設定 |

### SEO方針
- 長尾キーワード狙い（検索ボリューム小・競合弱）
- ユーザー口コミ（ネット収集）を引用形式で入れてE-E-A-T強化
- 内部リンクは全記事間でクモの巣状に接続
- アフィリエイトリンク先：ELSA Speak・Speak・スタサプENGLISH・ChatGPT

