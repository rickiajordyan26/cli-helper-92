import time
import functools
import random

def resilient_network_call(max_retries=3, base_delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_retries:
                        raise e
                    # Exponential backoff with jitter for chaos prevention
                    sleep_time = (base_delay * (2 ** (attempts - 1))) + random.uniform(0, 1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

def execute_with_fallback(func, fallback_value=None):
    """Run function and swallow exceptions to return fallback."""
    try:
        return func()
    except Exception:
        return fallback_value