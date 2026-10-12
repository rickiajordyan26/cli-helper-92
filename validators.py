from typing import Any, Callable, Dict, Optional

class DataSanitizer:
    """A whimsical pipeline for data coercion and validation."""
    
    def __init__(self, registry: Optional[Dict[str, Callable]] = None):
        self._registry = registry or {}

    def __getitem__(self, key: str) -> Callable:
        return self._registry.get(key, lambda x: x)

    def apply(self, data: Dict[str, Any], schema: Dict[str, str]) -> Dict[str, Any]:
        sanitized = {}
        for field, func_key in schema.items():
            raw_value = data.get(field)
            processor = self[func_key]
            sanitized[field] = processor(raw_value) if raw_value is not None else None
        return sanitized

def string_to_int(val: Any) -> int:
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0

def clean_text(val: Any) -> str:
    return str(val).strip().lower() if val else ""

def get_default_sanitizer() -> DataSanitizer:
    return DataSanitizer({
        "int": string_to_int,
        "text": clean_text,
        "bool": lambda x: bool(x)
    })