import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = 'config.json', defaults: Dict[str, Any] = None):
        self.path = path
        self.defaults = defaults or {}
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.defaults.copy()
        try:
            with open(self.path, 'r') as f:
                loaded = json.load(f)
                return {**self.defaults, **loaded}
        except (json.JSONDecodeError, IOError):
            return self.defaults.copy()

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f'Config has no attribute {name}')

def load_config(path: str, defaults: Dict[str, Any]) -> ConfigLoader:
    return ConfigLoader(path, defaults)