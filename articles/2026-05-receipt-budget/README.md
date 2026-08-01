# 家計簿レシート × Power Automate 記事プロジェクト

automate136.com 向け単発ブログ記事のメモ・成果物・運用記録。

## ステータス
- 状態: **WordPress 下書き（status=draft）**
- WordPress Post ID: **2423**
- 編集 URL: https://www.automate136.com/wp-admin/post.php?post=2423&action=edit
- プレビュー URL: https://www.automate136.com/?p=2423&preview=true
- 作成日: 2026-05-09
- 公開日: 未定（さら確認後に手動公開）
- カテゴリ: ID 76（Power Automate 実践・Tips）
- アイキャッチ: media ID 2422（[../assets/ogp/article-receipt-budget.png](../../assets/ogp/article-receipt-budget.png)）

## 企画意図（要点）

- **目的**: 「役立つ！この視点！」を中心軸にしたブログ単発記事
- **モチベ**: X（Twitter）でバズらせたい
- **形式**: ブログ記事のみ（PA45 講座テーマにはしない＝ありきたりになるため）
- **テーマの尖り**: 「家計簿、書いて終わってる問題」を Power Automate × AI Builder の OCR + テキスト生成で「見返す係」を自動化、という切り口
- **巷ゼロ度**: レシート OCR の技術記事は巷にあるが、「月末に AI が浪費パターンを 3 つ言ってくる」運用記事は前例ほぼなし
- **2 クラスタ重なり**: PA／業務効率化クラスタ × 家計クラスタ（PA 文脈外）の飛び火を狙う

## 重要な設計判断（記事に織り込み済み）

1. **OneDrive のフォルダを分ける**: 全写真同期だと家族写真にも Power Automate トリガーが発火し、AI Builder クレジットが秒で溶ける。`/Pictures/レシート` 専用フォルダ運用が必須
2. **iOS ショートカットで 1 タップ化**: 「ホーム画面アイコン → カメラ起動 → /Pictures/レシート 自動保存」までを iOS ショートカット 2 アクションで構成。続けるための要
3. **フローを 2 本に分ける**: ①〜③（撮影→Excel）と ④（月末通知）はトリガーが違う（イベント駆動 vs スケジュール）ので別フローにする
4. **店名・日付・合計だけに絞る**: 明細抽出は精度が揺れるので最初から狙わない
5. **読めなかったレシートの保険**: 金額が空だったら自分宛 Teams 通知の分岐
6. **コスト・プライバシー注記**: AI Builder クレジット消費・レシートの個人情報・OneDrive フォルダを共有しない設定、を本文末に正直に記載

## デモデータの扱い

- 「実データ 1 ヶ月運用」ではなく「**手元のレシート 5 枚で試運転**」前提で書いた
- 架空の具体額（例: 「カフェに月 1.2 万」）は **使っていない**（[feedback_pa45_blog_no_fabrication](../../../.claude/projects/C--Users-isamu-Documents/memory/feedback_pa45_blog_no_fabrication.md) と整合）
- 数字は「5 件中 3 件がついで買い」など、5 枚という小サンプルで実際に出る粒度に留めた
- 1 ヶ月運用後に追記版を出す余地あり

## ファイル構成

| ファイル | 用途 |
|---|---|
| README.md | このファイル（メモ・運用記録） |
| article.html | 記事本文（WordPress 投稿時の HTML、source of truth） |
| x-posts.md | X 投稿文 3 本（公開直後・翌日スレッド・1 週間後） |
| video-script.md | 30 秒 X 動画用テロップスクリプト |
| plan.md | 企画決定までの経緯（10 案 → レシート確定） |

## 公開後にやること

1. WordPress 手動レビュー → 公開（自動公開はしない＝CLAUDE.md ルール）
2. アイキャッチが反映されてるか確認
3. X 投稿 #1 を `scripts/post-scheduled-x.py` 等で予約
4. 翌日 X 投稿 #2（スレッド）
5. Qiita クロスポスト（`scripts/cross-post-qiita.py`）
6. 1 週間後の反応を見て #3 投稿（架空の声引用は禁止）

## 関連メモリ
- [feedback_blog_purpose](../../../.claude/projects/C--Users-isamu-Documents/memory/feedback_blog_purpose.md): automate136.com の記事は 活動実績の記録が主目的・SEO は二の次
- [feedback_pa45_blog_no_fabrication](../../../.claude/projects/C--Users-isamu-Documents/memory/feedback_pa45_blog_no_fabrication.md): 架空の体験談・盛り上げ描写は禁止
- [feedback_pa45_no_affiliate](../../../.claude/projects/C--Users-isamu-Documents/memory/feedback_pa45_no_affiliate.md): X 投稿にアフィリリンクを混ぜない

## 2026-07-22 全面リライト（Copilot Studio記事と同じ品質基準に）

`build_article.py` を新規作成。実行すると article.html を再生成して Post 2423 を上書き（status=draft 固定）。

- 本文 4,323字 → **10,756字**
- `.mb-*` デザインシステムを適用（step / table / note / warn / point / cards / check / cta / 免責）
- 句点ごとの `<br>` 改行、常体（〜だ・〜と思う）→ 敬体に統一
- 共感オープナー（「家計簿、3日続けて、4日目に飛ぶ」）を削除し、事実から入る書き出しに
- 図解SVG 3枚を新規作成（完成イメージ／フォルダを分ける効果／フロー2本の構成）

### ⚠️ 元の下書きにあった事実の誤り（Microsoft Learnで裏取りして修正）

| 元の記述 | 修正後（出典） |
|---|---|
| AI Builder「フォーム処理（レシート モデル）」 | **「領収書から情報を抽出する」**が正しいアクション名（flow-receipt-processing） |
| 「明細まで取ろうとすると揺れる」だけ | モデルとしては **PurchasedItems** で明細も出力される。揺れは実測としての所感、と書き分けた（prebuilt-receipt-processing） |
| 「クレジットが秒で溶ける」（数字なし） | **領収書1枚 = 32クレジット / Power Automate Premium = 5,000クレジット = 月約150枚**（credit-management） |
| 記載なし | **2026-11-01にシードクレジット廃止・新規はAI Builder容量アドオン購入不可**。公開時期を考えると必須なので警告ボックスで追記 |
| 記載なし | ファイル制限（JPEG/PNG/PDF・20MB・50×50〜10,000×10,000px）、**複数ページ非対応**、**60秒あたり360回**の呼び出し制限 |
| 「30日トライアル」「M365 Developer Program」 | 裏取りできなかったので削除した |

出典リンクは記事内に5箇所埋め込み済み。

### 実機スクショについて
実画面のモックは**作っていない**。アクション名は公式で裏取りしたが、設定パネルの
レイアウトまでは未確認のため、知識ベースで画面を創作しない方針に従った。
実機スクショを撮れば、各ステップ枠の下に差し込める。

## 次にやること
1. はるが内容確認・微修正
2. 実機スクショの追加（任意）
3. **手動で公開**（自動公開しない）
4. 公開後 IndexNow 送信
