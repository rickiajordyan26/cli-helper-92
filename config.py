import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = "config.json", defaults: Dict[str, Any] = None):
        self.path = path
        self.defaults = defaults or {}
        self._data = self.defaults.copy()
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    loaded = json.load(f)
                    self._data.update(loaded)
            except (json.JSONDecodeError, IOError):
                pass

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def save(self) -> None:
        with open(self.path, "w") as f:
            json.dump(self._data, f, indent=4)

    def update(self, **kwargs) -> None:
        self._data.update(kwargs)
        self.save()

def load_config(path: str = "config.json", defaults: Dict[str, Any] = None) -> ConfigLoader:
    return ConfigLoader(path, defaults)