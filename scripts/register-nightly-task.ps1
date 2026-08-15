# PA45 公開サイトの毎晩の自動更新を Windows タスクスケジューラに登録（一度だけ実行）
#   実行: powershell -ExecutionPolicy Bypass -File scripts\register-nightly-task.ps1
# 毎晩23:30に nightly-site-refresh.ps1 を走らせる。
# PCが23:30に落ちていても StartWhenAvailable で起動後に取りこぼしを拾う。

$taskName = "PA45 Nightly Site Refresh"
$script   = Join-Path $PSScriptRoot "nightly-site-refresh.ps1"

$action    = New-ScheduledTaskAction -Execute "powershell.exe" -Argument ("-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"{0}`"" -f $script)
$trigger   = New-ScheduledTaskTrigger -Daily -At ([datetime]"23:30")
# バッテリー駆動でも実行する。既定（DisallowStartIfOnBatteries=True）のままだと
# ノートPCを電源に挿していない夜はタスクが Queued のまま走らない。
$settings  = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 30) `
             -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
# 現在ユーザーで実行（-UserId 明示。省略すると環境により SID 解決に失敗する）
$principal = New-ScheduledTaskPrincipal -UserId (whoami) -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "PA45: 公開サイトの生成物（スライド一覧・録画リンク・集計・OGP）を毎晩まとめて最新化しpush" -Force | Out-Null

Write-Host "登録しました: タスク『$taskName』（毎晩23:30）"
Get-ScheduledTask -TaskName $taskName | Format-List TaskName, State
