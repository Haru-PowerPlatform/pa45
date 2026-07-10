@echo off
rem PA45 第18回 参加バッジ自動送信（予約: 2026-07-10 18:00 JST）
rem 対象=第18回アンケート回答者（7/9 event当日 ＋ 7/10 翌日分）。送信済みログで重複送信は防止。
cd /d C:\Users\isamu\Documents\pa45
set PYTHONUTF8=1
echo ==== %DATE% %TIME% send start ==== >> logs\badge-vol18-send.log
python scripts\send-badges.py --session 18 --date 2026-07-09 >> logs\badge-vol18-send.log 2>&1
python scripts\send-badges.py --session 18 --date 2026-07-10 >> logs\badge-vol18-send.log 2>&1
echo ==== %DATE% %TIME% send end (exit %ERRORLEVEL%) ==== >> logs\badge-vol18-send.log
