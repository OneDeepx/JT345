"""Bot Monitoring Tab"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QGroupBox, QTextEdit
)
from PyQt6.QtCore import Qt
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger('bot_tab')


class BotTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Status Section
        status_group = QGroupBox("Bot Status")
        status_layout = QVBoxLayout()
        
        # Status indicators
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4caf50;")
        status_layout.addWidget(self.status_label)
        
        # Mode display
        info_layout = QHBoxLayout()
        
        self.mode_label = QLabel("Mode: Paper Trading")
        self.mode_label.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(self.mode_label)
        
        self.auto_label = QLabel("Auto Trading: Disabled")
        self.auto_label.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(self.auto_label)
        
        info_layout.addStretch()
        status_layout.addLayout(info_layout)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Quick Stats
        stats_group = QGroupBox("Quick Stats")
        stats_layout = QHBoxLayout()
        
        # Placeholder stats
        self.balance_label = QLabel("Balance: $10,000.00")
        self.balance_label.setStyleSheet("font-size: 14px;")
        stats_layout.addWidget(self.balance_label)
        
        self.pnl_label = QLabel("Total P&L: $0.00")
        self.pnl_label.setStyleSheet("font-size: 14px; color: #888;")
        stats_layout.addWidget(self.pnl_label)
        
        self.trades_label = QLabel("Trades Today: 0")
        self.trades_label.setStyleSheet("font-size: 14px;")
        stats_layout.addWidget(self.trades_label)
        
        stats_layout.addStretch()
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Controls
        controls_group = QGroupBox("Controls")
        controls_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start Bot")
        self.start_btn.clicked.connect(self.toggle_bot)
        self.start_btn.setMinimumHeight(40)
        controls_layout.addWidget(self.start_btn)
        
        self.close_all_btn = QPushButton("Close All Positions")
        self.close_all_btn.setProperty("class", "danger")
        self.close_all_btn.setStyleSheet("background-color: #d32f2f;")
        self.close_all_btn.clicked.connect(self.close_all_positions)
        self.close_all_btn.setMinimumHeight(40)
        controls_layout.addWidget(self.close_all_btn)
        
        controls_group.setLayout(controls_layout)
        layout.addWidget(controls_group)
        
        # Activity Log
        log_group = QGroupBox("Activity Log")
        log_layout = QVBoxLayout()
        
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setMaximumHeight(200)
        self.log_display.append("System ready. Waiting for bot to start...")
        self.log_display.append("Configure API keys in Settings to enable live trading.")
        
        log_layout.addWidget(self.log_display)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        # Info Section
        info_group = QGroupBox("Implementation Status")
        info_layout = QVBoxLayout()
        
        info_text = QLabel(
            "🚧 This tab is partially implemented.\n\n"
            "✅ What works:\n"
            "   • Status display\n"
            "   • Settings integration\n"
            "   • Activity logging\n\n"
            "🔧 What needs implementation:\n"
            "   • Trading engine integration\n"
            "   • Real-time position monitoring\n"
            "   • Live P&L updates\n"
            "   • Chart display\n"
            "   • Order execution\n\n"
            "📚 See ROADMAP.md for implementation guide.\n"
            "💡 Use the Developer tab to ask Claude for help!"
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("color: #aaa; font-size: 11px;")
        info_layout.addWidget(info_text)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Initialize display
        self.update_display()
    
    def toggle_bot(self):
        """Toggle bot on/off"""
        auto_enabled = settings.get('trading.auto_trading_enabled', False)
        
        if not auto_enabled:
            # Check if API keys are configured
            claude_key = settings.get_api_key('claude').get('key')
            binance_key = settings.get_api_key('binance').get('key')
            
            if not claude_key or not binance_key:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self,
                    "API Keys Required",
                    "Please configure your API keys in Settings before starting the bot.\n\n"
                    "Required:\n"
                    "• Claude API key (for AI features)\n"
                    "• Binance API key (for trading)\n\n"
                    "Go to: File → Settings"
                )
                return
            
            # Enable auto trading
            settings.set('trading.auto_trading_enabled', True)
            self.start_btn.setText("Stop Bot")
            self.start_btn.setStyleSheet("background-color: #d32f2f;")
            self.log_display.append("✅ Bot started!")
            self.log_display.append("⚠️ Note: Core trading engine not yet implemented.")
            self.log_display.append("   See ROADMAP.md Phase 1 for implementation guide.")
            logger.info("Bot started (stub mode)")
        else:
            # Disable auto trading
            settings.set('trading.auto_trading_enabled', False)
            self.start_btn.setText("Start Bot")
            self.start_btn.setStyleSheet("")
            self.log_display.append("🛑 Bot stopped")
            logger.info("Bot stopped")
        
        self.update_display()
    
    def close_all_positions(self):
        """Close all open positions"""
        from PyQt6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self,
            "Close All Positions",
            "Are you sure you want to close ALL open positions?\n\n"
            "This will place limit orders at current market price.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.log_display.append("📍 Close all positions requested...")
            self.log_display.append("⚠️ Position manager not yet implemented.")
            self.log_display.append("   See ROADMAP.md Phase 1 for implementation.")
            QMessageBox.information(
                self,
                "Not Implemented",
                "Position management is not yet implemented.\n\n"
                "This feature will be added in Phase 1.\n"
                "See ROADMAP.md for details."
            )
    
    def update_display(self):
        """Update display with current status"""
        # Update mode
        is_paper = settings.get('trading.paper_trading', True)
        mode_text = "Paper Trading" if is_paper else "🔴 LIVE TRADING"
        self.mode_label.setText(f"Mode: {mode_text}")
        
        # Update auto status
        auto_enabled = settings.get('trading.auto_trading_enabled', False)
        auto_text = "🟢 Enabled" if auto_enabled else "Disabled"
        self.auto_label.setText(f"Auto Trading: {auto_text}")
        
        # Update status
        if auto_enabled:
            self.status_label.setText("Status: 🟢 Running")
            self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4caf50;")
        else:
            self.status_label.setText("Status: Standby")
            self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #888;")

