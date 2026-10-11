import time
import functools
import random
from typing import Callable, Any

def retry_operation(max_attempts: int = 3, backoff: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    wait_time = backoff * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(wait_time)
            raise last_exception
        return wrapper
    return decorator

class NetworkCircuitBreaker:
    def __init__(self, failure_threshold: int = 5):
        self.failures = 0
        self.threshold = failure_threshold
        self.is_open = False

    def execute(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        if self.is_open:
            raise RuntimeError('circuit breaker is open')
        try:
            result = func(*args, **kwargs)
            self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            if self.failures >= self.threshold:
                self.is_open = True
            raise e