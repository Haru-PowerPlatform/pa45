# PA45 第26回 YouTube 設定用（コピペ）

## タイトル
【Power Automate 45】第26回：毎日16時に届くTeamsカードを3択でタップ、報連相が自動でたまる ── アダプティブカードで報連相をワンタップに（PA45）

## 概要欄

初心者向けPower Automateハンズオン勉強会「PA45」第26回の録画です。
テーマ：毎日のカードで、報連相をワンタップに

報連相が抜けるのは、やる気の問題ではありません。「思い出す手間」と「言い出しにくさ」が原因です。今回は毎日16時にTeamsへ3択のカードが届き、🟢順調／🟡相談したい／🔴詰まってる を1つ押すだけで、記録も上司への一報も自動で回る仕組みを作ります。白紙に文章を書く必要はありません。非IT・初参加の方も歓迎です。

📌 今回のポイント
・4ブロックで完成：繰り返し → カードを送って待つ → 記録 → 条件で一報
・毎日16時に自動起動：スケジュール トリガーは頻度・時刻・タイムゾーン（東京）の3つだけ
・ここが今回の山場：Teamsには「カードを投稿するだけ」のアクションが無い。使うのは「アダプティブ カードを投稿して応答を待機する」で、押されるまでフローが一時停止する
・前提：Teamsに「ワークフロー」アプリが入っていること
・カードの中身はJSON：メッセージ欄にアダプティブカードのJSONをそのまま貼る。JSONはCopilotに書かせてよい
・押した答えの受け取り方：ボタンに data.status を持たせて body/data/status で取る（submitActionId より安定）
・記録の式を3つの部品に分解：body/data/status ／ coalesce() ／ convertTimeZone() を初心者向けに解説
・条件で分岐：🟢はログだけ、🟡🔴のときだけ上司へTeamsで一報
・1人でも完成：宛先を自分にすれば、最後まで動かして確認できます

📄 解説スライド（Web）
https://haru-powerplatform.github.io/pa45/slides/vol-26/

🛠️ ハンズオン手順（画面つき）
https://haru-powerplatform.github.io/pa45/slides/vol-26/handson.html

🗂️ 第26回の資料リンク集（完成フローのダウンロードあり）
https://haru-powerplatform.github.io/pa45/slides/vol-26/links.html

📺 過去回の動画アーカイブ
https://haru-powerplatform.github.io/pa45/videos/

🌐 PA45 参加者向けサイト（全回スライドまとめ）
https://haru-powerplatform.github.io/pa45/

📅 次回のPA45に参加する（connpass）
https://powerautomate-create.connpass.com/

PA45は「毎回45分・1テーマ・その場で一緒に作る」初心者向けのPower Automateハンズオン勉強会です。プログラミング経験ゼロでも大丈夫。見るだけの参加も歓迎です。

#PowerAutomate #PowerPlatform #Teams #報連相

## タグ（YouTubeタグ欄・カンマ区切りでコピペ）
Power Automate,パワーオートメート,PowerAutomate,PA45,Power Platform,パワープラットフォーム,Microsoft Teams,Teams,アダプティブカード,Adaptive Cards,報連相,ほうれんそう,日報,進捗管理,SharePoint,シェアポイント,スケジュールトリガー,定期実行,応答を待機,ワークフローアプリ,ノーコード,業務効率化,自動化,初心者,ハンズオン,勉強会,Microsoft 365

## その他の設定
- 再生リスト：PA45（Power Automate 45）ハンズオン
- 視聴者：子ども向けではありません（VIDEO_MADE_FOR_KIDS_NOT_MFK）
- 公開設定：公開
- 撮影日：2026-09-03

## サムネイル
C:\Users\isamu\Documents\pa45\assets\ogp\pa45-vol26-thumb.png （1280x720）
