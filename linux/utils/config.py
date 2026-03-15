import json
import os

class Config:
    def __init__(self, config_file="config.json"):
        # Store config in the user's home directory would be better for a real app
        # For now, we'll keep it in the project root or local folder
        self.config_file = config_file
        self.defaults = {
            "theme": "dark",
            "font_family": "Monospace",
            "font_size": 12,
            "auto_connect": False,
            "save_history": True,
            "last_connected_host": None,
            "language": "en"
        }
        self.data = self.load()

    def load(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                    # Merge user config with defaults to ensure all keys exist
                    return {**self.defaults, **user_config}
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.defaults.copy()
        return self.defaults.copy()

    def save(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key):
        return self.data.get(key, self.defaults.get(key))

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def reset_to_defaults(self):
        self.data = self.defaults.copy()
        self.save()
