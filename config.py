import os
from typing import Any, Dict, Callable

class EnvDefault:
    """Descriptor that resolves values from environment variables or fallbacks dynamically."""
    def __init__(self, default: Any, cast_type: type = str):
        self.default = default
        self.cast_type = cast_type
        self.name = ""

    def __set_name__(self, owner: Any, name: str):
        self.name = name

    def __get__(self, instance: Any, owner: Any) -> Any:
        env_key = f"CLI_HELPER_{self.name.upper()}"
        val = os.environ.get(env_key)
        if val is not None:
            try:
                if self.cast_type is bool:
                    return val.lower() in ("true", "1", "yes", "on")
                return self.cast_type(val)
            except (ValueError, TypeError):
                pass

        resolved = self.default() if callable(self.default) else self.default
        if resolved is not None and not isinstance(resolved, self.cast_type):
            return self.cast_type(resolved)
        return resolved

class Config:
    """Configuration schema defining defaults with environment variable overrides."""
    DEBUG = EnvDefault(False, bool)
    PORT = EnvDefault(8080, int)
    APP_DIR = EnvDefault(os.getcwd, str)
    API_VERSION = EnvDefault("v1", str)

    @classmethod
    def load_from_dict(cls, data: Dict[str, Any]):
        """Injects external dictionary values into environment for dynamic reloading."""
        for key, value in data.items():
            os.environ[f"CLI_HELPER_{key.upper()}"] = str(value)

    @classmethod
    def export(cls) -> Dict[str, Any]:
        """Exports all resolved configuration values as a flat dictionary."""
        return {
            key: getattr(cls, key)
            for key, val in cls.__dict__.items()
            if isinstance(val, EnvDefault)
        }