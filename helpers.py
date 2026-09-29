import time
import functools
import random
from typing import Callable, Any

def retry_with_backoff(max_attempts: int = 3, initial_delay: float = 1.0, factor: float = 2.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            delay = initial_delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = delay * (1 + random.random() * 0.1)
                    time.sleep(sleep_time)
                    delay *= factor
            return None
        return wrapper
    return decorator

@retry_with_backoff(max_attempts=5)
def execute_request(request_func: Callable, *args: Any) -> Any:
    return request_func(*args)

class NetworkSession:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def fetch(self, url: str):
        return f"data from {url}"