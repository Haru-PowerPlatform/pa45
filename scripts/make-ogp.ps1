# PA45 アイキャッチ自動生成スクリプト
# 使い方: powershell -File scripts\make-ogp.ps1 -Title "記事タイトル" -Label "ラベル" -Out "output.png"

param(
    [string]$Title = "Power Automateの`n最初の壁`"変数`"を`n45分で超えてみる講座",
    [string]$Label = "社外コミュニティ活動",
    [string]$Sub   = "Power Automate 45",
    [string]$Out   = "ogp-output.png"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$templatePath = Join-Path $scriptDir "ogp-template.html"
$outputPath = Join-Path $scriptDir $Out

# タイトルのHTMLエスケープと改行変換
$titleHtml = $Title -replace "`n", "<br>"

# Edge で PNG スクリーンショット生成
$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

& $edgePath `
    --headless `
    --disable-gpu `
    --window-size=1280,720 `
    --screenshot=$outputPath `
    --hide-scrollbars `
    "file:///$templatePath"

Start-Sleep -Seconds 3

if (Test-Path $outputPath) {
    Write-Host "✅ 生成完了: $outputPath"
} else {
    Write-Host "❌ 生成に失敗しました"
}
