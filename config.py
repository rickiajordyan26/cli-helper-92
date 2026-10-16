import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic configuration loader with fallback defaults."""
    def __init__(self, filepath: str, defaults: Dict[str, Any] = None):
        self.filepath = filepath
        self.defaults = defaults or {}

    def load(self) -> Dict[str, Any]:
        try:
            if not os.path.exists(self.filepath):
                return self._write_defaults()
            
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                return {**self.defaults, **data}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def _write_defaults(self) -> Dict[str, Any]:
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.defaults, f, indent=4)
        except IOError:
            pass
        return self.defaults

def get_config(key: str, default: Any = None) -> Any:
    """Quick access helper for the loader instance."""
    loader = ConfigLoader('config.json', {'debug': False, 'version': '1.0.0'})
    return loader.load().get(key, default)