@echo off
echo ============================================================
echo Discord Invite Link Scraper
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking for required packages...
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install required packages
        pause
        exit /b 1
    )
)

echo.
echo Starting scraper...
echo.

REM Run the scraper
python discord_scraper.py

echo.
echo ============================================================
echo Scraping completed!
echo Check invite_link.txt for results
echo ============================================================
pause

