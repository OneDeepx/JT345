"""
Main Application Window
"""
from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QStatusBar, QMenuBar, QMenu
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction

from ui.tabs.bot_tab import BotTab
from ui.tabs.manual_trade_tab import ManualTradeTab
from ui.tabs.charts_tab import ChartsTab
from ui.tabs.news_tab import NewsTab
from ui.tabs.strategy_adjuster_tab import StrategyAdjusterTab
from ui.tabs.strategy_tester_tab import StrategyTesterTab
from ui.tabs.developer_tab import DeveloperTab
from ui.styles.theme import apply_dark_theme
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger('main_window')


class MainWindow(QMainWindow):
    """Main application window with tabbed interface"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crypto Futures Auto Trading Bot")
        self.setGeometry(100, 100, 1600, 900)
        
        # Apply theme
        apply_dark_theme(self)
        
        # Create UI components
        self._create_menu_bar()
        self._create_tabs()
        self._create_status_bar()
        
        # Setup update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_ui)
        update_interval = settings.get('ui.update_interval', 1000)
        self.update_timer.start(update_interval)
        
        logger.info("Main window initialized")
    
    def _create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        settings_action = QAction('Settings', self)
        settings_action.triggered.connect(self._open_settings)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        check_updates_action = QAction('Check for Updates...', self)
        check_updates_action.triggered.connect(self._check_for_updates)
        file_menu.addAction(check_updates_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Trading menu
        trading_menu = menubar.addMenu('Trading')
        
        toggle_paper = QAction('Toggle Paper Trading', self)
        toggle_paper.triggered.connect(self._toggle_paper_trading)
        trading_menu.addAction(toggle_paper)
        
        toggle_auto = QAction('Toggle Auto Trading', self)
        toggle_auto.triggered.connect(self._toggle_auto_trading)
        trading_menu.addAction(toggle_auto)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        docs_action = QAction('Documentation', self)
        docs_action.triggered.connect(self._open_docs)
        help_menu.addAction(docs_action)
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _create_tabs(self):
        """Create tabbed interface"""
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Create tabs
        self.bot_tab = BotTab()
        self.manual_tab = ManualTradeTab()
        self.charts_tab = ChartsTab()
        self.news_tab = NewsTab()
        self.strategy_adjuster_tab = StrategyAdjusterTab()
        self.strategy_tester_tab = StrategyTesterTab()
        self.developer_tab = DeveloperTab()
        
        # Add tabs to widget
        self.tabs.addTab(self.bot_tab, "Bot")
        self.tabs.addTab(self.manual_tab, "Manual Trades")
        self.tabs.addTab(self.charts_tab, "Charts")
        self.tabs.addTab(self.news_tab, "News")
        self.tabs.addTab(self.strategy_adjuster_tab, "Strategy Adjuster")
        self.tabs.addTab(self.strategy_tester_tab, "Strategy Tester")
        self.tabs.addTab(self.developer_tab, "Developer")
    
    def _create_status_bar(self):
        """Create status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Initial status
        mode = "PAPER" if settings.get('trading.paper_trading', True) else "LIVE"
        auto = "ON" if settings.get('trading.auto_trading_enabled', False) else "OFF"
        self.status_bar.showMessage(f"Mode: {mode} | Auto Trading: {auto} | Ready")
    
    def _update_ui(self):
        """Update UI components periodically"""
        # Update each tab
        try:
            current_tab = self.tabs.currentWidget()
            if hasattr(current_tab, 'update_display'):
                current_tab.update_display()
        except Exception as e:
            logger.error(f"Error updating UI: {e}")
    
    def _toggle_paper_trading(self):
        """Toggle between paper and live trading"""
        current = settings.get('trading.paper_trading', True)
        settings.set('trading.paper_trading', not current)
        
        mode = "PAPER" if not current else "LIVE"
        self.status_bar.showMessage(f"Switched to {mode} trading mode")
        logger.info(f"Trading mode changed to: {mode}")
    
    def _toggle_auto_trading(self):
        """Toggle auto trading on/off"""
        current = settings.get('trading.auto_trading_enabled', False)
        settings.set('trading.auto_trading_enabled', not current)
        
        status = "ENABLED" if not current else "DISABLED"
        self.status_bar.showMessage(f"Auto trading {status}")
        logger.info(f"Auto trading {status}")
    
    def _open_settings(self):
        """Open settings dialog"""
        from ui.settings_dialog import SettingsDialog
        dialog = SettingsDialog(self)
        if dialog.exec():
            # Settings were saved, update status bar
            mode = "PAPER" if settings.get('trading.paper_trading', True) else "LIVE"
            auto = "ON" if settings.get('trading.auto_trading_enabled', False) else "OFF"
            self.status_bar.showMessage(f"Mode: {mode} | Auto Trading: {auto} | Settings Updated")
            logger.info("Settings updated by user")
    
    def _check_for_updates(self):
        """Check for software updates"""
        from ui.update_dialog import UpdateDialog
        dialog = UpdateDialog(self, auto_check=True)
        dialog.exec()
    
    def _open_docs(self):
        """Open documentation"""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Documentation", "Documentation coming soon!")
    
    def _show_about(self):
        """Show about dialog"""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            "About Crypto Futures Bot",
            "Crypto Futures Auto Trading Bot v1.0\n\n"
            "AI-powered cryptocurrency futures trading\n"
            "with continuous learning capabilities.\n\n"
            "Powered by Claude AI"
        )
    
    def closeEvent(self, event):
        """Handle window close event"""
        from PyQt6.QtWidgets import QMessageBox
        
        # Check if auto trading is enabled
        auto_enabled = settings.get('trading.auto_trading_enabled', False)
        is_paper = settings.get('trading.paper_trading', True)
        
        if auto_enabled and not is_paper:
            message = (
                'Are you sure you want to exit?\n\n'
                '⚠️ WARNING: Auto trading is ENABLED in LIVE mode!\n'
                'All open positions will remain active on Binance.\n\n'
                'Consider closing all positions before exiting.'
            )
        elif auto_enabled:
            message = (
                'Are you sure you want to exit?\n\n'
                'Auto trading in paper mode will stop.\n'
                'No real positions will be affected.'
            )
        else:
            message = (
                'Are you sure you want to exit?\n\n'
                'The application will close but any open positions\n'
                'on Binance will remain active.'
            )
        
        reply = QMessageBox.question(
            self,
            'Exit Crypto Futures Bot',
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            logger.info("Application closing...")
            event.accept()
        else:
            event.ignore()
