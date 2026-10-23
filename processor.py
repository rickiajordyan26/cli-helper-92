import functools
import time
import json
from typing import Callable, Any

def memoize_with_expiry(ttl_seconds: int = 60):
    def decorator(func: Callable):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in cache and (now - cache[key]['ts']) < ttl_seconds:
                return cache[key]['val']
            result = func(*args, **kwargs)
            cache[key] = {'val': result, 'ts': now}
            return result
        return wrapper
    return decorator

def deep_flatten(items: list) -> list:
    flat = []
    for item in items:
        if isinstance(item, list):
            flat.extend(deep_flatten(item))
        else:
            flat.append(item)
    return flat

def serialize_safe(data: Any) -> str:
    try:
        return json.dumps(data)
    except (TypeError, ValueError):
        return str(data)

def pipeline(*functions: Callable):
    def executor(data: Any):
        return functools.reduce(lambda acc, f: f(acc), functions, data)
    return executor

if __name__ == '__main__':
    double = lambda x: x * 2
    add_ten = lambda x: x + 10
    process = pipeline(double, add_ten)
    print(f'Pipeline output: {process(5)}')