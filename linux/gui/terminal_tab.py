import pyte
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPlainTextEdit
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QTextCursor, QFont
from utils.logger import logger

class TerminalThread(QThread):
    """Thread to read output from the SSH shell and emit signals."""
    output_received = pyqtSignal(str)

    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.running = True

    def run(self):
        logger.info(f"TerminalThread started for {self.connection.hostname}")
        while self.running:
            if self.connection.recv_ready():
                try:
                    output = self.connection.receive_output()
                    if output:
                        self.output_received.emit(output)
                except Exception as e:
                    logger.error(f"Error receiving SSH output: {e}")
            self.msleep(10) # 10ms sleep to prevent CPU hogging

    def stop(self):
        self.running = False

class TerminalTab(QWidget):
    def __init__(self, host_name="New Session", connection=None):
        super().__init__()
        self.host_name = host_name
        self.connection = connection
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Terminal Display
        self.terminal_display = QPlainTextEdit()
        self.terminal_display.setReadOnly(True)
        self.terminal_display.setFont(QFont("Monospace", 11))
        self.terminal_display.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1a1b26;
                color: #a9b1d6;
                border: none;
            }
        """)
        self.layout.addWidget(self.terminal_display)

        # Terminal Emulator State (pyte)
        self.screen = pyte.Screen(80, 24)
        self.stream = pyte.Stream(self.screen)

        if self.connection:
            self.start_session()

    def start_session(self):
        """Start the interactive SSH session and output thread."""
        if self.connection.open_shell():
            self.thread = TerminalThread(self.connection)
            self.thread.output_received.connect(self.update_display)
            self.thread.start()
            logger.info(f"Terminal session started for {self.host_name}")
        else:
            self.terminal_display.appendPlainText("Failed to open interactive shell.")

    def update_display(self, data):
        """Update the display with new data from the SSH session."""
        self.stream.feed(data)
        
        # Simple rendering for now: display the screen content
        # In a full emulator, we would handle updates more surgically
        cursor = self.terminal_display.textCursor()
        cursor.movePosition(QTextCursor.MovePosition.End)
        self.terminal_display.setTextCursor(cursor)
        self.terminal_display.insertPlainText(data)
        
        # Ensure scroll to bottom
        self.terminal_display.verticalScrollBar().setValue(
            self.terminal_display.verticalScrollBar().maximum()
        )

    def keyPressEvent(self, event):
        """Handle key presses and send them to the SSH session."""
        if not self.connection or not self.connection.shell:
            super().keyPressEvent(event)
            return

        text = event.text()
        if event.key() == Qt.Key.Key_Return:
            self.connection.send_command("\n")
        elif event.key() == Qt.Key.Key_Backspace:
            self.connection.send_command("\b")
        elif text:
            self.connection.send_command(text)
        
        event.accept()

    def closeEvent(self, event):
        """Clean up when the tab is closed."""
        if hasattr(self, 'thread'):
            self.thread.stop()
            self.thread.wait()
        if self.connection:
            self.connection.disconnect()
        logger.info(f"Terminal tab closed: {self.host_name}")
        super().closeEvent(event)
