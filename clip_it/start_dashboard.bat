@echo off
REM Clip Operations Center - Start Dashboard Script
cd /d "%~dp0"
call .venv\Scripts\activate.bat 2>nul
echo Starting Clip Operations Center Dashboard...
echo Dashboard: http://127.0.0.1:8765
.venv\Scripts\python.exe -m clipops serve