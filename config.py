from typing import Dict, Any, Union
from pathlib import Path
import json

class ConfigLoader:
    """Dynamic configuration loader with fallback chaining."""

    def __init__(self, file_path: Union[str, Path] = "config.json") -> None:
        self.path: Path = Path(file_path)
        self.data: Dict[str, Any] = {}

    def load(self) -> Dict[str, Any]:
        """Loads json data or returns empty mapping."""
        try:
            if self.path.exists():
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
        except (json.JSONDecodeError, OSError):
            self.data = {}
        return self.data

    def get_nested(self, key_path: str, default: Any = None) -> Any:
        """Retrieves value via dot-notation path."""
        keys = key_path.split(".")
        val = self.data
        try:
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            return default

    def __getitem__(self, key: str) -> Any:
        """Bracket syntax access for config."""
        return self.data.get(key)

def get_app_config(source: str = "config.json") -> ConfigLoader:
    """Factory function for config instantiation."""
    loader = ConfigLoader(source)
    loader.load()
    return loader