import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str, defaults: Dict[str, Any]):
        self.path = path
        self.defaults = defaults
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            self._save(self.defaults)
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                loaded = json.load(f)
                return {**self.defaults, **loaded}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def _save(self, data: Dict[str, Any]) -> None:
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

def load_config(path: str = 'config.json', **defaults) -> ConfigLoader:
    return ConfigLoader(path, defaults)