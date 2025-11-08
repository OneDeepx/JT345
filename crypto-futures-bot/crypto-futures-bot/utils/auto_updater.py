"""
Auto-Update System
Checks for and downloads updates from remote server
"""
import requests
import json
import os
import zipfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Tuple
from packaging import version
from utils.logger import setup_logger

logger = setup_logger('auto_update')

# Configuration
CURRENT_VERSION = "1.1.0"
UPDATE_SERVER_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/JT345/main"
# Replace YOUR_USERNAME with your actual GitHub username
# Repository: JT345

# For now, we'll use GitHub raw content as it's free and simple
# You can change this to your own server, S3 bucket, etc.


class AutoUpdater:
    """Handles checking for and applying updates"""
    
    def __init__(self):
        self.current_version = CURRENT_VERSION
        self.update_server = UPDATE_SERVER_URL
        self.base_dir = Path(__file__).parent.parent
        self.updates_dir = self.base_dir / "updates"
        self.backup_dir = self.base_dir / "backups"
    
    def check_for_updates(self) -> Tuple[bool, Optional[Dict]]:
        """
        Check if updates are available
        
        Returns:
            (has_update, update_info) tuple
        """
        try:
            logger.info("Checking for updates...")
            
            # Fetch version info from server
            version_url = f"{self.update_server}/version.json"
            response = requests.get(version_url, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Failed to check for updates: HTTP {response.status_code}")
                return False, None
            
            update_info = response.json()
            latest_version = update_info.get('version')
            
            if not latest_version:
                logger.error("Invalid version info from server")
                return False, None
            
            # Compare versions
            if version.parse(latest_version) > version.parse(self.current_version):
                logger.info(f"Update available: {latest_version} (current: {self.current_version})")
                return True, update_info
            else:
                logger.info("Already on latest version")
                return False, None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error checking for updates: {e}")
            return False, None
        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
            return False, None
    
    def download_update(self, update_info: Dict, progress_callback=None) -> bool:
        """
        Download update package from server
        
        Args:
            update_info: Update information from check_for_updates
            progress_callback: Optional callback for progress updates
            
        Returns:
            True if download successful
        """
        try:
            download_url = update_info.get('download_url')
            if not download_url:
                logger.error("No download URL in update info")
                return False
            
            logger.info(f"Downloading update from {download_url}")
            
            # Create updates directory
            self.updates_dir.mkdir(exist_ok=True)
            
            # Download with progress
            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            zip_path = self.updates_dir / "update.zip"
            
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            progress_callback(progress)
            
            logger.info("Download complete")
            return True
            
        except Exception as e:
            logger.error(f"Error downloading update: {e}")
            return False
    
    def create_backup(self) -> bool:
        """
        Create backup of current installation
        
        Returns:
            True if backup successful
        """
        try:
            from datetime import datetime
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"backup_{timestamp}"
            backup_path.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Creating backup at {backup_path}")
            
            # Backup critical directories
            dirs_to_backup = ['config', 'data', 'database', 'strategies', 'logs']
            
            for dir_name in dirs_to_backup:
                source = self.base_dir / dir_name
                if source.exists():
                    dest = backup_path / dir_name
                    shutil.copytree(source, dest, dirs_exist_ok=True)
                    logger.info(f"Backed up {dir_name}")
            
            logger.info("Backup complete")
            return True
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return False
    
    def extract_update(self) -> bool:
        """
        Extract downloaded update package
        
        Returns:
            True if extraction successful
        """
        try:
            zip_path = self.updates_dir / "update.zip"
            
            if not zip_path.exists():
                logger.error("Update package not found")
                return False
            
            logger.info("Extracting update package...")
            
            # Extract to updates directory
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.updates_dir)
            
            # Remove zip file
            zip_path.unlink()
            
            logger.info("Extraction complete")
            return True
            
        except Exception as e:
            logger.error(f"Error extracting update: {e}")
            return False
    
    def apply_update(self) -> bool:
        """
        Apply extracted update files
        
        Returns:
            True if update applied successfully
        """
        try:
            logger.info("Applying update...")
            
            # Look for files in updates/files directory
            files_dir = self.updates_dir / "files"
            
            if not files_dir.exists():
                logger.error("Update files directory not found")
                return False
            
            # Copy all files from updates/files to base directory
            for item in files_dir.rglob('*'):
                if item.is_file():
                    # Calculate relative path
                    rel_path = item.relative_to(files_dir)
                    dest_path = self.base_dir / rel_path
                    
                    # Create parent directories if needed
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy file
                    shutil.copy2(item, dest_path)
                    logger.info(f"Updated: {rel_path}")
            
            logger.info("Update applied successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error applying update: {e}")
            return False
    
    def cleanup(self):
        """Clean up temporary update files"""
        try:
            if self.updates_dir.exists():
                shutil.rmtree(self.updates_dir)
                logger.info("Cleaned up update files")
        except Exception as e:
            logger.error(f"Error cleaning up: {e}")
    
    def perform_update(self, update_info: Dict, progress_callback=None) -> Tuple[bool, str]:
        """
        Perform complete update process
        
        Args:
            update_info: Update information
            progress_callback: Optional callback for progress updates
            
        Returns:
            (success, message) tuple
        """
        try:
            # Step 1: Create backup
            if progress_callback:
                progress_callback(10, "Creating backup...")
            
            if not self.create_backup():
                return False, "Failed to create backup"
            
            # Step 2: Download update
            if progress_callback:
                progress_callback(30, "Downloading update...")
            
            def download_progress(percent):
                if progress_callback:
                    # Map download progress to 30-60% of total
                    total_progress = 30 + int(percent * 0.3)
                    progress_callback(total_progress, f"Downloading... {percent}%")
            
            if not self.download_update(update_info, download_progress):
                return False, "Failed to download update"
            
            # Step 3: Extract update
            if progress_callback:
                progress_callback(70, "Extracting files...")
            
            if not self.extract_update():
                return False, "Failed to extract update"
            
            # Step 4: Apply update
            if progress_callback:
                progress_callback(85, "Applying update...")
            
            if not self.apply_update():
                return False, "Failed to apply update"
            
            # Step 5: Cleanup
            if progress_callback:
                progress_callback(95, "Cleaning up...")
            
            self.cleanup()
            
            # Step 6: Update version file
            self._update_version_file(update_info['version'])
            
            if progress_callback:
                progress_callback(100, "Update complete!")
            
            return True, f"Successfully updated to version {update_info['version']}"
            
        except Exception as e:
            logger.error(f"Error performing update: {e}")
            return False, f"Update failed: {str(e)}"
    
    def _update_version_file(self, new_version: str):
        """Update local version file"""
        try:
            version_file = self.base_dir / "VERSION"
            version_file.write_text(new_version)
            logger.info(f"Updated version to {new_version}")
        except Exception as e:
            logger.error(f"Error updating version file: {e}")
    
    def get_current_version(self) -> str:
        """Get current version from file or default"""
        try:
            version_file = self.base_dir / "VERSION"
            if version_file.exists():
                return version_file.read_text().strip()
        except:
            pass
        return CURRENT_VERSION
    
    def get_changelog(self, update_info: Dict) -> str:
        """
        Fetch changelog for available update
        
        Args:
            update_info: Update information
            
        Returns:
            Changelog text
        """
        try:
            changelog_url = update_info.get('changelog_url')
            if changelog_url:
                response = requests.get(changelog_url, timeout=10)
                if response.status_code == 200:
                    return response.text
        except Exception as e:
            logger.error(f"Error fetching changelog: {e}")
        
        return "No changelog available"
