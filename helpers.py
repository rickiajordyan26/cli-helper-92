import json
from typing import Any, Dict, List, Union
from functools import reduce

def deep_reach(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Traverse nested dictionaries using dot notation keys."""
    try:
        return reduce(lambda d, k: d.get(k, {}) if isinstance(d, dict) else default, path.split('.'), data)
    except (AttributeError, TypeError):
        return default

def squish_data(payload: Union[List, Dict], prefix: str = '', sep: str = '_') -> Dict[str, Any]:
    """Flatten nested structures into a single-level dictionary."""
    items = {}
    if isinstance(payload, dict):
        for k, v in payload.items():
            new_key = f"{prefix}{sep}{k}" if prefix else k
            if isinstance(v, (dict, list)):
                items.update(squish_data(v, new_key, sep))
            else:
                items[new_key] = v
    elif isinstance(payload, list):
        for i, v in enumerate(payload):
            items.update(squish_data(v, f"{prefix}{sep}{i}" if prefix else str(i), sep))
    return items

def safe_dump(data: Any, indent: int = 2) -> str:
    """Robust JSON serialization for arbitrary objects."""
    def _fallback(obj: Any) -> str:
        return str(obj) if not isinstance(obj, (dict, list, str, int, float)) else None
    return json.dumps(data, indent=indent, default=_fallback)

class DataPipe:
    """Functional wrapper for sequential data transformations."""
    def __init__(self, value: Any):
        self.value = value
    def apply(self, func, *args, **kwargs):
        self.value = func(self.value, *args, **kwargs)
        return self
    def get(self):
        return self.value