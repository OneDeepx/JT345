"""
Setup and Installation Script
Run this after installing dependencies to configure the application
"""
import os
import sys
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        'data',
        'logs',
        'database',
        'config',
        'strategies',
        'backtest_results'
    ]
    
    print("Creating directories...")
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"  ✓ {directory}/")

def check_dependencies():
    """Check if all dependencies are installed"""
    print("\nChecking dependencies...")
    
    required = [
        'anthropic',
        'PyQt6',
        'pandas',
        'numpy',
        'binance',
        'ccxt',
        'sqlalchemy',
        'cryptography',
        'loguru'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - MISSING")
            missing.append(package)
    
    # Special check for TA-Lib
    try:
        import talib
        print(f"  ✓ talib")
    except ImportError:
        print(f"  ✗ talib - MISSING (requires special installation)")
        print(f"    See README.md for TA-Lib installation instructions")
        missing.append('talib')
    
    return missing

def create_config_template():
    """Create configuration template"""
    config_file = Path('config/api_config_template.txt')
    
    if not config_file.exists():
        print("\nCreating API configuration template...")
        config_file.write_text("""
# API Configuration Template
# Copy this to the application settings

[Anthropic Claude]
API Key: your-claude-api-key-here
Get from: https://console.anthropic.com

[Binance Futures]
API Key: your-binance-api-key
API Secret: your-binance-api-secret
Get from: https://www.binance.com/en/my/settings/api-management

[TradingView]
Username: your-username
Password: your-password
(Optional - can use Binance data instead)

[CryptoPanic]
API Key: your-cryptopanic-api-key
Get from: https://cryptopanic.com/developers/api/

SECURITY NOTES:
- Never share your API keys
- Enable IP whitelist on Binance
- Use trading-only permissions
- Enable 2FA on exchange accounts
- Keep this file secure
""")
        print(f"  ✓ Created {config_file}")

def create_example_strategy():
    """Create example strategy file"""
    strategy_file = Path('strategies/example_strategy.txt')
    
    if not strategy_file.exists():
        print("\nCreating example strategy...")
        strategy_file.write_text("""
# Example Trading Strategy
# This is a template - customize for your needs

STRATEGY NAME: RSI Reversal Strategy

ENTRY CONDITIONS:
1. RSI < 30 (Oversold) for Long
   RSI > 70 (Overbought) for Short
2. Price above 50 EMA for Long
   Price below 50 EMA for Short
3. Volume > 20% above 20-period average
4. Sentiment score >= +3 for Long
   Sentiment score <= -3 for Short
5. Bullish/Bearish candlestick pattern confirmation

EXIT CONDITIONS:
1. Take Profit: 2% from entry
2. Stop Loss: 1% from entry (50% of TP)
3. Time-based: Close position after 24 hours if no TP/SL hit
4. Sentiment reversal: If sentiment changes by 4 points

RISK MANAGEMENT:
- Position size: 1% of total capital
- Maximum concurrent positions: 3
- Never add to losing positions
- Respect daily loss limit: 3%

MARKET CONDITIONS:
- Best in trending markets
- Avoid during major news events
- Check Bitcoin dominance
- Monitor funding rates

TIMEFRAME:
- Primary: 15-minute chart
- Confirmation: 1-hour chart

INDICATORS:
- RSI (14 period)
- EMA (50, 200)
- Volume MA (20 period)
- ATR for volatility

NOTES:
- This strategy works best in volatile markets
- Backtest thoroughly before live trading
- Adjust parameters based on market conditions
- Always start with paper trading
""")
        print(f"  ✓ Created {strategy_file}")

def check_python_version():
    """Check Python version"""
    print("\nChecking Python version...")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 11:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor}.{version.micro}")
        print(f"    Python 3.11+ required")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("Crypto Futures Trading Bot - Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Setup failed: Python 3.11+ required")
        return False
    
    # Create directories
    create_directories()
    
    # Check dependencies
    missing = check_dependencies()
    
    # Create configuration files
    create_config_template()
    create_example_strategy()
    
    print("\n" + "=" * 60)
    
    if missing:
        print("⚠️  Setup completed with warnings")
        print("\nMissing dependencies:")
        for package in missing:
            print(f"  - {package}")
        print("\nInstall missing packages:")
        print("  pip install -r requirements.txt")
        if 'talib' in missing:
            print("\nFor TA-Lib, see special installation instructions in README.md")
    else:
        print("✅ Setup completed successfully!")
    
    print("\nNext steps:")
    print("1. Review config/api_config_template.txt")
    print("2. Get your API keys from the services")
    print("3. Run the application: python main.py")
    print("4. Configure API keys in Settings")
    print("5. Start with paper trading mode")
    print("6. Check out strategies/example_strategy.txt")
    print("7. Use the Developer tab for help")
    
    print("\n" + "=" * 60)
    
    return len(missing) == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
