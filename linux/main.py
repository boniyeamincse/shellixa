import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, 
                             QWidget, QHBoxLayout, QPushButton, QToolBar, QMessageBox)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
from gui.dashboard import Dashboard
from gui.terminal_tab import TerminalTab
from gui.sidebar import Sidebar
from gui.key_manager import KeyManager
from gui.logs_viewer import LogsViewer
from utils.logger import logger

def exception_hook(exctype, value, traceback):
    """Global exception handler to log uncaught exceptions."""
    logger.error("Uncaught Exception", exc_info=(exctype, value, traceback))
    sys.__excepthook__(exctype, value, traceback)

class ShellixaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("Initializing Shellixa Main Window")
        
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
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        self.dashboard = Dashboard()
        self.tabs.addTab(self.dashboard, "Dashboard")
        # Hide close button for Dashboard
        self.tabs.tabBar().setTabButton(0, self.tabs.tabBar().ButtonPosition.RightSide, None)
        
        self.key_manager = KeyManager()
        self.tabs.addTab(self.key_manager, "Key Management")
        self.tabs.tabBar().setTabButton(1, self.tabs.tabBar().ButtonPosition.RightSide, None)

        # Logs Viewer
        self.logs_viewer = LogsViewer()
        self.tabs.addTab(self.logs_viewer, "Logs")
        self.tabs.tabBar().setTabButton(2, self.tabs.tabBar().ButtonPosition.RightSide, None)

        # Initial Session
        self.add_terminal_tab("Local Terminal")

        self.content_layout.addWidget(self.tabs)
        self.main_layout.addWidget(self.content_container)
        
        logger.info("Shellixa Main Window Loaded Successfully")

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
        self.new_conn_btn.clicked.connect(lambda: self.add_terminal_tab("New Session"))
        self.toolbar.addWidget(self.new_conn_btn)

    def add_terminal_tab(self, name, connection=None):
        terminal = TerminalTab(name, connection)
        index = self.tabs.addTab(terminal, name)
        self.tabs.setCurrentIndex(index)
        logger.info(f"New terminal tab added: {name}")

    def close_tab(self, index):
        if index > 2: # Don't close Dashboard, Key Manager, or Logs
            widget = self.tabs.widget(index)
            if widget:
                widget.close() # TerminalTab handles its own cleanup in closeEvent
            self.tabs.removeTab(index)
            logger.info(f"Tab at index {index} removed")

    def toggle_sidebar(self):
        self.sidebar_visible = not self.sidebar_visible
        self.sidebar.setVisible(self.sidebar_visible)
        logger.debug(f"Sidebar visibility toggled to: {self.sidebar_visible}")

    def closeEvent(self, event):
        """Handle application shutdown."""
        logger.info("Application shutting down")
        # Ensure all tabs are closed to trigger their cleanup
        for i in range(self.tabs.count()-1, -1, -1):
            widget = self.tabs.widget(i)
            if widget:
                widget.close()
        event.accept()

if __name__ == "__main__":
    # Install exception hook
    sys.excepthook = exception_hook
    
    app = QApplication(sys.argv)
    window = ShellixaApp()
    window.show()
    sys.exit(app.exec())
