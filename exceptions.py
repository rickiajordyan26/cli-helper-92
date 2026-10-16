import time
import functools
from typing import Callable, Any

class TransientNetworkError(Exception):
    pass

def retry_with_backoff(max_attempts: int = 3, initial_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            delay = initial_delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (TransientNetworkError, ConnectionError) as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    time.sleep(delay)
                    delay *= 2
            return None
        return wrapper
    return decorator

def execute_with_rescue(action: Callable, *args, **kwargs) -> Any:
    strategy = retry_with_backoff()(action)
    return strategy(*args, **kwargs)

class NetworkCircuitBreaker:
    def __init__(self, failure_threshold: int = 5):
        self.failures = 0
        self.limit = failure_threshold
    
    def __call__(self, func: Callable):
        def proxy(*args, **kwargs):
            if self.failures >= self.limit:
                raise RuntimeError('Circuit broken: too many failures')
            try:
                result = func(*args, **kwargs)
                self.failures = 0
                return result
            except Exception as e:
                self.failures += 1
                raise e
        return proxy