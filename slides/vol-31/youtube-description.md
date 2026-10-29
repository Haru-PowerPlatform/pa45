# PA45 第31回 YouTube 設定用（コピペ）

## タイトル
【Power Automate 45】第31回：SharePointのファイルを選んで1クリックで、PDFにしてメールで送る（PA45）

## 概要欄

初心者向けPower Automateハンズオン勉強会「PA45」第31回の録画です。
テーマ：ファイルを選んで1クリックでPDFにして送る

見積書を送るたびに、Wordを開いてPDFで保存し直し、メールを書いて添付している。その手作業をなくす回です。SharePointのファイルの「…」からフローを動かし、送り先とひとことを入れるだけで、PDFに変換したファイルがメールに添付されて届きます。追加ライセンスの要らないOneDriveの「ファイルの変換」を使うため、一度自分のOneDriveにコピーしてから変換しています。

📌 今回の内容
・考え方：事務の仕事は6つの動詞の組み合わせ。今回は判断する（ファイルと相手を選ぶ）→作る（PDFにする）→知らせる（添付して送る）を1クリックでつなぐ
・作る前に：フローは既定の環境で作る。開発環境で作ると SharePoint の「…」に出てこない
・STEP 1：トリガーは「選択したファイルの場合」。押す人に送り先のメールとひとことを入れてもらう
・STEP 2：ファイルのプロパティの取得＝名前・ID などの情報、ファイル コンテンツの取得＝中身そのもの。名前を使いたいときと、ファイルを渡したいときで使い分ける
・STEP 3：OneDrive の「ファイルの変換」は自分の OneDrive のファイルしか扱えないので、ファイルの作成で一度置いてから PDF に変換する（Standard のまま使える）
・STEP 4：メールの送信 (V2)。宛先・件名・本文・添付の名前と中身は、全部前のステップの動的コンテンツから選ぶだけ
・STEP 5：保存して、SharePoint のファイルの「…」→ 統合 → フローから押して確かめる
・持ち帰り：「…」から押して PDF にする形は、請求書・議事録・申請書・Excel の表にも使える

📄 解説スライド（Web）
https://haru-powerplatform.github.io/pa45/slides/vol-31/

📝 手順書
https://haru-powerplatform.github.io/pa45/slides/vol-31/handson.html

🗂️ 第31回の資料リンク集
https://haru-powerplatform.github.io/pa45/slides/vol-31/links.html

📺 過去回の動画アーカイブ
https://haru-powerplatform.github.io/pa45/videos/

🌐 PA45 参加者向けサイト（全回スライドまとめ）
https://haru-powerplatform.github.io/pa45/

📅 次回のPA45に参加する（connpass）
https://powerautomate-create.connpass.com/

PA45は「毎回45分・1テーマ・その場で一緒に作る」初心者向けのPower Automateハンズオン勉強会です。プログラミング経験ゼロでも大丈夫。見るだけの参加も歓迎です。

#PowerAutomate #SharePoint #PDF #業務効率化

## タグ（YouTubeタグ欄・カンマ区切りでコピペ）
Power Automate,パワーオートメート,PowerAutomate,PA45,Power Platform,パワープラットフォーム,SharePoint,OneDrive,PDF,PDF変換,ファイルの変換,Word,見積書,選択したファイルの場合,ファイルのプロパティの取得,ファイルコンテンツの取得,メールの送信,添付ファイル,Outlook,既定の環境,インスタントフロー,ノーコード,業務効率化,自動化,初心者,ハンズオン,勉強会,Microsoft 365

## その他の設定
- 視聴者：子ども向けではありません（VIDEO_MADE_FOR_KIDS_NOT_MFK）
- 年齢制限：なし
- チャプターの自動生成：オン
- 公開設定：公開
- 撮影日：2026-10-15

## サムネイル
C:\Users\isamu\Documents\pa45\assets\ogp\pa45-vol31-thumb.png （1280x720）
