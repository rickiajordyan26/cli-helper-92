import json
import os
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = 'config.json', defaults: Dict[str, Any] = None):
        self.path = Path(path)
        self.defaults = defaults or {}
        self.data = self._initialize()

    def _initialize(self) -> Dict[str, Any]:
        if not self.path.exists():
            self._write_defaults()
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                content = json.load(f)
                return {**self.defaults, **content}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def _write_defaults(self) -> None:
        try:
            with open(self.path, 'w') as f:
                json.dump(self.defaults, f, indent=4)
        except IOError:
            pass

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

def load_app_config(defaults: Dict[str, Any]) -> ConfigLoader:
    return ConfigLoader(defaults=defaults)

# Example usage:
# config = load_app_config({'theme': 'dark', 'verbose': False})
# print(config.get('theme'))