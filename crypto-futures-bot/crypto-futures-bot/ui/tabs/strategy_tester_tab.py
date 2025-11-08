"""Strategy Tester Tab - Stub"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class StrategyTesterTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Strategy Tester Tab - Under Development"))
        self.setLayout(layout)
    
    def update_display(self):
        pass
