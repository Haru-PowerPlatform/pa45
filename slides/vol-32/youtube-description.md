# PA45 第32回 YouTube 設定用（コピペ）

## タイトル
【Power Automate 45】第32回：フォルダに置くだけで、ファイルが自動で月別フォルダに片付く（PA45）

## 概要欄

初心者向けPower Automateハンズオン勉強会「PA45」第32回の録画です。
テーマ：置くだけで月別フォルダに片付くファイル整理

スキャンした請求書や見積書は、保存先がいつも同じ1つのフォルダにたまっていく。月末に、月ごとのフォルダへ手で移している。その作業をなくす回です。OneDriveの「受け取り」フォルダにファイルが届いたら、フローがその月のフォルダ（例：2026-10）へ移し、どこに入ったかをTeamsで知らせます。月のフォルダ名は今日の日付から式で作るので、毎月書き換える必要はありません。

📌 今回の内容
・考え方：事務の仕事は6つの動詞の組み合わせ。今回は受け付ける→判断する（今月のフォルダを決める）→知らせるを、ファイルが届いただけでつなぐ
・こんなときに効く：複合機のスキャン、メール添付の自動保存、Forms のアップロード、Teams 会議の録画、スクリーンショットなど、置き場所を自分で選べないファイル
・しくみ：フローの始まり方は3つ（時刻になったら／人が押したら／何かが起きたら）。今回は「自動化したクラウド フロー」で、ファイルが届いたことがきっかけ
・準備：OneDrive に「受け取り」フォルダだけ作る。整理済みと月のフォルダは、移すときに自動で作られる
・STEP 1：トリガーは OneDrive の「ファイルの作成時 (プロパティのみ)」。フォルダーは受け取りを選ぶ
・STEP 2：ファイルの移動または名前変更。対象ファイルのパスは「/PA45第32回/整理済み/」＋ formatDateTime(utcNow(), 'yyyy-MM') ＋ ファイル名 の3つをつなげて作る
・注意：utcNow() は世界標準時。月初1日の 0:00〜8:59（日本時間）に置くと、前の月のフォルダに入る
・STEP 3：Teams のフロー ボットから、移動したあとの場所（Path）を知らせる
・STEP 4：保存して、受け取りフォルダにファイルを置き、1〜2分待って確かめる
・持ち帰り：「何かが起きたら動く」形は、メール添付の保存先の整理や、請求書が届いたら経理に知らせる仕事にも使える

📄 解説スライド（Web）
https://haru-powerplatform.github.io/pa45/slides/vol-32/

📝 手順書
https://haru-powerplatform.github.io/pa45/slides/vol-32/handson.html

🗂️ 第32回の資料リンク集
https://haru-powerplatform.github.io/pa45/slides/vol-32/links.html

📺 過去回の動画アーカイブ
https://haru-powerplatform.github.io/pa45/videos/

🌐 PA45 参加者向けサイト（全回スライドまとめ）
https://haru-powerplatform.github.io/pa45/

📅 次回のPA45に参加する（connpass）
https://powerautomate-create.connpass.com/

PA45は「毎回45分・1テーマ・その場で一緒に作る」初心者向けのPower Automateハンズオン勉強会です。プログラミング経験ゼロでも大丈夫。見るだけの参加も歓迎です。

#PowerAutomate #OneDrive #ファイル整理 #業務効率化

## タグ（YouTubeタグ欄・カンマ区切りでコピペ）
Power Automate,パワーオートメート,PowerAutomate,PA45,Power Platform,パワープラットフォーム,OneDrive,OneDrive for Business,ファイル整理,フォルダ整理,月別フォルダ,ファイルの作成時,ファイルの移動または名前変更,formatDateTime,utcNow,式,自動化したクラウドフロー,スキャン,請求書,Microsoft Teams,Teams,ノーコード,業務効率化,自動化,初心者,ハンズオン,勉強会,Microsoft 365

## その他の設定
- 視聴者：子ども向けではありません（VIDEO_MADE_FOR_KIDS_NOT_MFK）
- 年齢制限：なし
- チャプターの自動生成：オン
- 公開設定：公開
- 撮影日：2026-10-22

## サムネイル
C:\Users\isamu\Documents\pa45\assets\ogp\pa45-vol32-thumb.png （1280x720）
