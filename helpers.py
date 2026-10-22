import json
from typing import Any, Dict, List, Union, Optional
from functools import reduce

def deep_fetch(data: Union[Dict, List], path: str, default: Any = None) -> Any:
    """
    Navigates a nested structure using dot notation keys.
    Example: deep_fetch(data, 'user.profile.id')
    """
    keys = path.split('.')
    try:
        return reduce(lambda d, k: d[int(k)] if isinstance(d, list) else d.get(k), keys, data)
    except (KeyError, TypeError, IndexError, ValueError):
        return default

def sanitize_payload(payload: Dict[str, Any], keys_to_scrub: List[str]) -> Dict[str, Any]:
    """
    Recursively purges sensitive keys from a dictionary.
    """
    if not isinstance(payload, dict):
        return payload
    
    return {
        k: ('***' if k in keys_to_scrub else sanitize_payload(v, keys_to_scrub))
        for k, v in payload.items()
    }

def batch_process(items: List[Any], chunk_size: int = 10):
    """
    Yields successive chunks from a list.
    """
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

def stringify_if_json(data: Any) -> str:
    """
    Attempts to serialize complex objects as json.
    """
    if isinstance(data, (dict, list)):
        return json.dumps(data, sort_keys=True)
    return str(data)