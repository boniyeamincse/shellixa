from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QHBoxLayout, QPushButton

class TerminalTab(QWidget):
    def __init__(self, host_name="New Session"):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Terminal Display (Placeholder for real terminal emulator)
        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setStyleSheet("background-color: #1a1b26; color: #a9b1d6; font-family: monospace; font-size: 12pt;")
        self.layout.addWidget(self.terminal_output)

        # Input Area
        self.input_layout = QHBoxLayout()
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Enter command...")
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_command)
        
        self.input_layout.addWidget(self.input_line)
        self.input_layout.addWidget(self.send_button)
        self.layout.addLayout(self.input_layout)

    def send_command(self):
        command = self.input_line.text()
        if command:
            self.terminal_output.append(f"<font color='#7aa2f7'>$ {command}</font>")
            self.input_line.clear()
            # Logic to send command to SSH backend would go here
