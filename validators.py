import functools
import logging
from typing import Callable, Any, TypeVar, ParamSpec

P = ParamSpec('P')
R = TypeVar('R')

class ValidationError(Exception):
    pass

def robust_validator(default_fallback: Any = None) -> Callable[[Callable[P, R]], Callable[P, R | Any]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R | Any]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | Any:
            try:
                return func(*args, **kwargs)
            except (TypeError, ValueError, AttributeError, KeyError) as e:
                logging.error(f'Edge case detected in {func.__name__}: {e}')
                if default_fallback is not None:
                    return default_fallback
                raise ValidationError(f'Invalid state in {func.__name__}') from e
        return wrapper
    return decorator

@robust_validator(default_fallback=False)
def is_non_empty_string(value: Any) -> bool:
    if not isinstance(value, str):
        raise TypeError('Not a string')
    return len(value.strip()) > 0

@robust_validator(default_fallback=0)
def safe_index_lookup(data: list, index: int) -> Any:
    return data[index]

def validate_payload(data: dict, required_keys: list[str]) -> bool:
    return all(is_non_empty_string(data.get(k)) for k in required_keys)