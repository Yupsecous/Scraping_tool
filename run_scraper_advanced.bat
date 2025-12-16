@echo off
echo ============================================================
echo Discord Invite Link Scraper - Advanced Mode
echo ============================================================
echo.

set /p max_searches="Enter maximum number of searches (default 100): "
if "%max_searches%"=="" set max_searches=100

set /p output_file="Enter output file name (default invite_link.txt): "
if "%output_file%"=="" set output_file=invite_link.txt

echo.
echo Running scraper with:
echo   Max searches: %max_searches%
echo   Output file: %output_file%
echo.

python discord_scraper.py -n %max_searches% -o %output_file%

echo.
pause

