# Quick Setup: GitHub Update Server (5 Minutes)

## What You'll Have
A free update server on GitHub that your bot checks automatically!

## Steps

### 1. Create GitHub Repository (2 min)

1. Go to github.com
2. Click "New repository"
3. Name: `crypto-bot-updates`
4. Public repository
5. Click "Create repository"

### 2. Create Files Locally (2 min)

On your computer:

```bash
# Create folder
mkdir crypto-bot-updates
cd crypto-bot-updates

# Create structure
mkdir releases

# Create version.json
cat > version.json << 'EOF'
{
  "version": "1.1.0",
  "release_date": "2024-11-07",
  "download_url": "https://raw.githubusercontent.com/YOUR_USERNAME/crypto-bot-updates/main/releases/update-v1.1.zip",
  "changelog_url": "https://raw.githubusercontent.com/YOUR_USERNAME/crypto-bot-updates/main/releases/CHANGELOG-v1.1.md",
  "required": false,
  "min_version": "1.0.0",
  "notes": "Initial version"
}
EOF

# Create changelog
cat > releases/CHANGELOG-v1.1.md << 'EOF'
# Version 1.1.0

Initial release with auto-update system.

## Features
- Auto-update checking
- Settings dialog
- Bot monitoring

## Installation
Automatic via File → Check for Updates
EOF

# Create dummy update (placeholder for now)
mkdir -p temp/files
echo "# Placeholder" > temp/files/README.md
cd temp
zip -r update-v1.1.zip files/
mv update-v1.1.zip ../releases/
cd ..
rm -rf temp
```

### 3. Replace YOUR_USERNAME

**IMPORTANT:** Edit `version.json` and replace `YOUR_USERNAME` with your GitHub username!

```bash
# Mac/Linux
sed -i 's/YOUR_USERNAME/your-actual-username/g' version.json

# Or edit manually
nano version.json
```

### 4. Upload to GitHub (1 min)

```bash
git init
git add .
git commit -m "Initial setup"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/crypto-bot-updates.git
git push -u origin main
```

### 5. Configure Your Bot (30 seconds)

Edit `crypto-futures-bot/utils/auto_updater.py` line 15:

```python
UPDATE_SERVER_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/crypto-bot-updates/main"
```

Replace `YOUR_USERNAME` with your actual GitHub username!

### 6. Test It! (30 seconds)

1. Open your bot: `python main.py`
2. Click **File → Check for Updates**
3. Should say "You're already on the latest version!"

## Done! 🎉

Your update server is live!

## When You Want to Push an Update

### Create Update Package:

```bash
# 1. Create update folder
mkdir -p update-v1.2/files

# 2. Copy changed files (maintaining structure)
cp crypto-futures-bot/core/risk_manager.py update-v1.2/files/core/

# 3. Zip it
cd update-v1.2
zip -r update-v1.2.zip files/
mv update-v1.2.zip ../crypto-bot-updates/releases/

# 4. Create changelog
cat > ../crypto-bot-updates/releases/CHANGELOG-v1.2.md << 'EOF'
# Version 1.2.0

Added risk management system.

## New Features
- Risk calculator
- Position sizing

## Installation
Automatic via File → Check for Updates
EOF
```

### Update version.json:

```bash
cd crypto-bot-updates
nano version.json
```

Change to:
```json
{
  "version": "1.2.0",
  "release_date": "2024-11-08",
  "download_url": "https://raw.githubusercontent.com/YOUR_USERNAME/crypto-bot-updates/main/releases/update-v1.2.zip",
  "changelog_url": "https://raw.githubusercontent.com/YOUR_USERNAME/crypto-bot-updates/main/releases/CHANGELOG-v1.2.md",
  "required": false,
  "min_version": "1.0.0",
  "notes": "Risk management system added"
}
```

### Push to GitHub:

```bash
git add .
git commit -m "Release v1.2.0"
git push
```

### Users Get Update:

1. They click **File → Check for Updates**
2. See "Update available: 1.2.0"
3. Click "Install Update"
4. Done!

## Alternative: Using GitHub Releases

Even easier! Just use GitHub's release feature:

1. Go to your repo on GitHub
2. Click "Releases"
3. Click "Create a new release"
4. Upload your ZIP file
5. GitHub handles everything!

## Troubleshooting

**"Failed to check for updates"**
- Check `version.json` URL is correct
- Visit the URL in browser - should show JSON
- Verify YOUR_USERNAME is replaced

**"Download failed"**
- Check ZIP file uploaded correctly
- Verify file is public (not in private repo)
- Test download URL in browser

## That's It!

You now have a professional auto-update system running on GitHub for free! 🚀

Your users will love it!
