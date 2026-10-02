import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, filepath: str = 'config.json', defaults: Dict[str, Any] = None):
        self.filepath = filepath
        self.defaults = defaults or {}
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r') as f:
                    loaded = json.load(f)
                    return {**self.defaults, **loaded}
        except (json.JSONDecodeError, OSError):
            pass
        return self.defaults.copy()

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def reload(self):
        self._data = self._load()

def load_config(path: str, defaults: Dict[str, Any]) -> ConfigLoader:
    """
    Factory function for a persistent config bridge
    that merges dicts via dictionary unpacking magic.
    """
    loader = ConfigLoader(path, defaults)
    return loader