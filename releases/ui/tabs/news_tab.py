"""News Tab - CryptoPanic Live Feed"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QListWidget, QListWidgetItem,
    QTextBrowser, QSplitter, QMessageBox, QLineEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QUrl
from PyQt6.QtGui import QDesktopServices
from apis.cryptopanic_api import cryptopanic_api
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger('news_tab')


class NewsFetcherThread(QThread):
    """Thread for fetching news without blocking UI"""
    news_ready = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, filter_type, currencies):
        super().__init__()
        self.filter_type = filter_type
        self.currencies = currencies
    
    def run(self):
        try:
            # Reload API key in case it changed
            cryptopanic_api._load_api_key()
            
            posts = cryptopanic_api.get_posts(
                currencies=self.currencies,
                filter_type=self.filter_type,
                limit=50
            )
            self.news_ready.emit(posts)
        except Exception as e:
            self.error.emit(str(e))


class NewsTab(QWidget):
    """News tab with CryptoPanic live feed"""
    
    def __init__(self):
        super().__init__()
        self.current_posts = []
        self.init_ui()
        
        # Auto-refresh timer (5 minutes)
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_news)
        self.refresh_timer.start(300000)  # 5 minutes
    
    def init_ui(self):
        """Initialize the news tab UI"""
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("📰 Crypto News Feed")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.refresh_news)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Filters
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("Filter:"))
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            "Rising",
            "Hot", 
            "Important",
            "Bullish",
            "Bearish",
            "All News"
        ])
        self.filter_combo.currentTextChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(self.filter_combo)
        
        filter_layout.addWidget(QLabel("Currency:"))
        
        self.currency_input = QLineEdit()
        self.currency_input.setPlaceholderText("BTC,ETH (leave empty for all)")
        self.currency_input.setMaximumWidth(200)
        self.currency_input.returnPressed.connect(self.refresh_news)
        filter_layout.addWidget(self.currency_input)
        
        filter_layout.addStretch()
        
        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #aaa; font-size: 11px;")
        filter_layout.addWidget(self.status_label)
        
        layout.addLayout(filter_layout)
        
        # Splitter for news list and details
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # News list
        self.news_list = QListWidget()
        self.news_list.itemClicked.connect(self.on_news_selected)
        splitter.addWidget(self.news_list)
        
        # News details
        details_widget = QWidget()
        details_layout = QVBoxLayout()
        
        self.details_title = QLabel("Select a news item to view details")
        self.details_title.setWordWrap(True)
        self.details_title.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px;")
        details_layout.addWidget(self.details_title)
        
        self.details_browser = QTextBrowser()
        self.details_browser.setOpenExternalLinks(False)
        self.details_browser.anchorClicked.connect(self.open_link)
        details_layout.addWidget(self.details_browser)
        
        self.open_article_btn = QPushButton("Open Full Article")
        self.open_article_btn.clicked.connect(self.open_full_article)
        self.open_article_btn.setEnabled(False)
        details_layout.addWidget(self.open_article_btn)
        
        details_widget.setLayout(details_layout)
        splitter.addWidget(details_widget)
        
        # Set splitter sizes
        splitter.setSizes([400, 600])
        layout.addWidget(splitter)
        
        self.setLayout(layout)
        
        # Check if API key is configured
        if not cryptopanic_api.is_configured():
            self.show_api_key_warning()
        else:
            # Load initial news
            self.refresh_news()
    
    def show_api_key_warning(self):
        """Show warning that API key is not configured"""
        self.status_label.setText("⚠️ API key not configured")
        self.status_label.setStyleSheet("color: #ff9800; font-size: 11px;")
        
        item = QListWidgetItem("⚠️ CryptoPanic API Key Not Configured")
        item.setData(Qt.ItemDataRole.UserRole, {
            'title': 'API Key Required',
            'content': 'Please configure your CryptoPanic API key in Settings to view news.'
        })
        self.news_list.addItem(item)
        
        self.details_title.setText("CryptoPanic API Key Required")
        self.details_browser.setHtml(
            "<div style='padding: 20px;'>"
            "<h3>🔑 API Key Required</h3>"
            "<p>To use the news feed, you need a CryptoPanic API key.</p>"
            "<h4>How to get your API key:</h4>"
            "<ol>"
            "<li>Go to <a href='https://cryptopanic.com/developers/api/'>cryptopanic.com/developers/api/</a></li>"
            "<li>Sign up for a free account</li>"
            "<li>Copy your API key</li>"
            "<li>Go to <b>File → Settings → API Keys</b></li>"
            "<li>Paste your CryptoPanic API key</li>"
            "<li>Click Save</li>"
            "<li>Come back here and click Refresh</li>"
            "</ol>"
            "<p><b>Note:</b> The free tier allows 500 requests per day, which is plenty for this bot!</p>"
            "</div>"
        )
    
    def showEvent(self, event):
        """Called when tab becomes visible - reload API key if needed"""
        super().showEvent(event)
        # Reload API configuration when tab is shown
        cryptopanic_api._load_api_key()
        # If we were showing the warning but now have a key, refresh
        if self.status_label.text().startswith("⚠️") and cryptopanic_api.is_configured():
            self.refresh_news()
    
    def refresh_news(self):
        """Refresh news from CryptoPanic"""
        if not cryptopanic_api.is_configured():
            self.show_api_key_warning()
            return
        
        self.status_label.setText("Loading...")
        self.refresh_btn.setEnabled(False)
        self.news_list.clear()
        
        # Get filter
        filter_text = self.filter_combo.currentText().lower()
        if filter_text == "all news":
            filter_text = "rising"
        
        # Get currencies
        currencies = self.currency_input.text().strip() or None
        
        # Start fetcher thread
        self.fetcher_thread = NewsFetcherThread(filter_text, currencies)
        self.fetcher_thread.news_ready.connect(self.on_news_loaded)
        self.fetcher_thread.error.connect(self.on_news_error)
        self.fetcher_thread.start()
    
    def on_filter_changed(self):
        """Handle filter change"""
        self.refresh_news()
    
    def on_news_loaded(self, posts):
        """Handle news loaded"""
        self.current_posts = posts
        self.refresh_btn.setEnabled(True)
        
        logger.info(f"News loaded callback - received {len(posts)} posts")
        
        if not posts:
            self.status_label.setText("No news found")
            self.status_label.setStyleSheet("color: #ff9800; font-size: 11px;")
            item = QListWidgetItem("No news articles found for this filter. Try a different filter or leave currency blank.")
            self.news_list.addItem(item)
            
            # Add helpful message
            self.details_title.setText("No News Found")
            self.details_browser.setHtml(
                "<div style='padding: 20px;'>"
                "<h3>📰 No News Found</h3>"
                "<p>CryptoPanic didn't return any news for this filter.</p>"
                "<h4>Try:</h4>"
                "<ul>"
                "<li>Select a different filter (Rising, Hot, etc.)</li>"
                "<li>Leave the currency field empty for all news</li>"
                "<li>Wait a moment - news updates frequently</li>"
                "</ul>"
                "<p>If you keep seeing this, the API might be having issues or your filter is too specific.</p>"
                "</div>"
            )
            return
        
        self.status_label.setText(f"Loaded {len(posts)} articles")
        self.status_label.setStyleSheet("color: #4caf50; font-size: 11px;")
        
        # Add posts to list
        for post in posts:
            self.add_news_item(post)
    
    def add_news_item(self, post):
        """Add a news item to the list"""
        # Create display text
        sentiment = post.get('sentiment', 'Neutral')
        sentiment_emoji = {
            'Bullish': '🟢',
            'Bearish': '🔴',
            'Neutral': '⚪'
        }.get(sentiment, '⚪')
        
        currencies = post.get('currencies', [])
        currency_text = ', '.join(currencies[:3]) if currencies else 'General'
        
        time_str = post.get('published_at', '')
        title = post.get('title', 'No title')
        
        display_text = f"{sentiment_emoji} {title}\n   {currency_text} • {time_str}"
        
        item = QListWidgetItem(display_text)
        item.setData(Qt.ItemDataRole.UserRole, post)
        
        self.news_list.addItem(item)
    
    def on_news_selected(self, item):
        """Handle news item selected"""
        post = item.data(Qt.ItemDataRole.UserRole)
        if not post or not isinstance(post, dict):
            return
        
        self.display_news_details(post)
    
    def display_news_details(self, post):
        """Display details of selected news"""
        title = post.get('title', 'No title')
        self.details_title.setText(title)
        
        sentiment = post.get('sentiment', 'Neutral')
        sentiment_score = post.get('sentiment_score', 0)
        source = post.get('source', 'Unknown')
        published_at = post.get('published_at', 'Unknown')
        currencies = post.get('currencies', [])
        votes = post.get('votes', {})
        url = post.get('url', '')
        
        # Build HTML
        html = f"""
        <div style='padding: 15px; font-family: Arial, sans-serif;'>
            <h3 style='margin-top: 0;'>{title}</h3>
            
            <div style='margin: 10px 0; padding: 10px; background-color: #2d2d2d; border-radius: 5px;'>
                <p style='margin: 5px 0;'><b>Source:</b> {source}</p>
                <p style='margin: 5px 0;'><b>Published:</b> {published_at}</p>
                <p style='margin: 5px 0;'><b>Currencies:</b> {', '.join(currencies) if currencies else 'General'}</p>
            </div>
            
            <div style='margin: 10px 0; padding: 10px; background-color: #2d2d2d; border-radius: 5px;'>
                <h4 style='margin-top: 0;'>Sentiment Analysis</h4>
                <p style='margin: 5px 0; font-size: 16px;'>
                    <b>Overall:</b> <span style='color: {"#4caf50" if sentiment_score > 0 else "#f44336" if sentiment_score < 0 else "#888"};'>{sentiment}</span>
                </p>
                <p style='margin: 5px 0;'><b>Score:</b> {sentiment_score:.2f}</p>
            </div>
            
            <div style='margin: 10px 0; padding: 10px; background-color: #2d2d2d; border-radius: 5px;'>
                <h4 style='margin-top: 0;'>Community Votes</h4>
                <p style='margin: 5px 0;'>👍 Positive: {votes.get('positive', 0)}</p>
                <p style='margin: 5px 0;'>👎 Negative: {votes.get('negative', 0)}</p>
                <p style='margin: 5px 0;'>⭐ Important: {votes.get('important', 0)}</p>
                <p style='margin: 5px 0;'>❤️ Liked: {votes.get('liked', 0)}</p>
            </div>
            
            <p style='margin: 15px 0; color: #aaa; font-size: 12px;'>
                Click "Open Full Article" to read more on the original website.
            </p>
        </div>
        """
        
        self.details_browser.setHtml(html)
        self.open_article_btn.setEnabled(bool(url))
        self.current_article_url = url
    
    def open_full_article(self):
        """Open full article in browser"""
        if hasattr(self, 'current_article_url') and self.current_article_url:
            QDesktopServices.openUrl(QUrl(self.current_article_url))
    
    def open_link(self, url):
        """Open link in browser"""
        QDesktopServices.openUrl(url)
    
    def on_news_error(self, error):
        """Handle news fetch error"""
        self.refresh_btn.setEnabled(True)
        self.status_label.setText(f"Error: {error}")
        self.status_label.setStyleSheet("color: #f44336; font-size: 11px;")
        
        logger.error(f"News fetch error: {error}")
        
        self.news_list.clear()
        item = QListWidgetItem(f"❌ Error loading news: {error}")
        self.news_list.addItem(item)
        
        QMessageBox.warning(
            self,
            "Error Loading News",
            f"Failed to load news from CryptoPanic:\n\n{error}\n\n"
            "Please check:\n"
            "• Your internet connection\n"
            "• Your CryptoPanic API key in Settings\n"
            "• Check logs for details\n"
            "• CryptoPanic service status"
        )
    
    def update_display(self):
        """Update display (called by main window timer)"""
        # Update status if needed
        if cryptopanic_api.is_configured():
            if self.status_label.text().startswith("⚠️"):
                self.refresh_news()

