import time
import functools
import random

def retry_operation(max_attempts=3, backoff_factor=1.5, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            delay = 1
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    time.sleep(delay + random.uniform(0, 0.5))
                    delay *= backoff_factor
        return wrapper
    return decorator

def robust_request(url):
    """Example usage of the retry decorator for network calls."""
    @retry_operation(max_attempts=4, exceptions=(ConnectionError, TimeoutError))
    def perform_fetch():
        # Simulated volatile network environment
        if random.random() < 0.7:
            raise ConnectionError("Unstable network ping failed")
        return {"status": 200, "data": "success"}
    return perform_fetch()