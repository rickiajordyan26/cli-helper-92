import functools
import logging
import time
from typing import Callable, Any

def time_execution(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logging.getLogger('cli-helper-92').info(f'{func.__name__} finished in {elapsed:.4f}s')
        return result
    return wrapper

class Registry:
    def __init__(self):
        self._storage = {}

    def register(self, key: str):
        def decorator(cls):
            self._storage[key] = cls
            return cls
        return decorator

    def fetch(self, key: str) -> Any:
        return self._storage.get(key)

def sanitize_input(data: str) -> str:
    return ''.join(c for c in data if c.isalnum() or c in [' ', '_', '-']).strip()

def batch_process(items: list, chunk_size: int = 10):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

def retry_operation(attempts: int = 3, delay: float = 1.0):
    def decorator(func):
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