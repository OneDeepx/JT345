# Crypto Futures Auto Trading Bot

An AI-powered cryptocurrency futures trading application with auto-trading, manual trading, backtesting, and continuous learning capabilities. Built with PyQt6 and integrated with Claude AI for intelligent debugging and assistance.

## 🌟 Features

### Core Trading Features
- ✅ **Auto Trading**: AI-driven automated trading with configurable strategies
- ✅ **Manual Trading**: Intuitive interface for manual futures trading
- ✅ **Paper Trading**: Risk-free testing with simulated trading
- ✅ **Backtesting**: Test strategies on historical data
- ✅ **Live Data Integration**: Real-time data from TradingView and Binance
- ✅ **Risk Management**: Built-in 1% capital risk limit and stop loss controls

### AI & Intelligence
- 🤖 **Claude AI Assistant**: In-app debugging and code assistance
- 📚 **Document Learning**: Train bot with PDF, Word, Excel uploads
- 🧠 **Continuous Learning**: Adapts to market conditions over time
- 📊 **Strategy Testing**: Validate strategies before deployment

### Analysis & Indicators
- 📈 **Technical Analysis**: RSI, MACD, EMA, Bollinger Bands, ATR
- 📊 **Volume Analysis**: Volume profile and order book depth
- 😊 **Sentiment Analysis**: Multi-source sentiment scoring (-4 to +4)
- 🎯 **Chart Patterns**: Automatic detection of formations

### Safety & Core Rules (Immutable)
1. **Sentiment Threshold**: Only trade when sentiment is ≥ +3 or ≤ -3
2. **Maximum Risk**: Hard limit of 1% capital per trade
3. **Stop Loss Rule**: Stop loss must be ≤ 50% of take profit

## 📋 Requirements

### System Requirements
- **OS**: Windows 10/11, Linux, macOS
- **Python**: 3.11 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 2GB free space
- **Internet**: Stable connection for API calls

### API Keys Required
1. **Anthropic Claude API** - For AI assistant
2. **Binance Futures API** - For trading execution
3. **TradingView** - For chart data (optional)
4. **CryptoPanic API** - For news sentiment

## 🚀 Installation

### Step 1: Clone or Download
```bash
# If you have git
git clone <repository-url>
cd crypto-futures-bot

# Or download and extract the ZIP file
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install TA-Lib
TA-Lib requires special installation:

**Windows:**
1. Download wheel from: https://github.com/cgohlke/talib-build/releases
2. Install: `pip install TA_Lib‑0.4.28‑cp311‑cp311‑win_amd64.whl`

**Linux:**
```bash
sudo apt-get install ta-lib
pip install TA-Lib
```

**macOS:**
```bash
brew install ta-lib
pip install TA-Lib
```

### Step 5: Configure API Keys

Run the application for the first time:
```bash
python main.py
```

Go to **File → Settings** and enter your API keys:
- Claude API Key (from console.anthropic.com)
- Binance API Key & Secret (from binance.com)
- TradingView credentials (optional)
- CryptoPanic API Key (from cryptopanic.com)

⚠️ **Security**: API keys are encrypted and stored locally.

## 🎯 Quick Start

### First Launch
1. Launch the application: `python main.py`
2. You'll start in **Paper Trading** mode (safe!)
3. Configure your API keys in Settings
4. Start with the **Developer** tab to test Claude integration

### Basic Workflow
1. **Developer Tab**: Ask Claude for help anytime
2. **Strategy Adjuster**: Upload your trading strategy (PDF/Word/Excel)
3. **Strategy Tester**: Backtest your strategy
4. **Bot Tab**: Monitor automated trading
5. **Manual Trades**: Execute manual trades when needed

### Testing Your Strategy
1. Create a strategy document describing your approach
2. Upload it in **Strategy Adjuster** tab
3. Go to **Strategy Tester** tab
4. Run backtest on historical data
5. Review profitability and feasibility checks
6. Enable live paper trading to test with real-time data

### Going Live (Use with Caution!)
1. Verify everything works in paper trading mode
2. Start with small capital
3. Go to **File → Toggle Paper Trading**
4. Monitor closely in the **Bot** tab
5. Use **Close All Trades** button for emergency exits

## 📚 Usage Guide

### Auto Trading Bot

The bot follows this decision flow for every trade:

```
1. Collect market data from all sources
2. Calculate sentiment score (-4 to +4)
   ├─ If |sentiment| < 3 → Skip trade
   └─ If |sentiment| >= 3 → Continue
3. Analyze technical indicators and patterns
   ├─ If no valid setup → Skip trade
   └─ If valid setup → Continue
4. Analyze volume and order book
   ├─ If volume doesn't support → Skip trade
   └─ If volume supports → Continue
5. Calculate position size (1% of capital)
6. Verify stop loss <= 50% of take profit
   ├─ If not satisfied → Skip trade
   └─ If satisfied → Execute trade
```

### Manual Trading

**Opening a Position:**
1. Go to **Manual Trades** tab
2. Select Long or Short
3. Enter percentage of portfolio (e.g., "1" = 1%)
4. Bot automatically calculates position size
5. Click "Open Position"

**Closing Positions:**
- Individual: Click "Close" next to position
- All at once: Click "Close All Trades"

### Developer Console (Claude AI)

Ask Claude anything:
- "Why is this error occurring?"
- "Explain how the sentiment analyzer works"
- "How can I optimize this strategy?"
- "Debug this error: [paste error]"

**Tips:**
- Paste code in the "Code Context" section for better help
- Press Ctrl+Enter to send messages
- Export conversations for later reference

### Strategy Documents

Your strategy documents should include:
- Entry conditions (when to enter trades)
- Exit conditions (take profit, stop loss)
- Risk parameters
- Market conditions to trade in
- Indicators to use

**Example Strategy (strategy.txt):**
```
Entry Conditions:
- RSI below 30 (oversold)
- Price above 50 EMA
- Volume 20% above average
- Sentiment >= +3

