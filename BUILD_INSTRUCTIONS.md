# Building Discord Scraper GUI Executable

## Quick Build (Windows)

1. **Install dependencies:**
   ```bash
   pip install -r requirements_build.txt
   ```

2. **Run the build script:**
   ```bash
   build.bat
   ```

   Or manually:
   ```bash
   python build_exe.py
   ```

3. **Find your executable:**
   - Location: `dist/DiscordScraper.exe`
   - This is a standalone executable - no Python installation needed!

## Manual Build Steps

### Step 1: Install PyInstaller
```bash
pip install pyinstaller
```

### Step 2: Build the Executable
```bash
pyinstaller --onefile --windowed --name=DiscordScraper discord_scraper_gui.py
```

### Step 3: Include Required Modules
If you get import errors, use:
```bash
pyinstaller --onefile --windowed --name=DiscordScraper ^
    --add-data=discord_scraper.py;. ^
    --hidden-import=discord_scraper ^
    --collect-all=tkinter ^
    --collect-all=requests ^
    --collect-all=beautifulsoup4 ^
    discord_scraper_gui.py
```

## Advanced Options

### Add an Icon
1. Create or download an `.ico` file
2. Place it in the project folder as `icon.ico`
3. The build script will automatically use it

### Custom Build Options
Edit `build_exe.py` to customize:
- Output name
- Icon file
- Additional data files
- Hidden imports

## Troubleshooting

### "Module not found" errors
- Make sure all dependencies are installed: `pip install -r requirements_build.txt`
- Check that `discord_scraper.py` is in the same folder

### Large file size
- The executable includes Python and all libraries (~50-100MB)
- This is normal for PyInstaller one-file builds
- Users don't need Python installed to run it

### Antivirus warnings
- Some antivirus software may flag PyInstaller executables
- This is a false positive - the executable is safe
- You may need to add an exception or sign the executable

## Distribution

The `DiscordScraper.exe` file is standalone and can be:
- Copied to any Windows computer
- Distributed to users
- Run without Python installation

**Note:** Users will need an internet connection to use the scraper.

## File Structure After Build

```
project/
├── discord_scraper.py
├── discord_scraper_gui.py
├── build_exe.py
├── build.bat
├── dist/
│   └── DiscordScraper.exe  ← Your executable!
└── build/  (temporary build files)
```

## Testing the Executable

1. Run `dist/DiscordScraper.exe`
2. Test all features:
   - Start/Stop scraping
   - Browse for output file
   - Open output file
   - Check progress and logs

## Size Optimization (Optional)

To reduce file size, you can exclude unused modules:
```bash
pyinstaller --onefile --windowed --name=DiscordScraper ^
    --exclude-module=matplotlib ^
    --exclude-module=numpy ^
    discord_scraper_gui.py
```

