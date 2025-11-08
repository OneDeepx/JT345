# Auto-Update System Guide

## Overview

Your bot now has a professional auto-update system! Users click **File → Check for Updates** and the bot automatically downloads and installs updates from the internet.

## How It Works

```
User clicks "Check for Updates"
         ↓
Bot checks remote server (GitHub/Web)
         ↓
If update available → Shows changelog
         ↓
User clicks "Install Update"
         ↓
Bot automatically:
  1. Creates backup
  2. Downloads update
  3. Extracts files
  4. Applies changes
  5. Restarts
```

## Setup Options

You have 3 options for hosting updates:

### Option 1: GitHub (FREE & Recommended)

**Steps:**
1. Create a GitHub repository: `crypto-bot-updates`
2. Create this structure:
   ```
   crypto-bot-updates/
   ├── version.json
   └── releases/
       ├── update-v1.2.zip
       └── CHANGELOG-v1.2.md
   ```
3. Update `version.json` with new version info
4. Upload update ZIP files to `releases/`
5. Done! Bot will check this repo

**Configure the bot:**
Edit `utils/auto_updater.py` line 15:
```python
UPDATE_SERVER_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/crypto-bot-updates/main"
```

### Option 2: Your Own Web Server

**Requirements:**
- Any web server (Apache, Nginx, etc.)
- Public URL

**Structure:**
```
your-server.com/bot-updates/
├── version.json
└── releases/
    ├── update-v1.2.zip
    └── CHANGELOG-v1.2.md
```

**Configure the bot:**
```python
UPDATE_SERVER_URL = "https://your-server.com/bot-updates"
```

### Option 3: Cloud Storage (S3, Google Cloud, etc.)

**Steps:**
1. Create bucket with public read access
2. Upload files
3. Get public URLs
4. Configure bot with bucket URL

## Creating an Update

### Step 1: Prepare Files

Create folder structure:
```
update-v1.2/
└── files/
    ├── main.py                  (if changed)
    ├── core/
    │   └── risk_manager.py      (new file)
    ├── ui/
    │   └── tabs/
    │       └── bot_tab.py       (changed)
    └── requirements.txt         (if changed)
```

**Important:** Only include files that changed!

### Step 2: Create Changelog

Create `CHANGELOG-v1.2.md`:
```markdown
# Version 1.2.0 - Risk Manager Implementation

## What's New
- ✨ NEW: Risk management system
- ✨ NEW: Position size calculator
- 🔧 IMPROVED: Bot tab shows risk metrics

## Bug Fixes
- Fixed calculation error in sentiment analyzer

## Installation
This update will be installed automatically.
Backup is created automatically.
```

### Step 3: Package Update

```bash
cd update-v1.2
zip -r update-v1.2.zip files/
```

### Step 4: Update version.json

```json
{
  "version": "1.2.0",
  "release_date": "2024-11-07",
  "download_url": "https://your-url/releases/update-v1.2.zip",
  "changelog_url": "https://your-url/releases/CHANGELOG-v1.2.md",
  "required": false,
  "min_version": "1.0.0",
  "notes": "Adds risk management system"
}
```

### Step 5: Upload to Server

**GitHub:**
1. Upload `update-v1.2.zip` to `releases/`
2. Upload `CHANGELOG-v1.2.md` to `releases/`
3. Update `version.json` in root
4. Commit and push

**Web Server:**
1. FTP/Upload files to server
2. Ensure public read access

### Step 6: Test

1. Open bot
2. File → Check for Updates
3. Should see your new version
4. Test install process

## version.json Reference

```json
{
  "version": "1.2.0",              // New version number
  "release_date": "2024-11-07",    // Release date
  "download_url": "...",           // Direct download link to ZIP
  "changelog_url": "...",          // Direct link to changelog
  "required": false,               // True = force update
  "min_version": "1.0.0",          // Minimum version that can update
  "notes": "Short description"     // Brief description
}
```

## Update Package Structure

Your ZIP file must have this structure:

```
update-v1.2.zip
└── files/
    ├── [changed files maintaining folder structure]
    ├── core/
    │   └── risk_manager.py
    └── ui/
        └── tabs/
            └── bot_tab.py
```

**CRITICAL:** The `files/` folder is required! All content must be inside it.

## What Gets Backed Up

Before each update, automatically backed up:
- config/ (API keys, settings)
- data/ (user data)
- database/ (trade history)
- strategies/ (uploaded strategies)
- logs/ (activity logs)

## What Gets Updated

