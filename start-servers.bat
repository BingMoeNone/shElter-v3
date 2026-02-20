@echo off
echo Starting shElter-v3 Backend...
cd /d "C:\BM_Program\shElter-v3\backend"
start "Backend Server" python -m uvicorn src.main:app --reload --port 8000
echo Backend started at http://localhost:8000
echo.
echo Starting shElter-v3 Frontend...
cd /d "C:\BM_Program\shElter-v3\frontend"
start "Frontend Server" npm run dev
echo Frontend started at http://localhost:5173
echo.
echo Both servers are starting in separate windows.
echo.
echo API Docs: http://localhost:8000/api/docs
echo Frontend: http://localhost:5173
pause
