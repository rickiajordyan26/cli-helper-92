import functools
import sys
import logging

logger = logging.getLogger('cli-helper-92')

class EdgeCaseHandler:
    """Context manager/decorator for non-standard operational recovery."""
    def __init__(self, recovery_map=None):
        self.recovery_map = recovery_map or {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_type = type(e)
                if error_type in self.recovery_map:
                    logger.warning(f"Triggering edge case recovery for {error_type.__name__}")
                    return self.recovery_map[error_type](e)
                raise e
        return wrapper

def silent_fallback(func):
    """Swallow failures, return None, and log as debug output."""
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, KeyError) as e:
            logger.debug(f"Silent failure on {func.__name__}: {e}")
            return None
    return inner

def robust_map(data, transform_func):
    """Process sequence, filtering errors into a secondary registry."""
    results = []
    errors = []
    for item in data:
        try:
            results.append(transform_func(item))
        except Exception as err:
            errors.append({'item': item, 'reason': str(err)})
    return results, errors