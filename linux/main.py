import sys
from PyQt6.QtWidgets import (QApplication, QComboBox, QMainWindow, QTabWidget, QVBoxLayout,
                             QWidget, QHBoxLayout, QPushButton, QToolBar, QMessageBox)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
from database.db_handler import DBHandler
from gui.dashboard import Dashboard
from gui.sftp_browser import SFTPBrowser
from gui.snippet_library import SnippetLibrary
from gui.terminal_tab import TerminalTab
from gui.sidebar import Sidebar
from gui.key_manager import KeyManager
from gui.logs_viewer import LogsViewer
from utils.config import Config
from utils.logger import logger
from utils.theme import ThemeManager

def exception_hook(exctype, value, traceback):
    """Global exception handler to log uncaught exceptions."""
    logger.error("Uncaught Exception", exc_info=(exctype, value, traceback))
    sys.__excepthook__(exctype, value, traceback)

class ShellixaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("Initializing Shellixa Main Window")
        self.config = Config()
        self.theme_manager = ThemeManager(self.config)
        self.last_terminal = None
        
        self.setWindowTitle("Shellixa - Modern SSH Workstation")
        self.resize(1200, 800)
        self.theme_manager.apply_theme(self)

        # Main Layout Setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Sidebar
        self.sidebar_visible = True
        self.sidebar = Sidebar()
        self.sidebar.host_selected.connect(self.on_host_selected)
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
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
        self.dashboard = Dashboard()
        self.dashboard.connect_requested.connect(self.on_host_selected)
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

        self.snippet_library = SnippetLibrary()
        self.snippet_library.snippet_run_requested.connect(self.run_snippet_on_active_tab)
        self.tabs.addTab(self.snippet_library, "Snippets")
        self.tabs.tabBar().setTabButton(3, self.tabs.tabBar().ButtonPosition.RightSide, None)

        self.sftp_browser = SFTPBrowser()
        self.tabs.addTab(self.sftp_browser, "SFTP")
        self.tabs.tabBar().setTabButton(4, self.tabs.tabBar().ButtonPosition.RightSide, None)

        # Initial Session
        self.add_terminal_tab("Local Terminal")

        self.content_layout.addWidget(self.tabs)
        self.main_layout.addWidget(self.content_container)
        
        logger.info("Shellixa Main Window Loaded Successfully")

    def auth_gate(self):
        """Show login or setup dialog to unlock the vault."""
        meta = self.db.get_security_metadata()
        is_setup = not ('master_salt' in meta and 'master_pw_hash' in meta)
        
        login = LoginDialog(self, is_setup=is_setup)
        if login.exec():
            logger.info("Vault unlocked successfully")
            # The LoginDialog already initializes SecurityManager on success
            # We must refresh UI components that might have loaded before auth 
            # (though here we call it before building UI)
            return True
        else:
            logger.warning("Vault unlock cancelled or failed")
            return False

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
        self.new_conn_btn.setProperty("class", "primary")
        self.new_conn_btn.clicked.connect(lambda: self.add_terminal_tab("New Session"))
        self.toolbar.addWidget(self.new_conn_btn)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme_manager.available_themes())
        current_theme = self.config.get("theme")
        current_index = self.theme_combo.findText(current_theme)
        if current_index >= 0:
            self.theme_combo.setCurrentIndex(current_index)
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        self.toolbar.addWidget(self.theme_combo)

    def on_host_selected(self, host_data):
        """Handle host selection from sidebar with credential inheritance."""
        from backend.ssh_connection import SSHConnection
        
        # Inheritance Logic
        final_user = host_data.get('username')
        final_pass = host_data.get('password')
        final_key = host_data.get('key_path')
        
        group_id = host_data.get('group_id')
        db = DBHandler()
        
        # Traverse up groups if credentials are missing
        while group_id and (not final_user or not (final_pass or final_key)):
            groups = db.get_groups() # This is inefficient (fetches all), but works for now
            group = next((g for g in groups if g['id'] == group_id), None)
            if not group: break
            
            if not final_user: final_user = group.get('username')
            if not final_pass: final_pass = group.get('password')
            if not final_key: final_key = group.get('key_path')
            
            group_id = group.get('parent_id')

        # Fallback to local user if still empty (maybe?) 
        # For now, just attempt connection
        conn = SSHConnection(host_data['hostname'], final_user, final_pass, final_key)
        if conn.connect():
            self.add_terminal_tab(host_data['name'], conn)
            # Update Dashboard/Sidebar Recents
            self.sidebar.refresh_data()
        else:
            QMessageBox.critical(self, "Connection Failed", f"Could not connect to {host_data['name']}")

    def add_terminal_tab(self, name, connection=None):
        terminal = TerminalTab(name, connection)
        index = self.tabs.addTab(terminal, name)
        self.tabs.setCurrentIndex(index)
        self.on_tab_changed(index)
        logger.info(f"New terminal tab added: {name}")

    def close_tab(self, index):
        if index > 4: # Don't close Dashboard, Key Manager, Logs, Snippets, or SFTP
            widget = self.tabs.widget(index)
            if widget is self.last_terminal:
                self.last_terminal = None
            if widget:
                widget.close() # TerminalTab handles its own cleanup in closeEvent
            self.tabs.removeTab(index)
            logger.info(f"Tab at index {index} removed")

    def get_active_terminal(self):
        widget = self.tabs.currentWidget()
        if isinstance(widget, TerminalTab):
            return widget
        return self.last_terminal

    def run_snippet_on_active_tab(self, command):
        terminal = self.get_active_terminal()
        if not terminal:
            QMessageBox.information(self, "No Active Terminal", "Open or select a terminal tab before running a snippet.")
            return
        terminal.execute_command(command)

    def on_tab_changed(self, index):
        widget = self.tabs.widget(index)
        if isinstance(widget, TerminalTab) and widget.connection:
            self.last_terminal = widget
            self.sftp_browser.set_connection(widget.connection, widget.host_name)
        elif widget is self.sftp_browser and self.last_terminal and self.last_terminal.connection:
            self.sftp_browser.set_connection(self.last_terminal.connection, self.last_terminal.host_name)
        else:
            self.sftp_browser.set_connection(None, None)

    def change_theme(self, theme_name):
        self.theme_manager.apply_theme(self, theme_name)
        self.sidebar.refresh_data()

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
