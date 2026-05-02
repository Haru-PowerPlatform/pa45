# ユーザー指示の集約（はる ism136）

このファイルは過去のClaudeとの会話で**はる**（ユーザー）が出した指示・好み・ルールをまとめた永続記録。
新しい会話セッションでもこの内容を尊重して動くこと。

> 📌 Claude へ：会話開始時にこのドキュメントを必ず確認すること。`CLAUDE.md` から本ドキュメントを参照する設計。

---

## 1. 作業スタイル（最重要・全プロジェクト共通）

### 許可確認は不要・最後まで一気通貫
- 「進めていい？」「やる？」と聞かない
- 決めたら最後まで実行→最後に1回だけ報告
- ユーザーから繰り返し明示（2026-04-30〜05-02に6回以上）：
  - 「常に許可するから最後までまわして」
  - 「毎回許可きかないで」
  - 「許可聞かないで　あらゆる作業で　最後に一回だけでいい」
  - 「常に許可でOK！」
  - 「何度も許可を聞くのやめて欲しい」
  - 「全部許可するからそのまますすめて毎回許可確認しないで」

### 例外（必ず事前確認）
- リポジトリ・データベース削除など完全に元に戻せない操作
- パスワード/認証情報を外部に送信
- 第三者にメッセージ本番送信（dry-run なし）

### Plan Mode に入った場合
- ExitPlanMode で1回だけ承認を取り、以降は連続実行

---

## 2. ファイル・パス表示

### Cドライブのファイル/フォルダパスはコードブロック表示
エクスプローラーのアドレスバーに貼り付けて開ける形式で書く：
```
C:\Users\isamu\Documents\pa45
```

`file:///` リンクは Claudeチャットで開けないので **使わない**。

---

## 3. デザイン変更しない（HTML・CSS）

ユーザー指示「HTMLのデザインは変えないでね」（2026-05-01）。
- CSS・class・レイアウト・フォント色サイズ・構造には触らない
- テキスト・URL・日付・数値の修正のみ

---

## 4. PA45 プロジェクト

### 概要
- Power Automate 45分ハンズオン勉強会
- ブログ: https://www.automate136.com
- GitHub: https://github.com/Haru-PowerPlatform/pa45
- ローカル: `C:\Users\isamu\Documents\pa45`

### 命名ルール（フロー作成時の推奨提示）
ユーザーが「PA45のフロー作りたい」「Vol.Nのフロー作る」等と言ったら、**最初に必ず推奨命名を提示**：

```
推奨命名:
- フロー名（マイフロー）: PA45-No{N}-{Topic}
- Solution 表示名: PA45 No.{N} {テーマ短縮}
- Solution 名前（入力）: PA45_No{N}_{Topic}
- Solution UniqueName（自動）: PA45No{N}{Topic}
- GitHub内ZIP（自動）: flows/vol-{NN}/PA45-Vol{NN}-{Topic}.zip
```

詳細：[`docs/PA45_NAMING.md`](PA45_NAMING.md)

### 自動化パイプライン
- `scripts/release-flow.bat [N|all]` — pac CLI でPAからエクスポート→サイト反映→push
- `scripts/check-naming.py` — 命名整合性検証
- `scripts/add-vol-card.py` — 新Volカード生成＋マッピング自動同期
- `scripts/import-flow-zip.py` — ZIP配置＋HTML更新

### 開催後処理（「第N回が終わった」発火）
- 確認なし自動実行：JSON生成・index更新・git push・WordPress更新
- 落とし穴：vol3.json重複の誤集計、自動ActionでNext Sessionが「準備中」止まり、survey JSONが未追跡だとアンケートカード空白

---

## 5. ブログ記事（PA45 / automate136.com）

### 文体
- 温かみ・読者に語りかける口調
- 冒頭は淡々と本題へ
- 難しい概念を「〇〇みたいなもの」と例えで説明
- セクション間に `&nbsp;`

