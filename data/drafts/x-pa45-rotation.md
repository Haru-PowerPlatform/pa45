# X投稿ローテーション在庫 — PA45の蓄積を切り口別に回す（2026-07 作成）

募集ばかりにならないように、実績・アンケート・動画・スライド・設計思想を順番に回すための在庫。
すべてリンク先ページに専用OGPを用意済みなので、貼るとアイキャッチ付きのカードが出る。
文字数はXの重み付き280が上限（日本語=2・半角=1・URL=23）。ハッシュタグは1個。投稿ボタンははる本人が押す。
ボード（`python scripts/build-x-board.py` → Documents\pa45-x-drafts.html）から数クリックで下書きにできる。

| # | 切り口 | リンク先 | OGP |
|---|---|---|---|
| 1 | 累計実績 | achievements/insights/ | insights-numbers.png |
| 2 | できるようになったこと | insights/can-do.html | insights-can-do.png |
| 3 | 苦手が消えた声 | insights/voices.html | insights-voices.png |
| 4 | 時間の設計 | insights/design.html | insights-design.png |
| 5 | アンケート全回公開 | achievements/survey.html | og-survey.png |
| 6 | 活動の記録 | achievements/ | og-achievements.png |
| 7 | 要望→第16回 Copilot | youtu.be（第16回） | YouTube |
| 8 | 要望→第18回 承認 | youtu.be（第18回） | YouTube |
| 9 | 「45分では足りない」→スライド常設 | slides/ | og-slides.png |
| 10 | 「JSONが無理」→第14回 | youtu.be（第14回） | YouTube |
| 11 | 動画アーカイブ{{VID}}本 | videos/ | og-videos.png |
| 12 | 実行履歴の読み方（第11回） | youtu.be（第11回） | YouTube |
| 13 | スライド全{{N}}回 | slides/ | og-slides.png |
| 14 | 初参加ガイド | start-here/ | og-start-here.png |
| 15 | 参加者はこんな感じ | achievements/insights/ | insights-numbers.png |
| 16 | 次回募集 | sessions/ | og-sessions.png |
| 17 | 講座の設計思想 | method/ | og-method.png |
| 18 | 登壇・LT資料 | talks/ | og-talks.png |
| 19 | 伸びた回＝AI・JSON | achievements/insights/ | insights-numbers.png |
| 20 | いちばん難しかった回 | achievements/survey.html | og-survey.png |
| 21 | {{N}}回で扱ったアクション | achievements/insights/ | insights-numbers.png |
| 22 | 見るだけ参加が普通にいる | start-here/ | og-start-here.png |
| 23 | 上司にすすめられて来る人 | start-here/ | og-start-here.png |
| 24 | 教える側の人も来ている | method/ | og-method.png |
| 25 | 資格勉強の人が手を動かしに来る | videos/ | og-videos.png |
| 26 | 職場に持ち帰ってくれた人 | insights/voices.html | insights-voices.png |
| 27 | たとえ話で押し切る回 | youtu.be（第5回） | YouTube |
| 28 | アクションの命名ルール | method/ | og-method.png |
| 29 | 詰め込んだ回は理解度が落ちた | insights/design.html | insights-design.png |
| 30 | 英語表記を併記している理由 | method/ | og-method.png |
| 31 | {{N}}回、毎週ひとりで回している | achievements/ | og-achievements.png |
| 32 | アンケートを取り続ける理由 | achievements/survey.html | og-survey.png |
| 33 | 全部無料・登録なし | slides/ | og-slides.png |
| 34 | どこで知って来たのか | sessions/ | og-sessions.png |
| 35 | {{N}}回の積み上げ方（3段階） | videos/ | og-videos.png |
| 36 | 第23回アンケート結果 | achievements/vol-23-survey.html | pa45-vol23-survey-ogp.png |

---

## 1. 累計実績
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

PA45、{{N}}回でのべ{{PT}}名の方に参加してもらえました。ありがとうございます。

アンケート{{RT}}件で「内容が理解できた」{{UND}}%、「業務に役立ちそう」{{USE}}%でした。参加者数の推移と全{{N}}回のテーマをまとめています。

https://haru-powerplatform.github.io/pa45/achievements/insights/
```

## 2. できるようになったこと
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

アンケートの「できるようになったこと」を{{N}}回分あわせてみました。

・アクションの意味が分かった 77.3%
・自分で使えるようになった 40.3%

45分で届くのはこのあたりまで、が正直なところです。

https://haru-powerplatform.github.io/pa45/achievements/insights/can-do.html
```

