from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QScrollArea, QFrame, QDialog, QLineEdit, 
                             QFormLayout, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from database.db_handler import DBHandler
from utils.logger import logger

class HostDialog(QDialog):
    def __init__(self, parent=None, host_data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Host" if host_data else "Add New Host")
        self.setFixedWidth(400)
        self.layout = QVBoxLayout(self)
        self.form = QFormLayout()

        self.name_edit = QLineEdit()
        self.hostname_edit = QLineEdit()
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_edit = QLineEdit()
        
        # OS Type for Icons
        self.os_combo = QComboBox()
        self.os_combo.addItems(["Linux", "Ubuntu", "Debian", "CentOS", "Raspberry Pi", "Windows", "MacOS", "Generic"])

        if host_data:
            self.name_edit.setText(host_data.get('name', ''))
            self.hostname_edit.setText(host_data.get('hostname', ''))
            self.username_edit.setText(host_data.get('username', ''))
            self.password_edit.setText(host_data.get('password', ''))
            self.key_edit.setText(host_data.get('key_path', ''))
            
            index = self.os_combo.findText(host_data.get('os_type', 'Linux'))
            if index >= 0:
                self.os_combo.setCurrentIndex(index)

        self.form.addRow("Display Name:", self.name_edit)
        self.form.addRow("Hostname/IP:", self.hostname_edit)
        self.form.addRow("Username:", self.username_edit)
        self.form.addRow("Password:", self.password_edit)
        self.form.addRow("Key Path:", self.key_edit)
        self.form.addRow("OS Type:", self.os_combo)

        self.layout.addLayout(self.form)

        self.buttons = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        self.buttons.addWidget(self.save_btn)
        self.buttons.addWidget(self.cancel_btn)
        self.layout.addLayout(self.buttons)

    def get_data(self):
        return {
            "name": self.name_edit.text(),
            "hostname": self.hostname_edit.text(),
            "username": self.username_edit.text(),
            "password": self.password_edit.text(),
            "key_path": self.key_edit.text(),
            "os_type": self.os_combo.currentText()
        }

class HostCard(QFrame):
    connect_clicked = pyqtSignal(dict)
    edit_clicked = pyqtSignal(dict)
    delete_clicked = pyqtSignal(int)

    def __init__(self, host):
        super().__init__()
        self.host = host
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            HostCard { 
                background-color: #24283b; 
                border: 1px solid #414868; 
                border-radius: 8px; 
                margin: 5px;
            }
            HostCard:hover { border: 1px solid #7aa2f7; }
        """)
        
        self.layout = QHBoxLayout(self)
        
        # Icon mapping
        icons = {
            "Linux": "🐧",
            "Ubuntu": "🟠",
            "Debian": "🌀",
            "CentOS": "🟣",
            "Raspberry Pi": "🍓",
            "Windows": "🪟",
            "MacOS": "🍎",
            "Generic": "💻"
        }
        os_type = host.get('os_type', 'Linux')
        self.icon_label = QLabel(icons.get(os_type, "💻"))
        self.icon_label.setStyleSheet("font-size: 24px; padding: 10px;")
        self.layout.addWidget(self.icon_label)

        # Info
        self.info_layout = QVBoxLayout()
        self.name_label = QLabel(host['name'])
        self.name_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #7aa2f7;")
        self.detail_label = QLabel(f"{host['username']}@{host['hostname']}")
        self.detail_label.setStyleSheet("color: #565f89; font-size: 12px;")
        self.info_layout.addWidget(self.name_label)
        self.info_layout.addWidget(self.detail_label)
        self.layout.addLayout(self.info_layout)
        
        self.layout.addStretch()

        # Actions
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setStyleSheet("background-color: #7aa2f7; color: #1a1b26;")
        self.connect_btn.clicked.connect(lambda: self.connect_clicked.emit(self.host))
        
        self.edit_btn = QPushButton("✎")
        self.edit_btn.setToolTip("Edit")
        self.edit_btn.setFixedWidth(30)
        self.edit_btn.clicked.connect(lambda: self.edit_clicked.emit(self.host))

        self.delete_btn = QPushButton("🗑")
        self.delete_btn.setToolTip("Delete")
        self.delete_btn.setFixedWidth(30)
        self.delete_btn.setStyleSheet("color: #f7768e;")
        self.delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.host['id']))

        self.layout.addWidget(self.connect_btn)
        self.layout.addWidget(self.edit_btn)
        self.layout.addWidget(self.delete_btn)

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DBHandler()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Header
        self.header = QHBoxLayout()
        self.title = QLabel("Remote Hosts")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.add_btn = QPushButton("+ Add Host")
        self.add_btn.setStyleSheet("background-color: #bb9af7; color: #1a1b26; font-weight: bold;")
        self.add_btn.clicked.connect(self.on_add_host)
        
        self.header.addWidget(self.title)
        self.header.addStretch()
        self.header.addWidget(self.add_btn)
        self.layout.addLayout(self.header)

        # Host List Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.list_container)
        self.layout.addWidget(self.scroll)

        self.refresh_list()

    def refresh_list(self):
        # Clear current list
        for i in reversed(range(self.list_layout.count())): 
            self.list_layout.itemAt(i).widget().setParent(None)

        hosts = self.db.get_hosts()
        if not hosts:
            self.list_layout.addWidget(QLabel("No hosts found. Click 'Add Host' to get started!"))
        else:
            for host in hosts:
                card = HostCard(host)
                card.edit_clicked.connect(self.on_edit_host)
                card.delete_clicked.connect(self.on_delete_host)
                self.list_layout.addWidget(card)

    def on_add_host(self):
        dialog = HostDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            self.db.add_host(**data) # Passing os_type will fail for now, handled below
            logger.info(f"Host added: {data['name']}")
            self.refresh_list()

    def on_edit_host(self, host_data):
        dialog = HostDialog(self, host_data)
        if dialog.exec():
            data = dialog.get_data()
            self.db.update_host(host_data['id'], **data)
            logger.info(f"Host updated: {data['name']}")
            self.refresh_list()

    def on_delete_host(self, host_id):
        reply = QMessageBox.question(self, "Delete Host", "Are you sure you want to delete this host?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_host(host_id)
            logger.info(f"Host deleted: ID {host_id}")
            self.refresh_list()