### 絶対書かないこと
- **MVP（Microsoft Most Valuable Professional）審査・認定に関する文言は一切禁止**
- 「MVP審査で〇〇」「MVPを狙う」「MVP認定に有利」全てNG
- **架空の参加者反応・チャット欄実況・盛り上がり描写は禁止**（うそ混入NG）
  - 「参加者から『〜』という声」「チャット欄に『できました！』」「盛り上がりました」「明日から業務で使えそう」等NG
  - `<h2>当日の様子</h2>` セクション全体NG
  - 講師の語りかけ（「『できた！』を一緒に作りましょう」）はOK
  - 事実値（アンケート集計値など）はOK

### よく使うHTMLパターン
- 吹き出し: `<div class="speech-wrap sb-id-14 sbs-stn sbp-l sbis-cb cf">...</div>`
- 色強調: `<span style="color: #0000ff;"><strong>...</strong></span>`
- アバター: `https://www.automate136.com/wp-content/uploads/2026/04/haru-profile.png`

---

## 6. X投稿（PA45）

### ルール
- 時刻はすべて日本時間（JST）
- ハッシュタグは `#PowerAutomate #PA45 #PowerPlatform` の3つのみ
- `#自動化` `#ハンズオン` は使わない
- 「まだ間に合います」禁止 → 「参加登録はこちら↓」「よかったらぜひ↓」
- 予約投稿はChrome MCPでX.comを直接操作（X API は使わない）

### 毎回3本セット
- 月曜 12:15「今週開催のお知らせ」
- 木曜 12:15「当日案内」
- 木曜 19:30「開催直前」

---

## 7. PowerPoint（PA45スライド）

### 標準構成（P003以降・全11〜12枚）
1. PA45紹介
2. ご参加にあたってのお願い
3. 講師自己紹介
4. タイトル（Vol.N・テーマ）
5. 今日やること（3つだけ）
6. テーマ解説
7. 10分ハンズオン4ステップ
8. 今日のポイント3つ
9. 活用事例
10. うまくいかない時のチェック
11. アンケート誘導

### スタイル
- フォント最小16pt（例外なし）
- python-pptx で run.text 単位の置換（フォント情報維持）

---

## 8. WordPress（automate136.com）

### REST API直接アクセス可
`.env` に WP_USER / WP_PASS / WP_URL 設定済み。`/wp-json/wp/v2/` 経由で直接操作。

### カテゴリー
| ID | 名称 |
|---|---|
| 76 | Power Automate 実践・Tips |
| 77 | コミュニティ運営（PA45） |
| 78 | 社内DX推進・人材育成 |

- 既定: ID76
- 自動公開禁止 — 必ずユーザー確認後に手動公開

---

## 9. PL-300（Power BI Data Analyst）

ユーザーは PL-300 受験準備中。「PL-300の続き」等と言われたら：
1. `docs/pl300-START-HERE.md` を最初に読む
2. `docs/pl300-handoff.md` で進捗確認
3. `docs/pl300-mistakes.md` でミス傾向把握
4. START-HERE.md のスタイルで再開

---

## 10. Bitzemi（別プロジェクト）

PA45とは独立。3サイト運営：
- biz-english-ai.com（AI英会話レビュー）
- ai-gyomu.jp（AI業務効率化）
- side-invest.com（副業×投資）

GitHub: `bizzemiai-jpg`（PA45の `Haru-PowerPlatform` とは別アカウント）

### 記事スタイル
- インラインスタイルのみ（CSSクラス禁止・wpautop対策）
- ユーザー口コミOK（架空体験談禁止）
- 段落前に必ず空行（`\n\n<p>...</p>`）

---

## 11. C:\Temp の運用

ユーザー指示でカテゴリ別に整理（2026-05-02）：
```
C:\Temp\
├── pa45\          PA45資料・サムネ・サンプルExcel
├── wp-drafts\     WordPress下書き作成
├── seo-audit\     SEO監査
├── eyecatch-tools\ アイキャッチ生成
├── site-scripts\  ブログ整形スクリプト
├── html-work\     HTML作業
├── ai-gyomu\, side-invest\, other-projects\  既存プロジェクト
├── blog-html\, downloads\, evidence\, screenshots\, videos\, etc.
└── poppler\, __pycache__\
```

