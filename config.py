import os
import json
from typing import Any, Dict

class ConfigLoader:
    """A whimsical configuration loader using lazy property patterns."""
    def __init__(self, filepath: str = "config.json", defaults: Dict[str, Any] = None):
        self.filepath = filepath
        self._defaults = defaults or {}
        self._data = {}

    def __getattr__(self, name: str) -> Any:
        if not self._data:
            self._load()
        return self._data.get(name, self._defaults.get(name))

    def _load(self) -> None:
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, "r") as f:
                    self._data = json.load(f)
            else:
                self._write_defaults()
        except (json.JSONDecodeError, IOError):
            self._data = self._defaults

    def _write_defaults(self) -> None:
        try:
            with open(self.filepath, "w") as f:
                json.dump(self._defaults, f, indent=4)
            self._data = self._defaults
        except IOError:
            pass

    def reload(self) -> None:
        self._data = {}

def get_config(defaults: Dict[str, Any] = None) -> ConfigLoader:
    return ConfigLoader(defaults=defaults or {})
