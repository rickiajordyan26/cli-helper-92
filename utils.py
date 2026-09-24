import functools
import time
import json
from typing import Callable, Any

def time_execution(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"[DEBUG] {func.__name__} took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

def safe_json_load(data: str, default: dict = None) -> dict:
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default or {}

def memoize_with_expiry(ttl: int = 60):
    cache = {}
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any) -> Any:
            now = time.time()
            if args in cache:
                val, timestamp = cache[args]
                if now - timestamp < ttl:
                    return val
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator

def chunk_list(data: list, size: int):
    return [data[i:i + size] for i in range(0, len(data), size)]