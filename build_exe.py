"""
Build script for creating .exe file from the Discord scraper GUI
"""

import PyInstaller.__main__
import os
import sys

def build_exe():
    """Build the executable file."""
    print("=" * 60)
    print("Building Discord Scraper GUI Executable")
    print("=" * 60)
    
    # PyInstaller options
    options = [
        'discord_scraper_gui.py',  # Main script
        '--name=DiscordScraper',   # Output name
        '--onefile',               # Single executable file
        '--windowed',              # No console window (GUI only)
        '--icon=NONE',             # No icon (can add icon file later)
        '--add-data=discord_scraper.py;.',  # Include scraper module
        '--hidden-import=discord_scraper',  # Ensure module is included
        '--hidden-import=google_search_api',  # Include API module if exists
        '--collect-all=tkinter',   # Collect all tkinter files
        '--collect-all=requests',  # Collect all requests files
        '--collect-all=beautifulsoup4',  # Collect all bs4 files
        '--clean',                 # Clean cache before building
    ]
    
    # Add icon if it exists
    if os.path.exists('icon.ico'):
        options.append('--icon=icon.ico')
    
    print("\nRunning PyInstaller...")
    print("This may take a few minutes...\n")
    
    try:
        PyInstaller.__main__.run(options)
        print("\n" + "=" * 60)
        print("Build completed successfully!")
        print("=" * 60)
        print("\nExecutable location: dist/DiscordScraper.exe")
        print("\nYou can now distribute this .exe file!")
    except Exception as e:
        print(f"\nError building executable: {str(e)}")
        print("\nMake sure PyInstaller is installed:")
        print("  pip install pyinstaller")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()

