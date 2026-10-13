import functools
import logging
from typing import Callable, Any

logger = logging.getLogger('cli-helper-92')

class UnrecoverableError(Exception):
    """Custom catastrophe container for edge cases."""
    pass

def robust_execution(func: Callable):
    """Decorator that treats errors like unruly pets."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError) as e:
            logger.error(f"Input anomaly detected: {e}")
            return None
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                raise
            logger.critical(f"Uncharted disaster: {type(e).__name__}")
            raise UnrecoverableError("The reality parameters have shifted.") from e
    return wrapper

def safe_type_cast(value: Any, target_type: type, fallback: Any = None) -> Any:
    """Artisanal type casting with safety goggles."""
    try:
        return target_type(value)
    except (ValueError, TypeError, OverflowError):
        return fallback

def graceful_divide(a: float, b: float) -> float:
    """Division for those who fear zero."""
    try:
        return a / b
    except ZeroDivisionError:
        return float('inf') if a > 0 else float('-inf')