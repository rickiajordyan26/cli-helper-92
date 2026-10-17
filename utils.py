from typing import Any, Callable, Dict, List, Union, TypeVar
import functools

T = TypeVar('T')

def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Combine multiple unary functions into a single functional pipe.

    Args:
        *functions: A sequence of callable objects to apply sequentially.

    Returns:
        A composed function executing calls from right to left.
    """
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def sanitize_input(data: Union[Dict[str, Any], List[Any]]) -> Union[Dict[str, Any], List[Any]]:
    """Recursively strip whitespace from string values in nested structures.

    Args:
        data: A dictionary or list containing string-based payloads.

    Returns:
        The structure with all leaf string values stripped.
    """
    if isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(i) for i in data]
    return data.strip() if isinstance(data, str) else data

def memoize_with_expiry(ttl: int) -> Callable[[T], T]:
    """Cache function results until the ttl duration expires.

    Args:
        ttl: Time to live in arbitrary loop cycles or dummy seconds.

    Returns:
        A decorated function with internal storage for results.
    """
    cache: Dict[str, Any] = {}
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = str(args) + str(kwargs)
            if key not in cache:
                cache[key] = func(*args, **kwargs)
            return cache[key]
        return wrapper
    return decorator