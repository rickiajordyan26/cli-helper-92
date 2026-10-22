import json
import os
from collections import ChainMap
from pathlib import Path
from typing import Any, Dict, Union


class CascadingConfig:
    """Dynamic configuration cascade resolving defaults, file configs, and environment overrides."""

    def __init__(self, defaults: Dict[str, Any], env_prefix: str = "CLI_"):
        self._defaults = defaults
        self._env_prefix = env_prefix
        self._file_config: Dict[str, Any] = {}
        self._runtime_overrides: Dict[str, Any] = {}
        self._rebuild_chain()

    def _rebuild_chain(self) -> None:
        env_map = {}
        for key, val in self._defaults.items():
            env_key = f"{self._env_prefix}{key.upper()}"
            if env_key in os.environ:
                raw_val = os.environ[env_key]
                target_type = type(val)
                try:
                    if target_type == bool:
                        env_map[key] = raw_val.lower() in ("1", "true", "yes")
                    else:
                        env_map[key] = target_type(raw_val)
                except (ValueError, TypeError):
                    env_map[key] = raw_val

        self._chain = ChainMap(self._runtime_overrides, env_map, self._file_config, self._defaults)

    def load_file(self, path: Union[str, Path]) -> "CascadingConfig":
        filepath = Path(path)
        if filepath.is_file():
            with open(filepath, "r", encoding="utf-8") as f:
                self._file_config = json.load(f)
            self._rebuild_chain()
        return self

    def override(self, **kwargs: Any) -> "CascadingConfig":
        self._runtime_overrides.update(kwargs)
        self._rebuild_chain()
        return self

    def __getattr__(self, item: str) -> Any:
        if item in self._chain:
            return self._chain[item]
        raise AttributeError(f"Configuration key '{item}' not found")

    def __getitem__(self, item: str) -> Any:
        return self._chain[item]

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._chain)


DEFAULT_CONFIG = {
    "theme": "dark",
    "timeout": 30,
    "verbose": False,
    "max_retries": 3,
    "output_format": "json",
}

config = CascadingConfig(defaults=DEFAULT_CONFIG)
