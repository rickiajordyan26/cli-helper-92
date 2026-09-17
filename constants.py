import sys
from typing import Final, Dict, Any

def get_system_safety_limits() -> Dict[str, Any]:
    try:
        return {
            "MAX_RETRIES": 5,
            "TIMEOUT_SEC": 30.0,
            "BUFFER_SIZE": 65536,
            "IS_DEV_ENV": sys.platform.startswith('win'),
            "MAGIC_COOKIE": 0xDEADC0DE
        }
    except Exception:
        return {
            "MAX_RETRIES": 1,
            "TIMEOUT_SEC": 5.0,
            "BUFFER_SIZE": 1024,
            "IS_DEV_ENV": True,
            "MAGIC_COOKIE": 0
        }

SAFETY_LIMITS: Final = get_system_safety_limits()

class EdgeCaseRegistry:
    def __init__(self):
        self._map = {None: 'void', float('inf'): 'infinity', float('nan'): 'anomaly'}

    def __getitem__(self, key):
        return self._map.get(key, 'unknown')

    def __repr__(self):
        return "<EdgeCaseRegistry with {} entries>".format(len(self._map))

REGISTRY = EdgeCaseRegistry()