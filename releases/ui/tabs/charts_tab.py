"""Charts Tab - Live Price Charts"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from utils.logger import setup_logger

logger = setup_logger('charts_tab')

# Try to import WebEngine, use fallback if not available
try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    WEBENGINE_AVAILABLE = True
except ImportError:
    WEBENGINE_AVAILABLE = False
    logger.warning("PyQt6-WebEngine not available, using fallback charts")


class ChartsTab(QWidget):
    """Charts tab with live price data"""
    
    def __init__(self):
        super().__init__()
        self.current_symbol = 'BTCUSDT'
        self.current_timeframe = '1h'
        self.init_ui()
    
    def init_ui(self):
        """Initialize the charts UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)  # Minimal margins for max space
        
        # Header with controls - compact
        header_layout = QHBoxLayout()
        
        header_label = QLabel("📈 Live Charts")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
        header_layout.addWidget(header_label)
        
        header_layout.addStretch()
        
        # Symbol selector
        symbol_label = QLabel("Symbol:")
        header_layout.addWidget(symbol_label)
        
        self.symbol_combo = QComboBox()
        self.symbol_combo.addItems(['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT', 'XRPUSDT'])
        self.symbol_combo.currentTextChanged.connect(self.on_symbol_changed)
        header_layout.addWidget(self.symbol_combo)
        
        # Timeframe selector
        timeframe_label = QLabel("Timeframe:")
        header_layout.addWidget(timeframe_label)
        
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(['1m', '5m', '15m', '1h', '4h', '1d'])
        self.timeframe_combo.setCurrentText('1h')
        self.timeframe_combo.currentTextChanged.connect(self.on_timeframe_changed)
        header_layout.addWidget(self.timeframe_combo)
        
        # Open in browser button
        self.browser_btn = QPushButton("🌐 Open in Browser")
        self.browser_btn.clicked.connect(self.open_in_browser)
        self.browser_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: white;
                padding: 5px 15px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a8eef;
            }
        """)
        header_layout.addWidget(self.browser_btn)
        
        layout.addLayout(header_layout)
        
        # Main chart area - MAXIMUM SIZE
        if WEBENGINE_AVAILABLE:
            # TradingView embedded widget
            self.chart_widget = QWebEngineView()
            self.chart_widget.setMinimumHeight(650)  # Very tall
            self.load_tradingview_chart()
            layout.addWidget(self.chart_widget, stretch=1)  # Stretch to fill space
        else:
            # Fallback message with BIG, READABLE text
            fallback_widget = QWidget()
            fallback_widget.setStyleSheet("background-color: #2d2d2d; border-radius: 10px;")
            fallback_layout = QVBoxLayout()
            fallback_layout.setContentsMargins(40, 40, 40, 40)
            
            # Big, readable message
            message = QLabel(
                "📊 TradingView Charts Not Available\n\n\n"
                "To enable live charts, install PyQt6-WebEngine:\n\n"
                "pip install PyQt6-WebEngine --break-system-packages\n\n\n"
                "Then restart the bot.\n\n"
                "Or click below to open TradingView in your browser."
            )
            message.setAlignment(Qt.AlignmentFlag.AlignCenter)
            message.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    color: white;
                    line-height: 2.0;
                    font-weight: bold;
                }
            """)
            message.setWordWrap(True)
            fallback_layout.addWidget(message)
            
            # Big open in browser button
            open_btn = QPushButton("🌐 Open TradingView in Browser")
            open_btn.setMinimumHeight(60)
            open_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a9eff;
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 8px;
                    padding: 15px;
                }
                QPushButton:hover {
                    background-color: #3a8eef;
                }
            """)
            open_btn.clicked.connect(self.open_in_browser)
            fallback_layout.addWidget(open_btn)
            
            fallback_widget.setLayout(fallback_layout)
            layout.addWidget(fallback_widget)
        
        # Status bar at bottom - clear and visible
        status_layout = QHBoxLayout()
        
        self.price_label = QLabel(f"📊 {self.current_symbol} • {self.current_timeframe} timeframe")
        self.price_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: white;
                padding: 8px;
                background-color: #2d2d2d;
                border-radius: 4px;
                font-weight: bold;
            }
        """)
        status_layout.addWidget(self.price_label)
        
        status_layout.addStretch()
        
        self.status_label = QLabel("✅ Ready")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #4caf50;
                padding: 8px;
                font-weight: bold;
            }
        """)
        status_layout.addWidget(self.status_label)
        
        layout.addLayout(status_layout)
        
        self.setLayout(layout)
    
    def load_tradingview_chart(self):
        """Load TradingView chart widget"""
        if not WEBENGINE_AVAILABLE:
            return
        
        symbol = self.current_symbol.replace('USDT', '')
        
        # Clean HTML with proper error handling
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background-color: #1e1e1e;
                    overflow: hidden;
                }}
                .error-message {{
                    display: none;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    text-align: center;
                    padding: 100px 50px;
                    font-family: Arial, sans-serif;
                    background-color: #2d2d2d;
                    margin: 50px;
                    border-radius: 10px;
                    line-height: 2;
                }}
            </style>
        </head>
        <body>
            <div id="tradingview-container" style="height:100%;width:100%"></div>
            <div id="error-display" class="error-message">
                <div>⚠️</div>
                <div>Unable to Load Chart</div>
                <div style="font-size: 18px; margin-top: 20px;">
                    Check your internet connection<br>
                    or click "Open in Browser" above
                </div>
            </div>
            
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
            {{
              "container_id": "tradingview-container",
              "autosize": true,
              "symbol": "BINANCE:{symbol}USDT",
              "interval": "{self.current_timeframe}",
              "timezone": "Etc/UTC",
              "theme": "dark",
              "style": "1",
              "locale": "en",
              "enable_publishing": false,
              "allow_symbol_change": true,
              "calendar": false,
              "hide_top_toolbar": false,
              "hide_legend": false,
              "save_image": false,
              "support_host": "https://www.tradingview.com"
            }}
            </script>
            
            <script>
                // Show readable error if chart fails to load
                setTimeout(function() {{
                    var container = document.getElementById('tradingview-container');
                    var error = document.getElementById('error-display');
                    // Check if chart loaded
                    if (container && container.getElementsByTagName('iframe').length === 0) {{
                        container.style.display = 'none';
                        error.style.display = 'block';
                    }}
                }}, 15000);  // Wait 15 seconds
            </script>
        </body>
        </html>
        """
        
        self.chart_widget.setHtml(html)
        self.status_label.setText("⏳ Loading...")
        self.status_label.setStyleSheet("font-size: 12px; color: #ff9800; padding: 8px; font-weight: bold;")
        
        # Update status after delay
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(3000, lambda: self.status_label.setText("✅ Chart loaded") if WEBENGINE_AVAILABLE else None)
    
    def on_symbol_changed(self, symbol):
        """Handle symbol change"""
        self.current_symbol = symbol
        if WEBENGINE_AVAILABLE:
            self.load_tradingview_chart()
        self.update_labels()
    
    def on_timeframe_changed(self, timeframe):
        """Handle timeframe change"""
        self.current_timeframe = timeframe
        if WEBENGINE_AVAILABLE:
            self.load_tradingview_chart()
        self.update_labels()
    
    def update_labels(self):
        """Update display labels"""
        symbol_display = self.current_symbol.replace('USDT', '/USDT')
        self.price_label.setText(f"📊 {symbol_display} • {self.current_timeframe} timeframe")
    
    def open_in_browser(self):
        """Open TradingView in external browser"""
        symbol = self.current_symbol.replace('USDT', '')
        url = f"https://www.tradingview.com/chart/?symbol=BINANCE:{symbol}USDT&interval={self.current_timeframe}"
        QDesktopServices.openUrl(QUrl(url))
        self.status_label.setText("🌐 Opened in browser")
        self.status_label.setStyleSheet("font-size: 12px; color: #2196f3; padding: 8px; font-weight: bold;")
    
    def update_display(self):
        """Update display (called by main window timer)"""
        pass
