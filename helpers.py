import os
import json
from typing import Any, Callable

def path_resolver(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))

def memoize_file(filepath: str, func: Callable) -> Any:
    cache_path = path_resolver(filepath)
    if os.path.exists(cache_path):
        with open(cache_path, 'r') as f:
            return json.load(f)
    result = func()
    with open(cache_path, 'w') as f:
        json.dump(result, f)
    return result

def flatten_dict(d: dict, parent_key: str = '', sep: str = '_') -> dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def env_fallback(key: str, default: Any = None) -> Any:
    return os.environ.get(key, default)

def retry_execution(retries: int = 3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
            raise last_ex
        return wrapper
    return decorator