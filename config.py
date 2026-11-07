import json
import os
from pathlib import Path
from typing import Any, Dict, Union


class DynamicConfig(dict):
    """A hybrid dict allowing attribute access with environment & default fallbacks."""

    def __init__(self, defaults: Dict[str, Any] = None, **kwargs):
        super().__init__()
        self._defaults = defaults or {}
        self.update(kwargs)

    def __getitem__(self, key: str) -> Any:
        if key in self:
            val = super().__getitem__(key)
        elif key in self._defaults:
            val = self._defaults[key]
        else:
            env_val = os.getenv(key.upper())
            if env_val is not None:
                val = self._cast_env(env_val)
            else:
                raise KeyError(f"Config key '{key}' not found")

        if isinstance(val, dict) and not isinstance(val, DynamicConfig):
            sub_def = self._defaults.get(key, {}) if isinstance(self._defaults.get(key), dict) else {}
            return DynamicConfig(defaults=sub_def, **val)
        return val

    def __getattr__(self, item: str) -> Any:
        try:
            return self[item]
        except KeyError as err:
            raise AttributeError(err) from err

    @staticmethod
    def _cast_env(val: str) -> Union[int, float, bool, str]:
        if val.lower() in ("true", "false"):
            return val.lower() == "true"
        for cast in (int, float):
            try:
                return cast(val)
            except ValueError:
                pass
        return val


class ConfigLoader:
    """Loader that merges defaults, JSON file overrides, and dynamic environment variables."""

    DEFAULTS: Dict[str, Any] = {
        "app_name": "cli-helper-92",
        "debug": False,
        "timeout": 30,
        "output_format": "json",
        "max_retries": 3,
    }

    def __init__(self, path: Union[str, Path] = "config.json"):
        self.path = Path(path)

    def load(self) -> DynamicConfig:
        file_data: Dict[str, Any] = {}
        if self.path.is_file():
            try:
                file_data = json.loads(self.path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                file_data = {}
        merged = {**self.DEFAULTS, **file_data}
        return DynamicConfig(defaults=self.DEFAULTS, **merged)
