import sqlite3
from utils.logger import logger

class DBHandler:
    def __init__(self, db_path="shellixa.db"):
        logger.info(f"Initializing database at {db_path}")
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Groups Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                parent_id INTEGER,
                FOREIGN KEY (parent_id) REFERENCES groups (id)
            )
        ''')
        # Hosts Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hosts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                hostname TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT,
                key_path TEXT,
                group_id INTEGER,
                FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE SET NULL
            )
        ''')
        self.conn.commit()
        logger.debug("Database tables created/verified")

    # --- Group Operations ---
    def add_group(self, name, parent_id=None):
        logger.info(f"Adding new group: {name}")
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO groups (name, parent_id) VALUES (?, ?)', (name, parent_id))
        self.conn.commit()
        return cursor.lastrowid

    def get_groups(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM groups')
        return [dict(row) for row in cursor.fetchall()]

    def update_group(self, group_id, name=None, parent_id=None):
        logger.info(f"Updating group id {group_id}")
        cursor = self.conn.cursor()
        if name:
            cursor.execute('UPDATE groups SET name = ? WHERE id = ?', (name, group_id))
        if parent_id is not None:
            cursor.execute('UPDATE groups SET parent_id = ? WHERE id = ?', (parent_id, group_id))
        self.conn.commit()

    def delete_group(self, group_id):
        logger.warning(f"Deleting group id {group_id}")
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM groups WHERE id = ?', (group_id,))
        self.conn.commit()

    # --- Host Operations ---
    def add_host(self, name, hostname, username, password=None, key_path=None, group_id=None):
        logger.info(f"Adding new host: {name} ({hostname})")
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO hosts (name, hostname, username, password, key_path, group_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, hostname, username, password, key_path, group_id))
        self.conn.commit()
        return cursor.lastrowid

    def get_hosts(self, group_id=None):
        cursor = self.conn.cursor()
        if group_id:
            cursor.execute('SELECT * FROM hosts WHERE group_id = ?', (group_id,))
        else:
            cursor.execute('SELECT * FROM hosts')
        return [dict(row) for row in cursor.fetchall()]

    def update_host(self, host_id, **kwargs):
        logger.info(f"Updating host id {host_id}")
        if not kwargs:
            return
        keys = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values())
        values.append(host_id)
        cursor = self.conn.cursor()
        cursor.execute(f'UPDATE hosts SET {keys} WHERE id = ?', tuple(values))
        self.conn.commit()

    def delete_host(self, host_id):
        logger.warning(f"Deleting host id {host_id}")
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM hosts WHERE id = ?', (host_id,))
        self.conn.commit()

    def close(self):
        logger.info("Closing database connection")
        self.conn.close()
