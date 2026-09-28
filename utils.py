import time
import functools
import random

def retry(max_attempts=3, delay=1, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tries, current_delay = max_attempts, delay
            while tries > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    tries -= 1
                    if tries == 0:
                        raise e
                    time.sleep(current_delay + random.uniform(0, 0.1))
                    current_delay *= backoff
        return wrapper
    return decorator

def network_request_executor(url, fetch_func):
    @retry(max_attempts=4, delay=0.5)
    def operation():
        return fetch_func(url)
    return operation()