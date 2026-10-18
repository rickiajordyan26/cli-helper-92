import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = "config.json", defaults: Dict[str, Any] = None):
        self.path = path
        self.defaults = defaults or {}
        self.settings = self._load_recursive()

    def _load_recursive(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.path):
                with open(self.path, 'r') as f:
                    data = json.load(f)
                    return {**self.defaults, **data}
        except (json.JSONDecodeError, OSError):
            pass
        return self.defaults.copy()

    def __getitem__(self, key: str) -> Any:
        return self.settings.get(key)

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

def load_app_config() -> ConfigLoader:
    base = {
        "log_level": "INFO",
        "max_retries": 3,
        "timeout": 30.5
    }
    return ConfigLoader("settings.json", base)