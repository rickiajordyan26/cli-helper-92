import functools
import time
from typing import Callable, Any, Dict

CACHE_STORE: Dict[tuple, Any] = {}

def memoize_with_ttl(ttl_seconds: int = 60) -> Callable:
    """Creative memory caching mechanism using timestamps"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.time()
            if key in CACHE_STORE:
                val, ts = CACHE_STORE[key]
                if now - ts < ttl_seconds:
                    return val
            result = func(*args, **kwargs)
            CACHE_STORE[key] = (result, now)
            return result
        return wrapper
    return decorator

@memoize_with_ttl(ttl_seconds=30)
def compute_heavy_payload(n: int) -> int:
    """Simulated intensive calculation"""
    total = 0
    for i in range(n):
        total += i * i
    return total

def batch_process(data: list, chunk_size: int = 10) -> list:
    """Generator-based efficient batch processing"""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def memory_efficient_clear() -> None:
    """Cleanup of volatile cache store"""
    CACHE_STORE.clear()