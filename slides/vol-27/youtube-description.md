# PA45 第27回 YouTube 設定用（コピペ）

## タイトル
【Power Automate 45】第27回：Copilotに「何を渡すか」で答えが変わる ── スクショ・実行履歴・ZIPの中身、5つの渡し方（PA45）

## 概要欄

初心者向けPower Automateハンズオン勉強会「PA45」第27回の録画です。
テーマ：いま動いているフローを Copilot に相談する5つの渡し方

Copilotに聞いても的外れな答えが返ってくる。原因は質問の文章ではなく、渡している材料かもしれません。Copilotはあなたの画面を見ていないので、見せない限り推測で答えるしかないからです。今回は前回つくった「報連相カード」のフローを題材に、スクリーンショット・実行履歴・ZIPの中身をどう渡し分けるかを紹介します。今回はハンズオンなし、見るだけで最後まで成立する回です。

📌 今回のポイント
・① フロー全体のスクショを渡す：アクションは全部閉じて撮る。開いたままだと1つしか写らない
・② 実行履歴の「出力」を渡す：★整形された表示ではなく「未加工の出力を表示する」から取る。整形された画面から書き写すと項目名が実物と変わる
・③ エラーはスクショごと渡す：訳さない・要約しない。エラー文だけコピーすると「どのアクションで出たか」が抜ける
・④ 「日本語で」を足す：Copilotはアクション名を英語で返してくる。日本語画面に Create HTML table という名前は無い。「英語名（日本語名）で両方」と頼む
・⑤ ZIPの中のJSONを渡す：いちばん正確。折りたたまれた設定・条件の中身・式まで伝わる
・⑤の取り出し方：ソリューションを作る → フローを追加 → ★一覧側でエクスポート（フローを開いた画面の中には無い）→ アンマネージド → 展開 → Workflows フォルダの .json
・その前に：長いものを渡すときは Think Deeper に切り替える。通常モードは速く返る代わりに読み飛ばす
・貼る前に必ず：会社名・氏名・金額はサンプルに置き換える。スクショにも写ります。ZIPには環境IDや接続情報も入っています

📄 解説スライド（Web）
https://haru-powerplatform.github.io/pa45/slides/vol-27/

📋 そのまま貼れるプロンプト集（ZIPからJSONを取り出す手順つき）
https://haru-powerplatform.github.io/pa45/slides/vol-27/prompts.html

🗂️ 第27回の資料リンク集（題材フローのダウンロードあり）
https://haru-powerplatform.github.io/pa45/slides/vol-27/links.html

🧩 題材にしたフローの作り方（第26回）
https://haru-powerplatform.github.io/pa45/slides/vol-26/

📺 過去回の動画アーカイブ
https://haru-powerplatform.github.io/pa45/videos/

🌐 PA45 参加者向けサイト（全回スライドまとめ）
https://haru-powerplatform.github.io/pa45/

📅 次回のPA45に参加する（connpass）
https://powerautomate-create.connpass.com/

PA45は「毎回45分・1テーマ・その場で一緒に作る」初心者向けのPower Automateハンズオン勉強会です。プログラミング経験ゼロでも大丈夫。見るだけの参加も歓迎です。

#PowerAutomate #Copilot #PowerPlatform #業務効率化

## タグ（YouTubeタグ欄・カンマ区切りでコピペ）
Power Automate,パワーオートメート,PowerAutomate,PA45,Power Platform,パワープラットフォーム,Copilot,コパイロット,Microsoft Copilot,M365 Copilot,Think Deeper,プロンプト,プロンプトの書き方,AI活用,生成AI,スクリーンショット,実行履歴,エラー対処,エラーの直し方,JSON,ソリューション,エクスポート,アンマネージド,ノーコード,業務効率化,自動化,初心者,ハンズオン,勉強会,Microsoft 365

## その他の設定
- 再生リスト：PA45（Power Automate 45）ハンズオン
- 視聴者：子ども向けではありません（VIDEO_MADE_FOR_KIDS_NOT_MFK）
- 公開設定：公開
- 撮影日：2026-09-10

## サムネイル
C:\Users\isamu\Documents\pa45\assets\ogp\pa45-vol27-thumb.png （1280x720）
