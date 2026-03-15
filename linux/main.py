import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, 
                             QWidget, QHBoxLayout, QPushButton, QToolBar)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
from gui.dashboard import Dashboard
from gui.terminal_tab import TerminalTab
from gui.sidebar import Sidebar
from gui.key_manager import KeyManager

class ShellixaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shellixa - Modern SSH Workstation")
        self.resize(1200, 800)
        
        # Apply Global Style (Tokyo Night inspired)
        self.setStyleSheet("""
            QMainWindow { background-color: #1a1b26; }
            QWidget { background-color: #1a1b26; color: #a9b1d6; font-family: 'Segoe UI', sans-serif; }
            QTabWidget::pane { border: 1px solid #414868; top: -1px; background-color: #1a1b26; }
            QTabBar::tab { background: #24283b; padding: 10px 20px; border-top-left-radius: 4px; border-top-right-radius: 4px; margin-right: 2px; }
            QTabBar::tab:selected { background: #414868; color: #7aa2f7; border-bottom: 2px solid #7aa2f7; }
            QPushButton { background-color: #24283b; border: 1px solid #414868; padding: 5px 15px; border-radius: 3px; }
            QPushButton:hover { background-color: #414868; }
            QToolBar { background-color: #16161e; border-bottom: 1px solid #414868; spacing: 10px; padding: 5px; }
        """)

        # Main Layout Setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Sidebar
        self.sidebar_visible = True
        self.sidebar = Sidebar()
        self.main_layout.addWidget(self.sidebar)

        # 2. Content Area Container
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # Toolbar for Top-level actions
        self.init_toolbar()

        # Tabs
        self.tabs = QTabWidget()
        self.dashboard = Dashboard()
        self.tabs.addTab(self.dashboard, "Dashboard")
        
        self.key_manager = KeyManager()
        self.tabs.addTab(self.key_manager, "Key Management")

        # Initial Session
        self.terminal = TerminalTab("Local Terminal")
        self.tabs.addTab(self.terminal, "Local Terminal")

        self.content_layout.addWidget(self.tabs)
        self.main_layout.addWidget(self.content_container)

    def init_toolbar(self):
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)
        self.toolbar.setMovable(False)

        # Toggle Sidebar Action
        self.toggle_sidebar_btn = QPushButton("☰")
        self.toggle_sidebar_btn.setToolTip("Toggle Sidebar")
        self.toggle_sidebar_btn.setFixedWidth(40)
        self.toggle_sidebar_btn.clicked.connect(self.toggle_sidebar)
        self.toolbar.addWidget(self.toggle_sidebar_btn)

        # New Connection Button
        self.new_conn_btn = QPushButton("+ New Connection")
        self.new_conn_btn.setStyleSheet("background-color: #2ac3de; color: #1a1b26; font-weight: bold;")
        self.toolbar.addWidget(self.new_conn_btn)

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.hide()
            self.sidebar_visible = False
        else:
            self.sidebar.show()
            self.sidebar_visible = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShellixaApp()
    window.show()
    sys.exit(app.exec())
