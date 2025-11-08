#!/bin/bash
# Crypto Futures Bot - Update Script for Linux/Mac
# This script safely updates your bot while preserving settings and data

set -e  # Exit on error

echo "============================================================"
echo "   CRYPTO FUTURES BOT - UPDATE SCRIPT"
echo "============================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3 is not installed"
    echo "Please install Python 3.11+ from python.org"
    exit 1
fi

echo "[1/6] Checking current installation..."
if [ ! -f "main.py" ]; then
    echo -e "${RED}[ERROR]${NC} This script must be run from the crypto-futures-bot directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Found bot installation"
echo ""

# Create backup directory
echo "[2/6] Creating backup of current installation..."
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup critical files
echo "Backing up configuration and data..."
[ -d "config" ] && cp -r config "$BACKUP_DIR/" 2>/dev/null || true
[ -d "data" ] && cp -r data "$BACKUP_DIR/" 2>/dev/null || true
[ -d "logs" ] && cp -r logs "$BACKUP_DIR/" 2>/dev/null || true
[ -d "database" ] && cp -r database "$BACKUP_DIR/" 2>/dev/null || true
[ -d "strategies" ] && cp -r strategies "$BACKUP_DIR/" 2>/dev/null || true

echo -e "${GREEN}[OK]${NC} Backup created in: $BACKUP_DIR"
echo ""

# Check for updates folder
echo "[3/6] Looking for updates..."
if [ ! -d "updates" ]; then
    echo -e "${YELLOW}[INFO]${NC} No updates folder found"
    echo ""
    echo "To apply updates:"
    echo "  1. Download the update files"
    echo "  2. Extract to a folder named 'updates' in this directory"
    echo "  3. Run this script again"
    echo ""
    exit 0
fi

echo -e "${GREEN}[OK]${NC} Found updates folder"
echo ""

# Apply updates
echo "[4/6] Applying updates..."
echo ""

# Update Python files
if ls updates/*.py 1> /dev/null 2>&1; then
    echo "Updating Python files..."
    for file in updates/*.py; do
        filename=$(basename "$file")
        echo "  - $filename"
        cp "$file" .
    done
fi

# Update subdirectories
for dir in updates/*/; do
    if [ -d "$dir" ]; then
        dirname=$(basename "$dir")
        echo "Updating $dirname..."
        mkdir -p "$dirname"
        cp -r "$dir"* "$dirname/"
    fi
done

# Update config files (but don't overwrite existing settings)
if [ -f "updates/requirements.txt" ]; then
    echo "Updating requirements.txt..."
    cp updates/requirements.txt requirements.txt
fi

if [ -f "updates/README.md" ]; then
    echo "Updating documentation..."
    cp updates/README.md README.md
fi

if [ -f "updates/ROADMAP.md" ]; then
    cp updates/ROADMAP.md ROADMAP.md
fi

echo -e "${GREEN}[OK]${NC} Updates applied"
echo ""

# Update dependencies
echo "[5/6] Updating Python dependencies..."
if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    pip install -r requirements.txt --upgrade --quiet
    echo -e "${GREEN}[OK]${NC} Dependencies updated"
elif [ -f "venv/Scripts/activate" ]; then
    echo "Activating virtual environment..."
    source venv/Scripts/activate
    pip install -r requirements.txt --upgrade --quiet
    echo -e "${GREEN}[OK]${NC} Dependencies updated"
else
    echo -e "${YELLOW}[WARNING]${NC} Virtual environment not found"
    echo "Run: python3 -m venv venv"
    echo "Then run this script again"
fi
echo ""

# Cleanup
echo "[6/6] Cleaning up..."
if [ -d "updates" ]; then
    echo "Removing updates folder..."
    rm -rf updates
    echo -e "${GREEN}[OK]${NC} Cleanup complete"
fi
echo ""

echo "============================================================"
echo "   UPDATE COMPLETE!"
echo "============================================================"
echo ""
echo "Backup location: $BACKUP_DIR"
echo ""
echo "Changes have been applied. To start the bot:"
echo "  python3 main.py"
echo ""
echo "If you encounter any issues:"
echo "  1. Check the backup folder: $BACKUP_DIR"
echo "  2. Review logs in: logs/app.log"
echo "  3. Ask Claude in the Developer tab"
echo ""
