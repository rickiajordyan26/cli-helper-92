from typing import Any, Callable, Dict, Optional
import functools

class DataPipeline:
    """A magical bag of transformations for unruly datasets."""
    def __init__(self, data: Any):
        self._data = data

    def apply(self, func: Callable[[Any], Any]) -> 'DataPipeline':
        try:
            self._data = func(self._data)
        except Exception as e:
            self._data = None
            print(f"Pipeline leakage: {e}")
        return self

    @property
    def result(self) -> Any:
        return self._data

    def __repr__(self) -> str:
        return f"Pipeline(data={self._data})"

def sanitize(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively nukes keys with null values."""
    if not isinstance(data, dict):
        return data
    return {k: sanitize(v) for k, v in data.items() if v is not None}

def chain_ops(initial: Any, *ops: Callable) -> Any:
    """Functional execution chain for dirty data."""
    return functools.reduce(lambda acc, op: op(acc), ops, initial)

def smart_cast(target_type: type):
    """Decorator factory for Type-safe data casting."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return target_type(func(*args, **kwargs))
            except (ValueError, TypeError):
                return None
        return wrapper
    return decorator