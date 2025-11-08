# JT345 - Crypto Futures Bot Updates

This repository hosts updates for the Crypto Futures Trading Bot.

## Current Version
**1.2.0** - Functional news tab with live CryptoPanic feed

## What's New in v1.2.0

- 📰 Live cryptocurrency news feed
- 🎯 Multiple filters (Rising, Hot, Bullish, Bearish, Important)
- 🔍 Currency filtering (BTC, ETH, etc.)
- 😊 Sentiment analysis
- 🌐 Open articles in browser
- ✅ Test connection button in settings

## How Updates Work

Users click **File → Check for Updates** in the bot, and updates are downloaded and installed automatically from this repository.

## For Users

### Getting Updates
1. Open the Crypto Futures Trading Bot
2. Click **File → Check for Updates**
3. If an update is available, click **Install Update**
4. Bot will download, install, and restart automatically

### Features Added
- v1.2.0: News tab with live feed
- v1.1.0: Auto-update system, settings dialog, bot monitoring

## For Developers

### Repository Structure
```
JT345/
├── version.json              # Current version info
└── releases/
    ├── update-v1.2.zip      # Update packages
    └── CHANGELOG-v1.2.md    # Changelogs
```

### Releasing Updates
1. Create update package ZIP
2. Add to `releases/` folder
3. Update `version.json`
4. Commit and push
5. Users automatically receive update notification

## Links

- Bot Repository: [Main Repository]
- Documentation: See bot's README.md
- Support: Use Developer tab in bot to ask Claude

## License

Same as main bot project
