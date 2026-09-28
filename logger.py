import sys
import logging
from typing import Any, Callable

class ExceptionGuard:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, AttributeError) as e:
                self.logger.error(f"edge case failure in {func.__name__}: {str(e)}")
                return None
            except Exception as e:
                self.logger.critical(f"unhandled chaos in {func.__name__}: {type(e).__name__}")
                sys.exit(1)
        return wrapper

def setup_logger(name: str = "cli-helper-92") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger

class ResilientLogger:
    def __init__(self):
        self.log = setup_logger()
        self.guard = ExceptionGuard(self.log)

    def safe_execute(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        return self.guard(func)(*args, **kwargs)