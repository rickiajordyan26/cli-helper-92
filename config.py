import json
import os
from typing import Any, Dict

class ConfigManager:
    def __init__(self, path: str, defaults: Dict[str, Any]):
        self.path = path
        self.data = defaults
        self._load_and_merge()

    def _load_and_merge(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    loaded = json.load(f)
                    self.data.update({k: v for k, v in loaded.items() if k in self.data})
            except (json.JSONDecodeError, IOError):
                pass

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def persist(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

def load_config(path: str, defaults: Dict[str, Any]) -> ConfigManager:
    """Config wrapper with dictionary-like access semantics"""
    return ConfigManager(path, defaults)