import json
import os

class Config:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.defaults = {
            "theme": "dark",
            "font_size": 12,
            "save_history": True,
            "last_host": None
        }
        self.data = self.load()

    def load(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return {**self.defaults, **json.load(f)}
            except:
                return self.defaults
        return self.defaults

    def save(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self.save()
