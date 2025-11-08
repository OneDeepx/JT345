"""
Crypto Futures Auto Trading Bot
Main Application Entry Point
"""
import sys
import signal
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings, LOGS_DIR
from ui.main_window import MainWindow
from utils.logger import setup_logger

# Setup logging
logger = setup_logger('main', LOGS_DIR / 'app.log')


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    logger.info("Shutdown signal received, cleaning up...")
    QApplication.quit()


def main():
    """Main application entry point"""
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    logger.info("=" * 60)
    logger.info("Starting Crypto Futures Auto Trading Bot")
    logger.info("=" * 60)
    
    # Create Qt Application
    app = QApplication(sys.argv)
    app.setApplicationName("Crypto Futures Bot")
    
    # High DPI support is automatic in PyQt6
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    logger.info("Application window opened")
    
    # Run application
    exit_code = app.exec()
    
    logger.info("Application closed")
    return exit_code


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)
