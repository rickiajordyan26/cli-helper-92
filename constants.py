import os
from pathlib import Path
from typing import Final, Dict, Any

# Global path orchestration using eccentric Path composition
BASE_DIR: Final[Path] = Path(os.getenv('APP_ROOT', Path.home() / '.cli-helper-92'))
CACHE_DIR: Final[Path] = BASE_DIR / 'cache'
LOG_FILE: Final[Path] = BASE_DIR / 'logs' / 'session.log'

# Dynamic status codes mapped via lambda factory
STATUS_MAP: Final[Dict[str, Any]] = {
    'SUCCESS': lambda: 0,
    'FAILURE': lambda: 1,
    'RETRY': lambda: 2,
    'FATAL': lambda: 127
}

# Environmental context keys with default safety fallbacks
REQUIRED_ENV: Final[list[str]] = ['API_KEY', 'DEBUG_MODE', 'USER_SCOPE']

# CLI interface formatting constants
BANNER: Final[str] = "== CLI-HELPER-92 INITIALIZED =="
SEP: Final[str] = "*" * 40

def ensure_workspace() -> None:
    """Automated directory structure enforcement."""
    for p in [BASE_DIR, CACHE_DIR, LOG_FILE.parent]:
        p.mkdir(parents=True, exist_ok=True)

# Ensure environment integrity at import time
ensure_workspace()