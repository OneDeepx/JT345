# Update System Guide

## For Users: How to Apply Updates

### Windows:
1. Download the update package (update-vX.X.zip)
2. Extract it in your bot folder - it will create an "updates" folder
3. Double-click `update.bat`
4. Wait for completion
5. Done! Your settings and data are preserved

### Mac/Linux:
1. Download the update package (update-vX.X.tar.gz)
2. Extract it in your bot folder
3. Run: `./update.sh`
4. Wait for completion
5. Done! Your settings and data are preserved

### What Gets Preserved:
- ✅ Your API keys (encrypted)
- ✅ All settings
- ✅ Trade history database
- ✅ Logs
- ✅ Strategies
- ✅ Any custom configurations

### What Gets Updated:
- Python code files (.py)
- Requirements (dependencies)
- Documentation
- New features

### Safety:
- Automatic backup before update
- Backup folder created with timestamp
- If something breaks, restore from backup

---

## For Claude/Developers: How to Create Update Packages

When you deliver updates to the user, package them like this:

### Step 1: Create Updates Folder Structure

```
updates/
├── main.py                    (if updated)
├── requirements.txt           (if updated)
├── ui/
│   ├── settings_dialog.py    (new/updated files)
│   ├── main_window.py
│   └── tabs/
│       └── bot_tab.py
├── core/
│   ├── trading_engine.py     (new implementations)
│   └── risk_manager.py
├── apis/
│   └── binance_api.py        (new implementations)
└── README.md                  (updated docs)
```

### Step 2: Create Package

**For Windows users:**
```bash
# Create zip file
zip -r update-v1.1.zip updates/

# Or using 7-zip
7z a update-v1.1.zip updates/
```

**For Mac/Linux users:**
```bash
# Create tar.gz file
tar -czf update-v1.1.tar.gz updates/
```

### Step 3: Provide to User

Give the user:
1. The update package (zip or tar.gz)
2. A changelog (what's new)
3. Instructions: "Extract in bot folder and run update.bat/update.sh"

### Example Update Delivery:

```
📦 UPDATE v1.1 - Trading Engine Implementation

Files included:
- core/trading_engine.py (NEW)
- core/risk_manager.py (NEW)
- core/sentiment_analyzer.py (NEW)
- ui/tabs/bot_tab.py (UPDATED)
- requirements.txt (UPDATED - added TA-Lib)

To install:
1. Download update-v1.1.zip
2. Extract in your crypto-futures-bot folder
3. Run update.bat (Windows) or ./update.sh (Mac/Linux)
4. Restart the bot

Changes:
✨ NEW: Core trading engine implemented
✨ NEW: Risk management system
✨ NEW: Sentiment analysis
🔧 UPDATED: Bot tab now shows real trading data
```

### Important: Only Include Changed Files

Don't include:
- ❌ config/ folder (contains user's API keys)
- ❌ data/ folder (user's data)
- ❌ logs/ folder (user's logs)
- ❌ database/ folder (user's database)
- ❌ venv/ folder (virtual environment)
- ❌ __pycache__/ folders

Only include:
- ✅ New or modified .py files
- ✅ Updated requirements.txt
- ✅ Updated documentation
- ✅ New features

### Testing Updates Before Delivery

1. Create clean installation
2. Run update script with your package
3. Verify:
   - Update applies successfully
   - Bot still runs
   - Settings preserved
   - New features work
4. Then deliver to user

### Version Naming Convention

- update-v1.1.zip - Minor update (bug fixes, small features)
- update-v1.2.zip - Medium update (new tab, new feature)
- update-v2.0.zip - Major update (trading engine, big changes)

### Changelog Template

```markdown
# Update v1.1 - [Date]

## What's New
- Feature 1
- Feature 2

## Improvements
- Improvement 1
- Improvement 2

## Bug Fixes
- Fix 1
- Fix 2

## Files Changed
- path/to/file1.py (NEW/UPDATED)
- path/to/file2.py (NEW/UPDATED)

## Installation
1. Extract update package in bot folder
2. Run update.bat or ./update.sh
3. Restart bot

## Notes
- Any special instructions
- Breaking changes
- Required actions
```

---

## Quick Reference

### User Commands:
**Windows:** `update.bat`  
**Mac/Linux:** `./update.sh`

### Developer Workflow:
1. Make changes to code
2. Test thoroughly
3. Create updates/ folder with only changed files
4. Package as zip/tar.gz
5. Provide to user with changelog
6. User runs update script
7. Done!

### Emergency Rollback:
If update breaks something:
```bash
# User can restore from backup
cd backup_20241107_143022
cp -r * ..
```

---

## Benefits of This System

✅ **Safe** - Automatic backups before updates  
✅ **Easy** - One command to update  
✅ **Smart** - Preserves user data and settings  
✅ **Clean** - Only updates what changed  
✅ **Fast** - No need to reconfigure everything  
✅ **Rollback** - Can restore from backup if needed  

This makes your life easier and gives users confidence in updates!
