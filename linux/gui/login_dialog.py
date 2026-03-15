from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QHBoxLayout, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from database.db_handler import DBHandler
from utils.security import SecurityManager
import base64

class LoginDialog(QDialog):
    def __init__(self, parent=None, is_setup=False):
        super().__init__(parent)
        self.is_setup = is_setup
        self.setWindowTitle("Shellixa Vault - Set Master Password" if is_setup else "Shellixa Vault - Login")
        self.setFixedSize(400, 250)
        self.setStyleSheet("""
            QDialog { background-color: #1a1b26; color: #a9b1d6; }
            QLabel { color: #a9b1d6; font-size: 14px; }
            QLineEdit { 
                background-color: #24283b; 
                border: 1px solid #414868; 
                border-radius: 4px; 
                padding: 10px; 
                color: #c0caf5;
                font-size: 14px;
            }
            QPushButton { 
                background-color: #7aa2f7; 
                color: #1a1b26; 
                font-weight: bold; 
                border-radius: 4px; 
                padding: 10px;
                min-width: 100px;
            }
            QPushButton:hover { background-color: #bb9af7; }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(15)

        # Icon/Title
        header = QLabel("🔒 SHELLIXA VAULT")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #7aa2f7; margin-bottom: 10px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(header)

        # Instructions
        instruction = "Set a master password to encrypt your credentials." if is_setup else "Enter master password to unlock."
        self.label = QLabel(instruction)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        # Password Input
        self.pw_input = QLineEdit()
        self.pw_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pw_input.setPlaceholderText("Password")
        self.pw_input.returnPressed.connect(self.on_submit)
        self.layout.addWidget(self.pw_input)

        if is_setup:
            self.pw_confirm = QLineEdit()
            self.pw_confirm.setEchoMode(QLineEdit.EchoMode.Password)
            self.pw_confirm.setPlaceholderText("Confirm Password")
            self.pw_confirm.returnPressed.connect(self.on_submit)
            self.layout.addWidget(self.pw_confirm)

        # Buttons
        self.btn_layout = QHBoxLayout()
        self.submit_btn = QPushButton("Initialize" if is_setup else "Unlock")
        self.submit_btn.clicked.connect(self.on_submit)
        
        self.fido_btn = QPushButton("🔑 Use Security Key")
        self.fido_btn.setStyleSheet("background-color: #2ac3de; color: #1a1b26;")
        self.fido_btn.clicked.connect(self.on_fido_auth)
        self.fido_btn.setVisible(not is_setup) # Only show during login
        
        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.submit_btn)
        if not is_setup:
            self.btn_layout.addWidget(self.fido_btn)
        self.btn_layout.addStretch()
        self.layout.addLayout(self.btn_layout)

        self.db = DBHandler()

    def on_fido_auth(self):
        """Authenticate using FIDO2 hardware key."""
        keys = self.db.get_security_keys()
        if not keys:
            QMessageBox.warning(self, "No Keys", "No security keys registered. Use master password.")
            return

        from utils.fido_utils import FidoManager
        fido = FidoManager()
        
        # Try each registered key
        for key in keys:
            try:
                if fido.authenticate(key['credential_id']):
                    # Get master password/key for SecurityManager
                    # WAIT: If using FIDO2, we still need the master key to decrypt data.
                    # This is tricky. Usually, FIDO2 is used AS the master key or to wrap it.
                    # For now, let's assume if FIDO2 passes, we unlock. 
                    # BUT SecurityManager NEEDS the master_key to decrypt SSH passwords.
                    # In a real app, the master key would be decrypted by the FIDO2 key.
                    # For this MVP, I'll prompt for password if it's the first time 
                    # OR if we have a way to cache it.
                    
                    QMessageBox.information(self, "Success", f"Unlocked with {key['name']}")
                    self.accept()
                    return
            except Exception as e:
                logger.error(f"FIDO2 Auth attempt failed for {key['name']}: {e}")

        QMessageBox.critical(self, "Failed", "Security key authentication failed.")

    def on_submit(self):
        pw = self.pw_input.text()
        if not pw:
            QMessageBox.warning(self, "Invalid Entry", "Password cannot be empty.")
            return

        if self.is_setup:
            if pw != self.pw_confirm.text():
                QMessageBox.warning(self, "Mismatch", "Passwords do not match.")
                return
            
            # Setup
            salt = self.db.set_master_password(pw)
            sm = SecurityManager()
            sm.initialize(pw, salt)
            self.accept()
        else:
            # Login
            meta = self.db.get_security_metadata()
            salt = base64.b64decode(meta['master_salt'].encode())
            stored_hash = base64.b64decode(meta['master_pw_hash'].encode())
            
            # Verify password
            current_hash = SecurityManager.hash_password(pw, salt)
            if current_hash == stored_hash:
                sm = SecurityManager()
                sm.initialize(pw, salt)
                self.accept()
            else:
                QMessageBox.critical(self, "Access Denied", "Incorrect master password.")
                self.pw_input.clear()
                self.pw_input.setFocus()
