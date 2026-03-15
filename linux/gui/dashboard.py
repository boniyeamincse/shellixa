from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Welcome to Shellixa Dashboard\nManage your hosts and sessions here.")
        self.layout.addWidget(self.label)
