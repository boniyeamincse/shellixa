from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QLabel

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(250)
        self.layout = QVBoxLayout(self)

        self.label = QLabel("CONNECTIONS")
        self.label.setStyleSheet("font-weight: bold; color: #565f89; margin-top: 10px;")
        self.layout.addWidget(self.label)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setStyleSheet("background-color: transparent; border: none; color: #a9b1d6;")

        # Sample Groups
        favorites = QTreeWidgetItem(self.tree, ["Favorites"])
        production = QTreeWidgetItem(self.tree, ["Production"])
        staging = QTreeWidgetItem(self.tree, ["Staging"])

        # Sample Hosts
        QTreeWidgetItem(favorites, ["Home Server"])
        QTreeWidgetItem(production, ["Main DB", "Web cluster"])
        QTreeWidgetItem(staging, ["Testing Node"])

        self.tree.expandAll()
        self.layout.addWidget(self.tree)
