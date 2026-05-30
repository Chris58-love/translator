@echo off
chcp 65001 >nul
title Realtime Interpreter Launcher

cd /d "%~dp0"

echo ==========================================
echo Realtime Interpreter - Windows Launcher
echo ==========================================
echo.

if not exist "one_click_start_auto.py" (
    echo [ERROR] one_click_start_auto.py not found.
    echo Please make sure this bat file is in the project root directory.
    echo.
    pause
    exit /b 1
)

if not exist "backend" (
    echo [ERROR] backend folder not found.
    echo.
    pause
    exit /b 1
)

if not exist "frontend" (
    echo [ERROR] frontend folder not found.
    echo.
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found.
    echo.
    pause
    exit /b 1
)

if not exist ".env" (
    echo [ERROR] .env file not found.
    echo Please copy .env.template to .env and fill in your DeepSeek API key.
    echo.
    pause
    exit /b 1
)

echo Starting project...
echo.

python one_click_start_auto.py

if errorlevel 1 (
    echo.
    echo [ERROR] Project failed to start.
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo Project stopped.
pause