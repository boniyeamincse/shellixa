from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QLabel

class KeyManager(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.title = QLabel("SSH Key Management")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(self.title)

        self.key_list = QListWidget()
        self.key_list.addItem("id_rsa (Default)")
        self.key_list.addItem("work_key.pem")
        self.layout.addWidget(self.key_list)

        self.btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add New Key")
        self.import_btn = QPushButton("Import")
        self.export_btn = QPushButton("Export Public")
        
        self.btn_layout.addWidget(self.add_btn)
        self.btn_layout.addWidget(self.import_btn)
        self.btn_layout.addWidget(self.export_btn)
        
        self.layout.addLayout(self.btn_layout)
