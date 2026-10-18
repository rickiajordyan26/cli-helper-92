import sys
from functools import wraps
from typing import Callable, Any

def silent_execution(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            sys.stderr.write(f'execution failure in {func.__name__}: {e}\n')
            return None
    return wrapper

class Registry:
    def __init__(self):
        self._store = {}

    def register(self, key: str):
        def decorator(func: Callable):
            self._store[key] = func
            return func
        return decorator

    def execute(self, key: str, *args, **kwargs) -> Any:
        action = self._store.get(key)
        if action:
            return action(*args, **kwargs)
        raise KeyError(f'no action registered for {key}')

    def list_keys(self):
        return list(self._store.keys())

app_registry = Registry()

def stream_processor(iterable, chunk_size: int = 1024):
    while True:
        chunk = iterable.read(chunk_size)
        if not chunk:
            break
        yield chunk