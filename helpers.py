import functools
import logging
from typing import Callable, Any

logger = logging.getLogger('cli-helper-92')

class EdgeCaseError(Exception):
    """Custom exception for unpredictable CLI runtime states."""
    pass

def robust_execution(func: Callable):
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, KeyError) as e:
            logger.error(f"Data anomaly in {func.__name__}: {e}")
            return None
        except Exception as e:
            logger.critical(f"Unrecoverable chaos in {func.__name__}: {e}")
            raise EdgeCaseError(f"Failed during {func.__name__}") from e
    return wrapper

def safe_dict_get(data: dict, key: str, default: Any = None) -> Any:
    try:
        return data.get(key, default) if data else default
    except AttributeError:
        logger.warning(f"Invalid object type passed to safe_get: {type(data)}")
        return default

def sanitize_input(value: Any) -> str:
    if not isinstance(value, (str, int, float)):
        return str(value or '')
    return str(value).strip()