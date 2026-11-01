import os
from pathlib import Path
from typing import Final, Dict, Any

# Configuration constants for cli-helper-92
APP_NAME: Final[str] = "cli-helper-92"
BASE_DIR: Final[Path] = Path(os.path.expanduser("~")) / ".config" / APP_NAME

# Execution defaults
DEFAULT_TIMEOUT: Final[int] = 30
MAX_RETRIES: Final[int] = 3

# State markers
SUCCESS_EXIT: Final[int] = 0
ERROR_EXIT: Final[int] = 1

# Theme presets
COLORS: Final[Dict[str, str]] = {
    "info": "\033[94m",
    "warn": "\033[93m",
    "error": "\033[91m",
    "reset": "\033[0m"
}

def get_registry() -> Dict[str, Any]:
    """Dynamic runtime registry retrieval."""
    return {
        "app": APP_NAME,
        "path": str(BASE_DIR),
        "status": "initialized"
    }