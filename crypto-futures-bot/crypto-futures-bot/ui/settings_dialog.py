"""
Settings Dialog - Functional API Key Configuration
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTabWidget, QWidget,
    QGroupBox, QFormLayout, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger('settings_dialog')


class SettingsDialog(QDialog):
    """Settings dialog for configuring API keys and preferences"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """Initialize the settings UI"""
        layout = QVBoxLayout()
        
        # Create tabs
        tabs = QTabWidget()
        
        # API Keys Tab
        api_tab = self.create_api_keys_tab()
        tabs.addTab(api_tab, "API Keys")
        
        # Trading Tab
        trading_tab = self.create_trading_tab()
        tabs.addTab(trading_tab, "Trading")
        
        # General Tab
        general_tab = self.create_general_tab()
        tabs.addTab(general_tab, "General")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setMinimumWidth(100)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setMinimumWidth(100)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def create_api_keys_tab(self):
        """Create API keys configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Claude API
        claude_group = QGroupBox("Anthropic Claude API")
        claude_layout = QFormLayout()
        
        self.claude_key_input = QLineEdit()
        self.claude_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.claude_key_input.setPlaceholderText("sk-ant-...")
        claude_layout.addRow("API Key:", self.claude_key_input)
        
        claude_info = QLabel("Get your API key from: console.anthropic.com")
        claude_info.setStyleSheet("color: #aaaaaa; font-size: 10px;")
        claude_layout.addRow("", claude_info)
        
        claude_group.setLayout(claude_layout)
        layout.addWidget(claude_group)
        
        # Binance API
        binance_group = QGroupBox("Binance Futures API")
        binance_layout = QFormLayout()
        
        self.binance_key_input = QLineEdit()
        self.binance_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.binance_key_input.setPlaceholderText("Your Binance API Key")
        binance_layout.addRow("API Key:", self.binance_key_input)
        
        self.binance_secret_input = QLineEdit()
        self.binance_secret_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.binance_secret_input.setPlaceholderText("Your Binance API Secret")
        binance_layout.addRow("API Secret:", self.binance_secret_input)
        
        binance_info = QLabel(
            "Get from: binance.com → Account → API Management\n"
            "⚠️ Enable 'Futures' permission and use IP whitelist!"
        )
        binance_info.setStyleSheet("color: #aaaaaa; font-size: 10px;")
        binance_layout.addRow("", binance_info)
        
        binance_group.setLayout(binance_layout)
        layout.addWidget(binance_group)
        
        # CryptoPanic API
        cryptopanic_group = QGroupBox("CryptoPanic API")
        cryptopanic_layout = QFormLayout()
        
        self.cryptopanic_key_input = QLineEdit()
        self.cryptopanic_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.cryptopanic_key_input.setPlaceholderText("Your CryptoPanic API Key")
        cryptopanic_layout.addRow("API Key:", self.cryptopanic_key_input)
        
        # Test button
        test_crypto_btn = QPushButton("Test Connection")
        test_crypto_btn.clicked.connect(self.test_cryptopanic_connection)
        cryptopanic_layout.addRow("", test_crypto_btn)
        
        cryptopanic_info = QLabel("Get from: cryptopanic.com/developers/api/")
        cryptopanic_info.setStyleSheet("color: #aaaaaa; font-size: 10px;")
        cryptopanic_layout.addRow("", cryptopanic_info)
        
        cryptopanic_group.setLayout(cryptopanic_layout)
        layout.addWidget(cryptopanic_group)
        
        # TradingView (Optional)
        tradingview_group = QGroupBox("TradingView (Optional)")
        tradingview_layout = QFormLayout()
        
        self.tradingview_username_input = QLineEdit()
        self.tradingview_username_input.setPlaceholderText("Username")
        tradingview_layout.addRow("Username:", self.tradingview_username_input)
        
        self.tradingview_password_input = QLineEdit()
        self.tradingview_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.tradingview_password_input.setPlaceholderText("Password")
        tradingview_layout.addRow("Password:", self.tradingview_password_input)
        
        tradingview_info = QLabel("Optional - Can use Binance data instead")
        tradingview_info.setStyleSheet("color: #aaaaaa; font-size: 10px;")
        tradingview_layout.addRow("", tradingview_info)
        
        tradingview_group.setLayout(tradingview_layout)
        layout.addWidget(tradingview_group)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_trading_tab(self):
        """Create trading configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Trading Mode
        mode_group = QGroupBox("Trading Mode")
        mode_layout = QFormLayout()
        
        self.paper_trading_checkbox = QCheckBox("Enable Paper Trading (Recommended)")
        self.paper_trading_checkbox.setChecked(True)
        mode_layout.addRow("", self.paper_trading_checkbox)
        
        mode_info = QLabel("Paper trading uses simulated money. Always test strategies here first!")
        mode_info.setStyleSheet("color: #aaaaaa; font-size: 10px;")
        mode_info.setWordWrap(True)
        mode_layout.addRow("", mode_info)
        
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)
        
        # Auto Trading
        auto_group = QGroupBox("Auto Trading")
        auto_layout = QFormLayout()
        
        self.auto_trading_checkbox = QCheckBox("Enable Auto Trading")
        self.auto_trading_checkbox.setChecked(False)
        auto_layout.addRow("", self.auto_trading_checkbox)
        
        auto_info = QLabel("⚠️ Only enable after thorough testing in paper mode!")
        auto_info.setStyleSheet("color: #ff9800; font-size: 10px;")
        auto_layout.addRow("", auto_info)
        
        auto_group.setLayout(auto_layout)
        layout.addWidget(auto_group)
        
        # Symbol Selection
        symbol_group = QGroupBox("Default Symbol")
        symbol_layout = QFormLayout()
        
        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("BTCUSDT")
        symbol_layout.addRow("Symbol:", self.symbol_input)
        
        symbol_info = QLabel("Available: BTCUSDT, ETHUSDT, BNBUSDT, etc.")
        symbol_info.setStyleSheet("color: #aaaaaa; font-size: 10px;")
        symbol_layout.addRow("", symbol_info)
        
        symbol_group.setLayout(symbol_layout)
        layout.addWidget(symbol_group)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_general_tab(self):
        """Create general settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # UI Settings
        ui_group = QGroupBox("User Interface")
        ui_layout = QFormLayout()
        
        self.update_interval_input = QLineEdit()
        self.update_interval_input.setPlaceholderText("1000")
        ui_layout.addRow("Update Interval (ms):", self.update_interval_input)
        
        ui_info = QLabel("How often to refresh the UI (1000ms = 1 second)")
        ui_info.setStyleSheet("color: #aaaaaa; font-size: 10px;")
        ui_layout.addRow("", ui_info)
        
        ui_group.setLayout(ui_layout)
        layout.addWidget(ui_group)
        
        # Security Info
        security_group = QGroupBox("Security Information")
        security_layout = QVBoxLayout()
        
        security_info = QLabel(
            "🔒 All API keys are encrypted using Fernet encryption\n"
            "🔒 Keys are stored locally in config/api_keys.enc\n"
            "🔒 Never share your API keys or config files\n"
            "🔒 Use IP whitelist on Binance for extra security\n"
            "🔒 Enable 2FA on all exchange accounts"
        )
        security_info.setWordWrap(True)
        security_info.setStyleSheet("color: #4caf50; font-size: 10px;")
        security_layout.addWidget(security_info)
        
        security_group.setLayout(security_layout)
        layout.addWidget(security_group)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def load_settings(self):
        """Load current settings into the dialog"""
        try:
            # Load API keys
            claude_keys = settings.get_api_key('claude')
            if claude_keys.get('key'):
                self.claude_key_input.setText(claude_keys['key'])
            
            binance_keys = settings.get_api_key('binance')
            if binance_keys.get('key'):
                self.binance_key_input.setText(binance_keys['key'])
            if binance_keys.get('secret'):
                self.binance_secret_input.setText(binance_keys['secret'])
            
            cryptopanic_keys = settings.get_api_key('cryptopanic')
            if cryptopanic_keys.get('key'):
                self.cryptopanic_key_input.setText(cryptopanic_keys['key'])
            
            tradingview_keys = settings.get_api_key('tradingview')
            if tradingview_keys.get('key'):
                self.tradingview_username_input.setText(tradingview_keys['key'])
            if tradingview_keys.get('secret'):
                self.tradingview_password_input.setText(tradingview_keys['secret'])
            
            # Load trading settings
            paper_trading = settings.get('trading.paper_trading', True)
            self.paper_trading_checkbox.setChecked(paper_trading)
            
            auto_trading = settings.get('trading.auto_trading_enabled', False)
            self.auto_trading_checkbox.setChecked(auto_trading)
            
            symbol = settings.get('trading.symbol', 'BTCUSDT')
            self.symbol_input.setText(symbol)
            
            # Load general settings
            update_interval = settings.get('ui.update_interval', 1000)
            self.update_interval_input.setText(str(update_interval))
            
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings and API keys"""
        try:
            # Save API keys (only if not empty)
            claude_key = self.claude_key_input.text().strip()
            if claude_key:
                settings.save_api_key('claude', claude_key)
                logger.info("Claude API key saved")
            
            binance_key = self.binance_key_input.text().strip()
            binance_secret = self.binance_secret_input.text().strip()
            if binance_key and binance_secret:
                settings.save_api_key('binance', binance_key, binance_secret)
                logger.info("Binance API keys saved")
            
            cryptopanic_key = self.cryptopanic_key_input.text().strip()
            if cryptopanic_key:
                settings.save_api_key('cryptopanic', cryptopanic_key)
                logger.info("CryptoPanic API key saved")
            
            tradingview_username = self.tradingview_username_input.text().strip()
            tradingview_password = self.tradingview_password_input.text().strip()
            if tradingview_username and tradingview_password:
                settings.save_api_key('tradingview', tradingview_username, tradingview_password)
                logger.info("TradingView credentials saved")
            
            # Save trading settings
            settings.set('trading.paper_trading', self.paper_trading_checkbox.isChecked())
            settings.set('trading.auto_trading_enabled', self.auto_trading_checkbox.isChecked())
            settings.set('trading.symbol', self.symbol_input.text().strip() or 'BTCUSDT')
            
            # Save general settings
            try:
                update_interval = int(self.update_interval_input.text().strip() or 1000)
                settings.set('ui.update_interval', update_interval)
            except ValueError:
                settings.set('ui.update_interval', 1000)
            
            QMessageBox.information(
                self,
                "Settings Saved",
                "Settings and API keys have been saved successfully!\n\n"
                "API keys are encrypted and stored securely."
            )
            
            self.accept()
            
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to save settings:\n{str(e)}"
            )
    
    def test_cryptopanic_connection(self):
        """Test CryptoPanic API connection"""
        api_key = self.cryptopanic_key_input.text().strip()
        
        if not api_key:
            QMessageBox.warning(
                self,
                "No API Key",
                "Please enter your CryptoPanic API key first."
            )
            return
        
        # Temporarily save the key and test
        try:
            settings.save_api_key('cryptopanic', api_key)
            
            # Import and test
            from apis.cryptopanic_api import CryptoPanicAPI
            test_api = CryptoPanicAPI()
            
            success, message = test_api.test_connection()
            
            if success:
                QMessageBox.information(
                    self,
                    "Connection Successful",
                    f"✅ {message}\n\n"
                    "Your CryptoPanic API key is working correctly!"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Connection Failed",
                    f"❌ {message}\n\n"
                    "Please check your API key and try again."
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Test Failed",
                f"Error testing connection:\n{str(e)}"
            )
