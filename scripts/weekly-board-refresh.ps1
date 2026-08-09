# PA45 ボード自動リフレッシュ（毎朝実行し、新しい回が来たときだけ本処理する）
# やること: 集計を最新化 →（新回検知時のみ）アイキャッチOGP13枚を再生成→push
#          → 毎回ローカルのX投稿ボード(pa45-x-drafts.html)を再ビルド。
# これで「講座が終わったら数字もOGPも全部最新」になる。
#
# 手動実行:  powershell -ExecutionPolicy Bypass -File scripts\weekly-board-refresh.ps1
# タスク登録: scripts\register-weekly-task.ps1 を一度実行（毎朝08:00・PC起動時）
#
# 数字は build-x-board.py が insights.json から流し込む（rotation.md はトークン {{N}} 等）。
# 別途、最新回のアンケートOGP(pa45-vol{N}-survey-ogp.png)と #36 差し替えだけは
# 回ごとの文言が要るので手動/AIで（reference_pa45_insights_pages 参照）。

$ErrorActionPreference = "Continue"
$repo = Split-Path -Parent $PSScriptRoot   # ...\Documents\pa45
$meta = Join-Path $repo "data\meta"
$log  = Join-Path $meta "weekly-refresh.log"
$stateFile = Join-Path $meta "last-refresh-sessions.txt"
New-Item -ItemType Directory -Force $meta | Out-Null
function Log($m){ $line = "{0}  {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $m; Add-Content -Path $log -Value $line -Encoding utf8; Write-Host $line }

Set-Location $repo
$env:PYTHONUTF8 = "1"
Log "=== refresh 開始 ==="

# 1) リモートの最新（CIのparse-survey/build-insightsの結果）を取り込む
git pull --rebase --autostash origin main 2>&1 | ForEach-Object { Log "pull: $_" }

# 2) 集計を念のため再生成（CI未実行でも最新化）
python scripts\build-insights.py 2>&1 | ForEach-Object { Log "insights: $_" }

# 3) 集計値に変化があったか判定（開催回数だけでなく、回答増や%変化も拾う。
#    遅れて届くアンケート回答で件数・割合が変わっても最新化するため）
$sig = (python -c "import json;s=json.load(open(r'$repo\data\insights.json',encoding='utf-8'))['summary'];print('|'.join(str(s.get(k)) for k in ['sessions','participants_total','responses_total','understanding_avg','usefulness_avg','participants_max','participants_avg','archive_videos']))").Trim()
$prev = if (Test-Path $stateFile) { (Get-Content $stateFile -Raw).Trim() } else { "" }
Log "集計: 今回=$sig / 前回=$prev"

if ($sig -ne $prev) {
  Log "集計に変化を検知 → OGP再生成＋push"
  # 4) アイキャッチOGP 13枚を再生成（ヘッドレスChrome）
  python scripts\make-insight-ogp.py 2>&1 | ForEach-Object { Log "ogp: $_" }
  # 5) 変更があれば push（GitHub PagesにOGPを反映＝Xカードが最新絵になる）
  git add data\insights.json assets\ogp\*.png data\surveys\*.json 2>&1 | Out-Null
  if (git status --porcelain data\insights.json assets\ogp\*.png data\surveys\*.json) {
    git commit -m "auto: 集計・アイキャッチOGPを最新化" 2>&1 | ForEach-Object { Log "commit: $_" }
    git push origin HEAD 2>&1 | ForEach-Object { Log "push: $_" }
  } else { Log "OGPに差分なし" }
  Set-Content -Path $stateFile -Value $sig -Encoding utf8
} else {
  Log "集計に変化なし → OGP再生成はスキップ"
}

# 6) ローカルのX投稿ボードを毎回再ビルド（数字はinsights.jsonから流し込み）
python scripts\build-x-board.py 2>&1 | ForEach-Object { Log "board: $_" }

Log "=== 完了 ==="
