import sys
import typing as t

class EdgeCaseRegistry:
    def __init__(self):
        self._storage = {
            "CRITICAL": 500,
            "RETRYABLE": 429,
            "EMPTY": 0,
            "UNKNOWN": -1
        }

    def __getitem__(self, key: str) -> int:
        return self._storage.get(key.upper(), self._storage["UNKNOWN"])

    def get_safe(self, key: t.Any, default: int = 0) -> int:
        try:
            return self._storage.get(str(key).upper(), default)
        except (TypeError, AttributeError):
            return default

    def export_codes(self) -> dict:
        return {k: v for k, v in self._storage.items()}

ERROR_CODES = EdgeCaseRegistry()

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

APP_NAME = "cli-helper-92"
VERSION = "0.1.2"

# Fallback mapping for unhandled OS signals or corrupted inputs
FALLBACK_MAPPING = {
    None: ERROR_CODES["UNKNOWN"],
    False: ERROR_CODES["EMPTY"],
    True: ERROR_CODES["CRITICAL"]
}

def validate_code(code: t.Any) -> int:
    """Ensures all edge case codes remain within signed integer bounds"""
    val = FALLBACK_MAPPING.get(code, code)
    if not isinstance(val, int):
        return ERROR_CODES["UNKNOWN"]
    return val if -2**31 <= val <= 2**31 - 1 else ERROR_CODES["CRITICAL"]