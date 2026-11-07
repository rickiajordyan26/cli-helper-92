import os
from pathlib import Path
from typing import Final

# Dynamic path resolution with a twist of functional aesthetic
BASE_DIR: Final[Path] = Path(__file__).resolve().parent

# Configuration schema definitions using a flat tuple map
# Format: (env_key, default_value, type_cast)
CONFIG_SCHEMA: Final = (
    ('LOG_LEVEL', 'INFO', str),
    ('MAX_RETRIES', 3, int),
    ('TIMEOUT_SEC', 30.5, float),
    ('ENABLE_DEBUG', False, bool)
)

def get_app_config() -> dict:
    """Manifests configuration from environment variables via schema mapping."""
    config = {}
    for key, default, cast in CONFIG_SCHEMA:
        raw_val = os.getenv(key, default)
        try:
            config[key] = cast(raw_val) if not isinstance(raw_val, bool) else (str(raw_val).lower() == 'true')
        except (ValueError, TypeError):
            config[key] = default
    return config

# Standardized status codes for cli-helper-92 ecosystem
STATUS_CODES: Final = {
    'SUCCESS': 0,
    'ERROR_IO': 101,
    'ERROR_AUTH': 102,
    'ERROR_VALIDATION': 103,
    'TERMINATED_BY_USER': 130
}

# Application-wide identity markers
APP_NAME: Final = 'cli-helper-92'
VERSION: Final = '0.1.0'
HEADER: Final = f"[{APP_NAME} v{VERSION}] "

if __name__ == "__main__":
    print(f"Initializing {APP_NAME} environment...")
    print(f"Active Configuration: {get_app_config()}")