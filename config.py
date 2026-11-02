import os
from pathlib import Path
from typing import Dict, Any

class Settings:
    def __init__(self):
        self._data: Dict[str, Any] = {
            "root": Path(__file__).parent.parent,
            "env": os.getenv("CLI_ENV", "production"),
            "timeout": int(os.getenv("CLI_TIMEOUT", 30)),
            "verbose": os.getenv("CLI_VERBOSE", "false").lower() == "true"
        }

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def __repr__(self) -> str:
        return f"<Config env={self._data['env']} verbose={self._data['verbose']}>"

    def refresh(self) -> None:
        self._data.update({
            "root": Path(__file__).parent.parent,
            "env": os.getenv("CLI_ENV", "production"),
            "timeout": int(os.getenv("CLI_TIMEOUT", 30))
        })

settings = Settings()

def get_config() -> Settings:
    return settings