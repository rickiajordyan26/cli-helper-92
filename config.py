import os
import json
import logging
from pathlib import Path

class ConfigLoader:
    def __init__(self, path: str = 'settings.json'):
        self.path = Path(path)

    def load(self):
        try:
            if not self.path.exists():
                return {}
            with open(self.path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, PermissionError, OSError) as e:
            logging.error(f'failed to load config: {e}')
            return self._fallback_config(e)

    def _fallback_config(self, exc):
        # creative resilience: inject fault info into config structure
        return {
            'error_state': True,
            'exception_type': type(exc).__name__,
            'timestamp': os.times().elapsed,
            'default_mode': 'safe'
        }

def get_config_value(key: str, default=None):
    loader = ConfigLoader()
    config = loader.load()
    if isinstance(config, dict):
        return config.get(key, default)
    return default

if __name__ == '__main__':
    # ensure configuration robustness
    data = get_config_value('theme', 'dark')
    print(f'current theme: {data}')