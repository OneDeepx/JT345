"""
UI Theme and Styling
"""

DARK_THEME = """
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}

QTabWidget::pane {
    border: 1px solid #3d3d3d;
    background-color: #252525;
}

QTabBar::tab {
    background-color: #2d2d2d;
    color: #ffffff;
    padding: 10px 20px;
    border: 1px solid #3d3d3d;
    border-bottom: none;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #252525;
    border-bottom: 2px solid #0d7377;
}

QTabBar::tab:hover {
    background-color: #353535;
}

QPushButton {
    background-color: #0d7377;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #14919b;
}

QPushButton:pressed {
    background-color: #0a5c5f;
}

QPushButton:disabled {
    background-color: #3d3d3d;
    color: #666666;
}

QPushButton.danger {
    background-color: #d32f2f;
}

QPushButton.danger:hover {
    background-color: #f44336;
}

QPushButton.success {
    background-color: #388e3c;
}

QPushButton.success:hover {
    background-color: #4caf50;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    padding: 6px;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #0d7377;
}

QComboBox {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    padding: 6px;
}

QComboBox:hover {
    border: 1px solid #0d7377;
}

QComboBox::drop-down {
    border: none;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #ffffff;
    margin-right: 5px;
}

QLabel {
    color: #ffffff;
}

QGroupBox {
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 10px;
    color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QTableWidget {
    background-color: #2d2d2d;
    color: #ffffff;
    gridline-color: #3d3d3d;
    border: 1px solid #3d3d3d;
}

QTableWidget::item {
    padding: 5px;
}

QTableWidget::item:selected {
    background-color: #0d7377;
}

QHeaderView::section {
    background-color: #252525;
    color: #ffffff;
    padding: 8px;
    border: 1px solid #3d3d3d;
    font-weight: bold;
}

QScrollBar:vertical {
    background-color: #2d2d2d;
    width: 12px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #0d7377;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #14919b;
}

QScrollBar:horizontal {
    background-color: #2d2d2d;
    height: 12px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #0d7377;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #14919b;
}

QStatusBar {
    background-color: #252525;
    color: #ffffff;
    border-top: 1px solid #3d3d3d;
}

QMenuBar {
    background-color: #252525;
    color: #ffffff;
    border-bottom: 1px solid #3d3d3d;
}

QMenuBar::item {
    padding: 8px 12px;
    background-color: transparent;
}

QMenuBar::item:selected {
    background-color: #0d7377;
}

QMenu {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #3d3d3d;
}

QMenu::item {
    padding: 8px 24px;
}

QMenu::item:selected {
    background-color: #0d7377;
}

QSpinBox, QDoubleSpinBox {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    padding: 6px;
}

QCheckBox {
    color: #ffffff;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #3d3d3d;
    border-radius: 3px;
    background-color: #2d2d2d;
}

QCheckBox::indicator:checked {
    background-color: #0d7377;
    border-color: #0d7377;
}

QRadioButton {
    color: #ffffff;
}

QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #3d3d3d;
    border-radius: 9px;
    background-color: #2d2d2d;
}

QRadioButton::indicator:checked {
    background-color: #0d7377;
    border-color: #0d7377;
}
"""


def apply_dark_theme(app):
    """Apply dark theme to application"""
    app.setStyleSheet(DARK_THEME)


# Color palette for charts and indicators
CHART_COLORS = {
    'background': '#1e1e1e',
    'grid': '#3d3d3d',
    'text': '#ffffff',
    'candle_up': '#26a69a',  # Green
    'candle_down': '#ef5350',  # Red
    'volume': '#64b5f6',  # Blue
    'ema_fast': '#ffeb3b',  # Yellow
    'ema_slow': '#ff9800',  # Orange
    'buy_signal': '#4caf50',  # Green
    'sell_signal': '#f44336',  # Red
}
