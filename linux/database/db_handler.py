import sqlite3

class DBHandler:
    def __init__(self, db_path="shellixa.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hosts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                hostname TEXT,
                username TEXT,
                password TEXT,
                key_path TEXT
            )
        ''')
        self.conn.commit()

    def add_host(self, name, hostname, username, password=None, key_path=None):
        cursor = self.conn.conn.cursor()
        cursor.execute('''
            INSERT INTO hosts (name, hostname, username, password, key_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, hostname, username, password, key_path))
        self.conn.commit()

    def get_hosts(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM hosts')
        return cursor.fetchall()
