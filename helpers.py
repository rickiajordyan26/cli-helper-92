import time
import functools
import random
from typing import Callable, Any

def retry_with_backoff(max_attempts: int = 3, initial_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempts = 0
            delay = initial_delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    sleep_time = delay * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

def resilient_network_request(task: Callable):
    return retry_with_backoff(max_attempts=5, initial_delay=0.5)(task)

# Example usage:
# @resilient_network_request
# def fetch_data():
#     print('Fetching...')
#     raise ConnectionError('Network flap')
