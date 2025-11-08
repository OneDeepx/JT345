"""Manual Trade Tab - Stub"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ManualTradeTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Manual Trade Tab - Under Development"))
        self.setLayout(layout)
    
    def update_display(self):
        pass
