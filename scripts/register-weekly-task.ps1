# PA45 ボード自動リフレッシュを Windows タスクスケジューラに登録（一度だけ実行）
#   実行: powershell -ExecutionPolicy Bypass -File scripts\register-weekly-task.ps1
# 毎朝08:00に weekly-board-refresh.ps1 を走らせる（PCが8時に落ちていても
# StartWhenAvailable で起動後に取りこぼしを拾う）。
# 新しい回が来たときだけOGP再生成＋pushし、毎回ボードを再ビルドする。

$taskName = "PA45 Board Refresh"
$script   = Join-Path $PSScriptRoot "weekly-board-refresh.ps1"

$action   = New-ScheduledTaskAction -Execute "powershell.exe" -Argument ("-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"{0}`"" -f $script)
$trigger  = New-ScheduledTaskTrigger -Daily -At ([datetime]"08:00")
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 20)
# 現在ユーザーで実行（-UserId 明示。省略すると環境により SID 解決に失敗する）
$principal = New-ScheduledTaskPrincipal -UserId (whoami) -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "PA45: 開催後に集計・アイキャッチOGP・X投稿ボードを自動で最新化" -Force | Out-Null

Write-Host "登録しました: タスク『$taskName』（毎朝08:00）"
Get-ScheduledTask -TaskName $taskName | Format-List TaskName, State
