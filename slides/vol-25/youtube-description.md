# PA45 第25回 YouTube 設定用（コピペ）

## タイトル
【Power Automate 45】第25回：メールの添付を、開かずに保存する ── 今月のフォルダへ名前を変えて自動保存＋元メールに「保存済み」の印（PA45）

## 概要欄

初心者向けPower Automateハンズオン勉強会「PA45」第25回の録画です。
テーマ：メールの添付を自動で保存する

請求書が届くたびに、メールを開いて、添付を落として、フォルダに置く。この3手間をなくす回です。添付つきのメールが届いたら、今月のフォルダへ日付つきの名前で保存し、元のメールに「保存済み」の色ラベルをつけて、Teamsに「◯件保存しました」と知らせるところまでを一緒に作ります。プログラミング経験ゼロでも大丈夫です。

📌 今回のポイント
・5ブロックで完成：メール受信 → 添付を1件ずつ → 保存 → 元メールに印 → 通知
・★今日いちばんの山場：トリガー「新しいメールが届いたとき (V3)」の「添付ファイルを含める」は既定がオフ。オフのまま進めると、中身の無い0KBの空ファイルが保存される
・その設定は「すべて表示」を押さないと出てこない（添付ファイルを含める／添付ファイル付きのみ／件名フィルター／フォルダー）
・添付は1件とは限らない：1通に3つ入っていることもあるので Apply to each で1件ずつ取り出す。トリガーの「添付ファイル」を渡すだけ
・保存先のフォルダは、無くても自動で作られる
・ファイル名の頭に日付を付けると、同じ名前の添付による上書き事故が消える
・★画面に「ドキュメント」と日本語で出ていても、中の名前は /Shared Documents。表示名と内部名は別、という実務で必ず出るポイント
・元メールへの印：「Outlook カテゴリを割り当てます」でカテゴリ「保存済み」を付ける。受信トレイに色ラベルが残るので、二重処理を防げる
・最後に実物のフローで、メールを送る→フォルダにファイルが並ぶ→メールに色がつく、まで確認します

📄 解説スライド（Web）
https://haru-powerplatform.github.io/pa45/slides/vol-25/

🛠️ ハンズオン手順（画面つき）
https://haru-powerplatform.github.io/pa45/slides/vol-25/handson.html

🗂️ 第25回の資料リンク集（完成フローのダウンロードあり）
https://haru-powerplatform.github.io/pa45/slides/vol-25/links.html

📺 過去回の動画アーカイブ
https://haru-powerplatform.github.io/pa45/videos/

🌐 PA45 参加者向けサイト（全回スライドまとめ）
https://haru-powerplatform.github.io/pa45/

📅 次回のPA45に参加する（connpass）
https://powerautomate-create.connpass.com/

PA45は「毎回45分・1テーマ・その場で一緒に作る」初心者向けのPower Automateハンズオン勉強会です。プログラミング経験ゼロでも大丈夫。見るだけの参加も歓迎です。

#PowerAutomate #Outlook #SharePoint #業務効率化

## タグ（YouTubeタグ欄・カンマ区切りでコピペ）
Power Automate,パワーオートメート,PowerAutomate,PA45,Power Platform,パワープラットフォーム,Outlook,アウトルック,メール自動化,添付ファイル,添付ファイル保存,請求書,SharePoint,シェアポイント,ファイルの作成,Apply to each,繰り返し処理,Microsoft Teams,Teams,カテゴリ,色分け,ノーコード,業務効率化,自動化,初心者,ハンズオン,勉強会,Microsoft 365

## その他の設定
- 再生リスト：PA45（Power Automate 45）ハンズオン
- 視聴者：子ども向けではありません（VIDEO_MADE_FOR_KIDS_NOT_MFK）
- 公開設定：公開
- 撮影日：2026-08-27

## サムネイル
C:\Users\isamu\Documents\pa45\assets\ogp\pa45-vol25-thumb.png （1280x720）
