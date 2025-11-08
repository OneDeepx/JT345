"""
Update Dialog - UI for checking and installing updates
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QProgressBar, QTextEdit, QMessageBox, QWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from utils.auto_updater import AutoUpdater
from utils.logger import setup_logger

logger = setup_logger('update_dialog')


class UpdateCheckerThread(QThread):
    """Thread for checking updates without blocking UI"""
    update_found = pyqtSignal(dict)
    no_update = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.updater = AutoUpdater()
    
    def run(self):
        try:
            has_update, update_info = self.updater.check_for_updates()
            if has_update:
                self.update_found.emit(update_info)
            else:
                self.no_update.emit()
        except Exception as e:
            self.error.emit(str(e))


class UpdateInstallerThread(QThread):
    """Thread for installing updates without blocking UI"""
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, update_info):
        super().__init__()
        self.updater = AutoUpdater()
        self.update_info = update_info
    
    def run(self):
        try:
            def progress_callback(percent, message):
                self.progress.emit(percent, message)
            
            success, message = self.updater.perform_update(
                self.update_info,
                progress_callback
            )
            self.finished.emit(success, message)
        except Exception as e:
            self.finished.emit(False, str(e))


class UpdateDialog(QDialog):
    """Dialog for checking and installing updates"""
    
    def __init__(self, parent=None, auto_check=False):
        super().__init__(parent)
        self.setWindowTitle("Check for Updates")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        
        self.update_info = None
        self.init_ui()
        
        if auto_check:
            self.check_for_updates()
    
    def init_ui(self):
        """Initialize the update dialog UI"""
        layout = QVBoxLayout()
        
        # Current version
        version_layout = QHBoxLayout()
        version_layout.addWidget(QLabel("Current Version:"))
        self.current_version_label = QLabel("1.1.0")
        self.current_version_label.setStyleSheet("font-weight: bold;")
        version_layout.addWidget(self.current_version_label)
        version_layout.addStretch()
        layout.addLayout(version_layout)
        
        # Status label
        self.status_label = QLabel("Click 'Check for Updates' to begin")
        self.status_label.setStyleSheet("font-size: 12px; color: #aaa;")
        layout.addWidget(self.status_label)
        
        # Update info section (hidden initially)
        self.update_info_widget = QWidget()
        update_info_layout = QVBoxLayout()
        
        self.new_version_label = QLabel("")
        self.new_version_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #4caf50;")
        update_info_layout.addWidget(self.new_version_label)
        
        changelog_label = QLabel("What's New:")
        changelog_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        update_info_layout.addWidget(changelog_label)
        
        self.changelog_display = QTextEdit()
        self.changelog_display.setReadOnly(True)
        self.changelog_display.setMaximumHeight(200)
        update_info_layout.addWidget(self.changelog_display)
        
        self.update_info_widget.setLayout(update_info_layout)
        self.update_info_widget.hide()
        layout.addWidget(self.update_info_widget)
        
        # Progress bar (hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet("font-size: 10px; color: #aaa;")
        self.progress_label.hide()
        layout.addWidget(self.progress_label)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.check_button = QPushButton("Check for Updates")
        self.check_button.clicked.connect(self.check_for_updates)
        self.check_button.setMinimumWidth(150)
        button_layout.addWidget(self.check_button)
        
        self.install_button = QPushButton("Install Update")
        self.install_button.clicked.connect(self.install_update)
        self.install_button.setMinimumWidth(150)
        self.install_button.hide()
        button_layout.addWidget(self.install_button)
        
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.reject)
        self.close_button.setMinimumWidth(100)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def check_for_updates(self):
        """Check for available updates"""
        self.status_label.setText("Checking for updates...")
        self.check_button.setEnabled(False)
        
        # Start checker thread
        self.checker_thread = UpdateCheckerThread()
        self.checker_thread.update_found.connect(self.on_update_found)
        self.checker_thread.no_update.connect(self.on_no_update)
        self.checker_thread.error.connect(self.on_check_error)
        self.checker_thread.start()
    
    def on_update_found(self, update_info):
        """Handle update found"""
        self.update_info = update_info
        self.status_label.setText("Update available!")
        
        new_version = update_info.get('version', 'Unknown')
        self.new_version_label.setText(f"New Version Available: {new_version}")
        
        # Load and display changelog
        updater = AutoUpdater()
        changelog = updater.get_changelog(update_info)
        self.changelog_display.setPlainText(changelog)
        
        # Show update info and install button
        self.update_info_widget.show()
        self.install_button.show()
        self.check_button.setEnabled(True)
    
    def on_no_update(self):
        """Handle no update available"""
        self.status_label.setText("You're already on the latest version!")
        self.check_button.setEnabled(True)
        
        QMessageBox.information(
            self,
            "No Updates",
            "You're already running the latest version of Crypto Futures Bot!"
        )
    
    def on_check_error(self, error):
        """Handle error checking for updates"""
        self.status_label.setText(f"Error: {error}")
        self.check_button.setEnabled(True)
        
        QMessageBox.warning(
            self,
            "Update Check Failed",
            f"Failed to check for updates:\n\n{error}\n\n"
            "Please check your internet connection and try again."
        )
    
    def install_update(self):
        """Install the available update"""
        reply = QMessageBox.question(
            self,
            "Install Update",
            f"Install update to version {self.update_info.get('version')}?\n\n"
            "The application will need to restart after the update.\n"
            "A backup will be created automatically.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.No:
            return
        
        # Disable buttons
        self.check_button.setEnabled(False)
        self.install_button.setEnabled(False)
        
        # Show progress
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self.progress_label.show()
        
        self.status_label.setText("Installing update...")
        
        # Start installer thread
        self.installer_thread = UpdateInstallerThread(self.update_info)
        self.installer_thread.progress.connect(self.on_install_progress)
        self.installer_thread.finished.connect(self.on_install_finished)
        self.installer_thread.start()
    
    def on_install_progress(self, percent, message):
        """Handle installation progress"""
        self.progress_bar.setValue(percent)
        self.progress_label.setText(message)
    
    def on_install_finished(self, success, message):
        """Handle installation completion"""
        self.progress_bar.hide()
        self.progress_label.hide()
        
        if success:
            QMessageBox.information(
                self,
                "Update Complete",
                f"{message}\n\n"
                "The application will now restart to complete the update.\n\n"
                "Click OK to restart."
            )
            
            # Signal parent to restart
            self.accept()
            
            # Request application restart
            from PyQt6.QtWidgets import QApplication
            QApplication.quit()
            
        else:
            QMessageBox.critical(
                self,
                "Update Failed",
                f"{message}\n\n"
                "The application was not updated.\n"
                "You can restore from the backup if needed."
            )
            
            self.status_label.setText("Update failed")
            self.check_button.setEnabled(True)
            self.install_button.setEnabled(True)
