import functools
import time
from typing import Callable, Any

class CoreEngine:
    def __init__(self):
        self._cache = {}
        self._stats = {'hits': 0, 'misses': 0}

    def memoize_with_ttl(ttl: int = 60):
        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = (func.__name__, args, frozenset(kwargs.items()))
                now = time.time()
                if key in self._cache:
                    val, ts = self._cache[key]
                    if now - ts < ttl:
                        self._stats['hits'] += 1
                        return val
                
                result = func(*args, **kwargs)
                self._cache[key] = (result, now)
                self._stats['misses'] += 1
                return result
            return wrapper
        return decorator

    def process_heavy_payload(self, data: list):
        return sum(self._transform(x) for x in data)

    @memoize_with_ttl(ttl=30)
    def _transform(self, x: int) -> int:
        # Simulated expensive computation
        time.sleep(0.1)
        return x * x

    def get_metrics(self):
        total = self._stats['hits'] + self._stats['misses']
        if total == 0: return 0.0
        return self._stats['hits'] / total