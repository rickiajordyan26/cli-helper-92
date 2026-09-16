import os
import json
from typing import Any, Dict

class FallbackConfig:
    """
    A dynamic configuration loader resolving keys in sequence:
    1. Environment variables (prefixed with CLI_HELPER_)
    2. Local configuration JSON file
    3. Default fallbacks
    Coerces environment variable values to match the type of the default values.
    """
    def __init__(self, filepath: str, defaults: Dict[str, Any]):
        self._filepath = filepath
        self._defaults = defaults
        self._file_config = self._load_file()

    def _load_file(self) -> Dict[str, Any]:
        if os.path.exists(self._filepath):
            try:
                with open(self._filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return {}

    def __getattr__(self, name: str) -> Any:
        key = name.lower()
        if key not in self._defaults:
            raise AttributeError(f"Configuration option '{name}' is undefined.")

        default_val = self._defaults[key]
        env_key = f"CLI_HELPER_{name.upper()}"

        if env_key in os.environ:
            raw_val = os.environ[env_key]
            try:
                if isinstance(default_val, bool):
                    return raw_val.lower() in ('true', '1', 'yes', 'on')
                if isinstance(default_val, int):
                    return int(raw_val)
                if isinstance(default_val, float):
                    return float(raw_val)
                return raw_val
            except ValueError:
                return default_val

        if key in self._file_config:
            return self._file_config[key]

        return default_val

    def export_defaults(self) -> None:
        try:
            with open(self._filepath, 'w', encoding='utf-8') as f:
                json.dump(self._defaults, f, indent=4)
        except OSError as e:
            raise IOError(f"Could not write default configuration template: {e}")