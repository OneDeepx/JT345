@echo off
REM Helper script to create JT345 update repository structure
REM Run this to quickly set up your update server files

echo ==========================================
echo   JT345 Update Repository Setup
echo ==========================================
echo.

REM Get GitHub username
set /p GITHUB_USER="Enter your GitHub username: "

if "%GITHUB_USER%"=="" (
    echo Error: GitHub username required
    pause
    exit /b 1
)

echo.
echo Creating JT345 repository structure...

REM Create directory
mkdir JT345\releases 2>nul
cd JT345

REM Create version.json with actual username
(
echo {
echo   "version": "1.1.0",
echo   "release_date": "%date:~-4,4%-%date:~-10,2%-%date:~-7,2%",
echo   "download_url": "https://raw.githubusercontent.com/%GITHUB_USER%/JT345/main/releases/update-v1.1.zip",
echo   "changelog_url": "https://raw.githubusercontent.com/%GITHUB_USER%/JT345/main/releases/CHANGELOG-v1.1.md",
echo   "required": false,
echo   "min_version": "1.0.0",
echo   "notes": "Initial version with auto-update system"
echo }
) > version.json

echo [OK] Created version.json

REM Create changelog
(
echo # Version 1.1.0
echo.
echo Initial release with professional auto-update system.
echo.
echo ## Features
echo - Auto-update checking via File -^> Check for Updates
echo - Automatic download and installation
echo - Progress bar with status updates
echo - Automatic backup before updates
echo - Settings dialog with encrypted API keys
echo - Bot monitoring tab
echo.
echo ## Installation
echo Updates install automatically via File -^> Check for Updates
) > releases\CHANGELOG-v1.1.md

echo [OK] Created CHANGELOG-v1.1.md

REM Create placeholder update package
mkdir temp\files 2>nul
(
echo # JT345 Updates
echo This is the initial release package.
echo Version 1.1.0
) > temp\files\README.md

cd temp
powershell -command "Compress-Archive -Path files\* -DestinationPath ..\releases\update-v1.1.zip -Force"
cd ..
rmdir /S /Q temp

echo [OK] Created update-v1.1.zip

REM Create README
(
echo # JT345 - Update Repository
echo.
echo This repository hosts updates for the Crypto Futures Trading Bot.
echo.
echo ## Current Version
echo 1.1.0
echo.
echo ## Structure
echo - `version.json` - Current version information
echo - `releases/` - Update packages and changelogs
echo.
echo ## For Users
echo Updates are installed automatically via:
echo **File -^> Check for Updates** in the bot
echo.
echo ## For Developers
echo To release an update:
echo 1. Create update package in `releases/`
echo 2. Update `version.json`
echo 3. Commit and push
echo.
echo Users will automatically receive the update.
) > README.md

echo [OK] Created README.md

REM Initialize git
git init
git add .
git commit -m "Initial JT345 setup"
git branch -M main

echo.
echo ==========================================
echo   [OK] JT345 Repository Created!
echo ==========================================
echo.
echo Directory: %CD%
echo.
echo Next steps:
echo 1. Create repository on GitHub:
echo    - Go to github.com
echo    - Create new repository named: JT345
echo    - Make it PUBLIC
echo.
echo 2. Push to GitHub:
echo    cd JT345
echo    git remote add origin https://github.com/%GITHUB_USER%/JT345.git
echo    git push -u origin main
echo.
echo 3. Configure bot:
echo    Edit crypto-futures-bot\utils\auto_updater.py
echo    Change line 11 to:
echo    UPDATE_SERVER_URL = "https://raw.githubusercontent.com/%GITHUB_USER%/JT345/main"
echo.
echo 4. Test:
echo    python main.py
echo    File -^> Check for Updates
echo.
echo Your update server will be live!
echo ==========================================
pause
