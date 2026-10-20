import json
from typing import Any, Dict, Union

class DataTransformer:
    """A magical portal for heterogeneous data structures."""
    def __init__(self, data: Union[str, Dict[str, Any]]):
        self.raw = json.loads(data) if isinstance(data, str) else data

    def dive(self, path: str, default: Any = None) -> Any:
        keys = path.split('.')
        cursor = self.raw
        try:
            for key in keys:
                if isinstance(cursor, list):
                    cursor = cursor[int(key)]
                else:
                    cursor = cursor.get(key)
            return cursor if cursor is not None else default
        except (KeyError, IndexError, ValueError, TypeError):
            return default

    def flatten(self, prefix: str = '', sep: str = '_') -> Dict[str, Any]:
        items = {}
        for k, v in self.raw.items():
            new_key = f"{prefix}{sep}{k}" if prefix else k
            if isinstance(v, dict):
                items.update(DataTransformer(v).flatten(new_key, sep))
            else:
                items[new_key] = v
        return items

    def serialize(self, indent: int = 2) -> str:
        return json.dumps(self.raw, indent=indent)

def sanitize_data(data: Any) -> Any:
    """Recursive cleansing of types for clean export."""
    if isinstance(data, dict):
        return {str(k): sanitize_data(v) for k, v in data.items()}
    if isinstance(data, (list, tuple, set)):
        return [sanitize_data(i) for i in data]
    return data if isinstance(data, (str, int, float, bool)) else str(data)