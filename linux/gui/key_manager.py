from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QDialog, QLineEdit, QFormLayout, QMessageBox, QFileDialog, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from database.db_handler import DBHandler
from utils.logger import logger
from utils.ssh_utils import generate_ssh_key
import os

class KeyDialog(QDialog):
    """Dialog for key generation or import metadata."""
    def __init__(self, parent=None, is_import=False):
        super().__init__(parent)
        self.setWindowTitle("Import SSH Key" if is_import else "Generate New SSH Key")
        self.setFixedWidth(400)
        self.layout = QVBoxLayout(self)
        self.form = QFormLayout()

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g., Work Laptop")
        
        self.path_edit = QLineEdit()
        if is_import:
            self.path_btn = QPushButton("Browse...")
            self.path_btn.clicked.connect(self.browse_path)
            path_layout = QHBoxLayout()
            path_layout.addWidget(self.path_edit)
            path_layout.addWidget(self.path_btn)
            self.form.addRow("Private Key Path:", path_layout)
        else:
            default_path = os.path.expanduser("~/.ssh/shellixa_key")
            self.path_edit.setText(default_path)
            self.form.addRow("Save Path:", self.path_edit)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["RSA (2048)", "RSA (4096)", "Ed25519"])
        self.form.addRow("Key Type:", self.type_combo)

        self.layout.addLayout(self.form)

        self.buttons = QHBoxLayout()
        self.ok_btn = QPushButton("Import" if is_import else "Generate")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        self.buttons.addWidget(self.ok_btn)
        self.buttons.addWidget(self.cancel_btn)
        self.layout.addLayout(self.buttons)

    def browse_path(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Private Key")
        if file_path:
            self.path_edit.setText(file_path)

    def get_data(self):
        t = self.type_combo.currentText()
        key_type = "RSA" if "RSA" in t else "Ed25519"
        bits = 4096 if "4096" in t else 2048
        return {
            "name": self.name_edit.text(),
            "path": self.path_edit.text(),
            "type": key_type,
            "bits": bits
        }

class KeyManager(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DBHandler()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.title = QLabel("SSH Vault")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: #a9b1d6;")
        self.layout.addWidget(self.title)

        # Key Table
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Path", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 120)
        self.table.setStyleSheet("""
            QTableWidget { 
                background-color: #1a1b26; 
                border: 1px solid #414868; 
                gridline-color: #414868;
                color: #a9b1d6;
            }
            QHeaderView::section { background-color: #24283b; color: #7aa2f7; border: 1px solid #414868; padding: 5px; }
        """)
        self.layout.addWidget(self.table)

        # Buttons
        self.btn_layout = QHBoxLayout()
        self.gen_btn = QPushButton("+ Generate Key")
        self.gen_btn.setStyleSheet("background-color: #bb9af7; color: #1a1b26; font-weight: bold;")
        self.gen_btn.clicked.connect(self.on_generate)
        
        self.import_btn = QPushButton("↓ Import Key")
        self.import_btn.clicked.connect(self.on_import)
        
        self.btn_layout.addWidget(self.gen_btn)
        self.btn_layout.addWidget(self.import_btn)
        self.btn_layout.addStretch()
        self.layout.addLayout(self.btn_layout)

        self.refresh_keys()

    def refresh_keys(self):
        self.table.setRowCount(0)
        keys = self.db.get_keys()
        for key in keys:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            self.table.setItem(row, 0, QTableWidgetItem(key['name']))
            self.table.setItem(row, 1, QTableWidgetItem(key['type']))
            self.table.setItem(row, 2, QTableWidgetItem(key['private_path']))

            # Actions Layout
            actions = QWidget()
            a_layout = QHBoxLayout(actions)
            a_layout.setContentsMargins(0, 0, 0, 0)
            
            del_btn = QPushButton("🗑")
            del_btn.setToolTip("Delete Key Reference")
            del_btn.setFixedWidth(30)
            del_btn.setStyleSheet("color: #f7768e; border: none;")
            del_btn.clicked.connect(lambda checked, kid=key['id']: self.on_delete(kid))
            
            a_layout.addWidget(del_btn)
            a_layout.addStretch()
            self.table.setCellWidget(row, 3, actions)

    def on_generate(self):
        dialog = KeyDialog(self, is_import=False)
        if dialog.exec():
            data = dialog.get_data()
            try:
                priv, pub = generate_ssh_key(data['path'], data['type'], data['bits'])
                self.db.add_key(data['name'], priv, pub, data['type'])
                QMessageBox.information(self, "Success", f"SSH Key generated and saved to:\n{priv}")
                self.refresh_keys()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to generate key: {e}")

    def on_import(self):
        dialog = KeyDialog(self, is_import=True)
        if dialog.exec():
            data = dialog.get_data()
            if not os.path.exists(data['path']):
                QMessageBox.warning(self, "Error", "Selected file does not exist.")
                return
            self.db.add_key(data['name'], data['path'], key_type=data['type'])
            self.refresh_keys()

    def on_delete(self, key_id):
        reply = QMessageBox.question(self, "Delete Key", "Remove this key from Shellixa? (File will not be deleted)",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_key(key_id)
            self.refresh_keys()
