@echo off
cd /d "C:\BM_Program\shElter-v3\backend"
echo Starting backend server...
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000
pause
