# PA45 ― Power Automate 45分ハンズオン

Power Automate を初めて触る人が、45分で1本のフローを作り終えるオンライン講座です。\
週1回、無料で開催しています。

講座で使ったスライド、完成したフローのZIP、録画、アンケートの集計は、このリポジトリと公開サイトですべて無料で公開しています。\
参加していない人でも、同じ手順をあとから再現できる形で残しています。

- 公開サイト：https://haru-powerplatform.github.io/pa45/
- 参加申込（connpass）：https://powerautomate-create.connpass.com/
- 運営：Haru（X [@isamu_Automate](https://x.com/isamu_Automate)／ブログ [automate136.com](https://www.automate136.com/)）

> **About (English)** ― PA45 is a free, weekly, 45-minute hands-on online workshop that helps business users with no IT background build their first Power Automate cloud flow. Slides, importable flow solutions (ZIP), recordings and aggregated survey results for every session are published openly in this repository.

## 目次

- [数字で見る PA45](#数字で見る-pa45)
- [公開している教材](#公開している教材)
- [全回の一覧](#全回の一覧)
- [講座以外のコミュニティ活動](#講座以外のコミュニティ活動)
- [フローZIPの使い方](#フローzipの使い方)
- [利用条件（ライセンス）](#利用条件ライセンス)
- [リポジトリの構成](#リポジトリの構成)

## 数字で見る PA45

第1回（2026/03/06）〜第27回（2026/09/10）の集計です。

| 項目 | 値 |
|---|---|
| 開催回数 | 27回 |
| 延べ参加者 | 1,165名 |
| 1回あたりの参加者 | 平均 43.1名／最多 76名 |
| 参加者の推移 | 第1〜5回の平均 31.0名 → 直近5回の平均 60.0名 |
| アンケート回答 | 343件 |
| 理解度スコア（全回平均） | 89.9% |
| 役立ち度スコア（全回平均） | 92.6% |
| 録画を公開した回 | 24回 |
| 公開しているフローZIP | 19本 |
| 技術Tipsスライド | 119本 |

- 参加者数は connpass の参加者数、スコアは各回のアンケートから集計しています（`data/insights.json`）。
- 理解度スコア＝5択（とても理解できた100／理解できた75／普通50／少し難しかった25／難しかった0）の回答数による加重平均。
- 役立ち度スコア＝3択（役立ちそう100／少し役立ちそう50／まだイメージがついていない0）の加重平均。
- 回ごとの内訳と自由記述は [アンケート結果](https://haru-powerplatform.github.io/pa45/achievements/insights/) にあります。

## 公開している教材

| 教材 | 中身 | 場所 |
|---|---|---|
| 講座スライド | 各回のHTMLスライド。ブラウザで開けば、そのまま手順を追える | [全回の目次](https://haru-powerplatform.github.io/pa45/slides/links.html)／[`slides/`](slides/) |
| フローのZIP | 講座で作ったフローの完成品。自分の環境にインポートして動きを確認できる | [ダウンロードページ](https://haru-powerplatform.github.io/pa45/flows/)／[`flows/`](flows/) |
| 録画 | 講座当日の録画（YouTube） | [動画アーカイブ](https://haru-powerplatform.github.io/pa45/videos/) |
| アンケート結果 | 回ごとの理解度・役立ち度・自由記述 | [アンケート結果](https://haru-powerplatform.github.io/pa45/achievements/insights/) |
| 技術Tipsスライド | Power Automate／Copilot Studio の小技を1テーマ1枚にまとめたスライド | [スライド一覧](https://haru-powerplatform.github.io/pa45/slides/) |
| 初参加ガイド | 参加前に用意するもの、当日の流れ | [初めての方へ](https://haru-powerplatform.github.io/pa45/start-here/) |
| 講座の設計 | 45分に収める理由、1回1テーマに絞る理由 | [PA45 Method](https://haru-powerplatform.github.io/pa45/method/) |
| 登壇資料 | 外部のコミュニティイベントで話したときのスライド | [登壇・LT資料](https://haru-powerplatform.github.io/pa45/talks/) |

## 全回の一覧

次回は **第28回 Copilotと通知カード1枚でまとめて完了にする**（9月17日（木） 20:15〜21:00）です。申込は [connpass](https://powerautomate-create.connpass.com/event/406563/) から。

| 回 | 開催日 | テーマ | 参加 | スライド・資料 | フロー | 録画 | アンケート | レポート |
|---:|---|---|---:|:---:|:---:|:---:|:---:|:---:|
| 27 | 2026/09/10 | いま動いているフローをCopilotに相談する5つの渡し方 | 52名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-27/) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-27/PA45-Vol27-Demo.zip) | [見る](https://www.youtube.com/watch?v=h3L75SsbRXE) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-27.html) | ― |
| 26 | 2026/09/03 | 毎日のカードで報連相をワンタップ | 52名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-26/) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-26/PA45-Vol26-HourenCard.zip) | [見る](https://www.youtube.com/watch?v=VVGw6AUsAbk) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-26.html) | ― |
| 25 | 2026/08/27 | メールの添付を自動でSharePointへ保存 | 51名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-25/) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-25/PA45-Vol25-MailAttachment.zip) | [見る](https://www.youtube.com/watch?v=oO1aHXgcjc8) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-25.html) | ― |
| 24 | 2026/08/22 | スタンプ👍を押すだけで出欠集計 | 71名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-24/) | ― | [見る](https://www.youtube.com/watch?v=5j4O_vkfa6c) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-24.html) | ― |
| 23 | 2026/08/15 | Excelの「答え」でフローが分かれる | 74名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-23/) | ― | [見る](https://www.youtube.com/watch?v=UrbfQc6Iqps) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-23.html) | ― |
| 22 | 2026/08/06 | コードを書かずにExcel作業を自動化 | 76名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-22/) | ― | [見る](https://www.youtube.com/watch?v=kNwyUHMtFt4) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-22.html) | ― |
| 21 | 2026/07/30 | 原点回帰の復習回 | 59名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-21/) | ― | [見る](https://www.youtube.com/watch?v=24c58380CYg) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-21.html) | ― |
| 20 | 2026/07/23 | アダプティブカードの作り方 | 48名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-20/) | ― | [見る](https://www.youtube.com/watch?v=wOegDNZSeHU) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-20.html) | [記事](https://www.automate136.com/pa45-vol20-adaptive-card/) |
| 19 | 2026/07/16 | 自動化の成果を "見える化" | 48名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-19/) | ― | [見る](https://youtu.be/OT2v3aWweT0) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-19.html) | [記事](https://www.automate136.com/pa45-vol19-powerbi-dashboard/) |
| 18 | 2026/07/09 | 承認エスカレーション | 49名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-18/) | ― | [見る](https://youtu.be/cghp6TOJfw8) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-18.html) | [記事](https://www.automate136.com/pa45-vol18-approval-escalation/) |
| 17 | 2026/07/02 | 期限の見張り番 | 51名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-17/) | ― | [見る](https://youtu.be/jwOECxCtUPE) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-17.html) | [記事](https://www.automate136.com/pa45-vol17-deadline-reminder/) |
| 16 | 2026/06/25 | Copilotと作るPower Automate | 48名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-16/) | ― | [見る](https://youtu.be/dVM-WF1A79g) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-16.html) | [記事](https://www.automate136.com/pa45-vol16-copilot/) |
| 15 | 2026/06/18 | 共有フォルダ監視 → 自動メール通知 | 35名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-15/) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-15/PA45-Vol15-FolderWatchMail.zip) | [見る](https://youtu.be/yvzeXB73LFU) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-15.html) | [記事](https://www.automate136.com/pa45-vol15-folder-watch/) |
| 14 | 2026/06/11 | JSONの読み方 | 48名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-14/) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-14/PA45-Vol14-JsonReading.zip) | [見る](https://youtu.be/9fkbQmOR6Fo) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-14.html) | [記事](https://www.automate136.com/pa45-vol14-json/) |
| 13 | 2026/06/04 | Try-Catch でフロー運用を安心化 | 28名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-13/) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-13/PA45-Vol13-TryCatch.zip) | [見る](https://youtu.be/2XjY3GWomMA) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-13.html) | [記事](https://www.automate136.com/pa45-vol13-try-catch/) |
| 12 | 2026/05/28 | 「式」アレルギー、今日で卒業 | 27名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-12/) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-12/PA45-Vol12-Expression.zip) | [見る](https://youtu.be/QkrYCpP5hCc) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-12.html) | [記事](https://www.automate136.com/pa45-vol12-expressions/) |
| 11 | 2026/05/21 | 失敗しないフロー設計 | 26名 | [資料](https://haru-powerplatform.github.io/pa45/slides/vol-11/links.html) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-11/PA45-Vol11-RunHistory.zip) | [見る](https://youtu.be/0Wvv6Bf3n18) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-11.html) | [記事](https://www.automate136.com/pa45-vol11-run-history-report/) |
| 10 | 2026/05/14 | 4つを1本につなぐ総復習 | 28名 | [資料](https://haru-powerplatform.github.io/pa45/slides/vol-10/links.html) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-10/PA45-Vol10-BizReview.zip) | ― | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-10.html) | [記事](https://www.automate136.com/pa45-vol10-expense-review/) |
| 9 | 2026/05/07 | SharePointのファイル更新をTeamsに自動通知 | 35名 | [資料](https://haru-powerplatform.github.io/pa45/slides/vol-09/links.html) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-09/PA45-Vol09-SharePointUpdate.zip) | [見る](https://youtu.be/MIA3jPT_4YU) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-09.html) | [記事](https://www.automate136.com/pa45-vol9-sharepoint-teams-report/) |
| 8 | 2026/04/30 | 申請承認フロー（Approvals） | 41名 | [資料](https://haru-powerplatform.github.io/pa45/slides/vol-08/links.html) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-08/PA45-Vol08-ApprovalFlow.zip) | [見る](https://youtu.be/4QmDeRgGGLk) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-08.html) | [記事](https://www.automate136.com/pa45-vol8-approvals/) |
| 7 | 2026/04/23 | Formsの申請をSharePointに自動登録 | 26名 | [資料](https://haru-powerplatform.github.io/pa45/slides/vol-07/links.html) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-07/PA45-Vol07-FormsSPTeams.zip) | [見る](https://youtu.be/JOOlaiBvYgQ) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-07.html) | [記事](https://www.automate136.com/pa45-vol7-forms-sharepoint-teams/) |
| 6 | 2026/04/17 | Forms × Compose × Teams | 37名 | [資料](https://haru-powerplatform.github.io/pa45/slides/vol-06/links.html) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-06/PA45-Vol06-FormsMail.zip) | [見る](https://youtu.be/rvSX575fdbo) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-06.html) | [記事](https://www.automate136.com/pa45-vol6-forms-mail/) |
| 5 | 2026/04/09 | 基礎固めWeek | 38名 | [資料](https://haru-powerplatform.github.io/pa45/slides/vol-05/links.html) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-05/PA45-Vol05-Review.zip) | [見る](https://youtu.be/cltHw91fYm4) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-05.html) | [記事](https://www.automate136.com/pa45-vol5-basics-week/) |
| 4 | 2026/04/02 | Apply to Each を使おう | 29名 | [資料](https://haru-powerplatform.github.io/pa45/slides/vol-04/links.html) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-04/PA45-Vol04-ApplyToEach.zip) | [見る](https://youtu.be/RzHylaoTRrs) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-04.html) | [記事](https://www.automate136.com/pa45-vol4-apply-to-each/) |
| 3 | 2026/03/26 | 条件分岐を使おう | 30名 | [資料](https://haru-powerplatform.github.io/pa45/slides/vol-03/links.html) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-03/PA45-Vol03-Condition.zip) | ― | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-03.html) | [記事](https://www.automate136.com/pa45-vol3-condition/) |
| 2 | 2026/03/12 | 変数を操作しよう | 32名 | [資料](https://haru-powerplatform.github.io/pa45/slides/vol-02/links.html) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-02/PA45-Vol02-SetVariable.zip) | ― | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-02.html) | [記事](https://www.automate136.com/pa45-vol2-set-variable/) |
| 1 | 2026/03/06 | 変数の初期化 | 26名 | [資料](https://haru-powerplatform.github.io/pa45/slides/vol-01/links.html) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-01/PA45-Vol01-InitializeVariable.zip) | [見る](https://youtu.be/GEB2zGcmF88) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-01.html) | [記事](https://www.automate136.com/pa45-vol1-initialize-variable/) |

「―」は、その回の公開物をまだこのリポジトリに置いていないことを表します。

## 講座以外のコミュニティ活動

PA45 の外で、Power Platform／Copilot のコミュニティに関わった記録です。

| 日付 | 内容 | 役割 | 規模 | リンク |
|---|---|---|---|---|
| 2026/03/14 | DX推進 Power Platform MeetUp文化祭 in Hiroshima（PLUG 広島初の現地開催）を主催 | 主催（運営メンバー）/ 開会あいさつ / LT登壇 | 参加83名（現地21 / 現地運営12 / オンライン48 / LT2） | [connpass](https://plug.connpass.com/event/381240/) ／ [レポート](https://www.automate136.com/powerplatform_fes_202603/) |
| 2026/03/19 | 「一歩踏み出せTV」第25話にゲスト出演 | ゲスト出演 | ― | [connpass](https://ippo.connpass.com/event/386774/) |
| 2026/05/13 | なんでもCopilot #80（第3回なんコパLT大会）で登壇：会議コストBotを生み出した話 | 登壇 | ― | [connpass](https://nandemo.connpass.com/event/390633/) ／ [スライド](https://github.com/Haru-PowerPlatform/pa45/raw/main/assets/pa45/LT001_Copilot_MeetingCostBot_20260428.pptx) ／ [登壇資料](https://haru-powerplatform.github.io/pa45/talks/) |
| 2026/05/31 | PLUG MeetUp Vol.2（広島・ハイブリッド）を運営 | 運営メンバー（PLUG 発起人） | 参加75名（現地8 / オンライン60 / 運営7） | [connpass](https://plug.connpass.com/event/392237/) |
| 2026/06/06 | なんでもCopilot 大阪（初の出張会・現地）で登壇：学びを、成果に変える ── Copilot と Power Platform で進める社内DX | 登壇 | 現地コミュニティイベント（大阪出張会） | [スライド](https://haru-powerplatform.github.io/pa45/talks/2026-osaka-copilot/slides.html) ／ [登壇資料](https://haru-powerplatform.github.io/pa45/talks/) |
| 2026/08/29 | PLUG MeetUp Vol.3「対話からはじまる現場の変革」（広島・ハイブリッド）を運営 | 運営メンバー（PLUG 発起人） | 参加51名（現地14 / オンライン33 / 運営4） | [connpass](https://plug.connpass.com/event/401829/) |
| 2026/09/02 | Microsoft へ製品フィードバックを提出：Copilot Studio Evaluate で「Error（採点不能）」と「Fail（0点）」が区別できない問題の改善要望 | 報告者 | Copilot Studio Ideas（公開・投票可） | [公開ページ](https://ideas.powervirtualagents.com/d365community/idea/81439407-99a6-f111-85cd-7c1e52b98ad4) |
| 2026/09/02 | Power Platform Community で回答（2本）：SharePointの別リストから承認先を引く／Apply to each のネストを外す | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=71e16edd-35a6-f111-b8de-6045bdff2fc0) |
| 2026/09/24 | ビジュアルプログラミングIoTLT vol.24 でLT登壇：作らせる前に、使ってもらう ── 社内で非エンジニアにビジュアルプログラミングを教えた話 | 登壇 | オンラインLTイベント（YouTube配信） | [connpass](https://iotlt.connpass.com/event/400538/) |

すべての記録は [`data/activities/`](data/activities/) に1件1ファイルで置いています。サイト上では [活動の記録](https://haru-powerplatform.github.io/pa45/achievements/) で見られます。

## フローZIPの使い方

ZIPは Power Automate の「ソリューション」形式です。\
展開せずにそのままインポートします。

1. [フローのダウンロードページ](https://haru-powerplatform.github.io/pa45/flows/) から、使いたい回のZIPを保存する
2. make.powerautomate.com の左メニュー「ソリューション」→「インポート」→「ソリューションのインポート」でZIPを選ぶ
   - ソリューション形式にしているのは、フロー本体と接続の設定をまとめて持ち運べるため
3. インポートしたフローを開き、接続が必要と表示されたアクションに自分のアカウントで接続する
   - 接続は作った人のアカウントに紐づくため、インポートした側で付け直す必要がある
4. 保存してフローをオンにし、講座スライドの手順に沿って動かす

組織の環境によっては、ソリューションのインポート権限が無いことがあります。\
その場合は環境の管理者への確認が要ります。

## 利用条件（ライセンス）

| 対象 | ライセンス | できること |
|---|---|---|
| コード（フローZIP・`scripts/`・`.github/`・サイトのCSS/JS） | [MIT License](LICENSE) | 改変・再配布・業務での利用 |
| 教材（スライド・サイトの文章と図・アンケートの集計結果） | [CC BY-NC 4.0](LICENSE-CONTENT.md) | 出典を書けば、複製・改変・社内勉強会や研修での利用が可。販売は不可 |

いらすとやのイラスト、Microsoft 製品の画面やロゴ、参加者が書いたアンケートの自由記述は、どちらのライセンスの対象にも含めていません。\
詳しくは [LICENSE-CONTENT.md](LICENSE-CONTENT.md) にあります。

## リポジトリの構成

このリポジトリは GitHub Pages で公開サイトとしてそのまま配信しています。\
URLを変えないため、フォルダはサイトの階層と一致させています。

**講座の教材（誰でも使えるもの）**

| フォルダ | 中身 |
|---|---|
| [`slides/`](slides/) | 各回の講座スライド（`vol-NN/`）と技術Tipsスライドの一覧 |
| [`flows/`](flows/) | 各回のフローのZIP（`vol-NN/`） |
| [`sessions/`](sessions/) | 次回の案内と過去回のアーカイブ |
| [`videos/`](videos/) | 録画の一覧 |
| [`achievements/`](achievements/) | アンケート結果と活動の記録 |
| [`talks/`](talks/) | 外部イベントでの登壇資料 |
| [`start-here/`](start-here/)・[`method/`](method/)・[`about/`](about/) | 初参加ガイド、講座の設計、運営者の紹介 |
| [`assets/x/html/`](assets/x/html/) | 技術Tipsスライドの元HTML |

**サイトを動かす仕組み**

| フォルダ | 中身 |
|---|---|
| [`data/`](data/) | アンケート（`surveys/`）、活動記録（`activities/`）、集計結果（`insights.json`）など、サイトの数字の元データ |
| [`scripts/`](scripts/) | 集計・一覧ページ・この README を生成するスクリプト |
| [`.github/workflows/`](.github/workflows/) | 開催後の集計や一覧の更新を自動で回す GitHub Actions |

上記以外のフォルダ（`admin/` `tools/` `sites/` `articles/` `outputs/` など）は運営者の作業用・個人用で、講座の教材には含まれません。

---

この README は `scripts/build-readme.py` が `data/` から生成しています。\
数字は開催のたびに更新されます。\
Microsoft、Power Automate、Copilot Studio、Microsoft Teams、SharePoint は Microsoft Corporation の商標です。\
PA45 は個人が運営するコミュニティ講座で、Microsoft とは関係ありません。
