@echo off
REM ============================================================
REM PA45 フロー Vol別リリース・ワンコマンド
REM
REM 使い方:
REM   release-flow.bat 9
REM     → Vol.9 のソリューションを PA からエクスポート
REM     → flows/vol-09/ にコピー
REM     → sessions/index.html 更新
REM     → git commit & push
REM
REM   release-flow.bat all
REM     → 全Volのソリューションをエクスポート＆反映
REM ============================================================

@echo off
setlocal enabledelayedexpansion

set EXPORT_DIR=C:\Temp\pa45\flow-zips
set REPO_DIR=C:\Users\isamu\Documents\pa45

REM ZIP保存先を作成
if not exist "%EXPORT_DIR%" mkdir "%EXPORT_DIR%"

set VOL=%1
if "%VOL%"=="" (
    echo 使い方: release-flow.bat [Vol番号 ^| all]
    echo   release-flow.bat 9      Vol.9のみ
    echo   release-flow.bat all    全Vol一括
    exit /b 1
)

REM Vol → Solution UniqueName のマッピング
if "%VOL%"=="1" set SOLUTION=PA45_No1_Initialize
if "%VOL%"=="2" set SOLUTION=PA45_No2_SetVariable
if "%VOL%"=="3" set SOLUTION=PA45_No3_Condition
if "%VOL%"=="4" set SOLUTION=PA45_No4_ApplyToEach
if "%VOL%"=="5" set SOLUTION=PA45_No5_Review
if "%VOL%"=="6" set SOLUTION=PA45_No6_FormsMail
if "%VOL%"=="7" set SOLUTION=PA45_No7_FormsSPTeams
if "%VOL%"=="8" set SOLUTION=PA45_No8_Approval
if "%VOL%"=="9" set SOLUTION=PA45_No9_SharePointUpdate

if "%VOL%"=="all" (
    echo === 全Vol一括エクスポート ===
    for %%S in (PA45_No1_Initialize PA45_No2_SetVariable PA45_No3_Condition PA45_No4_ApplyToEach PA45_No5_Review PA45_No6_FormsMail PA45_No7_FormsSPTeams PA45_No8_Approval PA45_No9_SharePointUpdate) do (
        echo.
        echo --- %%S ---
        pac solution export --name %%S --path "%EXPORT_DIR%" --managed --overwrite
    )
    cd /d "%REPO_DIR%"
    python scripts\import-flow-zip.py --src "%EXPORT_DIR%" --all
    goto COMMIT
)

if "%SOLUTION%"=="" (
    echo Vol番号 %VOL% に対応するソリューションが定義されていません
    exit /b 1
)

echo === Vol.%VOL% リリース ===
echo Solution: %SOLUTION%

echo.
echo [1/3] Power Automate からエクスポート中...
pac solution export --name %SOLUTION% --path "%EXPORT_DIR%" --managed --overwrite
if errorlevel 1 (
    echo エクスポート失敗。pac auth list を確認してください。
    exit /b 1
)

echo.
echo [2/3] サイトに反映中...
cd /d "%REPO_DIR%"
python scripts\import-flow-zip.py --src "%EXPORT_DIR%" --vol %VOL%
if errorlevel 1 (
    echo インポート失敗
    exit /b 1
)

:COMMIT
echo.
echo [3/3] git commit ^& push...
cd /d "%REPO_DIR%"
git add -A
git commit -m "feat: PA45 フローZIP更新（Vol.%VOL%）"
git push origin main

echo.
echo ====================================
echo 完了！GitHub Pages反映を数分待ってね
echo ====================================
endlocal
