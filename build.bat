@echo off
echo ============================================================
echo Building Discord Scraper GUI Executable
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo.
echo Installing/updating required packages...
pip install -q requests beautifulsoup4 lxml

echo.
echo Building executable...
echo This may take a few minutes...
echo.

python build_exe.py

echo.
echo ============================================================
echo Build process completed!
echo Check the 'dist' folder for DiscordScraper.exe
echo ============================================================
pause

