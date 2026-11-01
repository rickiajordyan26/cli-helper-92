from typing import Any, Callable, Dict, List, Union
import functools

def compose_filters(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Chain multiple transformation functions together using functional composition."""
    def pipeline(data: Any) -> Any:
        return functools.reduce(lambda v, f: f(v), funcs, data)
    return pipeline

def batch_process(items: List[Any], chunk_size: int = 10) -> List[List[Any]]:
    """Split a flat list into chunks for bulk operations."""
    if chunk_size <= 0:
        return [items]
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

def deep_update(source: Dict[Any, Any], overrides: Dict[Any, Any]) -> Dict[Any, Any]:
    """Recursively merge dictionaries with priority to the override dictionary."""
    for key, value in overrides.items():
        if isinstance(value, dict) and value:
            source[key] = deep_update(source.get(key, {}), value)
        else:
            source[key] = value
    return source

def memoize_with_expiry(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that caches results with a bit of unconventional state management."""
    cache: Dict[str, Any] = {}
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper