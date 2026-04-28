# 引き継ぎメモ — 2026-04-28 12:30

新しい会話セッションでこのファイルを読み込めば作業を続けられる引き継ぎドキュメント。

---

## 🏗 3サイト運営状況

| サイト | URL | 記事数 | ヘッダーメニュー | アフィリ稼働 |
|-------|-----|-------|----------------|-------------|
| side-invest.com | 副業×投資ログ | 22 | ✅ 5項目 | A8(MF・freee・Misoca・弥生) |
| biz-english-ai.com | AI英会話レビュー | 38 | ✅ 5項目 | 申請中 (A8/afb) |
| ai-gyomu.jp | AI業務効率化 | 35 | ✅ 4項目 | A8(MF・freee・Misoca・弥生) |

---

## ✅ 2026-04-28 完了タスク

1. **3サイト 404内部リンク一斉修正** — ai-gyomu 7件・biz-english-ai 28件
2. **JSON-LD body内残存除去** — 94記事から `<script type="application/ld+json">` 削除（トップページ抜粋への文字漏れ解消）
3. **3サイト全95記事にナビゲーションカード追加** — 記事末尾に4枚グリッド
4. **WPヘッダーメニュー手動セットアップ** — 3サイトとも `menu-top menu-header menu-pc` 稼働
5. **記事冒頭の重複ナビカード撤去** — top-nav-card を全95記事から削除
6. **ダッシュボード更新（sites/index.html）** — ランクイン状況・月間検索数・クエリ組み合わせ併記
7. **ID:59「無料AI英会話」記事を11,402字に拡張＋5記事からインバウンドリンク** ← 順位92位を10位以内へ押し上げ施策

---

## 🔍 現在の検索ランクイン状況（GSC 2026-03-28〜04-25）

| 順位 | 記事 | クエリ組み合わせ | 月間検索数(推定) | 表示 | クリック |
|------|------|-----------------|----------------|------|---------|
| 2.0 | ai-gyomu.jp/transcope-how-to-use-blog/ | transcope＋aiライティング＋個人ブロガー | 10未満 | 1 | 0 |
| 92.0 | biz-english-ai.com/free-ai-english-conversation-app/ | ai＋英会話＋無料 | 2,400 | 4 | 0 |

**重点ターゲット**: 92位の biz-english-ai 記事を10位以内へ。本日11,402字に拡張済み・インバウンドリンク5本追加済み・modified date更新済み。次にGSCでインデックスリクエストを手動投入すべき。

---

## 🎯 次にやるべきタスク（優先順）

### 🔥 最優先（流入直結）
1. **GSCで ID:59 記事のインデックスリクエスト送信** — 本日大幅更新したのでクロール促す（手動）
2. **被リンク獲得** — Qiita/Zenn/note にレビュー記事を投稿して各サイトへ自然リンク（私が下書き作成可）

### 🟡 中優先（収益直結）
3. **A8.net 追加申請** — DMM英会話・スタサプENGLISH・ネイティブキャンプ
4. **DMM英会話A8 審査結果Gmail確認**

### 🟢 質改善
5. **FAQ Schema・HowTo Schema** を主要10記事のhead側に追加
6. **ロングテール記事追加** 各サイト3〜5本
7. **画像WebP化＋遅延読み込み**

### ❄️ 待ち
- もしもアフィリ再登録（2026-05-24以降）
- バリューコマース登録（2026-06-24以降）
- GHA 4本（Anthropic API残高入金後）

---

## 🔧 重要な認証情報（場所のみ・値はファイル参照）

- **WordPress (3サイト)**: `C:\Temp\other-projects\biz-english-ai\.env` と `C:\Temp\other-projects\side-invest\.env`
- **共通シークレット**: ANTHROPIC_API_KEY等は biz-english-ai/.env がマスター
- **GitHubアカウント**: `Haru-PowerPlatform` リポジトリへのアクセスは `isamu7pad-alt` で（`bizzemiai-jpg` は権限なし）

---

## 📝 運用ルール

- **PR画面手動操作は廃止** — ローカルで `git checkout main && git merge <branch> && git push origin main` を自動実行
- **指示は CLAUDE.md / memory/MEMORY.md に自動保存**
- **「OK」「マージして」で承認** → 後はClaudeが自動進行
- **ブログ・Qiita記事の自動公開は禁止** — ユーザー確認後のみ手動公開
- **MVP関連文言は記事に書かない**

---

## 📂 主要ファイル

| パス | 用途 |
|------|------|
| `sites/index.html` | 3サイト進捗ダッシュボード（noindex） |
| `data/activities/` | PA45活動JSON |
| `C:\Temp\boost_free_ai_english_article.py` | 本日実行した順位押し上げスクリプト（参考） |
| `C:\Temp\remove_top_nav_cards.py` | ナビカード撤去スクリプト |
| `CLAUDE.md` | プロジェクト永続コンテキスト |

---

## 🐛 既知の問題

- ai-gyomu.jp の `sync-articles` / `weekly-article-draft` ワークフロー失敗 → GHA要修正
- 一部記事の「筆者の経験」テンプレが汎用化されている → 34記事ユニーク化の大作業残

---

更新者: Claude × はる｜次回参照する場合は冒頭のセクションから順に読めば現状把握OK
