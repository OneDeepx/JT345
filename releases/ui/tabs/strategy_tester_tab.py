"""Strategy Tester Tab - Backtest Trading Strategies"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QProgressBar, QSplitter,
    QGroupBox, QFormLayout, QMessageBox, QFileDialog, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QPalette, QColor
import pandas as pd
from pathlib import Path
from core.strategy_parser import strategy_parser
from core.backtest_engine import backtest_engine
from utils.logger import setup_logger
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

logger = setup_logger('strategy_tab')


class DropZone(QLabel):
    """Drag and drop zone widget"""
    file_dropped = pyqtSignal(str)
    
    def __init__(self, label_text: str, file_types: str):
        super().__init__()
        self.label_text = label_text
        self.file_types = file_types
        self.file_path = None
        
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setWordWrap(True)
        self.setMinimumHeight(150)
        self.setAcceptDrops(True)
        self.update_display()
        
        # Styling
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #2d2d2d;
                padding: 20px;
            }
            QLabel:hover {
                border-color: #4a9eff;
                background-color: #353535;
            }
        """)
    
    def update_display(self):
        """Update display text"""
        if self.file_path:
            self.setText(f"✅ {Path(self.file_path).name}\n\nClick to change or drag another file")
        else:
            self.setText(f"📁 {self.label_text}\n\n{self.file_types}\n\nDrag & drop or click to browse")
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QLabel {
                    border: 2px solid #4a9eff;
                    border-radius: 10px;
                    background-color: #353535;
                    padding: 20px;
                }
            """)
    
    def dragLeaveEvent(self, event):
        """Handle drag leave"""
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #2d2d2d;
                padding: 20px;
            }
        """)
    
    def dropEvent(self, event: QDropEvent):
        """Handle file drop"""
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            self.set_file(files[0])
        
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #2d2d2d;
                padding: 20px;
            }
        """)
    
    def mousePressEvent(self, event):
        """Handle click to browse"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"Select {self.label_text}",
            "",
            self.file_types
        )
        if file_path:
            self.set_file(file_path)
    
    def set_file(self, file_path: str):
        """Set the file path"""
        self.file_path = file_path
        self.update_display()
        self.file_dropped.emit(file_path)


