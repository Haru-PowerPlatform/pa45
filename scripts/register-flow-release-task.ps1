# PA45 フローZIP 自動リリースを Windows タスクスケジューラに登録（一度だけ実行）
#   実行: powershell -ExecutionPolicy Bypass -File scripts\register-flow-release-task.ps1
# 毎週木曜21:30（講座の直後）に release-flow.bat all を走らせ、
# Power Automate のソリューションをエクスポート → flows/ に配置 → commit/push する。
#
# 2026-08-15に既存タスクの設定を作り直した。旧設定は
#   - StartWhenAvailable=False → 木21:30にPCが寝ている/ログオンしていないと取りこぼす
#     （実際 LastTaskResult=2147946720＝ログオンセッション無しで失敗し続けていた）
#   - DisallowStartIfOnBatteries=True → 電源を挿していない日は実行されない
#   - ExecutionTimeLimit=72時間 → 失敗時に居座る
# だったので、取りこぼしを拾う設定に変える。

$taskName = "PA45 Flow Auto Release"
$bat      = Join-Path $PSScriptRoot "release-flow.bat"
$repo     = Split-Path -Parent $PSScriptRoot

$action    = New-ScheduledTaskAction -Execute $bat -Argument "all" -WorkingDirectory $repo
$trigger   = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Thursday -At ([datetime]"21:30")
$settings  = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 1) `
             -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
# 現在ユーザーで実行（pac の認証プロファイルがこのユーザーに紐づくため）
$principal = New-ScheduledTaskPrincipal -UserId (whoami) -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "PA45: 講座後にフローZIPをエクスポートしてサイトへ反映（毎週木21:30・取りこぼしは起動後に実行）" -Force | Out-Null

Write-Host "登録しました: タスク『$taskName』（毎週木21:30）"
Get-ScheduledTask -TaskName $taskName | Format-List TaskName, State
