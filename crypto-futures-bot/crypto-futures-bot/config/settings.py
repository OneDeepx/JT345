"""
Application Settings Management
"""
import os
import json
from pathlib import Path
from typing import Any
from cryptography.fernet import Fernet

# Application paths
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / 'config'
DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = BASE_DIR / 'logs'
DB_DIR = BASE_DIR / 'database'

# Create directories if they don't exist
for directory in [DATA_DIR, LOGS_DIR, DB_DIR, CONFIG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Database
DATABASE_PATH = DB_DIR / 'trading_bot.db'

# API Configuration
API_RATE_LIMITS = {
    'binance': 1200,  # requests per minute
    'tradingview': 100,
    'cryptopanic': 30,
    'claude': 50
}

# Trading Configuration
DEFAULT_SYMBOL = 'BTCUSDT'
SUPPORTED_SYMBOLS = [
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 
    'SOLUSDT', 'XRPUSDT', 'DOGEUSDT', 'DOTUSDT'
]

# Technical Analysis
TA_TIMEFRAMES = ['1m', '5m', '15m', '1h', '4h', '1d']
DEFAULT_TIMEFRAME = '15m'

# Indicators
INDICATORS = {
    'RSI': {'period': 14, 'overbought': 70, 'oversold': 30},
    'MACD': {'fast': 12, 'slow': 26, 'signal': 9},
    'EMA': {'periods': [9, 21, 50, 200]},
    'BBANDS': {'period': 20, 'std_dev': 2},
    'ATR': {'period': 14},
    'VOLUME': {'ma_period': 20}
}

# Sentiment Analysis
SENTIMENT_SOURCES = ['cryptopanic', 'orderbook', 'volume']
SENTIMENT_WEIGHTS = {
    'news': 0.4,
    'orderbook': 0.3,
    'volume': 0.3
}

# Paper Trading
PAPER_TRADING_ENABLED = True  # Start in paper mode
PAPER_TRADING_INITIAL_BALANCE = 10000  # USD

# Backtesting
BACKTEST_START_DATE = '2024-01-01'
BACKTEST_SLIPPAGE = 0.001  # 0.1%
BINANCE_FUTURES_FEE = 0.0004  # 0.04% maker/taker

# UI Configuration
UI_UPDATE_INTERVAL = 1000  # milliseconds
CHART_CANDLESTICK_COUNT = 100

# Logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}'
LOG_ROTATION = '100 MB'

# Security
ENCRYPTION_KEY_FILE = CONFIG_DIR / '.key'


class Settings:
    """Settings manager with encryption support"""
    
    def __init__(self):
        self.settings_file = CONFIG_DIR / 'settings.json'
        self.api_keys_file = CONFIG_DIR / 'api_keys.enc'
        self._encryption_key = self._load_or_create_key()
        self._cipher = Fernet(self._encryption_key)
        self.settings = self._load_settings()
    
    def _load_or_create_key(self) -> bytes:
        """Load or create encryption key"""
        if ENCRYPTION_KEY_FILE.exists():
            return ENCRYPTION_KEY_FILE.read_bytes()
        else:
            key = Fernet.generate_key()
            ENCRYPTION_KEY_FILE.write_bytes(key)
            # Set file permissions to read-only for owner
            os.chmod(ENCRYPTION_KEY_FILE, 0o400)
            return key
    
    def _load_settings(self) -> dict:
        """Load settings from file"""
        if self.settings_file.exists():
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        return self._default_settings()
    
    def _default_settings(self) -> dict:
        """Return default settings"""
        return {
            'trading': {
                'symbol': DEFAULT_SYMBOL,
                'timeframe': DEFAULT_TIMEFRAME,
                'paper_trading': PAPER_TRADING_ENABLED,
                'auto_trading_enabled': False
            },
            'risk': {
                'max_risk_percent': 0.01,
                'max_positions': 5
            },
            'ui': {
                'theme': 'dark',
                'update_interval': UI_UPDATE_INTERVAL
            }
        }
    
    def save_settings(self):
        """Save settings to file"""
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get setting value by dot-notation path"""
        keys = key_path.split('.')
        value = self.settings
        for key in keys:
            value = value.get(key, {})
            if value == {}:
                return default
        return value if value != {} else default
    
    def set(self, key_path: str, value: Any):
        """Set setting value by dot-notation path"""
        keys = key_path.split('.')
        setting = self.settings
        for key in keys[:-1]:
            if key not in setting:
                setting[key] = {}
            setting = setting[key]
        setting[keys[-1]] = value
        self.save_settings()
    
    def save_api_key(self, service: str, key: str, secret: str = None):
        """Save encrypted API key"""
        api_keys = self._load_api_keys()
        api_keys[service] = {'key': key, 'secret': secret}
        
        encrypted_data = self._cipher.encrypt(json.dumps(api_keys).encode())
        self.api_keys_file.write_bytes(encrypted_data)
        os.chmod(self.api_keys_file, 0o400)
    
    def get_api_key(self, service: str) -> dict:
        """Get decrypted API key"""
        api_keys = self._load_api_keys()
        return api_keys.get(service, {'key': None, 'secret': None})
    
    def _load_api_keys(self) -> dict:
        """Load and decrypt API keys"""
        if not self.api_keys_file.exists():
            return {}
        
        encrypted_data = self.api_keys_file.read_bytes()
        decrypted_data = self._cipher.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())


# Global settings instance
settings = Settings()
