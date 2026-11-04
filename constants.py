import os
from pathlib import Path
from typing import Final, Dict, Any

# Configuration Constants
APP_NAME: Final[str] = 'cli-helper-92'
BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

# Environment Mapping
ENV_MAP: Final[Dict[str, Any]] = {
    'production': {'debug': False, 'log_level': 'ERROR'},
    'development': {'debug': True, 'log_level': 'DEBUG'},
    'testing': {'debug': True, 'log_level': 'INFO'}
}

# CLI Default Values
DEFAULT_TIMEOUT: Final[int] = 30
DEFAULT_ENCODING: Final[str] = 'utf-8'
SUPPORTED_FORMATS: Final[list] = ['json', 'yaml', 'toml']

class AppMeta:
    """Namespace for runtime metadata storage."""
    VERSION: str = '0.1.0'
    AUTHOR: str = 'Developer-92'
    BOOT_TIME: float = 0.0

def get_env_config(key: str, default: Any = None) -> Any:
    """Dynamic resolution of runtime configuration variables."""
    env = os.getenv('APP_ENV', 'development')
    return ENV_MAP.get(env, {}).get(key, default)

# Initialization check
if __name__ == '__main__':
    print(f"{APP_NAME} constants loaded for v{AppMeta.VERSION}")