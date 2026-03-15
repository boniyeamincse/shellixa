from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QHBoxLayout
from gui.dashboard import Dashboard
from gui.terminal_tab import TerminalTab
from gui.sidebar import Sidebar
from gui.key_manager import KeyManager

class ShellixaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shellixa - Modern SSH Workstation")
        self.resize(1200, 800)
        self.setStyleSheet("background-color: #1a1b26; color: #a9b1d6;")

        # Main horizontal layout (Sidebar | Content)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.main_layout.addWidget(self.sidebar)

        # Content Area (Tabs)
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabWidget::pane { border: 1px solid #414868; }")
        
        self.dashboard = Dashboard()
        self.tabs.addTab(self.dashboard, "Dashboard")
        
        self.key_manager = KeyManager()
        self.tabs.addTab(self.key_manager, "Key Management")

        # Sample Terminal Tab
        self.terminal = TerminalTab("Home Server")
        self.tabs.addTab(self.terminal, "Home Server")

        self.main_layout.addWidget(self.tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Apply a global dark fusion-like style or similar
    window = ShellixaApp()
    window.show()
    sys.exit(app.exec())
