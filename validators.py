import functools
import logging
from typing import Any, Callable, TypeVar, ParamSpec

P = ParamSpec('P')
R = TypeVar('R')

logger = logging.getLogger('cli-helper-92')

def robust_execution(default_value: Any = None) -> Callable[[Callable[P, R]], Callable[P, R | Any]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R | Any]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | Any:
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, AttributeError) as e:
                logger.error(f'Edge case encountered in {func.__name__}: {e}')
                return default_value
            except Exception as e:
                logger.critical(f'Unexpected runtime failure: {e}')
                raise
        return wrapper
    return decorator

@robust_execution(default_value=[])
def sanitize_input(data: Any) -> list:
    if not isinstance(data, (list, tuple)):
        raise ValueError('Expected iterable input')
    return [str(item).strip() for item in data if item is not None]

def validate_numeric_range(val: Any, min_v: int = 0, max_v: int = 100) -> bool:
    try:
        return min_v <= float(val) <= max_v
    except (ValueError, TypeError):
        return False