import functools
import logging
import sys

logger = logging.getLogger('cli-helper-92')

class EdgeCaseManager:
    def __init__(self, fallback_value=None):
        self.fallback = fallback_value

    def sanitize_execution(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, ZeroDivisionError) as e:
                logger.warning(f"graceful recovery from {type(e).__name__}: {e}")
                return self.fallback
            except Exception as e:
                logger.critical(f"unexpected system halt: {e}")
                sys.exit(1)
        return wrapper

def resilient_execute(data, action_func):
    """Attempts to run action on data, returning fallback on failure."""
    handler = EdgeCaseManager(fallback_value="[ERROR_HANDLED]")
    
    @handler.sanitize_execution
    def process():
        if not isinstance(data, (list, dict, str)):
            raise TypeError("invalid data type input")
        return action_func(data)

    return process()