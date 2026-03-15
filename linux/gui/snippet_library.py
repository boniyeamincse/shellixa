from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from database.db_handler import DBHandler
from utils.logger import logger


class SnippetDialog(QDialog):
    def __init__(self, parent=None, snippet=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Snippet" if snippet else "Add Snippet")
        self.setMinimumWidth(520)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.title_edit = QLineEdit(snippet["title"] if snippet else "")
        self.tags_edit = QLineEdit(snippet["tags"] if snippet else "")
        self.command_edit = QTextEdit(snippet["command"] if snippet else "")
        self.command_edit.setMinimumHeight(160)

        form.addRow("Title:", self.title_edit)
        form.addRow("Tags:", self.tags_edit)
        form.addRow("Command:", self.command_edit)
        layout.addLayout(form)

        buttons = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        buttons.addStretch()
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)

    def get_data(self):
        return {
            "title": self.title_edit.text().strip(),
            "tags": self.tags_edit.text().strip(),
            "command": self.command_edit.toPlainText().strip(),
        }


class SnippetLibrary(QWidget):
    snippet_run_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.db = DBHandler()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        header = QHBoxLayout()
        title = QLabel("Snippet Library")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search snippets by title, tag, or command...")
        self.search_edit.textChanged.connect(self.refresh_table)

        add_btn = QPushButton("+ Add Snippet")
        add_btn.clicked.connect(self.add_snippet)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.search_edit, 1)
        header.addWidget(add_btn)
        layout.addLayout(header)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Title", "Tags", "Command", "Usage", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        layout.addWidget(self.table)

        self.empty_label = QLabel("Save reusable shell commands here and run them against the active terminal tab.")
        self.empty_label.setProperty("class", "muted")
        layout.addWidget(self.empty_label)

        self.refresh_table()

    def refresh_table(self):
        snippets = self.db.get_snippets(self.search_edit.text().strip() or None)
        self.table.setRowCount(0)
        self.empty_label.setVisible(not snippets)

        for snippet in snippets:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(snippet["title"]))
            self.table.setItem(row, 1, QTableWidgetItem(snippet["tags"]))
            self.table.setItem(row, 2, QTableWidgetItem(snippet["command"]))
            self.table.setItem(row, 3, QTableWidgetItem(str(snippet["usage_count"])))

            actions = QWidget()
            actions_layout = QHBoxLayout(actions)
            actions_layout.setContentsMargins(0, 0, 0, 0)

            run_btn = QPushButton("Run")
            edit_btn = QPushButton("Edit")
            delete_btn = QPushButton("Delete")

            run_btn.clicked.connect(lambda _, s=snippet: self.run_snippet(s))
            edit_btn.clicked.connect(lambda _, s=snippet: self.edit_snippet(s))
            delete_btn.clicked.connect(lambda _, s_id=snippet["id"]: self.delete_snippet(s_id))

            actions_layout.addWidget(run_btn)
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            self.table.setCellWidget(row, 4, actions)

    def add_snippet(self):
        dialog = SnippetDialog(self)
        if not dialog.exec():
            return
        data = dialog.get_data()
        if not data["title"] or not data["command"]:
            QMessageBox.warning(self, "Invalid Snippet", "Title and command are required.")
            return
        self.db.add_snippet(**data)
        logger.info(f"Snippet added: {data['title']}")
        self.refresh_table()

    def edit_snippet(self, snippet):
        dialog = SnippetDialog(self, snippet)
        if not dialog.exec():
            return
        data = dialog.get_data()
        if not data["title"] or not data["command"]:
            QMessageBox.warning(self, "Invalid Snippet", "Title and command are required.")
            return
        self.db.update_snippet(snippet["id"], **data)
        logger.info(f"Snippet updated: {data['title']}")
        self.refresh_table()

    def delete_snippet(self, snippet_id):
        reply = QMessageBox.question(
            self,
            "Delete Snippet",
            "Delete this snippet from the library?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_snippet(snippet_id)
            self.refresh_table()

    def run_snippet(self, snippet):
        self.db.increment_snippet_usage(snippet["id"])
        self.snippet_run_requested.emit(snippet["command"])
        logger.info(f"Snippet executed from library: {snippet['title']}")
        self.refresh_table()
