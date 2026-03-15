from database.db_handler import DBHandler
from utils.security import SecurityManager
import sqlite3
import os

def test_encryption():
    db_file = "test_enc.db"
    if os.path.exists(db_file): os.remove(db_file)
    
    db = DBHandler(db_file)
    sm = SecurityManager()
    
    # 1. Setup Master Password
    password = "secret_password"
    salt = db.set_master_password(password)
    sm.initialize(password, salt)
    
    # 2. Add Host with sensitive data
    raw_pass = "root_password_123"
    db.add_host("SecureServer", "10.0.0.1", "root", password=raw_pass)
    
    # 3. Read directly from SQLite (Raw)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM hosts")
    stored_pass = cursor.fetchone()[0]
    conn.close()
    
    print(f"Raw Entry in DB: {stored_pass}")
    assert stored_pass != raw_pass, "ERROR: Password stored in plaintext!"
    print("SUCCESS: Database field is encrypted.")
    
    # 4. Read via DBHandler (Decrypted)
    hosts = db.get_hosts()
    decrypted_pass = hosts[0]['password']
    print(f"Decrypted via DBHandler: {decrypted_pass}")
    assert decrypted_pass == raw_pass, "ERROR: Decryption failed!"
    print("SUCCESS: Decryption works correctly.")
    
    db.close()
    os.remove(db_file)

if __name__ == "__main__":
    test_encryption()
