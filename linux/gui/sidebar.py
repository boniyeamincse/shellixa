from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, 
                             QLabel, QLineEdit, QHBoxLayout, QPushButton, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from database.db_handler import DBHandler
from utils.logger import logger

class Sidebar(QWidget):
    host_selected = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.db = DBHandler()
        self.setProperty("class", "sidebar")
        self.setFixedWidth(280)
        self.setStyleSheet("""
            QLineEdit { 
                border-radius: 4px; 
                padding: 5px; 
                margin-bottom: 10px;
            }
            QTreeWidget { 
                background-color: transparent; 
                border: none; 
                font-size: 13px;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 15, 10, 10)

        # 1. Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search hosts...")
        self.search_bar.textChanged.connect(self.filter_tree)
        self.layout.addWidget(self.search_bar)

        # 2. Main Tree (Favorites & Groups)
        self.label_connections = QLabel("CONNECTIONS")
        self.label_connections.setStyleSheet("font-weight: bold; font-size: 11px; margin-top: 10px;")
        self.label_connections.setProperty("class", "muted")
        self.layout.addWidget(self.label_connections)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(15)
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.layout.addWidget(self.tree)

        # 3. Recents Section
        self.label_recents = QLabel("RECENT SESSIONS")
        self.label_recents.setStyleSheet("font-weight: bold; font-size: 11px; margin-top: 20px;")
        self.label_recents.setProperty("class", "muted")
        self.layout.addWidget(self.label_recents)

        self.recent_list = QTreeWidget()
        self.recent_list.setHeaderHidden(True)
        self.recent_list.setMaximumHeight(150)
        self.recent_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.layout.addWidget(self.recent_list)

        self.refresh_data()

    def refresh_data(self):
        self.tree.clear()
        self.recent_list.clear()

        # Load Groups and their Hosts
        groups = self.db.get_groups()
        group_items = {}

        # First pass: Create group items
        for group in groups:
            item = QTreeWidgetItem([group['name']])
            item.setData(0, Qt.ItemDataRole.UserRole, {"type": "group", "id": group['id']})
            item.setIcon(0, QIcon.fromTheme("folder")) # Placeholder or emoji
            group_items[group['id']] = item

        # Second pass: Nest groups
        root_groups = []
        for group in groups:
            if group['parent_id'] and group['parent_id'] in group_items:
                group_items[group['parent_id']].addChild(group_items[group['id']])
            else:
                root_groups.append(group_items[group['id']])

        self.tree.addTopLevelItems(root_groups)

        # Third pass: Add hosts to groups or root
        hosts = self.db.get_hosts()
        for host in hosts:
            host_item = QTreeWidgetItem([host['name']])
            host_item.setData(0, Qt.ItemDataRole.UserRole, {"type": "host", "data": host})
            # OS Emoji mapping
            icons = {"Linux": "🐧", "Ubuntu": "🟠", "Windows": "🪟", "MacOS": "🍎"}
            host_item.setText(0, f"{icons.get(host['os_type'], '💻')} {host['name']}")
            
            if host['group_id'] and host['group_id'] in group_items:
                group_items[host['group_id']].addChild(host_item)
            else:
                self.tree.addTopLevelItem(host_item)

        # Load Recents
        recents = self.db.get_recent_hosts(limit=5)
        for host in recents:
            item = QTreeWidgetItem([host['name']])
            item.setData(0, Qt.ItemDataRole.UserRole, {"type": "host", "data": host})
            self.recent_list.addTopLevelItem(item)

        self.tree.expandAll()

    def filter_tree(self, text):
        """Recursive search filter for the tree."""
        query = text.lower()
        
        def filter_item(item):
            match = query in item.text(0).lower()
            child_matches = False
            for i in range(item.childCount()):
                if filter_item(item.child(i)):
                    child_matches = True
            
            show = match or child_matches
            item.setHidden(not show)
            if show and query:
                item.setExpanded(True)
            return show

        for i in range(self.tree.topLevelItemCount()):
            filter_item(self.tree.topLevelItem(i))
        
        # Also filter recents if needed, or just hide the section if empty
        for i in range(self.recent_list.topLevelItemCount()):
            item = self.recent_list.topLevelItem(i)
            item.setHidden(query not in item.text(0).lower())

    def on_item_double_clicked(self, item, column):
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data and data['type'] == 'host':
            host_data = data['data']
            logger.info(f"Host selected from sidebar: {host_data['name']}")
            self.host_selected.emit(host_data)
            # Update last connected in DB
            self.db.update_last_connected(host_data['id'])
            # Refresh recents list after a small delay or on next focus
