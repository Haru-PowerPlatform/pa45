# Haru ブログ 文体・スタイルガイド
参照記事: https://www.automate136.com/powerautomate45001/

---

## 文体の特徴

### トーン
- 親しみやすい口語体。「～です」「～ます」ベースだが堅くない
- 自分の体験・感情を素直に書く（「ホッとしております」「本当に嬉しかった」）
- ユーモアを添える（「Teams入室 → 自分ひとり → 独り言を45分続ける　という地獄を避けられてホッとしております。」）
- 読者への語りかけ口調（「気持ちは大変よく分かります。。」）
- AIっぽい「まとめると〜」「以上のように〜」は絶対使わない

### 文章スタイル
- 短い文を改行で区切る（1文1行が多い）
- 矢印（↓）で次の説明につなぐ（「そもそもの部分から少しご説明を↓」）
- 「"〇〇"」「"とりあえず触ってみる"」と二重引用符で強調
- 体言止めで簡潔に（「聞くだけ参加もOK」）
- 「。。」など感情表現をそのまま残す
- 箇条書きは簡潔に・体言止めで

### やらないこと
- 「本記事では〜を解説します」のような硬い導入
- 「〜と言えるでしょう」「〜が重要です」の締め
- 見出しに絵文字を入れない（記事内では使わない）
- 「まとめ」セクションを最後に作らない（自然に終わる）
- 「ぜひ〜してみてください」の常套句

---

## HTML構造

### 吹き出し（左：Haru が話す）
```html
<div class="speech-wrap sb-id-14 sbs-stn sbp-l sbis-cb cf">
  <div class="speech-person">
    <figure class="speech-icon">
      <img loading="lazy" decoding="async" class="speech-icon-image"
           src="https://www.automate136.com/wp-content/uploads/2025/07/u9429395585_side_profile_portrait_of_a_man_in_his_30s_with_me_e4cca787-50fc-42ba-8f64-d0185bce97e5_1.png"
           alt="" width="1024" height="1024" />
    </figure>
  </div>
  <div class="speech-balloon">
    <p>ここに吹き出しのテキスト</p>
  </div>
</div>
```

### 吹き出し（右：読者・相手が話す）
```html
<div class="speech-wrap sb-id-14 sbs-stn sbp-r sbis-cb cf">
  <div class="speech-person">
    <figure class="speech-icon">
      <img loading="lazy" decoding="async" class="speech-icon-image"
           src="https://www.automate136.com/wp-content/uploads/2025/07/u9429395585_side_profile_portrait_of_a_man_in_his_30s_with_me_e4cca787-50fc-42ba-8f64-d0185bce97e5_1.png"
           alt="" width="1024" height="1024" />
    </figure>
  </div>
  <div class="speech-balloon">
    <p>ここに吹き出しのテキスト</p>
  </div>
</div>
```

### 強調
```html
<strong>太字で強調</strong>
<span style="color: #ff0000;">赤字で強調</span>
<span style="color: #0000ff;">青字で強調</span>
<span style="font-size: 24px;"><strong>大きくして強調</strong></span>
```

### 引用（アンケートの声など）
```html
<blockquote>
  <p><strong>「〇〇〇」</strong></p>
</blockquote>
```

### 空白行
```html
<p>&nbsp;</p>
```

---

## カテゴリ → アイキャッチテーマ対応表

| カテゴリ          | --theme  | --label               | --sub               |
|------------------|----------|-----------------------|---------------------|
| Power Automate Tips | blue   | Power Automate Tips   | 実務で使えるフロー    |
| PA45 レポート     | orange   | PA45 開催レポート      | Power Automate 45   |
| Microsoft 365 活用 | green  | 業務効率化Tips         | Microsoft 365 活用   |
| 登壇・イベント    | red      | 登壇レポート           | 社外コミュニティ活動  |
| その他            | yellow   | Tips                  | automate136.com     |

---

## 毎回の投稿フロー（new-post.py）

```bash
python scripts/new-post.py \
  --title  "記事タイトル" \
  --body   "本文HTML" \
  --label  "pill上段" \
  --sub    "pill下段" \
  --theme  "blue" \
  --ogp    "アイキャッチ用タイトル\n2行目\n3行目" \
  --slug   "english-url-slug"
```

---

## PA45 スライド自動化フロー

### 講座前：スライド生成（pa45-gen.py）

```bash
python scripts/pa45-gen.py \
  --vol        2 \
  --title-ja   "変数を操作しよう" \
  --title-en   "Set variable" \
  --date       "2026-04-16" \
  --next-vol   3 \
  --next-title-ja "条件分岐を使おう" \
  --next-title-en "Condition" \
  --next-desc  "フローに「もし〜なら」の分岐を追加します。" \
  --template   "C:/Users/isamu/Downloads/.../P001_PA45_*.pptx"
```

自動で更新されるもの:
- `第N回` ラベル（全スライド）
- `Vol.N` 番号（タイトルスライド・次回予告）
- 英語タイトル行（Slide 5）
- 次回テーマ・説明・Vol番号（Slide 15）

### 講座後：公開フロー（pa45-publish.py）

```bash
python scripts/pa45-publish.py \
  --pptx     "outputs/pa45/P002_PA45_変数を操作しよう_20260416.pptx" \
  --vol      2 \
  --title-ja "変数を操作しよう" \
  --title-en "Set variable" \
  --date     "2026-04-16" \
  --publish
```

自動実行される処理:
1. PPTXを各スライドPNGに変換（win32com / LibreOffice）
2. スライド画像をWordPressにアップロード
3. OGPアイキャッチ（オレンジテーマ）生成・アップロード
4. スライド埋め込みブログ記事を作成
5. アイキャッチ・パーマリンク設定
6. PPTXをリポジトリ（assets/pa45/）にコピー
7. 活動データJSON（data/activities/）を追加
8. git commit & push → GitHub Pages 自動デプロイ

### スライドを手動でPNG変換した場合

```bash
python scripts/pa45-publish.py \
  --pptx     "outputs/pa45/P002_.pptx" \
  --vol      2 \
  --title-ja "変数を操作しよう" \
  --date     "2026-04-16" \
  --slides-dir "scripts/pa45-slides/vol002"  # slide_001.png ... を配置
```
