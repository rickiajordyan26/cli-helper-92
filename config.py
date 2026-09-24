import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], path: str = 'config.json'):
        self.path = path
        self.data = defaults
        self.load()

    def load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    self.data.update(json.load(f))
            except (json.JSONDecodeError, IOError):
                pass

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name)

    def save(self, key: str, value: Any) -> None:
        self.data[key] = value
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

def get_config(defaults: Dict[str, Any]) -> ConfigLoader:
    return ConfigLoader(defaults)

if __name__ == '__main__':
    # usage example: dynamic config object with defaults
    cfg = get_config({'timeout': 30, 'verbose': False})
    print(f'current timeout: {cfg.timeout}')