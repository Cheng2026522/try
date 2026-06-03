@echo off
cls
echo ===============================================
echo     Construction Management System - Backend
echo ===============================================

set "projectPath=%cd%"
set "backendPath=%projectPath%\backend"
set "venvPath=%backendPath%\Group_env"
set "venvActivate=%venvPath%\Scripts\Activate.bat"

echo.
echo [1/6] Changing to backend directory...
cd /d "%backendPath%"

echo.
echo [2/6] Checking virtual environment...
if not exist "%venvPath%" (
    echo Virtual environment not found, creating...
    python -m venv Group_env
    if not exist "%venvActivate%" (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
)

echo.
echo [3/6] Activating virtual environment...
call "%venvActivate%"

echo.
echo [4/6] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo Dependencies installed successfully

echo.
echo [5/6] Running database migrations...
python manage.py makemigrations --noinput
python manage.py migrate --noinput
if %errorlevel% neq 0 (
    echo ERROR: Database migration failed!
    pause
    exit /b 1
)
echo Database migrations completed

echo.
echo [6/6] Starting backend server...
echo ------------------------------------------------
echo   Server: http://localhost:8000
echo   Admin:  http://localhost:8000/admin/
echo   Links:  http://localhost:8000/
echo ------------------------------------------------
python manage.py runserver 0.0.0.0:8000

pause
