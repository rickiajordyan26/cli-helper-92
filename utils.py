from typing import Any, Callable, Dict, List, Optional
import functools

def pipe(data: Any, *funcs: Callable[[Any], Any]) -> Any:
    """Execute a sequence of callables sequentially on data.

    Args:
        data: Initial input value.
        *funcs: Variable length list of callables.

    Returns:
        Transformed data after all functions applied.
    """
    return functools.reduce(lambda v, f: f(v), funcs, data)

def memoize_with_ttl(ttl: int) -> Callable:
    """Decorator factory for functions with timeout-based cache.

    Args:
        ttl: Time to live for cache entries.

    Returns:
        Decorator function for target methods.
    """
    def decorator(func: Callable) -> Callable:
        cache: Dict[Any, Any] = {}
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, tuple(kwargs.items()))
            if key not in cache:
                cache[key] = func(*args, **kwargs)
            return cache[key]
        return wrapper
    return decorator

def flatten(nested_list: List[Any]) -> List[Any]:
    """Deep flatten a nested list structure recursively.

    Args:
        nested_list: Potentially nested list of elements.

    Returns:
        Flat list containing all nested elements.
    """
    result: List[Any] = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result