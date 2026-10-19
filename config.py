import json
import os
from pathlib import Path
from typing import Any, Dict, Union

DEFAULT_CONFIG: Dict[str, Any] = {
    "app_name": "cli-helper-92",
    "debug": False,
    "verbose": True,
    "timeout": 30,
    "output_format": "json",
    "theme": {"primary": "cyan", "secondary": "magenta"},
}

class ConfigBox:
    """A wrapper providing attribute access and deep dictionary conversion."""

    def __init__(self, data: Dict[str, Any]):
        for key, val in data.items():
            if isinstance(val, dict):
                setattr(self, key, ConfigBox(val))
            else:
                setattr(self, key, val)

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for k, v in self.__dict__.items():
            result[k] = v.to_dict() if isinstance(v, ConfigBox) else v
        return result

def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> None:
    for k, v in override.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v

def _apply_env_overrides(cfg: Dict[str, Any], prefix: str, path_prefix: str = "") -> None:
    for k, v in cfg.items():
        env_key = f"{prefix}{path_prefix}{k}".upper()
        if isinstance(v, dict):
            _apply_env_overrides(v, prefix, f"{path_prefix}{k}_")
        elif env_key in os.environ:
            raw_val = os.environ[env_key]
            cfg[k] = _cast_value(raw_val, type(v))

def _cast_value(val: str, target_type: type) -> Any:
    if target_type is bool:
        return val.lower() in ("true", "1", "yes", "on")
    try:
        return target_type(val)
    except (ValueError, TypeError):
        return val

def load_config(
    config_path: Union[str, Path] = "config.json",
    env_prefix: str = "CLI_HELPER_",
) -> ConfigBox:
    merged = DEFAULT_CONFIG.copy()
    path = Path(config_path)
    if path.is_file():
        try:
            with path.open("r", encoding="utf-8") as f:
                _deep_merge(merged, json.load(f))
        except json.JSONDecodeError:
            pass
    _apply_env_overrides(merged, env_prefix)
    return ConfigBox(merged)
