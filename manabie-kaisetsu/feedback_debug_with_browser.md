---
name: マナビー解説サイト デバッグは実ブラウザ検証で
description: HTMLが壊れている指摘を受けたら、推測せず Chrome MCP で公開URLを開き JS で DOM 構造を直接確認する
type: feedback
originSessionId: a5f0d332-7a02-419d-8152-46dcc49d023e
---
# マナビー解説サイトのデバッグは実ブラウザ検証で

「壊れてる」「表示が変」と言われたら、ファイル監査だけで判断せず **Chrome MCP で公開URLを開いて JavaScript で実DOMを検査** する。

**Why:** 2026-05-14 のシールちょう表示崩れ事故で、最初に「ファイル監査では問題なし」と判定して報告したら、実は HTMLパース時に大量の孤児要素（`.panel` の外に出てしまった section / .question）が発生していた。ファイル上はインデントが揃っていても、`</div>` の数が合わないとブラウザが要素を予期せぬ位置に配置する。これはソース目視では見抜けない。

**How to apply:**
- iPadでの見え方を聞いた時点で **公開URL `https://haru-powerplatform.github.io/pa45/manabie-kaisetsu/?t={timestamp}`** を Chrome MCP で開く
- `?t=Date.now()` でキャッシュバイパス必須
- 検査クエリ例：
  - `document.querySelectorAll('.question').forEach(q => { if(!q.closest('.panel')) ... })` で孤児発見
  - `getComputedStyle(panel).display` で各 panel の実表示状態
  - `el.closest('.panel')?.id` で要素がどの panel 配下か
- 修正は物理HTMLリファクタが理想だが、構造ズレが多数（数十箇所）に及ぶ場合は **起動時の JS パッチで孤児を直前 panel に取り込む** 方が現実的・確実
- 起動JS で `document.body` と `.container` の両方の children を走査することを忘れない（panel直下に container が挟まるケースあり）