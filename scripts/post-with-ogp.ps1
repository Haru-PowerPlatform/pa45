param(
    [Parameter(Mandatory=$true)][int]$PostId,
    [Parameter(Mandatory=$true)][string]$Title,
    [string]$Label = "PA45",
    [string]$Sub   = "Power Automate 45"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir   = Split-Path -Parent $scriptDir
$envFile   = Join-Path $rootDir ".env"

$envVars = @{}
Get-Content $envFile | ForEach-Object {
    if ($_ -match '^([^=]+)=(.+)$') {
        $envVars[$Matches[1].Trim()] = $Matches[2].Trim()
    }
}
$WP_USER = $envVars['WP_USER']
$WP_PASS = $envVars['WP_PASS']
$WP_URL  = $envVars['WP_URL']

$edgePath = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$tmplSrc  = Join-Path $scriptDir 'ogp-template.html'
$tempHtml = Join-Path $scriptDir 'ogp-temp.html'
$pngPath  = Join-Path $scriptDir 'ogp-output.png'

# Step 1: タイトル埋め込み
Write-Host 'Step 1: HTML生成...'
$titleHtml = $Title -replace '\n','<br>'
$html = [System.IO.File]::ReadAllText($tmplSrc, [System.Text.Encoding]::UTF8)
$html = [System.Text.RegularExpressions.Regex]::Replace($html,
    '(?s)(<div class="title" id="title">).*?(</div>)',
    ('${1}' + $titleHtml + '${2}'))
$html = [System.Text.RegularExpressions.Regex]::Replace($html,
    '(?s)(<span class="sub" id="sub">).*?(</span>)',
    ('${1}' + $Sub + '${2}'))
[System.IO.File]::WriteAllText($tempHtml, $html, [System.Text.Encoding]::UTF8)

# Step 2: スクリーンショット
Write-Host 'Step 2: PNG生成...'
if (Test-Path $pngPath) { Remove-Item $pngPath }
$fileUri = 'file:///' + $tempHtml.Replace('\','/')
& $edgePath --headless --disable-gpu --window-size=1280,720 "--screenshot=$pngPath" --hide-scrollbars $fileUri 2>$null
Start-Sleep -Seconds 5
if (-not (Test-Path $pngPath)) { Write-Host 'FAIL: PNG生成失敗'; exit 1 }
Write-Host '  PNG OK'

# Step 3: WPメディアアップロード (curl使用)
Write-Host 'Step 3: WordPressにアップロード...'
$fname = 'ogp-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '.png'
$auth  = "${WP_USER}:${WP_PASS}"

$mediaJson = & curl.exe -s -X POST "${WP_URL}/wp-json/wp/v2/media" `
    --user $auth `
    -H "Content-Disposition: attachment; filename=$fname" `
    -H "Content-Type: image/png" `
    --data-binary "@$pngPath"

$media   = $mediaJson | ConvertFrom-Json
$mediaId = $media.id
if (-not $mediaId) { Write-Host 'FAIL: アップロード失敗'; Write-Host $mediaJson; exit 1 }
Write-Host "  Media ID: $mediaId"

# Step 4: アイキャッチ設定 (curl使用)
Write-Host 'Step 4: アイキャッチ設定...'
& curl.exe -s -X POST "${WP_URL}/wp-json/wp/v2/posts/$PostId" `
    --user $auth `
    -H "Content-Type: application/json" `
    --data-binary "{`"featured_media`":$mediaId}" | Out-Null

Write-Host ""
Write-Host "完了! 投稿ID=$PostId / MediaID=$mediaId"
Write-Host "管理画面: ${WP_URL}/wp-admin/post.php?post=${PostId}&action=edit"
Remove-Item $tempHtml -ErrorAction SilentlyContinue
