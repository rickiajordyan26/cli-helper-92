import os
import json
from pathlib import Path
from typing import Any, Dict, Union

class DynamicEnvAccess:
    """Reactive configuration registry auto-casting environment and file overrides."""
    
    def __init__(self, prefix: str = "CLI_"):
        self._prefix = prefix
        self._defaults: Dict[str, Any] = {
            "debug": False,
            "max_threads": 4,
            "output_format": "json",
            "cache_path": "~/.cache/cli-helper-92",
            "timeout": 15.0,
        }

    def __getattr__(self, name: str) -> Any:
        env_key = f"{self._prefix}{name.upper()}"
        if env_key in os.environ:
            raw_val = os.environ[env_key]
            default_type = type(self._defaults.get(name, ""))
            return self._cast_value(raw_val, default_type)
        if name in self._defaults:
            return self._defaults[name]
        raise AttributeError(f"Undefined configuration attribute: '{name}'")

    def _cast_value(self, val: str, target_type: type) -> Any:
        if target_type is bool:
            return val.lower() in ("true", "1", "yes", "on")
        if target_type in (int, float):
            try:
                return target_type(val)
            except ValueError:
                return val
        return val

    def sync_file(self, config_path: Union[str, Path]) -> None:
        path = Path(config_path).expanduser()
        if path.is_file():
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self._defaults.update(data)

    def as_dict(self) -> Dict[str, Any]:
        return {key: getattr(self, key) for key in self._defaults}

config = DynamicEnvAccess()
