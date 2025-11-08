@echo off
REM Crypto Futures Bot - Update Script for Windows
REM This script safely updates your bot while preserving settings and data

echo ============================================================
echo    CRYPTO FUTURES BOT - UPDATE SCRIPT
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11+ from python.org
    pause
    exit /b 1
)

echo [1/6] Checking current installation...
if not exist "main.py" (
    echo [ERROR] This script must be run from the crypto-futures-bot directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo [OK] Found bot installation
echo.

REM Create backup directory
echo [2/6] Creating backup of current installation...
set BACKUP_DIR=backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_DIR=%BACKUP_DIR: =0%
mkdir "%BACKUP_DIR%" 2>nul

REM Backup critical files
echo Backing up configuration and data...
if exist "config" xcopy /E /I /Y config "%BACKUP_DIR%\config" >nul
if exist "data" xcopy /E /I /Y data "%BACKUP_DIR%\data" >nul
if exist "logs" xcopy /E /I /Y logs "%BACKUP_DIR%\logs" >nul
if exist "database" xcopy /E /I /Y database "%BACKUP_DIR%\database" >nul
if exist "strategies" xcopy /E /I /Y strategies "%BACKUP_DIR%\strategies" >nul

echo [OK] Backup created in: %BACKUP_DIR%
echo.

REM Check for updates folder
echo [3/6] Looking for updates...
if not exist "updates" (
    echo [INFO] No updates folder found
    echo.
    echo To apply updates:
    echo   1. Download the update files
    echo   2. Extract to a folder named "updates" in this directory
    echo   3. Run this script again
    echo.
    pause
    exit /b 0
)

echo [OK] Found updates folder
echo.

REM Apply updates
echo [4/6] Applying updates...
echo.

REM Update Python files
if exist "updates\*.py" (
    echo Updating Python files...
    for %%f in (updates\*.py) do (
        echo   - %%~nxf
        copy /Y "%%f" "." >nul
    )
)

REM Update subdirectories
for /d %%d in (updates\*) do (
    if exist "%%d\*.py" (
        echo Updating %%~nxd...
        if not exist "%%~nxd" mkdir "%%~nxd"
        xcopy /E /I /Y "%%d\*" "%%~nxd" >nul
    )
)

REM Update config files (but don't overwrite existing settings)
if exist "updates\requirements.txt" (
    echo Updating requirements.txt...
    copy /Y "updates\requirements.txt" "requirements.txt" >nul
)

if exist "updates\README.md" (
    echo Updating documentation...
    copy /Y "updates\README.md" "README.md" >nul
)

if exist "updates\ROADMAP.md" (
    copy /Y "updates\ROADMAP.md" "ROADMAP.md" >nul
)

echo [OK] Updates applied
echo.

REM Update dependencies
echo [5/6] Updating Python dependencies...
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt --upgrade --quiet
    echo [OK] Dependencies updated
) else (
    echo [WARNING] Virtual environment not found
    echo Run: python -m venv venv
    echo Then run this script again
)
echo.

REM Cleanup
echo [6/6] Cleaning up...
if exist "updates" (
    echo Removing updates folder...
    rmdir /S /Q updates
    echo [OK] Cleanup complete
)
echo.

echo ============================================================
echo    UPDATE COMPLETE!
echo ============================================================
echo.
echo Backup location: %BACKUP_DIR%
echo.
echo Changes have been applied. To start the bot:
echo   python main.py
echo.
echo If you encounter any issues:
echo   1. Check the backup folder: %BACKUP_DIR%
echo   2. Review logs in: logs\app.log
echo   3. Ask Claude in the Developer tab
echo.
pause
