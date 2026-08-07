# PA45 ローカル自動更新
# ローカルの pa45-x-drafts.html（開催告知/Tips/ブログ等の下書きボード）と
# insights.json を、リポジトリ内の最新データから再生成する。
# Windows タスクスケジューラから毎日実行される想定。git push はしない（ローカル生成のみ）。

$ErrorActionPreference = "Continue"
$repo = "C:\Users\isamu\Documents\pa45"
$log  = Join-Path $repo "data\meta\refresh-x-board.log"
$stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Set-Location $repo

# python 実行ファイルを解決。
# WindowsApps のアプリ実行エイリアスはタスクスケジューラ(非対話)で解決できないことがあるため、
# 実体パッケージの python.exe をまず探し、無ければ PATH 上の python にフォールバックする。
$py = Get-ChildItem "C:\Users\isamu\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.*\python.exe" -ErrorAction SilentlyContinue |
      Select-Object -First 1 -ExpandProperty FullName
if (-not $py) { $py = (Get-Command python -ErrorAction SilentlyContinue).Source }
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue).Source }

"$stamp  refresh start (py=$py)" | Out-File -FilePath $log -Append -Encoding utf8

& $py "scripts\build-insights.py"  2>&1 | Out-File -FilePath $log -Append -Encoding utf8
& $py "scripts\build-x-board.py"   2>&1 | Out-File -FilePath $log -Append -Encoding utf8

"$stamp  refresh done" | Out-File -FilePath $log -Append -Encoding utf8