Exit Conditions:
- Take profit: 2% above entry
- Stop loss: 0.8% below entry
- Time-based exit: 24 hours max

Risk:
- Position size: 1% of capital
- Max concurrent positions: 3
```

## 🔧 Configuration

### Core Rules (Cannot be Changed)
These rules are hardcoded for your safety:
- Maximum risk: 1% per trade
- Sentiment threshold: ±3
- Stop loss: ≤ 50% of take profit

### User Configurable
Edit in **config/settings.py**:
- Trading symbols
- Timeframes
- Indicator parameters
- UI update intervals

## 📊 Tabs Overview

### 1. Bot Tab
- Live trade monitoring
- PnL tracking
- TradingView chart integration
- Liquidation price display
- Daily trade count
- Close all trades button

### 2. Manual Trades Tab
- Long/Short position entry
- Percentage-based position sizing
- Live position display
- Quick close functions

### 3. Charts Tab
- TradingView chart integration
- Multiple timeframe support
- Indicator overlays

### 4. News Tab
- Real-time crypto news from CryptoPanic
- Sentiment indicators
- Filtered by impact level

### 5. Strategy Adjuster Tab
- Drag & drop strategy upload
- PDF, Word, Excel support
- Strategy parsing by Claude AI
- Strategy library management

### 6. Strategy Tester Tab
- Drag & drop backtest upload
- Historical data testing
- Performance metrics:
  - Win/Loss ratio
  - PnL
  - Profitability check (Pass/Fail)
  - Feasibility check (Pass/Fail)
- Live paper trading option

### 7. Developer Tab
- Claude AI debugging assistant
- Plain English code explanations
- Error diagnosis
- Code context support
- Conversation export

## 🗄️ Database & Learning

The bot maintains a local SQLite database with:
- **Trade History**: Every executed trade
- **Market Data**: Historical prices and indicators
- **Strategy Library**: Your uploaded strategies
- **Learning Data**: ML training data
- **Performance Metrics**: Bot performance over time

The bot learns from:
- Successful and failed trades
- Market conditions at trade time
- Strategy performance in different regimes
- User feedback and adjustments

## 🔐 Security Best Practices

1. **API Key Security**
   - Keys are encrypted with Fernet
   - Stored locally, never transmitted
   - Use API keys with trading permissions only
   - Enable IP whitelist on Binance

2. **Binance Security**
   - Enable 2FA on your account
   - Set withdrawal whitelist
   - Use futures account only
   - Start with minimal funds

3. **Data Backup**
   - Backup `database/` folder regularly
   - Export important strategies
   - Keep conversation logs from Claude

## 🛠️ Building Executable (.exe)

To create a standalone .exe file:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile \
            --windowed \
            --name="CryptoFuturesBot" \
            --icon=icon.ico \
            --add-data="config;config" \
            --add-data="ui/styles;ui/styles" \
            --hidden-import=anthropic \
            --hidden-import=ccxt \
            main.py

# Executable will be in dist/CryptoFuturesBot.exe
```

## 🐛 Troubleshooting

### Common Issues

**"No module named 'talib'"**
- Install TA-Lib following the special instructions above

**"API key not configured"**
- Go to File → Settings and add your API keys

**"Connection refused" errors**
- Check your internet connection
- Verify API keys are correct
- Check if Binance API has IP restrictions

**Bot not executing trades**
- Ensure sentiment meets ±3 threshold
- Check that you have valid technical setups
- Verify you're not at maximum position limit
- Look for error messages in Developer console

**Application won't start**
- Check Python version (3.11+)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check logs in `logs/` folder

### Getting Help

1. **Use Developer Tab**: Ask Claude to debug issues
2. **Check Logs**: Look in `logs/app.log`
3. **Export Conversation**: Save Claude conversations for reference

## 🔮 Future Features (DeFi Bot Integration)

The application is designed with a plugin architecture to support additional bots:

```python
# Future DeFi bot integration
class DeFiBot(BaseTradingBot):
    def __init__(self):
        # DEX integration
        # Liquidity pool analysis
        # Gas fee optimization
        pass
```

The modular design ensures adding new bot types won't affect the stability of existing bots.

## ⚠️ Disclaimer

**This software is for educational purposes.**

- Cryptocurrency trading carries significant risk
- Past performance does not guarantee future results
- Start with paper trading
- Only trade with money you can afford to lose
- The developers are not responsible for trading losses
- AI predictions are not financial advice
- Always do your own research (DYOR)

## 📝 License

[Your License Here]

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test thoroughly in paper trading mode
4. Submit a pull request

## 📞 Support

For issues and questions:
- Use the Developer Tab (Claude AI)
- Check documentation
- Review logs folder

## 🎓 Learning Resources

- [Binance Futures API Documentation](https://binance-docs.github.io/apidocs/futures/en/)
- [Technical Analysis Guide](https://www.investopedia.com/technical-analysis-4689657)
- [Risk Management in Trading](https://www.investopedia.com/articles/trading/09/risk-management.asp)
- [Claude AI Documentation](https://docs.anthropic.com)

---

**Built with ❤️ and 🤖 AI**

*Remember: Start with paper trading, learn the system, then gradually increase your involvement.*
