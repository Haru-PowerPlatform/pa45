# PA45 第28回 YouTube 設定用（コピペ）

## タイトル
【Power Automate 45】第28回：毎日のやること3件をTeamsでチェックするだけで、SharePointのリストが自動で完了になる（PA45）

## 概要欄

初心者向けPower Automateハンズオン勉強会「PA45」第28回の録画です。
テーマ：やること3件を1枚のTeamsカードに出し、チェックした分だけまとめて完了にする

SharePointのリストを1件ずつ開いて「完了」に直す作業を、送信1回にまとめる回です。未完了の3件をリストから取ってきてTeamsのカードに並べ、チェックを入れて送信すると、チェックした項目だけが「完了」に書き換わります。カードのJSONと、返ってきた答えを取り出す式は、Copilotに聞きながら作りました。

📌 今回の内容
・下ごしらえ：リストの列は半角の Done で作り、あとから表示名を「完了」に変える。日本語で作ると内部名が _x5b8c_ のような文字列になり、フローから指定できない
・① 複数の項目の取得：フィルター クエリ Done eq 0 で未完了だけ、上位3件
・② アダプティブ カードを投稿して応答を待機する：送信ボタンが押されるまでフローはそこで止まる。カードのJSONは形を指定してCopilotに出してもらう
・③ 条件を入れる前に1回動かす：テスト実行の出力（body の中の data の形だけ）をCopilotに見せてから式を聞く
・★山場：body/data/t1 で返るのは文字列の "true"。body/data で取るとかたまり（Object）になり、split などの文字列関数はエラーになる
・④ 条件×3で完了に：t1〜t3 は自分で付けた名前なので1から、取得した一覧の [0]〜[2] は並び順なので0から数える
・Copilotに聞いた4か所：日本語の列名が動かない理由／カードのJSON／答えを取り出す式／エラー文（訳さずそのまま）

📄 解説スライド（Web）
https://haru-powerplatform.github.io/pa45/slides/vol-28/

📝 手順書（カードJSON・プロンプトのコピーボタンつき）
https://haru-powerplatform.github.io/pa45/slides/vol-28/handson.html

🗂️ 第28回の資料リンク集
https://haru-powerplatform.github.io/pa45/slides/vol-28/links.html

📺 過去回の動画アーカイブ
https://haru-powerplatform.github.io/pa45/videos/

🌐 PA45 参加者向けサイト（全回スライドまとめ）
https://haru-powerplatform.github.io/pa45/

📅 次回のPA45に参加する（connpass）
https://powerautomate-create.connpass.com/

PA45は「毎回45分・1テーマ・その場で一緒に作る」初心者向けのPower Automateハンズオン勉強会です。プログラミング経験ゼロでも大丈夫。見るだけの参加も歓迎です。

#PowerAutomate #Copilot #Teams #業務効率化

## タグ（YouTubeタグ欄・カンマ区切りでコピペ）
Power Automate,パワーオートメート,PowerAutomate,PA45,Power Platform,パワープラットフォーム,Copilot,コパイロット,Microsoft Teams,Teams,アダプティブカード,Adaptive Card,SharePoint,SharePointリスト,項目の更新,複数の項目の取得,フィルタークエリ,内部名,条件分岐,式,JSON,チェックリスト,ノーコード,業務効率化,自動化,初心者,ハンズオン,勉強会,Microsoft 365

## その他の設定
- 再生リスト：PA45（Power Automate 45）ハンズオン
- 視聴者：子ども向けではありません（VIDEO_MADE_FOR_KIDS_NOT_MFK）
- 公開設定：公開
- 撮影日：2026-09-17

## サムネイル
C:\Users\isamu\Documents\pa45\assets\ogp\pa45-vol28-thumb.png （1280x720）
