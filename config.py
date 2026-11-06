import json
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
                loaded = json.load(f)
                return {**self.defaults, **loaded}
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

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __repr__(self) -> str:
        return f"ConfigLoader(source='{self.path}', keys={list(self.data.keys())})"