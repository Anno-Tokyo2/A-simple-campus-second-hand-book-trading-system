@echo off
chcp 65001 >nul 2>&1
setlocal

echo ========================================
echo   Campus Book Exchange - Starting...
echo ========================================
echo.

echo [0/2] Stopping old services on ports 8000 / 5173...
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":8000 " ^| findstr "LISTENING"') do taskkill /F /T /PID %%p >nul 2>&1
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":5173 " ^| findstr "LISTENING"') do taskkill /F /T /PID %%p >nul 2>&1
timeout /t 2 /nobreak >nul

echo [1/2] Starting backend on port 8000...
start "Backend" cmd /k "cd /d %~dp0backend && python main.py"

timeout /t 3 /nobreak >nul

echo [2/2] Starting frontend on port 5173...
start "Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo   Both services are starting...
echo   Open browser: http://localhost:5173
echo   Login: admin / admin123
echo ========================================
echo.
echo Press any key to close this window...
pause >nul
