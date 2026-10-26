import functools
from typing import Any, Callable, Dict, Optional

def cast_structure(mapping: Dict[str, type]):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            if not isinstance(data, dict):
                return data
            return {k: v(data.get(k)) if k in data and v else data.get(k) for k, v in mapping.items()}
        return wrapper
    return decorator

def shape_enforcer(required_keys: list):
    def wrapper(func: Callable):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            if not all(key in result for key in required_keys):
                raise ValueError(f"missing keys: {set(required_keys) - set(result.keys())}")
            return result
        return inner
    return wrapper

def sanitizer(cleaner: Callable[[Any], Any]):
    def wrapper(func: Callable):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            raw = func(*args, **kwargs)
            if isinstance(raw, list):
                return [cleaner(i) for i in raw]
            return cleaner(raw)
        return inner
    return wrapper