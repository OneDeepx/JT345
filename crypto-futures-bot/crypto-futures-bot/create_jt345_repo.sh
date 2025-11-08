#!/bin/bash
# Helper script to create JT345 update repository structure
# Run this to quickly set up your update server files

echo "=========================================="
echo "  JT345 Update Repository Setup"
echo "=========================================="
echo ""

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USER

if [ -z "$GITHUB_USER" ]; then
    echo "Error: GitHub username required"
    exit 1
fi

echo ""
echo "Creating JT345 repository structure..."

# Create directory
mkdir -p JT345/releases
cd JT345

# Create version.json with actual username
cat > version.json << EOF
{
  "version": "1.1.0",
  "release_date": "$(date +%Y-%m-%d)",
  "download_url": "https://raw.githubusercontent.com/$GITHUB_USER/JT345/main/releases/update-v1.1.zip",
  "changelog_url": "https://raw.githubusercontent.com/$GITHUB_USER/JT345/main/releases/CHANGELOG-v1.1.md",
  "required": false,
  "min_version": "1.0.0",
  "notes": "Initial version with auto-update system"
}
EOF

echo "✓ Created version.json"

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

echo "✓ Created CHANGELOG-v1.1.md"

# Create placeholder update package
mkdir -p temp/files
cat > temp/files/README.md << 'EOF'
# JT345 Updates
This is the initial release package.
Version 1.1.0
EOF

cd temp
zip -q -r update-v1.1.zip files/
mv update-v1.1.zip ../releases/
cd ..
rm -rf temp

echo "✓ Created update-v1.1.zip"

# Create README
cat > README.md << EOF
# JT345 - Update Repository

This repository hosts updates for the Crypto Futures Trading Bot.

## Current Version
1.1.0

## Structure
- \`version.json\` - Current version information
- \`releases/\` - Update packages and changelogs

## For Users
Updates are installed automatically via:
**File → Check for Updates** in the bot

## For Developers
To release an update:
1. Create update package in \`releases/\`
2. Update \`version.json\`
3. Commit and push

Users will automatically receive the update.
EOF

echo "✓ Created README.md"

# Initialize git
git init
git add .
git commit -m "Initial JT345 setup"
git branch -M main

echo ""
echo "=========================================="
echo "  ✓ JT345 Repository Created!"
echo "=========================================="
echo ""
echo "Directory: $(pwd)"
echo ""
echo "Next steps:"
echo "1. Create repository on GitHub:"
echo "   - Go to github.com"
echo "   - Create new repository named: JT345"
echo "   - Make it PUBLIC"
echo ""
echo "2. Push to GitHub:"
echo "   cd JT345"
echo "   git remote add origin https://github.com/$GITHUB_USER/JT345.git"
echo "   git push -u origin main"
echo ""
echo "3. Configure bot:"
echo "   Edit crypto-futures-bot/utils/auto_updater.py"
echo "   Change line 11 to:"
echo "   UPDATE_SERVER_URL = \"https://raw.githubusercontent.com/$GITHUB_USER/JT345/main\""
echo ""
echo "4. Test:"
echo "   python main.py"
echo "   File → Check for Updates"
echo ""
echo "Your update server will be live!"
echo "=========================================="