## 3. 苦手が消えた声
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【苦手だった人の声】

「JSONはよく分からないなぁっと勝手に苦手意識を持っていましたが」

PA45のアンケートにあった声です。JSON・式・実行履歴でつまずいた人が、そのあとどう書いてくれたか。{{RT}}件から集めました。

https://haru-powerplatform.github.io/pa45/achievements/insights/voices.html
```

## 4. 時間の設計
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【なぜ45分・木曜20:15か】

PA45を45分・木曜20:15でやっている理由を書いてみました。

希望時間を毎回聞いていて、{{RT}}件中{{TIME}}%が20:15〜21:00でした。「前編・後編に分けても」という声もあって、それも載せています。

https://haru-powerplatform.github.io/pa45/achievements/insights/design.html
```

## 5. アンケート全回公開
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

PA45は毎回アンケートを取って、結果はそのままサイトに出しています。

理解度・役立ち度のスコアと、コメントの原文。「少し難しかった」も隠さず残しています。第1回から第{{N}}回まで、回ごとに見られます。

https://haru-powerplatform.github.io/pa45/achievements/survey.html
```

## 6. 活動の記録
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【活動の記録】

PA45がこれまでやってきたことを、1ページにまとめました。

{{N}}回の開催、のべ{{PT}}名、アンケート{{RT}}件、登壇や記事も。数字も参加者の声も、そのまま置いています。

https://haru-powerplatform.github.io/pa45/achievements/
```

## 7. 要望→第16回 Copilot
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【第16回・Copilotで直す】

第12回のアンケートで「Copilotで作ると何が違うのか知りたい」という声をもらいました。

第16回でそこをやってみました。フローをCopilotに読ませて直していく流れです。録画はこちらです。

https://youtu.be/dVM-WF1A79g
```

## 8. 要望→第18回 承認
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【第18回・承認の催促】

第8回のアンケートで「承認や連続承認が難しくて、勉強したい」という声をもらいました。

第18回はそこを掘って、放置された承認をフローが催促して上に上げる回にしてみました。録画はこちらです。

https://youtu.be/cghp6TOJfw8
```

## 9. 「45分では足りない」→スライド常設
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

「45分に収まらないですね」「前編・後編でもいいかも」という声を毎回もらいます。

45分の枠は動かさない代わりに、解説スライドを全{{N}}回分そのまま置くことにしました。あとから同じ手順をたどれます。

https://haru-powerplatform.github.io/pa45/slides/
```

## 10. 「JSONが無理」→第14回
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【第14回・JSONだけ】

「英語とJSONを見ると、無理！と拒否反応が出てしまい」

第11回のアンケートにあった声です。第14回はJSONの読み方だけに絞ってやりました。録画を置いています。

https://youtu.be/9fkbQmOR6Fo
```

## 11. 動画アーカイブ{{VID}}本
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【録画アーカイブ{{VID}}本】

PA45の過去回の録画を{{VID}}本公開しています。

承認・Forms連携・通知・JSON・Copilotなど。気になるテーマの回だけ、その場で再生できます。1本45分です。

https://haru-powerplatform.github.io/pa45/videos/
```

## 12. 実行履歴の読み方（第11回）
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【第11回・実行履歴の読み方】

フローが失敗したとき、どこを見ればいいか分からない。そんな回でした。

第11回は実行履歴の読み方だけをやりました。「出力結果の存在を初めて知りました」という声が多かったです。

https://youtu.be/0Wvv6Bf3n18
```

## 13. スライド全{{N}}回
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【スライド全{{N}}回公開】

PA45で使った解説スライドを、全{{N}}回分そのまま公開しています。

登録もログインも要りません。動画と合わせて使うと、その場で追いつけなかったところを埋められます。

https://haru-powerplatform.github.io/pa45/slides/
```

## 14. 初参加ガイド
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【初参加ガイド】

PA45に初めて来る人向けに、必要なもの・当日の流れ・つまずいたときの逃げ道をまとめました。

カメラもマイクもオフで大丈夫。質問しなくても平気です。見るだけの参加もふつうにいるので、気軽にどうぞ。

https://haru-powerplatform.github.io/pa45/start-here/
```

## 15. 参加者はこんな感じ
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【参加者はこんな人たち】

PA45の参加者は、1回あたり平均{{AVGI}}名、多い回で{{MAX}}名でした。

