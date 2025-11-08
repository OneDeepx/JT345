# 🚀 Quick Start Guide

Get up and running with the Crypto Futures Trading Bot in 5 minutes!

## Prerequisites
- Python 3.11+ installed
- Internet connection
- Binance account (for live trading)
- Claude API key (get from console.anthropic.com)

## Step-by-Step Setup

### 1. Install Python Dependencies (2 minutes)

```bash
# Navigate to the project folder
cd crypto-futures-bot

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Run Setup Script (1 minute)

```bash
python setup.py
```

This will:
- Create necessary folders
- Check dependencies
- Create configuration templates
- Generate example strategy

### 3. Get Your API Keys (2 minutes)

**Claude API (Required):**
1. Go to https://console.anthropic.com
2. Create account / Sign in
3. Generate API key
4. Copy the key

**Binance API (For live trading):**
1. Go to https://www.binance.com
2. Account → API Management
3. Create new API key
4. Enable "Futures" permission
5. Copy key and secret
6. **Important**: Set IP whitelist for security

**CryptoPanic (For news):**
1. Go to https://cryptopanic.com/developers/api/
2. Sign up for free API key

### 4. Launch the Application

```bash
python main.py
```

The application will open in **Paper Trading** mode (safe - no real money!)

### 5. Configure API Keys (1 minute)

In the application:
1. Click **File** → **Settings**
2. Enter your API keys:
   - Claude API Key
   - Binance API Key & Secret (optional for paper trading)
   - CryptoPanic API Key
3. Click **Save**

## First Use

### Test Claude AI Assistant
1. Click the **Developer** tab
2. Type: "Hello Claude! Can you help me understand this bot?"
3. Press Ctrl+Enter or click Send
4. Claude will respond and help you!

### Upload a Strategy
1. Open the **Strategy Adjuster** tab
2. Drag and drop the example strategy file:
   `strategies/example_strategy.txt`
3. Claude will parse and validate it

### Backtest a Strategy
1. Go to **Strategy Tester** tab
2. Upload your strategy
3. Set date range
4. Click **Run Backtest**
5. Review results

### Monitor the Bot
1. Go to **Bot** tab
2. See live trades (if auto-trading enabled)
3. View PnL and statistics
4. Use "Close All Trades" for emergency exit

### Manual Trading
1. Go to **Manual Trades** tab
2. Select Long or Short
3. Enter position size (as % of capital)
4. Click **Open Position**

## Safety Checklist ✅

Before enabling auto-trading:

- [ ] Tested in Paper Trading mode
- [ ] Backtested your strategy
- [ ] Understand the core rules (1% risk, sentiment ±3, SL ≤ 50% TP)
- [ ] Set Binance IP whitelist
- [ ] Enabled 2FA on Binance
- [ ] Started with small capital
- [ ] Know how to use "Close All Trades"

## Common First-Time Questions

**Q: Do I need real money to start?**
A: No! Start in Paper Trading mode (default). It simulates trading with fake money.

**Q: What if I don't have Binance API keys?**
A: You can still use paper trading and the Developer console without Binance keys.

**Q: How do I switch from paper to live trading?**
A: **File** → **Toggle Paper Trading**. ⚠️ Only do this after thorough testing!

**Q: Why isn't the bot making trades?**
A: Check:
- Sentiment must be ≥ +3 or ≤ -3
- Valid technical setup required
- Volume confirmation needed
- Not at maximum position limit

**Q: How do I talk to Claude?**
A: Go to **Developer** tab, type your question, press Ctrl+Enter.

**Q: The bot made a bad trade!**
A: In paper trading, this is fine - the bot learns from mistakes. Review the trade in the Bot tab and adjust your strategy.

## Quick Commands

**Send message to Claude**: Ctrl+Enter in Developer tab  
**Emergency close all**: Button in Bot/Manual Trades tab  
**Toggle paper trading**: File → Toggle Paper Trading  
**Toggle auto trading**: File → Toggle Auto Trading

## Next Steps

1. **Read the full README.md** - Comprehensive documentation
2. **Experiment with strategies** - Create and test different approaches
3. **Use Claude for help** - Ask questions in Developer tab
4. **Monitor and learn** - Watch how the bot trades in paper mode
5. **Gradually increase complexity** - Start simple, add features

## Need Help?

- **Developer Tab**: Ask Claude anything!
- **Logs**: Check `logs/app.log` for errors
- **Documentation**: See README.md
- **Example Strategy**: `strategies/example_strategy.txt`

## Troubleshooting

**Application won't start:**
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt

# Run setup again
python setup.py
```

**"TA-Lib not found":**
See the special TA-Lib installation instructions in README.md

**API errors:**
- Verify keys are correct
- Check internet connection
- Ensure Binance API has futures permission

---

**You're ready! Start the bot with:** `python main.py`

Happy trading! 🚀📈

*Remember: Always start with paper trading and never risk more than you can afford to lose.*
