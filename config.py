import os
import json
from collections import ChainMap
from pathlib import Path
from typing import Any, Dict, Union

DEFAULT_CONFIG: Dict[str, Any] = {
    "app_name": "cli-helper-92",
    "debug": False,
    "max_retries": 3,
    "timeout": 30.0,
    "output_format": "json",
    "theme": "dark",
}

class DynamicConfig:
    """A flexible configuration loader using chained dictionaries and dynamic lookup."""
    
    def __init__(self, config_path: Union[str, Path, None] = None):
        self._user_file_config = self._load_file(config_path) if config_path else {}
        self._env_config = self._load_env_overrides()
        self._store = ChainMap(self._env_config, self._user_file_config, DEFAULT_CONFIG)

    def _load_file(self, path: Union[str, Path]) -> Dict[str, Any]:
        p = Path(path)
        if p.exists() and p.is_file():
            try:
                with p.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _load_env_overrides(self) -> Dict[str, Any]:
        overrides = {}
        prefix = "CLI_92_"
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                if config_key in DEFAULT_CONFIG:
                    target_type = type(DEFAULT_CONFIG[config_key])
                    overrides[config_key] = self._cast_val(value, target_type)
        return overrides

    @staticmethod
    def _cast_val(val: str, target_type: type) -> Any:
        if target_type is bool:
            return val.lower() in ("true", "1", "yes", "on")
        try:
            return target_type(val)
        except (ValueError, TypeError):
            return val

    def __getattr__(self, name: str) -> Any:
        if name in self._store:
            return self._store[name]
        raise AttributeError(f"Configuration key '{name}' not found")

    def __getitem__(self, item: str) -> Any:
        return self._store[item]

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._store)
