# PA45 第33回 YouTube 設定用（コピペ）

## タイトル
【Power Automate 45】第33回：SharePointリストの列の本当の名前（内部名）を、フローで一覧にしてメールで受け取る（PA45）

## 概要欄

初心者向けPower Automateハンズオン勉強会「PA45」第33回の録画です。
テーマ：内部名で困らない。内部名はフローが自動で調べる

SharePointリストをフローで使うと、列の名前が _x72b6__x614b_ のような記号の並びで出てくる。フィルター クエリにはこの名前で書かないと動かないので、列の設定を1つずつ開いて調べている。その作業をフローに任せる回です。リスト名を入れて押すと、表示名と内部名の表がメールで届きます。最後に、届いた内部名で「貸出中」の行だけ取り出すところを画面で確かめました。

📌 今回の内容
・内部名とは：列には、画面に出る表示名とは別に、作ったときに決まって変わらない内部名がある。日本語や空白は1文字ずつ記号になる（状 → _x72b6_）
・なぜ要る：フィルター クエリ・並べ替え・式・HTTP 要求の URI など、列を文字で直接書く欄では内部名を使う。動的コンテンツから選ぶ欄は表示名のままでよい
・準備：練習用のリスト「備品の貸し出し」を、列名は日本語のまま作る
・STEP 1：フローを手動でトリガーする。入力欄「リスト名」をつける
・STEP 2：SharePoint に HTTP 要求を送信します。方法は GET（読むだけ）、URI は _api/web/lists/getbytitle('リスト名')/fields に、隠れた列を除く条件と Title・InternalName だけ返す指定を付ける。ヘッダー Accept に application/json;odata=nometadata
・STEP 3：選択で、返事の value から表示名と内部名の2つだけ取り出す
・STEP 4：HTML テーブルの作成で、メールで読める表にする
・STEP 5：メールの送信 (V2) で自分あてに送る
・STEP 6：保存して、リスト名を入れて動かす
・使ってみる：届いた内部名で _x72b6__x614b_ eq '貸出中' と書くと、貸出中の行だけ返ってくる（表示名で書くとエラー）

📄 解説スライド（Web）
https://haru-powerplatform.github.io/pa45/slides/vol-33/

📝 手順書（URI・式のコピーボタンつき）
https://haru-powerplatform.github.io/pa45/slides/vol-33/handson.html

🗂️ 第33回の資料リンク集（配布フローのダウンロードあり）
https://haru-powerplatform.github.io/pa45/slides/vol-33/links.html

📺 過去回の動画アーカイブ
https://haru-powerplatform.github.io/pa45/videos/

🌐 PA45 参加者向けサイト（全回スライドまとめ）
https://haru-powerplatform.github.io/pa45/

📅 次回のPA45に参加する（connpass）
https://powerautomate-create.connpass.com/

PA45は「毎回45分・1テーマ・その場で一緒に作る」初心者向けのPower Automateハンズオン勉強会です。プログラミング経験ゼロでも大丈夫。見るだけの参加も歓迎です。

#PowerAutomate #SharePoint #内部名 #業務効率化

## タグ（YouTubeタグ欄・カンマ区切りでコピペ）
Power Automate,パワーオートメート,PowerAutomate,PA45,Power Platform,パワープラットフォーム,SharePoint,SharePointリスト,内部名,InternalName,表示名,列名,フィルタークエリ,HTTP要求,SharePointにHTTP要求を送信します,REST API,JSON,選択,HTMLテーブルの作成,メールの送信,式,ノーコード,業務効率化,自動化,初心者,ハンズオン,勉強会,Microsoft 365

## その他の設定
- 視聴者：子ども向けではありません（VIDEO_MADE_FOR_KIDS_NOT_MFK）
- 年齢制限：なし
- チャプターの自動生成：オン
- 公開設定：公開
- 撮影日：2026-10-29

## サムネイル
C:\Users\isamu\Documents\pa45\assets\ogp\pa45-vol33-thumb.png （1280x720）
