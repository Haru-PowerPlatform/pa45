@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

REM Force UTF-8 for the python steps. Without this, a CP932 console makes
REM check-naming.py crash on the "check mark" character and the whole
REM release aborts (hit on 2026-08-15).
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

REM ============================================================
REM PA45 Flow Release Pipeline
REM Usage:
REM   release-flow.bat 9        Export Vol.9 only
REM   release-flow.bat all      Export all Vols (1-9)
REM ============================================================

set EXPORT_DIR=C:\Temp\pa45\flow-zips
set REPO_DIR=C:\Users\isamu\Documents\pa45

if not exist "%EXPORT_DIR%" mkdir "%EXPORT_DIR%"

set VOL=%1
if "%VOL%"=="" (
    echo Usage: release-flow.bat [VolNumber or all]
    exit /b 1
)

REM Naming validation (skip with --skip-check)
if not "%2"=="--skip-check" (
    echo.
    echo === Naming validation ===
    python "%~dp0check-naming.py"
    if errorlevel 1 (
        echo.
        echo Naming check failed. Fix above issues, or run with --skip-check to bypass.
        exit /b 1
    )
)

REM Solution UniqueName mapping (Power Platform strips underscores)
if "%VOL%"=="1" set SOLUTION=PA45No1Initialize
if "%VOL%"=="2" set SOLUTION=PA45No2SetVariable
if "%VOL%"=="3" set SOLUTION=PA45No3Condition
if "%VOL%"=="4" set SOLUTION=PA45No4ApplyToEach
if "%VOL%"=="5" set SOLUTION=PA45No5Review
if "%VOL%"=="6" set SOLUTION=PA45No6FormsMail
if "%VOL%"=="7" set SOLUTION=PA45No7FormsSPTeams
if "%VOL%"=="8" set SOLUTION=PA45No8Approval
if "%VOL%"=="9" set SOLUTION=PA45No9SharePointUpdate
if "%VOL%"=="10" set SOLUTION=PA45No10BizReview
REM Vol.11 (PA45No11RunHistory) was removed from the PA45Demo environment.
REM flows\vol-11\PA45-Vol11-RunHistory.zip is already published, so it is not re-exported.
REM Leaving it in the map made check-naming.py fail and aborted every weekly run.

if "%VOL%"=="all" goto ALL

if "%SOLUTION%"=="" (
    echo Vol %VOL% is not defined
    exit /b 1
)

echo === Vol.%VOL% Release ===
echo Solution: %SOLUTION%

echo.
echo [1/3] Exporting from Power Automate...
REM "call" is required: pac is a .cmd wrapper, and calling it without "call"
REM hands over the batch context and never returns - the import/commit steps
REM below were silently skipped every run (found 2026-08-15).
call pac solution export --name %SOLUTION% --path "%EXPORT_DIR%" --managed --overwrite
if errorlevel 1 (
    echo Export failed
    exit /b 1
)

echo.
echo [2/3] Importing to site...
cd /d "%REPO_DIR%"
python scripts\import-flow-zip.py --src "%EXPORT_DIR%" --vol %VOL%
if errorlevel 1 (
    echo Import failed
    exit /b 1
)

goto COMMIT

:ALL
echo === All Vols Release ===
for %%S in (PA45No1Initialize PA45No2SetVariable PA45No3Condition PA45No4ApplyToEach PA45No5Review PA45No6FormsMail PA45No7FormsSPTeams PA45No8Approval PA45No9SharePointUpdate PA45No10BizReview) do (
    echo.
    echo --- %%S ---
    call pac solution export --name %%S --path "%EXPORT_DIR%" --managed --overwrite
)
cd /d "%REPO_DIR%"
python scripts\import-flow-zip.py --src "%EXPORT_DIR%" --all

:COMMIT
echo.
echo [3/3] Git commit and push...
cd /d "%REPO_DIR%"

REM Skip git ops while a Claude session is editing the repo (lock updated within 5 min).
powershell -NoProfile -ExecutionPolicy Bypass -Command "$f='C:\Users\isamu\.claude\locks\pa45.lock'; if ((Test-Path $f) -and (((Get-Date)-(Get-Item $f).LastWriteTime).TotalMinutes -lt 5)) { exit 1 } else { exit 0 }"
if errorlevel 1 (
    echo Another session is editing pa45 - skipped git commit/push. ZIPs are already updated locally.
    goto :DONE
)

REM Commit only what this pipeline generates. Never use "git add -A" here:
REM the repo is PUBLIC and usually holds unrelated work in progress.
git add -- flows sessions\index.html
git diff --cached --quiet -- flows sessions\index.html
if errorlevel 1 (
    git commit -m "feat: PA45 flow ZIP update (Vol.%VOL%)" -- flows sessions\index.html
    git push origin main
) else (
    echo No changes in flows/ or sessions/index.html - nothing to commit.
)

:DONE

echo.
echo === Done! GitHub Pages will reflect in a few minutes ===
endlocal
