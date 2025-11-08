"""Charts Tab - Stub"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ChartsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Charts Tab - Under Development"))
        self.setLayout(layout)
    
    def update_display(self):
        pass
