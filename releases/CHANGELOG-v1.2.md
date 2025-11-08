# Version 1.2.0 - Live News Feed

## Release Date
November 8, 2024

## What's New

### ✨ Fully Functional News Tab
- **Live CryptoPanic news feed** - Real-time cryptocurrency news
- **Multiple filters** - Rising, Hot, Important, Bullish, Bearish, All
- **Currency filtering** - Filter by specific cryptocurrencies (BTC, ETH, etc.)
- **Sentiment analysis** - See bullish/bearish sentiment for each article
- **Community votes** - View positive/negative votes from community
- **Article details** - Full information and analysis
- **Auto-refresh** - Updates every 5 minutes
- **Open in browser** - Click to read full articles

### 🔧 Improvements
- **Settings Dialog** - Added "Test Connection" button for CryptoPanic API
- **API Key Validation** - Test your CryptoPanic API key before saving
- **Better error handling** - Clear messages when API key is missing
- **Fixed QWidget import** - Resolved import error in update dialog

### 🐛 Bug Fixes
- Fixed missing QWidget import in update_dialog.py
- Fixed CryptoPanic API integration

## New Files
- `apis/cryptopanic_api.py` - CryptoPanic API integration
- `apis/__init__.py` - API module initialization

## Updated Files
- `ui/tabs/news_tab.py` - Complete rewrite with live feed
- `ui/settings_dialog.py` - Added test connection for CryptoPanic
- `ui/update_dialog.py` - Fixed import error

## Features in Detail

### News Tab Features
1. **Real-time Feed** - Connects to CryptoPanic API
2. **Smart Filters** - Choose from 6 different news filters
3. **Currency Search** - Filter news by specific coins
4. **Sentiment Indicators** - Visual bullish/bearish indicators
5. **Detailed View** - Click any article for full details
6. **External Links** - Open full articles in browser
7. **Auto-refresh** - Stays current automatically

### Settings Integration
1. **Test Connection** - Verify API key works before saving
2. **Clear Feedback** - See connection status immediately
3. **Secure Storage** - All keys encrypted automatically

## Getting Your CryptoPanic API Key

1. Go to https://cryptopanic.com/developers/api/
2. Sign up for free account
3. Copy your API token
4. In bot: File → Settings → API Keys tab
5. Paste CryptoPanic API key
6. Click "Test Connection"
7. Click "Save"
8. Go to News tab and click Refresh

**Free tier allows 500 requests/day** - Perfect for this bot!

## Installation

### Automatic (Recommended)
If you have v1.1.0 installed:
1. File → Check for Updates
2. Click "Install Update"
3. Done!

### Manual
1. Download update-v1.2.zip
2. Extract to get `files/` folder
3. Copy contents to your bot directory (overwrite files)
4. Restart bot

## What to Try

After updating:

1. **Configure API Key**
   - File → Settings → API Keys
   - Enter CryptoPanic API key
   - Click Test Connection
   - Save

2. **View News**
   - Click News tab
   - See live cryptocurrency news
   - Try different filters
   - Click articles for details

3. **Filter by Currency**
   - Enter "BTC" in currency box
   - See only Bitcoin news
   - Try "BTC,ETH" for multiple

## Known Issues
None - this is a stable release!

## Coming Next (v1.3)
- Charts tab with TradingView integration
- Manual trading interface
- Strategy adjuster

## Support

Issues? Questions?
1. Check Settings → Test Connection
2. Verify internet connection
3. Check API key is correct
4. Use Developer tab to ask Claude for help

---

**Enjoy the live news feed!** 📰🚀

Now you can stay updated with real-time crypto news directly in your bot!
