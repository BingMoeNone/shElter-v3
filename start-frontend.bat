@echo off
cd /d "C:\BM_Program\shElter-v3\frontend-legacy"
echo Starting frontend server on http://localhost:8080...
python -m http.server 8080
pause