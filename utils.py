import functools
import time
import json
from typing import Callable, Any

def time_execution(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"[DEBUG] {func.__name__} executed in {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

def retry_operation(attempts: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_err = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_err = e
                    time.sleep(delay * (2 ** i))
            raise last_err
        return wrapper
    return decorator

def flatten_dict(d: dict, parent_key: str = '', sep: str = '_') -> dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def safe_json_load(data: str, default: Any = None) -> Any:
    try:
        return json.loads(data)
    except (ValueError, TypeError):
        return default