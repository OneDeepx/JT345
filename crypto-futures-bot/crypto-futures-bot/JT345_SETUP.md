# Quick Setup: GitHub Update Server - JT345 Repository

## Repository Name: JT345

Your update repository will be named **JT345** on GitHub.

## Quick Setup (5 Minutes)

### 1. Create GitHub Repository

1. Go to github.com
2. Click "New repository"
3. **Name:** `JT345`
4. **Public** repository (required for raw file access)
5. Click "Create repository"

### 2. Create Files Locally

```bash
# Create folder
mkdir JT345
cd JT345

# Create structure
mkdir releases

# Create version.json
cat > version.json << 'EOF'
{
  "version": "1.1.0",
  "release_date": "2024-11-07",
  "download_url": "https://raw.githubusercontent.com/YOUR_USERNAME/JT345/main/releases/update-v1.1.zip",
  "changelog_url": "https://raw.githubusercontent.com/YOUR_USERNAME/JT345/main/releases/CHANGELOG-v1.1.md",
  "required": false,
  "min_version": "1.0.0",
  "notes": "Initial version with auto-update system"
}
EOF

# Create changelog
cat > releases/CHANGELOG-v1.1.md << 'EOF'
# Version 1.1.0

Initial release with professional auto-update system.

## Features
- Auto-update checking via File → Check for Updates
- Automatic download and installation
- Progress bar with status updates
- Automatic backup before updates
- Settings dialog with encrypted API keys
- Bot monitoring tab

## Installation
Updates install automatically via File → Check for Updates
EOF

# Create placeholder update package
mkdir -p temp/files
cat > temp/files/README.md << 'EOF'
# JT345 Updates
This is the initial release package.
EOF
cd temp
zip -r update-v1.1.zip files/
mv update-v1.1.zip ../releases/
cd ..
rm -rf temp
```

### 3. Replace YOUR_USERNAME

**CRITICAL:** Edit `version.json` and replace `YOUR_USERNAME` with your actual GitHub username!

```bash
# Mac/Linux
sed -i 's/YOUR_USERNAME/your-github-username/g' version.json

# Windows (edit manually)
notepad version.json

# Or use any text editor
```

Example: If your GitHub username is `johndoe`:
```json
"download_url": "https://raw.githubusercontent.com/johndoe/JT345/main/releases/update-v1.1.zip"
```

### 4. Upload to GitHub

```bash
# Initialize git
git init
git add .
git commit -m "Initial JT345 setup"
git branch -M main

# Connect to your repo (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/JT345.git

# Push
git push -u origin main
```

### 5. Configure Bot

Edit `crypto-futures-bot/utils/auto_updater.py` line 11:

```python
UPDATE_SERVER_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/JT345/main"
```

**Replace YOUR_USERNAME** with your actual GitHub username!

Example:
```python
UPDATE_SERVER_URL = "https://raw.githubusercontent.com/johndoe/JT345/main"
```

### 6. Test It!

1. Open bot: `python main.py`
2. Click **File → Check for Updates**
3. Should say: "You're already on the latest version!"

If you see this, your update server is working! 🎉

## Verify Setup

Test your URLs in a browser:

1. **Version file:**  
   `https://raw.githubusercontent.com/YOUR_USERNAME/JT345/main/version.json`  
   Should display JSON

2. **Changelog:**  
   `https://raw.githubusercontent.com/YOUR_USERNAME/JT345/main/releases/CHANGELOG-v1.1.md`  
   Should display markdown

3. **Update package:**  
   `https://raw.githubusercontent.com/YOUR_USERNAME/JT345/main/releases/update-v1.1.zip`  
   Should download ZIP

## Repository Structure

Your JT345 repository should look like:

```
JT345/
├── version.json              # Current version info
└── releases/
    ├── update-v1.1.zip      # Update package
    ├── CHANGELOG-v1.1.md    # Changelog
    ├── update-v1.2.zip      # Next update
    └── CHANGELOG-v1.2.md    # Next changelog
```

## Creating Your First Real Update

### 1. Make Changes to Bot Code

```bash
cd crypto-futures-bot
# Edit files, add features, etc.
vim core/risk_manager.py
```

### 2. Package the Update

```bash
# Create update structure
mkdir -p update-v1.2/files/core

# Copy ONLY changed files (maintaining folder structure)
cp core/risk_manager.py update-v1.2/files/core/

# Create ZIP
cd update-v1.2
zip -r update-v1.2.zip files/
```

### 3. Create Changelog

```bash
cat > CHANGELOG-v1.2.md << 'EOF'
# Version 1.2.0

## New Features
- ✨ Risk management system implemented
- ✨ Position size calculator
- ✨ Risk metrics in Bot tab

## Improvements
- 🔧 Better error handling
- 🔧 Performance optimizations

## Bug Fixes
- Fixed calculation error in sentiment analyzer

## Installation
Automatic via File → Check for Updates
Backup created automatically
EOF
```

### 4. Upload to JT345

```bash
# Copy files to JT345 repo
cd ../JT345
cp ../update-v1.2/update-v1.2.zip releases/
cp ../update-v1.2/CHANGELOG-v1.2.md releases/
```

### 5. Update version.json

Edit `JT345/version.json`:

```json
{
  "version": "1.2.0",
  "release_date": "2024-11-08",
  "download_url": "https://raw.githubusercontent.com/YOUR_USERNAME/JT345/main/releases/update-v1.2.zip",
  "changelog_url": "https://raw.githubusercontent.com/YOUR_USERNAME/JT345/main/releases/CHANGELOG-v1.2.md",
  "required": false,
  "min_version": "1.0.0",
  "notes": "Risk management system added"
}
```

### 6. Push to GitHub

```bash
git add .
git commit -m "Release v1.2.0 - Risk management system"
git push
```

### 7. Users Get the Update!

Users open bot → File → Check for Updates → See v1.2.0 → Click Install → Done!

## Troubleshooting

**"Failed to check for updates"**
- Verify YOUR_USERNAME is replaced in auto_updater.py
- Check repository is PUBLIC
- Visit version.json URL in browser to verify it's accessible

**"Repository not found"**
- Ensure repository name is exactly: `JT345`
- Make sure repository is public
- Check GitHub username is correct

**"Download failed"**
- Verify ZIP file uploaded correctly
- Check file size (should be > 0 bytes)
- Test download URL in browser

## Quick Commands Reference

```bash
# Test version.json
curl https://raw.githubusercontent.com/YOUR_USERNAME/JT345/main/version.json

# Test download
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/JT345/main/releases/update-v1.1.zip

# Update and push
cd JT345
git add .
git commit -m "Update v1.X.X"
git push
```

## Summary

✅ Repository name: **JT345**  
✅ Structure created  
✅ Bot configured  
✅ Ready for updates  

Your professional update system is live! 🚀

---

**Next:** Push code changes → Package update → Update version.json → Push to JT345 → Users get update automatically!
