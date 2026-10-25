import os
from pathlib import Path
from typing import Any, Dict

class AppConfig:
    """A dictionary-like bridge to environment settings."""
    def __init__(self, prefix: str = "CLI_92_"):
        self._prefix = prefix
        self._cache: Dict[str, Any] = {}

    def __getattr__(self, name: str) -> Any:
        if name not in self._cache:
            self._cache[name] = os.getenv(f"{self._prefix}{name.upper()}")
        return self._cache[name]

    @property
    def workspace(self) -> Path:
        return Path(os.getenv("CLI_WORKSPACE", "~/.cli-helper-92")).expanduser()

    def reset(self) -> None:
        self._cache.clear()

def get_settings() -> AppConfig:
    """Factory for config instance singleton."""
    if not hasattr(get_settings, "_instance"):
        get_settings._instance = AppConfig()
    return get_settings._instance

SETTINGS = get_settings()

def ensure_dirs() -> None:
    """Bootstrap directory structure for the app."""
    path = SETTINGS.workspace
    path.mkdir(parents=True, exist_ok=True)
    (path / "logs").mkdir(exist_ok=True)
    (path / "cache").mkdir(exist_ok=True)