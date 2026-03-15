import sqlite3
import base64
from utils.logger import logger
from utils.security import SecurityManager

class DBHandler:
    def __init__(self, db_path="shellixa.db"):
        logger.info(f"Initializing database at {db_path}")
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Groups Table (with support for inherited credentials)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                parent_id INTEGER,
                username TEXT,
                password TEXT,
                key_path TEXT,
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
                os_type TEXT DEFAULT 'Linux',
                group_id INTEGER,
                favorite INTEGER DEFAULT 0,
                last_connected DATETIME,
                FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE SET NULL
            )
        ''')
        # SSH Keys Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ssh_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                private_path TEXT NOT NULL,
                public_path TEXT,
                type TEXT DEFAULT 'RSA',
                passphrase TEXT
            )
        ''')
        # Metadata Table (Security stuff)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        self.conn.commit()
        logger.debug("Database tables created/verified")

    # --- Security Metadata ---
    def set_master_password(self, password):
        """Set the master password hash and salt for the first time."""
        salt = SecurityManager.generate_salt()
        pw_hash = SecurityManager.hash_password(password, salt)
        
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)', 
                      ('master_salt', base64.b64encode(salt).decode()))
        cursor.execute('INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)', 
                      ('master_pw_hash', base64.b64encode(pw_hash).decode()))
        self.conn.commit()
        return salt

    def get_security_metadata(self):
        """Retrieve salt and password hash from metadata."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT key, value FROM metadata WHERE key IN ("master_salt", "master_pw_hash")')
        rows = cursor.fetchall()
        return {row['key']: row['value'] for row in rows}

    # --- Group Operations ---
    def add_group(self, name, parent_id=None, username=None, password=None, key_path=None):
        logger.info(f"Adding new group: {name}")
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO groups (name, parent_id, username, password, key_path) 
            VALUES (?, ?, ?, ?, ?)
        ''', (name, parent_id, username, password, key_path))
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
    def add_host(self, name, hostname, username, password=None, key_path=None, group_id=None, os_type='Linux'):
        logger.info(f"Adding new host: {name} ({hostname})")
        
        # Encrypt sensitive fields
        sm = SecurityManager()
        enc_pass = sm.encrypt(password) if password else None
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO hosts (name, hostname, username, password, key_path, group_id, os_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, hostname, username, enc_pass, key_path, group_id, os_type))
        self.conn.commit()
        return cursor.lastrowid

    def get_recent_hosts(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM hosts WHERE last_connected IS NOT NULL ORDER BY last_connected DESC LIMIT ?', (limit,))
        
        rows = []
        sm = SecurityManager()
        for row in cursor.fetchall():
            d = dict(row)
            if d['password']:
                d['password'] = sm.decrypt(d['password'])
            rows.append(d)
        return rows

    def search_hosts(self, query):
        cursor = self.conn.cursor()
        q = f"%{query}%"
        cursor.execute('SELECT * FROM hosts WHERE name LIKE ? OR hostname LIKE ? OR username LIKE ?', (q, q, q))
        
        rows = []
        sm = SecurityManager()
        for row in cursor.fetchall():
            d = dict(row)
            if d['password']:
                d['password'] = sm.decrypt(d['password'])
            rows.append(d)
        return rows

    def update_last_connected(self, host_id):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE hosts SET last_connected = CURRENT_TIMESTAMP WHERE id = ?', (host_id,))
        self.conn.commit()
        logger.debug(f"Updated last_connected for host {host_id}")

    def get_hosts(self, group_id=None):
        cursor = self.conn.cursor()
        if group_id:
            cursor.execute('SELECT * FROM hosts WHERE group_id = ?', (group_id,))
        else:
            cursor.execute('SELECT * FROM hosts')
        
        rows = []
        sm = SecurityManager()
        for row in cursor.fetchall():
            d = dict(row)
            if d['password']:
                d['password'] = sm.decrypt(d['password'])
            rows.append(d)
        return rows

    def update_host(self, host_id, **kwargs):
        logger.info(f"Updating host id {host_id}")
        if not kwargs:
            return
        
        # Encrypt password if updated
        if 'password' in kwargs and kwargs['password']:
            sm = SecurityManager()
            kwargs['password'] = sm.encrypt(kwargs['password'])

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

    # --- Key Operations ---
    def add_key(self, name, private_path, public_path=None, key_type='RSA', passphrase=None):
        logger.info(f"Adding new SSH key: {name}")
        
        # Encrypt passphrase if provided
        sm = SecurityManager()
        enc_passphrase = sm.encrypt(passphrase) if passphrase else None
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO ssh_keys (name, private_path, public_path, type, passphrase)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, private_path, public_path, key_type, enc_passphrase))
        self.conn.commit()
        return cursor.lastrowid

    def get_keys(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM ssh_keys')
        
        rows = []
        sm = SecurityManager()
        for row in cursor.fetchall():
            d = dict(row)
            if d['passphrase']:
                d['passphrase'] = sm.decrypt(d['passphrase'])
            rows.append(d)
        return rows

    def delete_key(self, key_id):
        logger.warning(f"Deleting key id {key_id}")
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM ssh_keys WHERE id = ?', (key_id,))
        self.conn.commit()

    def close(self):
        logger.info("Closing database connection")
        self.conn.close()
