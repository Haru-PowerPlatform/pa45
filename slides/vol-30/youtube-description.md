# PA45 第30回 YouTube 設定用（コピペ）

## タイトル
【Power Automate 45】第30回：Teamsで頼まれたメッセージを、1クリックでTo Doのタスクにする（PA45）

## 概要欄

初心者向けPower Automateハンズオン勉強会「PA45」第30回の録画です。
テーマ：Teamsの頼まれごとを1クリックでTo Doに入れる

Teamsで頼まれたことを、To Doに手で書き写している。会議中に来た分は写し忘れて流れていく。その書き写しをなくす回です。Teamsのメッセージの「…」からフローを動かし、カードで期限・重要度・メモを選ぶと、メッセージの文がそのままTo Doのタスクになります。期限を選ばなかったときは3日後が入ります。カードのJSONと期日の式は、Copilotに1回で作ってもらいました。

📌 今回の内容
・考え方：事務の仕事は6つの動詞（受け付ける・書き写す・判断する・知らせる・まとめる・作る）の組み合わせ。今回は受け付ける→判断する→書き写す→知らせるを1クリックでつなぐ
・準備：M365 Copilot チャットに指示を1回送り、アダプティブ カードのJSON（期限・重要度・メモ）と期日の式をまとめて出してもらう
・STEP 1：インスタント クラウド フローで、トリガーは「選択されたメッセージに対して (V2)」
・STEP 2：トリガーの「アダプティブ カード の作成」にカードのJSONを貼る。カードで付けた id（dueDate・importance・memo）が、そのまま動的コンテンツの名前になる
・STEP 3：To Do を追加する (V3)。タイトル＝メッセージの内容、期日＝if(empty(…), addDays(…), …) の式、重要度とメモ＝カードの値
・STEP 4：フロー ボットから「To Do に追加しました」と返す
・STEP 5：保存して、Teams のメッセージの「…」から押して確かめる
・持ち帰り：「…」から押す入口は、Planner・Excel・SharePoint リスト・メール転送にも使える

📄 解説スライド（Web）
https://haru-powerplatform.github.io/pa45/slides/vol-30/

📝 手順書（カードJSON・プロンプトのコピーボタンつき）
https://haru-powerplatform.github.io/pa45/slides/vol-30/handson.html

🗂️ 第30回の資料リンク集
https://haru-powerplatform.github.io/pa45/slides/vol-30/links.html

📺 過去回の動画アーカイブ
https://haru-powerplatform.github.io/pa45/videos/

🌐 PA45 参加者向けサイト（全回スライドまとめ）
https://haru-powerplatform.github.io/pa45/

📅 次回のPA45に参加する（connpass）
https://powerautomate-create.connpass.com/

PA45は「毎回45分・1テーマ・その場で一緒に作る」初心者向けのPower Automateハンズオン勉強会です。プログラミング経験ゼロでも大丈夫。見るだけの参加も歓迎です。

#PowerAutomate #Teams #ToDo #業務効率化

## タグ（YouTubeタグ欄・カンマ区切りでコピペ）
Power Automate,パワーオートメート,PowerAutomate,PA45,Power Platform,パワープラットフォーム,Microsoft Teams,Teams,Microsoft To Do,To Do,タスク管理,選択されたメッセージに対して,アダプティブカード,Adaptive Card,Copilot,コパイロット,式,if,addDays,empty,期限,インスタントフロー,ノーコード,業務効率化,自動化,初心者,ハンズオン,勉強会,Microsoft 365

## その他の設定
- 視聴者：子ども向けではありません（VIDEO_MADE_FOR_KIDS_NOT_MFK）
- 年齢制限：なし
- チャプターの自動生成：オン
- 公開設定：公開
- 撮影日：2026-10-08

## サムネイル
C:\Users\isamu\Documents\pa45\assets\ogp\pa45-vol30-thumb.png （1280x720）