「Power Automateをさわったことがない」から来る人が中心です。{{N}}回分の推移と、テーマごとの人数を出しています。

https://haru-powerplatform.github.io/pa45/achievements/insights/
```

## 16. 次回募集
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【今週木曜・参加募集】

今週木曜20:15から、PA45をやります。45分だけ、一緒に手を動かす回です。

初参加歓迎、見るだけでも大丈夫です。過去{{N}}回の録画とスライドも置いてあるので、よかったら。

https://haru-powerplatform.github.io/pa45/sessions/
```
※開催前日〜当日に投稿する用。connpassのURLに差し替えてもいい。

## 17. 講座の設計思想
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【1回1テーマにする理由】

PA45は1回で1つしか扱いません。45分に詰め込まないほうが、そのあと手が動くからです。

なぜ45分か、なぜ1回1粒か。設計の話を書いてみました。

https://haru-powerplatform.github.io/pa45/method/
```

## 18. 登壇・LT資料
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【登壇・LT資料】

PA45の外でも、ときどき話しています。

なんでもCopilotや、広島のPower Platform勉強会で発表したLT資料を置いています。そのまま使ってもらってかまいません。

https://haru-powerplatform.github.io/pa45/talks/
```

## 19. 伸びた回＝AI・JSON
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【人が集まった回】

PA45で人が多かったのは、第22回76名、第21回59名、第17回51名でした。

Excelの手作業を自動化する回と、最初の一歩をまるごと復習する回。「いま詰まっているところ」の回に、人が集まるようです。

https://haru-powerplatform.github.io/pa45/achievements/insights/
```

## 20. いちばん難しかった回
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

{{N}}回のうち、理解度がいちばん低かったのは第12回の「式」で72.7%でした。

日数計算を扱った回で「難しかったです（笑）」というコメントも来ました。うまくいかなかった回も、数字のまま置いています。

https://haru-powerplatform.github.io/pa45/achievements/survey.html
```

## 21. {{N}}回で扱ったアクション
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

PA45の{{N}}回で扱ってきたものを並べてみました。

変数／条件分岐／Apply to each／Forms連携／SharePoint登録／承認／Teams通知／実行履歴／式／Try-Catch／JSON／スケジュール／Copilot／見える化／アダプティブカード／Officeスクリプト

一覧はこちらです。

https://haru-powerplatform.github.io/pa45/achievements/insights/
```

## 22. 見るだけ参加が普通にいる
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

PA45には「見るだけ参加」の人がふつうにいます。

会社PCの制限で操作できない、帰宅途中で音声だけ、私物PCにライセンスがない。そのまま見てもらって大丈夫です。あとで録画とスライドで手を動かせます。

https://haru-powerplatform.github.io/pa45/start-here/
```

## 23. 上司にすすめられて来る人
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

「会社の上司に進められて、視聴させて頂きました。すごく苦手意識が強かったですが、少しずつ触れる勇気がでました」

自分から来た人ばかりではありません。すすめられて来た人でも続けられるといいなと思って作っています。

https://haru-powerplatform.github.io/pa45/start-here/
```

## 24. 教える側の人も来ている
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

PA45には、社内でPower Automateを教える側の人も来てくれます。

「初心者に教えるときの参考になった」と言ってもらえたことがあって、それ以来、つまずく場所の見せ方を意識するようになりました。

https://haru-powerplatform.github.io/pa45/method/
```

## 25. 資格勉強の人が手を動かしに来る
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

「PL-900の試験勉強中なのですが、PA45のハンズオンをしているとイメージが掴みやすい」

資格の勉強と手を動かすのは、セットにすると早いようです。録画が{{VID}}本あるので、出てきた用語をその場で触って確かめられます。

https://haru-powerplatform.github.io/pa45/videos/
```

## 26. 職場に持ち帰ってくれた人
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

「職場で試したところ、送った中の一人が興味を持ってくださったので、PA45も紹介させていただきました」

こういう話がいちばん嬉しいです。1人が持ち帰ってくれると、その職場でもう1人増えます。

https://haru-powerplatform.github.io/pa45/achievements/insights/voices.html
```

## 27. たとえ話で押し切る回
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【たとえ話で覚える】

条件分岐を「面接おじさん」、繰り返しを「大根の輪切り」でたとえた回があります。

用語で分からないなら、絵で分かればいい。そう思って、たとえ話を多めにしています。よかったら見てみてください。

