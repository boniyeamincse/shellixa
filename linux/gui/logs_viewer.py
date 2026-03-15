from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtCore import QTimer
import os

class LogsViewer(QWidget):
    def __init__(self, log_file="logs/shellixa.log"):
        super().__init__()
        self.log_file = log_file
        self.layout = QVBoxLayout(self)

        self.title = QLabel("Application Logs")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(self.title)

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet("background-color: #16161e; color: #a9b1d6; font-family: monospace;")
        self.layout.addWidget(self.log_display)

        self.btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_logs)
        self.clear_btn = QPushButton("Clear File")
        self.clear_btn.clicked.connect(self.clear_logs)
        
        self.btn_layout.addWidget(self.refresh_btn)
        self.btn_layout.addWidget(self.clear_btn)
        self.btn_layout.addStretch()
        self.layout.addLayout(self.btn_layout)

        # Auto-refresh timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_logs)
        self.timer.start(2000) # Refresh every 2 seconds

        self.refresh_logs()

    def refresh_logs(self):
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    # Show only last 100 lines for performance
                    lines = f.readlines()
                    self.log_display.setPlainText("".join(lines[-100:]))
                    # Scroll to bottom
                    self.log_display.verticalScrollBar().setValue(
                        self.log_display.verticalScrollBar().maximum()
                    )
            except Exception as e:
                self.log_display.setPlainText(f"Error reading logs: {e}")

    def clear_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write("")
            self.refresh_logs()
