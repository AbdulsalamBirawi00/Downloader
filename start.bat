@echo off
REM Simple startup script for Windows

echo.
echo =================================
echo Telegram Video Downloader Bot
echo =================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.7 or higher from python.org
    echo.
    pause
    exit /b 1
)

REM Display Python version
echo Python is installed:
python --version
echo.

REM Check if bot token is set
if "%TELEGRAM_BOT_TOKEN%"=="" (
    echo ERROR: TELEGRAM_BOT_TOKEN is not set!
    echo.
    echo Please set your bot token first:
    echo   set TELEGRAM_BOT_TOKEN=your_bot_token_here
    echo.
    echo Or for permanent setting, add it to System Environment Variables
    echo.
    echo Get your bot token from @BotFather on Telegram:
    echo   1. Open Telegram and search for @BotFather
    echo   2. Send /newbot command
    echo   3. Follow instructions and copy the token
    echo.
    pause
    exit /b 1
)

echo Bot token is set
echo.
echo Starting bot...
echo Press Ctrl+C to stop
echo.

REM Run the bot
python bot.py