https://youtu.be/cltHw91fYm4
```

## 28. アクションの命名ルール
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【アクションの命名ルール】

PA45ではアクション名を「既定名 - 一言説明」に書き換えています。既定名を消さないのがポイントです。

半年後の自分が読めるようになります。地味だけど効く小ネタです。

https://haru-powerplatform.github.io/pa45/method/
```

## 29. 詰め込んだ回は理解度が落ちた
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【詰め込むと理解度が落ちる】

{{N}}回やってみて分かったのは、詰め込んだ回ほど理解度が落ちる、ということでした。

式を扱った第12回は72.7%。1つに絞った回は9割を超えます。だから45分で1つしか扱わないようにしています。

https://haru-powerplatform.github.io/pa45/achievements/insights/design.html
```

## 30. 英語表記を併記している理由
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【英語表記を併記する理由】

PA45のスライドは、アクション名に英語表記も併記しています。

「耳を慣らすトレーニングになる」と言ってもらえて、続けています。日本語UIと英語の情報がズレたときにも効きます。

https://haru-powerplatform.github.io/pa45/method/
```

## 31. {{N}}回、毎週ひとりで回している
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

PA45は毎週木曜、スライドを作って、実機で通して、当日進行して、アンケートを集計して録画を出す、という流れでやっています。

{{N}}回続けてきました。ひとりでやっているぶん、毎回ちょっとずつやり方を見直しています。

https://haru-powerplatform.github.io/pa45/achievements/
```

## 32. アンケートを取り続ける理由
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【アンケートを取り続ける理由】

PA45は{{N}}回すべてでアンケートを取っていて、{{RT}}件たまりました。

理解度が落ちた回は、次の回の作りを変えています。声を読むためというより、次を直すために取っている感じです。

https://haru-powerplatform.github.io/pa45/achievements/survey.html
```

## 33. 全部無料・登録なし
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

【全部無料・登録なし】

PA45は参加無料で、スライドも録画も登録なしで見られます。

会社のPCでは開けない、ログインを増やしたくない、という人がいるからです。リンクを踏めばそのまま読めます。

https://haru-powerplatform.github.io/pa45/slides/
```

## 34. どこで知って来たのか
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

PA45を知ったきっかけで多いのは、Xとconnpass、それと他のコミュニティです。

「一歩をフミダセTVで知りました」「なんでもCopilot大阪で知りました」という人が実際に来てくれています。次回はこちらです。

https://haru-powerplatform.github.io/pa45/sessions/
```

## 35. {{N}}回の積み上げ方
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

PA45の{{N}}回は、3段階で積んできました。

第1〜5回で変数・条件・繰り返し。第6〜10回でForms・SharePoint・承認・Teams。第11回以降は実行履歴や式など、つまずきやすいところ。

録画はどこからでも見られます。

https://haru-powerplatform.github.io/pa45/videos/
```

## 36. 第23回アンケート結果
```
【#PowerAutomate 45分ハンズオン講座＝PA45】

第23回のアンケート結果です。Officeスクリプトの戻り値で、フローを振り分ける回。

15名回答で、理解できた92%、役立ちそう83%。「今まで扱ったことが無いフロー」という声も。コメントはそのまま載せています。

https://haru-powerplatform.github.io/pa45/achievements/vol-23-survey.html
```
※開催直後に出す用。回ごとの単発なので、次の回が終わったら差し替えていく。

---

### 回し方のメモ
- 週2本くらい。35本あるので、同じネタが回ってくるのは約4ヶ月後。
- **同じ系統を続けない**。系統は6つ：
  データ（1・2・4・15・19・20・21・29）／声（3・26）／
  記録の公開（5・6・32・33）／動画・スライド（9・11・12・13・35）／
  入口（14・16・22・23・34）／設計と裏側（7・8・10・17・18・24・25・27・28・30・31）
- 例：データ → 動画 → 声 → 入口 → 設計 → 記録 の順で回すと重ならない。
- 開催週は 16（募集）を必ず入れて、それ以外の日に在庫を消化する。
- 新しい回が終わったら `python scripts/build-insights.py` → `python scripts/make-insight-ogp.py` を回す。
  数字が変わるので、1・2・4・15の本文の数値も更新する。
- 回別アンケート（36）は `python scripts/parse-survey.py` → `achievements/vol-N-survey.html` を前回分からコピーして差し替え →
  `python scripts/make-vol-survey-ogp.py N`（見出し・引用は同スクリプトの `VOL_TEXT` に足す）。
- OGPカードが古いまま出るときは https://cards-dev.twitter.com/validator でキャッシュを更新。
