# PA45 公開サイト 毎晩の自動最新化（タスク「PA45 Nightly Site Refresh」毎晩23:30）
# やること:
#   1) リモートを取り込む（git pull --rebase --autostash）
#   2) 生成物を作り直す
#        build-insights.py       → data/insights.json（achievements/insights/ が読む）
#        build-slides-gallery.py → slides/index.html（Xスライドのギャラリー）
#        sync-youtube-links.py   → sessions/index.html（録画リンクを追加）
#   3) 集計値が前回と変わったときだけ make-insight-ogp.py でOGP13枚を再生成
#   4) 生成物のパスだけを commit → push（GitHub Pages に反映＝サイトが最新になる）
#   5) ローカルのX投稿ボード pa45-x-drafts.html を再ビルド（pushしない）
#
# 手動実行: powershell -ExecutionPolicy Bypass -File scripts\nightly-site-refresh.ps1
# タスク登録: scripts\register-nightly-task.ps1 を一度だけ実行
#
# 安全側の作り:
#   - 他のClaudeセッションが pa45 を編集中（ロックが5分以内に更新）なら何もせず終わる
#   - merge/rebase の途中なら git を触らず、生成だけして終わる
#   - commit は生成物のパス限定。他セッションの作業中ファイルを巻き込まない
#   - git add に assets\ogp\*.png のワイルドカードは使わない（無関係な画像が入る）

$ErrorActionPreference = "Continue"
$repo      = Split-Path -Parent $PSScriptRoot   # ...\Documents\pa45
$meta      = Join-Path $repo "data\meta"
$log       = Join-Path $meta "nightly-site-refresh.log"
$stateFile = Join-Path $meta "last-refresh-sessions.txt"
$lockDir   = "C:\Users\isamu\.claude\locks"
$lockFile  = Join-Path $lockDir "pa45.lock"

New-Item -ItemType Directory -Force $meta | Out-Null
function Log($m) {
  $line = "{0}  {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $m
  Add-Content -Path $log -Value $line -Encoding utf8
  Write-Host $line
}

# python の実体を解決する。WindowsApps の実行エイリアスは
# タスクスケジューラ（非対話）から解決できないことがある。
$py = Get-ChildItem "C:\Users\isamu\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.*\python.exe" -ErrorAction SilentlyContinue |
      Select-Object -First 1 -ExpandProperty FullName
if (-not $py) { $py = (Get-Command python -ErrorAction SilentlyContinue).Source }
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue).Source }

Set-Location $repo
$env:PYTHONUTF8 = "1"
Log "=== nightly 開始 (py=$py) ==="

if (-not $py) { Log "python が見つからない → 中止"; exit 1 }

# 0) 他セッションが編集中なら触らない（feedback_multi_session_lock の5分ルール）
if (Test-Path $lockFile) {
  $age = ((Get-Date) - (Get-Item $lockFile).LastWriteTime).TotalMinutes
  if ($age -lt 5) {
    Log ("別セッションが pa45 を編集中（lock {0:N1}分前）→ 今夜はスキップ" -f $age)
    exit 0
  }
  Log ("古いロックを検出（{0:N1}分前）→ 引き継ぐ" -f $age)
}
New-Item -ItemType Directory -Force $lockDir | Out-Null
$lockBody = '{"pid":"nightly-site-refresh","ts":"' + (Get-Date).ToUniversalTime().ToString("s") + 'Z","task":"nightly site refresh"}'
Set-Content -Path $lockFile -Value $lockBody -Encoding ascii

try {
  # 1) リモートの最新（CIの parse-survey / activities index など）を取り込む
  $gitBusy = (Test-Path (Join-Path $repo ".git\MERGE_HEAD")) -or
             (Test-Path (Join-Path $repo ".git\rebase-merge")) -or
             (Test-Path (Join-Path $repo ".git\rebase-apply"))
  if ($gitBusy) {
    Log "merge/rebase の途中 → git 操作はスキップ（生成だけ行う）"
  } else {
    git pull --rebase --autostash origin main 2>&1 | ForEach-Object { Log "pull: $_" }
  }

  # 2) 生成物を作り直す
  & $py "scripts\build-insights.py"       2>&1 | ForEach-Object { Log "insights: $_" }
  & $py "scripts\build-slides-gallery.py" 2>&1 | ForEach-Object { Log "slides: $_" }
  & $py "scripts\sync-youtube-links.py"   2>&1 | ForEach-Object { Log "youtube: $_" }

  # 3) 集計値に変化があったときだけOGPを作り直す（ヘッドレスChromeで重いため）
  $sig = (& $py -c "import json;s=json.load(open(r'$repo\data\insights.json',encoding='utf-8'))['summary'];print('|'.join(str(s.get(k)) for k in ['sessions','participants_total','responses_total','understanding_avg','usefulness_avg','participants_max','participants_avg','archive_videos']))").Trim()
  $prev = ""
  if (Test-Path $stateFile) { $prev = (Get-Content $stateFile -Raw).Trim() }
  Log "集計: 今回=$sig / 前回=$prev"
  if ($sig -ne "" -and $sig -ne $prev) {
    Log "集計に変化を検知 → OGP13枚を再生成"
    & $py "scripts\make-insight-ogp.py" 2>&1 | ForEach-Object { Log "ogp: $_" }
    Set-Content -Path $stateFile -Value $sig -Encoding utf8
  } else {
    Log "集計に変化なし → OGP再生成はスキップ"
  }

  # 4) 生成物のパス限定で commit → push
  if ($gitBusy) {
    Log "merge/rebase の途中 → commit/push はスキップ"
  } else {
    $paths = @(
      "data\insights.json",
      "slides\index.html",
      "sessions\index.html",
      "assets\ogp\insights-*.png",
      "assets\ogp\og-*.png"
    )
    git add -- $paths 2>&1 | Out-Null
    $staged = (git diff --cached --name-only -- $paths | Out-String).Trim()
    if ($staged -ne "") {
      Log ("commit 対象: " + ($staged -replace "\r?\n", " / "))
      (git commit -m "auto: サイトを最新化（スライド一覧・録画リンク・集計/OGP）" -- $paths 2>&1) | ForEach-Object { Log "commit: $_" }
      (git push origin HEAD 2>&1) | ForEach-Object { Log "push: $_" }
    } else {
      Log "サイト側に差分なし → commit しない"
    }
  }

  # 5) ローカルのX投稿ボード（repo外・pushしない）
  #    先にブログの投稿状況を取り直してからボードを組む（ブログタブが古くならない）
  & $py "scripts\fetch-blog-status.py" 2>&1 | ForEach-Object { Log "blog: $_" }
  & $py "scripts\build-x-board.py"     2>&1 | ForEach-Object { Log "board: $_" }
}
finally {
  Remove-Item $lockFile -Force -ErrorAction SilentlyContinue
  Log "=== 完了 ==="
  # ログが伸び続けないよう直近2000行だけ残す
  if (Test-Path $log) {
    $lines = Get-Content $log
    if ($lines.Count -gt 2000) { $lines[-2000..-1] | Set-Content -Path $log -Encoding utf8 }
  }
}
