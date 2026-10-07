import os
import json
from typing import Any, Dict

class Config:
    DEFAULTS = {
        "verbose": False,
        "max_retries": 3,
        "timeout": 30.0,
        "api_url": "https://api.example.com",
    }

    def __init__(self, filepath: str = None):
        self._config = self.DEFAULTS.copy()
        if filepath and os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    self._merge(json.load(f))
            except (json.JSONDecodeError, OSError):
                pass
        self._load_env_overrides()

    def _merge(self, data: Dict[str, Any]):
        for key, val in data.items():
            if key in self._config:
                expected_type = type(self._config[key])
                if expected_type is bool and isinstance(val, str):
                    self._config[key] = val.lower() in ("true", "1", "yes", "on")
                else:
                    try:
                        self._config[key] = expected_type(val)
                    except (ValueError, TypeError):
                        pass

    def _load_env_overrides(self):
        for key in self._config:
            env_var = f"CLI_{key.upper()}"
            if env_var in os.environ:
                self._merge({key: os.environ[env_var]})

    def __getattr__(self, name: str) -> Any:
        if name in self._config:
            return self._config[name]
        raise AttributeError(f"Configuration has no parameter {name!r}")

    def __repr__(self) -> str:
        return f"Config({self._config})"
