import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, file_path: str = "config.json", defaults: Dict[str, Any] = None):
        self.file_path = file_path
        self.defaults = defaults or {}
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.file_path):
            return self.defaults
        with open(self.file_path, "r") as f:
            try:
                loaded = json.load(f)
                return {**self.defaults, **loaded}
            except json.JSONDecodeError:
                return self.defaults

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def __getattr__(self, item: str) -> Any:
        return self.data.get(item)

def get_config(path: str, defaults: Dict[str, Any] = None) -> ConfigLoader:
    return ConfigLoader(path, defaults or {})

if __name__ == "__main__":
    cfg = get_config("settings.json", {"debug": False, "port": 8080})
    print(f"Active port: {cfg.port}")