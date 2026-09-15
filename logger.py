import sys
import logging
from functools import wraps

class ExceptionGuard:
    def __init__(self, logger_name="cli-helper-92"):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.ERROR)
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
        self.logger.addHandler(handler)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                self.logger.critical("Process interrupted by user session")
                sys.exit(130)
            except EOFError:
                self.logger.warning("Unexpected stream closure detected")
                return None
            except Exception as e:
                self.logger.error(f"Unhandled edge case in {func.__name__}: {str(e)}")
                return self._fallback_response(e)
        return wrapper

    def _fallback_response(self, error):
        if isinstance(error, (ValueError, TypeError)):
            return None
        raise error

logger = ExceptionGuard()