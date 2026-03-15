import os
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from utils.config import Config
from utils.logger import logger


class SFTPBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.connection = None
        self.host_name = None
        self.current_path = "."
        self.config = Config()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        header = QHBoxLayout()
        self.title = QLabel("SFTP Browser")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.status_label = QLabel("Select a connected SSH tab to browse remote files.")
        self.status_label.setProperty("class", "muted")
        header.addWidget(self.title)
        header.addStretch()
        header.addWidget(self.status_label)
        layout.addLayout(header)

        controls = QHBoxLayout()
        self.path_edit = QLineEdit(self.config.get("default_sftp_path"))
        self.path_edit.returnPressed.connect(self.refresh_directory)

        self.refresh_btn = QPushButton("Refresh")
        self.up_btn = QPushButton("Up")
        self.download_btn = QPushButton("Download")
        self.upload_btn = QPushButton("Upload")

        self.refresh_btn.clicked.connect(self.refresh_directory)
        self.up_btn.clicked.connect(self.go_up)
        self.download_btn.clicked.connect(self.download_selected)
        self.upload_btn.clicked.connect(self.upload_file)

        controls.addWidget(QLabel("Remote Path:"))
        controls.addWidget(self.path_edit, 1)
        controls.addWidget(self.refresh_btn)
        controls.addWidget(self.up_btn)
        controls.addWidget(self.download_btn)
        controls.addWidget(self.upload_btn)
        layout.addLayout(controls)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Size", "Modified"])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.itemDoubleClicked.connect(self.open_selected_item)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        self.set_enabled_state(False)

    def set_enabled_state(self, enabled):
        for widget in (self.path_edit, self.refresh_btn, self.up_btn, self.download_btn, self.upload_btn, self.table):
            widget.setEnabled(enabled)

    def set_connection(self, connection=None, host_name=None):
        self.connection = connection
        self.host_name = host_name
        if not connection:
            self.status_label.setText("Select a connected SSH tab to browse remote files.")
            self.table.setRowCount(0)
            self.set_enabled_state(False)
            return

        self.status_label.setText(f"Browsing {host_name}")
        self.set_enabled_state(True)
        self.path_edit.setText(self.config.get("default_sftp_path"))
        self.refresh_directory()

    def refresh_directory(self):
        if not self.connection:
            return
        path = self.path_edit.text().strip() or "."
        try:
            normalized = self.connection.normalize_remote_path(path)
            entries = self.connection.list_directory(normalized)
            self.current_path = normalized
            self.path_edit.setText(normalized)
            self.table.setRowCount(0)
            for entry in entries:
                row = self.table.rowCount()
                self.table.insertRow(row)
                name_item = QTableWidgetItem(entry["name"])
                name_item.setData(Qt.ItemDataRole.UserRole, entry)
                self.table.setItem(row, 0, name_item)
                self.table.setItem(row, 1, QTableWidgetItem("Directory" if entry["is_dir"] else "File"))
                self.table.setItem(row, 2, QTableWidgetItem("-" if entry["is_dir"] else str(entry["size"])))
                modified = datetime.fromtimestamp(entry["mtime"]).strftime("%Y-%m-%d %H:%M")
                self.table.setItem(row, 3, QTableWidgetItem(modified))
        except Exception as error:
            logger.error(f"Failed to list remote directory {path}: {error}")
            QMessageBox.critical(self, "SFTP Error", f"Failed to list remote directory:\n{error}")

    def selected_entry(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return None
        item = self.table.item(current_row, 0)
        return item.data(Qt.ItemDataRole.UserRole) if item else None

    def open_selected_item(self, *_args):
        entry = self.selected_entry()
        if entry and entry["is_dir"]:
            self.path_edit.setText(entry["path"])
            self.refresh_directory()

    def go_up(self):
        if not self.current_path or self.current_path == "/":
            return
        parent = os.path.dirname(self.current_path.rstrip("/")) or "/"
        self.path_edit.setText(parent)
        self.refresh_directory()

    def download_selected(self):
        entry = self.selected_entry()
        if not entry or entry["is_dir"]:
            QMessageBox.information(self, "Download", "Select a file to download.")
            return
        local_path, _ = QFileDialog.getSaveFileName(self, "Save Remote File", entry["name"])
        if not local_path:
            return
        try:
            self.connection.download_file(entry["path"], local_path)
        except Exception as error:
            logger.error(f"Failed to download {entry['path']}: {error}")
            QMessageBox.critical(self, "Download Failed", str(error))

    def upload_file(self):
        if not self.connection:
            return
        local_path, _ = QFileDialog.getOpenFileName(self, "Upload File")
        if not local_path:
            return
        remote_path = f"{self.current_path.rstrip('/')}/{os.path.basename(local_path)}" if self.current_path != "/" else f"/{os.path.basename(local_path)}"
        try:
            self.connection.upload_file(local_path, remote_path)
            self.refresh_directory()
        except Exception as error:
            logger.error(f"Failed to upload {local_path}: {error}")
            QMessageBox.critical(self, "Upload Failed", str(error))
