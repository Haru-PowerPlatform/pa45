# PA45 命名ルール（重要・絶対遵守）

このドキュメントは PA45 のフロー・Solution・GitHub上のZIPファイル名の整合性を保つためのルール集。
**新Vol追加時はこのドキュメントを必ず確認すること**。

---

## 1. Solution 命名（Power Automate）

### 1-1. 表示名（自由）
- 例：`PA45 No.10 Forms→Teams`
- 日本語・記号OK

### 1-2. 名前（厳密ルール）
- 形式：`PA45_NoN_TopicXxx`
- 半角英数 + アンダースコア（`_`）のみ
- `P` は大文字（`pa45_...` ではなく `PA45_...`）
- `N` は1〜2桁の数字
- `TopicXxx` は CamelCase の英単語（短縮可）

### 1-3. 実体（UniqueName）
Power Platform は `名前` の `_` を自動削除する。
- 入力：`PA45_No10_FormsTeams`
- 実体：`PA45No10FormsTeams` ← `pac CLI` で参照する名前

---

## 2. フロー命名（マイフロー / Solution内）

- 形式：`PA45-No{N}-{Topic}`
- 例：`PA45-No10-FormsTeams`
- ハイフン区切り。日本語OKだがツール連携で表記ゆれ防止のため英語推奨

---

## 3. トピック語彙（標準形）

新Volを追加するときは以下の規則で `Topic` 部分を決める：

| 推奨 | 用途 |
|---|---|
| `Initialize` | 変数の初期化 |
| `SetVariable` | 変数の設定 |
| `Condition` | 条件分岐 |
| `ApplyToEach` | 繰り返し |
| `Review` | 復習回 |
| `FormsMail` | Forms→メール |
| `FormsSPTeams` | Forms→SharePoint→Teams |
| `Approval` | 承認フロー |
| `SharePointUpdate` | SharePoint更新検知 |

**新規追加時のルール**：
- 英単語の連結（`SchedulePost`、`HttpRequest` など）
- 既存のトピック名と重複しない
- スペース・記号・日本語禁止

---

## 4. GitHub内のZIP命名（自動）

`scripts/import-flow-zip.py` が以下の規則で配置：
```
flows/vol-{NN}/PA45-Vol{NN}-{Topic}.zip
```

`{NN}` は2桁ゼロパディング（`vol-09`）、`{Topic}` は `import-flow-zip.py` の `VOL_TOPIC` マッピングから取得。

---

## 5. 命名ミスを検出する

### 5-1. 検証スクリプト
新Vol追加後、または `release-flow.bat` 実行前にチェック：
```powershell
python scripts/check-naming.py
```

不整合を検出したら具体的な対処を表示する。

### 5-2. 自動同期スクリプト
新Vol追加時はこれを使えば、`release-flow.bat` と `import-flow-zip.py` のマッピングが自動更新される（手で書かない）：
```powershell
python scripts/add-vol-card.py --vol 10 --topic FormsTeams \
    --title "Forms→Teams通知" --date "2026-05-14" \
    --participants 30 --pptx P010_PA45_FormsTeams_20260514.pptx \
    --solution-name PA45No10FormsTeams \
    --blog-slug pa45-vol10-forms-teams
```

---

## 6. 既存のVolマッピング（参考）

| Vol | 入力名 | 実体（UniqueName） | flows/トピック |
|---|---|---|---|
| 1 | PA45_No1_Initialize | PA45No1Initialize | InitializeVariable |
| 2 | PA45_No2_SetVariable | PA45No2SetVariable | SetVariable |
| 3 | PA45_No3_Condition | PA45No3Condition | Condition |
| 4 | PA45_No4_ApplyToEach | PA45No4ApplyToEach | ApplyToEach |
| 5 | PA45_No5_Review | PA45No5Review | Review |
| 6 | PA45_No6_FormsMail | PA45No6FormsMail | FormsMail |
| 7 | PA45_No7_FormsSPTeams | PA45No7FormsSPTeams | FormsSPTeams |
| 8 | PA45_No8_Approval | PA45No8Approval | ApprovalFlow |
| 9 | PA45_No9_SharePointUpdate | PA45No9SharePointUpdate | SharePointUpdate |

---

## 7. 日常運用フロー（チェックリスト）

### 既存Vol のフロー更新
1. PA で対象Solution内のフローを編集・保存
2. `python scripts/check-naming.py` で命名OK確認
3. `.\scripts\release-flow.bat all` で全Vol一括同期（推奨）
   - または `.\scripts\release-flow.bat 9` で対象Volだけ

### 新Vol（Vol.10〜）の追加
1. **PA で Solution 作成**
   - 表示名：`PA45 No.10 Topic`
   - 名前：`PA45_No10_TopicXxx`
   - 公開元：PA45
2. **フローを Solution に追加**
   - + 既存追加 → クラウドフロー → Dataverseの外
3. **サイト側マッピング更新**（自動同期）
   ```powershell
   python scripts/add-vol-card.py --vol 10 --topic TopicXxx ...
   ```
4. **検証**
   ```powershell
   python scripts/check-naming.py
   ```
5. **エクスポート＆反映**
   ```powershell
   .\scripts\release-flow.bat 10
   ```

---

## 8. CLAUDE.md にも記録

このルールは `CLAUDE.md` の「PA45 命名ルール」セクションに簡略版を記載。
変更する場合は両方更新すること。
