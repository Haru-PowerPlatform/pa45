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

第1回（2026/03/06）〜第33回（2026/10/29）の集計です。

| 項目 | 値 |
|---|---|
| 開催回数 | 33回 |
| 延べ参加者 | 1,568名 |
| 1回あたりの参加者 | 平均 47.5名／最多 76名 |
| 参加者の推移 | 第1〜5回の平均 31.0名 → 直近5回の平均 68.4名 |
| アンケート回答 | 415件 |
| 理解度スコア（全回平均） | 88.3% |
| 役立ち度スコア（全回平均） | 91.9% |
| 録画を公開した回 | 30回 |
| 公開しているフローZIP | 23本 |
| 技術Tipsスライド | 177本 |

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

| 回 | 開催日 | テーマ | 参加 | スライド・資料 | フロー | 録画 | アンケート | レポート |
|---:|---|---|---:|:---:|:---:|:---:|:---:|:---:|
| 33 | 2026/10/29 | 内部名で困らない。内部名はフローが自動で調べる | 71名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-33/) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-33/PA45-Vol33-InternalNames.zip) | [見る](https://www.youtube.com/watch?v=eahDKL1qc98) | ― | ― |
| 32 | 2026/10/22 | 置くだけで月別フォルダに片付くファイル整理 | 67名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-32/) | ― | [見る](https://www.youtube.com/watch?v=JvyOqWzQt-U) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-32.html) | ― |
| 31 | 2026/10/15 | ファイルを選んで1クリックでPDFにして送る | 56名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-31/) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-31/PA45-Vol31-PdfSend.zip) | [見る](https://www.youtube.com/watch?v=-BgrN1pSsyo) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-31.html) | ― |
| 30 | 2026/10/08 | Teamsの頼まれごとを1クリックでTo Doに入れる | 76名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-30/) | ― | [見る](https://www.youtube.com/watch?v=wSEYs5TMeZY) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-30.html) | ― |
| 29 | 2026/10/01 | 動的コンテンツに出てこない値も、Copilotと一緒に式で取り出せるようになる | 72名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-29/) | ― | [見る](https://www.youtube.com/watch?v=a7dNYZq8K7k) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-29.html) | ― |
| 28 | 2026/09/17 | Copilotと通知カード1枚でまとめて完了にする | 61名 | [開く](https://haru-powerplatform.github.io/pa45/slides/vol-28/) | [ZIP](https://haru-powerplatform.github.io/pa45/flows/vol-28/PA45-Vol28-CardBulk.zip) | [見る](https://www.youtube.com/watch?v=aW_MSf5uvfg) | [結果](https://haru-powerplatform.github.io/pa45/achievements/insights/vol-28.html) | ― |
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
| 2026/09/05 | Power Platform Community で回答：Generative Answers が6つのナレッジのうち2つしか参照しない | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=b78f3d69-ef21-f111-8341-7ced8dcd2148) |
| 2026/09/10 | Power Platform Community で回答：フローをコピーできない（環境変数定義の読み取り権限） | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=ce8d1f71-b3aa-f111-aaac-7c1e520ce0ef) |
| 2026/09/11 | Power Platform Community で回答：SQL の server/database を環境変数で環境ごとに切り替えられるか | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=c4aabdcf-c4ad-f111-aaac-7c1e520ce2de) |
| 2026/09/12 | Power Platform Community で回答：Populate a Word Template で「doesn't contain template elements」 | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=e9ad2164-e7ad-f111-aaac-7ced8d1df5e7) |
| 2026/09/13 | Power Platform Community で回答：式の上限 131,072 文字は何に掛かるのか（実機検証） | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=987bd374-0bae-f111-aaac-00224834aaff) |
| 2026/09/13 | Power Platform Community で回答：PAD で並んだ矢印のうち正しい1つを安定してクリックしたい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=92c41d9b-e7ae-f111-aaac-00224834acc6) |
| 2026/09/15 | Power Platform Community で回答：Excel の Delete a row が No row was found になる | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=9f6690d1-0fb0-f111-aaac-000d3a54bc5d) |
| 2026/09/17 | Power Platform Community で回答：PAD で Outlook のフォルダーの添付を OneDrive に保存したい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=2e890072-fbb1-f111-aaac-70a8a58b23c2) |
| 2026/09/18 | Power Platform Community で回答：PAD コンソールに Premium 環境のフローが出ない | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=a001cb5b-dfb2-f111-aaac-00224834af37) |
| 2026/09/18 | Power Platform Community で回答：PAD の無人実行で OneDrive の同期が進まず Excel が開けない | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=daf866fc-69b2-f111-aaac-00224834cd63) |
| 2026/09/19 | 第57回 Microsoft 365 勉強会（Japan Microsoft 365 Users Group）で登壇：エージェントに渡す前に ── Power Automate で終わる仕事の見つけ方 | 登壇者 | オンライン勉強会 414名申込（connpass）・セッション50分 | [connpass](https://jpo365ug.connpass.com/event/405603/) |
| 2026/09/19 | Power Platform Community で回答：ファイル名の変更で拡張子がおかしくなる（substring とピリオド） | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=9c3e4e6a-12b3-f111-aaac-3833c5e85f91) |
| 2026/09/23 | Power Platform Community で回答：pac CLI で環境内の PCF コントロールを一覧したい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=aaa166a8-aeb6-f111-aaac-000d3a54bc5d) |
| 2026/09/24 | ビジュアルプログラミングIoTLT vol.24 でLT登壇：作らせる前に、使ってもらう ── 社内で非エンジニアにビジュアルプログラミングを教えた話 | 登壇 | オンラインLTイベント（YouTube配信） | [connpass](https://iotlt.connpass.com/event/400538/) ／ [レポート](https://www.automate136.com/iotlt-24-power-automate-node-red/) |
| 2026/09/25 | Power Platform Community で回答：Copilot Studio のテストパネルの会話は課金されるか | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=dee58f7a-b1b8-f111-aaac-3833c5e8602a) |
| 2026/09/26 | Power Platform Community で回答：pac CLI でソリューション外のアプリ・フローを移行したい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=ff112885-8bb8-f111-aaac-3833c5e85ffd) |
| 2026/09/28 | Power Platform Community で回答：退職者がオーナーのフローが動かなくなった | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=169e4e11-21bb-f111-aaaf-000d3a54b202) |
| 2026/09/29 | Power Platform Community で回答：Copilot Studio の SharePoint ナレッジに新しい文書が出てこない | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=c23261c0-bbbb-f111-aaaf-3833c5e85f5f) |
| 2026/09/29 | Power Platform Community で回答：SharePoint ナレッジが所有者には返り訪問者には返らない | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=e9a2ee05-57bb-f111-aaaf-3833c5e85f91) |
| 2026/10/01 | CUGJ_MEETUP Vol.22（Copilot User Group Japan）でLT登壇：答えるエージェントから、仕事を進めるエージェントへ ── エージェントフローで広がる Copilot Studio の使い道 | LT登壇 | オンラインLT 10分・参加50名（connpass） | [connpass](https://cugj.connpass.com/event/407194/) ／ [スライド](https://haru-powerplatform.github.io/pa45/talks/2026-10-01-cugj-lt/) |
| 2026/10/01 | Power Platform Community で回答：共有メールボックスのメールに移動しても切れないリンクを付けたい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=55d405ce-1ebd-f111-aaaf-00224834a8dc) |
| 2026/10/12 | Power Platform Community で回答：作成アクションでサムネイル画像の HTML リンクが作れない | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=99685483-82c3-f111-aaad-3833c5e8605a) |
| 2026/10/12 | Power Platform Community で回答：flowlog テーブル（エラスティック）を照会できない | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=2ae1ca81-fd86-f011-b4cb-7c1e527f8bbe) |
| 2026/10/12 | Power Platform Community で回答：OneDrive の Excel でスケジュール実行した Office スクリプトが効かない | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=e0a4a84e-b500-f111-8407-7ced8ddcc3f3) |
| 2026/10/12 | Power Platform Community で回答：レビュー期限まで30日超のファイルをメールで知らせたい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=75b785fa-67c2-f111-aaaf-3833c5e86001) |
| 2026/10/13 | Power Platform Community で回答：Copilot Studio の評価が24時間で20回までに制限される | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=59592d7e-2bc3-f111-aaaf-6045bdff210b) |
| 2026/10/13 | Power Platform Community で回答：オンプレミス SQL Server を Copilot Studio のナレッジに使うときのライセンス | 回答者 | Power Platform Community（公開・日本語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=929d1930-eac2-f111-aaad-3833c5e85f91) |
| 2026/10/13 | Power Platform Community で回答：共有メールボックスから送信すると Forbidden になる | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=de98eeb7-30c6-f111-aaaf-00224834c045) |
| 2026/10/14 | Power Platform Community で回答：Copilot でフローを作ろうとして空の条件エラーから抜けられない | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=9842efad-41c7-f111-aaad-3833c5e85f91) |
| 2026/10/14 | Power Platform Community で回答：GitHub Copilot ハーネスで Teams ユーザーの会話を自動でリセットしたい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=8eb720df-a8c7-f111-aaaf-6045bdff2b76) |
| 2026/10/14 | Power Platform Community で回答：Copilot Studio を単独で従量課金にしてエージェントを公開したい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=ca12d281-56c7-f111-aaad-00224834cd63) |
| 2026/10/14 | Power Platform Community で回答：Customer Voice のフォームからフローで質問文が取れない | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=4d749646-5ac7-f111-aaaf-7c1e520ce2de) |
| 2026/10/14 | Power Platform Community で回答：従量課金の環境ごとの上限と AI Builder・Copilot クレジットの扱い | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=6974ab07-42c7-f111-aaaf-3833c5e85fd8) |
| 2026/10/14 | Power Platform Community で回答：作成元 ID でトリガー条件を書きたい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=05098d12-b2c7-f111-aaaf-6045bdff210b) |
| 2026/10/16 | Power Platform Community で回答：Copilot Studio の1回の依頼で添付付きの下書きを20件以上作りたい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=5dc5c1f4-f6c7-f111-aaaf-7c1e520ce2de) |
| 2026/10/16 | Power Platform Community で回答：自動返信メールでフローが動かないようにしたい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=c441a7bd-9bc8-f111-aaaf-3833c5e86048) |
| 2026/10/17 | Power Platform Community で回答：Copilot クレジットがすぐ減ってしまう | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=f669bbb5-3cc9-f111-aaad-7c1e52017561) |
| 2026/10/17 | Power Platform Community で回答：メール本文に特定の文字列があるか判定できない | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=70e26622-a7c9-f111-aaaf-6045bdff2b76) |
| 2026/10/18 | Power Platform Community で回答：承認を開始して待機するとメールが2件目以降に送られない | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=5579ac53-60ca-f111-a05c-00224834c045) |
| 2026/10/18 | Power Platform Community で回答：Teams チャネルに貼られた画像をフローで送りたい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=e7fe1d16-63ca-f111-a05a-6045bdd73b92) |
| 2026/10/18 | Power Platform Community で回答：Teams のトランスクリプトを自動で取得するフローが失敗する | 回答者 | Power Platform Community（公開・日本語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=49224dad-36ca-f111-a05c-3833c5e85fd8) |
| 2026/10/19 | RPACommunity「Power Automate スペシャル！ライトニングトーク会」でLT登壇：講座の運営をクラウドフローで自動化した話 | LT登壇 | LT 10分・申込132名（connpass） | [connpass](https://rpacommunity.connpass.com/event/407193/) ／ [レポート](https://www.automate136.com/rpacommunity-lt-power-automate-koza-ops/) |
| 2026/10/20 | Power Platform Community で回答：AI Builder のプロンプト実行が CrossGeoFlagDisabled で失敗する | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=9be27d6d-a7ca-f111-a05c-7c1e520ce2de) |
| 2026/10/20 | Power Platform Community で回答：画面表示時にコレクションを作るときの注意 | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=4788ff99-71cc-f111-a05c-3833c5e86048) |
| 2026/10/20 | Power Platform Community で回答：Power Apps で2,000件超の関連レコードを欠けずに読み込みたい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=c610facb-8dcb-f111-a05a-3833c5e85c0e) |
| 2026/10/20 | Power Platform Community で回答：コピーを送信の機能が動かない | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=80a2de81-decb-f111-a05c-7c1e520ce2de) |
| 2026/10/21 | Power Platform Community で回答：去年のフォームとリスト用のフローを今年も使いたい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=0eefaa21-98cc-f111-a05a-3833c5e86001) |
| 2026/10/21 | Power Platform Community で回答：フローのエラー「dynamic conditions not met」 | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=4b22ebb9-ddcc-f111-a05c-6045bdff2b76) |
| 2026/10/21 | Power Platform Community で回答：ギャラリーの変更を SharePoint リストに書き戻したい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=4440323b-2ccd-f111-a05c-3833c5e859ac) |
| 2026/10/21 | Power Platform Community で回答：モデル駆動型アプリのビューのフィルターで結果が空になる | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=60ec3e7f-16cd-f111-a05c-3833c5e8602a) |
| 2026/10/21 | Power Platform Community で回答：Power Automate for desktop でフィルター後の最初の行を参照したい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=37308124-89cc-f111-a05a-3833c5e86001) |
| 2026/10/21 | Power Platform Community で回答：Power Apps で100を掛けると小数がずれる | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=69b0ab86-00cd-f111-a05a-3833c5e85ed9) |
| 2026/10/23 | Power Platform Community で回答：キャンバスアプリへの閲覧権限をまとめて付けたい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=5ceda7e7-3fce-f111-a05c-00224834c045) |
| 2026/10/24 | Power Platform Community で回答：送信済みアイテムから最新のメールを取りたい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=a95b21c7-cbce-f111-a05c-6045bdff2b76) |
| 2026/10/25 | Power Platform Community で回答：マルチセッション VM をマシングループで使いたい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=28e1f2cf-adcf-f111-a059-3833c5e8605a) |
| 2026/10/26 | Happy Low-Code【ゲスト回】で登壇：AIが画面を操作する時代に、PADが活躍できる場所 | ゲスト登壇 | オンライン登壇・申込81名（connpass） | [connpass](https://happylowcode.connpass.com/event/406298/) ／ [スライド](https://haru-powerplatform.github.io/pa45/talks/2026-10-26-happy-lowcode/) ／ [レポート](https://www.automate136.com/happy-lowcode-pad-vs-computer-use/) |
| 2026/10/27 | Power Platform Community で回答：埋め込んだ Copilot Studio エージェントの前に同意画面を出したい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=ff4db8b2-82d1-f111-a059-3833c5e85f91) |
| 2026/10/27 | Power Platform Community で回答：FlowRun テーブルで使われていないフローを見つけたい | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=23006b69-b2d1-f111-a05b-7c1e520ce0ef) |
| 2026/10/28 | Power Platform Community で回答：テナントをまたいでソリューションをインポートすると接続エラーになる | 回答者 | Power Platform Community（公開・英語） | [スレッド](https://community.powerplatform.com/forums/thread/details/?threadid=84bd5ce1-bad1-f111-a05b-00224834c045) |
| 2026/10/29 | Microsoft へ製品フィードバックを提出：Power Automate の実行履歴で、入力・出力の項目名をデザイナーと同じラベルにする改善要望 | 報告者 | Power Automate Ideas（公開・投票可） | [公開ページ](https://ideas.powerautomate.com/d365community/idea/fe3d5e56-58d3-f111-aad1-7c1e52b8b616) |
| 2026/10/29 | Microsoft へ製品フィードバック：Copilot Studio Evaluate で、範囲外の質問を正しく断っても 0%・失敗になる問題を既存アイデアに再現つきで追加 | 報告者 | Copilot Studio Ideas（公開・投票可） | [公開ページ](https://ideas.powervirtualagents.com/d365community/idea/98037dab-9da5-f111-85cd-6045bd856ac7) |

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
