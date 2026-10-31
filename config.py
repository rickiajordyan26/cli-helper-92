import json
import os
from typing import Any, Dict

class ConfigLoader:
    """A magical config loader that merges defaults with disk overrides."""
    def __init__(self, defaults: Dict[str, Any], path: str = 'config.json'):
        self.defaults = defaults
        self.path = path

    def load(self) -> Dict[str, Any]:
        data = self.defaults.copy()
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    disk_data = json.load(f)
                    data.update(disk_data)
            except (json.JSONDecodeError, IOError):
                pass
        return data

    @classmethod
    def create_if_missing(cls, defaults: Dict[str, Any], path: str = 'config.json') -> Dict[str, Any]:
        if not os.path.exists(path):
            with open(path, 'w') as f:
                json.dump(defaults, f, indent=4)
            return defaults
        return cls(defaults, path).load()

def get_app_config(config_defaults: Dict[str, Any]) -> Dict[str, Any]:
    return ConfigLoader.create_if_missing(config_defaults)