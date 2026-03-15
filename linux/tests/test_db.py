import sys
import os

# Add the linux directory to the path so we can import the database module
linux_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(linux_dir)

from database.db_handler import DBHandler

def test_db():
    db_path = "test_shellixa.db"
    
    # Clean up existing test db
    if os.path.exists(db_path):
        os.remove(db_path)
        
    db = DBHandler(db_path)
    
    # 1. Test Groups
    print("Testing Groups...")
    gid = db.add_group("Production")
    print(f"Added group: {gid}")
    
    groups = db.get_groups()
    assert len(groups) == 1
    assert groups[0]['name'] == "Production"
    
    db.update_group(gid, name="Production Servers")
    groups = db.get_groups()
    assert groups[0]['name'] == "Production Servers"
    print("Groups CRUD OK.")
    
    # 2. Test Hosts
    print("Testing Hosts...")
    hid = db.add_host("Web01", "192.168.1.10", "admin", group_id=gid)
    print(f"Added host: {hid}")
    
    hosts = db.get_hosts()
    assert len(hosts) == 1
    assert hosts[0]['name'] == "Web01"
    assert hosts[0]['group_id'] == gid
    
    db.update_host(hid, name="WebServer-01", hostname="10.0.0.1")
    hosts = db.get_hosts()
    assert hosts[0]['name'] == "WebServer-01"
    assert hosts[0]['hostname'] == "10.0.0.1"
    
    db.delete_host(hid)
    assert len(db.get_hosts()) == 0
    print("Hosts CRUD OK.")
    
    db.delete_group(gid)
    assert len(db.get_groups()) == 0
    print("Group deletion OK.")
    
    db.close()
    os.remove(db_path)
    print("\nAll DB tests passed!")

if __name__ == "__main__":
    test_db()