---

## 12. ツール・環境

### インストール済み
| ツール | パス |
|---|---|
| LibreOffice | `C:\Program Files\LibreOffice\program\soffice.exe` |
| Poppler (pdftoppm) | `C:\Temp\poppler\poppler-24.08.0\Library\bin\pdftoppm.exe` |
| Power Platform CLI (pac) | システムPATH（v2.6.4 以降） |
| Python (openpyxl, python-pptx, requests, dotenv) | システムPython |

### スライド画像変換手順
```bash
cp "assets/pa45/PXXX.pptx" "C:\Temp\test.pptx"
"C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to pdf "C:\Temp\test.pptx" --outdir "C:\Temp"
"/c/Temp/poppler/poppler-24.08.0/Library/bin/pdftoppm.exe" -jpeg -r 120 "C:\Temp\test.pdf" "C:\Temp\slides\slide"
```
※ ファイルパスに日本語があるとLibreOfficeがエラーになるため C:\Temp にコピーしてから変換

---

## 13. 重要な認証情報の場所（値は環境ファイル参照）

| 用途 | 場所 |
|---|---|
| WordPress (automate136.com) | `pa45/.env` |
| WordPress (biz-english-ai) | `C:\Temp\other-projects\biz-english-ai\.env` |
| WordPress (side-invest) | `C:\Temp\other-projects\side-invest\.env` |
| ANTHROPIC_API_KEY マスター | biz-english-ai/.env |
| GitHub アカウント | `Haru-PowerPlatform`（PA45）と `bizzemiai-jpg`（Bitzemi）|
| `Haru-PowerPlatform` リポへのpush | `isamu7pad-alt` でアクセス |

---

## 14. ブランチ運用

- `main` に直接push（基本）
- `git push` rejected時: `git pull --rebase origin main && git push origin main`
- `.claude/settings.json` で `Bash` 系全許可、`git push:*` `git commit:*` も allow に登録済み

---

## 15. 自動メモリ運用

`C:\Users\isamu\.claude\projects\C--Users-isamu-Documents\memory\` に `MEMORY.md` インデックス＋個別ファイルで保存。
- ユーザーから指示があれば即追記
- 「保存して」と言われなくても更新
- 既存メモリと重複しないこと

---

## 16. Edgeお気に入り（Profile 3 = ixa_mct@plug136）

### ⚠️ クラウド同期の罠
Microsoft アカウントの**クラウド同期**が ON だと、Bookmarksファイル直編集はEdge起動時に上書きされる。

### 整理する場合の手順
1. Edge設定 → プロファイル → 同期 → **「お気に入り」を OFF**
2. Edge完全終了（msedge.exe プロセスもなし）
3. `python C:/Temp/pa45/reorganize_bookmarks.py` でJSON書き換え
4. Edge起動 → ローカル構造で固定

### 8カテゴリの命名（設定済み）
```
📊 管理ダッシュボード   ← 私が作ったHTMLダッシュボード
🚀 PA45 運営           ← 内部・運営者専用
🌐 PA45 受講生向け     ← 公開・受講生も見る
🪟 M365 / Power Platform
✍️ Bizemi 3サイト
📘 PL-300 学習
🛠️ ツール・参考
👤 個人
```

### スクリプト場所
`C:\Temp\pa45\reorganize_bookmarks.py`（Profile 3 専用）
バックアップ：`C:\Users\isamu\AppData\Local\Microsoft\Edge\User Data\Profile 3\Bookmarks.bak`

### 他Profile
- Default = isamu.u@outlook.jp
- Profile 2 = Isamu136@1dwg4q.onmicrosoft.com
- Profile 3 = ixa_mct@plug136.onmicrosoft.com（PA45メイン作業）

---

## 17. このドキュメントの更新

ユーザーから新しい指示・好み・ルールが出たら、このドキュメントを更新して push する。
更新の判断基準：
- 「次もこうして」と明示された
- 「いつも〇〇」と暗示された
- 同じ修正を3回以上要求された
