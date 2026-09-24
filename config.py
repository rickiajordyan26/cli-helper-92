import os
from typing import Dict, Any, Optional

class ConfigLoader:
    """Handles environment-based configuration for cli-helper-92."""

    def __init__(self, prefix: str = "CLI_92_") -> None:
        self.prefix: str = prefix
        self._cache: Dict[str, Any] = {}

    def fetch(self, key: str, default: Optional[Any] = None) -> Any:
        """Retrieve config value with environment override logic."""
        env_var: str = f"{self.prefix}{key.upper()}"
        return os.getenv(env_var, self._cache.get(key, default))

    def update_cache(self, mapping: Dict[str, Any]) -> None:
        """Inject external dictionary into configuration layer."""
        self._cache.update(mapping)

    def purge(self) -> None:
        """Clear internal volatile configuration storage."""
        self._cache = {}

def get_default_config() -> Dict[str, str]:
    """Factory for base application settings."""
    return {
        "version": "0.9.2",
        "mode": "development",
        "path": os.getcwd()
    }