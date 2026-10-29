# PA45 第29回 YouTube 設定用（コピペ）

## タイトル
【Power Automate 45】第29回：毎朝届くメールの件数といちばん新しい件名を、Teamsに1通にまとめて届ける（PA45）

## 概要欄

初心者向けPower Automateハンズオン勉強会「PA45」第29回の録画です。
テーマ：動的コンテンツに出てこない値も、Copilotと一緒に式で取り出せるようになる

毎朝、受信トレイの件名をチャットに書き写して課長に送る。その10分をフローにする回です。メールを取得して Teams に件名を入れると、For each が勝手に付いて3通に分かれ、件数は動的コンテンツの一覧のどこにもありません。そこでアクションの「未加工の出力」を開き、{ } と [ ] の読み方を確認してから、件数といちばん新しい件名を式で取り出して1通にまとめました。

📌 今回の内容
・第1章 まず動かす：自分あてに「PA45 …」のメールを3通送る → 繰り返し（東京・8時）→ メールを取得する (V3)（件名フィルター PA45・上位5）→ テストで緑を確認
・第2章 つまずく：Teams の本文で「件名」を選ぶと For each が付き、3通に分かれる。件数は一覧に無い。Copilotに聞いた式は、本文で「/」→「式を挿入する」で入れる
・第3章 出力を読む：テスト結果 →「未加工の出力を表示する」。出力のほとんどは配送の記録と本文のHTMLで、見るのは value・subject・from／receivedDateTime の3か所
・value は棚、{ } はひとかたまり、[ ] は並び、/ は「の中の」と読む。出力の名前を上から順にたどると式になる
・第4章 取り出す：For each を消して Teams を外に置く。件数＝length(body('メールを取得する_(V3)')?['value'])、いちばん新しい件名＝first(…)?['subject']。1行足すたびにテストする
・持ち帰り：差出人 ?['from']、受信日時 ?['receivedDateTime']、2件目 ?[1]、最後 last() も同じたどり方で取れる

📄 解説スライド（Web）
https://haru-powerplatform.github.io/pa45/slides/vol-29/

📝 手順書
https://haru-powerplatform.github.io/pa45/slides/vol-29/handson.html

🗂️ 第29回の資料リンク集
https://haru-powerplatform.github.io/pa45/slides/vol-29/links.html

📺 過去回の動画アーカイブ
https://haru-powerplatform.github.io/pa45/videos/

🌐 PA45 参加者向けサイト（全回スライドまとめ）
https://haru-powerplatform.github.io/pa45/

📅 次回のPA45に参加する（connpass）
https://powerautomate-create.connpass.com/

PA45は「毎回45分・1テーマ・その場で一緒に作る」初心者向けのPower Automateハンズオン勉強会です。プログラミング経験ゼロでも大丈夫。見るだけの参加も歓迎です。

#PowerAutomate #Copilot #Outlook #業務効率化

## タグ（YouTubeタグ欄・カンマ区切りでコピペ）
Power Automate,パワーオートメート,PowerAutomate,PA45,Power Platform,パワープラットフォーム,Copilot,コパイロット,式,関数,length,first,last,JSON,配列,動的コンテンツ,未加工の出力,For each,Apply to each,メールを取得する,Outlook,Microsoft Teams,Teams,繰り返し,ノーコード,業務効率化,自動化,初心者,ハンズオン,勉強会,Microsoft 365

## その他の設定
- 再生リスト：PA45（Power Automate 45）ハンズオン
- 視聴者：子ども向けではありません（VIDEO_MADE_FOR_KIDS_NOT_MFK）
- 公開設定：公開
- 撮影日：2026-10-01

## サムネイル
C:\Users\isamu\Documents\pa45\assets\ogp\pa45-vol29-thumb.png （1280x720）