Only files in the update package:
- Python code (.py files)
- Configuration (requirements.txt, etc.)
- Documentation (README, etc.)

User data is NEVER overwritten.

## User Experience

### Checking for Updates:
1. User: File → Check for Updates
2. Bot: "Checking for updates..."
3. Bot: Shows version, changelog
4. User: Clicks "Install Update"
5. Bot: Shows progress bar
6. Bot: "Update complete! Restarting..."

### No Updates Available:
1. User: File → Check for Updates
2. Bot: "You're already on the latest version!"

## Example GitHub Setup

### 1. Create Repository

```bash
# On GitHub, create repo: crypto-bot-updates
git clone https://github.com/YOUR_USERNAME/crypto-bot-updates
cd crypto-bot-updates
```

### 2. Create Structure

```bash
mkdir releases
touch version.json
```

### 3. Add version.json

```json
{
  "version": "1.1.0",
  "release_date": "2024-11-07",
  "download_url": "https://raw.githubusercontent.com/YOUR_USERNAME/crypto-bot-updates/main/releases/update-v1.1.zip",
  "changelog_url": "https://raw.githubusercontent.com/YOUR_USERNAME/crypto-bot-updates/main/releases/CHANGELOG-v1.1.md",
  "required": false,
  "min_version": "1.0.0",
  "notes": "Initial release"
}
```

### 4. Create First Release

```bash
# Create update package
mkdir -p temp/files/ui
cp /path/to/changed/file.py temp/files/ui/
cd temp
zip -r update-v1.1.zip files/
mv update-v1.1.zip ../releases/

# Create changelog
echo "# Version 1.1.0
Initial release with auto-update support" > releases/CHANGELOG-v1.1.md
```

### 5. Commit and Push

```bash
git add .
git commit -m "Initial release v1.1.0"
git push
```

### 6. Configure Bot

In `utils/auto_updater.py`:
```python
UPDATE_SERVER_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/crypto-bot-updates/main"
```

### 7. Test

Open bot → File → Check for Updates

## Troubleshooting

### "Failed to check for updates"
- Check internet connection
- Verify UPDATE_SERVER_URL is correct
- Check server is accessible
- View logs/app.log for details

### "Download failed"
- Check download_url is correct
- Verify file exists on server
- Check file permissions (public read)

### "Update failed to apply"
- Check ZIP structure (must have files/ folder)
- Verify file paths are correct
- Check logs/app.log

### Updates not showing
- Verify version.json has higher version number
- Check version.json format is valid JSON
- Ensure URLs are accessible
- Clear browser cache if using CDN

## Security Considerations

### Best Practices:
1. ✅ Use HTTPS URLs only
2. ✅ Sign your updates (advanced)
3. ✅ Use GitHub releases (built-in integrity)
4. ✅ Test updates before publishing
5. ✅ Keep backup of all versions

### Don't:
1. ❌ Use HTTP (not secure)
2. ❌ Upload to untrusted servers
3. ❌ Skip testing
4. ❌ Delete old versions immediately

## Advanced: GitHub Releases

Instead of raw files, use GitHub Releases:

```python
UPDATE_SERVER_URL = "https://api.github.com/repos/YOUR_USERNAME/crypto-bot/releases/latest"
```

Requires different parsing but provides:
- Built-in checksums
- Download statistics
- Better version management

## Quick Reference

### Release Checklist:
- [ ] Create update package with files/ folder
- [ ] Create changelog
- [ ] Update version.json
- [ ] Upload to server
- [ ] Test download URLs
- [ ] Test update process
- [ ] Announce to users

### File Locations:
- Server: `version.json` and `releases/`
- Bot: `VERSION` file (current version)
- Backups: `backups/backup_TIMESTAMP/`

### Commands:
```bash
# Create update package
zip -r update-v1.2.zip files/

# Test locally
python -m http.server 8000
# Then update URL to http://localhost:8000
```

## Future Improvements

Consider adding:
1. **Automatic checks** - Check on startup
2. **Notification badge** - Show update indicator
3. **Download resume** - Handle interrupted downloads
4. **Delta updates** - Only download changes
5. **Rollback** - One-click revert to previous version
6. **Update scheduling** - Install updates at specific time

## Support

If users have update issues:
1. Check logs/app.log
2. Verify internet connection
3. Try manual update (download ZIP)
4. Restore from backup if needed
5. Contact support with log file

---

**You now have a professional auto-update system!** Users will love the convenience of automatic updates. 🎉
