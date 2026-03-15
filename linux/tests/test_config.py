import sys
import os

# Add the linux directory to the path
linux_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(linux_dir)

from utils.config import Config

def test_config():
    test_file = "test_config.json"
    if os.path.exists(test_file):
        os.remove(test_file)
        
    conf = Config(test_file)
    
    # 1. Test Defaults
    print("Testing defaults...")
    assert conf.get("theme") == "dark"
    assert conf.get("font_size") == 12
    assert conf.get("auto_connect") is False
    
    # 2. Test Set & Save
    print("Testing set and save...")
    conf.set("theme", "light")
    conf.set("font_size", 14)
    conf.set("auto_connect", True)
    
    # Reload to verify persistence
    conf2 = Config(test_file)
    assert conf2.get("theme") == "light"
    assert conf2.get("font_size") == 14
    assert conf2.get("auto_connect") is True
    
    # 3. Test Add New Key
    print("Testing dynamic keys...")
    conf.set("custom_setting", "enabled")
    conf3 = Config(test_file)
    assert conf3.get("custom_setting") == "enabled"
    
    # 4. Test Reset
    print("Testing reset...")
    conf.reset_to_defaults()
    assert conf.get("theme") == "dark"
    assert conf.get("font_size") == 12
    
    if os.path.exists(test_file):
        os.remove(test_file)
    print("\nAll Config tests passed!")

if __name__ == "__main__":
    test_config()
