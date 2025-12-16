# Quick Start Guide

## Running the GUI Application

### Option 1: Run Python Script Directly
```bash
python discord_scraper_gui.py
```

### Option 2: Build Executable (.exe)
```bash
# Install build dependencies
pip install -r requirements_build.txt

# Build the executable
build.bat

# Or manually:
python build_exe.py
```

The executable will be in the `dist` folder: `DiscordScraper.exe`

## GUI Features

1. **Settings**
   - Choose output file location
   - Set maximum number of searches
   - Option to use Google Custom Search API

2. **Controls**
   - **Start Scraping**: Begin collecting Discord invite links
   - **Stop**: Stop the current scraping process
   - **Open Output File**: Open the results file in your default text editor

3. **Progress Display**
   - Real-time progress updates
   - Total links counter
   - New links counter
   - Detailed log of all activities

4. **Log Window**
   - See all scraping activity in real-time
   - View found Discord links
   - Monitor errors and status messages

## Usage Tips

- Start with a small number of searches (10-20) to test
- The scraper saves progress every 10 searches
- You can stop and restart - it will continue from existing links
- Check the log window for detailed information

## Troubleshooting

- **GUI won't start**: Make sure tkinter is installed (usually included with Python)
- **Import errors**: Run `pip install -r requirements.txt`
- **Build fails**: Make sure PyInstaller is installed: `pip install pyinstaller`

