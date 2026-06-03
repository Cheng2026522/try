@echo off
cls
echo ===============================================
echo     Construction Management System - Frontend
echo ===============================================

set "projectPath=%cd%"
set "frontendPath=%projectPath%\frontend"

echo.
echo [1/3] Changing to frontend directory...
cd /d "%frontendPath%"

echo.
echo [2/3] Checking Node.js...
node --version
if %errorlevel% neq 0 (
    echo ERROR: Node.js not installed or not in PATH!
    pause
    exit /b 1
)
echo Node.js version:
node --version

echo.
echo [3/3] Starting frontend server...
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
)

echo ------------------------------------------------
echo   Server: http://localhost:8084
echo   Login:  http://localhost:8084/login
echo   Index:  http://localhost:8084/
echo ------------------------------------------------
npm run dev -- --host 0.0.0.0 --port 8084

pause
