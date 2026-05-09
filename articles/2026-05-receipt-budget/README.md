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
- [feedback_pa45_blog_purpose_mvp](../../../.claude/projects/C--Users-isamu-Documents/memory/feedback_pa45_blog_purpose_mvp.md): automate136.com の記事は MVP 申請の証跡が主目的・SEO は二の次
- [feedback_pa45_blog_no_fabrication](../../../.claude/projects/C--Users-isamu-Documents/memory/feedback_pa45_blog_no_fabrication.md): 架空の体験談・盛り上げ描写は禁止
- [feedback_pa45_no_affiliate](../../../.claude/projects/C--Users-isamu-Documents/memory/feedback_pa45_no_affiliate.md): X 投稿にアフィリリンクを混ぜない
