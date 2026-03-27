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
| 3 | 2026-03-26 | 387593 | 条件分岐（Condition） | 30人 |
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

### 初回セットアップ（まだ未実施）
1. FormsにE-mailアドレス入力列を追加する
2. Forms → 「Excelで開く」でOneDriveにExcelをリンク保存する
3. そのExcelのファイルIDを `BADGE_FORMS_FILE_ID` に設定する
4. Outlookアプリパスワードを発行して `SMTP_USER` / `SMTP_PASSWORD` に設定する

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
- タイトル・説明欄はClaude が生成し、ユーザーがコピペ
- 公開設定は「公開」

### アップロード後の自動処理（Claudeが実施）
1. `data/activities/YYYY-MM-DD-pa45-volN.json` の `evidence.youtube` にURLを追記
2. `sessions/index.html` の該当回カードに「▶ YouTube動画を見る →」ボタンを追加
3. git commit & push

### YouTube動画URL記録
| 回 | YouTube URL |
|----|-------------|
| 1 | https://youtu.be/GEB2zGcmF88 |

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
