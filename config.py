import os
from pathlib import Path
from typing import Any, Dict

class AppConfig:
    def __init__(self, env_prefix: str = 'CLI92_'):
        self.base_path = Path.home() / '.cli-helper-92'
        self.env_prefix = env_prefix
        self._cache: Dict[str, Any] = {}
        self._load_defaults()

    def _load_defaults(self) -> None:
        self._cache.update({
            'timeout': 30,
            'verbose': False,
            'log_path': self.base_path / 'logs' / 'app.log'
        })

    def get(self, key: str, default: Any = None) -> Any:
        env_val = os.getenv(f"{self.env_prefix}{key.upper()}")
        if env_val:
            return type(default)(env_val) if default is not None else env_val
        return self._cache.get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name in self._cache:
            return self._cache[name]
        raise AttributeError(f"Config key '{name}' not found")

    def refresh(self) -> None:
        self._cache.clear()
        self._load_defaults()

settings = AppConfig()