class BacktestThread(QThread):
    """Thread for running backtest"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, strategy_file, data_file):
        super().__init__()
        self.strategy_file = strategy_file
        self.data_file = data_file
    
    def run(self):
        try:
            # Parse strategy
            self.progress.emit("📖 Parsing strategy document...")
            strategy_dict = strategy_parser.parse_file(self.strategy_file)
            
            if not strategy_dict:
                self.error.emit("Failed to parse strategy document")
                return
            
            self.progress.emit(f"✅ Strategy parsed: {strategy_dict.get('strategy_name', 'Unknown')}")
            
            # Load chart data
            self.progress.emit("📊 Loading historical data...")
            data = self._load_data(self.data_file)
            
            if data is None:
                self.error.emit("Failed to load chart data")
                return
            
            self.progress.emit(f"✅ Loaded {len(data)} candles")
            
            # Load data into engine
            if not backtest_engine.load_data(data):
                self.error.emit("Invalid data format")
                return
            
            # Convert strategy to executable rules
            self.progress.emit("⚙️ Converting strategy to executable rules...")
            executable_rules = strategy_parser.convert_to_executable(strategy_dict)
            
            # Run backtest
            self.progress.emit("🚀 Running backtest simulation...")
            results = backtest_engine.execute_strategy(executable_rules)
            
            # Add strategy info to results
            results['strategy_info'] = strategy_dict
            results['data_info'] = {
                'candles': len(data),
                'start_date': str(data['timestamp'].min()),
                'end_date': str(data['timestamp'].max())
            }
            
            self.progress.emit("✅ Backtest complete!")
            self.finished.emit(results)
            
        except Exception as e:
            logger.error(f"Backtest error: {e}")
            self.error.emit(str(e))
    
    def _load_data(self, file_path: str) -> pd.DataFrame:
        """Load chart data from file"""
        try:
            ext = Path(file_path).suffix.lower()
            
            if ext == '.csv':
                data = pd.read_csv(file_path)
            elif ext in ['.xlsx', '.xls']:
                data = pd.read_excel(file_path)
            elif ext == '.json':
                data = pd.read_json(file_path)
            else:
                logger.error(f"Unsupported data format: {ext}")
                return None
            
            # Standardize column names
            data.columns = [col.lower() for col in data.columns]
            
            # Check for required columns
            required = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            
            # Try to map common column names
            column_mapping = {
                'time': 'timestamp',
                'date': 'timestamp',
                'datetime': 'timestamp',
                'o': 'open',
                'h': 'high',
                'l': 'low',
                'c': 'close',
                'v': 'volume',
                'vol': 'volume'
            }
            
            for old, new in column_mapping.items():
                if old in data.columns and new not in data.columns:
                    data = data.rename(columns={old: new})
            
            return data
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None


class EquityChart(FigureCanvasQTAgg):
    """Matplotlib chart for equity curve"""
    
    def __init__(self, parent=None, width=8, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#1e1e1e')
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        
        # Style the plot
        self.axes.set_facecolor('#2d2d2d')
        self.axes.tick_params(colors='white', which='both')
        self.axes.spines['bottom'].set_color('white')
        self.axes.spines['left'].set_color('white')
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        
    def plot_equity(self, equity_curve, initial_capital):
        """Plot equity curve"""
        self.axes.clear()
        self.axes.set_facecolor('#2d2d2d')
        
        self.axes.plot(equity_curve, color='#4a9eff', linewidth=2)
        self.axes.axhline(y=initial_capital, color='gray', linestyle='--', alpha=0.5, label='Initial Capital')
        
        self.axes.set_title('Equity Curve', color='white', fontsize=14, pad=20)
        self.axes.set_xlabel('Candle', color='white')
        self.axes.set_ylabel('Capital ($)', color='white')
        self.axes.legend(facecolor='#2d2d2d', edgecolor='white', labelcolor='white')
        self.axes.grid(True, alpha=0.2, color='white')
        
        self.draw()


class StrategyTesterTab(QWidget):
    """Strategy testing tab with backtest capability"""
    
    def __init__(self):
        super().__init__()
        self.strategy_file = None
        self.data_file = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the strategy tester UI"""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("🧪 Strategy Backtester")
        header.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(header)
        
        # Instructions
        instructions = QLabel(
            "Upload your trading strategy and historical data to backtest. "
            "The system will parse your strategy, simulate trades, and show profitability results."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #aaa; padding: 5px;")
        layout.addWidget(instructions)
        
        # Splitter for drop zones and results
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Top section: Drop zones
        top_widget = QWidget()
        top_layout = QHBoxLayout()
        
        # Strategy drop zone
        strategy_group = QGroupBox("Step 1: Upload Strategy")
        strategy_layout = QVBoxLayout()
        
        self.strategy_drop = DropZone(
            "Drop Strategy File Here",
            "PDF (*.pdf);;Word (*.docx *.doc);;Excel (*.xlsx *.xls);;Text (*.txt);;Pine Script (*.pine);;All Files (*.*)"
        )
        self.strategy_drop.file_dropped.connect(self.on_strategy_uploaded)
        strategy_layout.addWidget(self.strategy_drop)
        
        strategy_hint = QLabel("✓ Accepted: PDF, Word, Excel, TXT, Pine Script")
        strategy_hint.setStyleSheet("color: #888; font-size: 10px;")
        strategy_layout.addWidget(strategy_hint)
        
        strategy_group.setLayout(strategy_layout)
        top_layout.addWidget(strategy_group)
        
        # Data drop zone
        data_group = QGroupBox("Step 2: Upload Chart Data")
        data_layout = QVBoxLayout()
        
        self.data_drop = DropZone(
            "Drop Chart Data Here",
            "CSV (*.csv);;Excel (*.xlsx *.xls);;JSON (*.json);;All Files (*.*)"
        )
        self.data_drop.file_dropped.connect(self.on_data_uploaded)
        data_layout.addWidget(self.data_drop)
        
        data_hint = QLabel("✓ Required columns: timestamp, open, high, low, close, volume")
        data_hint.setStyleSheet("color: #888; font-size: 10px;")
        data_layout.addWidget(data_hint)
        
        data_group.setLayout(data_layout)
        top_layout.addWidget(data_group)
        
        top_widget.setLayout(top_layout)
        splitter.addWidget(top_widget)
        
        # Middle section: Run button and progress
        middle_widget = QWidget()
        middle_layout = QVBoxLayout()
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.run_button = QPushButton("🚀 Run Backtest")
        self.run_button.setMinimumHeight(50)
        self.run_button.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px 30px;
            }
            QPushButton:hover {
                background-color: #3a8eef;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
        """)
        self.run_button.clicked.connect(self.run_backtest)
        self.run_button.setEnabled(False)
        button_layout.addWidget(self.run_button)
        
        button_layout.addStretch()
        middle_layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setVisible(False)
        middle_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Upload strategy and data files to begin")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #aaa; padding: 10px;")
        middle_layout.addWidget(self.status_label)
        
        middle_widget.setLayout(middle_layout)
        splitter.addWidget(middle_widget)
        
        # Bottom section: Results
        results_widget = QWidget()
        results_layout = QVBoxLayout()
        
        results_label = QLabel("📊 Backtest Results")
        results_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        results_layout.addWidget(results_label)
        
        # Results scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(300)
        
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout()
        self.results_widget.setLayout(self.results_layout)
        scroll.setWidget(self.results_widget)
        
        results_layout.addWidget(scroll)
        results_widget.setLayout(results_layout)
        splitter.addWidget(results_widget)
        
        # Set splitter sizes
        splitter.setSizes([300, 100, 400])
        layout.addWidget(splitter)
        
        self.setLayout(layout)
    
    def on_strategy_uploaded(self, file_path: str):
        """Handle strategy file upload"""
        self.strategy_file = file_path
        self.status_label.setText(f"✅ Strategy: {Path(file_path).name}")
        self.check_ready()
    
    def on_data_uploaded(self, file_path: str):
        """Handle data file upload"""
        self.data_file = file_path
        self.status_label.setText(f"✅ Data: {Path(file_path).name}")
        self.check_ready()
    
    def check_ready(self):
        """Check if ready to run backtest"""
        if self.strategy_file and self.data_file:
            self.run_button.setEnabled(True)
            self.status_label.setText("✅ Ready to run backtest!")
            self.status_label.setStyleSheet("color: #4caf50; padding: 10px; font-weight: bold;")
    
    def run_backtest(self):
        """Run the backtest"""
        self.run_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        
        # Clear previous results
        for i in reversed(range(self.results_layout.count())): 
            self.results_layout.itemAt(i).widget().setParent(None)
        
        # Start backtest thread
        self.backtest_thread = BacktestThread(self.strategy_file, self.data_file)
        self.backtest_thread.progress.connect(self.on_progress)
        self.backtest_thread.finished.connect(self.on_backtest_complete)
        self.backtest_thread.error.connect(self.on_backtest_error)
        self.backtest_thread.start()
    
    def on_progress(self, message: str):
        """Handle progress update"""
        self.status_label.setText(message)
    
    def on_backtest_complete(self, results: dict):
        """Handle backtest completion"""
        self.progress_bar.setVisible(False)
        self.run_button.setEnabled(True)
        
        if 'error' in results:
            self.on_backtest_error(results['error'])
            return
        
        self.status_label.setText("✅ Backtest Complete!")
        self.status_label.setStyleSheet("color: #4caf50; padding: 10px; font-weight: bold;")
        
        # Display results
        self.display_results(results)
    
    def on_backtest_error(self, error: str):
        """Handle backtest error"""
        self.progress_bar.setVisible(False)
        self.run_button.setEnabled(True)
        self.status_label.setText(f"❌ Error: {error}")
        self.status_label.setStyleSheet("color: #f44336; padding: 10px;")
        
        QMessageBox.critical(self, "Backtest Error", f"Failed to run backtest:\n\n{error}")
    
    def display_results(self, results: dict):
        """Display backtest results"""
        # Strategy info
        strategy_info = results.get('strategy_info', {})
        info_box = QGroupBox(f"Strategy: {strategy_info.get('strategy_name', 'Unknown')}")
        info_layout = QFormLayout()
        info_layout.addRow("Description:", QLabel(strategy_info.get('description', 'N/A')))
        info_layout.addRow("Timeframe:", QLabel(strategy_info.get('timeframe', 'N/A')))
        indicators = ', '.join(strategy_info.get('indicators', []))
        info_layout.addRow("Indicators:", QLabel(indicators or 'None specified'))
        info_box.setLayout(info_layout)
        self.results_layout.addWidget(info_box)
        
        # Performance metrics
        profitable = results.get('profitable', False)
        profit_color = '#4caf50' if profitable else '#f44336'
        
        metrics_box = QGroupBox("📈 Performance Metrics")
        metrics_layout = QFormLayout()
        
        # Profitability indicator
        profit_status = "✅ PROFITABLE" if profitable else "❌ NOT PROFITABLE"
        profit_label = QLabel(profit_status)
        profit_label.setStyleSheet(f"color: {profit_color}; font-weight: bold; font-size: 16px;")
        metrics_layout.addRow("Status:", profit_label)
        
        # Key metrics
        metrics_layout.addRow("Total Trades:", QLabel(str(results.get('total_trades', 0))))
        
        win_rate = results.get('win_rate', 0)
        win_rate_label = QLabel(f"{win_rate:.2f}%")
        win_rate_label.setStyleSheet(f"color: {'#4caf50' if win_rate > 50 else '#f44336'};")
        metrics_layout.addRow("Win Rate:", win_rate_label)
        
        total_return = results.get('total_return_percent', 0)
        return_label = QLabel(f"{total_return:.2f}%")
        return_label.setStyleSheet(f"color: {profit_color}; font-weight: bold;")
        metrics_layout.addRow("Total Return:", return_label)
        
        metrics_layout.addRow("Initial Capital:", QLabel(f"${results.get('initial_capital', 0):.2f}"))
        
        final_capital = results.get('final_capital', 0)
        final_label = QLabel(f"${final_capital:.2f}")
        final_label.setStyleSheet(f"color: {profit_color}; font-weight: bold;")
        metrics_layout.addRow("Final Capital:", final_label)
        
        total_profit = results.get('total_profit', 0)
        profit_label_widget = QLabel(f"${total_profit:.2f}")
        profit_label_widget.setStyleSheet(f"color: {profit_color}; font-weight: bold; font-size: 14px;")
        metrics_layout.addRow("Total Profit:", profit_label_widget)
        
        metrics_layout.addRow("Max Drawdown:", QLabel(f"{results.get('max_drawdown_percent', 0):.2f}%"))
        metrics_layout.addRow("Sharpe Ratio:", QLabel(f"{results.get('sharpe_ratio', 0):.2f}"))
        metrics_layout.addRow("Profit Factor:", QLabel(f"{results.get('profit_factor', 0):.2f}"))
        metrics_layout.addRow("Avg Trade Duration:", QLabel(f"{results.get('avg_trade_duration_hours', 0):.1f}h"))
        
        metrics_box.setLayout(metrics_layout)
        self.results_layout.addWidget(metrics_box)
        
        # Equity curve
        if 'equity_curve' in results:
            chart_box = QGroupBox("💹 Equity Curve")
            chart_layout = QVBoxLayout()
            
            chart = EquityChart()
            chart.plot_equity(results['equity_curve'], results.get('initial_capital', 10000))
            chart_layout.addWidget(chart)
            
            chart_box.setLayout(chart_layout)
            self.results_layout.addWidget(chart_box)
        
        # Trade breakdown
        trade_box = QGroupBox("📋 Trade Breakdown")
        trade_layout = QFormLayout()
        trade_layout.addRow("Winning Trades:", QLabel(str(results.get('winning_trades', 0))))
        trade_layout.addRow("Losing Trades:", QLabel(str(results.get('losing_trades', 0))))
        trade_layout.addRow("Average Win:", QLabel(f"${results.get('avg_win', 0):.2f}"))
        trade_layout.addRow("Average Loss:", QLabel(f"${results.get('avg_loss', 0):.2f}"))
        trade_box.setLayout(trade_layout)
        self.results_layout.addWidget(trade_box)
        
        self.results_layout.addStretch()
    
    def update_display(self):
        """Update display (called by main window timer)"""
        pass
